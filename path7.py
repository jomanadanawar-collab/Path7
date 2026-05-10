import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# 2. القاموس الذكي (لمنع تعارض اللغات)
TRANSLATIONS = {
    "ar": {
        "title": "📍 Path7 | المسار الذكي",
        "subtitle": "نظام التوافق اللحظي للسياحة الذكية",
        "name_label": "اسم السائح الموقر",
        "welcome": "مرحباً يا",
        "weather_label": "الجو في الرياض",
        "weather_val": "ليل صافي 🌙" if current_hour > 18 or current_hour < 5 else "مشمس ☀️",
        "budget_label": "حدد نوع الميزانية للرحلة",
        "eco": "اقتصادية", "lux": "فاخرة",
        "start_btn": "استكشف مسارك الآن 🚀",
        "day": "اليوم", "of": "من",
        "interests_q": "🌟 ما هي اهتماماتك المفضلة لليوم؟",
        "analyze": "تحليل الوجهات الأنسب 🔍",
        "transport_q": "🚕 كيف تفضل الوصول لوجهاتك؟",
        "metro": "🚇 مترو الرياض", "car": "🚗 سيارتي", "taxi": "🚕 تاكسي",
        "time_est": "⏱️ الوقت المقدر:",
        "rating_title": "⭐ تقييمك لمسار اليوم",
        "next_day": "اليوم التالي ⏩",
        "finish": "✨ شكراً لاستخدامك Path7.. رحلة سعيدة! ✨",
        "reset": "🔄 ضبط جديد",
        "lang_btn": "English 🌐",
        "dir": "rtl", "align": "right"
    },
    "en": {
        "title": "📍 Path7 | Smart Journey",
        "subtitle": "Real-time Smart Tourism Compatibility System",
        "name_label": "Tourist Name",
        "welcome": "Welcome",
        "weather_label": "Riyadh Weather",
        "weather_val": "Clear Night 🌙" if current_hour > 18 or current_hour < 5 else "Sunny ☀️",
        "budget_label": "Select Trip Budget",
        "eco": "Economy", "lux": "Luxury",
        "start_btn": "Explore Your Path Now 🚀",
        "day": "Day", "of": "of",
        "interests_q": "🌟 What are your interests today?",
        "analyze": "Analyze Destinations 🔍",
        "transport_q": "🚕 How do you prefer to travel?",
        "metro": "🚇 Riyadh Metro", "car": "🚗 My Car", "taxi": "🚕 Taxi",
        "time_est": "⏱️ Estimated Time:",
        "rating_title": "⭐ Rate Today's Path",
        "next_day": "Next Day ⏩",
        "finish": "✨ Thank you for using Path7.. Enjoy your stay! ✨",
        "reset": "🔄 Reset",
        "lang_btn": "العربية 🌐",
        "dir": "ltr", "align": "left"
    }
}

# 3. قاعدة البيانات (مترجمة وجاهزة للجنة التحكيم)
INTERESTS_MAP = {
    "ar": ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"],
    "en": ["History", "Entertainment", "Shopping", "Dining", "Nature"]
}

DB = {
    "Economy": {
        "ar": [
            {"name": "حصن المصمك", "cat": "تاريخ وآثار", "desc": "رمز لتوحيد المملكة.", "time": 28, "metro": True},
            {"name": "وادي حنيفة", "cat": "طبيعة", "desc": "مساحات خضراء وبحيرات.", "time": 35, "metro": False}
        ],
        "en": [
            {"name": "Masmak Fortress", "cat": "History", "desc": "Symbol of Saudi unification.", "time": 28, "metro": True},
            {"name": "Hanifa Valley", "cat": "Nature", "desc": "Stunning green landscapes.", "time": 35, "metro": False}
        ]
    },
    "Luxury": {
        "ar": [
            {"name": "فيا رياض", "cat": "ترفيه", "desc": "وجهة فاخرة وسينما عالمية.", "time": 15, "metro": False},
            {"name": "مطل البجيري", "cat": "مطاعم ومقاهي", "desc": "إطلالة تاريخية فاخرة.", "time": 18, "metro": True}
        ],
        "en": [
            {"name": "Via Riyadh", "cat": "Entertainment", "desc": "Luxury dining and world-class cinema.", "time": 15, "metro": False},
            {"name": "Bujairi Terrace", "cat": "Dining", "desc": "Premium historic views of At-Turaif.", "time": 18, "metro": True}
        ]
    }
}

# 4. إدارة الحالة
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'u_name' not in st.session_state: st.session_state.u_name = ""
if 'u_budget' not in st.session_state: st.session_state.u_budget = "Economy"
if 'suggestions' not in st.session_state: st.session_state.suggestions = []

T = TRANSLATIONS[st.session_state.lang]

# 5. التنسيق والخط العربي
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {{
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: {T["dir"]}; text-align: {T["align"]};
    }}
    .main-card {{ background: white; padding: 25px; border-radius: 25px; border-top: 12px solid #0284C7; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }}
    .info-box {{ background: white; padding: 20px; border-radius: 20px; border-{T["align"]}: 8px solid #38BDF8; margin-bottom: 15px; border: 1px solid #BAE6FD; }}
    .stButton>button {{ background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important; color: white !important; border-radius: 15px !important; font-weight: bold !important; height: 3.5em; border: none; }}
    </style>
''', unsafe_allow_html=True)

# زر اللغة
col_l1, col_l2 = st.columns([0.85, 0.15])
if col_l2.button(T["lang_btn"]):
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
    st.rerun()

# --- الصفحة الأولى ---
if st.session_state.page == 'welcome':
    with st.form("welcome_form"):
        st.markdown(f'<h1 style="text-align: center;">{T["title"]}</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center;">{T["subtitle"]}</p>', unsafe_allow_html=True)
        
        name_input = st.text_input(T["name_label"], value=st.session_state.u_name)
        budget_input = st.radio(T["budget_label"], [T["eco"], T["lux"]], horizontal=True)
        
        if st.form_submit_button(T["start_btn"]):
            st.session_state.u_name = name_input if name_input else "Guest"
            st.session_state.u_budget = "Economy" if budget_input in ["اقتصادية", "Economy"] else "Luxury"
            st.session_state.page = 'system'
            st.rerun()

# --- الصفحة الثانية ---
else:
    col_main, col_stats = st.columns([2, 1])
    with col_main:
        st.markdown(f'''<div class="main-card">
            <h3>📅 {T["day"]} 1 {T["of"]} 3</h3>
            <p>{T["welcome"]} <b>{st.session_state.u_name}</b> | {T["weather_label"]}: <b>{T["weather_val"]}</b></p>
        </div>''', unsafe_allow_html=True)
        
        u_interests = st.multiselect(T["interests_q"], INTERESTS_MAP[st.session_state.lang])

        if st.button(T["analyze"]):
            # سحب البيانات الصحيحة حسب الميزانية واللغة المختارة
            db_segment = DB[st.session_state.u_budget][st.session_state.lang]
            st.session_state.suggestions = db_segment # تبسيط للتحليل
            st.rerun()
        
        for p in st.session_state.suggestions:
            st.markdown(f'''<div class="info-box">
                <h4>📍 {p["name"]}</h4>
                <p>{p["desc"]}</p>
                <b>{T["time_est"]} {p["time"]} min</b>
            </div>''', unsafe_allow_html=True)

    with col_stats:
        if st.button(T["reset"]):
            st.session_state.clear()
            st.rerun()
