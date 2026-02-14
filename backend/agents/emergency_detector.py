"""
Emergency Detector Agent
Identifies sudden health concerns requiring immediate attention
"""

from openai import OpenAI
import json


class EmergencyDetector:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        
    def analyze(self, current_text, conversation_history):
        """
        Analyze text for emergency health situations
        Returns: dict with detection results
        """
        
        context = "\n".join([
            f"{entry['speaker']}: {entry['text']}" 
            for entry in conversation_history[-5:]
        ])
        
        prompt = f"""You are an emergency medical triage system. Analyze for life-threatening or urgent situations:

CRITICAL SIGNS (require immediate 911):
- Chest pain, heart attack symptoms
- Difficulty breathing, choking
- Severe bleeding
- Loss of consciousness
- Stroke symptoms (facial drooping, slurred speech, arm weakness)
- Severe allergic reactions
- Suicidal ideation or self-harm
- Severe injuries

URGENT SIGNS (require immediate medical attention):
- High fever with concerning symptoms
- Severe pain
- Sudden vision changes
- Severe headache
- Persistent vomiting
- Signs of infection

Recent conversation:
{context}

Current statement: {current_text}

Respond in JSON format:
{{
    "is_emergency": true/false,
    "severity": "critical/urgent/moderate",
    "emergency_type": "type of emergency",
    "confidence": 0-100,
    "symptoms": ["list of concerning symptoms"],
    "action": "immediate action to take (e.g., 'Call 911', 'Go to ER', 'Contact doctor immediately')",
    "description": "brief explanation"
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an emergency medical triage expert. Be cautious and err on the side of safety. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,  # Lower temperature for more consistent emergency detection
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            if result.get('is_emergency'):
                severity = result.get('severity', 'urgent')
                emoji = "🚨" if severity == "critical" else "⚠️"
                result['message'] = f"{emoji} EMERGENCY DETECTED: {result.get('description', 'Immediate attention required')}"
            
            return result
            
        except Exception as e:
            print(f"Emergency Detection Error: {e}")
            return {"is_emergency": False, "error": str(e)}
