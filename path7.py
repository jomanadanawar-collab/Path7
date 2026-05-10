import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# 2. القاموس الموحد (عربي/إنجليزي) - الترجمة الاحترافية للجنة
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
        "trans_label": "🚕 وسيلة المواصلات (لتحديث الوقت لحظياً):",
        "m_car": "🚗 سيارة", "m_taxi": "🚕 تاكسي", "m_metro": "🚇 مترو",
        "time_est": "⏱️ الوقت المقدر:",
        "compat": "🔄 التوافق اللحظي:",
        "rating": "⭐ تقييمك لمسار اليوم:",
        "reset": "🔄 إعادة ضبط",
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
        "trans_label": "🚕 Transport (Real-time time update):",
        "m_car": "🚗 Car", "m_taxi": "Taxi", "m_metro": "Metro",
        "time_est": "⏱️ Est. Travel Time:",
        "compat": "🔄 Compatibility:",
        "rating": "⭐ Rate Today's Path:",
        "reset": "🔄 Reset",
        "lang_btn": "العربية 🌐",
        "dir": "ltr", "align": "left"
    }
}

# 3. قاعدة البيانات - الربط بمفاتيح ثابتة لمنع KeyError
DB = {
    "Economy": {
        "ar": [
            {"name": "حصن المصمك", "cat": "تاريخ وآثار", "desc": "رمز توحيد المملكة.", "time": 25, "compat": "95%"},
            {"name": "وادي حنيفة", "cat": "طبيعة", "desc": "مساحات خضراء خلابة.", "time": 40, "compat": "88%"}
        ],
        "en": [
            {"name": "Masmak Fortress", "cat": "History", "desc": "Symbol of unification.", "time": 25, "compat": "95%"},
            {"name": "Hanifa Valley", "cat": "Nature", "desc": "Beautiful landscapes.", "time": 40, "compat": "88%"}
        ]
    },
    "Luxury": {
        "ar": [
            {"name": "فيا رياض", "cat": "ترفيه", "desc": "مطاعم وسينما فاخرة.", "time": 15, "compat": "98%"},
            {"name": "مطل البجيري", "cat": "مطاعم ومقاهي", "desc": "إطلالة تاريخية فاخرة.", "time": 20, "compat": "92%"}
        ],
        "en": [
            {"name": "Via Riyadh", "cat": "Entertainment", "desc": "Luxury dining & cinema.", "time": 15, "compat": "98%"},
            {"name": "Bujairi Terrace", "cat": "Dining", "desc": "Premium historic views.", "time": 20, "compat": "92%"}
        ]
    }
}

# 4. الحالة (Session State) - تهيئة آمنة
for key, val in [('lang','ar'), ('page','welcome'), ('u_name',''), ('u_budget','Economy'), ('suggestions',[])]:
    if key not in st.session_state: st.session_state[key] = val

T = TRANSLATIONS[st.session_state.lang]

# 5. التنسيق والخط (IBM Plex Sans Arabic)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button {{
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: {T["dir"]}; text-align: {T["align"]};
    }}
    .main-card {{ background: white; padding: 25px; border-radius: 25px; border-top: 12px solid #0284C7; box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin-bottom: 20px; }}
    .info-box {{ background: #F8FAFC; padding: 20px; border-radius: 20px; border-{T["align"]}: 8px solid #38BDF8; margin-bottom: 15px; }}
    .stButton>button {{ background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important; color: white !important; border-radius: 12px !important; border: none; font-weight: bold; height: 3.5em; }}
    </style>
''', unsafe_allow_html=True)

# زر اللغة
col_l1, col_l2 = st.columns([0.85, 0.15])
if col_l2.button(T["lang_btn"]):
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
    st.rerun()

# --- الصفحة الأولى (Welcome) ---
if st.session_state.page == 'welcome':
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("main_form"):
        st.markdown(f"<h1 style='text-align:center; color:#0369A1;'>{T['title']}</h1>", unsafe_allow_html=True)
        name_in = st.text_input(T["name_label"], value=st.session_state.u_name)
        budget_in = st.radio(T["budget_label"], [T["eco"], T["lux"]], horizontal=True)
        if st.form_submit_button(T["start_btn"]):
            st.session_state.u_name = name_in if name_in else "Guest"
            st.session_state.u_budget = "Economy" if budget_in in [T["eco"], "اقتصادية"] else "Luxury"
            st.session_state.page = 'system'
            st.rerun()

# --- الصفحة الثانية (System) ---
else:
    col_main, col_side = st.columns([2, 1])
    with col_main:
        st.markdown(f'''<div class="main-card">
            <h3>📅 {T["day"]} 1 {T["of"]} 3 | {T["welcome"]} {st.session_state.u_name}</h3>
            <p>{T["weather_label"]}: <b>{T["weather_val"]}</b></p>
        </div>''', unsafe_allow_html=True)

        # التوافق اللحظي: المواصلات
        st.write(T["trans_label"])
        transport = st.radio("", [T["m_car"], T["m_taxi"], T["m_metro"]], horizontal=True, label_visibility="collapsed")
        # منطق تحديث الوقت لحظياً
        time_factor = 1.4 if transport == T["m_metro"] else 1.0

        st.markdown(f"<h4>{T['interests_q']}</h4>", unsafe_allow_html=True)
        cats = ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"] if st.session_state.lang == 'ar' else ["History", "Entertainment", "Shopping", "Dining", "Nature"]
        u_interests = st.multiselect("", cats, label_visibility="collapsed")

        if st.button(T["analyze"]):
            st.session_state.suggestions = DB[st.session_state.u_budget][st.session_state.lang]
            st.rerun()
        
        for p in st.session_state.suggestions:
            calc_time = int(p["time"] * time_factor)
            st.markdown(f'''<div class="info-box">
                <h4>📍 {p["name"]} <small>({p["cat"]})</small></h4>
                <p>{p["desc"]}</p>
                <div style="display: flex; justify-content: space-between; font-weight: bold; color: #0369A1;">
                    <span>{T["compat"]} {p["compat"]}</span>
                    <span>{T["time_est"]} {calc_time} min</span>
                </div>
            </div>''', unsafe_allow_html=True)

    with col_side:
        st.markdown(f"<h4>{T['rating']}</h4>", unsafe_allow_html=True)
        st.feedback("stars") # النجوم
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button(T["reset"]):
            st.session_state.clear()
            st.rerun()
