"""
Sentiment Mismatch Analyzer Agent
Detects when audio sentiment doesn't match spoken words (potential danger scenarios)
"""

from openai import OpenAI
import json


class SentimentMismatchAnalyzer:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        
    def analyze(self, current_text, audio_data, conversation_history):
        """
        Analyze for sentiment-content mismatch
        In a full implementation, this would use audio analysis libraries
        For hackathon, we'll simulate with GPT-4's understanding of context
        
        Returns: dict with analysis results
        """
        
        context = "\n".join([
            f"{entry['speaker']}: {entry['text']}" 
            for entry in conversation_history[-10:]
        ])
        
        # In production, you'd extract audio features like:
        # - Pitch/tone analysis
        # - Speaking rate
        # - Voice tremor
        # - Background noise analysis
        # For hackathon, we'll use contextual analysis
        
        prompt = f"""You are an expert at detecting distress signals and potential danger situations through conversation analysis.

Analyze the conversation for signs that the speaker might be in danger or under duress:

DANGER INDICATORS:
- Saying "I'm fine" but conversation suggests otherwise
- Unusual formality or stiffness in responses
- Avoiding direct answers
- Code words or phrases that seem out of place
- Sudden change in communication pattern
- Contradictory statements
- Signs of being coached or monitored
- Hesitation or unusual pauses (if mentioned in context)
- Background disturbances or interruptions
- Person sounds scared despite saying positive things

EXAMPLES:
- Bank teller being robbed might say "everything is fine" but tone suggests fear
- Domestic violence victim might deny problems while showing distress signals
- Kidnapping victim might give coded messages
- Medical patient under duress might minimize symptoms

Conversation history:
{context}

Current statement: {current_text}

Analyze for sentiment-content mismatch and potential danger. Respond in JSON format:
{{
    "mismatch_detected": true/false,
    "confidence": 0-100,
    "analysis": {{
        "stated_sentiment": "what they're saying",
        "actual_sentiment": "what might be true",
        "indicators": ["list of warning signs"],
        "context_clues": ["contextual evidence"]
    }},
    "risk_level": "low/medium/high/critical",
    "scenario_type": "possible scenario (e.g., 'coercion', 'distress', 'emergency_hidden', 'normal')",
    "action": "recommended action",
    "description": "explanation of the mismatch"
}}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in detecting distress signals and danger through conversation analysis. Be careful but thorough. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            if result.get('mismatch_detected'):
                risk = result.get('risk_level', 'medium')
                emoji = "🚨" if risk in ['high', 'critical'] else "⚠️"
                result['message'] = f"{emoji} Potential Danger: {result.get('description', 'Sentiment mismatch detected')}"
            
            return result
            
        except Exception as e:
            print(f"Sentiment Analysis Error: {e}")
            return {"mismatch_detected": False, "error": str(e)}
    
    def analyze_audio_features(self, audio_data):
        """
        Placeholder for audio feature extraction
        In production, use libraries like librosa, pyAudioAnalysis
        """
        # This would extract:
        # - MFCC features
        # - Pitch contours
        # - Energy levels
        # - Speaking rate
        # - Voice quality metrics
        
        return {
            "tone": "neutral",  # Would be extracted from audio
            "stress_level": 0,  # Would be computed
            "speaking_rate": "normal"  # Would be measured
        }
