# Test Metadata Samples for Upload Form

## Sample 1: Tab-Separated Format (Copy both lines)
```
buyer_identifier	seller_identifier	city_name	state_name	mcat_name	mcat_id	pns_call_modrefname
24028768	91737092	Jamnagar	Gujarat	Wheat Cleaning Machine	140835	Automatic Powder Coated Wheat Cleaning Machine farmar use, Single Phase
```

## Sample 2: JSON Format (Copy entire JSON)
```json
{
  "seller_identifier": "91737092",
  "buyer_identifier": "24028768",
  "city": "Jamnagar",
  "state": "Gujarat",
  "mcat_name": "Wheat Cleaning Machine",
  "mcat_id": "140835",
  "main_product": "Automatic Powder Coated Wheat Cleaning Machine farmar use, Single Phase"
}
```

## Sample 3: Another Tab-Separated Example
```
buyer_identifier	seller_identifier	city_name	state_name	mcat_name	mcat_id_x	pns_call_modrefname
8801	5901	Chennai	Tamil Nadu	Commercial Kitchen Equipment	5570	Stainless Steel Kitchen Equipment
```

## Test Audio URL
```
https://storage.googleapis.com/im-model-product/pns/0d8b44731c1a7a2afb2f9773d4e76cc762c606cf72dcec698a7453064f5680b.mp3?X-Goog-Algorithm=GOOG4-RSA-SHA256
```

## How to Test:

1. Go to http://127.0.0.1:5000
2. Click on "Audio File URL" tab
3. Paste the audio URL in the "Audio File URL" field
4. Paste one of the metadata samples (tab-separated or JSON) in the "Call Metadata" field
5. Click "🚀 Process & Analyze Call"
6. Check the terminal/console for detailed logs showing:
   - 📤 Input parameters sent to webhook
   - 📥 Response received from webhook

## Expected Console Output Format:

```
================================================================================
📤 SENDING TO WEBHOOK - AUDIO URL
================================================================================
{
  "audio_url": "https://storage.googleapis.com/...",
  "seller_buyer_meta_data": {
    "seller_identifier": "91737092",
    "buyer_identifier": "24028768",
    "city": "Jamnagar",
    "state": "Gujarat",
    "mcat_name": "Wheat Cleaning Machine",
    "mcat_id": "140835",
    "main_product": "Automatic Powder Coated Wheat Cleaning Machine"
  }
}
================================================================================

================================================================================
📥 WEBHOOK RESPONSE
================================================================================
Status Code: 200
Response Headers: {...}
Response Body: {...}
================================================================================
```
