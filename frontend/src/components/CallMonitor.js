import React, { useEffect, useRef, useState } from 'react';
import io from 'socket.io-client';
import { Mic, MicOff } from 'lucide-react';
import './CallMonitor.css';

const SOCKET_URL = process.env.REACT_APP_SOCKET_URL || 'http://localhost:5000';

function CallMonitor({ sessionId, onAlert, onTranscriptUpdate }) {
  const [isRecording, setIsRecording] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0);
  const socketRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);

  useEffect(() => {
    // Initialize socket connection
    socketRef.current = io(SOCKET_URL);

    socketRef.current.on('connect', () => {
      console.log('Connected to server');
      socketRef.current.emit('join_session', { session_id: sessionId });
    });

    socketRef.current.on('alert', (alert) => {
      console.log('🔔 Alert received:', alert);
      onAlert(alert);
    });

    socketRef.current.on('transcript_update', (update) => {
      console.log('📝 Transcript received:', update);
      onTranscriptUpdate(update);
    });

    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
      stopRecording();
    };
  }, [sessionId]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Setup audio visualization
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
      analyserRef.current = audioContextRef.current.createAnalyser();
      const source = audioContextRef.current.createMediaStreamSource(stream);
      source.connect(analyserRef.current);
      analyserRef.current.fftSize = 256;
      
      visualizeAudio();

      // Setup MediaRecorder
      const options = { mimeType: 'audio/webm' };
      mediaRecorderRef.current = new MediaRecorder(stream, options);
      
      const audioChunks = [];
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };

      // Send audio chunks periodically (every 3 seconds)
      let chunkInterval = setInterval(() => {
        if (audioChunks.length > 0) {
          const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
          audioChunks.length = 0; // Clear chunks
          
          // Convert to base64 and send to server
          const reader = new FileReader();
          reader.onloadend = () => {
            const base64Audio = reader.result.split(',')[1];
            socketRef.current.emit('audio_chunk', {
              session_id: sessionId,
              audio: base64Audio
            });
          };
          reader.readAsDataURL(audioBlob);
        }
      }, 3000);

      mediaRecorderRef.current.onstop = () => {
        clearInterval(chunkInterval);
        stream.getTracks().forEach(track => track.stop());
      };

      mediaRecorderRef.current.start(100); // Capture in 100ms chunks
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Unable to access microphone. Please grant permission.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
    }
  };

  const visualizeAudio = () => {
    if (!analyserRef.current) return;
    
    const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount);
    
    const updateLevel = () => {
      if (!isRecording) return;
      
      analyserRef.current.getByteFrequencyData(dataArray);
      const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
      setAudioLevel(average / 255 * 100);
      
      requestAnimationFrame(updateLevel);
    };
    
    updateLevel();
  };

  return (
    <div className="call-monitor">
      <div className="monitor-header">
        <h2>Call Monitor</h2>
        {isRecording && <span className="recording-badge">● RECORDING</span>}
      </div>

      <div className="monitor-content">
        <div className="audio-visualizer">
          <div className="visualizer-circle" style={{ 
            transform: `scale(${1 + audioLevel / 100})`,
            opacity: 0.3 + (audioLevel / 100) * 0.7
          }}>
            {isRecording ? <Mic size={48} color="#fff" /> : <MicOff size={48} color="#999" />}
          </div>
          
          <div className="audio-level-bar">
            <div 
              className="audio-level-fill" 
              style={{ width: `${audioLevel}%` }}
            ></div>
          </div>
        </div>

        <div className="monitor-controls">
          {!isRecording ? (
            <button className="btn-record" onClick={startRecording}>
              <Mic size={24} />
              Start Recording
            </button>
          ) : (
            <button className="btn-stop-record" onClick={stopRecording}>
              <MicOff size={24} />
              Stop Recording
            </button>
          )}
        </div>

        <div className="monitor-info">
          <p className="info-text">
            {isRecording 
              ? '🎤 Listening and analyzing in real-time with parallel AI agents...'
              : '🎙️ Click "Start Recording" to begin call monitoring'}
          </p>
        </div>
      </div>
    </div>
  );
}

export default CallMonitor;
