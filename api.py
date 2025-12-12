from flask import Flask, request, jsonify
import os
from translation_service import TranslationService

app = Flask(__name__)

# Initialize translation service
API_KEY = os.getenv('SARVAM_API_KEY', 'khemchandwillprovidethekey')
translation_service = TranslationService(api_key=API_KEY)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'service': 'audio-translation-api'
    }), 200


@app.route('/translate', methods=['POST'])
def translate_audio():
    """
    Translate audio from URL to text with speaker diarization.
    
    Request JSON:
        {
            "audio_url": "https://example.com/audio.mp3"
        }
    
    Response JSON:
        {
            "status": "success",
            "language_code": "hi-IN",
            "full_transcript": "Complete transcript text...",
            "speakers": [
                {
                    "speaker_id": "speaker_1",
                    "text": "Hello",
                    "start_time": 0.5,
                    "end_time": 1.2
                },
                ...
            ]
        }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                'status': 'error',
                'message': 'Request must be JSON'
            }), 400
        
        data = request.get_json()
        audio_url = data.get('audio_url')
        
        if not audio_url:
            return jsonify({
                'status': 'error',
                'message': 'Missing required field: audio_url'
            }), 400
        
        # Process audio
        result = translation_service.translate_from_url(audio_url)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/', methods=['GET'])
def index():
    """API documentation endpoint."""
    return jsonify({
        'service': 'Audio Translation API',
        'version': '1.0.0',
        'endpoints': {
            'POST /translate': {
                'description': 'Translate audio from URL with speaker diarization',
                'request': {
                    'audio_url': 'URL of the audio file to translate'
                },
                'response': {
                    'status': 'success/error',
                    'language_code': 'Detected language code',
                    'full_transcript': 'Complete transcript',
                    'speakers': 'Array of speaker-wise transcripts with timestamps'
                }
            },
            'GET /health': {
                'description': 'Health check endpoint',
                'response': {
                    'status': 'healthy'
                }
            }
        }
    }), 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8888))
    debug = os.getenv('FLASK_ENV', 'production') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
