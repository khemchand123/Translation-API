from collections import defaultdict
import re
import json
import os
from statistics import mean

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
SAMPLE_FILE = os.path.join(DATA_DIR, 'sample_calls.json')

SAMPLE_CATEGORIES = [
    'Steel Rods',
    'Textiles',
    'Electronics Components',
    'Agriculture Seeds',
    'Packaging Materials',
    'Furniture',
]

SPEC_PATTERNS = [
    r"\b(\d+\s?mm)\b",
    r"\b(\d+\s?kg)\b",
    r"\b(\d+\s?meters?)\b",
    r"\b(\d+\s?units?)\b",
    r"\b(grade\s?[A-D])\b",
]
PRICE_PATTERN = r"(?:INR|Rs\.?|Rupees)\s?(\d{2,7})(?:\s?per\s?(?:kg|unit|meter|piece))?"
QTY_PATTERN = r"\b(\d{1,5})\s?(?:kg|units?|meters?|pieces?)\b"
CITY_STATE_PATTERN = (
    r"\b(Delhi|Mumbai|Kolkata|Chennai|Bengaluru|Hyderabad|Jaipur|Surat|Pune)\b|"
    r"\b(UP|MH|DL|RJ|GJ|TN|WB|KA|TS)\b"
)


def extract_entities(transcript: str):
    # Very simple regex-based extraction as a mock
    specs = []
    for pat in SPEC_PATTERNS:
        specs += re.findall(pat, transcript, flags=re.IGNORECASE)

    prices = [int(p) for p in re.findall(PRICE_PATTERN, transcript, flags=re.IGNORECASE)]
    quantities = [int(q) for q in re.findall(QTY_PATTERN, transcript, flags=re.IGNORECASE)]

    # sentiment heuristic: count positive/negative words
    pos_words = sum(w in transcript.lower() for w in ['good','ok','yes','fine','deal','confirm'])
    neg_words = sum(w in transcript.lower() for w in ['no','delay','price high','issue','problem','cancel'])
    sentiment = 'positive' if pos_words > neg_words else ('negative' if neg_words > pos_words else 'neutral')

    return {
        'specs': list(set(specs)),
        'prices': prices,
        'quantities': quantities,
        'sentiment': sentiment,
    }


def process_call(transcript: str, metadata: dict):
    ents = extract_entities(transcript)
    avg_price = mean(ents['prices']) if ents['prices'] else None
    total_qty = sum(ents['quantities']) if ents['quantities'] else None

    result = {
        'metadata': metadata,
        'transcript': transcript,
        'extracted': ents,
        'derived': {
            'avg_price': avg_price,
            'total_qty': total_qty,
            'price_per_qty': (avg_price / total_qty) if avg_price and total_qty else None,
        }
    }

    # persist to sample file for aggregation demo
    os.makedirs(DATA_DIR, exist_ok=True)
    calls = []
    if os.path.exists(SAMPLE_FILE):
        with open(SAMPLE_FILE, 'r', encoding='utf-8') as f:
            try:
                calls = json.load(f)
            except Exception:
                calls = []
    calls.append(result)
    with open(SAMPLE_FILE, 'w', encoding='utf-8') as f:
        json.dump(calls, f, ensure_ascii=False, indent=2)

    return result


def aggregate_insights():
    # Read saved calls and produce category and location insights
    if not os.path.exists(SAMPLE_FILE):
        return {
            'categories': {},
            'locations': {},
            'overall': {
                'total_calls': 0,
                'cities_covered': [],
                'top_cities': [],
            }
        }

    with open(SAMPLE_FILE, 'r', encoding='utf-8') as f:
        calls = json.load(f)

    cat_prices = defaultdict(list)
    cat_qty = defaultdict(list)
    sentiments = defaultdict(lambda: defaultdict(int))
    location_counts = defaultdict(int)

    for c in calls:
        cat = c['metadata'].get('category_name','Misc')
        city = c['metadata'].get('city','Unknown')
        if c['extracted']['prices']:
            cat_prices[cat] += c['extracted']['prices']
        if c['extracted']['quantities']:
            cat_qty[cat] += c['extracted']['quantities']
        sentiments[cat][c['extracted']['sentiment']] += 1
        location_counts[city] += 1

    categories = {}
    for cat in set(list(cat_prices.keys()) + list(cat_qty.keys()) + list(sentiments.keys())):
        categories[cat] = {
            'avg_price': round(mean(cat_prices[cat]), 2) if cat_prices[cat] else None,
            'avg_qty': round(mean(cat_qty[cat]), 2) if cat_qty[cat] else None,
            'sentiment': sentiments[cat],
        }

    top_cities = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:5] if location_counts else []
    
    overall = {
        'total_calls': len(calls),
        'cities_covered': sorted(location_counts.keys()) if location_counts else [],
        'top_cities': top_cities,
    }

    return {
        'categories': categories,
        'locations': dict(location_counts),
        'overall': overall,
    }
