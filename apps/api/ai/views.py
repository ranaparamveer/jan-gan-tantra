from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .translation import get_bhashini_client
from .voice import get_whisper_client, transcribe_audio_bytes
from .llm import get_llm_client
from .serializers import (
    TranslationRequestSerializer,
    TranslationResponseSerializer,
    LanguageDetectionRequestSerializer,
    LanguageDetectionResponseSerializer,
    VoiceTranscriptionRequestSerializer,
    VoiceTranscriptionResponseSerializer,
    JargonSimplificationRequestSerializer,
    JargonSimplificationResponseSerializer,
    ComplaintDraftRequestSerializer,
    ComplaintDraftResponseSerializer,
    DocumentSummaryRequestSerializer,
    DocumentSummaryResponseSerializer,
    RTIQueryRequestSerializer,
    RTIQueryResponseSerializer,
)


class TranslateView(APIView):
    """
    Translate text between Indian languages using Bhashini
    """
    
    @swagger_auto_schema(
        request_body=TranslationRequestSerializer,
        responses={200: TranslationResponseSerializer}
    )
    def post(self, request):
        serializer = TranslationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        text = serializer.validated_data['text']
        source_lang = serializer.validated_data['source_lang']
        target_lang = serializer.validated_data['target_lang']
        
        client = get_bhashini_client()
        translated = client.translate(text, source_lang, target_lang)
        
        return Response({
            'original_text': text,
            'translated_text': translated,
            'source_lang': source_lang,
            'target_lang': target_lang
        })


class DetectLanguageView(APIView):
    """
    Detect the language of input text
    """
    
    @swagger_auto_schema(
        request_body=LanguageDetectionRequestSerializer,
        responses={200: LanguageDetectionResponseSerializer}
    )
    def post(self, request):
        serializer = LanguageDetectionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        text = serializer.validated_data['text']
        
        client = get_bhashini_client()
        detected_lang = client.detect_language(text)
        
        return Response({
            'text': text,
            'detected_language': detected_lang
        })


class VoiceToTextView(APIView):
    """
    Convert voice audio to text using Whisper
    """
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'audio_file',
                openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description='Audio file (WAV, MP3, etc.)'
            ),
            openapi.Parameter(
                'language',
                openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=False,
                description='Language code (e.g., hi, en)'
            ),
        ],
        responses={200: VoiceTranscriptionResponseSerializer}
    )
    def post(self, request):
        audio_file = request.FILES.get('audio_file')
        language = request.data.get('language', 'en')
        
        if not audio_file:
            return Response(
                {'error': 'audio_file is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Read audio bytes
            audio_bytes = audio_file.read()
            
            # Transcribe
            transcribed_text = transcribe_audio_bytes(
                audio_bytes,
                filename=audio_file.name,
                language=language
            )
            
            return Response({
                'transcribed_text': transcribed_text,
                'language': language
            })
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SimplifyJargonView(APIView):
    """
    Simplify government jargon using LLM
    """
    
    @swagger_auto_schema(
        request_body=JargonSimplificationRequestSerializer,
        responses={200: JargonSimplificationResponseSerializer}
    )
    def post(self, request):
        serializer = JargonSimplificationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        text = serializer.validated_data['text']
        language = serializer.validated_data['language']
        
        try:
            client = get_llm_client()
            simplified = client.simplify_jargon(text, language)
            
            return Response({
                'original_text': text,
                'simplified_text': simplified
            })
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DraftComplaintView(APIView):
    """
    Generate a formal complaint letter using LLM
    """
    
    @swagger_auto_schema(
        request_body=ComplaintDraftRequestSerializer,
        responses={200: ComplaintDraftResponseSerializer}
    )
    def post(self, request):
        serializer = ComplaintDraftRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            client = get_llm_client()
            letter = client.draft_complaint_letter(serializer.validated_data)
            
            return Response({'letter': letter})
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SummarizeDocumentView(APIView):
    """
    Summarize long government documents using LLM
    """
    
    @swagger_auto_schema(
        request_body=DocumentSummaryRequestSerializer,
        responses={200: DocumentSummaryResponseSerializer}
    )
    def post(self, request):
        serializer = DocumentSummaryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        document_text = serializer.validated_data['document_text']
        max_points = serializer.validated_data['max_points']
        
        try:
            client = get_llm_client()
            summary = client.summarize_document(document_text, max_points)
            
            return Response({'summary': summary})
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GenerateRTIQueryView(APIView):
    """
    Generate an RTI query template using LLM
    """
    
    @swagger_auto_schema(
        request_body=RTIQueryRequestSerializer,
        responses={200: RTIQueryResponseSerializer}
    )
    def post(self, request):
        serializer = RTIQueryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        topic = serializer.validated_data['topic']
        department = serializer.validated_data['department']
        
        try:
            client = get_llm_client()
            query = client.generate_rti_query(topic, department)
            
            return Response({'query': query})
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
