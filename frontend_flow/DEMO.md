# Quick Demo Script

## Pre-Demo Setup (30 seconds)
```powershell
. .venv\Scripts\activate
python seed_data.py    # Populates 18 sample calls
python app.py          # Starts server on http://localhost:5000
```

## Demo Walkthrough (5 minutes)

### 1. Dashboard Overview (1 min)
- Open http://localhost:5000
- Show **Overview card**: 18 calls, 8 cities
- Point to **Top Cities bar chart**: Delhi, Mumbai leading
- Scroll to **Category Insights table**:
  - Steel Rods: Avg ₹16,833 price
  - Textiles: Avg ₹218 price
  - Sentiment breakdown per category

### 2. Add New Call Live (2 min)
- Click **"Add Call"** in nav
- Paste this transcript:
  ```
  Hi, I need aluminum sheets 2mm thickness. 100 kg quantity needed. 
  Seller: Rs 15000 for 100 kg. Premium quality grade C. 
  Buyer: Good price, please deliver to Mumbai by Friday. Deal confirmed.
  ```
- Select **Category**: Electronics Components
- Select **City**: Mumbai
- Click **"Process Call"**
- Show extraction results:
  - Prices: 15000
  - Quantities: 100
  - Sentiment: positive
  - Derived: Avg price ₹15,000, Price per kg ₹150

### 3. Updated Dashboard (1 min)
- Click **"Back to Dashboard"**
- Show **19 total calls** now
- Electronics Components avg updated
- Mumbai call count increased in bar chart

### 4. Summary Slide (1 min)
- Open `static/summary_slide.html` in browser
- Highlight:
  - **What We Built**: End-to-end pipeline
  - **Key Insights**: 18 calls, 6 categories, 8 cities
  - **Actionable**: 4 real-world use cases for IndiaMART
  - **Tech Stack**: Flask, Plotly, Python NLP

## Key Talking Points
1. **Coverage**: Works across **6 diverse categories** (exceeds 5 minimum)
2. **Generalizability**: Same pipeline handles Steel Rods, Textiles, Electronics, Seeds, Packaging, Furniture
3. **Actionable Insights**:
   - Dynamic pricing based on market rates
   - Spec discovery from buyer conversations
   - Lead quality scoring via sentiment
   - Regional expansion opportunities
4. **Extensibility**: Ready for audio-to-text, advanced NLP (spaCy/BERT), real-time WebSocket updates

## Optional: Show Code (if time permits)
- `app/services/pipeline.py` → `extract_entities()` function (regex patterns)
- `app/services/pipeline.py` → `aggregate_insights()` function (category/location grouping)
- `templates/dashboard.html` → Plotly chart generation

## Judges' Questions - Prep Answers
**Q: Why not use ML models?**  
A: Regex is fast, deterministic, and sufficient for demo. Production can layer spaCy NER or LLMs on top.

**Q: How does this scale to millions of calls?**  
A: Current JSON file → Replace with database (PostgreSQL), async processing (Celery), caching (Redis).

**Q: What if categories change?**  
A: Pipeline is category-agnostic. Extracts prices/quantities regardless of domain.

**Q: Can you show it working on a new category?**  
A: Yes! Add a call for "Cement" or "Laptops" and watch the dashboard update live.
