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
        "analyze": "تحليل الوجهات الأنسب لهذا اليوم 🔍",
        "trans_label": "🚕 اختر وسيلة المواصلات (تحديث لحظي):",
        "m_car": "🚗 سيارتي", "m_taxi": "🚕 تاكسي", "m_metro": "🚇 مترو الرياض",
        "time_est": "⏱️ الوقت المقدر:",
        "compat": "🔄 التوافق اللحظي:",
        "rating_title": "⭐ تقييمك لليوم",
        "rating_btn": "نجوم",
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
        "start_btn": "Explore Now 🚀",
        "day": "Day", "of": "of",
        "interests_q": "🌟 What are your interests today?",
        "analyze": "Analyze Best Destinations 🔍",
        "trans_label": "🚕 Choose Transport (Real-time update):",
        "m_car": "🚗 Car", "m_taxi": "Taxi", "m_metro": "Metro",
        "time_est": "⏱️ Est. Travel Time:",
        "compat": "🔄 Compatibility:",
        "rating_title": "⭐ Rate Your Day",
        "rating_btn": "Stars",
        "reset": "🔄 Reset",
        "lang_btn": "العربية 🌐",
        "dir": "ltr", "align": "left"
    }
}

# 3. قاعدة البيانات - الربط بمفاتيح ثابتة وتحديد المترو
DB = {
    "Economy": {
        "ar": [
            {"name": "حصن المصمك", "cat": "تاريخ وآثار", "desc": "رمز لتوحيد المملكة وتأسيسها.", "time": 25, "compat": "95%", "metro_access": True},
            {"name": "وادي حنيفة", "cat": "طبيعة", "desc": "مساحات خضراء وبحيرات خلابة.", "time": 40, "compat": "88%", "metro_access": False}
        ],
        "en": [
            {"name": "Masmak Fortress", "cat": "History", "desc": "Symbol of unification.", "time": 25, "compat": "95%", "metro_access": True},
            {"name": "Hanifa Valley", "cat": "Nature", "desc": "Stunning landscapes and lakes.", "time": 40, "compat": "88%", "metro_access": False}
        ]
    },
    "Luxury": {
        "ar": [
            {"name": "فيا رياض", "cat": "ترفيه", "desc": "مطاعم وسينما فاخرة عالمية.", "time": 15, "compat": "98%", "metro_access": False},
            {"name": "مطل البجيري", "cat": "مطاعم ومقاهي", "desc": "إطلالة تاريخية فاخرة على الطريف.", "time": 20, "compat": "92%", "metro_access": True}
        ],
        "en": [
            {"name": "Via Riyadh", "cat": "Entertainment", "desc": "Luxury dining & world-class cinema.", "time": 15, "compat": "98%", "metro_access": False},
            {"name": "Bujairi Terrace", "cat": "Dining", "desc": "Premium historic views.", "time": 20, "compat": "92%", "metro_access": True}
        ]
    }
}

# 4. الحالة
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'u_name' not in st.session_state: st.session_state.u_name = "JOMAN" # قيمة افتراضية لتفادي KeyError
if 'u_budget' not in st.session_state: st.session_state.u_budget = "Economy"
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'trans_factor' not in st.session_state: st.session_state.trans_factor = 1.0

T = TRANSLATIONS[st.session_state.lang]

