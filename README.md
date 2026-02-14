# MedCall - AI-Powered Healthcare Call Monitoring 🏥

[![Hackathon Project](https://img.shields.io/badge/TreeHacks-2026-blue)](https://treehacks.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

MedCall is an innovative healthcare call monitoring system that uses parallel AI agents to analyze live conversations in real-time. Built for TreeHacks 2026, it helps identify adverse events, scheduling conflicts, emergencies, and potential danger through audio-sentiment mismatch analysis.

## 🌟 Features

### Parallel AI Agents

1. **Adverse Event (AE) Detector** ⚠️
   - Identifies medication side effects and treatment complications
   - Detects allergic reactions and unexpected medical issues
   - Provides severity assessment and recommended actions

2. **Appointment Agent** 📅
   - Detects missed appointments and scheduling conflicts
   - Suggests next steps for rescheduling
   - Identifies follow-up needs

3. **Emergency Detector** 🚨
   - Recognizes life-threatening situations
   - Detects urgent health concerns
   - Provides immediate action recommendations

4. **Sentiment Mismatch Analyzer** 🎭
   - Analyzes audio-content discrepancies
   - Detects potential danger situations (e.g., coercion, distress)
   - Identifies hidden emergencies

## 🚀 Tech Stack

### Backend
- **Python 3.8+** with Flask
- **OpenAI API** (GPT-4 + Whisper)
- **Flask-SocketIO** for real-time communication
- **Threading** for parallel agent execution

### Frontend
- **React 18**
- **Socket.io Client** for WebSocket connections
- **Web Audio API** for microphone access
- **Responsive design** with custom CSS

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- OpenAI API key

### Backend Setup

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy environment file
Copy-Item .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your-actual-api-key-here
```

### Frontend Setup

```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment file
Copy-Item .env.example .env

# The default values should work for local development
```

## 🎯 Usage

### Starting the Backend

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python app.py
```

The backend will start on `http://localhost:5000`

### Starting the Frontend

```powershell
cd frontend
npm start
```

The frontend will start on `http://localhost:3000`

### Using the Application

1. **Start a Session**
   - Click "Start Monitoring" to create a new call session
   - All four AI agents will be activated in parallel

2. **Begin Recording**
   - Click "Start Recording" in the Call Monitor
   - Grant microphone permissions when prompted
   - Speak naturally - the system will transcribe and analyze in real-time

3. **Monitor Alerts**
   - Alerts appear in real-time on the Alert Dashboard
   - Color-coded by severity: Critical (red), High (orange), Medium (yellow)
   - Each alert includes recommended actions

4. **View Transcript**
   - Live transcription appears as you speak
   - Auto-scrolls to show latest content

5. **End Session**
   - Stop recording when done
   - Click "Stop Session" to end monitoring
   - View session summary with alert statistics

## 🏗️ Project Structure

```
MedCall/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── ae_detector.py           # Adverse event detection
│   │   ├── appointment_agent.py     # Appointment management
│   │   ├── emergency_detector.py    # Emergency identification
│   │   └── sentiment_analyzer.py    # Sentiment-content mismatch
│   ├── audio/
│   │   ├── __init__.py
│   │   └── processor.py             # Whisper transcription
│   ├── app.py                       # Main Flask application
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── SessionControl.js    # Session management
│   │   │   ├── CallMonitor.js       # Audio recording & visualization
│   │   │   ├── AlertDashboard.js    # Alert display
│   │   │   └── TranscriptView.js    # Live transcript
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── .env.example
└── README.md
```

## 🔧 Configuration

### Backend Environment Variables

```env
OPENAI_API_KEY=your-openai-api-key-here
FLASK_ENV=development
DEBUG=True
HOST=0.0.0.0
PORT=5000
```

### Frontend Environment Variables

```env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_SOCKET_URL=http://localhost:5000
```

## 🎨 Key Features Explained

### Parallel Processing
All four AI agents run simultaneously using Python threading, ensuring:
- Fast response times
- No blocking operations
- Real-time analysis

### Real-time Communication
WebSocket connection provides:
- Instant alert notifications
- Live transcript updates
- Bi-directional communication

### Audio Processing
- **Whisper API** for accurate transcription
- **MediaRecorder API** for audio capture
- **Audio visualization** with level meters
- Chunked processing every 3 seconds

## 🔒 Privacy & Security

- Audio data is processed in real-time and not stored permanently
- All communications use WebSocket for secure transmission
- API keys stored in environment variables
- Patient data handled according to HIPAA guidelines (production deployment)

## 🚧 Future Enhancements

- [ ] Advanced audio analysis (pitch, tone, stress detection)
- [ ] Integration with EHR systems
- [ ] Multi-language support
- [ ] Voice authentication
- [ ] Automated reporting and documentation
- [ ] Mobile application
- [ ] Dashboard analytics and insights
- [ ] Historical call playback

## 📝 API Endpoints

### REST API

- `GET /health` - Health check
- `POST /api/session/start` - Start new session
- `POST /api/session/:id/stop` - Stop session
- `GET /api/session/:id/alerts` - Get all alerts
- `GET /api/session/:id/transcript` - Get full transcript

### WebSocket Events

**Client → Server:**
- `join_session` - Join a session room
- `audio_chunk` - Send audio data

**Server → Client:**
- `alert` - New alert detected
- `transcript_update` - New transcript entry
- `connection_response` - Connection confirmation

## 🤝 Contributing

This is a hackathon project, but contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

MIT License - feel free to use this code for your own projects!

## 👥 Team

Built for TreeHacks 2026

## 🙏 Acknowledgments

- OpenAI for GPT-4 and Whisper APIs
- TreeHacks for the inspiration
- Healthcare professionals for domain expertise

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Contact the development team

---

**Note:** Replace `your-openai-api-key-here` with your actual OpenAI API key before running the application.

**Disclaimer:** This is a proof-of-concept developed for a hackathon. For production use in healthcare settings, ensure compliance with HIPAA, GDPR, and other relevant regulations.