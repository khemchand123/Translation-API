# Audio Translation API v2.0

A Flask REST API wrapper for audio translation with speaker diarization using SarvamAI. This service downloads audio from URLs or accepts file uploads, transcribes and translates the content to English, and returns speaker-wise transcripts.

## Features

- 🎤 **Audio Translation**: Transcribe and translate audio files from URLs or uploads
- 👥 **Speaker Diarization**: Separate and identify different speakers
- 🌐 **Language Detection**: Automatic language identification (supports Telugu, Hindi, Tamil, and more)
- 🔄 **Auto Translation**: Automatically translates to English
- 📦 **Metadata Support**: Pass custom metadata and get it back in the response
- 📤 **File Upload**: Support both URL-based and direct file upload
- 🐳 **Docker Ready**: Easy deployment with Docker
- 🔍 **Health Monitoring**: Built-in health check endpoint

## API Endpoints

### `POST /translate`

Translate audio from URL with speaker diarization and optional metadata.

**Request:**
```json
{
  "audio_url": "https://example.com/audio.mp3",
  "seller_buyer_meta_data": {
    "seller_identifier": "5901",
    "buyer_identifier": "8801",
    "city": "Chennai",
    "state": "Tamil Nadu",
    "mcat_name": "Commercial Kitchen Equipment",
    "mcat_id": "5570",
    "main_product": "Product Name"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "language_code": "hi-IN",
  "speakers": [
    {
      "speaker_id": "speaker_1",
      "text": "Hello"
    },
    {
      "speaker_id": "speaker_2",
      "text": "Hi there"
    }
  ],
  "seller_buyer_meta_data": {
    "seller_identifier": "5901",
    "buyer_identifier": "8801",
    "city": "Chennai",
    "state": "Tamil Nadu",
    "mcat_name": "Commercial Kitchen Equipment",
    "mcat_id": "5570",
    "main_product": "Product Name"
  }
}
```

### `POST /translate-file`

Upload and translate audio file with speaker diarization.

**Request (multipart/form-data):**
- `audio_file`: Audio file (mp3, wav, etc.)
- `seller_buyer_meta_data`: JSON string with metadata (optional)

**Example:**
```bash
curl -X POST http://localhost:8888/translate-file \
  -F "audio_file=@audio.mp3" \
  -F 'seller_buyer_meta_data={"seller_identifier":"5901","city":"Chennai"}'
```

**Response:** Same format as `/translate` endpoint

### `GET /health`

Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "service": "audio-translation-api"
}
```

### `GET /`

API documentation and information.

## Local Development

### Prerequisites

- Python 3.10+
- SarvamAI API key

### Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd /home/khem-chand/Hackathon/translation
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables (optional):**
   ```bash
   export SARVAM_API_KEY=your_api_key_here
   export FLASK_ENV=development
   export PORT=8888
   ```

4. **Run the API:**
   ```bash
   python api.py
   ```

   The API will be available at `http://localhost:8888`

### Testing the API

**Using cURL (with metadata):**
```bash
curl -X POST http://localhost:8888/translate \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://sr.knowlarity.com/vr/fetchsound/?callid=48bdfa3f-2d1b-4ef4-a686-369d4862f106",
    "seller_buyer_meta_data": {
      "seller_identifier": "5901",
      "buyer_identifier": "8801",
      "city": "Chennai"
    }
  }'
```

**Upload File:**
```bash
curl -X POST http://localhost:8888/translate-file \
  -F "audio_file=@audio.mp3" \
  -F 'seller_buyer_meta_data={"seller_identifier":"5901"}'
```

**Using Python:**
```python
import requests

# URL-based translation with metadata
response = requests.post(
    'http://localhost:8888/translate',
    json={
        'audio_url': 'https://example.com/audio.mp3',
        'seller_buyer_meta_data': {
            'seller_identifier': '5901',
            'buyer_identifier': '8801',
            'city': 'Chennai'
        }
    }
)

result = response.json()
print(f"Language: {result['language_code']}")

for speaker in result['speakers']:
    print(f"{speaker['speaker_id']}: {speaker['text']}")

# File upload
with open('audio.mp3', 'rb') as f:
    files = {'audio_file': f}
    data = {'seller_buyer_meta_data': '{"seller_identifier":"5901"}'}
    response = requests.post('http://localhost:8888/translate-file', files=files, data=data)
    print(response.json())
```
```

## Docker Deployment

### Build Docker Image

```bash
docker build -t audio-translation-api .
```

### Run Docker Container

**With environment variable:**
```bash
docker run -p 8888:8888 \
  -e SARVAM_API_KEY=your_api_key_here \
  audio-translation-api
