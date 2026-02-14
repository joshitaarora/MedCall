import React, { useState } from 'react';
import axios from 'axios';
import { Play, Square, Radio } from 'lucide-react';
import './SessionControl.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function SessionControl({ onSessionStart, onSessionStop, isActive, sessionId }) {
  const [loading, setLoading] = useState(false);

  const startSession = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/session/start`, {
        session_id: `session_${Date.now()}`
      });
      
      onSessionStart(response.data.session_id);
    } catch (error) {
      console.error('Failed to start session:', error);
      alert('Failed to start session. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const stopSession = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/session/${sessionId}/stop`);
      
      onSessionStop();
      
      // Show session summary
      alert(`Session Summary:\nDuration: ${Math.round(response.data.duration)}s\nTotal Alerts: ${response.data.total_alerts}`);
    } catch (error) {
      console.error('Failed to stop session:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="session-control">
      <div className="session-header">
        <h2>Session Control</h2>
        {isActive && (
          <div className="status-indicator">
            <Radio className="pulse" size={20} color="#10b981" />
            <span>LIVE</span>
          </div>
        )}
      </div>

      <div className="session-info">
        {sessionId ? (
          <div className="info-row">
            <span className="label">Session ID:</span>
            <span className="value">{sessionId}</span>
          </div>
        ) : (
          <p className="info-text">Start a new monitoring session to begin</p>
        )}
      </div>

      <div className="session-actions">
        {!isActive ? (
          <button 
            className="btn btn-start" 
            onClick={startSession}
            disabled={loading}
          >
            <Play size={20} />
            {loading ? 'Starting...' : 'Start Monitoring'}
          </button>
        ) : (
          <button 
            className="btn btn-stop" 
            onClick={stopSession}
            disabled={loading}
          >
            <Square size={20} />
            {loading ? 'Stopping...' : 'Stop Session'}
          </button>
        )}
      </div>

      <div className="agent-status">
        <h3>Active Agents</h3>
        <div className="agent-grid">
          <div className={`agent-card ${isActive ? 'active' : ''}`}>
            <div className="agent-icon">⚠️</div>
            <div className="agent-name">AE Detector</div>
          </div>
          <div className={`agent-card ${isActive ? 'active' : ''}`}>
            <div className="agent-icon">📅</div>
            <div className="agent-name">Appointment Agent</div>
          </div>
          <div className={`agent-card ${isActive ? 'active' : ''}`}>
            <div className="agent-icon">🚨</div>
            <div className="agent-name">Emergency Detector</div>
          </div>
          <div className={`agent-card ${isActive ? 'active' : ''}`}>
            <div className="agent-icon">🎭</div>
            <div className="agent-name">Sentiment Analyzer</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SessionControl;
