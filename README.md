# Audio Translation API

A Flask REST API wrapper for audio translation with speaker diarization using SarvamAI. This service downloads audio from URLs, transcribes and translates the content, and returns speaker-wise transcripts with timestamps.

## Features

- 🎤 **Audio Translation**: Transcribe and translate audio files from URLs
- 👥 **Speaker Diarization**: Separate and identify different speakers
- 🌐 **Language Detection**: Automatic language identification
- 🐳 **Docker Ready**: Easy deployment with Docker
- 🔍 **Health Monitoring**: Built-in health check endpoint

## API Endpoints

### `POST /translate`

Translate audio from URL with speaker diarization.

**Request:**
```json
{
  "audio_url": "https://example.com/audio.mp3"
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
  ]
}
```

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

**Using cURL:**
```bash
curl -X POST http://localhost:8888/translate \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://sr.knowlarity.com/vr/fetchsound/?callid=48bdfa3f-2d1b-4ef4-a686-369d4862f106"
  }'
```

**Using Python:**
```python
import requests

response = requests.post(
    'http://localhost:8888/translate',
    json={'audio_url': 'https://example.com/audio.mp3'}
)

result = response.json()
print(f"Language: {result['language_code']}")

for speaker in result['speakers']:
    print(f"{speaker['speaker_id']}: {speaker['text']}")
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

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SARVAM_API_KEY` | SarvamAI API subscription key | - | Yes |
| `FLASK_ENV` | Flask environment (development/production) | production | No |
| `PORT` | Port to run the API on | 8888 | No |

## Project Structure

```
translation/
├── api.py                    # Flask REST API
├── translation_service.py    # Core translation logic
├── app.py                    # CLI version (original)
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── .dockerignore            # Docker ignore rules
├── .env.example             # Environment variables template
└── README.md                # This file
```

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

