# Jan-Gan-Tantra API Guide

## Base URL

```
http://localhost:8000
```

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **OpenAPI JSON**: http://localhost:8000/swagger.json

---

## AI Services

### 1. Translation (Bhashini)

**Endpoint**: `POST /api/ai/translate/`

**Request**:
```json
{
  "text": "How do I file a complaint?",
  "source_lang": "en",
  "target_lang": "hi"
}
```

**Response**:
```json
{
  "original_text": "How do I file a complaint?",
  "translated_text": "मैं शिकायत कैसे दर्ज करूं?",
  "source_lang": "en",
  "target_lang": "hi"
}
```

**Supported Languages**:
- `en` - English
- `hi` - Hindi
- `ta` - Tamil
- `te` - Telugu
- `bn` - Bengali
- `mr` - Marathi
- `gu` - Gujarati
- `kn` - Kannada
- `ml` - Malayalam
- `pa` - Punjabi
- `or` - Odia
- `as` - Assamese

---

### 2. Language Detection

**Endpoint**: `POST /api/ai/detect-language/`

**Request**:
```json
{
  "text": "मुझे सहायता चाहिए"
}
```

**Response**:
```json
{
  "text": "मुझे सहायता चाहिए",
  "detected_language": "hi"
}
```

---

### 3. Voice to Text (Whisper)

**Endpoint**: `POST /api/ai/voice-to-text/`

**Request** (multipart/form-data):
```
audio_file: [audio file]
language: hi
```

**Response**:
```json
{
  "transcribed_text": "मुझे अपने इलाके में कचरा संग्रहण की समस्या है",
  "language": "hi"
}
```

**Supported Audio Formats**: WAV, MP3, M4A, FLAC, OGG

---

### 4. Simplify Jargon

**Endpoint**: `POST /api/ai/simplify-jargon/`

**Request**:
```json
{
  "text": "As per Municipal Solid Waste Management Rules 2016, Section 4(1)(d), the local authority shall ensure segregation of waste at source and facilitate collection of segregated wastes from the waste generators.",
  "language": "en"
}
```

**Response**:
```json
{
  "original_text": "As per Municipal Solid Waste...",
  "simplified_text": "• Your local government must make sure garbage is separated into different types at your home\n• They should help you collect this separated garbage\n• This is required by the 2016 waste management law"
}
```

---

### 5. Draft Complaint Letter

**Endpoint**: `POST /api/ai/draft-complaint/`

**Request**:
```json
{
  "issue": "Garbage not collected for 2 weeks",
  "location": "Sector 4, Ward 12, Mumbai",
  "officer_name": "Rajesh Kumar",
  "officer_designation": "Ward Sanitary Inspector"
}
```

**Response**:
```json
{
  "letter": "To,\nRajesh Kumar\nWard Sanitary Inspector\nMumbai Municipal Corporation\n\nSubject: Complaint regarding non-collection of garbage in Sector 4, Ward 12\n\nRespected Sir,\n\nI am writing to bring to your attention the serious issue of garbage not being collected in Sector 4, Ward 12 for the past two weeks...\n\n[Full formatted letter]"
}
```

---

### 6. Summarize Document

**Endpoint**: `POST /api/ai/summarize-document/`

**Request**:
```json
{
  "document_text": "[Long government document text...]",
  "max_points": 5
}
```

**Response**:
```json
{
  "summary": "1. Citizens have the right to file RTI within 30 days\n2. Information must be provided within 48 hours for life/liberty issues\n3. First appeal can be filed if no response\n4. Penalty of ₹250/day for delays\n5. All government records are public unless exempted"
}
```

---

### 7. Generate RTI Query

**Endpoint**: `POST /api/ai/generate-rti/`

**Request**:
```json
{
  "topic": "Details of road repair budget for Ward 12",
  "department": "Public Works Department, Mumbai"
}
```

**Response**:
```json
{
  "query": "To,\nPublic Information Officer\nPublic Works Department\nMumbai Municipal Corporation\n\nSubject: RTI Application under Section 6(1) of RTI Act 2005\n\nI request the following information:\n\n1. Total budget allocated for road repairs in Ward 12 for FY 2024-25\n2. List of roads repaired with dates and contractor details\n3. Pending repair requests with reasons for delay\n\nAs per RTI Act 2005, please provide this information within 30 days.\n\n[Full RTI query]"
}
```

