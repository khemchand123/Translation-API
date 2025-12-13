"""
Test the working GST API with your API key
"""

import requests
import json

def test_working_gst_api():
    api_key = "35763275830677245b5785e216f6afdf"
    test_gst = "24AAFCR0479J1Z8"
    
    url = f"https://sheet.gstincheck.co.in/check/{api_key}/{test_gst}"
    
    print("="*80)
    print("🔍 TESTING WORKING GST API")
    print("="*80)
    print(f"API Key: {api_key}")
    print(f"GST Number: {test_gst}")
    print(f"URL: {url}")
    print("="*80)
    
    try:
        response = requests.get(url, timeout=15)
        print(f"\n✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📦 FULL RESPONSE:")
            print(json.dumps(data, indent=2))
            
            print(f"\n{'='*80}")
            print("📊 EXTRACTED INFORMATION")
            print(f"{'='*80}")
            
            # Check what data is available
            if isinstance(data, dict):
                # Check for common GST response patterns
                if 'data' in data:
                    gst_data = data['data']
                    print(f"\n✅ Found 'data' section")
                    
                    # Trade name
                    if 'tradeNam' in gst_data or 'tradeName' in gst_data:
                        trade_name = gst_data.get('tradeNam') or gst_data.get('tradeName')
                        print(f"   🏢 Trade Name: {trade_name}")
                    
                    # Legal name
                    if 'lgnm' in gst_data or 'legalName' in gst_data:
                        legal_name = gst_data.get('lgnm') or gst_data.get('legalName')
                        print(f"   📋 Legal Name: {legal_name}")
                    
                    # Business type / Nature of business
                    if 'nba' in gst_data or 'nature_of_business' in gst_data or 'dty' in gst_data:
                        nba = gst_data.get('nba') or gst_data.get('nature_of_business') or gst_data.get('dty')
                        print(f"   💼 Nature of Business: {nba}")
                    
                    # Registration date
                    if 'rgdt' in gst_data or 'registrationDate' in gst_data:
                        reg_date = gst_data.get('rgdt') or gst_data.get('registrationDate')
                        print(f"   📅 Registration Date: {reg_date}")
                    
                    # Status
                    if 'sts' in gst_data or 'status' in gst_data or 'taxpayerType' in gst_data:
                        status = gst_data.get('sts') or gst_data.get('status') or gst_data.get('taxpayerType')
                        print(f"   ✓ Status: {status}")
                    
                    # Business activities / categories
                    if 'ctb' in gst_data or 'constitution' in gst_data:
                        ctb = gst_data.get('ctb') or gst_data.get('constitution')
                        print(f"   🏭 Constitution: {ctb}")
                    
                    # State jurisdiction
                    if 'stj' in gst_data or 'state' in gst_data:
                        state = gst_data.get('stj') or gst_data.get('state')
                        print(f"   📍 State: {state}")
                    
                    # Principal place of business
                    if 'pradr' in gst_data:
                        pradr = gst_data['pradr']
                        if 'addr' in pradr:
                            addr = pradr['addr']
                            print(f"\n   📍 Address:")
                            if 'bnm' in addr:
                                print(f"      Building: {addr['bnm']}")
                            if 'st' in addr:
                                print(f"      Street: {addr['st']}")
                            if 'loc' in addr:
                                print(f"      Location: {addr['loc']}")
                            if 'dst' in addr:
                                print(f"      District: {addr['dst']}")
                            if 'city' in addr:
                                print(f"      City: {addr['city']}")
                            if 'pncd' in addr:
                                print(f"      Pincode: {addr['pncd']}")
                
                # Check if flag indicates success
                if 'flag' in data:
                    print(f"\n   Flag: {data['flag']}")
                
                if 'status_cd' in data:
                    print(f"   Status Code: {data['status_cd']}")
            
            print(f"\n{'='*80}")
            print("💡 MATCHING WITH INDIAMART DATA")
            print(f"{'='*80}")
            print("""
From Government GST we can match:
1. Trade Name / Legal Name - matches with Company Name
2. Nature of Business - can match with GST Nature of Business from IndiaMART
3. Constitution (Proprietorship/Company/etc) - matches GST Legal status
4. State - matches location data
5. Registration Date - matches GST Registration year

NOTE: Government GST does NOT provide product lists
So we'll use:
- IndiaMART product list as primary source
- Government GST for business verification
- Match business categories/nature between both sources
""")
            
            return data
            
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    result = test_working_gst_api()
    
    if result:
        print("\n" + "="*80)
        print("🎉 API IS WORKING! Ready to integrate!")
        print("="*80)
