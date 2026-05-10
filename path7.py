import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة (نفس إعدادات النسخة اللي أبهرتكِ)
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)

# 2. قاموس اللغات (Dictionary) مع إضافة حقول النقص
TRANSLATIONS = {
    "ar": {
        "title": "📍 Path7 | المسار الذكي",
        "subtitle": "نظام التوافق اللحظي للسياحة الذكية",
        "welcome": "مرحباً بك",
        "budget": "الميزانية",
        "interests": "الاهتمامات",
        "analyze": "تحليل الوجهات الأنسب 🔍",
        "transport_q": "🚕 كيف تفضل الوصول لوجهاتك اليوم؟",
        "metro": "🚇 مترو الرياض", "car": "🚗 سيارتي", "taxi": "🚕 تاكسي",
        "time_est": "⏱️ الوقت المقدر:",
        "start_btn": "استكشف مسارك الآن 🚀",
        "day": "اليوم", "of": "من",
        "interests_q": "🌟 ما هي اهتماماتك المفضلة لليوم؟",
        "eco": "اقتصادية", "lux": "فاخرة",
        "dir": "rtl", "align": "right", "lang_btn": "English 🌐"
    },
    "en": {
        "title": "📍 Path7 | Smart Journey",
        "subtitle": "Real-time Smart Tourism Compatibility System",
        "welcome": "Welcome",
        "budget": "Budget",
        "interests": "Interests",
        "analyze": "Analyze Best Destinations 🔍",
        "transport_q": "🚕 How do you prefer to get there?",
        "metro": "🚇 Riyadh Metro", "car": "🚗 My Car", "taxi": "🚕 Taxi",
        "time_est": "⏱️ Estimated Time:",
        "start_btn": "Explore Your Path Now 🚀",
        "day": "Day", "of": "of",
        "interests_q": "🌟 What are your interests for today?",
        "eco": "Economy", "lux": "Luxury",
        "dir": "ltr", "align": "left", "lang_btn": "العربية 🌐"
    }
}

# 3. إدارة الحالة (لحماية الكود من الانهيار)
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

T = TRANSLATIONS[st.session_state.lang]
st.set_page_config(page_title=T["title"], layout="wide")

# 4. التنسيق الجمالي (نسخة الكربون من تصميمك المفضل)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"], p, label, button, input {{
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
        color: white !important; border-radius: 15px !important; font-weight: bold !important; border: none !important;
    }}
    </style>
''', unsafe_allow_html=True)

# زر تبديل اللغة
col_l1, col_l2 = st.columns([0.9, 0.1])
if col_l2.button(T["lang_btn"]):
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
    st.rerun()

# 5. البيانات المحدثة (من ملف الميزانية الجديد)
PLACES_DB = {
    "اقتصادية": [
        {"الوجهة": "أسواق المعيقلية", "الفئة": "تسوق", "time": 25, "metro": True},
        {"الوجهة": "حصن المصمك", "الفئة": "تاريخ وآثار", "time": 28, "metro": True},
        {"الوجهة": "سوق الزل", "الفئة": "تسوق", "time": 27, "metro": True},
        {"الوجهة": "مركز الملك عبدالله المالي (KAFD)", "الفئة": "طبيعة", "time": 10, "metro": True},
        {"الوجهة": "وادي حنيفة / نمار", "الفئة": "طبيعة", "time": 35, "metro": False},
        {"الوجهة": "منتزه الملك عبد الله", "الفئة": "طبيعة", "time": 30, "metro": False},
        {"الوجهة": "حافة العالم", "الفئة": "طبيعة", "time": 90, "metro": False}
    ],
    "فاخرة": [
        {"الوجهة": "حي الطريف", "الفئة": "تاريخ وآثار", "time": 18, "metro": True},
        {"الوجهة": "فيا الرياض", "الفئة": "ترفيه", "time": 15, "metro": False},
        {"الوجهة": "بوليفارد ستي", "الفئة": "ترفيه", "time": 12, "metro": False},
        {"الوجهة": "مطل البجيري", "الفئة": "مطاعم ومقاهي", "time": 18, "metro": True}
    ]
}

# --- الصفحة الأولى: الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("welcome_form"):
        st.markdown(f'<h1 style="text-align: center; color: #0369A1;">{T["title"]}</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; color: #64748B;">{T["subtitle"]}</p>', unsafe_allow_html=True)
        u_name = st.text_input("Name" if st.session_state.lang == 'en' else "اسم السائح الموقر", value="") 
        u_budget = st.radio(T["budget"], [T["eco"], T["lux"]], horizontal=True)
        if st.form_submit_button(T["start_btn"]):
            st.session_state.user_name = u_name
            st.session_state.user_budget = "اقتصادية" if u_budget in ["Economy", "اقتصادية"] else "فاخرة"
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
    interest_list = ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"]
    u_interests = st.multiselect("", interest_list, label_visibility="collapsed")

    if st.button(T["analyze"]):
        # منطق التعدد: يعرض كل ما يطابق أي اهتمام مختار
        db = PLACES_DB["اقتصادية" if st.session_state.user_budget == "اقتصادية" else "فاخرة"]
        st.session_state.suggestions = [p for p in db if p['الفئة'] in u_interests]
        st.session_state.transport_choice = None

    if st.session_state.suggestions:
        st.markdown(f'<br><div class="highlight-box"><h4>{T["transport_q"]}</h4></div>', unsafe_allow_html=True)
        t1, t2, t3 = st.columns(3)
        if t1.button(T["metro"]): st.session_state.transport_choice = "metro"
        if t2.button(T["car"]): st.session_state.transport_choice = "car"
        if t3.button(T["taxi"]): st.session_state.transport_choice = "taxi"

        for p in st.session_state.suggestions:
            st.markdown(f'<div class="info-box"><h4>📍 {p["الوجهة"]}</h4><p>{p["الفئة"]}</p><p>{T["time_est"]} {p["time"]} min</p></div>', unsafe_allow_html=True)

    if st.button("🔄 Reset" if st.session_state.lang == 'en' else "🔄 إعادة ضبط"):
        st.session_state.clear()
        st.rerun()
