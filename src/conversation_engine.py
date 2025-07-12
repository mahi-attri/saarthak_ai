# src/conversation_engine.py - Working Conversation Engine

import json
import re
from typing import Dict, List, Optional
import os
from pathlib import Path

class SaarthakConversationEngine:
    """Enhanced conversation engine with real government schemes data"""
    
    def __init__(self):
        self.schemes_data = self.load_schemes_database()
        self.user_context = {}
        
    def load_schemes_database(self) -> List[Dict]:
        """Load schemes database with fallback to hardcoded data"""
        
        # Try to load from file first
        try:
            data_path = Path(__file__).parent.parent / "data" / "schemes_database.json"
            if data_path.exists():
                with open(data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('schemes', [])
        except Exception as e:
            print(f"Could not load schemes database: {e}")
        
        # Fallback to hardcoded schemes data
        return self.get_hardcoded_schemes()
    
    def get_hardcoded_schemes(self) -> List[Dict]:
        """Hardcoded schemes data for demo purposes"""
        
        return [
            {
                "id": "pm_kisan",
                "name_hindi": "प्रधानमंत्री किसान सम्मान निधि",
                "name_english": "PM Kisan Samman Nidhi",
                "category": "agriculture",
                "target_group": "farmers",
                "benefits": {
                    "amount": "6000",
                    "description": "₹6,000 per year in 3 installments of ₹2,000 each",
                    "frequency": "yearly"
                },
                "eligibility": {
                    "criteria": "Small and marginal farmers with up to 2 hectares land",
                    "income_limit": "No income limit",
                    "age_limit": "18+"
                },
                "documents": ["Aadhaar Card", "Land Records", "Bank Account"],
                "application_process": {
                    "website": "pmkisan.gov.in",
                    "steps": ["Visit pmkisan.gov.in", "Register with Aadhaar", "Fill farmer details", "Upload land records", "Submit application"]
                },
                "keywords": ["किसान", "farmer", "6000", "agriculture", "kisan", "farming", "खेती"]
            },
            {
                "id": "ayushman_bharat",
                "name_hindi": "आयुष्मान भारत प्रधानमंत्री जन आरोग्य योजना",
                "name_english": "Ayushman Bharat PMJAY",
                "category": "health",
                "target_group": "low_income_families",
                "benefits": {
                    "amount": "500000",
                    "description": "₹5 lakh health insurance coverage per family per year",
                    "frequency": "yearly"
                },
                "eligibility": {
                    "criteria": "BPL families and lower middle class as per SECC 2011",
                    "income_limit": "BPL category",
                    "age_limit": "All ages"
                },
                "documents": ["Aadhaar Card", "Ration Card", "Income Certificate"],
                "application_process": {
                    "website": "pmjay.gov.in",
                    "steps": ["Visit nearest Jan Aushadhi Kendra", "Verify eligibility", "Get Golden Card made", "Use at empaneled hospitals"]
                },
                "keywords": ["health", "स्वास्थ्य", "5 lakh", "insurance", "ayushman", "pmjay", "बीमा", "इलाज"]
            },
            {
                "id": "pm_awas_urban",
                "name_hindi": "प्रधानमंत्री आवास योजना शहरी",
                "name_english": "PM Awas Yojana Urban",
                "category": "housing",
                "target_group": "urban_poor",
                "benefits": {
                    "amount": "267000",
                    "description": "₹2.67 lakh subsidy for home construction/purchase",
                    "frequency": "one_time"
                },
                "eligibility": {
                    "criteria": "EWS, LIG, MIG families without pucca house",
                    "income_limit": "₹18 lakh per annum for MIG",
                    "age_limit": "18+"
                },
                "documents": ["Aadhaar Card", "Income Certificate", "Property Documents"],
                "application_process": {
                    "website": "pmaymis.gov.in",
                    "steps": ["Visit pmaymis.gov.in", "Fill online application", "Upload documents", "Submit and track status"]
                },
                "keywords": ["house", "घर", "awas", "आवास", "home", "subsidy", "housing", "मकान"]
            },
            {
                "id": "national_scholarship",
                "name_hindi": "राष्ट्रीय छात्रवृत्ति पोर्टल",
                "name_english": "National Scholarship Portal",
                "category": "education",
                "target_group": "students",
                "benefits": {
                    "amount": "36000",
                    "description": "Up to ₹36,000 per year for higher education",
                    "frequency": "yearly"
                },
                "eligibility": {
                    "criteria": "Students from SC/ST/OBC/Minority communities",
                    "income_limit": "₹2.5 lakh per annum",
                    "age_limit": "18-25"
                },
                "documents": ["Aadhaar Card", "Marksheets", "Income Certificate", "Caste Certificate"],
                "application_process": {
                    "website": "scholarships.gov.in",
                    "steps": ["Register on NSP portal", "Fill scholarship form", "Upload documents", "Submit before deadline"]
                },
                "keywords": ["scholarship", "छात्रवृत्ति", "student", "education", "nsp", "पढ़ाई"]
            },
            {
                "id": "pm_mudra",
                "name_hindi": "प्रधानमंत्री मुद्रा योजना",
                "name_english": "PM Mudra Yojana",
                "category": "finance",
                "target_group": "micro_enterprises",
                "benefits": {
                    "amount": "1000000",
                    "description": "Loans up to ₹10 lakh for micro enterprises",
                    "frequency": "as_needed"
                },
                "eligibility": {
                    "criteria": "Non-farm small/micro enterprises",
                    "income_limit": "No specific limit",
                    "age_limit": "18+"
                },
                "documents": ["Aadhaar Card", "PAN Card", "Business Plan", "Bank Statements"],
                "application_process": {
                    "website": "mudra.org.in",
                    "steps": ["Prepare business plan", "Visit nearest bank", "Fill loan application", "Submit documents", "Get loan approval"]
                },
                "keywords": ["loan", "business", "mudra", "enterprise", "micro", "व्यापार", "कारोबार"]
            },
            {
                "id": "pm_ujjwala",
                "name_hindi": "प्रधानमंत्री उज्ज्वला योजना",
                "name_english": "PM Ujjwala Yojana",
                "category": "women",
                "target_group": "bpl_women",
                "benefits": {
                    "amount": "1600",
                    "description": "Free LPG connection with ₹1,600 support",
                    "frequency": "one_time"
                },
                "eligibility": {
                    "criteria": "BPL families with women as applicant",
                    "income_limit": "BPL category",
                    "age_limit": "18+"
                },
                "documents": ["BPL Ration Card", "Aadhaar Card", "Bank Account", "Address Proof"],
                "application_process": {
                    "website": "pmuy.gov.in",
                    "steps": ["Visit LPG distributor", "Fill KYC form", "Submit BPL documents", "Get free connection"]
                },
                "keywords": ["lpg", "उज्ज्वला", "gas", "women", "cooking", "रसोई", "गैस"]
            }
        ]
    
    def process_query(self, user_input: str, language: str = "hindi") -> str:
        """Process user query and return appropriate response"""
        
        try:
            # Extract user information
            user_info = self.extract_user_info(user_input)
            
            # Find matching schemes
            matching_schemes = self.find_matching_schemes(user_input, user_info)
            
            # Generate response
            if matching_schemes:
                return self.generate_scheme_response(matching_schemes, language)
            else:
                return self.generate_general_response(user_input, language)
                
        except Exception as e:
            print(f"Error in process_query: {e}")
            return self.get_fallback_response(language)
    
    def extract_user_info(self, user_input: str) -> Dict:
        """Extract user information from input"""
        
        user_input_lower = user_input.lower()
        user_info = {}
        
        # Detect profession/category
        if any(word in user_input_lower for word in ["किसान", "farmer", "खेती", "farming"]):
            user_info["category"] = "agriculture"
            user_info["profession"] = "farmer"
        
        elif any(word in user_input_lower for word in ["student", "छात्र", "पढ़ाई", "study"]):
            user_info["category"] = "education"
            user_info["profession"] = "student"
        
        elif any(word in user_input_lower for word in ["business", "व्यापार", "कारोबार", "startup"]):
            user_info["category"] = "finance"
            user_info["profession"] = "business"
        
        elif any(word in user_input_lower for word in ["health", "स्वास्थ्य", "इलाज", "hospital"]):
            user_info["category"] = "health"
        
        elif any(word in user_input_lower for word in ["house", "घर", "आवास", "home", "मकान"]):
            user_info["category"] = "housing"
        
        elif any(word in user_input_lower for word in ["job", "काम", "employment", "skill"]):
            user_info["category"] = "employment"
        
        elif any(word in user_input_lower for word in ["women", "महिला", "lpg", "gas"]):
            user_info["category"] = "women"
        
        # Extract age if mentioned
        age_match = re.search(r'(\d+)\s*(?:साल|year|age|उम्र)', user_input_lower)
        if age_match:
            user_info["age"] = int(age_match.group(1))
        
        return user_info
    
    def find_matching_schemes(self, user_input: str, user_info: Dict) -> List[Dict]:
        """Find schemes matching user query"""
        
        matching_schemes = []
        user_input_lower = user_input.lower()
        
        for scheme in self.schemes_data:
            score = 0
            
            # Category match
            if user_info.get("category") == scheme.get("category"):
                score += 5
            
            # Keyword match
            keywords = scheme.get("keywords", [])
            for keyword in keywords:
                if keyword.lower() in user_input_lower:
                    score += 3
            
            # Target group match
            target_group = scheme.get("target_group", "")
            if user_info.get("profession") and user_info["profession"] in target_group:
                score += 4
            
            # Add scheme if it has any relevance
            if score > 0:
                scheme["match_score"] = score
                matching_schemes.append(scheme)
        
        # Sort by relevance score
        matching_schemes.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        
        return matching_schemes[:3]  # Return top 3 matches
    
    def generate_scheme_response(self, schemes: List[Dict], language: str) -> str:
        """Generate response with scheme information"""
        
        if language == "english":
            response = "Great! Here are the government schemes for you:\n\n"
        else:
            response = "बहुत अच्छा! आपके लिए ये सरकारी योजनाएं हैं:\n\n"
        
        for i, scheme in enumerate(schemes, 1):
            if language == "english":
                response += f"**{i}. {scheme['name_english']}**\n"
                response += f"💰 Benefit: {scheme['benefits']['description']}\n"
                response += f"✅ Eligibility: {scheme['eligibility']['criteria']}\n"
                response += f"📄 Documents: {', '.join(scheme['documents'][:3])}\n"
                response += f"🌐 Apply: {scheme['application_process']['website']}\n\n"
            else:
                response += f"**{i}. {scheme['name_hindi']}**\n"
                response += f"💰 लाभ: {scheme['benefits']['description']}\n"
                response += f"✅ पात्रता: {scheme['eligibility']['criteria']}\n"
                response += f"📄 दस्तावेज: {', '.join(scheme['documents'][:3])}\n"
                response += f"🌐 आवेदन: {scheme['application_process']['website']}\n\n"
        
        if language == "english":
            response += "Would you like more details about any specific scheme?"
        else:
            response += "क्या आप किसी विशेष योजना के बारे में और जानकारी चाहते हैं?"
        
        return response
    
    def generate_general_response(self, user_input: str, language: str) -> str:
        """Generate general response when no specific schemes match"""
        
        if language == "english":
            return """
I can help you find government schemes! Please tell me:
- What is your profession? (farmer, student, business owner, etc.)
- What kind of help do you need? (financial, health, education, housing)
- Your age group?

Popular schemes:
🌾 PM Kisan - ₹6,000/year for farmers
🏥 Ayushman Bharat - ₹5 lakh health insurance
🎓 Scholarships - Up to ₹36,000 for students
🏠 PM Awas - ₹2.67 lakh housing subsidy
💼 Mudra Loan - Up to ₹10 lakh for business
            """
        else:
            return """
मैं आपको सरकारी योजना खोजने में मदद कर सकता हूं! कृपया बताएं:
- आप क्या काम करते हैं? (किसान, छात्र, व्यापारी, आदि)
- आपको किस तरह की मदद चाहिए? (पैसा, स्वास्थ्य, शिक्षा, घर)
- आपकी उम्र कितनी है?

प्रमुख योजनाएं:
🌾 PM Kisan - किसानों को ₹6,000/साल
🏥 आयुष्मान भारत - ₹5 लाख स्वास्थ्य बीमा
🎓 छात्रवृत्ति - छात्रों को ₹36,000 तक
🏠 PM आवास - घर के लिए ₹2.67 लाख
💼 मुद्रा लोन - व्यापार के लिए ₹10 लाख तक
            """
    
    def get_fallback_response(self, language: str) -> str:
        """Fallback response when there's an error"""
        
        if language == "english":
            return "I'm here to help you find government schemes! Please ask about farmers, health, education, housing, or business schemes."
        else:
            return "मैं आपको सरकारी योजनाओं के बारे में बताने के लिए यहां हूं! किसान, स्वास्थ्य, शिक्षा, आवास, या व्यापार योजनाओं के बारे में पूछें।"