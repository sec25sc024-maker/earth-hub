import os
import webbrowser
from threading import Timer
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder=".")
CORS(app)

# Comprehensive Scholarship Dataset (All 22 Schemes)
SCHOLARSHIPS_DB = [
    {
        "id": 1,
        "name": {
            "en": "BC / MBC Scholarship (TN Govt)",
            "ta": "பிற்படுத்தப்பட்டோர் / மிகப்பிற்படுத்தப்பட்டோர் நல உதவித்தொகை",
            "hi": "पिछड़ा वर्ग / अति पिछड़ा वर्ग छात्रवृत्ति (तमिलनाडु सरकार)"
        },
        "type": {"en": "State Government", "ta": "மாநில அரசு", "hi": "राज्य सरकार"},
        "max_income": 200000,
        "caste_allowed": ["OBC / BC / MBC", "BC", "MBC"],
        "min_marks": 0,
        "value": {
            "en": "Tuition Fees + Special Allowances",
            "ta": "கல்விக் கட்டணம் + சிறப்பு உதவித்தொகை",
            "hi": "शिक्षण शुल्क एवं विशेष भत्ता"
        },
        "documents": {
            "en": "Income Certificate from Tahsildar, 1st Graduate Certificate (if applicable), Community Certificate, Marksheet",
            "ta": "தாசில்தார் வருமானச் சான்றிதழ், முதல் பட்டதாரி சான்றிதழ் (பொருந்தினால்), சாதிச் சான்றிதழ், மதிப்பெண் சான்றிதழ்",
            "hi": "तहसीलदार द्वारा जारी आय प्रमाण पत्र, प्रथम स्नातक प्रमाण पत्र, जाति प्रमाण पत्र, अंक पत्र"
        },
        "where": {
            "en": "T.N. Govt BC / MBC Welfare Officer / CEG Scholarship Office",
            "ta": "தமிழ்நாடு அரசு பிசி/எம்பிசி நல அலுவலகம் / கல்லூரி உதவித்தொகை பிரிவு",
            "hi": "तमिलनाडु सरकार पिछड़ा वर्ग कल्याण कार्यालय / कॉलेज छात्रवृत्ति अनुभाग"
        }
    },
    {
        "id": 2,
        "name": {
            "en": "SC / ST Post-Matric Scholarship",
            "ta": "ஆதிதிராவிடர் மற்றும் பழங்குடியினர் கல்வி உதவித்தொகை",
            "hi": "अनुसूचित जाति / जनजाति पोस्ट-मैट्रिक छात्रवृत्ति"
        },
        "type": {"en": "State Government", "ta": "மாநில அரசு", "hi": "राज्य सरकार"},
        "max_income": 250000,
        "caste_allowed": ["SC", "ST"],
        "min_marks": 0,
        "value": {
            "en": "100% Compulsory Tuition Fee + Maintenance Allowance",
            "ta": "முழு கல்விக் கட்டண விலக்கு + மாதாந்திர பராமரிப்பு உதவித்தொகை",
            "hi": "100% शिक्षण शुल्क छूट एवं मासिक रखरखाव भत्ता"
        },
        "documents": {
            "en": "Tahsildar Income Certificate, SC/ST Community Certificate, Bank Passbook, ID Proof, Marksheet",
            "ta": "வருமானச் சான்றிதழ், ஆதிதிராவிடர் சாதிச் சான்றிதழ், வங்கி கணக்கு புத்தகம், அடையாள அட்டை, மதிப்பெண் சான்றிதழ்",
            "hi": "आय प्रमाण पत्र, जाति प्रमाण पत्र, बैंक पासबुक, पहचान पत्र, अंक पत्र"
        },
        "where": {
            "en": "TN Adi-Dravidar & Tribal Welfare Dept / College Scholarship Section",
            "ta": "தமிழ்நாடு ஆதிதிராவிடர் மற்றும் பழங்குடியினர் நலத்துறை / கல்லூரி உதவித்தொகை பிரிவு",
            "hi": "तमिलनाडु आदि-द्रविड़ और जनजाति कल्याण विभाग"
        }
    },
    {
        "id": 3,
        "name": {
            "en": "Chief Minister Award for SC / ST Students",
            "ta": "ஆதிதிராவிடர் / பழங்குடியின மாணவர்களுக்கான முதலமைச்சர் விருது",
            "hi": "अनुसूचित जाति / जनजाति छात्रों के लिए मुख्यमंत्री पुरस्कार"
        },
        "type": {"en": "State Government", "ta": "மாநில அரசு", "hi": "राज्य सरकार"},
        "max_income": 9999999,
        "caste_allowed": ["SC", "ST"],
        "min_marks": 75,
        "value": {
            "en": "Rs. 3,000 / year",
            "ta": "ஆண்டுக்கு ரூ. 3,000",
            "hi": "3,000 रुपये प्रति वर्ष"
        },
        "documents": {
            "en": "+2 Marksheet, School Recommendation Letter, Community Certificate, Bank Details",
            "ta": "+2 மதிப்பெண் சான்றிதழ், பள்ளி பரிந்துரை கடிதம், சாதிச் சான்றிதழ், வங்கி விவரங்கள்",
            "hi": "12वीं का अंक पत्र, स्कूल सिफारिश पत्र, जाति प्रमाण पत्र, बैंक विवरण"
        },
        "where": {
            "en": "District Collectorate / School Education Dept (Recommended via School)",
            "ta": "மாவட்ட ஆட்சியர் அலுவலகம் / பள்ளி கல்வித்துறை",
            "hi": "जिला कलेक्टर कार्यालय / स्कूल शिक्षा विभाग"
        }
    },
    {
        "id": 4,
        "name": {
            "en": "SC / ST Special Higher Education Scholarship",
            "ta": "ஆதிதிராவிடர் மற்றும் பழங்குடியினர் சிறப்பு உயர்கல்வி உதவித்தொகை",
            "hi": "अनुसूचित जाति / जनजाति विशेष उच्च शिक्षा छात्रवृत्ति"
        },
        "type": {"en": "State Government", "ta": "மாநில அரசு", "hi": "राज्य सरकार"},
        "max_income": 200000,
        "caste_allowed": ["SC", "ST"],
        "min_marks": 0,
        "value": {
            "en": "Rs. 8,000 / year",
            "ta": "ஆண்டுக்கு ரூ. 8,000",
            "hi": "8,000 रुपये प्रति वर्ष"
        },
        "documents": {
            "en": "Income Certificate from Tahsildar, SC/ST Community Certificate, Hostel Warden Bonafide",
            "ta": "தாசில்தார் வருமானச் சான்றிதழ், சாதிச் சான்றிதழ், விடுதி காப்பாளர் சான்றிதழ்",
            "hi": "आय प्रमाण पत्र, जाति प्रमाण पत्र, हॉस्टल बोनाफाइड"
        },
        "where": {
            "en": "Commissioner, SC/ST Adi-Dravida and Tribes Welfare Officer / CEG Section",
            "ta": "ஆதிதிராவிடர் மற்றும் பழங்குடியினர் நல ஆணையர் அலுவலகம்",
            "hi": "आदि-द्रविड़ और जनजाति कल्याण आयुक्त कार्यालय"
        }
    },
    {
        "id": 5,
        "name": {
            "en": "Gandhi Memorial Award (SC/ST Top Students)",
            "ta": "காந்தி நினைவக விருது (பள்ளி முதன்மை மாணவர்கள்)",
            "hi": "गांधी मेमोरियल पुरस्कार (अनुसूचित जाति / जनजाति)"
        },
        "type": {"en": "State Government", "ta": "மாநில அரசு", "hi": "राज्य सरकार"},
        "max_income": 9999999,
        "caste_allowed": ["SC", "ST"],
        "min_marks": 80,
        "value": {
            "en": "1st Yr: Rs. 1,500 | 2nd-4th Yr: Rs. 1,000 / year",
            "ta": "1ம் ஆண்டு: ரூ. 1,500 | 2-4ம் ஆண்டு: ரூ. 1,000",
            "hi": "प्रथम वर्ष: 1,500 रुपये | 2-4 वर्ष: 1,000 रुपये"
        },
        "documents": {
            "en": "School Top Rank Certificate, School Recommendation, Marksheet, Community Certificate",
            "ta": "பள்ளி முதன்மை தரவரிசைச் சான்றிதழ், பள்ளி பரிந்துரை, மதிப்பெண் சான்றிதழ்",
            "hi": "स्कूल टॉप रैंक प्रमाण पत्र, सिफारिश पत्र, अंक पत्र"
        },
        "where": {
            "en": "Collector Office / Recommended by High School Headmaster",
            "ta": "மாவட்ட ஆட்சியர் அலுவலகம் / பள்ளி தலைமையாசிரியர் பரிந்துரை",
            "hi": "जिला कलेक्टर कार्यालय / स्कूल हेडमास्टर"
        }
    },
    {
        "id": 6,
        "name": {
            "en": "Chief Minister Award for BC / MBC Top Students",
            "ta": "பிற்படுத்தப்பட்டோர் மாணவர்களுக்கான முதலமைச்சர் விருது",
            "hi": "पिछड़ा वर्ग छात्रों के लिए मुख्यमंत्री पुरस्कार"
        },
        "type": {"en": "State Government", "ta": "மாநில அரசு", "hi": "राज्य सरकार"},
        "max_income": 9999999,
        "caste_allowed": ["OBC / BC / MBC", "BC", "MBC"],
        "min_marks": 80,
        "value": {
            "en": "Rs. 3,000 / year",
            "ta": "ஆண்டுக்கு ரூ. 3,000",
            "hi": "3,000 रुपये प्रति वर्ष"
        },
        "documents": {
            "en": "School Top 1000 Merit Rank Certificate, Marksheet, Community Certificate",
            "ta": "பள்ளி முதன்மை 1000 தரவரிசைச் சான்றிதழ், மதிப்பெண் சான்றிதழ்",
            "hi": "टॉप 1000 मेरिट रैंक प्रमाण पत्र, अंक पत्र"
        },
        "where": {
            "en": "TN BC and Minorities Welfare Officer / School Headmaster",
            "ta": "தமிழ்நாடு பிற்படுத்தப்பட்டோர் நல அலுவலர் / பள்ளி தலைமையாசிரியர்",
            "hi": "पिछड़ा वर्ग और अल्पसंख्यक कल्याण अधिकारी"
        }
    },
    {
        "id": 7,
        "name": {
            "en": "UGC National Scholarship Scheme",
            "ta": "பல்கலைக்கழக மானியக் குழு (UGC) உதவித்தொகை",
            "hi": "यूजीसी राष्ट्रीय छात्रवृत्ति योजना"
        },
        "type": {"en": "Central Government", "ta": "மத்திய அரசு", "hi": "केंद्र सरकार"},
        "max_income": 600000,
        "caste_allowed": ["SC", "ST", "OBC / BC / MBC", "General / OC", "EWS", "DNT"],
        "min_marks": 75,
        "value": {
            "en": "Rs. 1,50,000/- Grant",
            "ta": "ரூ. 1,50,000 உதவி நிதி",
            "hi": "1,50,000 रुपये अनुदान"
        },
        "documents": {
            "en": "UGC Application Form, Academic Marksheets, Bonafide Student Certificate",
            "ta": "UGC விண்ணப்பப் படிவம், கல்வி மதிப்பெண் சான்றிதழ், கல்லூரி மாணவர் சான்றிதழ்",
            "hi": "यूजीसी आवेदन पत्र, शैक्षणिक अंक पत्र, बोनाफाइड प्रमाण पत्र"
        },
        "where": {
            "en": "University Grants Commission (UGC) Portal / College Forwarded",
            "ta": "பல்கலைக்கழக மானியக் குழு (UGC) இணையதளம்",
            "hi": "विश्वविद्यालय अनुदान आयोग (यूजीसी) पोर्टल"
        }
    },
    {
        "id": 8,
        "name": {
            "en": "Merit cum Means Minority Scholarship",
            "ta": "சிறுபான்மையினர் தகுதி மற்றும் வருவாய் வழி உதவித்தொகை",
            "hi": "मेरिट सह साधन अल्पसंख्यक छात्रवृत्ति"
        },
        "type": {"en": "Central / State Govt", "ta": "மத்திய / மாநில அரசு", "hi": "केंद्र / राज्य सरकार"},
        "max_income": 250000,
        "caste_allowed": ["DNT", "General / OC", "OBC / BC / MBC", "SC", "ST", "EWS"],
        "min_marks": 50,
        "value": {
            "en": "Course Fee + Maintenance (Hosteller: Rs. 10,000 | Day Scholar: Rs. 5,000)",
            "ta": "கல்விக் கட்டணம் + பராமரிப்பு உதவித்தொகை",
            "hi": "पाठ्यक्रम शुल्क + रखरखाव भत्ता"
        },
        "documents": {
            "en": "Minority Declaration (Christian, Muslim, Sikh, Buddhist), Income Certificate, Marksheet",
            "ta": "சிறுபான்மையினர் சுயசான்றளிப்பு, வருமானச் சான்றிதழ், முந்தைய தேர்வு மதிப்பெண் சான்று",
            "hi": "अल्पसंख्यक घोषणा पत्र, आय प्रमाण पत्र, अंक पत्र"
        },
        "where": {
            "en": "National Scholarship Portal (scholarships.gov.in)",
            "ta": "தேசிய உதவித்தொகை இணையதளம் (scholarships.gov.in)",
            "hi": "राष्ट्रीय छात्रवृत्ति पोर्टल (scholarships.gov.in)"
        }
    },
    {
        "id": 9,
        "name": {
            "en": "Central Sector Scheme of Scholarship (MHRD)",
            "ta": "மத்திய அரசின் உயர்கல்வி உதவித்தொகைத் திட்டம் (MHRD)",
            "hi": "केंद्रीय क्षेत्र की छात्रवृत्ति योजना"
        },
        "type": {"en": "Central Government", "ta": "மத்திய அரசு", "hi": "केंद्र सरकार"},
        "max_income": 600000,
        "caste_allowed": ["SC", "ST", "OBC / BC / MBC", "General / OC", "EWS", "DNT"],
        "min_marks": 80,
        "value": {
            "en": "Rs. 10,000 / year (UG)",
            "ta": "ஆண்டுக்கு ரூ. 10,000",
            "hi": "10,000 रुपये प्रति वर्ष"
        },
        "documents": {
            "en": "Class 12 Marksheet (>= 80% Top Percentile), Income Certificate, ID Proof, Bank Details",
            "ta": "12ஆம் வகுப்பு மதிப்பெண் சான்றிதழ் (80% மேல்), வருமானச் சான்றிதழ், அடையாள அட்டை, வங்கி விவரங்கள்",
            "hi": "12वीं अंक पत्र (80% या अधिक), आय प्रमाण पत्र, पहचान पत्र, बैंक विवरण"
        },
        "where": {
            "en": "National Scholarship Portal (NSP scholarships.gov.in)",
            "ta": "தேசிய உதவித்தொகை இணையதளம் (NSP scholarships.gov.in)",
            "hi": "राष्ट्रीय छात्रवृत्ति पोर्टल (scholarships.gov.in)"
        }
    },
    {
        "id": 10,
        "name": {
            "en": "Tamil Nadu District Topper Award",
            "ta": "தமிழ்நாடு மாவட்ட அளவிலான முதன்மை மாணவர் விருது",
            "hi": "तमिलनाडु जिला टॉपर पुरस्कार"
        },
        "type": {"en": "State Government", "ta": "மாநில அரசு", "hi": "राज्य सरकार"},
        "max_income": 9999999,
        "caste_allowed": ["SC", "ST", "OBC / BC / MBC", "General / OC", "EWS", "DNT"],
        "min_marks": 90,
        "value": {
            "en": "Total Academic Expenditure Reimbursed",
            "ta": "முழு கல்விச் செலவும் திருப்பி அளிக்கப்படும்",
            "hi": "संपूर्ण शैक्षणिक व्यय प्रतिपूर्ति"
        },
        "documents": {
            "en": "District/State 1st-3rd Rank Certificate in 12th Std, Marksheet, College Bonafide",
            "ta": "12ஆம் வகுப்பில் மாவட்ட/மாநில அளவில் 1 முதல் 3ஆம் இடம் பெற்ற சான்றிதழ்",
            "hi": "12वीं कक्षा में जिला/राज्य स्तरीय प्रथम 3 रैंक प्रमाण पत्र"
        },
        "where": {
            "en": "Chief Educational Officer (CEO), District Education Dept",
            "ta": "முதன்மைக் கல்வி அலுவலர் (CEO), மாவட்டக் கல்வித் துறை",
            "hi": "मुख्य शिक्षा अधिकारी (सीईओ), जिला शिक्षा विभाग"
        }
    },
    {
        "id": 11,
        "name": {
            "en": "NCERT National Talent Search Scholarship",
            "ta": "என்.சி.இ.ஆர்.டி தேசிய திறனாய்வு உதவித்தொகை",
            "hi": "एनसीईआरटी राष्ट्रीय प्रतिभा खोज छात्रवृत्ति"
        },
        "type": {"en": "Central Government", "ta": "மத்திய அரசு", "hi": "केंद्र सरकार"},
        "max_income": 9999999,
        "caste_allowed": ["SC", "ST", "OBC / BC / MBC", "General / OC", "EWS", "DNT"],
        "min_marks": 60,
        "value": {
            "en": "Rs. 6,000 / year",
            "ta": "ஆண்டுக்கு ரூ. 6,000",
            "hi": "6,000 रुपये प्रति वर्ष"
        },
        "documents": {
            "en": "NCERT Selection Exam Scorecard/Certificate, Marksheets, Bonafide",
            "ta": "NCERT தேர்வு தேர்ச்சிச் சான்றிதழ், மதிப்பெண் சான்றிதழ், மாணவர் சான்றிதழ்",
            "hi": "एनसीईआरटी परीक्षा स्कोरकार्ड, अंक पत्र"
        },
        "where": {
            "en": "NCERT National Talent Search Unit, New Delhi",
            "ta": "என்.சி.இ.ஆர்.டி தேசிய திறனாய்வு பிரிவு, புதுடெல்லி",
            "hi": "एनसीईआरटी राष्ट्रीय प्रतिभा खोज इकाई, नई दिल्ली"
        }
    },
    {
        "id": 12,
        "name": {
            "en": "National Teachers Welfare Fund Scholarship",
            "ta": "தேசிய ஆசிரியர் நல நிதி உதவித்தொகை",
            "hi": "राष्ट्रीय शिक्षक कल्याण कोष छात्रवृत्ति"
        },
        "type": {"en": "State Government", "ta": "மாநில அரசு", "hi": "राज्य सरकार"},
        "max_income": 280000,
        "caste_allowed": ["SC", "ST", "OBC / BC / MBC", "General / OC", "EWS", "DNT"],
        "min_marks": 50,
        "value": {
            "en": "Rs. 5,000 / year",
            "ta": "ஆண்டுக்கு ரூ. 5,000",
            "hi": "5,000 रुपये प्रति वर्ष"
        },
        "documents": {
            "en": "Parent's Govt School Teacher Employment Proof, Income Proof, Marksheets",
            "ta": "பெற்றோரின் அரசுப் பள்ளி ஆசிரியர் பணிச்சான்று, வருமானச் சான்றிதழ், மதிப்பெண் சான்று",
            "hi": "माता-पिता का सरकारी स्कूल शिक्षक रोजगार प्रमाण पत्र, आय प्रमाण पत्र"
        },
        "where": {
            "en": "Director of School Education, Chennai / School Portal",
            "ta": "பள்ளிக் கல்வி இயக்குநர் அலுவலகம், சென்னை",
            "hi": "स्कूल शिक्षा निदेशक, चेन्नई"
        }
    },
    {
        "id": 13,
        "name": {
            "en": "National Merit Scholarship (Collegiate Education)",
            "ta": "தேசிய தகுதி உதவித்தொகை (கல்லூரி கல்வி)",
            "hi": "राष्ट्रीय योग्यता छात्रवृत्ति (कॉलेज शिक्षा)"
        },
        "type": {"en": "State Government", "ta": "மாநில அரசு", "hi": "राज्य सरकार"},
        "max_income": 9999999,
        "caste_allowed": ["SC", "ST", "OBC / BC / MBC", "General / OC", "EWS", "DNT"],
        "min_marks": 50,
        "value": {
            "en": "Collegiate Education Merit Grant",
            "ta": "கல்லூரி கல்வி தகுதி உதவி நிதி",
            "hi": "कॉलेज शिक्षा मेरिट अनुदान"
        },
        "documents": {
            "en": "Marksheet showing 50%+ marks, Character and Conduct Certificate",
            "ta": "50% மதிப்பெண் சான்றிதழ், நன்னடத்தை சான்றிதழ்",
            "hi": "50% अंकों के साथ अंक पत्र, चरित्र प्रमाण पत्र"
        },
        "where": {
            "en": "Director of Collegiate Education, Chennai / Forwarded via CEG",
            "ta": "கல்லூரிக் கல்வி இயக்குநர், சென்னை / கல்லூரி வழியாக",
            "hi": "कॉलेज शिक्षा निदेशक, चेन्नई"
        }
    },
    {
        "id": 14,
        "name": {
            "en": "Tamil Nadu Educational Trust Scholarship",
            "ta": "தமிழ்நாடு கல்வி அறக்கட்டளை உதவித்தொகை",
            "hi": "तमिलनाडु शैक्षिक ट्रस्ट छात्रवृत्ति"
        },
        "type": {"en": "Trust / Non-Profit", "ta": "அறக்கட்டளை", "hi": "ट्रस्ट"},
        "max_income": 200000,
        "caste_allowed": ["SC", "ST", "OBC / BC / MBC", "General / OC", "EWS", "DNT"],
        "min_marks": 60,
        "value": {
            "en": "Rs. 5,000 to Rs. 6,000 / year",
            "ta": "ஆண்டுக்கு ரூ. 5,000 முதல் ரூ. 6,000 வரை",
            "hi": "5,000 से 6,000 रुपये प्रति वर्ष"
        },
        "documents": {
            "en": "Income Certificate (< Rs. 2,00,000), No-Arrear Semester Marksheet Proof, Bonafide",
            "ta": "வருமானச் சான்றிதழ் (₹2,00,000 கீழ்), அரியர் இல்லா மதிப்பெண் சான்று",
            "hi": "आय प्रमाण पत्र (2,00,000 रुपये से कम), कोई बैकलाग न होने का अंक पत्र"
        },
        "where": {
            "en": "Tamil Nadu Educational Trust Office, Chennai",
            "ta": "தமிழ்நாடு கல்வி அறக்கட்டளை அலுவலகம், சென்னை",
            "hi": "तमिलनाडु शैक्षिक ट्रस्ट कार्यालय, சென்னை"
        }
    },
    {
        "id": 15,
        "name": {
            "en": "IOCL Scholarship (Indian Oil Corporation)",
            "ta": "இந்தியன் ஆயில் கார்ப்பரேஷன் (IOCL) உதவித்தொகை",
            "hi": "इंडियन ऑयल कॉर्पोरेशन (आईओसीएल) छात्रवृत्ति"
        },
        "type": {"en": "Private / Corporate CSR", "ta": "தனியார் / பொதுத்துறை CSR", "hi": "सार्वजनिक क्षेत्र सीएसआर"},
        "max_income": 9999999,
        "caste_allowed": ["SC", "ST", "OBC / BC / MBC", "General / OC", "EWS", "DNT"],
        "min_marks": 65,
        "value": {
            "en": "Rs. 36,000 / year",
            "ta": "ஆண்டுக்கு ரூ. 36,000",
            "hi": "36,000 रुपये प्रति वर्ष"
        },
        "documents": {
            "en": "IOCL Exam Score, HOD Conduct Performance Certificate, Semester Marksheets",
            "ta": "IOCL தேர்வு சான்றிதழ், துறைத் தலைவர் நன்னடத்தை சான்றிதழ்",
            "hi": "आईओसीएल परीक्षा स्कोर, एचओडी आचरण और प्रदर्शन प्रमाण पत्र"
        },
        "where": {
            "en": "Indian Oil Corporation Portal (Sify Tech / IOCL Portal)",
            "ta": "இந்தியன் ஆயில் கார்ப்பரேஷன் இணையதளம்",
            "hi": "इंडियन ऑयल कॉर्पोरेशन पोर्टल"
        }
    },
    {
        "id": 16,
        "name": {
            "en": "Bank of Tokyo Mitsubishi Scholarship",
            "ta": "டோக்கியோ வங்கி மிட்சுபிஷி கல்வி உதவித்தொகை",
            "hi": "बैंक ऑफ टोक्यो मित्सुबिशी छात्रवृत्ति"
        },
        "type": {"en": "Private / Corporate CSR", "ta": "தனியார் சிஎஸ்ஆர்", "hi": "निजी सीएसआर"},
        "max_income": 36000,
        "caste_allowed": ["SC", "ST", "OBC / BC / MBC", "General / OC", "EWS", "DNT"],
        "min_marks": 70,
        "value": {
            "en": "Rs. 23,100 / year",
            "ta": "ஆண்டுக்கு ரூ. 23,100",
            "hi": "23,100 रुपये प्रति वर्ष"
        },
        "documents": {
            "en": "Income Certificate (< Rs. 36,000/yr), +2 Academic Performance Marksheet, CGPA >= 6.5",
            "ta": "வருமானச் சான்றிதழ் (ஆண்டுக்கு ₹36,000 கீழ்), +2 மதிப்பெண் சான்றிதழ், CGPA 6.5",
            "hi": "आय प्रमाण पत्र (36,000 रुपये से कम), 12वीं अंक पत्र, सीजीपीए 6.5"
        },
        "where": {
            "en": "Bank of Tokyo Mitsubishi Ltd / CEG Dean Office",
            "ta": "பேங்க் ஆஃப் டோக்கியோ மிட்சுபிஷி / சி.இ.ஜி முதல்வர் அலுவலகம்",
            "hi": "बैंक ऑफ टोक्यो मित्सुबिशी / डीन कार्यालय"
        }
    },
    {
        "id": 17,
        "name": {
            "en": "Cognizant Foundation Scholarship (CSE / IT)",
            "ta": "காக்னிசென்ட் பவுண்டேஷன் உதவித்தொகை (கணினி துறை)",
            "hi": "कॉग्निजेंट फाउंडेशन छात्रवृत्ति (सीएसई / आईटी)"
        },
        "type": {"en": "Private / Corporate CSR", "ta": "தனியார் சிஎஸ்ஆர்", "hi": "निजी सीएसआर"},
        "max_income": 200000,
        "caste_allowed": ["SC", "ST", "OBC / BC / MBC", "General / OC", "EWS", "DNT"],
        "min_marks": 70,
        "value": {
            "en": "Rs. 35,000 / year",
            "ta": "ஆண்டுக்கு ரூ. 35,000",
            "hi": "35,000 रुपये प्रति वर्ष"
        },
        "documents": {
            "en": "+2 Marksheet, 1st Sem GPA, Income Proof, 70% Attendance Record, CSE/IT Bonafide",
            "ta": "+2 மதிப்பெண் சான்றிதழ், 1ம் செமஸ்டர் GPA, வருமானச் சான்றிதழ், 70% வருகைப் பதிவு",
            "hi": "12वीं अंक पत्र, पहला सेमेस्टर जीपीए, आय प्रमाण पत्र, 70% उपस्थिति"
        },
        "where": {
            "en": "Cognizant Technology Solutions CSR / CEG CSE Department",
            "ta": "காக்னிசென்ட் சிஎஸ்ஆர் பிரிவு / சி.இ.ஜி கணினித் துறை",
            "hi": "कॉग्निजेंट सीएसआर / सीईजी सीएसई विभाग"
        }
    },
    {
        "id": 18,
        "name": {
            "en": "Handicapped Disability Scholarship (NHFDC)",
            "ta": "மாற்றுத்திறனாளிகளுக்கான மாநில அரசு உதவித்தொகை",
            "hi": "दिव्यांगजन छात्रवृत्ति (एनएचएफडीसी)"
        },
        "type": {"en": "State / Central Govt", "ta": "மாநில / மத்திய அரசு", "hi": "राज्य / केंद्र सरकार"},
        "max_income": 300000,
        "caste_allowed": ["SC", "ST", "OBC / BC / MBC", "General / OC", "EWS", "DNT"],
        "min_marks": 0,
        "value": {
            "en": "Assistive Allowances + Educational Grant",
            "ta": "உதவி உபகரண நிதி + கல்வி உதவித்தொகை",
            "hi": "सहायक भत्ता + शैक्षणिक अनुदान"
        },
        "documents": {
            "en": "Disability Certificate (>40%), Identity Proof, College Bonafide, Marksheets",
            "ta": "மாற்றுத்திறனாளி சான்றிதழ் (40% மேல்), அடையாள அட்டை, கல்லூரி சான்றிதழ்",
            "hi": "दिव्यांगता प्रमाण पत्र (40% से अधिक), पहचान पत्र, बोनाफाइड"
        },
        "where": {
            "en": "NHFDC Official Portal (www.nhfdc.com) / District Welfare Officer",
            "ta": "என்.எச்.எஃப்.டி.சி இணையதளம் (www.nhfdc.com) / மாவட்ட மாற்றுத்திறனாளி நல அலுவலர்",
            "hi": "एनएचएफडीसी पोर्टल (www.nhfdc.com)"
        }
    },
    {
        "id": 19,
        "name": {
            "en": "CEG 72 Trust Endowment Scholarship",
            "ta": "சி.இ.ஜி 72 அறக்கட்டளை முன்னாள் மாணவர் உதவித்தொகை",
            "hi": "सीईजी 72 ट्रस्ट पूर्व छात्र छात्रवृत्ति"
        },
        "type": {"en": "Alumni / Trust", "ta": "முன்னாள் மாணவர் அறக்கட்டளை", "hi": "पूर्व छात्र ट्रस्ट"},
        "max_income": 100000,
        "caste_allowed": ["SC", "ST", "OBC / BC / MBC", "General / OC", "EWS", "DNT"],
        "min_marks": 75,
        "value": {
            "en": "Rs. 8,000 / year",
            "ta": "ஆண்டுக்கு ரூ. 8,000",
            "hi": "8,000 रुपये प्रति वर्ष"
        },
        "documents": {
            "en": "2nd Year Civil/Mech/EEE/ECE Branch Proof, CGPA >= 7.5, Income Proof (< Rs. 1,00,000)",
            "ta": "2ஆம் ஆண்டு சிவில்/மெக்/EEE/ECE துறை சான்று, CGPA 7.5, வருமானச் சான்றிதழ்",
            "hi": "द्वितीय वर्ष सिविल/मैकेनिकल/ईईई/ईसीई शाखा प्रमाण, सीजीपीए 7.5, आय प्रमाण पत्र"
        },
        "where": {
            "en": "CEG 72 Alumni Trust / CEG Dean Office",
            "ta": "சி.இ.ஜி 72 முன்னாள் மாணவர் அறக்கட்டளை / கல்லூரி முதல்வர் அலுவலகம்",
            "hi": "सीईजी 72 पूर्व छात्र ट्रस्ट / डीन कार्यालय"
        }
    },
    {
        "id": 20,
        "name": {
            "en": "CEG 73 Alumni Endowment Scholarship",
            "ta": "சி.இ.ஜி 73 முன்னாள் மாணவர் உதவித்தொகை",
            "hi": "சிஇஜி 73 पूर्व छात्र छात्रवृत्ति"
        },
        "type": {"en": "Alumni / Trust", "ta": "முன்னாள் மாணவர் அறக்கட்டளை", "hi": "पूर्व छात्र ट्रस्ट"},
        "max_income": 9999999,
        "caste_allowed": ["SC", "ST", "OBC / BC / MBC", "General / OC", "EWS", "DNT"],
        "min_marks": 75,
        "value": {
            "en": "Rs. 20,000 / year",
            "ta": "ஆண்டுக்கு ரூ. 20,000",
            "hi": "20,000 रुपये प्रति वर्ष"
        },
        "documents": {
            "en": "+2 PCM Cutoff Marksheet, 1st Year B.E./B.Tech Admission Allotment Order",
            "ta": "+2 கணிதம், இயற்பியல், வேதியியல் மதிப்பெண் சான்று, சேர்க்கை ஆணை",
            "hi": "12वीं पीसीएम अंक पत्र, प्रथम वर्ष प्रवेश आवंटन पत्र"
        },
        "where": {
            "en": "CEG 73 Alumni Association / CEG Dean Office",
            "ta": "சி.இ.ஜி 73 முன்னாள் மாணவர் சங்கம் / கல்லூரி முதல்வர் அலுவலகம்",
            "hi": "सीईजी 73 पूर्व छात्र संघ"
        }
    },
    {
        "id": 21,
        "name": {
            "en": "CEG 1956-60 Alumni Endowment Scholarship",
            "ta": "CEG 1956-60 முன்னாள் மாணவர் அறக்கட்டளை உதவித்தொகை",
            "hi": "CEG 1956-60 पूर्व छात्र छात्रवृत्ति"
        },
        "type": {"en": "Alumni / Trust", "ta": "முன்னாள் மாணவர் அறக்கட்டளை", "hi": "पूर्व छात्र ट्रस्ट"},
        "max_income": 100000,
        "caste_allowed": ["SC", "ST", "OBC / BC / MBC", "General / OC", "EWS", "DNT"],
        "min_marks": 60,
        "value": {
            "en": "Rs. 15,000 / year",
            "ta": "ஆண்டுக்கு ரூ. 15,000",
            "hi": "15,000 रुपये प्रति वर्ष"
        },
        "documents": {
            "en": "Income Proof (< Rs. 1,00,000), 1st Year Marksheet, Bonafide",
            "ta": "வருமானச் சான்றிதழ் (₹1,00,000 கீழ்), மதிப்பெண் சான்றிதழ்",
            "hi": "आय प्रमाण पत्र (1,00,000 रुपये से कम), अंक पत्र"
        },
        "where": {
            "en": "CEG 1956-60 Alumni Batch / CEG Scholarship Office",
            "ta": "CEG 1956-60 முன்னாள் மாணவர்கள் பிரிவு",
            "hi": "सीईजी 1956-60 पूर्व छात्र अनुभाग"
        }
    },
    {
        "id": 22,
        "name": {
            "en": "Anna University Chennai Student Welfare Endowment",
            "ta": "அண்ணா பல்கலைக்கழக மாணவர் நல அறக்கட்டளை உதவித்தொகை",
            "hi": "अन्ना विश्वविद्यालय छात्र कल्याण छात्रवृत्ति"
        },
        "type": {"en": "University Endowment", "ta": "பல்கலைக்கழக நிதி", "hi": "विश्वविद्यालय बंदोबस्ती"},
        "max_income": 100000,
        "caste_allowed": ["SC", "ST", "OBC / BC / MBC", "General / OC", "EWS", "DNT"],
        "min_marks": 60,
        "value": {
            "en": "Rs. 25,000 / year",
            "ta": "ஆண்டுக்கு ரூ. 25,000",
            "hi": "25,000 रुपये प्रति वर्ष"
        },
        "documents": {
            "en": "Single Window Counselling Allotment, Income Certificate, No Arrear Proof",
            "ta": "கலந்தாய்வு சேர்க்கை ஆணை, வருமானச் சான்றிதழ், அரியர் இல்லா சான்று",
            "hi": "काउंसलिंग आवंटन पत्र, आय प्रमाण पत्र, कोई बैकलॉग न होने का प्रमाण"
        },
        "where": {
            "en": "Anna University Student Affairs Office / Dean CEG",
            "ta": "அண்ணா பல்கலைக்கழக மாணவர் நல அலுவலகம்",
            "hi": "अन्ना विश्वविद्यालय छात्र कल्याण कार्यालय"
        }
    }
]

