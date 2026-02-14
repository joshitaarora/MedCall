import React, { useState, useEffect } from 'react';
import './App.css';
import CallMonitor from './components/CallMonitor';
import AlertDashboard from './components/AlertDashboard';
import TranscriptView from './components/TranscriptView';
import SessionControl from './components/SessionControl';
import { Activity } from 'lucide-react';

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [isSessionActive, setIsSessionActive] = useState(false);
  const [alerts, setAlerts] = useState([]);
  const [transcript, setTranscript] = useState([]);

  const handleSessionStart = (newSessionId) => {
    setSessionId(newSessionId);
    setIsSessionActive(true);
    setAlerts([]);
    setTranscript([]);
  };

  const handleSessionStop = () => {
    setIsSessionActive(false);
  };

  const handleNewAlert = (alert) => {
    setAlerts(prev => [...prev, alert]);
  };

  const handleTranscriptUpdate = (entry) => {
    setTranscript(prev => [...prev, entry]);
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <Activity size={32} color="#fff" />
            <h1>MedCall</h1>
          </div>
          <p className="tagline">AI-Powered Healthcare Call Monitoring</p>
        </div>
      </header>

      <main className="app-main">
        <div className="content-grid">
          {/* Session Control */}
          <div className="session-section">
            <SessionControl
              onSessionStart={handleSessionStart}
              onSessionStop={handleSessionStop}
              isActive={isSessionActive}
              sessionId={sessionId}
            />
          </div>

          {/* Call Monitor */}
          {isSessionActive && (
            <div className="monitor-section">
              <CallMonitor
                sessionId={sessionId}
                onAlert={handleNewAlert}
                onTranscriptUpdate={handleTranscriptUpdate}
              />
            </div>
          )}

          {/* Alert Dashboard */}
          <div className="dashboard-section">
            <AlertDashboard alerts={alerts} />
          </div>

          {/* Transcript */}
          {isSessionActive && (
            <div className="transcript-section">
              <TranscriptView transcript={transcript} />
            </div>
          )}
        </div>
      </main>

      <footer className="app-footer">
        <p>Parallel AI Agents: AE Detection | Appointment Management | Emergency Detection | Sentiment Analysis</p>
      </footer>
    </div>
  );
}

export default App;
