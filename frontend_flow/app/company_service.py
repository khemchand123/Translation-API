import requests
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class CompanyService:
    def __init__(self):
        # Using IP address instead of domain for better accessibility
        self.base_url_template_1 = "http://34.93.120.35/wservce/company/detail/glusrid/{user_id}/alias//cat_link//token/imobile@15061981/req_server/home_server/modid/tdw/is_mob_device/"
        self.base_url_template_2 = "http://34.93.120.35/wservce/company/detail/glusrid//alias/{alias}/cat_link//token/imobile@15061981/req_server/home_server/modid/tdw/is_mob_device/"
        # Working GST API with updated key
        self.gst_api_key = "d315ec2fa9590c48e436cad6520f5110"
        self.gst_api_url = f"https://sheet.gstincheck.co.in/check/{self.gst_api_key}/{{gst_number}}"

    def get_showroom_alias(self, user_id: str) -> Optional[str]:
        """
        Fetches the showroom alias for a given user ID.
        """
        url = self.base_url_template_1.format(user_id=user_id)
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "URL_DETAIL" in data and "FREESHOWROOM_ALIAS" in data["URL_DETAIL"]:
                    return data["URL_DETAIL"]["FREESHOWROOM_ALIAS"]
                else:
                    logger.warning(f"FREESHOWROOM_ALIAS not found for user_id {user_id}")
                    return None
            else:
                logger.error(f"Failed to fetch alias for user_id {user_id}. Status: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error fetching alias for user_id {user_id}: {e}")
            return None

    def get_company_details(self, alias: str) -> Optional[Dict[str, Any]]:
        """
        Fetches company details using the showroom alias.
        """
        url = self.base_url_template_2.format(alias=alias)
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                logger.error(f"Failed to fetch details for alias {alias}. Status: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error fetching details for alias {alias}: {e}")
            return None

    def verify_gst_from_government(self, gst_number: str) -> Optional[Dict[str, Any]]:
        """
        Verifies GST number using government GST verification API.
        Returns GST details from government records.
        """
        if not gst_number:
            return None
        
        try:
            url = self.gst_api_url.format(gst_number=gst_number)
            logger.info(f"🔍 Verifying GST {gst_number} with government API")
            
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                
                # Check if GST is valid (flag should be true)
                if data.get("flag") == True or data.get("flag") == "true":
                    gst_data = data.get("data", {})
                    logger.info(f"✅ GST {gst_number} verified by government")
                    
                    return {
                        'verified': True,
                        'trade_name': gst_data.get("tradeNam", ""),
                        'legal_name': gst_data.get("lgnm", ""),
                        'registration_date': gst_data.get("rgdt", ""),
                        'status': gst_data.get("sts", ""),
                        'state': gst_data.get("stj", ""),
                        'constitution': gst_data.get("ctb", ""),  # Private Limited Company, etc.
                        'nature_of_business': gst_data.get("nba", []),  # ['Retail', 'Wholesale', 'Manufacturing']
                        'gstin': gst_data.get("gstin", gst_number),
                        'address': gst_data.get("pradr", {}).get("adr", ""),
                        'taxpayer_type': gst_data.get("dty", ""),  # Regular, Composite, etc.
                        'raw_data': gst_data
                    }
                else:
                    logger.warning(f"⚠️ GST {gst_number} not found in government records")
                    return {'verified': False, 'error': 'GST not found in government database'}
            else:
                logger.error(f"❌ GST API returned status {response.status_code}")
                return {'verified': False, 'error': f'API error: {response.status_code}'}
                
        except Exception as e:
            logger.error(f"❌ Error verifying GST {gst_number}: {e}")
            return {'verified': False, 'error': str(e)}

    def match_business_categories(self, indiamart_gst_info: Dict[str, Any], govt_gst_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Matches business categories between IndiaMART GST info and Government GST data.
        Returns matching analysis.
        """
        matches = []
        mismatches = []
        
        try:
            # Get IndiaMART data
            im_nature_of_business = indiamart_gst_info.get("GST Nature of business", "")
            im_legal_status = indiamart_gst_info.get("GST Legal status", "")
            im_additional_nob = indiamart_gst_info.get("GST Additional NOB", "")
            
            # Get Government data
            govt_nature_of_business = govt_gst_data.get("nature_of_business", [])
            govt_constitution = govt_gst_data.get("constitution", "")
            
            # Match Legal Status with Constitution
            if im_legal_status and govt_constitution:
                im_legal_lower = im_legal_status.lower()
                govt_const_lower = govt_constitution.lower()
                
                # Check if they match (even partially)
                if (im_legal_lower in govt_const_lower or govt_const_lower in im_legal_lower or
                    ("limited" in im_legal_lower and "limited" in govt_const_lower) or
                    ("proprietor" in im_legal_lower and "proprietor" in govt_const_lower) or
                    ("partnership" in im_legal_lower and "partnership" in govt_const_lower)):
                    matches.append({
                        'category': 'Legal Status / Constitution',
                        'indiamart': im_legal_status,
                        'government': govt_constitution,
                        'match_type': 'exact' if im_legal_status.lower() == govt_constitution.lower() else 'similar'
                    })
                else:
                    mismatches.append({
                        'category': 'Legal Status / Constitution',
                        'indiamart': im_legal_status,
                        'government': govt_constitution
                    })
            
            # Match Nature of Business - Enhanced semantic matching
            if im_nature_of_business and govt_nature_of_business:
                im_nob_lower = im_nature_of_business.lower()
                govt_nob_list = [str(nob).lower().strip() for nob in govt_nature_of_business]
                
                # Split IndiaMART NOB by common separators (comma, slash, hyphen)
                import re
                im_nob_parts = [p.strip() for p in re.split(r'[,/\-]', im_nob_lower) if p.strip()]
                
                # Check if any IndiaMART part matches any government nature
                match_found = False
                matched_items = []
                
                # First check: direct substring match
                for govt_nob in govt_nob_list:
                    for im_part in im_nob_parts:
                        if govt_nob in im_part or im_part in govt_nob:
                            match_found = True
                            matched_items.append(f"{im_part} ↔ {govt_nob}")
                            break
                    if match_found:
                        break
                
                # Second check: word-level semantic match (e.g., "trader" matches "wholesale", "retail")
                if not match_found:
                    semantic_keywords = {
                        'trader': ['wholesale', 'retail', 'trading'],
                        'retailer': ['retail', 'trading'],
                        'wholesaler': ['wholesale', 'trading'],
                        'manufacturer': ['manufacturing', 'factory'],
                        'exporter': ['export'],
                        'importer': ['import'],
                        'service': ['service provider']
                    }
                    
                    for im_part in im_nob_parts:
                        for keyword, synonyms in semantic_keywords.items():
                            if keyword in im_part:
                                for govt_nob in govt_nob_list:
                                    if any(syn in govt_nob for syn in synonyms):
                                        match_found = True
                                        matched_items.append(f"{im_part} ↔ {govt_nob}")
                                        break
                            if match_found:
                                break
                        if match_found:
                            break
                
                if match_found:
                    matches.append({
                        'category': 'Nature of Business',
                        'indiamart': im_nature_of_business,
                        'government': govt_nature_of_business,
                        'match_type': 'semantic',
                        'matched_items': matched_items
                    })
                else:
                    mismatches.append({
                        'category': 'Nature of Business',
                        'indiamart': im_nature_of_business,
                        'government': govt_nature_of_business
                    })
            
            # Match Additional NOB with Government Nature of Business
            if im_additional_nob and govt_nature_of_business:
                im_add_nob_parts = [part.strip().lower() for part in im_additional_nob.split(',')]
                govt_nob_list = [str(nob).lower() for nob in govt_nature_of_business]
                
                matched_categories = []
                for im_part in im_add_nob_parts:
                    for govt_nob in govt_nob_list:
                        if im_part in govt_nob or govt_nob in im_part:
                            matched_categories.append(f"{im_part} ↔ {govt_nob}")
                
                if matched_categories:
                    matches.append({
                        'category': 'Business Activities',
                        'indiamart': im_additional_nob,
                        'government': govt_nature_of_business,
                        'match_type': 'category',
                        'matched_items': matched_categories
                    })
            
            # Calculate match score
            total_checks = len(matches) + len(mismatches)
            match_score = (len(matches) / total_checks * 100) if total_checks > 0 else 0
            
            return {
                'matches': matches,
                'mismatches': mismatches,
                'match_score': round(match_score, 1),
                'summary': f"{len(matches)}/{total_checks} categories match" if total_checks > 0 else "No categories to compare"
            }
            
        except Exception as e:
            logger.error(f"Error matching business categories: {e}")
            return {
                'matches': [],
                'mismatches': [],
                'match_score': 0,
                'summary': f"Error: {str(e)}"
            }

    def fetch_seller_products(self, seller_id: str) -> Dict[str, Any]:
        """
        Fetches seller's registered products from IndiaMART database.
        Returns a dict with company name, product count, list of products, and GST info.
        """
        result = {
            'success': False,
            'company_name': None,
            'product_count': 0,
            'products': [],
            'gst_number': None,
            'gst_info': None,
            'error': None
        }
        
        try:
            # Detect if seller_id is numeric (gluser_id) or alphanumeric (alias)
            if seller_id.isdigit():
                # Step 1: Get showroom alias from gluser_id
                logger.info(f"🔍 Fetching alias for gluser_id: {seller_id}")
                alias = self.get_showroom_alias(seller_id)
                if not alias:
                    result['error'] = 'Could not fetch seller alias'
                    return result
            else:
                # seller_id is already an alias
                logger.info(f"🔍 Using seller_id as alias: {seller_id}")
                alias = seller_id
            
            # Step 2: Get company details
            details = self.get_company_details(alias)
            if not details or "DATA" not in details:
                result['error'] = 'Could not fetch company details'
                return result
            
            data_section = details["DATA"]
            
            # Extract company info
            company_detail = data_section.get("COMPANYDETAIL", {})
            result['company_name'] = company_detail.get("DIR_SEARCH_COMPANY", "Unknown")
            
            # Extract GST information from FACTSHEET (new location)
            factsheet = data_section.get("FACTSHEET", [])
            gst_data = None
            
            for info_section in factsheet:
                if isinstance(info_section, dict) and info_section.get("TITLE") == "GST Information":
                    gst_data = info_section.get("DATA", [])
                    break
            
            # If not in FACTSHEET, try ADDITIONALINFO (fallback for older format)
            if not gst_data:
                additional_info = data_section.get("ADDITIONALINFO", [])
                for info_section in additional_info:
                    if isinstance(info_section, dict) and info_section.get("TITLE") == "GST Information":
                        gst_data = info_section.get("DATA", [])
                        break
            
            if gst_data:
                gst_info = {}
                for item in gst_data:
                    if isinstance(item, dict):
                        title = item.get("TITLE", "")
                        data = item.get("DATA", "")
                        gst_info[title] = data
                        if title == "GST":
                            result['gst_number'] = data
                
                result['gst_info'] = gst_info
                logger.info(f"📋 Found GST Number: {result['gst_number']}")
            
            # Extract products
            prd_serv = data_section.get("PRDSERV", [])
            result['product_count'] = data_section.get("PRD_COUNT", 0)
            
            if isinstance(prd_serv, list):
                for item in prd_serv:
                    if isinstance(item, dict) and "ITEM_NAME" in item:
                        result['products'].append(item["ITEM_NAME"])
            
            result['success'] = True
            logger.info(f"✅ Fetched {result['product_count']} products for seller {seller_id}")
            
        except Exception as e:
            logger.error(f"❌ Error in fetch_seller_products: {e}")
            result['error'] = str(e)
        
        return result

    def validate_seller_products(self, seller_id: str, conversation_products: List[str]) -> Dict[str, Any]:
        """
        Validates if seller actually deals in the products mentioned in conversation.
        Also verifies GST with government database and matches business categories.
        Returns validation status and details.
        """
        seller_data = self.fetch_seller_products(seller_id)
        
        if not seller_data['success']:
            return {
                'validation_status': 'error',
                'message': f"Could not validate seller: {seller_data.get('error', 'Unknown error')}",
                'seller_data': None,
                'government_gst_verification': None,
                'business_category_match': None
            }
        
        # Verify GST with government if GST number is available
        government_gst = None
        business_category_match = None
        
        if seller_data.get('gst_number'):
            government_gst = self.verify_gst_from_government(seller_data['gst_number'])
            
            # If government verification succeeded, match business categories
            if government_gst and government_gst.get('verified') and seller_data.get('gst_info'):
                business_category_match = self.match_business_categories(
                    seller_data['gst_info'],
                    government_gst
                )
                logger.info(f"📊 Business category match score: {business_category_match.get('match_score', 0)}%")
        
        # Check if conversation products match seller's registered products
        registered_products = [p.lower() for p in seller_data['products']]
        conversation_products_lower = [p.lower() for p in conversation_products]
        
        matches = []
        non_matches = []
        
        for conv_product in conversation_products:
            found = False
            for reg_product in seller_data['products']:
                # Fuzzy matching - if conversation product is substring of registered product
                if conv_product.lower() in reg_product.lower() or reg_product.lower() in conv_product.lower():
                    matches.append({
                        'conversation': conv_product,
                        'registered': reg_product
                    })
                    found = True
                    break
            
            if not found:
                non_matches.append(conv_product)
        
        # Determine validation status
        if len(matches) > 0 and len(non_matches) == 0:
            validation_status = 'verified'
            message = '✅ Seller is verified GST supplier for all discussed products'
        elif len(matches) > 0:
            validation_status = 'partial'
            message = '⚠️ Seller verified for some products, but not all'
        else:
            validation_status = 'unverified'
            message = '❌ WARNING: Seller not registered for discussed products'
        
        return {
            'validation_status': validation_status,
            'message': message,
            'seller_data': seller_data,
            'matches': matches,
            'non_matches': non_matches,
            'government_gst_verification': government_gst,
            'business_category_match': business_category_match
        }

# Global instance
company_service = CompanyService()
