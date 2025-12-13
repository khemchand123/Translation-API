"""
Test script for GST validation feature
Tests with provided seller data:
- GST Number: 24AAFCR0479J1Z8
- Glusr ID: 3676307
"""

from app.company_service import company_service

def test_gst_validation():
    print("=" * 80)
    print("🧪 TESTING GST VALIDATION FEATURE")
    print("=" * 80)
    
    # Test data provided by user
    test_glusrid = "3676307"
    expected_gst = "24AAFCR0479J1Z8"
    test_products = ["Steel", "Iron", "Metal Products"]
    
    print(f"\n📌 Test Parameters:")
    print(f"   Seller ID (glusrid): {test_glusrid}")
    print(f"   Expected GST: {expected_gst}")
    print(f"   Test Products: {test_products}")
    
    print(f"\n{'='*80}")
    print("STEP 1: Fetching Seller Products from IndiaMART")
    print(f"{'='*80}")
    
    seller_data = company_service.fetch_seller_products(test_glusrid)
    
    if seller_data['success']:
        print(f"✅ Successfully fetched seller data")
        print(f"\n📋 Company Information:")
        print(f"   Company Name: {seller_data['company_name']}")
        print(f"   GST Number: {seller_data.get('gst_number', 'Not found')}")
        print(f"   Product Count: {seller_data['product_count']}")
        
        if seller_data.get('gst_info'):
            print(f"\n📄 GST Information from IndiaMART:")
            for key, value in seller_data['gst_info'].items():
                print(f"   {key}: {value}")
        
        print(f"\n📦 Registered Products (first 10):")
        for i, product in enumerate(seller_data['products'][:10], 1):
            print(f"   {i}. {product}")
        if len(seller_data['products']) > 10:
            print(f"   ... and {len(seller_data['products']) - 10} more")
    else:
        print(f"❌ Failed to fetch seller data: {seller_data.get('error')}")
        return
    
    print(f"\n{'='*80}")
    print("STEP 2: Verifying GST with Government Portal")
    print(f"{'='*80}")
    
    if seller_data.get('gst_number'):
        gov_gst = company_service.verify_gst_from_government(seller_data['gst_number'])
        
        if gov_gst and gov_gst.get('verified'):
            print(f"✅ GST verified by Government")
            print(f"\n🏛️ Government GST Details:")
            print(f"   GST Number: {seller_data['gst_number']}")
            print(f"   Trade Name: {gov_gst.get('trade_name', 'N/A')}")
            print(f"   Legal Name: {gov_gst.get('legal_name', 'N/A')}")
            print(f"   Registration Date: {gov_gst.get('registration_date', 'N/A')}")
            print(f"   Status: {gov_gst.get('status', 'N/A')}")
        else:
            print(f"⚠️ Could not verify GST with government: {gov_gst.get('error', 'Unknown error')}")
    else:
        print(f"⚠️ No GST number found in seller data")
    
    print(f"\n{'='*80}")
    print("STEP 3: Validating Products")
    print(f"{'='*80}")
    
    validation_result = company_service.validate_seller_products(test_glusrid, test_products)
    
    print(f"\n🔍 Validation Result:")
    print(f"   Status: {validation_result['validation_status'].upper()}")
    print(f"   Message: {validation_result['message']}")
    
    if validation_result.get('matches'):
        print(f"\n✅ Matched Products ({len(validation_result['matches'])}):")
        for match in validation_result['matches']:
            if isinstance(match, dict):
                print(f"   - Conversation: '{match['conversation']}' → Registered: '{match['registered']}'")
            else:
                print(f"   - {match}")
    
    if validation_result.get('non_matches'):
        print(f"\n❌ Non-Matched Products ({len(validation_result['non_matches'])}):")
        for product in validation_result['non_matches']:
            print(f"   - {product}")
    
    if validation_result.get('government_gst_verification'):
        gov_verification = validation_result['government_gst_verification']
        if gov_verification.get('verified'):
            print(f"\n🏛️ Government Verification: ✅ VERIFIED")
        else:
            print(f"\n🏛️ Government Verification: ❌ NOT VERIFIED")
    
    print(f"\n{'='*80}")
    print("✅ TEST COMPLETED")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    test_gst_validation()
