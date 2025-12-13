import json
import os
import requests
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, Response, stream_with_context
from werkzeug.utils import secure_filename
from .services.pipeline import process_call, aggregate_insights, SAMPLE_CATEGORIES
from .company_service import company_service
import csv
import time
import queue
import threading
import random

bp = Blueprint('main', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg', 'webm', 'csv'}

# Store for bulk processing results
bulk_results = {
    'states': {},  # state_name: {calls: [], cities: set(), categories: set(), positive: 0, negative: 0, neutral: 0}
    'processing': False,
    'total_calls': 0,
    'processed_calls': 0
}

# Queue for SSE updates
update_queue = queue.Queue()

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        # Initialize variables
        audio_file = None
        audio_url = None
        transcript = None
        is_bulk_processing = False  # Flag to skip GST validation for bulk processing
        
        # Check if JSON request (from bulk processing)
        if request.is_json:
            data = request.get_json()
            audio_url = data.get('audio_url')
            metadata = data.get('metadata', {})
            is_bulk_processing = True  # Mark as bulk processing to skip GST validation
            
            # Convert metadata dict to seller_buyer_meta_data format
            seller_buyer_meta_data = {
                'seller_identifier': metadata.get('seller_identifier', ''),
                'buyer_identifier': metadata.get('buyer_identifier', ''),
                'city': metadata.get('city_name', metadata.get('city', '')),
                'state': metadata.get('state_name', metadata.get('state', '')),
                'mcat_name': metadata.get('mcat_name', ''),
                'mcat_id': metadata.get('mcat_id', ''),
                'main_product': metadata.get('pns_call_modrefname', metadata.get('main_product', ''))
            }
        else:
            # Handle form data (from upload page)
            audio_file = request.files.get('audio_file')
            audio_url = request.form.get('audio_url')
            transcript = request.form.get('transcript')
            metadata_raw = request.form.get('metadata', '')
            
            # Parse metadata into structured format
            seller_buyer_meta_data = parse_metadata(metadata_raw)
        
        try:
            # Handle audio file upload
            if audio_file and audio_file.filename:
                if allowed_file(audio_file.filename):
                    filename = secure_filename(audio_file.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    audio_file.save(filepath)
                    
                    # Prepare multipart form data
                    files_to_send = {'audio_file': (filename, open(filepath, 'rb'), 'audio/mpeg')}
                    data_to_send = {
                        'seller_buyer_meta_data': json.dumps(seller_buyer_meta_data),
                        'summary': 'true'
                    }
                    
                    print("\n" + "="*80)
                    print("📤 SENDING TO WEBHOOK - AUDIO FILE UPLOAD")
                    print("="*80)
                    print(f"File: {filename}")
                    print(f"Metadata: {json.dumps(seller_buyer_meta_data, indent=2)}")
                    print("="*80 + "\n")
                    
                    response = requests.post(
                        'https://imworkflow.intermesh.net/webhook/buyer-seller-insight',
                        data=data_to_send,
                        files=files_to_send
                    )
                    
                    print("\n" + "="*80)
                    print("📥 WEBHOOK RESPONSE")
                    print("="*80)
                    print(f"Status Code: {response.status_code}")
                    print(f"Response Body: {response.text}")
                    print("="*80 + "\n")
                else:
                    return jsonify({'error': 'Invalid file type'}), 400
            
            # Handle audio URL - send as JSON
            elif audio_url:
                webhook_payload = {
                    'audio_url': audio_url,
                    'seller_buyer_meta_data': seller_buyer_meta_data,
                    'summary': True
                }
                
                print("\n" + "="*80)
                print("📤 SENDING TO WEBHOOK - AUDIO URL")
                print("="*80)
                print(json.dumps(webhook_payload, indent=2))
                print("="*80 + "\n")
                
                response = requests.post(
                    'https://imworkflow.intermesh.net/webhook/buyer-seller-insight',
                    headers={'Content-Type': 'application/json'},
                    json=webhook_payload
                )
                
                print("\n" + "="*80)
                print("📥 WEBHOOK RESPONSE")
                print("="*80)
                print(f"Status Code: {response.status_code}")
                print(f"Response Headers: {dict(response.headers)}")
                print(f"Response Body: {response.text}")
                print("="*80 + "\n")
                
                # Check if webhook returned error
                if response.status_code >= 400:
                    error_msg = f"Webhook error ({response.status_code}): {response.text}"
                    print(f"❌ {error_msg}")
                    return jsonify({
                        'error': error_msg,
                        'webhook_status': response.status_code,
                        'webhook_response': response.text,
                        'payload_sent': webhook_payload
                    }), 500
            
            # Handle transcript - send as JSON
            elif transcript:
                webhook_payload = {
                    'transcript': transcript,
                    'seller_buyer_meta_data': seller_buyer_meta_data
                }
                
                print("\n" + "="*80)
                print("📤 SENDING TO WEBHOOK - TRANSCRIPT")
                print("="*80)
                print(json.dumps(webhook_payload, indent=2))
                print("="*80 + "\n")
                
                response = requests.post(
                    'https://imworkflow.intermesh.net/webhook/buyer-seller-insight',
                    headers={'Content-Type': 'application/json'},
                    json=webhook_payload
                )
                
                print("\n" + "="*80)
                print("📥 WEBHOOK RESPONSE")
                print("="*80)
                print(f"Status Code: {response.status_code}")
                print(f"Response Body: {response.text}")
                print("="*80 + "\n")
            else:
                return jsonify({'error': 'No input provided'}), 400
            
            # Check webhook response
            if response.status_code in [200, 201]:
                try:
                    response_data = response.json()
                    
                    # GST Validation - ONLY for single uploads (not bulk processing)
                    # Bulk processing skips this to preserve API trial limits (max 20 calls)
                    gst_validation = None
                    if not is_bulk_processing:  # Only validate for single upload page
                        if response_data and isinstance(response_data, list) and len(response_data) > 0:
                            output = response_data[0].get('output', {})
                            seller_id = output.get('seller_identifier') or seller_buyer_meta_data.get('seller_identifier')
                            
                            if seller_id:
                                print(f"\n🔍 Validating seller: {seller_id}")
                                
                                # Get products from conversation
                                conversation_products = []
                                if output.get('products'):
                                    for product in output['products']:
                                        if isinstance(product, dict) and product.get('product_name'):
                                            conversation_products.append(product['product_name'])
                                if output.get('mcat_name'):
                                    conversation_products.append(output['mcat_name'])
                                if output.get('main_product'):
                                    conversation_products.append(output['main_product'])
                                
                                # Remove duplicates
                                conversation_products = list(set(conversation_products))
                                
                                print(f"📦 Products in conversation: {conversation_products}")
                                
                                if conversation_products:
                                    gst_validation = company_service.validate_seller_products(
                                        seller_id, 
                                        conversation_products
                                    )
                                    print(f"✅ GST Validation: {gst_validation['validation_status']}")
                    else:
                        print(f"\n⏭️  Skipping GST validation for bulk processing (preserving API trial limits)")
                    
                    return jsonify({
                        'success': True, 
                        'message': 'Call processed successfully',
                        'webhook_response': response_data,
                        'gst_validation': gst_validation
                    })
                except:
                    return jsonify({
                        'success': True, 
                        'message': 'Call processed successfully',
                        'webhook_response': response.text
                    })
            elif response.status_code == 404:
                return jsonify({
                    'error': 'Webhook not registered',
                    'message': 'The webhook "buyer-seller-insight" is not registered. Please click the "Execute workflow" button in your workflow canvas first.',
                    'details': response.text,
                    'status': response.status_code
                }), 404
            else:
                return jsonify({
                    'error': f'Webhook error: {response.status_code}',
                    'details': response.text
                }), 500
                
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}\n")
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500
    
    return render_template('upload.html', categories=SAMPLE_CATEGORIES)

def parse_metadata(metadata_raw):
    """Parse metadata from tab-separated or JSON format"""
    if not metadata_raw or not metadata_raw.strip():
        return {}
    
    metadata_raw = metadata_raw.strip()
    
    print(f"\n🔍 DEBUG: Raw metadata received:")
    print(f"Length: {len(metadata_raw)}")
    print(f"Content: {repr(metadata_raw)}")
    print(f"Lines: {metadata_raw.split(chr(10))}\n")
    
    # Try to parse as JSON first
    if metadata_raw.startswith('{'):
        try:
            parsed = json.loads(metadata_raw)
            print(f"✅ Parsed as JSON: {parsed}")
            return parsed
        except Exception as e:
            print(f"❌ JSON parse failed: {e}")
            pass
    
    # Parse tab-separated format (handle both \n and \r\n)
    lines = [line.strip() for line in metadata_raw.replace('\r\n', '\n').split('\n') if line.strip()]
    
    print(f"🔍 Split into {len(lines)} lines")
    
    if len(lines) >= 2:
        # First line: headers, second line: values
        headers = [h.strip() for h in lines[0].split('\t')]
        values = [v.strip() for v in lines[1].split('\t')]
        
        print(f"📋 Headers ({len(headers)}): {headers}")
        print(f"📋 Values ({len(values)}): {values}")
        
        # Map to the required structure
        metadata_dict = dict(zip(headers, values))
        
        # Map all available fields from the metadata
        result = {
            'seller_identifier': metadata_dict.get('seller_identifier', ''),
            'buyer_identifier': metadata_dict.get('buyer_identifier', ''),
            'city': metadata_dict.get('city_name', metadata_dict.get('city', '')),
            'state': metadata_dict.get('state_name', metadata_dict.get('state', '')),
            'mcat_name': metadata_dict.get('mcat_name', ''),
            'mcat_id': metadata_dict.get('mcat_id_x', metadata_dict.get('mcat_id', metadata_dict.get('mcat_id_y', ''))),
            'main_product': metadata_dict.get('pns_call_modrefname', metadata_dict.get('main_product', '')),
            # Include all extra fields that were in the input
            **{k: v for k, v in metadata_dict.items() if k not in ['seller_identifier', 'buyer_identifier', 'city_name', 'city', 'state_name', 'state', 'mcat_name', 'mcat_id', 'mcat_id_x', 'mcat_id_y', 'pns_call_modrefname', 'main_product']}
        }
        
        print(f"✅ Parsed metadata: {json.dumps(result, indent=2)}")
        return result
    
    print(f"⚠️ Not enough lines for tab-separated format")
    # Default empty structure
    return {}

@bp.route('/bulk-processing')
def bulk_processing():
    return render_template('bulk_processing.html', results=bulk_results)

@bp.route('/bulk-upload', methods=['POST'])
def bulk_upload():
    if 'csv_file' not in request.files:
        return jsonify({'error': 'No CSV file provided'}), 400
    
    csv_file = request.files['csv_file']
    if not csv_file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be CSV format'}), 400
    
    # Reset bulk results
    bulk_results['states'] = {}
    bulk_results['processing'] = True
    bulk_results['total_calls'] = 0
    bulk_results['processed_calls'] = 0
    
    # Save CSV
    filename = secure_filename(csv_file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    csv_file.save(filepath)
    
    # Start processing in background thread
    thread = threading.Thread(target=process_bulk_csv, args=(filepath,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'message': 'Processing started'})

@bp.route('/bulk-stream')
def bulk_stream():
    """Server-Sent Events endpoint for real-time updates"""
    def generate():
        while True:
            try:
                # Wait for updates with timeout
                update = update_queue.get(timeout=1)
                yield f"data: {json.dumps(update)}\n\n"
            except queue.Empty:
                # Send heartbeat to keep connection alive
                yield f"data: {{\"heartbeat\": true}}\n\n"
            
            # Stop if processing complete
            if not bulk_results['processing'] and update_queue.empty():
                break
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

def process_bulk_csv(filepath):
    """Process CSV file and send real-time updates"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            bulk_results['total_calls'] = len(rows)
            
            for idx, row in enumerate(rows):
                # Extract data from CSV
                state = row.get('state', 'Unknown')
                city = row.get('city', '')
                category = row.get('category', 'General')
                transcript = row.get('transcript', '')
                audio_url = row.get('audio_url', '')
                
                # Initialize state if not exists
                if state not in bulk_results['states']:
                    bulk_results['states'][state] = {
                        'calls': [],
                        'cities': set(),
                        'categories': set(),
                        'positive': 0,
                        'negative': 0,
                        'neutral': 0,
                        'call_count': 0
                    }
                
                # Simulate processing (in real scenario, call webhook and get structured output)
                time.sleep(0.05)  # Simulate processing time
                
                # Mock sentiment (in production, extract from structured output)
                sentiment = random.choice(['positive', 'positive', 'neutral', 'negative'])
                
                # Update state data
                state_data = bulk_results['states'][state]
                state_data['call_count'] += 1
                state_data['calls'].append({
                    'transcript': transcript[:100] if transcript else 'No transcript',
                    'category': category,
                    'city': city,
                    'audio_url': audio_url
                })
                if city:
                    state_data['cities'].add(city)
                state_data['categories'].add(category)
                state_data[sentiment] += 1
                
                bulk_results['processed_calls'] = idx + 1
                
                # Send update via SSE
                update_queue.put({
                    'state': state,
                    'call_count': state_data['call_count'],
                    'processed': bulk_results['processed_calls'],
                    'total': bulk_results['total_calls'],
                    'cities_count': len(state_data['cities']),
                    'categories': list(state_data['categories']),
                    'positive': state_data['positive'],
                    'negative': state_data['negative'],
                    'neutral': state_data['neutral']
                })
                
        bulk_results['processing'] = False
        update_queue.put({'complete': True})
        
    except Exception as e:
        bulk_results['processing'] = False
        update_queue.put({'error': str(e)})

@bp.route('/state-details/<state_name>')
def state_details(state_name):
    """Get detailed information for a specific state"""
    if state_name in bulk_results['states']:
        state_data = bulk_results['states'][state_name]
        return jsonify({
            'state': state_name,
            'call_count': state_data['call_count'],
            'cities': list(state_data['cities']),
            'categories': list(state_data['categories']),
            'sentiment': {
                'positive': state_data['positive'],
                'negative': state_data['negative'],
                'neutral': state_data['neutral']
            },
            'recent_calls': state_data['calls'][-10:]  # Last 10 calls
        })
    return jsonify({'error': 'State not found'}), 404

@bp.route('/api/aggregate')
def api_aggregate():
    return jsonify(aggregate_insights())
