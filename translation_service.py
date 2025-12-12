from sarvamai import SarvamAI
import requests
import os
import tempfile
import json


class TranslationService:
    """Service class for handling audio translation using SarvamAI API."""
    
    def __init__(self, api_key):
        """Initialize the translation service with API key.
        
        Args:
            api_key (str): SarvamAI API subscription key
        """
        self.client = SarvamAI(api_subscription_key=api_key)
    
    def download_audio(self, audio_url):
        """Download audio file from URL and save to temporary file.
        
        Args:
            audio_url (str): URL of the audio file to download
            
        Returns:
            str: Path to the downloaded temporary file
            
        Raises:
            requests.RequestException: If download fails
        """
        response = requests.get(audio_url, timeout=30)
        response.raise_for_status()
        
        # Save to temporary file
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_audio.write(response.content)
        temp_audio.close()
        
        return temp_audio.name
    
    def process_audio(self, audio_path):
        """Process audio file using SarvamAI speech-to-text-translate service.
        
        Args:
            audio_path (str): Path to the audio file
            
        Returns:
            dict: Translation results containing transcript and diarization
            
        Raises:
            Exception: If processing fails
        """
        # Create and configure batch STTT job
        job = self.client.speech_to_text_translate_job.create_job(
            model="saaras:v2.5",
            with_diarization=True,
            num_speakers=2,
            prompt="Official meeting"
        )
        
        # Upload and process files
        job.upload_files(file_paths=[audio_path])
        job.start()
        
        # Wait for completion
        job.wait_until_complete()
        
        # Check file-level results
        file_results = job.get_file_results()
        
        if len(file_results['successful']) == 0:
            error_msg = "Audio processing failed"
            if file_results['failed']:
                error_msg = file_results['failed'][0].get('error_message', error_msg)
            raise Exception(error_msg)
        
        # Download outputs to temporary directory
        output_dir = tempfile.mkdtemp()
        job.download_outputs(output_dir=output_dir)
        
        # Read the result JSON
        file_name = file_results['successful'][0]['file_name']
        json_path = os.path.join(output_dir, f"{file_name}.json")
        
        with open(json_path, 'r', encoding='utf-8') as json_file:
            result_data = json.load(json_file)
        
        # Cleanup
        os.unlink(json_path)
        os.rmdir(output_dir)
        
        return result_data
    
    def format_response(self, result_data):
        """Format the translation result into a clean API response.
        
        Args:
            result_data (dict): Raw result data from SarvamAI
            
        Returns:
            dict: Formatted response with status, language, and speakers
        """
        speakers = []
        
        if 'diarized_transcript' in result_data and 'entries' in result_data['diarized_transcript']:
            for entry in result_data['diarized_transcript']['entries']:
                speakers.append({
                    'speaker_id': entry.get('speaker_id', 'Unknown'),
                    'text': entry.get('transcript', '')
                })
        
        return {
            'status': 'success',
            'language_code': result_data.get('language_code', 'N/A'),
            'speakers': speakers
        }
    
    def translate_from_url(self, audio_url):
        """Complete translation workflow from URL to formatted response.
        
        Args:
            audio_url (str): URL of the audio file
            
        Returns:
            dict: Formatted translation response
            
        Raises:
            Exception: If any step fails
        """
        temp_file = None
        try:
            # Download audio
            temp_file = self.download_audio(audio_url)
            
            # Process audio
            result_data = self.process_audio(temp_file)
            
            # Format response
            return self.format_response(result_data)
        
        finally:
            # Cleanup temporary file
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except Exception:
                    pass  # Ignore cleanup errors
