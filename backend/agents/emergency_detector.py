"""
Emergency Detector Agent - Post-Surgery Emergency Focus
Identifies sudden health concerns requiring immediate medical attention
"""

from openai import OpenAI
import json


class EmergencyDetector:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        
    def analyze(self, current_text, conversation_history):
        """
        Analyze text for post-surgery emergencies requiring immediate action
        Returns: dict with detection results
        """
        
        context = "\n".join([
            f"{entry['speaker']}: {entry['text']}" 
            for entry in conversation_history[-5:]
        ])
        
        prompt = f"""You are an emergency medical triage system specializing in post-surgery complications.

POST-SURGERY EMERGENCIES (require immediate action):

**CRITICAL (Call 911 / Go to ER immediately):**
- Chest pain with difficulty breathing (PE risk)
- Sudden severe headache, confusion, stroke symptoms
- Severe allergic reaction (throat swelling, severe rash)
- Heavy bleeding that won't stop
- Severe abdominal pain (could indicate internal bleeding)
- Can't breathe / severe shortness of breath
- Loss of consciousness or extreme dizziness
- Signs of blood clot: sudden leg swelling, pain, warmth, redness
- Fever >103°F with confusion or severe symptoms
- Suicidal ideation or self-harm thoughts

**URGENT (Contact surgeon/doctor immediately - within 1 hour):**
- Fever >101°F with chills
- Wound opening or dehiscence
- Signs of infection worsening rapidly
- Uncontrolled pain despite medications
- Inability to urinate for >8 hours after surgery
- Severe vomiting preventing medication/fluid intake
- Sudden vision changes
- Numbness or tingling in extremities

**MODERATE (Contact doctor within 24 hours):**
- Low-grade fever (100-101°F)
- Moderate wound drainage
- Pain increasing gradually
- Mild swelling at surgical site

Recent conversation:
{context}

Current patient statement: {current_text}

Respond in JSON format:
{{
    "is_emergency": true/false,
    "severity": "critical/urgent/moderate",
    "emergency_type": "type of emergency",
    "confidence": 0-100,
    "post_surgery_complication": "specific complication type (PE, infection, DVT, etc.)",
    "symptoms_duration": "how long symptoms present if mentioned",
    "vital_signs_mentioned": {{"fever": "temp if mentioned", "pain_level": "0-10 if mentioned"}},
    "symptoms": ["list of concerning symptoms"],
    "action": "specific immediate action (Call 911, Go to ER, Call surgeon immediately, etc.)",
    "time_sensitivity": "immediate/within 1 hour/within 24 hours",
    "description": "brief clinical explanation"
}}

Be cautious - err on the side of escalation for patient safety."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an emergency medical triage expert for post-surgery patients. Respond only with valid JSON. Patient safety is paramount - when in doubt, escalate."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            if result.get('is_emergency'):
                severity = result.get('severity', 'urgent')
                emoji = "🚨" if severity == "critical" else "⚠️" if severity == "urgent" else "🔴"
                action = result.get('action', 'Immediate medical attention required')
                result['message'] = f"{emoji} POST-SURGERY EMERGENCY: {result.get('description', 'Immediate attention required')} - {action}"
            
            return result
            
        except Exception as e:
            print(f"Emergency Detection Error: {e}")
            return {"is_emergency": False, "error": str(e)}