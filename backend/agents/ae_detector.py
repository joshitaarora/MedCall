"""
Adverse Event (AE) Detector Agent
Identifies adverse events reported during medical calls
"""

from openai import OpenAI
import json


class AdverseEventDetector:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        
    def analyze(self, current_text, conversation_history):
        """
        Analyze text for adverse events
        Returns: dict with detection results
        """
        
        # Build context from conversation history
        context = "\n".join([
            f"{entry['speaker']}: {entry['text']}" 
            for entry in conversation_history[-5:]  # Last 5 exchanges
        ])
        
        prompt = f"""You are a medical adverse event detection system. Analyze the following conversation for any adverse events (AEs).

An adverse event includes:
- Side effects from medications
- Unexpected medical complications
- Allergic reactions
- Treatment-related problems
- New or worsening symptoms after treatment
- Medication errors
- Device malfunctions

Recent conversation context:
{context}

Current statement: {current_text}

Analyze if an adverse event is being reported. Respond in JSON format:
{{
    "detected": true/false,
    "confidence": 0-100,
    "ae_type": "type of adverse event",
    "severity": "mild/moderate/severe",
    "description": "brief description",
    "action": "recommended next steps"
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a medical adverse event detection expert. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            if result.get('detected'):
                result['message'] = f"⚠️ Adverse Event Detected: {result.get('description', 'Unknown AE')}"
            
            return result
            
        except Exception as e:
            print(f"AE Detection Error: {e}")
            return {"detected": False, "error": str(e)}