@app.route("/")
def index():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/match-scholarship", methods=["POST"])
def match_scholarship():
    try:
        data = request.get_json(force=True) or {}
        try:
            marks = float(data.get("marks", 0))
        except (ValueError, TypeError):
            marks = 0.0

        try:
            income = float(data.get("income", 0))
        except (ValueError, TypeError):
            income = 0.0

        caste = data.get("caste", "OBC / BC / MBC")
        lang = data.get("lang", "en")
        if lang not in ["en", "ta", "hi"]:
            lang = "en"

        matched = []
        for s in SCHOLARSHIPS_DB:
            # Check income condition
            income_ok = income <= s["max_income"]
            # Check marks condition
            marks_ok = marks >= s["min_marks"]
            # Check caste condition
            caste_ok = (caste in s["caste_allowed"]) or ("General / OC" in s["caste_allowed"])

            if income_ok and marks_ok and caste_ok:
                matched.append(s)

        # Fallback to general open schemes if none strictly match criteria
        if not matched:
            matched = [s for s in SCHOLARSHIPS_DB if s["id"] in [7, 9, 14]]

        headers = {
            "en": ["Scholarship / Scheme Name", "Donor / Sector", "Value / Benefit", "Mandatory Documents", "Where to Apply"],
            "ta": ["உதவித்தொகை / திட்டத்தின் பெயர்", "வழங்கும் அமைப்பு", "உதவித் தொகை", "தேவையான ஆவணங்கள்", "விண்ணப்பிக்கும் இடம்"],
            "hi": ["छात्रवृत्ति / योजना का नाम", "प्रदाता / क्षेत्र", "छात्रवृत्ति राशि", "आवश्यक दस्तावेज", "आवेदन कहाँ करें"]
        }

        th_cols = "".join([f"<th>{col}</th>" for col in headers[lang]])

        tr_rows = ""
        for s in matched:
            name = s["name"][lang]
            stype = s["type"][lang]
            val = s["value"][lang]
            docs = s["documents"][lang]
            where = s["where"][lang]

            tr_rows += f"""
            <tr>
                <td><strong>{name}</strong></td>
                <td><span class="badge">{stype}</span></td>
                <td>{val}</td>
                <td>{docs}</td>
                <td>{where}</td>
            </tr>
            """

        table_html = f"""
        <table class="results-table">
            <thead>
                <tr>{th_cols}</tr>
            </thead>
            <tbody>
                {tr_rows}
            </tbody>
        </table>
        """

        return jsonify({"success": True, "result": table_html.strip(), "count": len(matched)})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    print("Server running at: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)