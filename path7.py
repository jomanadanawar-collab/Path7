import streamlit as st
import random
from datetime import datetime
import pytz

# 1. الإعدادات الأساسية والوقت
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

# 2. قاموس اللغات (The Translation Dictionary)
LANG = {
    "العربية": {
        "title": "📍 Path7 | مسار 7",
        "subtitle": "نظام التوافق اللحظي للسياحة الذكية",
        "welcome": "مرحباً بك في الرياض",
        "budget_label": "حدد ميزانية الرحلة",
        "start_btn": "استكشف مسارك الآن 🚀",
        "day": "اليوم",
        "of": "من",
        "weather": "الجو في الرياض",
        "sunny": "مشمس ☀️",
        "night": "ليل صافي 🌙",
        "interests_q": "ما هي اهتماماتك المفضلة لهذا اليوم؟",
        "analyze_btn": "تحليل الوجهات الأنسب 🔍",
        "transport_q": "كيف تفضل الوصول لوجهاتك؟",
        "metro": "🚇 مترو الرياض",
        "car": "🚗 سيارة",
        "taxi": "🚕 تاكسي",
        "metro_fail": "المترو غير متاح لهذه الوجهات ❌",
        "est_time": "الوقت المقدر",
        "rating_q": "⭐ تقييمك لليوم",
        "next_day": "التوجه نحو مسار اليوم التالي ⏩",
        "finish": "✨ نتمنى لك ذكريات لا تُنسى في الرياض! ✨",
        "reset": "🔄 ضبط جديد",
        "eco": "اقتصادية", "lux": "فاخرة"
    },
    "English": {
        "title": "📍 Path7 | Smart Journey",
        "subtitle": "Real-time Compatibility System for Smart Tourism",
        "welcome": "Welcome to Riyadh",
        "budget_label": "Select Trip Budget",
        "start_btn": "Explore Your Path Now 🚀",
        "day": "Day",
        "of": "of",
        "weather": "Weather in Riyadh",
        "sunny": "Sunny ☀️",
        "night": "Clear Night 🌙",
        "interests_q": "What are your interests for today?",
        "analyze_btn": "Analyze Best Destinations 🔍",
        "transport_q": "How would you like to travel?",
        "metro": "🚇 Riyadh Metro",
        "car": "🚗 My Car",
        "taxi": "🚕 Taxi",
        "metro_fail": "Metro is not available for these locations ❌",
        "est_time": "Estimated Time",
        "rating_q": "⭐ Rate Your Day",
        "next_day": "Move to Next Day ⏩",
        "finish": "✨ We wish you unforgettable memories in Riyadh! ✨",
        "reset": "🔄 Reset System",
        "eco": "Economy", "lux": "Luxury"
    }
}

# 3. إعداد الصفحة والستايل (CSS)
st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# 4. إدارة الحالة (Session State)
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'star_rating' not in st.session_state: st.session_state.star_rating = 0
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

T = LANG[st.session_state.lang] # اختصار للقاموس المختار

