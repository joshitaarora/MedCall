import React, { useState, useRef, useEffect } from 'react';
import io from 'socket.io-client';
import { Upload, File } from 'lucide-react';
import './AudioFileUpload.css';

const SOCKET_URL = process.env.REACT_APP_SOCKET_URL || 'http://localhost:5001';

function AudioFileUpload({ sessionId }) {
  const [uploading, setUploading] = useState(false);
  const [fileName, setFileName] = useState('');
  const socketRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    // Cleanup socket connection on component unmount
    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, []);

  const initializeSocket = () => {
    if (socketRef.current && socketRef.current.connected) {
      return; // Socket already connected
    }

    console.log('🔌 Initializing socket connection for file upload to:', SOCKET_URL);
    socketRef.current = io(SOCKET_URL, {
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5
    });
    
    socketRef.current.on('connect', () => {
      console.log('✅ Upload socket connected, Socket ID:', socketRef.current.id);
      console.log('📤 Sending join_session with sessionId:', sessionId);
      socketRef.current.emit('join_session', { session_id: sessionId });
    });

    socketRef.current.on('joined', (data) => {
      console.log('✅ Successfully joined session:', data);
    });

    socketRef.current.on('transcript_update', () => {
      setUploading(false);
    });

    socketRef.current.on('connect_error', (error) => {
      console.error('❌ Upload socket connection error:', error);
    });

    socketRef.current.on('error', (error) => {
      console.error('❌ Upload socket error:', error);
    });
  };

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
      initializeSocket();

      const reader = new FileReader();
      reader.onload = async (e) => {
        // Give socket time to connect if needed
        if (!socketRef.current.connected) {
          console.log('⏳ Waiting for socket to connect...');
          await new Promise(resolve => {
            socketRef.current.once('connect', resolve);
            setTimeout(resolve, 2000); // Timeout after 2s
          });
        }

        const base64Audio = e.target.result.split(',')[1];
        console.log('📤 Emitting audio_chunk with sessionId:', sessionId);
        socketRef.current.emit('audio_chunk', {
          session_id: sessionId,
          audio: base64Audio
        });
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
