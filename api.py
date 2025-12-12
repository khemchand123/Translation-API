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
    
    Response JSON:
        {
            "status": "success",
            "language_code": "hi-IN",
            "speakers": [...],
            "seller_buyer_meta_data": {...}
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
        metadata = data.get('seller_buyer_meta_data', {})
        
        if not audio_url:
            return jsonify({
                'status': 'error',
                'message': 'Missing required field: audio_url'
            }), 400
        
        # Process audio
        result = translation_service.translate_from_url(audio_url)
        
        # Add metadata to response if provided
        if metadata:
            result['seller_buyer_meta_data'] = metadata
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/translate-file', methods=['POST'])
def translate_audio_file():
    """
    Translate uploaded audio file to text with speaker diarization.
    
    Form Data:
        - audio_file: Audio file (mp3, wav, etc.)
        - seller_buyer_meta_data: JSON string with metadata (optional)
    
    Response JSON:
        {
            "status": "success",
            "language_code": "hi-IN",
            "speakers": [...],
            "seller_buyer_meta_data": {...}
        }
    """
    try:
        # Check if file is present
        if 'audio_file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'Missing required field: audio_file'
            }), 400
        
        audio_file = request.files['audio_file']
        
        if audio_file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400
        
        # Get metadata if provided
        import json
        metadata = {}
        if 'seller_buyer_meta_data' in request.form:
            try:
                metadata = json.loads(request.form['seller_buyer_meta_data'])
            except json.JSONDecodeError:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid JSON in seller_buyer_meta_data'
                }), 400
        
        # Process uploaded file
        result = translation_service.translate_from_file(audio_file)
        
        # Add metadata to response if provided
        if metadata:
            result['seller_buyer_meta_data'] = metadata
        
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
        'version': '2.0.0',
        'endpoints': {
            'POST /translate': {
                'description': 'Translate audio from URL with speaker diarization',
                'request': {
                    'audio_url': 'URL of the audio file to translate (required)',
                    'seller_buyer_meta_data': 'Optional metadata object to include in response'
                },
                'response': {
                    'status': 'success/error',
                    'language_code': 'Detected language code',
                    'speakers': 'Array of speaker-wise transcripts',
                    'seller_buyer_meta_data': 'Metadata passed from request (if provided)'
                }
            },
            'POST /translate-file': {
                'description': 'Translate uploaded audio file with speaker diarization',
                'request': {
                    'audio_file': 'Audio file upload (multipart/form-data)',
                    'seller_buyer_meta_data': 'Optional JSON string with metadata'
                },
                'response': {
                    'status': 'success/error',
                    'language_code': 'Detected language code',
                    'speakers': 'Array of speaker-wise transcripts',
                    'seller_buyer_meta_data': 'Metadata passed from request (if provided)'
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
