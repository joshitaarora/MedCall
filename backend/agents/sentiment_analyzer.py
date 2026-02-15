"""
Sentiment Mismatch Analyzer Agent - Danger Detection
Detects when patient's words don't match their emotional state
Critical for identifying coercion, abuse, or hidden distress in post-surgery calls
"""

from openai import OpenAI
import json


class SentimentMismatchAnalyzer:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        
    def analyze(self, current_text, audio_data, conversation_history):
        """
        Analyze for sentiment-content mismatch indicating potential danger
        
        In production: would analyze audio features (pitch, tremor, hesitation)
        For MVP: uses conversational analysis to detect distress signals
        
        Returns: dict with analysis results
        """
        
        context = "\n".join([
            f"{entry['speaker']}: {entry['text']}" 
            for entry in conversation_history[-10:]
        ])
        
        prompt = f"""You are an expert at detecting hidden distress and danger signals in post-surgery patient calls.

POST-SURGERY DANGER SCENARIOS:

1. **Coercion/Abuse:**
   - Patient minimizing pain while showing distress signals
   - Caregiver pressuring patient to say they're "fine"
   - Patient seems coached or monitored during call
   - Unusual formality or scripted responses

2. **Hidden Complications:**
   - Says "everything's fine" but describes concerning symptoms
   - Downplaying severe pain (may fear being "difficult")
   - Contradictory statements about recovery progress
   - Avoiding direct answers about symptoms

3. **Mental Health Crisis:**
   - Saying positive things but tone suggests depression
   - Mentions of hopelessness despite claiming recovery is fine
   - Social isolation patterns
   - Suicidal ideation hidden in casual language

4. **Medication/Substance Issues:**
   - Confusion about medications while claiming compliance
   - Inconsistent pain reporting (possible opioid concerns)
   - Defensive responses about medication usage

5. **Financial/Access Barriers:**
   - Saying they're fine but can't afford follow-up care
   - Avoiding discussion of recommended treatments
   - Not filling prescriptions but claiming they are

CONVERSATIONAL RED FLAGS:
- "I'm fine but..." followed by concerning description
- Hesitation before answering simple questions
- Third party speaking for patient frequently
- Patient sounds scared/stressed despite positive words
- Abrupt topic changes when asked direct questions
- Background voices coaching responses

Conversation history:
{context}

Current statement: {current_text}

Analyze for hidden danger or distress. Respond in JSON format:
{{
    "mismatch_detected": true/false,
    "confidence": 0-100,
    "analysis": {{
        "stated_content": "what patient is saying",
        "detected_subtext": "what they might actually mean",
        "verbal_indicators": ["list of concerning phrases or patterns"],
        "behavioral_red_flags": ["hesitation, avoidance, coaching, etc."]
    }},
    "risk_category": "coercion/hidden_complication/mental_health/medication_concern/access_barrier/normal",
    "risk_level": "low/medium/high/critical",
    "specific_concern": "detailed explanation of what seems wrong",
    "recovery_impact": "how this might affect post-surgery recovery",
    "recommended_action": "specific intervention needed (welfare check, mental health referral, social worker, private follow-up call, etc.)",
    "description": "concise summary of the mismatch"
}}

Be thorough but not alarmist. Genuine concern vs. normal recovery anxiety."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in detecting hidden distress, coercion, and danger signals in medical calls. Respond ONLY with valid JSON, no other text. Balance thoroughness with avoiding false alarms."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )
            
            content = response.choices[0].message.content.strip()
            # Try to extract JSON if there's extra text
            if not content.startswith('{'):
                start = content.find('{')
                if start != -1:
                    content = content[start:]
            if not content.endswith('}'):
                end = content.rfind('}')
                if end != -1:
                    content = content[:end+1]
            
            result = json.loads(content)
            
            if result.get('mismatch_detected'):
                risk = result.get('risk_level', 'medium')
                emoji = "🚨" if risk in ['high', 'critical'] else "⚠️" if risk == 'medium' else "🔍"
                category = result.get('risk_category', 'concern').replace('_', ' ').title()
                result['message'] = f"{emoji} Potential {category}: {result.get('description', 'Sentiment-content mismatch detected')}"
            
            return result
            
        except Exception as e:
            print(f"Sentiment Analysis Error: {e}")
            return {"mismatch_detected": False, "error": str(e)}
    
    def analyze_audio_features(self, audio_data):
        """
        Placeholder for future audio feature extraction
        In production, integrate libraries like librosa or pyAudioAnalysis to detect:
        - Voice tremor (anxiety, fear)
        - Pitch variations (stress indicators)
        - Speaking rate changes (coached vs natural)
        - Pauses and hesitations
        - Background noise patterns
        """
        # Future implementation:
        # - Extract MFCC features
        # - Detect pitch contours
        # - Measure speaking rate
        # - Identify pauses/hesitations
        # - Background voice detection
        
        return {
            "tone": "neutral",  # Would be extracted from audio
            "stress_level": 0,  # Would be computed from voice features
            "speaking_rate": "normal",  # Would be measured
            "background_voices": False  # Would be detected
        }