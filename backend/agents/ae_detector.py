"""
Adverse Event (AE) Detector Agent - Clinical Post-Surgery Focus
Identifies adverse events in post-surgery patient calls with medical precision
"""

from openai import OpenAI
import json


class AdverseEventDetector:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        
    def analyze(self, current_text, conversation_history):
        """
        Analyze text for post-surgery adverse events with clinical precision
        Returns: dict with detection results
        """
        
        # Build context from conversation history
        context = "\n".join([
            f"{entry['speaker']}: {entry['text']}" 
            for entry in conversation_history[-5:]  # Last 5 exchanges
        ])
        
        prompt = f"""You are a clinical AI assistant analyzing post-surgery patient calls for adverse events.

CRITICAL RED FLAGS (must detect):
1. **Infection Symptoms:**
   - Fever (>100.4°F / 38°C)
   - Redness, warmth, swelling at incision site
   - Drainage, pus, or unusual discharge
   - Foul odor from wound

2. **Severe Pain:**
   - Pain level 7+/10 (despite pain medication)
   - Sudden increase in pain
   - Sharp, stabbing pain at surgical site

3. **Medication Issues:**
   - Severe side effects (nausea, vomiting, dizziness)
   - Allergic reactions (rash, itching, swelling)
   - Not responding to prescribed medications

4. **Bleeding/Circulation:**
   - Excessive bleeding from incision
   - Blood in urine/stool
   - Swelling in legs (DVT risk)

5. **Respiratory/Cardiac:**
   - Difficulty breathing
   - Chest pain
   - Rapid heartbeat

6. **Other Complications:**
   - Unable to urinate/move bowels
   - Confusion, disorientation
   - Persistent nausea preventing eating/drinking

Recent conversation context:
{context}

Current patient statement: {current_text}

Analyze if an adverse event is being reported. Respond in JSON format:
{{
    "detected": true/false,
    "confidence": 0-100,
    "ae_category": "infection/severe_pain/medication/bleeding/respiratory/other",
    "severity": "mild/moderate/severe",
    "pain_level": "numeric 0-10 if mentioned, null otherwise",
    "specific_symptoms": ["list of exact symptoms mentioned"],
    "days_post_surgery": "number of days if mentioned, null otherwise",
    "surgery_type": "type if mentioned, null otherwise",
    "description": "brief clinical description",
    "clinical_reasoning": "1-2 sentence justification for severity",
    "recommended_action": "specific next steps (immediate callback, ER visit, medication adjustment, etc.)"
}}

Be conservative - flag anything potentially serious. Better safe than sorry."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a clinical adverse event detection expert for post-surgery patients. Respond only with valid JSON. Be thorough and conservative - patient safety is paramount."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            if result.get('detected'):
                severity_emoji = {"mild": "⚠️", "moderate": "🔴", "severe": "🚨"}
                emoji = severity_emoji.get(result.get('severity', 'moderate'), "⚠️")
                
                # Enhanced message with clinical details
                symptoms = ", ".join(result.get('specific_symptoms', ['adverse event']))
                pain = f" (Pain: {result['pain_level']}/10)" if result.get('pain_level') else ""
                result['message'] = f"{emoji} Post-Surgery AE Detected: {symptoms}{pain}"
            
            return result
            
        except Exception as e:
            print(f"AE Detection Error: {e}")
            return {"detected": False, "error": str(e)}