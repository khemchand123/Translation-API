"""
Test GST validation with real seller_identifier from metadata
This simulates what happens when user uploads audio with seller metadata
"""

from app.company_service import company_service
import json

def test_real_seller_flow():
    print("="*80)
    print("🧪 TESTING REAL SELLER FLOW")
    print("="*80)
    
    # Simulate what comes from metadata when user uploads audio
    # seller_identifier = gluser_id
    test_seller_id = "quickshop-surat"  # This is what would come from seller_identifier
    
    print(f"\n📋 Simulated Upload Metadata:")
    print(f"   seller_identifier: {test_seller_id}")
    print(f"   (This would come from the audio upload metadata)")
    
    print(f"\n{'='*80}")
    print("STEP 1: Fetch Seller Data from IndiaMART")
    print(f"{'='*80}")
    
    # This is what happens in the backend
    seller_data = company_service.fetch_seller_products(test_seller_id)
    
    if seller_data['success']:
        print(f"✅ Successfully fetched seller data!")
        print(f"\n📋 Company Information:")
        print(f"   Company Name: {seller_data['company_name']}")
        print(f"   GST Number: {seller_data.get('gst_number', 'NOT FOUND')}")
        print(f"   Product Count: {seller_data['product_count']}")
        
        if seller_data.get('gst_info'):
            print(f"\n📄 GST Information from IndiaMART:")
            for key, value in seller_data['gst_info'].items():
                print(f"   {key}: {value}")
        
        if seller_data.get('products'):
            print(f"\n📦 Registered Products (first 5):")
            for i, product in enumerate(seller_data['products'][:5], 1):
                print(f"   {i}. {product}")
            if len(seller_data['products']) > 5:
                print(f"   ... and {len(seller_data['products']) - 5} more")
        
        # Now test government GST verification if we have GST number
        if seller_data.get('gst_number'):
            print(f"\n{'='*80}")
            print("STEP 2: Verify GST with Government Portal")
            print(f"{'='*80}")
            
            gst_number = seller_data['gst_number']
            print(f"GST Number: {gst_number}")
            print(f"API URL: https://sheet.gstincheck.co.in/check/.../{gst_number}")
            
            gov_result = company_service.verify_gst_from_government(gst_number)
            
            if gov_result and gov_result.get('verified'):
                print(f"\n✅ Government GST Verification: SUCCESS")
                print(f"   Trade Name: {gov_result.get('trade_name')}")
                print(f"   Legal Name: {gov_result.get('legal_name')}")
                print(f"   Constitution: {gov_result.get('constitution')}")
                print(f"   Nature of Business: {gov_result.get('nature_of_business')}")
                print(f"   Status: {gov_result.get('status')}")
                
                # Test business category matching
                if seller_data.get('gst_info'):
                    print(f"\n{'='*80}")
                    print("STEP 3: Match Business Categories")
                    print(f"{'='*80}")
                    
                    category_match = company_service.match_business_categories(
                        seller_data['gst_info'],
                        gov_result
                    )
                    
                    print(f"Match Score: {category_match.get('match_score')}%")
                    print(f"Summary: {category_match.get('summary')}")
                    
                    if category_match.get('matches'):
                        print(f"\n✅ Matched Categories:")
                        for match in category_match['matches']:
                            print(f"   • {match['category']}")
                            print(f"     IndiaMART: {match['indiamart']}")
                            print(f"     Government: {match['government']}")
            else:
                print(f"\n❌ Government GST Verification: FAILED")
                if gov_result:
                    print(f"   Error: {gov_result.get('error')}")
        else:
            print(f"\n⚠️  No GST number found in IndiaMART data")
            print(f"   GST validation cannot proceed")
    else:
        print(f"❌ Failed to fetch seller data")
        print(f"   Error: {seller_data.get('error')}")
        print(f"\n💡 Possible issues:")
        print(f"   1. Check if seller_identifier is correct (should be gluser_id or alias)")
        print(f"   2. Check if IndiaMART API is accessible")
        print(f"   3. Check if the IP address 34.93.120.35 is reachable")
    
    print(f"\n{'='*80}")
    print("TEST COMPLETE")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    test_real_seller_flow()
