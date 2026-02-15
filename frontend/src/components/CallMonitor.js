import React, { useEffect, useRef, useState } from 'react';
import io from 'socket.io-client';
import { Mic, MicOff, Loader } from 'lucide-react';
import './CallMonitor.css';

const SOCKET_URL = process.env.REACT_APP_SOCKET_URL || 'http://localhost:5001';

function CallMonitor({ sessionId, onAlert, onTranscriptUpdate }) {
  const [isRecording, setIsRecording] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0);
  const socketRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const streamRef = useRef(null);
  const isRecordingRef = useRef(false);

  useEffect(() => {
    socketRef.current = io(SOCKET_URL, {
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5
    });

    socketRef.current.on('connect', () => {
      console.log('✅ Socket connected:', socketRef.current.id);
      socketRef.current.emit('join_session', { session_id: sessionId });
    });

    socketRef.current.on('alert', (alert) => {
      console.log('🔔 Alert received:', alert);
      onAlert(alert);
    });

    socketRef.current.on('transcript_update', (update) => {
      console.log('📝 Transcript received:', update);
      onTranscriptUpdate(update);
      setIsAnalyzing(false);
    });

    socketRef.current.on('disconnect', () => console.log('❌ Socket disconnected'));
    socketRef.current.on('connect_error', (e) => console.error('❌ Socket error:', e));

    return () => {
      if (socketRef.current) socketRef.current.disconnect();
      stopRecording();
    };
  }, [sessionId]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      // Audio visualizer
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
      analyserRef.current = audioContextRef.current.createAnalyser();
      const source = audioContextRef.current.createMediaStreamSource(stream);
      source.connect(analyserRef.current);
      analyserRef.current.fftSize = 256;

      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : 'audio/webm';

      const recorder = new MediaRecorder(stream, { mimeType });
      mediaRecorderRef.current = recorder;
      const chunks = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunks.push(e.data);
      };

      recorder.onstop = () => {
        if (chunks.length > 0) {
          const blob = new Blob(chunks, { type: mimeType });
          const reader = new FileReader();
          reader.onloadend = () => {
            const base64Audio = reader.result.split(',')[1];
            socketRef.current?.emit('audio_chunk', {
              session_id: sessionId,
              audio: base64Audio
            });
            setIsAnalyzing(true);
          };
          reader.readAsDataURL(blob);
        }
      };

      recorder.start();
      isRecordingRef.current = true;
      setIsRecording(true);
      visualizeAudio();
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Unable to access microphone. Please grant permission.');
    }
  };

  const stopRecording = () => {
    isRecordingRef.current = false;
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
      audioContextRef.current.close();
    }
    audioContextRef.current = null;
    setIsRecording(false);
    setAudioLevel(0);
  };

  const visualizeAudio = () => {
    if (!analyserRef.current) return;
    const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount);
    const update = () => {
      if (!isRecordingRef.current) return;
      analyserRef.current.getByteFrequencyData(dataArray);
      const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
      setAudioLevel(average / 255 * 100);
      requestAnimationFrame(update);
    };
    update();
  };

  const statusText = () => {
    if (isAnalyzing) return '⏳ Analyzing with AI agents...';
    if (isRecording) return '🎤 Recording — press Stop when done';
    return '🎙️ Click "Start Recording" to begin';
  };

  return (
    <div className="call-monitor">
      <div className="monitor-header">
        <h2>Call Monitor</h2>
        {isRecording && <span className="recording-badge">● RECORDING</span>}
        {isAnalyzing && <span className="analyzing-badge">⏳ ANALYZING</span>}
      </div>

      <div className="monitor-content">
        <div className="audio-visualizer">
          <div className="visualizer-circle" style={{
            transform: `scale(${1 + audioLevel / 100})`,
            opacity: 0.3 + (audioLevel / 100) * 0.7
          }}>
            {isAnalyzing
              ? <Loader size={48} color="#667eea" className="spinning" />
              : isRecording
                ? <Mic size={48} color="#fff" />
                : <MicOff size={48} color="#999" />}
          </div>

          <div className="audio-level-bar">
            <div className="audio-level-fill" style={{ width: `${audioLevel}%` }} />
          </div>
        </div>

        <div className="monitor-controls">
          {!isRecording && !isAnalyzing && (
            <button className="btn-record" onClick={startRecording}>
              <Mic size={24} />
              Start Recording
            </button>
          )}
          {isRecording && (
            <button className="btn-stop-record" onClick={stopRecording}>
              <MicOff size={24} />
              Stop &amp; Analyze
            </button>
          )}
        </div>

        <div className="monitor-info">
          <p className="info-text">{statusText()}</p>
        </div>
      </div>
    </div>
  );
}

export default CallMonitor;
