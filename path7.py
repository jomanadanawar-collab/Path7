import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# 2. قاموس اللغات الشامل (Dictionary)
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
        "name_label": "Tourist Name",
        "welcome": "Welcome",
        "weather_label": "Riyadh Weather",
        "weather_val": "Clear Night 🌙" if current_hour > 18 or current_hour < 5 else "Sunny ☀️",
        "budget_label": "Select Trip Budget",
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

# 3. قاعدة البيانات ثنائية اللغة
PLACES_DB = {
    "ar": {
        "اقتصادية": [
            {"الوجهة": "حصن المصمك", "الفئة": "تاريخ وآثار", "وصف": "رمز لتوحيد المملكة وتأسيسها.", "base_time": 28, "metro": True},
            {"الوجهة": "وادي حنيفة", "الفئة": "طبيعة", "وصف": "مساحات خضراء وبحيرات خلابة.", "base_time": 35, "metro": False}
        ],
        "فاخرة": [
            {"الوجهة": "فيا رياض", "الفئة": "ترفيه", "وصف": "وجهة فاخرة تضم مطاعم وسينما عالمية.", "base_time": 15, "metro": False},
            {"الوجهة": "مطل البجيري", "الفئة": "مطاعم ومقاهي", "وصف": "إطلالة تاريخية فاخرة على الطريف.", "base_time": 18, "metro": True}
        ]
    },
    "en": {
        "Economy": [
            {"الوجهة": "Masmak Fortress", "الفئة": "History", "وصف": "Symbol of Saudi unification.", "base_time": 28, "metro": True},
            {"الوجهة": "Hanifa Valley", "الفئة": "Nature", "وصف": "Stunning landscapes and lakes.", "base_time": 35, "metro": False}
        ],
        "Luxury": [
            {"الوجهة": "Via Riyadh", "الفئة": "Entertainment", "وصف": "Luxury dining and world-class cinema.", "base_time": 15, "metro": False},
            {"الوجهة": "Bujairi Terrace", "الفئة": "Dining", "وصف": "Premium historic views of At-Turaif.", "base_time": 18, "metro": True}
        ]
    }
}

# 4. إدارة الحالة
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'u_name' not in st.session_state: st.session_state.u_name = ""

T = TRANSLATIONS[st.session_state.lang]

# 5. التنسيق (استخدام الخط المعتمد)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"] {{
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: {T["dir"]}; text-align: {T["align"]};
    }}
    .main-card {{ background: white; padding: 25px; border-radius: 25px; border-top: 12px solid #0284C7; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }}
    .info-box {{ background: white; padding: 20px; border-radius: 20px; border-{T["align"]}: 8px solid #38BDF8; margin-bottom: 15px; border: 1px solid #BAE6FD; }}
    .stButton>button {{ background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important; color: white !important; border: none !important; border-radius: 15px !important; font-weight: bold !important; width: 100%; }}
    </style>
''', unsafe_allow_html=True)

# زر اللغة
col_l1, col_l2 = st.columns([0.85, 0.15])
if col_l2.button(T["lang_btn"]):
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
    st.rerun()

# --- الصفحة الأولى ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.form("welcome_form"):
        st.markdown(f'<h1 style="text-align: center; color: #0369A1;">{T["title"]}</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; color: #64748B;">{T["subtitle"]}</p>', unsafe_allow_html=True)
        
        # إدخال الاسم
        name_input = st.text_input(T["name_label"], value=st.session_state.u_name)
        
        u_budget = st.radio(T["budget_label"], [T["eco"], T["lux"]], horizontal=True)
        
        if st.form_submit_button(T["start_btn"]):
            st.session_state.u_name = name_input if name_input else "Guest"
            st.session_state.user_budget = "Economy" if u_budget in ["اقتصادية", "Economy"] else "Luxury"
            st.session_state.page = 'system'
            st.rerun()

# --- الصفحة الثانية ---
else:
    col_main, col_stats = st.columns([2, 1])
    with col_main:
        # عرض الاسم في الترحيب
        st.markdown(f'''<div class="main-card">
            <h3>📅 {T["day"]} {st.session_state.current_day} {T["of"]} 3</h3>
            <p>{T["welcome"]} <b>{st.session_state.u_name}</b> | {T["weather_label"]}: <b>{T["weather_val"]}</b></p>
        </div>''', unsafe_allow_html=True)
        
        st.markdown(f"<br><h4>{T['interests_q']}</h4>", unsafe_allow_html=True)
        u_interests = st.multiselect("", T["interests_list"], label_visibility="collapsed")

        if st.button(T["analyze"]):
            db = PLACES_DB[st.session_state.lang][st.session_state.user_budget]
            # منطق اختيار الوجهات (مثال)
            st.session_state.suggestions = [random.choice(db)]
            st.rerun()
        
        for p in st.session_state.suggestions:
            st.markdown(f'''<div class="info-box">
                <h4>📍 {p["الوجهة"]}</h4>
                <p>{p["وصف"]}</p>
                <b>{T["time_est"]} {p["base_time"]} min</b>
            </div>''', unsafe_allow_html=True)

    with col_stats:
        if st.button(T["reset"]):
            st.session_state.clear()
            st.rerun()