# 5. التنسيق الجمالي "البركات والحركات" (استخدام IBM Plex Sans Arabic)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {{
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: {T["dir"]}; text-align: {T["align"]};
    }}
    .stApp {{ background-color: #F0F9FF !important; }} /* خلفية سماوية فاتحة جـداً */
    
    /* الكارد الرئيسي الملون */
    .main-card {{
        background: white; padding: 25px; border-radius: 25px;
        border-top: 12px solid #0284C7; /* أزرق ملكي في الأعلى */
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 20px;
    }}
    
    /* صناديق الواجهات العائمة */
    .info-box {{
        background: white; padding: 20px; border-radius: 20px;
        border-{"right" if st.session_state.lang == 'ar' else "left"}: 8px solid #38BDF8; /* أزرق سماوي مضيء */
        margin-bottom: 15px; border: 1px solid #BAE6FD;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05); transition: transform 0.3s ease;
    }}
    .info-box:hover {{ transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }}

    /* أزرار المواصلات والتحليل - التوهج عند التمرير */
    .stButton>button {{
        background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important;
        color: white !important; border: none !important; border-radius: 12px !important;
        font-weight: bold !important; width: 100%; height: 3.5em !important;
        transition: all 0.3s ease !important;
    }}
    .stButton>button:hover {{
        transform: translateY(-2px); box-shadow: 0 5px 15px rgba(2, 132, 199, 0.4) !important;
    }}

    /* الأزرار العادية */
    .stFormSubmitButton>button {{ background: #10B981 !important; }} /* زر أخضر للترحيب */
    .stFormSubmitButton>button:hover {{ box-shadow: 0 5px 15px rgba(16, 185, 129, 0.4) !important; }}
    
    /* نجوم التقييم المضاءة */
    .stRating button {{ color: #FFD700 !important; font-size: 2em; }}
    .stRating button[data-checked="true"] {{ text-shadow: 0 0 10px #FFD700; }}
    
    /* عناوين مضيئة */
    .highlight-text {{ color: #0369A1; font-weight: bold; text-shadow: 1px 1px 2px rgba(3, 105, 161, 0.1); }}
    
    [data-testid="stSidebar"] {{ display: none !important; }}
    </style>
''', unsafe_allow_html=True)

# زر اللغة
col_l1, col_l2 = st.columns([0.85, 0.15])
if col_l2.button(T["lang_btn"]):
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
    st.rerun()

# --- الصفحة الأولى (Welcome) ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.form("w_form"):
        st.markdown(f"<h1 style='text-align:center; color:#0369A1; font-size:3.5em;'>{T['title']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; color:#64748B; font-size:1.2em;'>{T['subtitle']}</p><br>", unsafe_allow_html=True)
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
            <h3 class="highlight-text">📅 {T["day"]} 1 {T["of"]} 3 | {T["welcome"]} {st.session_state.u_name}</h3>
            <p>{T["weather_label"]}: <b style="color:#0284C7;">{T["weather_val"]}</b></p>
        </div>''', unsafe_allow_html=True)

        # المواصلات: التوافق اللحظي
        st.write(T["trans_label"])
        transport = st.radio("", [T["m_car"], T["m_taxi"], T["m_metro"]], horizontal=True, label_visibility="collapsed")
        # منطق تحديث الوقت لحظياً
        st.session_state.trans_factor = 1.3 if transport == T["m_metro"] else 1.0

        st.markdown(f"<br><h4 class='highlight-text'>{T['interests_q']}</h4>", unsafe_allow_html=True)
        cats = ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"] if st.session_state.lang == 'ar' else ["History", "Entertainment", "Shopping", "Dining", "Nature"]
        u_interests = st.multiselect("", cats, label_visibility="collapsed")

        if st.button(T["analyze"]):
            st.session_state.suggestions = DB[st.session_state.u_budget][st.session_state.lang]
            st.rerun()
        
        if st.session_state.suggestions:
            for p in st.session_state.suggestions:
                calc_time = int(p["time"] * st.session_state.trans_factor)
                st.markdown(f'''<div class="info-box">
                    <h4 class="highlight-text">📍 {p["name"]} <small>({p["cat"]})</small></h4>
                    <p style="color:#475569; font-size:0.95em;">{p["desc"]}</p>
                    <div style="display: flex; justify-content: space-between; font-weight: bold; color: #0369A1;">
                        <span>{T["compat"]} {p["compat"]}</span>
                        <span>{T["time_est"]} <b style="color:#0284C7;">{calc_time} min</b></span>
                    </div>
                </div>''', unsafe_allow_html=True)

    with col_side:
        st.markdown(f"<h4 class='highlight-text'>{T['rating_title']}</h4>", unsafe_allow_html=True)
        st.feedback("stars") # النجوم المضاءة
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button(T["reset"]):
            st.session_state.clear()
            st.rerun()
