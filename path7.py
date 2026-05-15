import streamlit as st
import json
from datetime import datetime
import pytz
import os

# 1. تحميل البيانات من ملف الـ JSON
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading JSON file: {e}")
        return {}

DATA_ALL = load_data()

# 2. التوافق اللحظي والوقت (توقيت الرياض)
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
hour = now_riyadh.hour

# 3. إدارة الحالة والصفحات (تعريف مبكر لمنع خطأ NameError)
if 'lang' not in st.session_state: st.session_state.lang = None
if 'page' not in st.session_state: st.session_state.page = 'lang_selection'
if 'day' not in st.session_state: st.session_state.day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'rated' not in st.session_state: st.session_state.rated = False

# --- بوابة اختيار اللغة الأولى ---
if st.session_state.page == 'lang_selection':
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); }
        
        /* كرت العنوان مع مسافة سفلية تمنع الالتصاق نهائياً */
        .lang-card { 
            background: rgba(255, 255, 255, 0.8); 
            backdrop-filter: blur(10px); 
            padding: 40px; 
            border-radius: 30px; 
            text-align: center; 
            margin-top: 50px; 
            margin-bottom: 45px !important; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.1); 
        }
        
        /* أنيميشن ناعم وسلس لأزرار اللغتين */
        div[data-testid="stHorizontalBlock"] .stButton > button {
            background: white !important;
            color: #0284C7 !important;
            border: 2px solid rgba(2, 132, 199, 0.15) !important;
            border-radius: 15px !important;
            padding: 12px 24px !important;
            font-size: 16px !important;
            font-weight: bold !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        
        div[data-testid="stHorizontalBlock"] .stButton > button:hover {
            transform: translateY(-5px) scale(1.02) !important;
            background: linear-gradient(90deg, #0284C7, #38BDF8) !important;
            color: white !important;
            box-shadow: 0 10px 22px rgba(2, 132, 199, 0.3) !important;
            border-color: transparent !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="lang-card"><h1>Path7 📍</h1><h3>Select Your Language / اختر اللغة</h3></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("English 🇬🇧", use_container_width=True):
            st.session_state.lang = "English"
            st.session_state.page = 'welcome'
            st.rerun()
    with col2:
        if st.button("العربية 🇸🇦", use_container_width=True):
            st.session_state.lang = "العربية"
            st.session_state.page = 'welcome'
            st.rerun()
    st.stop()

# جلب بيانات اللغة المحددة ديناميكياً من الـ JSON لربط النصوص والاهتمامات والوجهات كاملة باللغة المختارة
lang_data = DATA_ALL.get(st.session_state.lang, DATA_ALL.get("العربية", {}))
IS_AR = st.session_state.lang == "العربية"

strings = {
    "title": lang_data.get("p_name", "Path7 📍"),
    "sub": lang_data.get("subtitle", ""),
    "name_q": lang_data.get("visitor_name", "Welcome, what is your name?"),
    "budget_q": lang_data.get("budget_q", "Choose your trip style:"),
    "budgets": [lang_data.get("eco", "Economy"), lang_data.get("lux", "Luxury")],
    "start_btn": lang_data.get("start_btn", "Explore Riyadh 🚀"),
    "day_lbl": f"📅 {lang_data.get('day', 'Day')} {st.session_state.day} {lang_data.get('of', 'of')} 3",
    "weather": (lang_data.get("sunny", "Sunny ☀️") if 5 <= hour <= 17 else lang_data.get("night", "Clear 🌙")),
    "interests_q": lang_data.get("interests_q", "What are your interests today?"),
    "interests_list": lang_data.get("interests_list", []),
    "analyze_btn": lang_data.get("analyze_btn", "Smart Path Analysis 🔍"),
    "trans_q": lang_data.get("transport_q", "Preferred Transport"),
    "metro": lang_data.get("m_btn", "🚇 Metro"),
    "car": lang_data.get("c_btn", "🚗 Car"),
    "taxi": lang_data.get("t_btn", "🚕 Taxi"),
    "est_time": lang_data.get("est_time", "Est. Time"),
    "mins": lang_data.get("min", "mins"),
    "map_btn": lang_data.get("map_btn", "📍 Open Maps"),
    "metro_msg": lang_data.get("metro_msg", "Metro station is nearby."),
    "metro_fail": lang_data.get("metro_fail", "No direct metro line to this destination."),
    "select_trans": lang_data.get("wait_choice", "⏳ Select transport to see path"),
    "rating_t": lang_data.get("rating_q", "Rate your experience ⭐"),
    "next_day": lang_data.get("next_day", "Next Day ⏭️"),
    "reset": "إعادة ضبط 🔄" if IS_AR else "Reset 🔄",
    "final_msg": lang_data.get("finish", "Thank you for trusting Path7.. Have a great trip! ✨")
}

# 4. التنسيق البصري العام للواجهة والأزرار والبطاقات المقاومة للاهتزاز
text_align = "right" if IS_AR else "left"
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&family=Inter:wght@400;700&display=swap');
    * {{ font-family: {"'IBM Plex Sans Arabic'" if IS_AR else "'Inter'"}, sans-serif !important; direction: {"rtl" if IS_AR else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); background-attachment: fixed; }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 25px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 15px 35px rgba(0,0,0,0.1); margin-bottom: 20px; text-align: {text_align}; }}
    .center-rating {{ text-align: center !important; }}
    .dest-card {{ background: white; padding: 20px; border-radius: 20px; border-{"right" if IS_AR else "left"}: 10px solid #0EA5E9; margin-bottom: 15px; text-align: {text_align}; }}
    .map-btn {{ background-color: #0284C7; color: white !important; padding: 8px 16px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 10px; }}
    
    /* تصميم الأزرار العامة */
    .stButton>button {{ background: linear-gradient(90deg, #0284C7, #38BDF8) !important; color: white !important; border-radius: 10px !important; width: 100%; }}
    
    /* أزرار الأرقام للتقييم (تصميم مربّع متناسق بدون نجوم مكررة) */
    .center-rating .stButton>button {{
        width: 45px !important;
        height: 45px !important;
        padding: 0px !important;
        line-height: 45px !important;
        border-radius: 10px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 auto !important;
    }}
    </style>
''', unsafe_allow_html=True)

# زر الشريط الجانبي لتغيير اللغة في أي وقت كخيار طوارئ للمحكّم
if st.sidebar.button("Switch Language / تغيير اللغة"):
    st.session_state.lang = "English" if IS_AR else "العربية"
    st.rerun()

# --- الصفحات ---
# أ. صفحة الترحيب وتأكيد تذكرة الطيران والثبات الرقمي
if st.session_state.page == 'welcome':
    st.markdown(f'<div class="glass-card" style="text-align: center;"><h1>{strings["title"]}</h1><p>{strings["sub"]}</p></div>', unsafe_allow_html=True)
    col_w1, col_w2, col_w3 = st.columns([1, 2, 1])
    
    with col_w2:
        # التذكرة الثابتة كلياً والمحاكية لبيانات طيران حقيقية قادمة للرياض
        st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.85); padding: 18px; border-radius: 15px; border-left: 6px solid #1E3A8A; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 22px; text-align: center;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-weight: bold; color: #1E3A8A; font-size: 0.95em;">✈️ الخطوط السعودية / SAUDIA</span>
                    <span style="background: #E0F2FE; color: #0369A1; padding: 2px 10px; border-radius: 20px; font-size: 0.8em; font-weight: bold;">Tourist / سياحة</span>
                </div>
                <div style="margin: 12px 0;">
                    <span style="color: #64748B; font-size: 0.85em; display: block; margin-bottom: 2px;">رقم الحجز المربوط / Linked PNR</span>
                    <strong style="font-size: 1.3em; color: #0284C7; letter-spacing: 2px; font-family: 'Inter', sans-serif;">SV-RUH2026X</strong>
                </div>
                <div style="border-top: 1px dashed #CBD5E1; margin-top: 10px; padding-top: 8px; font-size: 0.8em; color: #64748B;">
                    📍 Destination: Riyadh (RUH) | الوجهة: الرياض
                </div>
            </div>
        """, unsafe_allow_html=True
