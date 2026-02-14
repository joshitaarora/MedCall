# MedCall Project - Quick Reference Guide

## 🚀 Quick Start

### 1. Run Setup Script (Windows)
```powershell
.\setup.ps1
```

### 2. Add Your API Key
Edit `backend\.env` and replace:
```
OPENAI_API_KEY=your-openai-api-key-here
```

### 3. Start Backend
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python app.py
```

### 4. Start Frontend (New Terminal)
```powershell
cd frontend
npm start
```

## 🎯 How It Works

### Architecture Flow
```
Microphone → Audio Capture → Whisper (Transcription)
                                      ↓
                              Parallel AI Agents
              ┌─────────────────┬────────┴────────┬──────────────────┐
              ↓                 ↓                 ↓                  ↓
      AE Detector    Appointment Agent   Emergency Detector  Sentiment Analyzer
              │                 │                 │                  │
              └─────────────────┴────────┬────────┴──────────────────┘
                                         ↓
                                Alert Dashboard + Transcript
```

### Parallel Processing
- All 4 agents run simultaneously using Python threading
- No blocking - instant analysis
- Real-time WebSocket updates to frontend

## 🔧 Troubleshooting

### Backend Issues

**Port already in use:**
```powershell
# Change port in backend/.env
PORT=5001
```

**OpenAI API errors:**
- Check your API key is correct
- Ensure you have credits in your OpenAI account
- Verify internet connection

### Frontend Issues

**Cannot connect to backend:**
- Ensure backend is running on port 5000
- Check `REACT_APP_API_URL` in frontend/.env

**Microphone access denied:**
- Allow microphone permissions in browser
- Use HTTPS in production (required for mic access)

## 📊 Testing the Application

### Test Scenarios

**1. Test AE Detection:**
Say: "I've been having severe side effects from the medication - nausea and dizziness."

**2. Test Appointment:**
Say: "I missed my appointment yesterday and need to reschedule."

**3. Test Emergency:**
Say: "I'm having severe chest pain and difficulty breathing."

**4. Test Sentiment Mismatch:**
Say: "Everything is fine..." (in a distressed tone)
Context: The AI will analyze the conversation pattern for inconsistencies

## 🎨 Customization

### Adding New Agents

1. Create new agent in `backend/agents/your_agent.py`:
```python
class YourAgent:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def analyze(self, text, history):
        # Your logic here
        return result
```

2. Import in `backend/app.py`:
```python
from agents.your_agent import YourAgent
your_agent = YourAgent(OPENAI_API_KEY)
```

3. Add to parallel processing:
```python
def run_your_analysis():
    results['your_feature'] = your_agent.analyze(text, history)

threads.append(threading.Thread(target=run_your_analysis))
```

### Modifying Agent Behavior

Edit the prompts in each agent file:
- `agents/ae_detector.py` - Line ~25
- `agents/appointment_agent.py` - Line ~25
- `agents/emergency_detector.py` - Line ~25
- `agents/sentiment_analyzer.py` - Line ~25

## 📱 Production Deployment

### Backend (Heroku/Railway)
1. Add `Procfile`:
```
web: python app.py
```

2. Set environment variables:
```
OPENAI_API_KEY=your-key
FLASK_ENV=production
```

### Frontend (Vercel/Netlify)
1. Build:
```powershell
npm run build
```

2. Set environment variables:
```
REACT_APP_API_URL=https://your-backend-url.com
REACT_APP_SOCKET_URL=https://your-backend-url.com
```

## 🔐 Security Notes

- Never commit `.env` files
- Use environment variables for all secrets
- In production, implement proper authentication
- Consider end-to-end encryption for audio data
- Implement rate limiting on API endpoints

## 📈 Performance Optimization

### Backend
- Use Redis for session storage (currently in-memory)
- Implement request queuing for high traffic
- Cache GPT-4 responses for common patterns
- Use Whisper's streaming API when available

### Frontend
- Implement audio compression before sending
- Add buffering for better network handling
- Lazy load components
- Use React.memo for expensive components

## 🐛 Common Issues

### "Module not found" errors
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### React app won't start
```powershell
cd frontend
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

### WebSocket connection issues
- Check firewall settings
- Ensure both frontend and backend URLs match
- Try using different ports

## 📚 Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Flask-SocketIO Docs](https://flask-socketio.readthedocs.io/)
- [React Documentation](https://react.dev/)
- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)

## 🎯 Hackathon Tips

1. **Demo Preparation**
   - Prepare test scripts for each feature
   - Have backup recordings ready
   - Test on different browsers

2. **Presentation Points**
   - Emphasize parallel processing
   - Show real-time capabilities
   - Demonstrate all 4 agents
   - Highlight healthcare impact

3. **Known Limitations (Be Honest)**
   - Requires internet connection
   - Limited audio analysis (MVP)
   - English language only (currently)
   - Simulated sentiment analysis

## 💡 Extension Ideas

- Multi-speaker detection
- Language translation
- Integration with calendar systems
- Automated email summaries
- Voice authentication
- HIPAA-compliant storage
- Mobile app version
- Browser extension
