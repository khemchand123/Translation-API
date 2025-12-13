"""
Seed script to populate sample buyer-seller call data for demo purposes.
Run this before starting the app to see pre-populated insights.
"""
import json
import os
from datetime import datetime, timedelta
import random

DATA_DIR = 'data'
SAMPLE_FILE = os.path.join(DATA_DIR, 'sample_calls.json')

# Mock transcripts for different categories
MOCK_TRANSCRIPTS = {
    'Steel Rods': [
        "Hello, I need 500 kg of 12 mm steel rods for construction. What's your price? Seller: Rs 45000 per ton, we deliver in Delhi. Buyer: Good, send me the specs grade A. Deal confirmed.",
        "Hi, looking for steel rods 16 mm. How much for 200 kg? Seller: INR 9500. Buyer: Price is a bit high. Can you do Rs 9000? Seller: Okay fine, 9000 per 200kg.",
        "Need TMT bars urgently, 10 mm size. 1000 kg quantity. Seller: Rs 48 per kg. Grade B available. Buyer: Yes ok, please confirm delivery to Mumbai by Thursday.",
    ],
    'Textiles': [
        "I want 500 meters of cotton fabric for garment manufacturing. Seller: Rs 120 per meter, good quality. Buyer: Send samples first. Seller: Yes sure, will courier today.",
        "Hello, do you have silk fabric? Need 200 meters. Seller: Yes, Rs 450 per meter. Premium quality. Buyer: Price okay, but need it in Bengaluru. Seller: We deliver, no problem.",
        "Looking for polyester blend 300 meters. Seller: INR 85 per meter. Buyer: Good deal, confirm the order.",
    ],
    'Electronics Components': [
        "Need 1000 units of resistors 10k ohm. What price? Seller: Rs 2 per piece. Buyer: Okay good, ship to Hyderabad. Seller: Done, will dispatch tomorrow.",
        "Hi, I want microcontrollers ESP32. 200 units needed. Seller: INR 250 per unit. Buyer: Price is okay. Send invoice. Seller: Yes, confirmed.",
        "Looking for capacitors 100uF. 500 pieces. Seller: Rs 5 per piece. Buyer: Deal fine, please pack properly for shipping.",
    ],
    'Agriculture Seeds': [
        "I need wheat seeds for 50 acres. How much per kg? Seller: Rs 45 per kg, certified seeds. Buyer: Good variety? Seller: Yes grade A, high yield. Buyer: Okay send 200 kg to Jaipur.",
        "Want rice seeds, 100 kg. Seller: INR 60 per kg. Buyer: Delivery to Pune? Seller: Yes we deliver. Buyer: Fine, confirm order.",
        "Need corn seeds urgently. 150 kg. Seller: Rs 55 per kg. Buyer: Good, ship to Surat tomorrow.",
    ],
    'Packaging Materials': [
        "Hello, need corrugated boxes for packaging. 500 units, what size available? Seller: 12x10x8 inches, Rs 25 per box. Buyer: Good, confirm order for Chennai delivery.",
        "I want plastic containers 1 liter size. 1000 pieces. Seller: INR 15 per piece. Buyer: Okay deal, send to Kolkata. Seller: Yes confirmed.",
        "Need bubble wrap rolls. 200 meters. Seller: Rs 35 per meter. Buyer: Price okay, please dispatch today.",
    ],
    'Furniture': [
        "Looking for office chairs. Need 50 units. Seller: Rs 3500 per chair, ergonomic design. Buyer: Good quality? Seller: Yes premium. Buyer: Okay confirm, deliver to Delhi office.",
        "Hi, want wooden desks. 20 pieces needed. Seller: INR 8500 per desk. Buyer: Price fine, send dimensions. Seller: Will share catalog.",
        "Need conference table. 5 meter size. Seller: Rs 45000 for custom made. Buyer: Good, finalize the design and confirm.",
    ],
}

CITIES = ['Delhi', 'Mumbai', 'Bengaluru', 'Hyderabad', 'Chennai', 'Kolkata', 'Jaipur', 'Surat', 'Pune']
STATES = {
    'Delhi': 'Delhi', 'Mumbai': 'Maharashtra', 'Bengaluru': 'Karnataka',
    'Hyderabad': 'Telangana', 'Chennai': 'Tamil Nadu', 'Kolkata': 'West Bengal',
    'Jaipur': 'Rajasthan', 'Surat': 'Gujarat', 'Pune': 'Maharashtra'
}

def generate_seed_data():
    """Generate realistic mock call data across all categories"""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    calls = []
    call_id = 1
    base_time = datetime.now() - timedelta(days=30)
    
    for category, transcripts in MOCK_TRANSCRIPTS.items():
        for i, transcript in enumerate(transcripts):
            city = random.choice(CITIES)
            timestamp = (base_time + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))).isoformat()
            
            # Extract mock entities (simplified version of pipeline logic)
            import re
            prices = [int(p) for p in re.findall(r"(?:INR|Rs\.?|Rupees)\s?(\d{2,7})", transcript, re.IGNORECASE)]
            quantities = [int(q) for q in re.findall(r"\b(\d{1,5})\s?(?:kg|units?|meters?|pieces?)\b", transcript, re.IGNORECASE)]
            
            # Simple sentiment
            pos_words = sum(w in transcript.lower() for w in ['good', 'ok', 'yes', 'fine', 'deal', 'confirm'])
            neg_words = sum(w in transcript.lower() for w in ['no', 'delay', 'high', 'issue', 'problem', 'cancel'])
            sentiment = 'positive' if pos_words > neg_words else ('negative' if neg_words > pos_words else 'neutral')
            
            avg_price = sum(prices) / len(prices) if prices else None
            total_qty = sum(quantities) if quantities else None
            
            call = {
                'metadata': {
                    'buyer_id': f'B-{call_id:03d}',
                    'seller_id': f'S-{call_id:03d}',
                    'category_id': category.lower().replace(' ', '_'),
                    'category_name': category,
                    'city': city,
                    'state': STATES[city],
                    'timestamp': timestamp,
                    'duration': random.randint(60, 300),
                },
                'transcript': transcript,
                'extracted': {
                    'specs': [],
                    'prices': prices,
                    'quantities': quantities,
                    'sentiment': sentiment,
                },
                'derived': {
                    'avg_price': avg_price,
                    'total_qty': total_qty,
                    'price_per_qty': (avg_price / total_qty) if avg_price and total_qty else None,
                }
            }
            calls.append(call)
            call_id += 1
    
    with open(SAMPLE_FILE, 'w', encoding='utf-8') as f:
        json.dump(calls, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Generated {len(calls)} sample calls across {len(MOCK_TRANSCRIPTS)} categories")
    print(f"✓ Data saved to {SAMPLE_FILE}")
    print(f"\nCategories: {', '.join(MOCK_TRANSCRIPTS.keys())}")
    print(f"Cities covered: {', '.join(set(c['metadata']['city'] for c in calls))}")

if __name__ == '__main__':
    generate_seed_data()
