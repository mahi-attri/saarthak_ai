import streamlit as st
import requests
import re
from difflib import SequenceMatcher

class EnhancedConversationEngine:
    """Enhanced conversation engine with robust Hindi/Hinglish support"""
    
    def __init__(self):
        self.user_profile = {}
        self.conversation_stage = "initial"
        self.schemes_database = self.load_schemes()
        self.selected_scheme = None
        self.show_details = False
        self.language_patterns = self.load_language_patterns()
        self.waiting_for_city = False  # New flag to track when waiting for city input
        
    def load_language_patterns(self):
        """Comprehensive language patterns for Hindi/Hinglish/English"""
        return {
            "age_indicators": [
                "age", "years old", "year old", "yrs", "i am",
                "umra", "umr", "saal", "varsh", "main", "hun", "hoon",
                "umar", "age hai", "saal ka", "saal ki"
            ],
            
            "profession_keywords": {
                "farmer": [
                    "farmer", "farming", "agriculture", "crop", "farm",
                    "किसान", "खेती", "कृषि", "खेत", "फसल", "कृषक",
                    "kisan", "kheti", "krishi", "khet", "fasal", "krshak",
                    "farming karta", "kheti karta", "farmer hun"
                ],
                "student": [
                    "student", "study", "studying", "college", "school", "education",
                    "छात्र", "छात्रा", "पढ़ाई", "पढ़ता", "पढ़ती", "कॉलेज", "स्कूल", "शिक्षा",
                    "chatra", "chhatra", "padhai", "padhta", "padhti", "college", "school",
                    "student hun", "padh raha", "padh rahi", "study karta"
                ],
                "employee": [
                    "job", "work", "working", "employee", "service", "office",
                    "नौकरी", "काम", "कार्य", "सेवा", "ऑफिस", "कर्मचारी", "कामगार",
                    "naukri", "nokri", "kaam", "karya", "seva", "office", "karmchari",
                    "job karta", "kaam karta", "naukri hai", "service mein"
                ],
                "business_owner": [
                    "business", "shop", "store", "entrepreneur", "owner", "trade",
                    "व्यापार", "व्यवसाय", "दुकान", "कारोबार", "धंधा", "मालिक",
                    "vyapar", "vyvasay", "dukan", "karobar", "dhanda", "malik", 
                    "business karta", "shop hai", "vyapar karta"
                ],
                "unemployed": [
                    "unemployed", "no job", "jobless", "searching job",
                    "बेरोजगार", "बिना काम", "काम नहीं", "नौकरी नहीं",
                    "berojgar", "berozgar", "kaam nahi", "naukri nahi", "job nahi",
                    "koi kaam nahi", "unemployed hun"
                ]
            },
            
            "location_keywords": {
                "rural": [
                    "village", "rural", "countryside", "farm area",
                    "गांव", "गाँव", "ग्रामीण", "देहात", "खेत",
                    "gaon", "ganv", "grameen", "dehat", "village mein",
                    "gaon se", "rural area"
                ],
                "urban": [
                    "city", "town", "urban", "metro", "municipal",
                    "शहर", "नगर", "महानगर", "कस्बा", "शहरी",
                    "sheher", "shahar", "nagar", "mahanagar", "kasba", "shahri",
                    "city mein", "town mein", "urban area"
                ]
            },
            
            "income_keywords": [
                "income", "salary", "earning", "earn", "rupees", "rs", "inr",
                "आय", "वेतन", "कमाई", "कमाता", "कमाती", "रुपए", "रुपये", "पैसा",
                "aay", "vetan", "kamai", "kamata", "kamati", "rupee", "rupaye", "paisa",
                "salary hai", "kamai hai", "income hai", "kamata hun"
            ],
            
            "family_keywords": [
                "family", "members", "people", "persons",
                "परिवार", "सदस्य", "लोग", "व्यक्ति", "घर", "घरवाले",
                "parivar", "parivaar", "sadasya", "log", "vyakti", "ghar", "gharwale",
                "family mein", "ghar mein", "members hai"
            ],
            
            "number_words": {
                "एक": 1, "दो": 2, "तीन": 3, "चार": 4, "पांच": 5, "छह": 6, "सात": 7, "आठ": 8, "नौ": 9, "दस": 10,
                "ग्यारह": 11, "बारह": 12, "तेरह": 13, "चौदह": 14, "पंद्रह": 15, "सोलह": 16, "सत्रह": 17, "अट्ठारह": 18, "उन्नीस": 19, "बीस": 20,
                "ek": 1, "do": 2, "teen": 3, "char": 4, "panch": 5, "chhe": 6, "saat": 7, "aath": 8, "nau": 9, "das": 10,
                "gyarah": 11, "barah": 12, "terah": 13, "chaudah": 14, "pandrah": 15, "solah": 16, "satrah": 17, "atharah": 18, "unnis": 19, "bees": 20
            }
        }
    
    def load_schemes(self):
        """Load schemes with location-specific data"""
        return {
            "pm_kisan": {
                "name_hindi": "PM किसान सम्मान निधि",
                "name_english": "PM Kisan Samman Nidhi",
                "category": "agriculture",
                "benefit_amount": 6000,
                "benefit_summary_english": "₹6,000/year in 3 installments",
                "benefit_summary_hindi": "₹6,000/वर्ष 3 किस्तों में",
                "eligibility_summary_english": "Small & marginal farmers with up to 2 hectares land",
                "eligibility_summary_hindi": "2 हेक्टेयर तक भूमि वाले छोटे और सीमांत किसान",
                "target_users": ["farmer"],
                "website": "pmkisan.gov.in",
                "helpline": "155261",
                "quick_docs_english": ["Aadhaar", "Land records", "Bank account"],
                "quick_docs_hindi": ["आधार", "भूमि रिकॉर्ड", "बैंक खाता"]
            },
            "ayushman_bharat": {
                "name_hindi": "आयुष्मान भारत",
                "name_english": "Ayushman Bharat PM-JAY", 
                "category": "health",
                "benefit_amount": 500000,
                "benefit_summary_english": "₹5 lakh health insurance per family",
                "benefit_summary_hindi": "₹5 लाख प्रति परिवार स्वास्थ्य बीमा",
                "eligibility_summary_english": "BPL families and SECC 2011 eligible categories",
                "eligibility_summary_hindi": "BPL परिवार और SECC 2011 पात्र श्रेणियां",
                "target_users": ["unemployed", "employee"],
                "website": "pmjay.gov.in",
                "helpline": "14555",
                "quick_docs_english": ["Aadhaar", "Ration card", "SECC verification"],
                "quick_docs_hindi": ["आधार", "राशन कार्ड", "SECC सत्यापन"]
            },
            "pm_awas_urban": {
                "name_hindi": "PM आवास योजना",
                "name_english": "PM Awas Yojana Urban",
                "category": "housing", 
                "benefit_amount": 267000,
                "benefit_summary_english": "₹2.67 lakh housing subsidy",
                "benefit_summary_hindi": "₹2.67 लाख आवास सब्सिडी",
                "eligibility_summary_english": "Urban families without pucca house, income up to ₹18 lakh",
                "eligibility_summary_hindi": "पक्का मकान न होने वाले शहरी परिवार, ₹18 लाख तक आय",
                "target_users": ["employee", "unemployed"],
                "website": "pmaymis.gov.in", 
                "helpline": "1800116446",
                "quick_docs_english": ["Aadhaar", "Income certificate", "Property documents"],
                "quick_docs_hindi": ["आधार", "आय प्रमाण पत्र", "संपत्ति दस्तावेज"]
            },
            "nsp_scholarship": {
                "name_hindi": "राष्ट्रीय छात्रवृत्ति",
                "name_english": "National Scholarship Portal",
                "category": "education",
                "benefit_amount": 36000,
                "benefit_summary_english": "Up to ₹36,000/year for studies",
                "benefit_summary_hindi": "अध्ययन के लिए ₹36,000/वर्ष तक",
                "eligibility_summary_english": "SC/ST/OBC/Minority students, family income up to ₹2.5 lakh",
                "eligibility_summary_hindi": "SC/ST/OBC/अल्पसंख्यक छात्र, ₹2.5 लाख तक पारिवारिक आय",
                "target_users": ["student"],
                "website": "scholarships.gov.in",
                "helpline": "0120-6619540", 
                "quick_docs_english": ["Aadhaar", "Marksheets", "Income certificate", "Caste certificate"],
                "quick_docs_hindi": ["आधार", "मार्कशीट", "आय प्रमाण पत्र", "जाति प्रमाण पत्र"]
            }
        }
    
    def normalize_text(self, text):
        """Normalize text for better matching"""
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[।,.\-_!?]', ' ', text)
        return text.strip()
    
    def fuzzy_match_keywords(self, text, keyword_list, threshold=0.7):
        """Fuzzy matching for keywords to handle typos and variations"""
        text_normalized = self.normalize_text(text)
        
        for keyword in keyword_list:
            keyword_normalized = self.normalize_text(keyword)
            
            if keyword_normalized in text_normalized:
                return True
            
            if len(keyword_normalized) > 3:
                similarity = SequenceMatcher(None, keyword_normalized, text_normalized).ratio()
                if similarity >= threshold:
                    return True
                
                words = text_normalized.split()
                for word in words:
                    if len(word) > 2:
                        similarity = SequenceMatcher(None, keyword_normalized, word).ratio()
                        if similarity >= threshold:
                            return True
        
        return False
    
    def extract_numbers_with_context(self, text):
        """Extract numbers with better context understanding"""
        text_normalized = self.normalize_text(text)
        
        for word, number in self.language_patterns["number_words"].items():
            if word in text_normalized:
                return number
        
        number_patterns = [
            r'\b(\d{1,2})\s*(?:saal|sal|year|years|yrs|साल|वर्ष)',
            r'(?:main|mai|मैं)\s*(\d{1,2})',
            r'(?:age|umr|umar|उम्र)\s*(\d{1,2})',
            r'(\d{1,2})\s*(?:ka|ki|है|हूं|हूँ|hun|hoon)',
            r'\b(\d{1,2})\b'
        ]
        
        for pattern in number_patterns:
            match = re.search(pattern, text_normalized)
            if match:
                number = int(match.group(1))
                if self.is_valid_age(number):
                    return number
        
        return None
    
    def is_valid_age(self, number):
        """Check if number is a valid age"""
        return 15 <= number <= 100
    
    def extract_income_amount(self, text):
        """Enhanced income extraction supporting multiple formats"""
        text_lower = text.lower()
        
        low_income_indicators = [
            "very low", "bahut kam", "बहुत कम", "kam", "कम", "low", "poor", 
            "gareeb", "गरीब", "below poverty", "bpl"
        ]
        
        if any(indicator in text_lower for indicator in low_income_indicators):
            return 30000
        
        text_clean = re.sub(r'[₹$¢€£]', '', text_lower)
        
        income_patterns = [
            (r'(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|लाख|लाखों|l|L)', 100000),
            (r'(\d+(?:\.\d+)?)\s*(?:thousand|thousands|हजार|हज़ार|k|K)', 1000),
            (r'(\d+(?:\.\d+)?)\s*(?:crore|crores|करोड़|करोड़ों)', 10000000),
            (r'(\d{1,3}(?:,\d{3})+)', 1),
            (r'(\d{4,8})', 1),
        ]
        
        for pattern, multiplier in income_patterns:
            match = re.search(pattern, text_clean)
            if match:
                try:
                    amount_str = match.group(1).replace(',', '')
                    amount = float(amount_str)
                    total = int(amount * multiplier)
                    
                    if 1000 <= total <= 50000000:
                        return total
                except ValueError:
                    continue
        
        return None
    
    def extract_user_info_from_text(self, text):
        """Enhanced information extraction with better language support"""
        text_normalized = self.normalize_text(text)
        
        if "age" not in self.user_profile:
            age = self.extract_numbers_with_context(text)
            if age:
                self.user_profile["age"] = age
        
        if "profession" not in self.user_profile:
            for profession, keywords in self.language_patterns["profession_keywords"].items():
                if self.fuzzy_match_keywords(text_normalized, keywords):
                    self.user_profile["profession"] = profession
                    break
        
        if "location" not in self.user_profile:
            for location_type, keywords in self.language_patterns["location_keywords"].items():
                if self.fuzzy_match_keywords(text_normalized, keywords):
                    self.user_profile["location"] = location_type
                    break
        
        if "annual_income" not in self.user_profile:
            income = self.extract_income_amount(text)
            if income:
                self.user_profile["annual_income"] = income
        
        if "family_size" not in self.user_profile and "age" in self.user_profile:
            family_size = None
            
            simple_match = re.search(r'^\s*(\d{1,2})\s*$', text_normalized)
            if simple_match:
                family_size = int(simple_match.group(1))
            else:
                patterns = [
                    r'(?:family|parivar|परिवार|ghar|घर).*?(\d{1,2})',
                    r'(\d{1,2}).*?(?:members|sadasya|सदस्य|log|लोग)',
                    r'(?:hum|हम|main|मैं)\s*(\d{1,2})',
                    r'(\d{1,2})\s*(?:log|लोग|member|sadasya|सदस्य)'
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, text_normalized)
                    if match:
                        family_size = int(match.group(1))
                        break
            
            if family_size and family_size != self.user_profile["age"] and 1 <= family_size <= 20:
                self.user_profile["family_size"] = family_size
    
    def get_smart_response(self, missing_field, language):
        """Generate contextual responses based on previous inputs"""
        
        if language == "हिंदी":
            questions = {
                "age": ["आपकी उम्र क्या है? 🎂", "*संख्या लिखें (जैसे: 25)*"],
                "profession": ["आप क्या करते हैं? 💼", "• 'किसान' 🌾 • 'छात्र' 📚 • 'नौकरी' 💼"],
                "location": ["आप कहाँ रहते हैं? 🏠", "• 'गांव' 🌾 • 'शहर' 🏙️"],
                "annual_income": ["सालाना पारिवारिक आय? 💰", "जैसे: '2 लाख' या '50000'"],
                "family_size": ["परिवार में कितने सदस्य? 👨‍👩‍👧‍👦", "*संख्या लिखें (जैसे: 4)*"]
            }
        else:
            questions = {
                "age": ["What is your age? 🎂", "*Type a number (e.g., 25)*"],
                "profession": ["What do you do? 💼", "• 'farmer' 🌾 • 'student' 📚 • 'job' 💼"],
                "location": ["Where do you live? 🏠", "• 'village' 🌾 • 'city' 🏙️"],
                "annual_income": ["Family income per year? 💰", "e.g., '2 lakh' or '50000'"],
                "family_size": ["How many family members? 👨‍👩‍👧‍👦", "*Type a number (e.g., 4)*"]
            }
        
        return "\n".join(questions.get(missing_field, ["Please provide more details."]))
    
    def find_matching_schemes(self):
        """Find schemes matching user profile"""
        matching = []
        user_profession = self.user_profile.get("profession", "")
        user_income = self.user_profile.get("annual_income", 0)
        
        for scheme_id, scheme in self.schemes_database.items():
            if user_profession in scheme["target_users"]:
                matching.append(scheme)
            elif scheme_id == "ayushman_bharat" and user_income < 200000:
                matching.append(scheme)
            elif scheme_id == "pm_awas_urban" and user_income < 1800000:
                matching.append(scheme)
        
        return matching
    
    def process_query(self, user_input, language="English"):
        """Process with improved UX - progressive disclosure"""
        
        user_input_lower = user_input.lower().strip()
        
        # Handle city input when we're waiting for a city name
        if self.waiting_for_city:
            self.waiting_for_city = False  # Reset the flag
            # Clean the city name and get office information
            city_name = user_input.strip().title()
            return self.get_city_specific_offices(city_name, language)
        
        # Handle city-specific office requests with explicit patterns
        city_office_patterns = [
            r'(?:offices?|office|कार्यालय) (?:in|mein|में) ([a-zA-Zअ-ह\s]+)',
            r'([a-zA-Zअ-ह\s]+) (?:mein|में) (?:offices?|office|कार्यालय)',
            r'([a-zA-Zअ-ह\s]+) (?:ke|का|की) (?:offices?|office|कार्यालय)'
        ]
        
        for pattern in city_office_patterns:
            city_match = re.search(pattern, user_input_lower)
            if city_match:
                city_name = city_match.group(1).strip().title()
                # Clean up common Hindi words from city name
                city_name = re.sub(r'\b(mein|में|ke|का|की|office|कार्यालय)\b', '', city_name, flags=re.IGNORECASE).strip()
                if city_name:
                    return self.get_city_specific_offices(city_name, language)
        
        # Handle scheme details requests
        if user_input_lower.startswith("details"):
            scheme_id = user_input_lower.replace("details ", "").strip()
            return self.show_scheme_details(scheme_id, language)
        
        # Handle location services
        if ("near me" in user_input_lower or "office address" in user_input_lower or 
            user_input_lower == "offices near me"):
            return self.provide_location_services(language)
        
        # Regular conversation flow
        if self.conversation_stage == "initial":
            return self.handle_initial_query(user_input, language)
        elif self.conversation_stage == "gathering_details":
            return self.handle_detail_gathering(user_input, language)
        elif self.conversation_stage == "recommendations":
            return self.provide_smart_recommendations(language)
    
    def handle_initial_query(self, user_input, language):
        """Smart initial handling"""
        self.extract_user_info_from_text(user_input.lower())
        
        if "age" not in self.user_profile:
            self.conversation_stage = "gathering_details"
            return self.get_smart_response("age", language)
        
        return self.continue_questioning(language)
    
    def continue_questioning(self, language):
        """Continue with next question in proper sequence"""
        question_sequence = ["age", "profession", "location", "annual_income", "family_size"]
        
        for field in question_sequence:
            if field not in self.user_profile:
                return self.get_smart_response(field, language)
        
        self.conversation_stage = "recommendations"
        return self.provide_smart_recommendations(language)
    
    def handle_detail_gathering(self, user_input, language):
        """Handle follow-up answers and continue conversation flow"""
        missing = self.get_missing_information()
        current_field = missing[0] if missing else None
        
        self.extract_user_info_from_text(user_input.lower())
        
        if current_field == "annual_income" and "annual_income" not in self.user_profile:
            income = self.extract_income_amount(user_input)
            if income:
                self.user_profile["annual_income"] = income
        
        if current_field == "family_size" and "family_size" not in self.user_profile:
            number_match = re.search(r'\b(\d{1,2})\b', user_input.strip())
            if number_match:
                family_size = int(number_match.group(1))
                if (family_size != self.user_profile.get("age", 0) and 
                    1 <= family_size <= 20):
                    self.user_profile["family_size"] = family_size
        
        return self.continue_questioning(language)
    
    def get_missing_information(self):
        """Check what's missing in proper sequence"""
        required_sequence = ["age", "profession", "location", "annual_income", "family_size"]
        missing = [field for field in required_sequence if field not in self.user_profile]
        return missing
    
    def provide_smart_recommendations(self, language):
        """Provide clean, scannable recommendations"""
        matching_schemes = self.find_matching_schemes()
        
        if not matching_schemes:
            if language == "हिंदी":
                return "आपकी प्रोफ़ाइल से मेल खाने वाली कोई योजना नहीं मिली।"
            else:
                return "No schemes found matching your profile."
        
        if language == "हिंदी":
            response = """🎯 **बहुत बढ़िया! आपके लिए सबसे अच्छी सरकारी योजनाएं मिल गईं!**

नीचे दिए गए कार्ड पर क्लिक करके किसी भी योजना की पूरी जानकारी देखें। 👇"""
        else:
            response = """🎯 **Perfect! Found the best government schemes for you!**

Click on any card below to see complete details for that scheme. 👇"""
        
        return response
    
    def show_scheme_details(self, scheme_number, language):
        """Show detailed information for specific scheme"""
        
        try:
            scheme_index = int(scheme_number) - 1
            matching_schemes = self.find_matching_schemes()
            
            if scheme_index >= len(matching_schemes):
                if language == "हिंदी":
                    return "गलत योजना नंबर। कृपया फिर से कोशिश करें।"
                else:
                    return "Invalid scheme number. Please try again."
            
            scheme = matching_schemes[scheme_index]
            
            if language == "हिंदी":
                benefit_summary = scheme['benefit_summary_hindi']
                eligibility_summary = scheme['eligibility_summary_hindi']
                quick_docs = scheme['quick_docs_hindi']
                
                return f"""
## 📋 {scheme['name_hindi']} - पूरी जानकारी

**💰 वित्तीय लाभ:**
{benefit_summary} (कुल: ₹{scheme['benefit_amount']:,})

**✅ पात्रता:**
{eligibility_summary}

**📄 आवश्यक दस्तावेज:**
{', '.join(quick_docs)}

**🌐 आवेदन कैसे करें:**
1. वेबसाइट पर जाएं: {scheme['website']}
2. 'नया पंजीकरण' पर क्लिक करें
3. आधार OTP से फॉर्म भरें
4. दस्तावेज अपलोड करें (PDF, अधिकतम 200KB)
5. सबमिट करें और रेफरेंस नंबर सेव करें

**📞 सहायता:**
• हेल्पलाइन: {scheme['helpline']} (टोल-फ्री)
• समय: सुबह 9 से शाम 6 बजे
• ईमेल: support@{scheme['website']}

**⏰ समयसीमा:**
• प्रोसेसिंग: 15-30 दिन
• पहला भुगतान: अप्रूवल के 2-3 महीने बाद

**💡 सुझाव:**
• योजना की डेडलाइन में आवेदन करें (मार्च/सितंबर)
• मोबाइल नंबर आधार से लिंक रखें
• आवेदन कन्फर्मेशन का स्क्रीनशॉट लें

*नजदीकी आवेदन केंद्र खोजने के लिए 'offices near me' लिखें*
                """
            else:
                benefit_summary = scheme['benefit_summary_english']
                eligibility_summary = scheme['eligibility_summary_english']
                quick_docs = scheme['quick_docs_english']
                
                return f"""
## 📋 {scheme['name_english']} - Complete Details

**💰 Financial Benefit:**
{benefit_summary} (Total: ₹{scheme['benefit_amount']:,})

**✅ Eligibility:**
{eligibility_summary}

**📄 Required Documents:**
{', '.join(quick_docs)}

**🌐 How to Apply:**
1. Visit: {scheme['website']}
2. Click 'New Registration'
3. Fill form with Aadhaar OTP
4. Upload documents (PDF, max 200KB each)
5. Submit and save reference number

**📞 Help & Support:**
• Helpline: {scheme['helpline']} (Toll-free)
• Timings: 9 AM to 6 PM
• Email: support@{scheme['website']}

**⏰ Timeline:**
• Processing: 15-30 days
• First payment: 2-3 months after approval

**💡 Pro Tips:**
• Apply during scheme deadlines (March/September)
• Keep mobile number linked with Aadhaar
• Take screenshots of application confirmation

*Type 'offices near me' to find local application centers*
                """
        except:
            if language == "हिंदी":
                return "कृपया सही योजना नंबर बताएं (1, 2, या 3)।"
            else:
                return "Please specify a valid scheme number (1, 2, or 3)."
    
    def get_user_location(self):
        """Get user's approximate location for local office addresses"""
        try:
            response = requests.get('https://ipapi.co/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'city': data.get('city', 'Unknown'),
                    'state': data.get('region', 'Unknown'),
                    'country': data.get('country_name', 'India'),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude')
                }
        except Exception as e:
            return {
                'city': 'Delhi',
                'state': 'Delhi',
                'country': 'India'
            }
        return None
    
    def get_city_specific_offices(self, city_name, language):
        """Get offices for a specific city mentioned by user"""
        
        city_state_map = {
            'mumbai': 'Maharashtra', 'delhi': 'Delhi', 'bangalore': 'Karnataka',
            'chennai': 'Tamil Nadu', 'kolkata': 'West Bengal', 'hyderabad': 'Telangana',
            'pune': 'Maharashtra', 'ahmedabad': 'Gujarat', 'jaipur': 'Rajasthan',
            'lucknow': 'Uttar Pradesh', 'kanpur': 'Uttar Pradesh', 'nagpur': 'Maharashtra',
            'indore': 'Madhya Pradesh', 'thane': 'Maharashtra', 'bhopal': 'Madhya Pradesh',
            'visakhapatnam': 'Andhra Pradesh', 'pimpri': 'Maharashtra', 'patna': 'Bihar',
            'vadodara': 'Gujarat', 'ghaziabad': 'Uttar Pradesh', 'ludhiana': 'Punjab',
            'agra': 'Uttar Pradesh', 'nashik': 'Maharashtra', 'faridabad': 'Haryana',
            'meerut': 'Uttar Pradesh', 'rajkot': 'Gujarat', 'kalyan': 'Maharashtra'
        }
        
        state = city_state_map.get(city_name.lower(), city_name)
        offices = self.get_local_offices(city_name, state)
        
        if language == "English":
            response = f"**🏢 Government Offices in {city_name}, {state}:**\n\n"
            for i, office in enumerate(offices, 1):
                response += f"{i}. {office}\n"
            
            response += f"""
**📱 For Exact Locations:**
• Google Maps: Search "{offices[0]}"
• Phone Directory: Call 1800-180-1551
• State Portal: Search "{state} government offices"

**🚀 Quick Tips for {city_name}:**
• Best time to visit: 11 AM - 3 PM (less crowded)
• Carry: All originals + 2 photocopies
• Parking: Most offices have visitor parking

**📞 {city_name} Helplines:**
• General Govt Info: 100
• District Administration: 1800-180-1551
• Aadhaar Support: 1947
            """
        else:
            response = f"**🏢 {city_name}, {state} में सरकारी कार्यालय:**\n\n"
            for i, office in enumerate(offices, 1):
                response += f"{i}. {office}\n"
            
            response += f"""
**📱 सटीक स्थान के लिए:**
• Google Maps: "{offices[0]}" खोजें
• फोन डायरेक्टरी: 1800-180-1551 पर कॉल करें
• राज्य पोर्टल: "{state} सरकारी कार्यालय" खोजें

**🚀 {city_name} के लिए त्वरित सुझाव:**
• जाने का बेस्ट समय: 11 AM - 3 PM (कम भीड़)
• साथ लेकर जाएं: सभी मूल + 2 फोटोकॉपी
• पार्किंग: ज्यादातर कार्यालयों में विजिटर पार्किंग है

**📞 {city_name} हेल्पलाइन:**
• सामान्य सरकारी जानकारी: 100
• जिला प्रशासन: 1800-180-1551
• आधार सपोर्ट: 1947
            """
        
        return response

    def get_real_government_offices(self, city, state):
        """Get real government office locations using OpenStreetMap Nominatim API"""
        try:
            # Search for government offices in the city
            search_queries = [
                f"District Collector Office {city} {state} India",
                f"Tehsildar Office {city} {state} India", 
                f"Block Development Office {city} {state} India",
                f"Municipal Corporation {city} {state} India"
            ]
            
            offices = []
            
            for query in search_queries:
                try:
                    # Using Nominatim API (free OpenStreetMap service)
                    url = f"https://nominatim.openstreetmap.org/search"
                    params = {
                        'q': query,
                        'format': 'json',
                        'limit': 1,
                        'countrycodes': 'in',
                        'addressdetails': 1
                    }
                    
                    response = requests.get(url, params=params, timeout=3, 
                                          headers={'User-Agent': 'SaarthakAI/1.0'})
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data:
                            place = data[0]
                            address = place.get('display_name', '')
                            # Clean up the address
                            if address:
                                # Extract relevant parts
                                address_parts = address.split(',')
                                clean_address = ', '.join(address_parts[:3])
                                offices.append(clean_address)
                except:
                    continue
                    
            # If API calls fail, fallback to template offices
            if not offices:
                offices = [
                    f"District Collector Office, {city}, {state}",
                    f"Municipal Corporation, {city}, {state}",
                    f"Tehsil Office, {city}, {state}"
                ]
                
            return offices[:3]  # Return top 3
            
        except Exception as e:
            # Fallback to manual addresses
            return [
                f"District Collector Office, {city}, {state}",
                f"Municipal Corporation, {city}, {state}",
                f"Tehsil Office, {city}, {state}"
            ]
    
    def get_local_offices(self, city, state, scheme_type="general"):
        """Legacy method - redirects to new method for backward compatibility"""
        return self.get_real_government_offices(city, state)
    
    def provide_location_services(self, language):
        """Provide location-specific office information"""
        
        location_data = self.get_user_location()
        
        if location_data and location_data.get('city') != 'Unknown':
            city = location_data.get('city', 'Delhi')
            state = location_data.get('state', 'Delhi')
            
            offices = self.get_real_government_offices(city, state)
            
            if language == "हिंदी":
                response = f"""
**🏢 आपके नजदीक सरकारी कार्यालय ({city}, {state}):**

"""
                for i, office in enumerate(offices, 1):
                    response += f"**{i}.** {office}\n\n"
                
                response += f"""
**📱 त्वरित सहायता:**

• **सटीक दिशा:** Google Maps पर "{offices[0]}" खोजें
• **फोन सहायता:** 1800-180-1551 (जिला हेल्पलाइन)
• **ऑनलाइन सूची:** {state} सरकार पोर्टल देखें

**💡 यात्रा के सुझाव:**

• **CSC केंद्र** तेज़ होते हैं और कम इंतजार
• सभी दस्तावेजों के **मूल + 2 फोटोकॉपी** लेकर जाएं
• कम भीड़ के लिए **11 AM - 3 PM** के बीच जाएं
                """
            else:
                response = f"""
**🏢 Government Offices Near You ({city}, {state}):**

"""
                for i, office in enumerate(offices, 1):
                    response += f"**{i}.** {office}\n\n"
                
                response += f"""
**📱 Quick Assistance:**

• **Exact Directions:** Search "{offices[0]}" on Google Maps
• **Phone Support:** 1800-180-1551 (District Helpline)
• **Complete List:** Visit {state} Government Portal

**💡 Travel Tips:**

• **CSC Centers** are faster with less waiting time
• Carry **originals + 2 photocopies** of all documents
• Visit during **11 AM - 3 PM** for shorter queues
                """
        else:
            # Set flag to indicate we're waiting for city input
            self.waiting_for_city = True
            
            if language == "हिंदी":
                response = """
### 🏢 अपने नजदीक सरकारी कार्यालय खोजें:

**अपने शहर का नाम बताएं**, मैं सटीक कार्यालय खोजूंगा! 🎯

*उदाहरण: "मुंबई", "दिल्ली", "जयपुर", "लखनऊ" लिखें*

---

### 📋 सामान्य कार्यालय प्रकार:

• **जिला कलेक्टर कार्यालय** - मुख्य प्रशासनिक केंद्र
• **तहसील कार्यालय** - उप-जिला स्तर के आवेदन
• **ब्लॉक विकास कार्यालय** - ग्रामीण योजना आवेदन
• **कॉमन सर्विस सेंटर (CSC)** - डिजिटल सेवा केंद्र

### 📞 सार्वभौमिक हेल्पलाइन:

• **सामान्य सरकारी जानकारी:** 1800-180-1551
• **CSC लोकेटर:** 1800-121-3468
• **आधार सहायता:** 1947

### 🌐 ऑनलाइन संसाधन:

• Google Maps पर "[आपका शहर] जिला कलेक्टर कार्यालय" खोजें
• अपनी राज्य सरकार की वेबसाइट देखें
• नजदीकी केंद्रों के लिए 'जन औषधि' ऐप का उपयोग करें
                """
            else:
                response = """
### 🏢 Find Government Offices Near You:

**Tell me your city name**, and I'll find exact offices! 🎯

*Example: Type "Mumbai", "Delhi", "Jaipur", "Lucknow"*

---

### 📋 Common Office Types:

• **District Collector Office** - Main administrative center
• **Tehsil Office** - Sub-district level applications  
• **Block Development Office** - Rural scheme applications
• **Common Service Center (CSC)** - Digital services hub

### 📞 Universal Helplines:

• **General Government Info:** 1800-180-1551
• **CSC Locator:** 1800-121-3468  
• **Aadhaar Help:** 1947

### 🌐 Online Resources:

• Search "[Your City] District Collector Office" on Google Maps
• Visit your state government website
• Use 'Jan Aushadhi' app for nearest centers
                """
        
        return response

