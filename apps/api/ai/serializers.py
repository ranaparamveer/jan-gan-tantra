from rest_framework import serializers


class TranslationRequestSerializer(serializers.Serializer):
    text = serializers.CharField()
    source_lang = serializers.CharField(default='en', max_length=10)
    target_lang = serializers.CharField(max_length=10)


class TranslationResponseSerializer(serializers.Serializer):
    original_text = serializers.CharField()
    translated_text = serializers.CharField()
    source_lang = serializers.CharField()
    target_lang = serializers.CharField()


class LanguageDetectionRequestSerializer(serializers.Serializer):
    text = serializers.CharField()


class LanguageDetectionResponseSerializer(serializers.Serializer):
    text = serializers.CharField()
    detected_language = serializers.CharField()


class VoiceTranscriptionRequestSerializer(serializers.Serializer):
    audio_file = serializers.FileField()
    language = serializers.CharField(default='en', max_length=10)


class VoiceTranscriptionResponseSerializer(serializers.Serializer):
    transcribed_text = serializers.CharField()
    language = serializers.CharField()


class JargonSimplificationRequestSerializer(serializers.Serializer):
    text = serializers.CharField()
    language = serializers.CharField(default='en', max_length=10)


class JargonSimplificationResponseSerializer(serializers.Serializer):
    original_text = serializers.CharField()
    simplified_text = serializers.CharField()


class ComplaintDraftRequestSerializer(serializers.Serializer):
    issue = serializers.CharField()
    location = serializers.CharField()
    officer_name = serializers.CharField(required=False, allow_blank=True)
    officer_designation = serializers.CharField(required=False, allow_blank=True)


class ComplaintDraftResponseSerializer(serializers.Serializer):
    letter = serializers.CharField()


class DocumentSummaryRequestSerializer(serializers.Serializer):
    document_text = serializers.CharField()
    max_points = serializers.IntegerField(default=5, min_value=1, max_value=10)


class DocumentSummaryResponseSerializer(serializers.Serializer):
    summary = serializers.CharField()


class RTIQueryRequestSerializer(serializers.Serializer):
    topic = serializers.CharField()
    department = serializers.CharField()


class RTIQueryResponseSerializer(serializers.Serializer):
    query = serializers.CharField()
