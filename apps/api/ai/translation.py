"""
Bhashini API client for Indian language translation
"""
import requests
from django.conf import settings


class BhashiniClient:
    """
    Client for Bhashini (National Language Translation Mission) API
    Supports 22+ Indian languages
    """
    
    BASE_URL = "https://dhruva-api.bhashini.gov.in/services"
    
    # Language codes
    LANGUAGES = {
        'en': 'English',
        'hi': 'Hindi',
        'ta': 'Tamil',
        'te': 'Telugu',
        'bn': 'Bengali',
        'mr': 'Marathi',
        'gu': 'Gujarati',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'pa': 'Punjabi',
        'or': 'Odia',
        'as': 'Assamese',
    }
    
    def __init__(self, api_key=None):
        self.api_key = api_key or settings.BHASHINI_API_KEY
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
    
    def translate(self, text, source_lang='en', target_lang='hi'):
        """
        Translate text from source language to target language
        
        Args:
            text: Text to translate
            source_lang: Source language code (e.g., 'en')
            target_lang: Target language code (e.g., 'hi')
        
        Returns:
            Translated text
        """
        if not self.api_key:
            # Fallback: Return original text if no API key
            return text
        
        try:
            payload = {
                'input': text,
                'sourceLanguage': source_lang,
                'targetLanguage': target_lang
            }
            
            response = self.session.post(
                f'{self.BASE_URL}/translation',
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('output', text)
        
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Fallback to original
    
    def detect_language(self, text):
        """
        Detect the language of input text
        
        Args:
            text: Text to analyze
        
        Returns:
            Language code (e.g., 'hi', 'en')
        """
        if not self.api_key:
            return 'en'  # Default fallback
        
        try:
            payload = {'input': text}
            
            response = self.session.post(
                f'{self.BASE_URL}/language-detection',
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('language', 'en')
        
        except Exception as e:
            print(f"Language detection error: {e}")
            return 'en'
    
    def batch_translate(self, texts, source_lang='en', target_lang='hi'):
        """
        Translate multiple texts in a single request
        
        Args:
            texts: List of texts to translate
            source_lang: Source language code
            target_lang: Target language code
        
        Returns:
            List of translated texts
        """
        if not self.api_key:
            return texts
        
        try:
            payload = {
                'inputs': texts,
                'sourceLanguage': source_lang,
                'targetLanguage': target_lang
            }
            
            response = self.session.post(
                f'{self.BASE_URL}/batch-translation',
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('outputs', texts)
        
        except Exception as e:
            print(f"Batch translation error: {e}")
            return texts


# Singleton instance
_bhashini_client = None

def get_bhashini_client():
    """Get or create Bhashini client instance"""
    global _bhashini_client
    if _bhashini_client is None:
        _bhashini_client = BhashiniClient()
    return _bhashini_client
