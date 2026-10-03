"""
Multilingual Localization & Translation Engine for ScamShield AI.
Provides simple, jargon-free local language explanations and warning cards
for English, Hindi, Tamil, Telugu, Malayalam, and Kannada.
"""
from typing import Dict, Any

LANGUAGES = {
    "en": "English",
    "hi": "हिन्दी (Hindi)",
    "ta": "தமிழ் (Tamil)",
    "te": "తెలుగు (Telugu)",
    "ml": "മലയാളം (Malayalam)",
    "kn": "ಕನ್ನಡ (Kannada)"
}

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "classification_safe": "SAFE",
        "classification_suspicious": "SUSPICIOUS",
        "classification_scam": "HIGH RISK SCAM",
        "summary_high_risk": "This message exhibits strong characteristics of a financial or phishing scam designed to steal credentials or money.",
        "summary_suspicious": "This communication contains suspicious psychological pressure or unverified links. Exercise caution.",
        "summary_safe": "No obvious scam indicators found. Standard vigilance is still advised.",
        "urgency_explanation": "Creates artificial panic and rushes you into making a hasty decision before checking.",
        "threat_explanation": "Uses intimidation such as account suspension or fake legal threats to frighten you.",
        "credential_explanation": "Attempts to steal your passwords, banking PIN, or sensitive personal documents.",
        "otp_explanation": "Tries to get your 6-digit OTP code. Sharing this gives the scammer access to your money.",
        "financial_explanation": "Demands money transfers, advance fees, or processing charges.",
        "domain_explanation": "The website address is fake and does not belong to the official bank or company.",
        "action_dont_click": "Do not click the link or open attachments.",
        "action_dont_share_otp": "Never share your OTP or password with anyone, even if they claim to be a bank manager.",
        "action_verify_official": "Check directly using the official bank app or by typing the official website yourself.",
        "guardian_title": "SCAM ALERT FOR FAMILY",
        "guardian_warning": "Warning: A message pretending to be an urgent bank or delivery notification has been detected. Do not click links or share OTPs."
    },
    "ta": {
        "classification_safe": "பாதுகாப்பானது",
        "classification_suspicious": "சந்தேகத்திற்குரியது",
        "classification_scam": "அதிக ஆபத்துள்ள மோசடி",
        "summary_high_risk": "இந்த செய்தி உங்கள் பணம் அல்லது வங்கிக் கணக்கு விவரங்களைத் திருடுவதற்கான மோசடி ஆகும்.",
        "summary_suspicious": "இந்த செய்தியில் அவசரப்படுத்தும் வார்த்தைகள் அல்லது சரிபார்க்கப்படாத இணைப்புகள் உள்ளன. கவனமாக இருங்கள்.",
        "summary_safe": "வெளிப்படையான மோசடி அறிகுறிகள் எதுவும் இல்லை. எப்போதும் விழிப்புடன் இருங்கள்.",
        "urgency_explanation": "இந்த செய்தி உங்களை அவசரமாக செயல்பட வைக்க முயற்சிக்கிறது.",
        "threat_explanation": "கணக்கு முடக்கப்படும் அல்லது காவல் துறை நடவடிக்கை எடுக்கப்படும் என்று உங்களை பயமுறுத்துகிறது.",
        "credential_explanation": "உங்கள் கடவுச்சொல், ஏடிஎம் பின் அல்லது ஆவணங்களை திருட முயற்சிக்கிறது.",
        "otp_explanation": "உங்கள் OTP ரகசிய எண்ணை கேட்கிறது. இதை பகிர்ந்தால் உங்கள் வங்கிக் கணக்கில் உள்ள பணம் திருடப்படலாம்.",
        "financial_explanation": "முன்பணம் அல்லது கட்டணம் செலுத்துமாறு உங்களை கேட்கிறது.",
        "domain_explanation": "இந்த இணையதள முகவரி போலியானது; இது வங்கியின் அதிகாரப்பூர்வ தளம் அல்ல.",
        "action_dont_click": "எந்த லிங்க்கையும் கிளிக் செய்யாதீர்கள்.",
        "action_dont_share_otp": "உங்கள் OTP அல்லது கடவுச்சொல்லை யாரிடமும் பகிராதீர்கள்.",
        "action_verify_official": "வங்கியின் அதிகாரப்பூர்வ செயலி மூலமாக மட்டுமே சரிபாருங்கள்.",
        "guardian_title": "குடும்பத்தினருக்கான மோசடி எச்சரிக்கை",
        "guardian_warning": "எச்சரிக்கை: வங்கி அல்லது பார்சல் என்ற பெயரில் போலி குறுஞ்செய்தி பரவுகிறது. லிங்க்கை கிளிக் செய்யாதீர்கள், OTP சொல்லாதீர்கள்."
    },
    "hi": {
        "classification_safe": "सुरक्षित",
        "classification_suspicious": "संदेहास्पद",
        "classification_scam": "अत्यधिक जोखिमपूर्ण घोटाला",
        "summary_high_risk": "यह संदेश आपके पैसे या बैंकिंग क्रेडेंशियल चुराने के लिए बनाया गया एक फ़िशिंग स्कैम प्रतीत होता है।",
        "summary_suspicious": "इस संदेश में दबाव बनाने वाले शब्द या असत्यापित लिंक शामिल हैं। सावधानी बरतें।",
        "summary_safe": "कोई स्पष्ट घोटाला संकेत नहीं मिला। सामान्य सावधानी बनाए रखें।",
        "urgency_explanation": "यह संदेश आपको बिना सोचे-समझे तुरंत प्रतिक्रिया देने के लिए जल्दबाजी कराता है।",
        "threat_explanation": "खाता बंद करने या पुलिस कार्रवाई का डर दिखाकर आपको डराया जा रहा है।",
        "credential_explanation": "यह आपके पासवर्ड, पिन या पहचान पत्रों को चुराने का प्रयास कर रहा है।",
        "otp_explanation": "यह आपका 6-अंकों का ओटीपी मांग रहा है। इसे साझा करने से आपका बैंक खाता खाली हो सकता है।",
        "financial_explanation": "अनावश्यक अग्रिम शुल्क या पैसों के ट्रांसफर की मांग कर रहा है।",
        "domain_explanation": "यह वेबसाइट लिंक नकली है और आधिकारिक बैंक का नहीं है।",
        "action_dont_click": "दिए गए लिंक पर बिल्कुल क्लिक न करें।",
        "action_dont_share_otp": "अपना ओटीपी, पासवर्ड या पिन किसी के साथ भी साझा न करें।",
        "action_verify_official": "केवल आधिकारिक बैंक ऐप या वेबसाइट पर जाकर ही जांच करें।",
        "guardian_title": "परिवार के लिए स्कैम चेतावनी",
        "guardian_warning": "सावधान: बैंक या डिलीवरी के नाम पर नकली संदेश भेजा जा रहा है। किसी लिंक पर क्लिक न करें और ओटीपी साझा न करें।"
    },
    "te": {
        "classification_safe": "సురక్షితం",
        "classification_suspicious": "అనుమానాస్పదం",
        "classification_scam": "తీవ్రమైన మోసం (స్కామ్)",
        "summary_high_risk": "ఈ సందేశం మీ బ్యాంకింగ్ వివరాలు లేదా డబ్బును దొంగిలించడానికి రూపొందించిన మోసం.",
        "summary_suspicious": "ఈ సందేశంలో అనుమానాస్పద లింకులు లేదా ఒత్తిడి చేసే పదాలు ఉన్నాయి. జాగ్రత్తగా ఉండండి.",
        "summary_safe": "స్పష్టమైన మోసపూరిత గుర్తులు ఏవీ కనుగొనబడలేదు. అప్రమత్తంగా ఉండండి.",
        "urgency_explanation": "ఈ సందేశం మిమ్మల్ని ఆలోచించకుండా త్వరగా స్పందించేలా ఒత్తిడి చేస్తోంది.",
        "threat_explanation": "ఖాతా రద్దు చేయబడుతుందని లేదా చట్టపరమైన చర్యలు ఉంటాయని బెదిరిస్తోంది.",
        "credential_explanation": "మీ పాస్‌వర్డ్ లేదా బ్యాంక్ పిన్ వివరాలను దొంగిలించడానికి ప్రయత్నిస్తోంది.",
        "otp_explanation": "మీ ఓటీపీ (OTP) అడుగుతోంది. దీన్ని పంచుకుంటే ఖాతాలోని డబ్బు పోయే ప్రమాదం ఉంది.",
        "financial_explanation": "డబ్బు బదిలీ చేయాలని లేదా రుసుము చెల్లించాలని డిమాండ్ చేస్తోంది.",
        "domain_explanation": "ఈ వెబ్‌సైట్ లింక్ నకిలీది, అధికారిక బ్యాంకుకు చెందినది కాదు.",
        "action_dont_click": "లింక్‌పై ఎట్టిపరిస్థితుల్లోనూ క్లిక్ చేయవద్దు.",
        "action_dont_share_otp": "మీ OTP లేదా పిన్ ఎవరితోనూ పంచుకోవద్దు.",
        "action_verify_official": "అధికారిక యాప్ లేదా వెబ్‌సైట్ ద్వారా మాత్రమే సరిచూసుకోండి.",
        "guardian_title": "కుటుంబ సభ్యులకు హెచ్చరిక",
        "guardian_warning": "హెచ్చరిక: బ్యాంకు పేరిట మోసపూరిత మెసేజ్ వచ్చింది. లింకులు క్లిక్ చేయకండి, OTP ఇవ్వకండి."
    },
    "ml": {
        "classification_safe": "സുരക്ഷിതം",
        "classification_suspicious": "സംശയാസ്പദം",
        "classification_scam": "വലിയ തട്ടിപ്പ് (സ്കാം)",
        "summary_high_risk": "നിങ്ങളുടെ ബാങ്കിംഗ് വിവരങ്ങളോ പണമോ തട്ടിയെടുക്കാൻ ലക്ഷ്യമിട്ടുള്ള വ്യാജ സന്ദേശമാണിത്.",
        "summary_suspicious": "ഈ സന്ദേശത്തിൽ സംശയാസ്പദമായ ലിങ്കുകളും സമ്മർദ്ദമുണ്ടാക്കുന്ന വാക്കുകളും അടങ്ങിയിരിക്കുന്നു.",
        "summary_safe": "വ്യക്തമായ തട്ടിപ്പ് ലക്ഷണങ്ങൾ കണ്ടെത്തിയില്ല. ശ്രദ്ധ പുലർത്തുക.",
        "urgency_explanation": "ആലോചിക്കാൻ സമയം തരാതെ വേഗത്തിൽ പ്രവർത്തിക്കാൻ നിങ്ങളെ നിർബന്ധിക്കുന്നു.",
        "threat_explanation": "അക്കൗണ്ട് ബ്ലോക്ക് ചെയ്യുമെന്നോ നിയമനടപടി സ്വീകരിക്കുമെന്നോ ഭീഷണിപ്പെടുത്തുന്നു.",
        "credential_explanation": "നിങ്ങളുടെ പാസ്‌വേഡോ ബാങ്കിംഗ് പിൻ നമ്പറോ ചോർത്താൻ ശ്രമിക്കുന്നു.",
        "otp_explanation": "നിങ്ങളുടെ ഒടിപി (OTP) ആവശ്യപ്പെടുന്നു. ഇത് നൽകിയാൽ പണം നഷ്ടപ്പെടാം.",
        "financial_explanation": "മുൻകൂർ ഫീസോ പണമോ കൈമാറാൻ ആവശ്യപ്പെടുന്നു.",
        "domain_explanation": "ഈ വെബ്സൈറ്റ് വിലാസം വ്യാജമാണ്, ബാങ്കിന്റെ യഥാർത്ഥ സൈറ്റല്ല.",
        "action_dont_click": "ലിങ്കിൽ ക്ലിക്ക് ചെയ്യരുത്.",
        "action_dont_share_otp": "ഒടിപിയോ പാസ്‌വേഡോ ആരുമായും പങ്കിടരുത്.",
        "action_verify_official": "ഔദ്യോഗിക ആപ്പ് വഴി മാത്രം വിവരങ്ങൾ ഉറപ്പുവരുത്തുക.",
        "guardian_title": "കുടുംബാംഗങ്ങൾക്കുള്ള മുന്നറിയിപ്പ്",
        "guardian_warning": "മുന്നറിയിപ്പ്: വ്യാജ ബാങ്ക് സന്ദേശങ്ങൾ പ്രചരിക്കുന്നു. ലിങ്കുകൾ ക്ലിക്ക് ചെയ്യുകയോ ഒടിപി പങ്കിടുകയോ ചെയ്യരുത്."
    },
    "kn": {
        "classification_safe": "ಸುರಕ್ಷಿತ",
        "classification_suspicious": "ಅನುಮಾನಾಸ್ಪದ",
        "classification_scam": "ಹೆಚ್ಚಿನ ಅಪಾಯದ ವಂಚನೆ",
        "summary_high_risk": "ಈ ಸಂದೇಶವು ನಿಮ್ಮ ಬ್ಯಾಂಕಿಂಗ್ ವಿವರಗಳು ಅಥವಾ ಹಣವನ್ನು ಕದಿಯಲು ರೂಪಿಸಲಾದ ವಂಚನೆಯಾಗಿದೆ.",
        "summary_suspicious": "ಈ ಸಂದೇಶದಲ್ಲಿ ಆತುರಪಡಿಸುವ ಅಥವಾ ಅನುಮಾನಾಸ್ಪದ ಲಿಂಕ್‌ಗಳಿವೆ. ಎಚ್ಚರವಹಿಸಿ.",
        "summary_safe": "ಯಾವುದೇ ಸ್ಪಷ್ಟ ವಂಚನೆಯ ಲಕ್ಷಣಗಳು ಕಂಡುಬಂದಿಲ್ಲ. ಜಾಗರೂಕರಾಗಿರಿ.",
        "urgency_explanation": "ಯೋಚಿಸದೆ ತಕ್ಷಣ ಪ್ರತಿಕ್ರಿಯಿಸುವಂತೆ ಈ ಸಂದೇಶವು ನಿಮ್ಮ ಮೇಲೆ ಒತ್ತಡ ಹೇರುತ್ತದೆ.",
        "threat_explanation": "ಖಾತೆ ನಿರ್ಬಂಧಿಸುವುದಾಗಿ ಅಥವಾ ಕಾನೂನು ಕ್ರಮ ಜರುಗಿಸುವುದಾಗಿ ಹೆದರಿಸಲಾಗುತ್ತಿದೆ.",
        "credential_explanation": "ನಿಮ್ಮ ಪಾಸ್‌ವರ್ಡ್ ಅಥವಾ ಬ್ಯಾಂಕಿಂಗ್ ಪಿನ್ ಕದಿಯಲು ಯತ್ನಿಸುತ್ತಿದೆ.",
        "otp_explanation": "ನಿಮ್ಮ ಒಟಿಪಿ (OTP) ಕೇಳುತ್ತಿದೆ. ಇದನ್ನು ಹಂಚಿಕೊಂಡರೆ ಹಣ ಕಳೆದುಕೊಳ್ಳುವ ಅಪಾಯವಿದೆ.",
        "financial_explanation": "ಮುಂಗಡ ಹಣ ಅಥವಾ ಶುಲ್ಕ ಪಾವತಿಸಲು ಒತ್ತಾಯಿಸುತ್ತಿದೆ.",
        "domain_explanation": "ಈ ವೆಬ್‌ಸೈಟ್ ವಿಳಾಸ ನಕಲಿಯಾಗಿದ್ದು, ಅಧಿಕೃತ ಬ್ಯಾಂಕಿನದ್ದಲ್ಲ.",
        "action_dont_click": "ಯಾವುದೇ ಕಾರಣಕ್ಕೂ ಲಿಂಕ್ ಕ್ಲಿಕ್ ಮಾಡಬೇಡಿ.",
        "action_dont_share_otp": "ನಿಮ್ಮ ಒಟಿಪಿ ಅಥವಾ ಪಾಸ್‌ವರ್ಡ್ ಯಾರೊಂದಿಗೂ ಹಂಚಿಕೊಳ್ಳಬೇಡಿ.",
        "action_verify_official": "ಕೇವಲ ಅಧಿಕೃತ ಬ್ಯಾಂಕ್ ಆ್ಯಪ್ ಮೂಲಕವೇ ಪರಿಶೀಲಿಸಿ.",
        "guardian_title": "ಕುಟುಂಬದವರಿಗೆ ವಂಚನೆ ಎಚ್ಚರಿಕೆ",
        "guardian_warning": "ಎಚ್ಚರಿಕೆ: ಬ್ಯಾಂಕ್ ಹೆಸರಿನಲ್ಲಿ ನಕಲಿ ಸಂದೇಶಗಳು ಬರುತ್ತಿವೆ. ಲಿಂಕ್‌ಗಳನ್ನು ಕ್ಲಿಕ್ ಮಾಡಬೇಡಿ ಮತ್ತು ಒಟಿಪಿ ನೀಡಬೇಡಿ."
    }
}

def get_localized_explanations(classification: str) -> Dict[str, Dict[str, str]]:
    """Generate localized summaries and warnings for all supported languages."""
    result = {}
    for lang_code, t_dict in TRANSLATIONS.items():
        if classification == "SAFE":
            summary = t_dict["summary_safe"]
            status = t_dict["classification_safe"]
        elif classification == "SUSPICIOUS":
            summary = t_dict["summary_suspicious"]
            status = t_dict["classification_suspicious"]
        else:
            summary = t_dict["summary_high_risk"]
            status = t_dict["classification_scam"]
            
        result[lang_code] = {
            "language": LANGUAGES[lang_code],
            "status": status,
            "summary": summary,
            "guardian_title": t_dict["guardian_title"],
            "guardian_warning": t_dict["guardian_warning"],
            "primary_action": t_dict["action_dont_click"] if classification != "SAFE" else t_dict["action_verify_official"]
        }
    return result
