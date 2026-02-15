"""
MedCall Backend - Live Call Monitoring with Parallel AI Agents
Hackathon Project for Healthcare Call Analysis
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
from dotenv import load_dotenv
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from agents.ae_detector import AdverseEventDetector
from agents.appointment_agent import AppointmentAgent
from agents.emergency_detector import EmergencyDetector
from agents.sentiment_analyzer import SentimentMismatchAnalyzer
from audio.processor import AudioProcessor

load_dotenv() 

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in .env file")

# Initialize agents
ae_detector = AdverseEventDetector(OPENAI_API_KEY)
appointment_agent = AppointmentAgent(OPENAI_API_KEY)
emergency_detector = EmergencyDetector(OPENAI_API_KEY)
sentiment_analyzer = SentimentMismatchAnalyzer(OPENAI_API_KEY)
audio_processor = AudioProcessor(OPENAI_API_KEY)

# Store active sessions
active_sessions = {}

class CallSession:
    ALERT_COOLDOWN_SECONDS = 30

    def __init__(self, session_id):
        self.session_id = session_id
        self.transcript = []
        self.alerts = []
        self.start_time = datetime.now()
        self.is_active = True
        self._last_alert_time = {}  # alert_type -> datetime
        
    def add_transcript(self, text, speaker="user"):
        self.transcript.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": speaker,
            "text": text
        })
        
    def can_emit_alert(self, alert_type):
        last = self._last_alert_time.get(alert_type)
        if last is None:
            return True
        return (datetime.now() - last).total_seconds() >= self.ALERT_COOLDOWN_SECONDS

    def add_alert(self, alert_type, message, severity, action=None):
        alert = {
            "timestamp": datetime.now().isoformat(),
            "type": alert_type,
            "message": message,
            "severity": severity,
            "action": action
        }
        self.alerts.append(alert)
        self._last_alert_time[alert_type] = datetime.now()
        return alert


def process_audio_chunk_parallel(session_id, audio_data, transcript_text):
    """Process audio with all agents in parallel using gpt-4o-mini"""
    session = active_sessions.get(session_id)
    if not session:
        print(f"❌ Session {session_id} not found in processing!")
        return

    session.add_transcript(transcript_text)
    print(f"🚀 Running 3 agents in parallel for: {transcript_text[:80]}...")

    try:
        agent_tasks = {
            'ae':          lambda: ae_detector.analyze(transcript_text, session.transcript),
            'appointment': lambda: appointment_agent.analyze(transcript_text, session.transcript),
            'emergency':   lambda: emergency_detector.analyze(transcript_text, session.transcript),
        }

        results = {}
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(fn): key for key, fn in agent_tasks.items()}
            for future in as_completed(futures):
                key = futures[future]
                try:
                    results[key] = future.result()
                    print(f"✅ {key} agent done")
                except Exception as e:
                    print(f"❌ {key} agent error: {e}")
                    results[key] = {"detected": False, "issue_detected": False, "is_emergency": False, "error": str(e)}

        print("✅ All agents complete — emitting results")
        handle_analysis_results(session_id, results)
    except Exception as e:
        print(f"❌ CRITICAL ERROR in processing: {e}")
        import traceback
        traceback.print_exc()


def handle_analysis_results(session_id, results):
    """Handle results from parallel agents and emit alerts"""
    print(f"\n{'='*50}")
    print(f"📊 HANDLING ANALYSIS RESULTS")
    print(f"Session: {session_id}")
    print(f"Results keys: {list(results.keys())}")
    print(f"{'='*50}\n")
    
    session = active_sessions.get(session_id)
    if not session:
        print(f"❌ Session not found in handle_analysis_results!")
        return
    
    alerts_emitted = 0
    
    # Adverse Event Detection
    ae_result = results.get('ae', {})
    if ae_result and ae_result.get('detected') and session.can_emit_alert('adverse_event'):
        try:
            alert = session.add_alert(
                'adverse_event',
                ae_result.get('message', 'Adverse event detected'),
                'high',
                ae_result.get('recommended_action')
            )
            socketio.emit('alert', alert)
            alerts_emitted += 1
            print("✅ AE Alert emitted!")
        except Exception as e:
            print(f"❌ Error emitting AE alert: {e}")
    elif ae_result and ae_result.get('detected'):
        print("⏳ AE alert suppressed (cooldown)")

    # Appointment Issues
    appt_result = results.get('appointment', {})
    if appt_result and appt_result.get('issue_detected') and session.can_emit_alert('appointment'):
        try:
            alert = session.add_alert(
                'appointment',
                appt_result.get('message', 'Appointment issue detected'),
                'medium',
                appt_result.get('suggested_action')
            )
            socketio.emit('alert', alert)
            alerts_emitted += 1
            print("✅ Appointment Alert emitted!")
        except Exception as e:
            print(f"❌ Error emitting appointment alert: {e}")
    elif appt_result and appt_result.get('issue_detected'):
        print("⏳ Appointment alert suppressed (cooldown)")

    # Emergency Detection
    emerg_result = results.get('emergency', {})
    if emerg_result and emerg_result.get('is_emergency') and session.can_emit_alert('emergency'):
        try:
            alert = session.add_alert(
                'emergency',
                emerg_result.get('message', 'Emergency detected'),
                'critical',
                emerg_result.get('action')
            )
            socketio.emit('alert', alert)
            alerts_emitted += 1
            print("✅ Emergency Alert emitted!")
        except Exception as e:
            print(f"❌ Error emitting emergency alert: {e}")
    elif emerg_result and emerg_result.get('is_emergency'):
        print("⏳ Emergency alert suppressed (cooldown)")
    

    # Send transcript update
    print("📝 Emitting transcript update...")
    socketio.emit('transcript_update', {
        'text': session.transcript[-1]['text'],
        'timestamp': session.transcript[-1]['timestamp']
    })
    print("✅ Transcript update emitted!")
    
    print(f"\n{'='*50}")
    print(f"✅ ANALYSIS COMPLETE - {alerts_emitted} alert(s) emitted")
    print(f"{'='*50}\n")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "MedCall Backend"})


@app.route('/api/session/start', methods=['POST'])
def start_session():
    """Start a new call monitoring session"""
    session_id = request.json.get('session_id', str(datetime.now().timestamp()))
    
    session = CallSession(session_id)
    active_sessions[session_id] = session
    
    return jsonify({
        "session_id": session_id,
        "status": "active",
        "start_time": session.start_time.isoformat()
    })


@app.route('/api/session/<session_id>/stop', methods=['POST'])
def stop_session(session_id):
    """Stop a call monitoring session"""
    session = active_sessions.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404
    
    session.is_active = False
    
    summary = {
        "session_id": session_id,
        "duration": (datetime.now() - session.start_time).total_seconds(),
        "total_alerts": len(session.alerts),
        "alerts_by_type": {},
        "transcript_length": len(session.transcript)
    }
    
    for alert in session.alerts:
        alert_type = alert['type']
        summary['alerts_by_type'][alert_type] = summary['alerts_by_type'].get(alert_type, 0) + 1
    
    return jsonify(summary)


@app.route('/api/session/<session_id>/alerts', methods=['GET'])
def get_alerts(session_id):
    """Get all alerts for a session"""
    session = active_sessions.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404
    
    return jsonify({"alerts": session.alerts})


@app.route('/api/session/<session_id>/transcript', methods=['GET'])
def get_transcript(session_id):
    """Get full transcript for a session"""
    session = active_sessions.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404
    
    return jsonify({"transcript": session.transcript})


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connection_response', {'status': 'connected'})


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('join_session')
def handle_join_session(data):
    session_id = data.get('session_id')
    print(f"\n{'='*50}")
    print(f"🔗 JOIN SESSION REQUEST")
    print(f"Session ID: {session_id}")
    print(f"Socket ID: {request.sid}")
    print(f"{'='*50}\n")
    
    if session_id in active_sessions:
        print(f"✅ Session found, joining room...")
        # Join the room for this session - THIS IS CRITICAL!
        from flask_socketio import join_room
        join_room(session_id)
        print(f"✅ Joined room: {session_id}")
        emit('joined', {'session_id': session_id})
        print(f"✅ Sent 'joined' confirmation")
    else:
        print(f"❌ Session {session_id} not found!")
        print(f"Available sessions: {list(active_sessions.keys())}")


@socketio.on('audio_chunk')
def handle_audio_chunk(data):
    """Handle incoming audio chunks for real-time processing"""
    print("=" * 50)
    print("🎤 AUDIO CHUNK RECEIVED!")
    print("=" * 50)
    
    session_id = data.get('session_id')
    audio_data = data.get('audio')
    
    print(f"Session ID: {session_id}")
    print(f"Audio data type: {type(audio_data)}")
    print(f"Audio data size: {len(audio_data) if audio_data else 0} bytes")
    
    if session_id not in active_sessions:
        print(f"❌ ERROR: Session {session_id} not found!")
        print(f"Available sessions: {list(active_sessions.keys())}")
        emit('error', {'message': 'Invalid session'})
        return
    
    print("✅ Session found, starting transcription...")
    
    # Transcribe audio
    try:
        transcript_text = audio_processor.transcribe(audio_data)
        print(f"📝 Transcription result: '{transcript_text}'")  # ADD THIS
        print(f"📝 Transcription type: {type(transcript_text)}")  # ADD THIS
        print(f"📝 Transcription length: {len(transcript_text) if transcript_text else 0}")  # ADD THIS
    except Exception as e:
        print(f"❌ TRANSCRIPTION ERROR: {e}")  # ADD THIS
        import traceback
        traceback.print_exc()  # ADD THIS
        return
    
    # Require at least 15 meaningful characters to avoid noise/silence/Whisper hallucinations
    if transcript_text and len(transcript_text.strip()) >= 15:
        print("✅ Starting parallel agent analysis...")
        socketio.start_background_task(
            process_audio_chunk_parallel,
            session_id, audio_data, transcript_text
        )
    else:
        print(f"⚠️ Skipping analysis - transcript too short or empty: '{transcript_text}'")
        # Still append to transcript so the UI shows the text
        if transcript_text and transcript_text.strip():
            session = active_sessions.get(session_id)
            if session:
                session.add_transcript(transcript_text.strip())
                socketio.emit('transcript_update', {
                    'text': transcript_text.strip(),
                    'timestamp': datetime.now().isoformat()
                })


if __name__ == '__main__':
    print("🏥 MedCall Backend Starting...")
    print(f"📡 WebSocket server ready for real-time call monitoring")
    port = int(os.getenv('PORT', 5001))
    print(f"🚀 Running on port {port}")
    socketio.run(app, debug=True, host='0.0.0.0', port=port, use_reloader=False)