def main():
    st.set_page_config(
        page_title="SaarthakAI",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Modern ChatGPT-like interface
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Reset and base styles */
        .main .block-container {
            padding: 0;
            max-width: 100%;
            font-family: 'Inter', sans-serif;
        }
        
        /* Main app background */
        .stApp {
            background: #f7f7f8;
        }
        
        /* Top header bar like ChatGPT */
        .top-header {
            background: white;
            border-bottom: 1px solid #e5e5e5;
            padding: 16px 24px;
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        
        .app-title {
            font-size: 18px;
            font-weight: 600;
            color: #202123;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .language-selector {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 14px;
        }
        
        /* Main chat container */
        .chat-container {
            max-width: 768px;
            margin: 0 auto;
            min-height: calc(100vh - 120px);
            display: flex;
            flex-direction: column;
        }
        
        /* Welcome section */
        .welcome-section {
            text-align: center;
            padding: 48px 24px;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .welcome-title {
            font-size: 32px;
            font-weight: 600;
            color: #202123;
            margin-bottom: 16px;
        }
        
        .welcome-subtitle {
            font-size: 16px;
            color: #6b7280;
            margin-bottom: 32px;
            line-height: 1.5;
        }
        
        /* Progress indicator */
        .progress-indicator {
            background: white;
            border: 1px solid #e5e5e5;
            border-radius: 12px;
            padding: 16px;
            margin: 16px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .progress-info {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            color: #6b7280;
        }
        
        .progress-badge {
            background: #3b82f6;
            color: white;
            padding: 4px 8px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .progress-bar {
            height: 4px;
            background: #f3f4f6;
            border-radius: 2px;
            overflow: hidden;
            margin: 8px 0;
            width: 100%;
        }
        
        .progress-fill {
            height: 100%;
            background: #3b82f6;
            border-radius: 2px;
            transition: width 0.3s ease;
        }
        
        /* Chat messages area */
        .messages-area {
            flex: 1;
            padding: 0 24px 24px 24px;
            overflow-y: auto;
        }
        
        /* Message bubbles like ChatGPT */
        .stChatMessage {
            margin: 0 0 24px 0;
            padding: 0;
        }
        
        .stChatMessage > div {
            max-width: 100%;
            margin: 0;
            padding: 0;
            background: transparent;
            border: none;
            box-shadow: none;
        }
        
        /* Assistant messages */
        .stChatMessage[data-testid="assistant-message"] {
            background: transparent;
        }
        
        .stChatMessage[data-testid="assistant-message"] > div {
            background: transparent;
            padding: 24px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .stChatMessage[data-testid="assistant-message"] > div > div {
            background: transparent;
            padding: 0;
            max-width: 100%;
        }
        
        /* User messages */
        .stChatMessage[data-testid="user-message"] {
            background: #f7f7f8;
        }
        
        .stChatMessage[data-testid="user-message"] > div {
            background: #f7f7f8;
            padding: 24px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .stChatMessage[data-testid="user-message"] > div > div {
            background: transparent;
            padding: 0;
            max-width: 100%;
        }
        
        /* Message content styling */
        .stChatMessage p {
            margin: 0 0 12px 0;
            font-size: 16px;
            line-height: 1.6;
            color: #374151;
        }
        
        .stChatMessage strong {
            font-weight: 600;
            color: #111827;
        }
        
        /* Input area */
        .input-area {
            position: sticky;
            bottom: 0;
            background: white;
            border-top: 1px solid #e5e5e5;
            padding: 16px 24px;
        }
        
        .stChatInput > div {
            max-width: 768px;
            margin: 0 auto;
            border: 1px solid #d1d5db;
            border-radius: 12px;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .stChatInput > div:focus-within {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
        }
        
        .stChatInput input {
            border: none;
            background: transparent;
            font-size: 16px;
            padding: 12px 16px;
            color: #374151;
            font-family: 'Inter', sans-serif;
        }
        
        .stChatInput input::placeholder {
            color: #9ca3af;
        }
        
        /* Language selector styling */
        .stSelectbox {
            min-width: 120px;
        }
        
        .stSelectbox > div > div {
            border: 1px solid #d1d5db;
            border-radius: 8px;
            background: white;
            font-size: 14px;
            min-height: 36px;
        }
        
        .stSelectbox > div > div:focus-within {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
        }
        
        /* Scheme cards */
        .stExpander {
            background: white;
            border: 1px solid #e5e5e5;
            border-radius: 12px;
            margin: 16px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .stExpander > div:first-child {
            background: #3b82f6;
            color: white;
            font-weight: 600;
            padding: 16px 20px;
            border: none;
            font-size: 16px;
        }
        
        .stExpander > div:last-child {
            padding: 20px;
            background: white;
        }
        
        .stExpander svg {
            color: white !important;
        }
        
        /* Buttons */
        .stButton > button {
            background: #3b82f6;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 500;
            font-size: 14px;
            transition: background-color 0.2s;
        }
        
        .stButton > button:hover {
            background: #2563eb;
        }
        
        /* Stats section */
        .stats-section {
            background: white;
            border: 1px solid #e5e5e5;
            border-radius: 12px;
            padding: 20px;
            margin: 16px 24px;
            text-align: center;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-top: 16px;
        }
        
        .stat-item {
            padding: 12px;
            background: #f9fafb;
            border-radius: 8px;
        }
        
        .stat-value {
            font-size: 20px;
            font-weight: 600;
            color: #3b82f6;
        }
        
        .stat-label {
            font-size: 12px;
            color: #6b7280;
            margin-top: 4px;
        }
        
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Responsive design */
        @media (max-width: 768px) {
            .top-header {
                padding: 12px 16px;
            }
            
            .chat-container {
                margin: 0;
            }
            
            .messages-area {
                padding: 0 16px 16px 16px;
            }
            
            .input-area {
                padding: 12px 16px;
            }
            
            .welcome-section {
                padding: 32px 16px;
            }
            
            .welcome-title {
                font-size: 24px;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
        
        /* Scrollbar styling */
        .messages-area::-webkit-scrollbar {
            width: 4px;
        }
        
        .messages-area::-webkit-scrollbar-track {
            background: transparent;
        }
        
        .messages-area::-webkit-scrollbar-thumb {
            background: #d1d5db;
            border-radius: 2px;
        }
        
        .messages-area::-webkit-scrollbar-thumb:hover {
            background: #9ca3af;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Top header like ChatGPT
    st.markdown("""
    <div class="top-header">
        <div class="app-title">
            🚀 SaarthakAI
        </div>
        <div class="language-selector">
            <span style="color: #6b7280; font-size: 14px;">Language:</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Language selector in header
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        language = st.selectbox("", ["English", "हिंदी"], key="lang", label_visibility="collapsed")
    
    # Initialize engine
    if "enhanced_engine" not in st.session_state:
        st.session_state.enhanced_engine = EnhancedConversationEngine()
    
    # Progress indicator
    if len(st.session_state.enhanced_engine.user_profile) < 5:
        total_steps = 5
        completed_steps = len(st.session_state.enhanced_engine.user_profile)
        progress_width = min((completed_steps / total_steps) * 100, 100)
        
        st.markdown(f"""
        <div class="progress-indicator">
            <div>
                <div class="progress-info">
                    <span>📊 Profile Setup</span>
                    <span class="progress-badge">Step {completed_steps}/5</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress_width}%"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Welcome section (show only initially)
    if "enhanced_messages" not in st.session_state:
        st.markdown("""
        <div class="welcome-section">
            <h1 class="welcome-title">Welcome to SaarthakAI</h1>
            <p class="welcome-subtitle">
                I'll help you find the perfect government schemes by asking just 5 quick questions. 
                You can respond in English, Hindi, or Hinglish!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Initialize messages
    if "enhanced_messages" not in st.session_state or st.session_state.get("current_lang") != language:
        welcome_msg = """Hello! I'm your smart assistant! 🚀

I'll find **perfect schemes** for you by asking just **5 quick questions**.

You can respond in **English, Hindi, or Hinglish**! 

**What's your age?** 🎂
*Examples: "25", "twenty five", "25 saal"*""" if language == "English" else """नमस्ते! मैं आपका स्मार्ट सहायक हूं! 🚀

मैं सिर्फ **5 आसान सवाल** पूछकर **बेहतरीन योजनाएं** खोजूंगा।

आप **हिंदी, English, या Hinglish** में जवाब दे सकते हैं!

**आपकी उम्र क्या है?** 🎂
*उदाहरण: "25", "पच्चीस", "25 years"*"""
        
        st.session_state.enhanced_messages = [
            {"role": "assistant", "content": welcome_msg}
        ]
        st.session_state.current_lang = language
        st.session_state.enhanced_engine = EnhancedConversationEngine()
    
    # Messages area
    st.markdown('<div class="messages-area">', unsafe_allow_html=True)
    for message in st.session_state.enhanced_messages:
        with st.chat_message(message["role"]):
            st.markdown(message['content'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Scheme recommendations
    if (len(st.session_state.enhanced_engine.user_profile) >= 5 and 
        st.session_state.enhanced_engine.conversation_stage == "recommendations"):
        
        matching_schemes = st.session_state.enhanced_engine.find_matching_schemes()
        
        if matching_schemes:
            for i, scheme in enumerate(matching_schemes[:3]):
                if language == "हिंदी":
                    benefit_summary = scheme['benefit_summary_hindi']
                    eligibility_summary = scheme['eligibility_summary_hindi']
                    quick_docs = scheme['quick_docs_hindi']
                    scheme_name = scheme['name_hindi']
                else:
                    benefit_summary = scheme['benefit_summary_english']
                    eligibility_summary = scheme['eligibility_summary_english']
                    quick_docs = scheme['quick_docs_english']
                    scheme_name = scheme['name_english']
                
                with st.expander(f"💰 **{i+1}. {scheme_name}**"):
                    st.markdown(f"""
                    **💰 {'लाभ' if language == 'हिंदी' else 'Benefit'}:**
                    {benefit_summary}
                    
                    **👥 {'पात्रता' if language == 'हिंदी' else 'Eligibility'}:**
                    {eligibility_summary}
                    
                    **📄 {'दस्तावेज' if language == 'हिंदी' else 'Documents'}:**
                    {', '.join(quick_docs[:2])} + more
                    
                    **🌐 {'संपर्क' if language == 'हिंदी' else 'Contact'}:**
                    Website: {scheme['website']}  
                    Helpline: {scheme['helpline']}
                    """)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"📋 {'पूरी जानकारी' if language == 'हिंदी' else 'Full Details'}", key=f"details_{i}"):
                            # Show complete scheme details
                            details_response = st.session_state.enhanced_engine.show_scheme_details(str(i+1), language)
                            st.session_state.enhanced_messages.append({"role": "assistant", "content": details_response})
                            st.rerun()
                    with col2:
                        if st.button(f"📞 {'संपर्क करें' if language == 'हिंदी' else 'Contact'}", key=f"contact_{i}"):
                            st.info(f"📱 Call: {scheme['helpline']}")
    
    # Stats section
    if len(st.session_state.enhanced_engine.user_profile) >= 5:
        st.markdown("""
        <div class="stats-section">
            <h3 style="margin: 0 0 16px 0; color: #374151;">💡 Trusted • Free • Secure</h3>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">25+</div>
                    <div class="stat-label">Schemes</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">2min</div>
                    <div class="stat-label">Setup</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">Multi</div>
                    <div class="stat-label">Language</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area at bottom
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    placeholder = "Type your answer..." if language == "English" else "अपना जवाब टाइप करें..."
    
    if prompt := st.chat_input(placeholder):
        st.session_state.enhanced_messages.append({"role": "user", "content": prompt})
        
        with st.spinner("🔍 Finding schemes..." if language == "English" else "🔍 योजनाएं खोज रहा हूं..."):
            response = st.session_state.enhanced_engine.process_query(prompt, language)
            st.session_state.enhanced_messages.append({"role": "assistant", "content": response})
        
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()