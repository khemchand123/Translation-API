from sarvamai import SarvamAI
import requests
import os
import tempfile
import json

def main():
    client = SarvamAI(api_subscription_key="khemchandwillprovidethekey")

    # Download audio file from URL
    audio_url = "https://sr.knowlarity.com/vr/fetchsound/?callid=48bdfa3f-2d1b-4ef4-a686-369d4862f106"
    
    print(f"Downloading audio from: {audio_url}")
    response = requests.get(audio_url)
    response.raise_for_status()  # Raise an error for bad status codes
    
    # Save to temporary file
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_audio.write(response.content)
    temp_audio.close()
    
    print(f"Audio downloaded to: {temp_audio.name}")

    # Create and configure batch STTT job
    job = client.speech_to_text_translate_job.create_job(
        model="saaras:v2.5",
        with_diarization=True,
        num_speakers=2,
        prompt="Official meeting"
    )

    # Upload and process files
    audio_paths = [temp_audio.name]
    job.upload_files(file_paths=audio_paths)
    job.start()

    # Wait for completion
    job.wait_until_complete()

    # Check file-level results
    file_results = job.get_file_results()

    print(f"\nSuccessful: {len(file_results['successful'])}")
    for f in file_results['successful']:
        print(f"  ✓ {f['file_name']}")

    print(f"\nFailed: {len(file_results['failed'])}")
    for f in file_results['failed']:
        print(f"  ✗ {f['file_name']}: {f['error_message']}")

    # Handle all files failed
    if len(file_results['successful']) == 0:
        print("\nAll files failed.")
        return

    # Download outputs to temporary directory
    output_dir = tempfile.mkdtemp()
    job.download_outputs(output_dir=output_dir)
    print(f"\nDownloaded {len(file_results['successful'])} file(s) to temporary directory")
    
    # Print translation results
    print("\n" + "="*80)
    print("TRANSLATION RESULTS")
    print("="*80)
    
    for f in file_results['successful']:
        file_name = f['file_name']
        json_path = os.path.join(output_dir, f"{file_name}.json")
        
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as json_file:
                result_data = json.load(json_file)
                
                print(f"\n📄 File: {file_name}")
                print(f"🌐 Language: {result_data.get('language_code', 'N/A')}")
                print(f"\n📝 Full Transcript:")
                print("-" * 80)
                print(result_data.get('transcript', 'No transcript available'))
                print("-" * 80)
                
                # Print diarized transcript if available
                if 'diarized_transcript' in result_data and 'entries' in result_data['diarized_transcript']:
                    print(f"\n🎤 Speaker-by-Speaker Transcript:")
                    print("-" * 80)
                    
                    for entry in result_data['diarized_transcript']['entries']:
                        speaker = entry.get('speaker_id', 'Unknown')
                        text = entry.get('transcript', '')
                        start_time = entry.get('start_time_seconds', 0)
                        end_time = entry.get('end_time_seconds', 0)
                        
                        print(f"[{start_time:.2f}s - {end_time:.2f}s] {speaker}: {text}")
                    
                    print("-" * 80)
    
    print("\n" + "="*80)
    
    # Cleanup temporary directory and files
    try:
        for file in os.listdir(output_dir):
            os.unlink(os.path.join(output_dir, file))
        os.rmdir(output_dir)
        print(f"\n🧹 Cleaned up temporary files")
    except Exception as e:
        print(f"\n⚠️  Warning: Could not delete temporary directory: {e}")
    
    # Cleanup temporary audio file
    try:
        os.unlink(temp_audio.name)
        print(f"🧹 Cleaned up temporary audio file: {temp_audio.name}")
    except Exception as e:
        print(f"⚠️  Warning: Could not delete temporary file {temp_audio.name}: {e}")

if __name__ == "__main__":
    main()

# --- Notebook/Colab usage ---
# main()
