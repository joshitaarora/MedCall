import React, { useEffect, useRef } from 'react';
import { FileText } from 'lucide-react';
import './TranscriptView.css';

function TranscriptView({ transcript }) {
  const transcriptEndRef = useRef(null);

  useEffect(() => {
    // Auto-scroll to bottom when new transcript arrives
    transcriptEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [transcript]);

  const fullText = transcript.map(e => e.text?.trim()).filter(Boolean).join(' ');

  return (
    <div className="transcript-view">
      <div className="transcript-header">
        <FileText size={24} />
        <h2>Live Transcript</h2>
      </div>

      <div className="transcript-container">
        {transcript.length === 0 ? (
          <div className="no-transcript">
            <FileText size={48} color="#d1d5db" />
            <p>No transcript yet</p>
            <p className="sub-text">Start recording to see live transcription</p>
          </div>
        ) : (
          <div className="transcript-text">
            {fullText}
            <div ref={transcriptEndRef} />
          </div>
        )}
      </div>
    </div>
  );
}

export default TranscriptView;
