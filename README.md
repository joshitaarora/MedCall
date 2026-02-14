# MedCall - AI-Powered Post-Surgery Call Monitoring 🏥

[![TreeHacks 2026](https://img.shields.io/badge/TreeHacks-2026-blue)](https://treehacks.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**MedCall** is a clinical AI system that monitors post-surgery patient phone calls in real-time using parallel AI agents. Built for TreeHacks 2026, it detects adverse events, scheduling conflicts, emergencies, and hidden danger signals through audio-sentiment mismatch analysis.

## 🎯 The Problem

After surgery, patients call with symptoms and concerns. Nurses manually take notes during these calls, and **critical information gets lost, delayed, or misunderstood:**

- 🔴 Infection symptoms dismissed as "normal healing"
- 🔴 Severe pain (8/10) documented but urgency missed
- 🔴 Medication side effects buried in 10-minute conversations
- 🔴 Scheduling conflicts delay critical follow-ups

**Result:** Preventable ER visits, complications, and poor patient outcomes.

## 💡 The Solution

MedCall AI analyzes post-surgery calls in real-time with **4 specialized clinical agents** running in parallel:

### 1️⃣ **Adverse Event (AE) Detector** ⚠️
Identifies post-surgery complications with medical precision:
- **Infection symptoms:** Fever >100.4°F, redness, drainage, swelling
- **Severe pain:** Pain level 7+/10, sudden pain increase
- **Medication issues:** Side effects, allergic reactions, non-response
- **Bleeding/circulation:** Excessive bleeding, DVT risk
- **Respiratory/cardiac:** Breathing difficulty, chest pain

**Clinical accuracy:** Detects pain levels, days post-surgery, specific symptoms

### 2️⃣ **Emergency Detector** 🚨
Triages sudden health concerns requiring immediate action:
- **CRITICAL:** PE risk, stroke symptoms, severe bleeding → Call 911
- **URGENT:** High fever, wound dehiscence, uncontrolled pain → Contact surgeon within 1 hour
- **MODERATE:** Low-grade fever, mild drainage → Contact doctor within 24 hours

**Time-sensitive escalation** based on complication type and severity

### 3️⃣ **Appointment Agent** 📅
Manages post-surgery follow-up scheduling:
- Missed wound checks, PT sessions, suture removal
- Scheduling conflicts affecting recovery timeline
- Urgent rescheduling due to complications
- Follow-up needs (specialist referrals, additional visits)

**Tracks clinical impact** on patient recovery

### 4️⃣ **Sentiment Mismatch Analyzer** 🎭 *(Ambitious Feature)*
Detects hidden danger through audio-content discrepancies:
- **Coercion/abuse:** Patient minimizing pain under pressure
- **Hidden complications:** Says "fine" but describes concerning symptoms
- **Mental health crisis:** Depression/suicidal ideation masked
- **Access barriers:** Can't afford care but claiming recovery is good

**Identifies patterns:** Coached responses, third-party influence, financial barriers

---

## 🚀 How It Works

### **Parallel AI Architecture**
```
Microphone → Audio Capture → Whisper Transcription
                                      ↓
                         ┌────────────┴──────────────┐
                         │   Parallel Processing     │
           ┌─────────────┼─────────────┼─────────────┼──────────────┐
           ↓             ↓             ↓             ↓              ↓
    AE Detector   Appointment   Emergency    Sentiment        Clinical
   (Infections,     (Missed      (Critical    (Hidden        Note Gen
    Pain 7+/10,    Follow-ups,   PE/DVT,     Distress,       (Future)
    Med Issues)    Scheduling)   Sepsis)     Coercion)
           │             │             │             │              │
           └─────────────┴─────────────┴─────────────┴──────────────┘
                                      ↓
                     Real-time Alerts + Live Transcript
```

**All 4 agents run simultaneously** - no blocking, instant analysis.

---

## 🌟 Key Features

✅ **Clinical Precision**
- Detects pain levels (0-10 scale)
- Tracks days post-surgery
- Identifies specific complication types (PE, DVT, infection, dehiscence)

✅ **Real-Time Processing**
- Live audio transcription with OpenAI Whisper
- Parallel agent execution (Python threading)
- WebSocket updates to dashboard

✅ **Structured Clinical Output**
- Severity classification (mild/moderate/severe)
- Urgency levels (immediate/1hr/24hr)
- Actionable recommendations (Call 911, Contact surgeon, Schedule follow-up)

✅ **Comprehensive Monitoring**
- Post-surgery adverse events
- Missed appointments affecting recovery
- Life-threatening emergencies
- Hidden danger signals (coercion, mental health, access barriers)

---

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** with Flask
- **OpenAI API** (GPT-4 + Whisper)
- **Flask-SocketIO** for real-time communication
- **Threading** for parallel agent execution

### Frontend
- **React 18**
- **Socket.io Client** for WebSocket
- **Web Audio API** for microphone
- **Responsive design**

---

## 📦 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key

### 1️⃣ **Run Setup Script (Windows)**
```powershell
.\setup.ps1
```

### 2️⃣ **Add Your OpenAI API Key**
Edit `backend/.env`:
```
OPENAI_API_KEY=your-actual-api-key-here
```

### 3️⃣ **Start Backend**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python app.py
```

### 4️⃣ **Start Frontend** (New Terminal)
```powershell
cd frontend
npm start
```

Access at: `http://localhost:3000`

---

## 🧪 Testing with Clinical Scenarios

### **Test 1: Post-Surgery Infection**
**Say:** *"I had my appendectomy 3 days ago, and now I have a fever of 101 degrees. The incision site is red and there's some yellowish drainage coming out."*

**Expected Alerts:**
- ⚠️ **AE Detector:** Infection symptoms (fever, drainage, redness)
- 🔴 **Emergency Detector:** Urgent - Contact surgeon within 1 hour
- **Pain Level:** Extracted if mentioned
- **Days Post-Op:** 3 days

---

### **Test 2: Severe Pain Crisis**
**Say:** *"The pain is unbearable - I'd rate it 9 out of 10. The pain medication isn't helping at all, and it's getting worse."*

**Expected Alerts:**
- 🚨 **AE Detector:** Severe pain (9/10), medication non-response
- 🚨 **Emergency Detector:** Urgent - Uncontrolled pain
- **Action:** Immediate surgical consultation

---

### **Test 3: Missed Follow-up Appointment**
**Say:** *"Oh no, I completely forgot about my wound check appointment yesterday. I've been having some drainage but thought it was normal."*

**Expected Alerts:**
- 📅 **Appointment Agent:** Missed wound check
- ⚠️ **Clinical Impact:** Yes (drainage present, needs evaluation)
- **Action:** Urgent rescheduling + wound assessment

---

### **Test 4: Sentiment Mismatch (Ambitious)**
**Say (in distressed tone):** *"Everything is fine, I'm managing okay. My husband says I'm doing great and I shouldn't bother the doctor..."*

**Expected Alerts:**
- 🎭 **Sentiment Analyzer:** Potential coercion/hidden distress
- **Red Flags:** Third-party influence, minimizing symptoms
- **Action:** Private follow-up call, welfare check

---

### **Test 5: Critical Emergency**
**Say:** *"I'm having severe chest pain and I can't catch my breath. My left leg is also really swollen and painful."*

**Expected Alerts:**
- 🚨🚨 **Emergency Detector:** CRITICAL - Possible PE/DVT
- **Action:** Call 911 immediately
- **Symptoms:** Chest pain, dyspnea, leg swelling (classic PE presentation)

---

## 📊 Clinical Accuracy

- ✅ **Pain Level Detection:** Extracts numeric scale (0-10)
- ✅ **Timeline Tracking:** Days post-surgery calculation
- ✅ **Symptom Classification:** Maps to clinical categories
- ✅ **Urgency Triage:** Follows post-op emergency protocols
- ✅ **Conservative Flagging:** Better false positive than missed emergency

---

## 🎨 Dashboard Features

### Real-Time Alert Panel
- Color-coded severity (🚨 Critical, 🔴 High, ⚠️ Medium)
- Alert statistics (Critical/High/Medium counts)
- Recommended actions for each alert
- Timestamp tracking

### Live Transcript View
- Auto-scrolling conversation
- Speaker identification
- Searchable history
- Timestamp on each entry

### Audio Monitor
- Visual level meter
- Recording status indicator
- Microphone access control

---

## 🏗️ Architecture Details

### Session Management
- Each call = unique session ID
- Conversation history maintained
- Alerts linked to sessions
- Summary statistics on session end

### Parallel Processing
```python
# All agents run simultaneously
threads = [
    Thread(target=ae_detector.analyze),
    Thread(target=appointment_agent.analyze),
    Thread(target=emergency_detector.analyze),
    Thread(target=sentiment_analyzer.analyze)
]
for thread in threads:
    thread.start()
```

### Real-Time Communication
- WebSocket for bi-directional updates
- Audio chunks sent every 3 seconds
- Instant alert notifications
- Live transcript streaming

---

## 🔐 Privacy & Compliance

- **Audio Processing:** Real-time, not permanently stored (MVP)
- **HIPAA Readiness:** Encryption, audit logging (production roadmap)
- **Data Retention:** Configurable session cleanup
- **Access Control:** Role-based permissions (future)

---

## 🚧 Roadmap

### Phase 1: Clinical Validation *(Current)*
- [x] Core 4-agent system
- [x] Post-surgery focus
- [ ] Clinical note generation
- [ ] Structured medical reporting

### Phase 2: Production Features
- [ ] OpenEvidence API integration (clinical guidelines)
- [ ] EHR integration (Epic, Cerner)
- [ ] Advanced audio analysis (pitch, tone, stress detection)
- [ ] Multi-language support
- [ ] HIPAA compliance certification

### Phase 3: Scale
- [ ] FDA clearance as clinical decision support
- [ ] Hospital pilot programs
- [ ] Automated workflow triggers (paging, scheduling)
- [ ] Analytics dashboard for outcomes tracking

---

## 🏆 TreeHacks 2026 Submission

### Target Prizes
- **Zingage Healthcare Voice AI** (Primary)
- **Anthropic Claude SDK Prize**
- **OpenEvidence Medical AI**
- **Most Impactful Project**

### Demo Video Script
1. **Problem:** Show nurse manually taking notes, missing fever mention
2. **Solution:** MedCall detects fever + infection → urgent alert
3. **Technical:** Show parallel agents running simultaneously
4. **Impact:** "Prevents ER visits, saves lives, reduces nurse burnout"

---

## 👥 Team & Acknowledgments

Built for TreeHacks 2026

**Technologies:**
- OpenAI (GPT-4 + Whisper)
- React + Flask
- Socket.io
- Web Audio API

**Special Thanks:**
- Clinical advisors for medical accuracy validation
- TreeHacks organizers
- Open source community

---

## 📄 License

MIT License - See LICENSE file

---

## 🔗 Links

- [Devpost Submission](#)
- [Demo Video](#)
- [GitHub Repository](#)

---

**Built with ❤️ for better patient outcomes**