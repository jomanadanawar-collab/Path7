import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

# 2. قاموس اللغات (Dictionary)
TRANSLATIONS = {
    "ar": {
        "title": "📍 Path7 | المسار الذكي",
        "subtitle": "نظام التوافق اللحظي للسياحة الذكية",
        "welcome": "مرحباً بك",
        "budget": "الميزانية",
        "interests": "الاهتمامات",
        "analyze": "تحليل الوجهات الأنسب 🔍",
        "transport_q": "🚕 كيف تفضل الوصول لوجهاتك اليوم؟",
        "metro": "🚇 مترو الرياض",
        "car": "🚗 سيارتي",
        "taxi": "🚕 تاكسي",
        "time_est": "⏱️ الوقت المقدر:",
        "next_day": "التوجه نحو مسار اليوم التالي ⏩",
        "finish": "✨ نتمنى لك رحلة سعيدة في الرياض! ✨",
        "lang_btn": "English 🌐",
        "start_btn": "استكشف مسارك الآن 🚀",
        "day": "اليوم",
        "of": "من",
        "interests_q": "🌟 ما هي اهتماماتك المفضلة لليوم؟",
        "eco": "اقتصادية",
        "lux": "فاخرة",
        "dir": "rtl",
        "align": "right"
    },
    "en": {
        "title": "📍 Path7 | Smart Journey",
        "subtitle": "Real-time Smart Tourism Compatibility System",
        "welcome": "Welcome",
        "budget": "Budget",
        "interests": "Interests",
        "analyze": "Analyze Best Destinations 🔍",
        "transport_q": "🚕 How do you prefer to get there?",
        "metro": "🚇 Riyadh Metro",
        "car": "🚗 My Car",
        "taxi": "🚕 Taxi",
        "time_est": "⏱️ Estimated Time:",
        "next_day": "Move to Next Day ⏩",
        "finish": "✨ We wish you a happy journey in Riyadh! ✨",
        "lang_btn": "العربية 🌐",
        "start_btn": "Explore Your Path Now 🚀",
        "day": "Day",
        "of": "of",
        "interests_q": "🌟 What are your interests for today?",
        "eco": "Economy",
        "lux": "Luxury",
        "dir": "ltr",
        "align": "left"
    }
}

# 3. إدارة الحالة (Session State)
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

T = TRANSLATIONS[st.session_state.lang]

st.set_page_config(page_title=T["title"], layout="wide")

# 4. التنسيق الجمالي (CSS) - يدعم اللغتين
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&family=Inter:wght@400;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'IBM Plex Sans Arabic', 'Inter', sans-serif !important;
        direction: {T["dir"]}; text-align: {T["align"]};
    }}

    .stApp {{ background-color: #F0F9FF !important; }}
    .highlight-box {{
        background-color: #E0F2FE; padding: 20px; border-radius: 18px;
        border-{"right" if st.session_state.lang == 'ar' else "left"}: 10px solid #0EA5E9;
        margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}
    .main-card {{ 
        background: white; padding: 25px; border-radius: 25px; 
        border-top: 12px solid #0284C7; box-shadow: 0 10px 30px rgba(0,0,0,0.08); 
    }}
    .info-box {{ 
        background: white; padding: 20px; border-radius: 20px; 
        border: 1px solid #BAE6FD; border-{"right" if st.session_state.lang == 'ar' else "left"}: 8px solid #38BDF8; 
        margin-bottom: 15px; 
    }}
    .stButton>button {{
        background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important;
        color: white !important; border-radius: 15px !important; font-weight: bold !important;
    }}
    </style>
''', unsafe_allow_html=True)

# زر تبديل اللغة في الأعلى
col_l1, col_l2 = st.columns([0.9, 0.1])
if col_l2.button(T["lang_btn"]):
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
    st.rerun()

# البيانات (PLACES_DB) - مبسطة للمثال
PLACES_DB = {
    "اقتصادية": [{"الوجهة": "حصن المصمك", "الفئة": "تاريخ وآثار", "base_time": 28, "metro_access": True}],
    "Economy": [{"الوجهة": "Masmak Fortress", "الفئة": "History", "base_time": 28, "metro_access": True}],
    "فاخرة": [{"الوجهة": "بوليفارد سيتي", "الفئة": "ترفيه", "base_time": 12, "metro_access": False}],
    "Luxury": [{"الوجهة": "Boulevard City", "الفئة": "Entertainment", "base_time": 12, "metro_access": False}]
}

# --- الصفحة الأولى: الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("welcome_form"):
        st.markdown(f'<h1 style="text-align: center; color: #0369A1;">{T["title"]}</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; color: #64748B;">{T["subtitle"]}</p>', unsafe_allow_html=True)
        
        u_name = st.text_input("Name" if st.session_state.lang == 'en' else "الاسم", "Jumanah")
        u_budget = st.radio(T["budget"], [T["eco"], T["lux"]], horizontal=True)
        
        if st.form_submit_button(T["start_btn"]):
            st.session_state.user_name = u_name
            st.session_state.user_budget = u_budget
            st.session_state.page = 'system'
            st.rerun()

# --- الصفحة الثانية: لوحة التحكم ---
else:
    st.markdown(f'''
        <div class="main-card">
            <h3>📅 {T["day"]} {st.session_state.current_day} {T["of"]} 3</h3>
            <p>{T["welcome"]} <b>{st.session_state.user_name}</b></p>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown(f'<div class="highlight-box"><h4>{T["interests_q"]}</h4></div>', unsafe_allow_html=True)
    
    # هنا تضعين الـ multiselect والتحليل كما في الكود السابق مع استخدام T["analyze"] للأزرار

    if st.button(T["analyze"]):
        st.success("Analyzing..." if st.session_state.lang == 'en' else "جاري التحليل...")
        # (بقية منطق البحث عن الأماكن)

    if st.button("🔄 Reset" if st.session_state.lang == 'en' else "🔄 إعادة ضبط"):
        st.session_state.clear()
        st.rerun()
