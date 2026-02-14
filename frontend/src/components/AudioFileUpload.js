import React, { useState, useRef } from 'react';
import io from 'socket.io-client';
import { Upload, File } from 'lucide-react';
import './AudioFileUpload.css';

const SOCKET_URL = process.env.REACT_APP_SOCKET_URL || 'http://localhost:5001';

function AudioFileUpload({ sessionId, onAlert, onTranscriptUpdate }) {
  const [uploading, setUploading] = useState(false);
  const [fileName, setFileName] = useState('');
  const socketRef = useRef(null);
  const fileInputRef = useRef(null);

  const handleFileSelect = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const validTypes = ['audio/wav', 'audio/mp3', 'audio/mpeg', 'audio/webm', 'audio/m4a', 'audio/ogg'];
    if (!validTypes.includes(file.type) && !file.name.match(/\.(wav|mp3|webm|m4a|ogg)$/i)) {
      alert('Please upload a valid audio file (WAV, MP3, WEBM, M4A, OGG)');
      return;
    }

    setFileName(file.name);
    setUploading(true);

    try {
      if (!socketRef.current) {
        socketRef.current = io(SOCKET_URL);
        
        socketRef.current.on('connect', () => {
          console.log('Connected for file upload');
          socketRef.current.emit('join_session', { session_id: sessionId });
        });

        socketRef.current.on('alert', (alert) => {
          console.log('🔔 Alert received from upload:', alert);
          onAlert(alert);
        });

        socketRef.current.on('transcript_update', (update) => {
          console.log('📝 Transcript from upload:', update);
          onTranscriptUpdate(update);
        });
      }

      const reader = new FileReader();
      reader.onload = async (e) => {
        const base64Audio = e.target.result.split(',')[1];
        
        socketRef.current.emit('audio_chunk', {
          session_id: sessionId,
          audio: base64Audio
        });

        setTimeout(() => {
          setUploading(false);
          alert('Audio file processed! Check alerts and transcript.');
        }, 2000);
      };

      reader.readAsDataURL(file);

    } catch (error) {
      console.error('File upload error:', error);
      alert('Error processing audio file');
      setUploading(false);
    }
  };

  return (
    <div className="audio-file-upload">
      <h3>Upload Audio File for Testing</h3>
      
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileSelect}
        accept="audio/*"
        style={{ display: 'none' }}
      />

      <button
        className="btn-upload"
        onClick={() => fileInputRef.current.click()}
        disabled={uploading}
      >
        {uploading ? (
          <>
            <File size={20} className="spinning" />
            Processing {fileName}...
          </>
        ) : (
          <>
            <Upload size={20} />
            Upload Audio File
          </>
        )}
      </button>

      <p className="upload-info">
        Supports: WAV, MP3, M4A, WEBM, OGG
      </p>

      {fileName && !uploading && (
        <p className="upload-success">✅ Processed: {fileName}</p>
      )}
    </div>
  );
}

export default AudioFileUpload;
