# API v2.0 - New Features

## 1. Metadata Support

You can now pass `seller_buyer_meta_data` in your request, and it will be included in the response.

### Example Request with Metadata:

```bash
curl -X POST http://localhost:8888/translate \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://storage.googleapis.com/im-model-product/pns/e6cfac340062588533cbdc8d2a1b4debe9f98510d615c3e26d60fcc33dae1e04.mp3?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=mayank-docker%40model-product.iam.gserviceaccount.com%2F20251212%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20251212T091332Z&X-Goog-Expires=604800&X-Goog-SignedHeaders=host&X-Goog-Signature=0da02ca6cbc1e2a05a14f010e836104f40d4b31c94b0729ea622ca380386c67dc565a51a82af8b0ff35f691abc00bf565d9c507f6cdad3dd79c8fa671be5c1b3d10facc2f9451e8cfc980eca0dc78c721f41b519cd191ab319b87206e13db0be8e46fe229f55cf7781c630ff6f6456ea8579f966124f6fc6bdda508b399709e2a5825aa36448018186c84d4d0ce59ec039d0e1e7d36a940b76b75ce8f9279b8eeb3af64ff978d94332bbec05bb1de7878c13abcbe15e1cb4458817babe1fc3514a97759fe259459aeef3d3419714aa0fc4813bc15d8f12a8d6155abb1673f1781f8a5bb9360e326e81e2432e8a8ba2cc7f9e945791bd87f03f6dc701df8b5196",
    "seller_buyer_meta_data": {
      "seller_identifier": "5901",
      "buyer_identifier": "8801",
      "city": "Chennai",
      "state": "Tamil Nadu",
      "mcat_name": "Commercial Kitchen Equipment",
      "mcat_id": "5570",
      "main_product": "Product Name"
    }
  }'
```

### Response with Metadata:

```json
{
  "status": "success",
  "language_code": "te-IN",
  "speakers": [
    {
      "speaker_id": "speaker_1",
      "text": "Hello, how are you?"
    },
    {
      "speaker_id": "speaker_2",
      "text": "I am fine, thank you"
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

---

## 2. File Upload Support

New endpoint `/translate-file` allows you to upload audio files directly instead of providing a URL.

### Example: Upload Audio File

```bash
curl -X POST http://localhost:8888/translate-file \
  -F "audio_file=@/path/to/your/audio.mp3" \
  -F 'seller_buyer_meta_data={"seller_identifier":"5901","buyer_identifier":"8801","city":"Chennai","state":"Tamil Nadu","mcat_name":"Commercial Kitchen Equipment","mcat_id":"5570","main_product":"Product Name"}'
```

### Python Example with File Upload:

```python
import requests

# Upload file with metadata
with open('audio.mp3', 'rb') as audio_file:
    files = {'audio_file': audio_file}
    data = {
        'seller_buyer_meta_data': json.dumps({
            "seller_identifier": "5901",
            "buyer_identifier": "8801",
            "city": "Chennai",
            "state": "Tamil Nadu",
            "mcat_name": "Commercial Kitchen Equipment",
            "mcat_id": "5570",
            "main_product": "Product Name"
        })
    }
    
    response = requests.post(
        'http://localhost:8888/translate-file',
        files=files,
        data=data
    )
    
    result = response.json()
    print(result)
```

---

## API Endpoints Summary

### 1. POST /translate (URL-based)
- **Input**: Audio URL + optional metadata
- **Use case**: When audio is already hosted somewhere

### 2. POST /translate-file (File upload)
- **Input**: Audio file upload + optional metadata  
- **Use case**: When you have the audio file locally

### 3. GET /health
- **Health check endpoint**

### 4. GET /
- **API documentation**

---

## Key Features

✅ **Metadata Pass-through**: Any metadata you send is returned in the response  
✅ **Dual Input Methods**: Support both URL and file upload  
✅ **Language Detection**: Automatically detects source language  
✅ **Auto Translation**: Translates to English automatically  
✅ **Speaker Diarization**: Separates different speakers  
✅ **Clean Response**: Only essential data (no timestamps, no full transcript)
