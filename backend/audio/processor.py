"""
Audio Processor
Handles audio transcription using OpenAI Whisper
"""

from openai import OpenAI
import base64
import io
import os


class AudioProcessor:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        
    def transcribe(self, audio_data):
        """
        Transcribe audio using OpenAI Whisper API
        
        Args:
            audio_data: Base64 encoded audio or raw bytes
            
        Returns:
            Transcribed text
        """
        try:
            # Handle base64 encoded audio
            if isinstance(audio_data, str):
                audio_bytes = base64.b64decode(audio_data)
            else:
                audio_bytes = audio_data
            
            # Create a file-like object
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = "audio.webm"  # Whisper needs a filename
            
            # Transcribe using Whisper
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
            
            return transcript
            
        except Exception as e:
            print(f"Transcription Error: {e}")
            return None
    
    def transcribe_file(self, file_path):
        """
        Transcribe audio from a file
        """
        try:
            with open(file_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            
            return transcript
            
        except Exception as e:
            print(f"File Transcription Error: {e}")
            return None
