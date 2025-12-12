# New API Response Format Example

## Request
```bash
curl -X POST http://localhost:8888/translate \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://sr.knowlarity.com/vr/fetchsound/?callid=48bdfa3f-2d1b-4ef4-a686-369d4862f106"
  }'
```

## New Response Format (Simplified)
```json
{
  "status": "success",
  "language_code": "hi-IN",
  "speakers": [
    {
      "speaker_id": "speaker_1",
      "text": "Yes sir."
    },
    {
      "speaker_id": "speaker_2",
      "text": "Yes."
    },
    {
      "speaker_id": "speaker_1",
      "text": "Yes."
    },
    {
      "speaker_id": "speaker_2",
      "text": "So if you want to connect now, let's do it now."
    },
    {
      "speaker_id": "speaker_1",
      "text": "Yes, I will do it now sir, because it will be better. The seniors were sitting, I will take them on a video call too. It will be better."
    }
  ]
}
```

## What Changed

### ❌ Removed Fields:
- `full_transcript` - No longer included in response
- `start_time` - Removed from each speaker entry
- `end_time` - Removed from each speaker entry

### ✅ Kept Fields:
- `status` - Success/error status
- `language_code` - Detected language (e.g., "hi-IN")
- `speakers` - Array of speaker entries
  - `speaker_id` - Speaker identifier (e.g., "speaker_1", "speaker_2")
  - `text` - What the speaker said

## Benefits
- **Cleaner response** - Only essential information
- **Smaller payload** - Faster API responses
- **Easier to parse** - Simpler data structure
- **Focus on content** - Speaker dialogue without timing complexity
