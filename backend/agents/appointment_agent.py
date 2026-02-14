"""
Appointment Agent - Post-Surgery Follow-up Management
Identifies scheduling conflicts, missed appointments, and follow-up needs
"""

from openai import OpenAI
import json


class AppointmentAgent:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        
    def analyze(self, current_text, conversation_history):
        """
        Analyze text for post-surgery appointment and follow-up issues
        Returns: dict with analysis results
        """
        
        context = "\n".join([
            f"{entry['speaker']}: {entry['text']}" 
            for entry in conversation_history[-5:]
        ])
        
        prompt = f"""You are a post-surgery appointment scheduling assistant. Analyze the conversation for scheduling issues.

DETECT:
1. **Missed Appointments:**
   - Patient forgot scheduled follow-up
   - No-show for wound check
   - Missed physical therapy session
   - Skipped medication review

2. **Scheduling Conflicts:**
   - Can't make scheduled appointment time
   - Needs to reschedule due to complications
   - Transportation issues preventing visit
   - Work/family conflicts

3. **Follow-up Needs:**
   - Patient unsure when to return
   - Hasn't scheduled required follow-up
   - Needs additional appointments (PT, specialist)
   - Suture/staple removal scheduling

4. **Urgent Rescheduling:**
   - Symptoms require earlier follow-up
   - Post-op check needed sooner than scheduled
   - Complication requiring re-evaluation

Recent conversation:
{context}

Current statement: {current_text}

Respond in JSON format:
{{
    "issue_detected": true/false,
    "issue_type": "missed_appointment/scheduling_conflict/follow_up_needed/urgent_reschedule",
    "appointment_context": {{
        "original_date": "if mentioned",
        "original_time": "if mentioned",
        "appointment_type": "follow-up/wound check/PT/suture removal/etc.",
        "days_post_surgery": "if calculable from context",
        "reason_for_issue": "why they missed or need to reschedule"
    }},
    "urgency": "low/medium/high",
    "clinical_impact": "does this scheduling issue affect patient recovery? (yes/no/maybe)",
    "description": "brief description of scheduling issue",
    "suggested_action": "specific next steps (offer immediate reschedule, find alternative time, arrange transport, etc.)",
    "timeline": "when this needs to be resolved (today, this week, flexible)"
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a post-surgery appointment scheduling expert. Respond only with valid JSON. Consider impact on patient recovery."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            if result.get('issue_detected'):
                issue_type = result.get('issue_type', 'scheduling issue')
                urgency_emoji = {"low": "📅", "medium": "⚠️", "high": "🔴"}
                emoji = urgency_emoji.get(result.get('urgency', 'medium'), "📅")
                
                # Enhanced message
                clinical_impact = " [Affects Recovery]" if result.get('clinical_impact') == 'yes' else ""
                result['message'] = f"{emoji} Post-Surgery Scheduling: {result.get('description', issue_type)}{clinical_impact}"
            
            return result
            
        except Exception as e:
            print(f"Appointment Analysis Error: {e}")
            return {"issue_detected": False, "error": str(e)}