st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if st.session_state.lang == "العربية" else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%); }}
    .main-card {{ background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); padding: 30px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 15px 35px rgba(0,0,0,0.05); margin-bottom: 20px; }}
    .info-box {{ background: white; padding: 20px; border-radius: 20px; border-{"right" if st.session_state.lang == "العربية" else "left"}: 10px solid #0EA5E9; margin-bottom: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.02); }}
    .stButton>button {{ background: linear-gradient(90deg, #0284C7, #38BDF8) !important; color: white !important; border: none !important; border-radius: 12px !important; font-weight: bold !important; transition: 0.3s !important; width: 100%; }}
    .stButton>button:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px rgba(2, 132, 199, 0.3); }}
    [data-testid="stSidebar"] {{ display: none !important; }}
    </style>
''', unsafe_allow_html=True)

# زر تبديل اللغة في الزاوية
col_l1, col_l2 = st.columns([8, 1])
with col_l2:
    if st.button("EN/عربي"):
        st.session_state.lang = "English" if st.session_state.lang == "العربية" else "العربية"
        st.rerun()

# --- البيانات ---
PLACES_DB = {
    "اقتصادية": [
        {"الوجهة": "حصن المصمك", "وصف": "رمز لتوحيد المملكة.", "base_time": 25, "metro": True},
        {"الوجهة": "وادي حنيفة", "وصف": "طبيعة خلابة ومساحات خضراء.", "base_time": 35, "metro": False}
    ],
    "فاخرة": [
        {"الوجهة": "فيا رياض", "وصف": "فخامة معمارية ومطاعم عالمية.", "base_time": 15, "metro": False},
        {"الوجهة": "حي الطريف", "وصف": "تاريخ نجد العريق.", "base_time": 20, "metro": True}
    ]
}

# --- الصفحة الأولى: الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown(f'<div class="main-card" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown(f'<h1 style="color: #0369A1;">{T["title"]}</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: #64748B;">{T["subtitle"]}</p>', unsafe_allow_html=True)
        u_budget = st.radio(T["budget_label"], [T["eco"], T["lux"]], horizontal=True)
        if st.button(T["start_btn"]):
            st.session_state.user_budget = "اقتصادية" if u_budget in [T["eco"], "اقتصادية"] else "فاخرة"
            st.session_state.page = 'system'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الثانية: لوحة التحكم ---
else:
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.markdown(f'''<div class="main-card">
            <h3 style="margin:0; color:#0369A1;">📅 {T["day"]} {st.session_state.current_day} {T["of"]} 3</h3>
            <p>{T["weather"]}: <b>{T["sunny"] if 5 <= current_hour <= 17 else T["night"]}</b></p>
        </div>''', unsafe_allow_html=True)

        st.subheader(T["interests_q"])
        interests = st.multiselect("", ["تاريخ وآثار", "طبيعة", "ترفيه", "تسوق"], label_visibility="collapsed")
        
        if st.button(T["analyze_btn"]):
            st.session_state.suggestions = PLACES_DB[st.session_state.user_budget]
            st.session_state.transport_choice = None

        if st.session_state.suggestions:
            st.markdown(f"### {T['transport_q']}")
            no_metro = any(not p['metro'] for p in st.session_state.suggestions)
            t_cols = st.columns(3)
            if not no_metro:
                if t_cols[0].button(T["metro"]): st.session_state.transport_choice = "metro"
            else:
                t_cols[0].markdown(f'<p style="color:gray; font-size:0.8em;">{T["metro_fail"]}</p>', unsafe_allow_html=True)
            
            if t_cols[1].button(T["car"]): st.session_state.transport_choice = "car"
            if t_cols[2].button(T["taxi"]): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                st.markdown(f'''<div class="info-box">
                    <h4>📍 {p["الوجهة"]}</h4>
                    <p style="color:#64748B;">{p["وصف"]}</p>
                    <p style="font-weight:bold; color:#0EA5E9;">⏱️ {T["est_time"]}: {p["base_time"]} min</p>
                </div>''', unsafe_allow_html=True)

    with col_side:
        st.markdown(f'<div class="main-card"><h4>{T["rating_q"]}</h4>', unsafe_allow_html=True)
        rating = st.select_slider("", options=[1, 2, 3, 4, 5], key="r_slider")
        if rating > 0:
            st.session_state.star_rating = rating
            if st.session_state.current_day < 3:
                if st.button(T["next_day"]):
                    st.session_state.current_day += 1
                    st.session_state.suggestions = []
                    st.session_state.star_rating = 0
                    st.rerun()
            else:
                st.success(T["finish"])
        
        if st.button(T["reset"]): st.session_state.clear(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #94A3B8;'>Path7 | Engineering Excellence @ IAU</p>", unsafe_allow_html=True)
