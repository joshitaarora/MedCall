import React, { useEffect, useRef } from 'react';
import { FileText } from 'lucide-react';
import './TranscriptView.css';

function TranscriptView({ transcript }) {
  const transcriptEndRef = useRef(null);

  useEffect(() => {
    // Auto-scroll to bottom when new transcript arrives
    transcriptEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [transcript]);

  return (
    <div className="transcript-view">
      <div className="transcript-header">
        <FileText size={24} />
        <h2>Live Transcript</h2>
        <div className="transcript-count">{transcript.length} entries</div>
      </div>

      <div className="transcript-container">
        {transcript.length === 0 ? (
          <div className="no-transcript">
            <FileText size={48} color="#d1d5db" />
            <p>No transcript yet</p>
            <p className="sub-text">Start recording to see live transcription</p>
          </div>
        ) : (
          <div className="transcript-list">
            {transcript.map((entry, index) => (
              <div key={index} className="transcript-entry">
                <div className="entry-header">
                  <div className={`speaker-badge ${entry.speaker}`}>
                    {entry.speaker === 'user' ? '👤 Patient' : '🎧 Call'}
                  </div>
                  <div className="entry-timestamp">
                    {new Date(entry.timestamp).toLocaleTimeString()}
                  </div>
                </div>
                <div className="entry-text">
                  {entry.text}
                </div>
              </div>
            ))}
            <div ref={transcriptEndRef} />
          </div>
        )}
      </div>
    </div>
  );
}

export default TranscriptView;
