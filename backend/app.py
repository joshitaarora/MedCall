"""
MedCall Backend - Live Call Monitoring with Parallel AI Agents
Hackathon Project for Healthcare Call Analysis
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import json
import threading
from datetime import datetime
from agents.ae_detector import AdverseEventDetector
from agents.appointment_agent import AppointmentAgent
from agents.emergency_detector import EmergencyDetector
from agents.sentiment_analyzer import SentimentMismatchAnalyzer
from audio.processor import AudioProcessor

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-api-key-here')

# Initialize agents
ae_detector = AdverseEventDetector(OPENAI_API_KEY)
appointment_agent = AppointmentAgent(OPENAI_API_KEY)
emergency_detector = EmergencyDetector(OPENAI_API_KEY)
sentiment_analyzer = SentimentMismatchAnalyzer(OPENAI_API_KEY)
audio_processor = AudioProcessor(OPENAI_API_KEY)

# Store active sessions
active_sessions = {}

class CallSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.transcript = []
        self.alerts = []
        self.start_time = datetime.now()
        self.is_active = True
        
    def add_transcript(self, text, speaker="user"):
        self.transcript.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": speaker,
            "text": text
        })
        
    def add_alert(self, alert_type, message, severity, action=None):
        alert = {
            "timestamp": datetime.now().isoformat(),
            "type": alert_type,
            "message": message,
            "severity": severity,
            "action": action
        }
        self.alerts.append(alert)
        return alert


def process_audio_chunk_parallel(session_id, audio_data, transcript_text):
    """Process audio chunk with all agents in parallel"""
    session = active_sessions.get(session_id)
    if not session:
        return
    
    session.add_transcript(transcript_text)
    
    results = {}
    threads = []
    
    # Create threads for parallel processing
    def run_ae_detection():
        results['ae'] = ae_detector.analyze(transcript_text, session.transcript)
    
    def run_appointment_check():
        results['appointment'] = appointment_agent.analyze(transcript_text, session.transcript)
    
    def run_emergency_check():
        results['emergency'] = emergency_detector.analyze(transcript_text, session.transcript)
    
    def run_sentiment_analysis():
        results['sentiment'] = sentiment_analyzer.analyze(transcript_text, audio_data, session.transcript)
    
    # Start all agents in parallel
    threads = [
        threading.Thread(target=run_ae_detection),
        threading.Thread(target=run_appointment_check),
        threading.Thread(target=run_emergency_check),
        threading.Thread(target=run_sentiment_analysis)
    ]
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Process results and emit alerts
    handle_analysis_results(session_id, results)


def handle_analysis_results(session_id, results):
    """Handle results from parallel agents and emit alerts"""
    session = active_sessions.get(session_id)
    if not session:
        return
    
    # Adverse Event Detection
    if results.get('ae') and results['ae']['detected']:
        alert = session.add_alert(
            'adverse_event',
            results['ae']['message'],
            'high',
            results['ae'].get('action')
        )
        socketio.emit('alert', alert, room=session_id)
    
    # Appointment Issues
    if results.get('appointment') and results['appointment']['issue_detected']:
        alert = session.add_alert(
            'appointment',
            results['appointment']['message'],
            'medium',
            results['appointment'].get('suggested_action')
        )
        socketio.emit('alert', alert, room=session_id)
    
    # Emergency Detection
    if results.get('emergency') and results['emergency']['is_emergency']:
        alert = session.add_alert(
            'emergency',
            results['emergency']['message'],
            'critical',
            results['emergency'].get('action')
        )
        socketio.emit('alert', alert, room=session_id)
    
    # Sentiment Mismatch (potential danger)
    if results.get('sentiment') and results['sentiment']['mismatch_detected']:
        alert = session.add_alert(
            'sentiment_mismatch',
            results['sentiment']['message'],
            'high',
            results['sentiment'].get('action')
        )
        socketio.emit('alert', alert, room=session_id)
    
    # Send transcript update
    socketio.emit('transcript_update', {
        'text': session.transcript[-1]['text'],
        'timestamp': session.transcript[-1]['timestamp']
    }, room=session_id)


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
    if session_id in active_sessions:
        # Join the room for this session
        emit('joined', {'session_id': session_id})


@socketio.on('audio_chunk')
def handle_audio_chunk(data):
    """Handle incoming audio chunks for real-time processing"""
    session_id = data.get('session_id')
    audio_data = data.get('audio')
    
    if session_id not in active_sessions:
        emit('error', {'message': 'Invalid session'})
        return
    
    # Transcribe audio
    transcript_text = audio_processor.transcribe(audio_data)
    
    if transcript_text:
        # Process with parallel agents in background thread
        threading.Thread(
            target=process_audio_chunk_parallel,
            args=(session_id, audio_data, transcript_text)
        ).start()


if __name__ == '__main__':
    print("🏥 MedCall Backend Starting...")
    print(f"📡 WebSocket server ready for real-time call monitoring")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
