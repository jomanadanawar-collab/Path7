import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# 2. قاموس اللغات الشامل (بدون متغيرات الاسم)
TRANSLATIONS = {
    "ar": {
        "title": "📍 Path7 | المسار الذكي",
        "subtitle": "نظام التوافق اللحظي للسياحة الذكية",
        "welcome": "أهلاً بك في رحلتك",
        "weather_label": "الجو في الرياض",
        "weather_val": "ليل صافي 🌙" if current_hour > 18 or current_hour < 5 else "مشمس ☀️",
        "budget_label": "حدد نوع الميزانية",
        "eco": "اقتصادية", "lux": "فاخرة",
        "start_btn": "استكشف مسارك الآن 🚀",
        "day": "اليوم", "of": "من",
        "interests_q": "🌟 ما هي اهتماماتك المفضلة لليوم؟",
        "interests_list": ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"],
        "analyze": "تحليل الوجهات الأنسب 🔍",
        "transport_q": "🚕 كيف تفضل الوصول لوجهاتك؟",
        "metro": "🚇 مترو الرياض", "car": "🚗 سيارتي", "taxi": "🚕 تاكسي",
        "time_est": "⏱️ الوقت المقدر:",
        "rating_title": "⭐ تقييمك لمسار اليوم",
        "next_day": "اليوم التالي ⏩",
        "finish": "✨ رحلة سعيدة! ✨",
        "reset": "🔄 ضبط جديد",
        "lang_btn": "English 🌐",
        "dir": "rtl", "align": "right"
    },
    "en": {
        "title": "📍 Path7 | Smart Journey",
        "subtitle": "Real-time Smart Tourism System",
        "welcome": "Welcome to your journey",
        "weather_label": "Riyadh Weather",
        "weather_val": "Clear Night 🌙" if current_hour > 18 or current_hour < 5 else "Sunny ☀️",
        "budget_label": "Select Budget Type",
        "eco": "Economy", "lux": "Luxury",
        "start_btn": "Explore Your Path Now 🚀",
        "day": "Day", "of": "of",
        "interests_q": "🌟 What are your interests today?",
        "interests_list": ["History", "Entertainment", "Shopping", "Dining", "Nature"],
        "analyze": "Analyze Destinations 🔍",
        "transport_q": "🚕 How do you prefer to travel?",
        "metro": "🚇 Riyadh Metro", "car": "🚗 My Car", "taxi": "🚕 Taxi",
        "time_est": "⏱️ Estimated Time:",
        "rating_title": "⭐ Rate Today's Path",
        "next_day": "Next Day ⏩",
        "finish": "✨ Enjoy your trip! ✨",
        "reset": "🔄 Reset",
        "lang_btn": "العربية 🌐",
        "dir": "ltr", "align": "left"
    }
}

# 3. قاعدة البيانات ثنائية اللغة (لضمان احترافية الترجمة)
PLACES_DB = {
    "ar": {
        "اقتصادية": [
            {"الوجهة": "حصن المصمك", "الفئة": "تاريخ وآثار", "وصف": "رمز توحيد المملكة.", "base_time": 28, "metro": True},
            {"الوجهة": "وادي حنيفة", "الفئة": "طبيعة", "وصف": "مساحات خضراء خلابة.", "base_time": 35, "metro": False}
        ],
        "فاخرة": [
            {"الوجهة": "فيا رياض", "الفئة": "ترفيه", "وصف": "مطاعم وسينما عالمية.", "base_time": 15, "metro": False},
            {"الوجهة": "مطل البجيري", "الفئة": "مطاعم ومقاهي", "وصف": "إطلالة تاريخية فاخرة.", "base_time": 18, "metro": True}
        ]
    },
    "en": {
        "Economy": [
            {"الوجهة": "Masmak Fortress", "الفئة": "History", "وصف": "Symbol of Saudi unification.", "base_time": 28, "metro": True},
            {"الوجهة": "Hanifa Valley", "الفئة": "Nature", "وصف": "Beautiful green landscapes.", "base_time": 35, "metro": False}
        ],
        "Luxury": [
            {"الوجهة": "Via Riyadh", "الفئة": "Entertainment", "وصف": "Luxury dining and cinema.", "base_time": 15, "metro": False},
            {"الوجهة": "Bujairi Terrace", "الفئة": "Dining", "وصف": "Premium historic views.", "base_time": 18, "metro": True}
        ]
    }
}

# 4. إدارة الحالة
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []

T = TRANSLATIONS[st.session_state.lang]

# 5. التنسيق
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {T["dir"]}; text-align: {T["align"]}; }}
    .main-card {{ background: white; padding: 20px; border-radius: 20px; border-top: 10px solid #0284C7; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
    .info-box {{ background: #F8FAFC; padding: 15px; border-radius: 15px; border-{T["align"]}: 8px solid #38BDF8; margin-bottom: 10px; border: 1px solid #E2E8F0; }}
    </style>
''', unsafe_allow_html=True)

# زر اللغة
if st.button(T["lang_btn"]):
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
    st.rerun()

# --- الصفحة الأولى ---
if st.session_state.page == 'welcome':
    with st.form("welcome"):
        st.title(T["title"])
        st.write(T["subtitle"])
        u_budget = st.radio(T["budget_label"], [T["eco"], T["lux"]], horizontal=True)
        if st.form_submit_button(T["start_btn"]):
            st.session_state.user_budget = u_budget
            st.session_state.page = 'system'
            st.rerun()

# --- الصفحة الثانية ---
else:
    st.markdown(f'''<div class="main-card">
        <h3>📅 {T["day"]} {st.session_state.current_day} {T["of"]} 3</h3>
        <p>{T["welcome"]} | {T["weather_label"]}: <b>{T["weather_val"]}</b></p>
    </div>''', unsafe_allow_html=True)
    
    st.markdown(f"<br><h4>{T['interests_q']}</h4>", unsafe_allow_html=True)
    u_interests = st.multiselect("", T["interests_list"], label_visibility="collapsed")

    if st.button(T["analyze"]):
        db = PLACES_DB[st.session_state.lang][st.session_state.user_budget]
        st.session_state.suggestions = [random.choice(db)] # مثال للتبسيط
    
    for p in st.session_state.suggestions:
        st.markdown(f'''<div class="info-box">
            <h4>📍 {p["الوجهة"]}</h4>
            <p>{p["وصف"]}</p>
            <b>{T["time_est"]} {p["base_time"]} min</b>
        </div>''', unsafe_allow_html=True)

    if st.button(T["reset"]):
        st.session_state.clear()
        st.rerun()
