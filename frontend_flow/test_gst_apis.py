"""
Test multiple GST verification APIs to find working ones
Testing with GST: 24AAFCR0479J1Z8
"""

import requests
import json

def test_gst_api(name, url, headers=None):
    """Test a single GST API"""
    print(f"\n{'='*80}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print(f"{'='*80}")
    
    try:
        response = requests.get(url, headers=headers or {}, timeout=15)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ SUCCESS - Got JSON response")
                print(f"\nResponse Preview:")
                print(json.dumps(data, indent=2)[:1000])
                
                # Try to extract key information
                if data:
                    print(f"\n📋 Data Structure:")
                    print(f"   Keys: {list(data.keys())[:10]}")
                    
                    # Check for common patterns
                    if "taxpayerInfo" in data or data.get("flag") or data.get("success"):
                        print(f"   ✅ LOOKS LIKE VALID GST DATA!")
                        return True, data
                    
                return True, data
            except Exception as e:
                print(f"   Response Text: {response.text[:500]}")
                return False, None
        else:
            print(f"❌ FAILED - Status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False, None
            
    except requests.Timeout:
        print(f"⏱️ TIMEOUT - API took too long")
        return False, None
    except Exception as e:
        print(f"❌ ERROR - {str(e)}")
        return False, None

def main():
    test_gst = "24AAFCR0479J1Z8"
    
    print("="*80)
    print(f"🔍 TESTING GST VERIFICATION APIs")
    print(f"GST Number: {test_gst}")
    print("="*80)
    
    # List of GST APIs to test
    apis = [
        {
            "name": "GST Portal (tera-api)",
            "url": f"https://gst-verification.p.rapidapi.com/api/v1/gst-verify?gstNo={test_gst}",
            "headers": {
                "X-RapidAPI-Key": "demo_key",
                "X-RapidAPI-Host": "gst-verification.p.rapidapi.com"
            }
        },
        {
            "name": "MasterIndia GST API",
            "url": f"https://commonapi.mastersindia.co/commonapis/searchgstin?gstin={test_gst}",
            "headers": {}
        },
        {
            "name": "GST Search India",
            "url": f"https://services.gst.gov.in/services/api/search?action=TP&gstin={test_gst}",
            "headers": {}
        },
        {
            "name": "KnowYourGST API",
            "url": f"https://knowyourgst.com/developers/get_gstin_details?gstin={test_gst}",
            "headers": {}
        },
        {
            "name": "AppyFlow GST",
            "url": f"https://appyflow.in/verifyGST?gstNo={test_gst}&key_secret=YXBweWZsb3c6YXBweWZsb3c=",
            "headers": {}
        },
        {
            "name": "Aadise GST",
            "url": f"https://aadise.com/api/verify-gst.php?gst={test_gst}",
            "headers": {}
        },
        {
            "name": "GST Verify Pro",
            "url": f"https://gstverifypro.com/api/verify?gstin={test_gst}",
            "headers": {}
        },
        {
            "name": "IndiaFilings GST",
            "url": f"https://indiafilings.com/api/verify/gstin/{test_gst}",
            "headers": {}
        },
        {
            "name": "ClearTax GST API",
            "url": f"https://api.cleartax.in/gst/public/v1/gstin/{test_gst}",
            "headers": {}
        },
        {
            "name": "GST Portal Public Search",
            "url": f"https://services.gst.gov.in/services/searchtp?gstin={test_gst}",
            "headers": {}
        },
    ]
    
    working_apis = []
    
    for api in apis:
        success, data = test_gst_api(api["name"], api["url"], api.get("headers"))
        if success:
            working_apis.append({
                "name": api["name"],
                "url": api["url"],
                "data": data
            })
    
    print("\n\n")
    print("="*80)
    print(f"📊 SUMMARY")
    print("="*80)
    print(f"Total APIs Tested: {len(apis)}")
    print(f"Working APIs: {len(working_apis)}")
    
    if working_apis:
        print(f"\n✅ WORKING APIs:")
        for i, api in enumerate(working_apis, 1):
            print(f"   {i}. {api['name']}")
            print(f"      URL: {api['url']}")
    else:
        print(f"\n❌ NO WORKING APIs FOUND")
        print(f"\n💡 Suggestions:")
        print(f"   1. These APIs may require authentication/API keys")
        print(f"   2. Government GST portal may need browser session")
        print(f"   3. Consider using paid GST verification services")
        print(f"   4. Use IndiaMART GST data as primary source")
    
    print("\n")

if __name__ == "__main__":
    main()