---

## Example Workflows

### Workflow 1: Voice Search in Hindi

```bash
# Step 1: Record voice and send to API
curl -X POST http://localhost:8000/api/ai/voice-to-text/ \
  -F "audio_file=@recording.wav" \
  -F "language=hi"

# Response: {"transcribed_text": "कचरा संग्रहण की समस्या", "language": "hi"}

# Step 2: Translate to English for search
curl -X POST http://localhost:8000/api/ai/translate/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "कचरा संग्रहण की समस्या",
    "source_lang": "hi",
    "target_lang": "en"
  }'

# Response: {"translated_text": "garbage collection problem", ...}

# Step 3: Search solutions
curl "http://localhost:8000/api/wiki/solutions/?search=garbage+collection"
```

---

### Workflow 2: Generate Complaint with AI

```bash
# Step 1: Find responsible officer
curl "http://localhost:8000/api/govgraph/officers/find_responsible/?category=sanitation&city=Mumbai"

# Step 2: Draft complaint letter
curl -X POST http://localhost:8000/api/ai/draft-complaint/ \
  -H "Content-Type: application/json" \
  -d '{
    "issue": "Overflowing garbage bins",
    "location": "Sector 4, Ward 12",
    "officer_name": "Rajesh Kumar",
    "officer_designation": "Ward Sanitary Inspector"
  }'

# Step 3: Translate to Hindi if needed
curl -X POST http://localhost:8000/api/ai/translate/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "[Generated letter]",
    "source_lang": "en",
    "target_lang": "hi"
  }'
```

---

### Workflow 3: Simplify Government Document

```bash
# Step 1: Upload document and summarize
curl -X POST http://localhost:8000/api/ai/summarize-document/ \
  -H "Content-Type: application/json" \
  -d '{
    "document_text": "[Paste full document]",
    "max_points": 5
  }'

# Step 2: Simplify each point
curl -X POST http://localhost:8000/api/ai/simplify-jargon/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "[Complex point from summary]",
    "language": "en"
  }'
```

---

## Error Handling

All AI endpoints return errors in this format:

```json
{
  "error": "Error message description"
}
```

**Common Error Codes**:
- `400` - Bad request (missing parameters)
- `500` - Internal server error (AI service unavailable)

**Fallback Behavior**:
- Translation: Returns original text if Bhashini API fails
- Voice: Requires OpenAI API key
- LLM: Falls back to OpenAI if Ollama is unavailable

---

## Rate Limiting

Currently no rate limiting is implemented. For production:
- Recommended: 100 requests/minute per user
- Voice transcription: 10 requests/minute (expensive)
- LLM operations: 20 requests/minute

---

## Setup Requirements

### Environment Variables

```bash
# Required for translation
BHASHINI_API_KEY=your_bhashini_key

# Required for voice and LLM (if not using Ollama)
OPENAI_API_KEY=your_openai_key
```

### Ollama Setup (Optional, for self-hosted LLM)

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull Llama 3 model
ollama pull llama3

# Start Ollama server (runs on port 11434)
ollama serve
```

If Ollama is not available, the system automatically falls back to OpenAI GPT-3.5.

---

## Testing AI Services

### Quick Test Script

```bash
#!/bin/bash

# Test translation
echo "Testing translation..."
curl -X POST http://localhost:8000/api/ai/translate/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "source_lang": "en", "target_lang": "hi"}'

# Test jargon simplification
echo "\n\nTesting jargon simplification..."
curl -X POST http://localhost:8000/api/ai/simplify-jargon/ \
  -H "Content-Type: application/json" \
  -d '{"text": "As per Section 4(1)(d) of the Act...", "language": "en"}'

# Test RTI generation
echo "\n\nTesting RTI generation..."
curl -X POST http://localhost:8000/api/ai/generate-rti/ \
  -H "Content-Type: application/json" \
  -d '{"topic": "Road repair budget", "department": "PWD"}'
```

---

## Next Steps

1. **Get API Keys**:
   - Bhashini: https://bhashini.gov.in/
   - OpenAI: https://platform.openai.com/

2. **Update `.env`**:
   ```
   BHASHINI_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
   ```

3. **Test Endpoints**: Visit http://localhost:8000/swagger/

4. **Integrate with Frontend**: Use these APIs in React components

---

For more examples, see the [Swagger documentation](http://localhost:8000/swagger/).
