"""
Voice-to-text service using OpenAI Whisper
"""
import os
import tempfile
from openai import OpenAI
from django.conf import settings


class WhisperClient:
    """
    Client for OpenAI Whisper ASR (Automatic Speech Recognition)
    Optimized for Indian accents and languages
    """
    
    SUPPORTED_LANGUAGES = {
        'en': 'english',
        'hi': 'hindi',
        'ta': 'tamil',
        'te': 'telugu',
        'bn': 'bengali',
        'mr': 'marathi',
        'gu': 'gujarati',
        'kn': 'kannada',
        'ml': 'malayalam',
        'pa': 'punjabi',
    }
    
    def __init__(self, api_key=None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
    
    def transcribe(self, audio_file, language='en', prompt=None):
        """
        Transcribe audio to text
        
        Args:
            audio_file: File object or path to audio file
            language: Language code (e.g., 'hi' for Hindi)
            prompt: Optional context to improve accuracy
        
        Returns:
            Transcribed text
        """
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        try:
            # Convert language code to Whisper format
            whisper_lang = self.SUPPORTED_LANGUAGES.get(language, 'english')
            
            # Transcribe using Whisper
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=whisper_lang,
                prompt=prompt,
                response_format="text"
            )
            
            return transcript
        
        except Exception as e:
            print(f"Transcription error: {e}")
            raise
    
    def transcribe_with_timestamps(self, audio_file, language='en'):
        """
        Transcribe audio with word-level timestamps
        
        Args:
            audio_file: File object or path to audio file
            language: Language code
        
        Returns:
            Dict with text and timestamps
        """
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        try:
            whisper_lang = self.SUPPORTED_LANGUAGES.get(language, 'english')
            
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=whisper_lang,
                response_format="verbose_json",
                timestamp_granularities=["word"]
            )
            
            return {
                'text': transcript.text,
                'words': transcript.words if hasattr(transcript, 'words') else []
            }
        
        except Exception as e:
            print(f"Transcription error: {e}")
            raise
    
    def translate_to_english(self, audio_file):
        """
        Transcribe and translate any language to English
        
        Args:
            audio_file: File object or path to audio file
        
        Returns:
            English translation
        """
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        try:
            translation = self.client.audio.translations.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
            
            return translation
        
        except Exception as e:
            print(f"Translation error: {e}")
            raise


# Singleton instance
_whisper_client = None

def get_whisper_client():
    """Get or create Whisper client instance"""
    global _whisper_client
    if _whisper_client is None:
        _whisper_client = WhisperClient()
    return _whisper_client


def transcribe_audio_bytes(audio_bytes, filename='audio.wav', language='en'):
    """
    Helper function to transcribe audio from bytes
    
    Args:
        audio_bytes: Audio data as bytes
        filename: Filename for temp file
        language: Language code
    
    Returns:
        Transcribed text
    """
    client = get_whisper_client()
    
    # Write bytes to temporary file
    with tempfile.NamedTemporaryFile(suffix=os.path.splitext(filename)[1], delete=False) as temp_file:
        temp_file.write(audio_bytes)
        temp_path = temp_file.name
    
    try:
        with open(temp_path, 'rb') as audio_file:
            return client.transcribe(audio_file, language=language)
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
