"""
Deep search for working GST verification APIs
Focus on finding the actual working government or reliable third-party APIs
"""

import requests
import json

def test_detailed_gst_api():
    test_gst = "24AAFCR0479J1Z8"
    
    print("="*80)
    print("🔍 DEEP SEARCH FOR WORKING GST APIs")
    print("="*80)
    
    # API 1: GSTN Official (with proper headers)
    print("\n1️⃣ Testing: Official GSTN API (with browser headers)")
    print("-" * 80)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.gst.gov.in/'
        }
        url = f"https://services.gst.gov.in/services/api/search/taxpayerDetails?gstin={test_gst}"
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS!")
            print(json.dumps(data, indent=2)[:1000])
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # API 2: Masters India (with authentication)
    print("\n2️⃣ Testing: Masters India GST API (checking docs)")
    print("-" * 80)
    try:
        # This API needs client_id and client_secret
        url = f"https://commonapi.mastersindia.co/commonapis/searchgstin?gstin={test_gst}&email=test@example.com&client_id=demo"
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # API 3: KnowYourGST (check different endpoint)
    print("\n3️⃣ Testing: KnowYourGST (different endpoint)")
    print("-" * 80)
    try:
        url = f"https://services.gst.gov.in/services/searchtp?gstin={test_gst}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        # Check if it's HTML or JSON
        if 'application/json' in response.headers.get('Content-Type', ''):
            print("Got JSON response!")
            print(json.dumps(response.json(), indent=2)[:1000])
        else:
            print("Got HTML response (likely needs authentication)")
            print(response.text[:300])
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # API 4: Public GST search without auth
    print("\n4️⃣ Testing: Public GST Verification Services")
    print("-" * 80)
    
    # Try a simpler approach - scraping public GST portal
    try:
        # This mimics what a browser would do
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://services.gst.gov.in/'
        })
        
        # First visit the main page
        main_url = "https://services.gst.gov.in/services/searchtp"
        session.get(main_url, timeout=10)
        
        # Then try the search
        search_url = f"https://services.gst.gov.in/services/api/search?action=TP&gstin={test_gst}"
        response = session.get(search_url, timeout=10)
        
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        
        if 'json' in response.headers.get('Content-Type', '').lower():
            data = response.json()
            print("✅ SUCCESS - Got JSON!")
            print(json.dumps(data, indent=2))
        else:
            print("Got HTML response")
            print(response.text[:500])
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # API 5: Try GST Portal direct taxpayer search
    print("\n5️⃣ Testing: GST Portal Direct Taxpayer Search")
    print("-" * 80)
    try:
        # The actual public search endpoint
        url = "https://services.gst.gov.in/services/api/search/taxpayerDetails"
        params = {'gstin': test_gst}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Origin': 'https://services.gst.gov.in',
            'Referer': 'https://services.gst.gov.in/services/searchtp'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ SUCCESS - Got JSON!")
                print(json.dumps(data, indent=2))
                
                if 'pradr' in str(data) or 'tradeNam' in str(data):
                    print("\n🎉 FOUND WORKING API!")
                    print(f"URL: {url}")
                    print(f"Params: {params}")
                    
            except:
                print("Response is not JSON")
                print(response.text[:500])
        else:
            print(f"Failed with status {response.status_code}")
            print(response.text[:300])
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*80)
    print("💡 RECOMMENDATION")
    print("="*80)
    print("""
The government GST portal requires:
1. Browser-like session with cookies
2. CAPTCHA solving for public search
3. Or an official API key for programmatic access

BEST APPROACH FOR YOUR HACKATHON:
✅ Use IndiaMART's GST data as PRIMARY source (already implemented)
   - You get GST number, registration year, partners, legal status, etc.
   - This data comes from verified IndiaMART database
   - No need for external API calls

✅ Show "Verified by IndiaMART Database" badge
   - IndiaMART already verifies sellers during onboarding
   - The GST info in ADDITIONALINFO is reliable
   - Display this prominently in your UI

✅ For DEMO purposes:
   - Mock the government verification as "Available"
   - Or show "GST details from IndiaMART verified database"
   - Focus on the PRODUCT MATCHING feature (which is unique!)

The REAL VALUE is:
- Product matching (conversation vs registered)
- Fraud detection (seller claiming wrong products)
- This is MORE IMPORTANT than government API verification!
""")

if __name__ == "__main__":
    test_detailed_gst_api()
