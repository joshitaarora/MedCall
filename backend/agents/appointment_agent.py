"""
Appointment Agent
Identifies scheduling conflicts and missed appointments
"""

from openai import OpenAI
import json


class AppointmentAgent:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        
    def analyze(self, current_text, conversation_history):
        """
        Analyze text for appointment-related issues
        Returns: dict with analysis results
        """
        
        context = "\n".join([
            f"{entry['speaker']}: {entry['text']}" 
            for entry in conversation_history[-5:]
        ])
        
        prompt = f"""You are an appointment scheduling assistant. Analyze the conversation for:
- Missed appointments
- Scheduling conflicts
- Rescheduling requests
- Cancellations
- Confusion about appointment times
- Need for follow-up appointments

Recent conversation:
{context}

Current statement: {current_text}

Respond in JSON format:
{{
    "issue_detected": true/false,
    "issue_type": "missed_appointment/scheduling_conflict/rescheduling/cancellation/follow_up",
    "description": "brief description",
    "urgency": "low/medium/high",
    "suggested_action": "specific next steps to resolve",
    "appointment_details": {{
        "date_mentioned": "if any",
        "time_mentioned": "if any",
        "reason": "reason for appointment issue"
    }}
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an appointment scheduling expert. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            if result.get('issue_detected'):
                issue_type = result.get('issue_type', 'scheduling issue')
                result['message'] = f"📅 Appointment Issue: {result.get('description', issue_type)}"
            
            return result
            
        except Exception as e:
            print(f"Appointment Analysis Error: {e}")
            return {"issue_detected": False, "error": str(e)}
