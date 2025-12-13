# Buyer–Seller Voice Insights (Hackathon Demo)

End-to-end mock solution demonstrating insights pipeline from buyer–seller conversations for IndiaMART hackathon.

## Features
- **Per-call processing**: Extract specs, prices, quantities, sentiment (regex + heuristic NLP)
- **Aggregated insights**: Category-level and city-level analytics
- **Interactive dashboard**: Plotly visualizations, dark theme UI
- **6 categories demo-ready**: Steel Rods, Textiles, Electronics Components, Agriculture Seeds, Packaging Materials, Furniture
- **18 pre-seeded calls**: Instant demo with realistic mock conversations

## Tech Stack
- Flask 3.0, Jinja2 templates
- Plotly for interactive charts
- TextBlob for basic NLP (extensible to spaCy)
- Regex-based entity extraction (price, quantity, specs)
- JSON file-based persistence

## Quick Start

```powershell
# 1. Create virtual environment and install dependencies
python -m venv .venv
. .venv\Scripts\activate
pip install -r requirements.txt

# 2. Seed sample data (optional but recommended for demo)
python seed_data.py

# 3. Run the app
python app.py
```

Open **http://localhost:5000** in your browser.

## Demo Flow
1. **Dashboard** (`/`): View aggregated insights
   - Total calls, cities covered
   - Top cities by call volume (bar chart)
   - Category-level avg prices, quantities, sentiment distribution
2. **Add Call** (`/upload`): Paste mock transcript with metadata
   - See per-call extraction: prices, quantities, specs, sentiment
   - Derived metrics: avg price, price per quantity
3. **Back to Dashboard**: See updated aggregations with your new call

## Sample Usage

### Add a New Call
Go to `/upload`, paste this transcript:
```
Hello, I need 300 kg of cement for my site. What's your price? 
Seller: Rs 7500 for 300 kg. Grade M30. 
Buyer: Good deal, confirm delivery to Delhi.
```
Select category, city, and submit to see instant extraction!

### View API
- `GET /api/aggregate` - JSON response with all aggregated insights

## Project Structure
```
Seller_Buyer_Insights/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # Blueprint routes
│   └── services/
│       └── pipeline.py      # Processing & aggregation logic
├── templates/
│   ├── base.html            # Base layout
│   ├── dashboard.html       # Aggregated view
│   ├── upload.html          # Add call form
│   └── call_result.html     # Per-call result
├── static/
│   ├── css/style.css        # Dark theme styles
│   └── js/app.js            # Future interactivity
├── data/
│   └── sample_calls.json    # Persisted calls (auto-created)
├── seed_data.py             # Pre-populate 18 calls
├── app.py                   # Entry point
├── requirements.txt
└── README.md
```

## Insights Provided

### Per-Call
- Extracted: Prices (INR/Rs patterns), quantities (kg/units/meters), specs (mm/grade), sentiment
- Derived: Avg price, total quantity, price per quantity unit

### Aggregated
- **By Category**: Avg price, avg quantity, sentiment breakdown (positive/negative/neutral)
- **By Location**: Top cities by call volume
- **Overall**: Total calls, cities covered

## Hackathon Alignment
- ✅ Covers **6 categories** (exceeds 5 minimum)
- ✅ End-to-end: Raw transcript → extraction → insight → actionable display
- ✅ Clear "so what?": Category pricing trends, location demand patterns, buyer-seller sentiment
- ✅ Generalizable: Works across any category with text input

## Notes
- **Mock data only** — no real IndiaMART data used
- Extraction is regex-based; can enhance with spaCy NER or LLMs for production
- Sentiment is heuristic; upgrade with TextBlob polarity or transformers (BERT)

## Future Enhancements
- Audio-to-text (Whisper API or Google Speech)
- Advanced NLP: Named entity recognition, topic modeling
- Real-time dashboard updates (WebSocket)
- Export insights as CSV/PDF reports
- One-slide auto-generator from aggregates