```

**With .env file:**
```bash
# Create .env file from template
cp .env.example .env
# Edit .env with your API key

# Run container
docker run -p 8888:8888 --env-file .env audio-translation-api
```

### Run in Background (Detached Mode)

```bash
docker run -d -p 8888:8888 \
  -e SARVAM_API_KEY=your_api_key_here \
  --name audio-translation \
  audio-translation-api
```

### Check Container Status

```bash
# View logs
docker logs audio-translation

# Check health
curl http://localhost:8888/health
```

### Stop Container

```bash
docker stop audio-translation
docker rm audio-translation
```

## Deploy Anywhere

This Docker container can be deployed to:

- **Cloud Platforms**: AWS ECS, Google Cloud Run, Azure Container Instances
- **Kubernetes**: Deploy with kubectl or Helm
- **VPS/Servers**: Any server with Docker installed
- **Platform-as-a-Service**: Heroku, Railway, Render, etc.

### Example: Deploy to Cloud Run (GCP)

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/audio-translation-api

# Deploy to Cloud Run
gcloud run deploy audio-translation-api \
  --image gcr.io/YOUR_PROJECT_ID/audio-translation-api \
  --platform managed \
  --region us-central1 \
  --set-env-vars SARVAM_API_KEY=your_api_key_here
```

## Supported Languages

The API automatically detects and translates from these Indian languages to English:

- **Hindi** (hi-IN)
- **Telugu** (te-IN)
- **Tamil** (ta-IN)
- **Kannada** (kn-IN)
- **Malayalam** (ml-IN)
- **Bengali** (bn-IN)
- **Gujarati** (gu-IN)
- **Marathi** (mr-IN)
- And more...

The `language_code` field in the response indicates which language was detected.

## Project Structure

```
translation/
├── api.py                      # Flask REST API (v2.0)
├── translation_service.py      # Core translation logic
├── app.py                      # CLI version (original)
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── .dockerignore              # Docker ignore rules
├── .gitignore                 # Git ignore rules
├── .env.example               # Environment variables template
├── README.md                  # This file
├── API_V2_FEATURES.md         # v2.0 features documentation
└── RESPONSE_FORMAT.md         # Response format examples
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SARVAM_API_KEY` | SarvamAI API subscription key | khemchandwillprovidethekey | Yes |
| `FLASK_ENV` | Flask environment (development/production) | production | No |
| `PORT` | Port to run the API on | 8888 | No |

## What's New in v2.0

### ✨ New Features
- **Metadata Pass-through**: Include custom metadata in requests and get it back in responses
- **File Upload Support**: New `/translate-file` endpoint for direct file uploads
- **Simplified Response**: Removed `full_transcript`, `start_time`, and `end_time` for cleaner output
- **Multi-language Support**: Explicitly supports Telugu, Hindi, Tamil, and other Indian languages
- **Auto-translation**: All audio is automatically translated to English

### 🔄 Breaking Changes
- Response format changed: removed `full_transcript` field
- Removed `start_time` and `end_time` from speaker entries
- API version bumped to 2.0.0

### 📚 Migration from v1.0
If you were using v1.0, update your code to:
- Remove references to `full_transcript` in responses
- Remove timestamp handling (`start_time`, `end_time`)
- Optionally add `seller_buyer_meta_data` to requests

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `400`: Bad request (missing or invalid parameters)
- `500`: Server error (processing failed)

**Error Response:**
```json
{
  "status": "error",
  "message": "Error description"
}
```

## License

This project uses the SarvamAI API. Please refer to SarvamAI's terms of service for usage limits and licensing.

## Support

For issues or questions:
- Check the API documentation at `http://localhost:8888/`
- Review the health endpoint at `http://localhost:8888/health`
- Check Docker logs: `docker logs audio-translation`



#how to start the project
1. 
docker build -t audio-translation-api .
2. 
docker run -d -p 8888:8888 \
  -e SARVAM_API_KEY=sk_s5zsx47h_vV1ePqgm4ZRa7g8QgEnGgvTF \
  --name audio-translation \
  audio-translation-api

3. 
curl -X POST http://localhost:8888/translate \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://sr.knowlarity.com/vr/fetchsound/?callid=48bdfa3f-2d1b-4ef4-a686-369d4862f106"
  }'

