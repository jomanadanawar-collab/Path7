import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

st.set_page_config(page_title="Path7 | Smart Journey", layout="wide", initial_sidebar_state="collapsed")

# 2. قاموس اللغات (ثابت لتسهيل التحويل)
TRANSLATIONS = {
    "ar": {
        "title": "📍 Path7 | المسار الذكي",
        "subtitle": "نظام التوافق اللحظي للسياحة الذكية",
        "name_label": "اسم السائح الموقر",
        "budget_label": "حدد نوع الميزانية للرحلة",
        "eco": "اقتصادية", "lux": "فاخرة",
        "start_btn": "استكشف مسارك الآن 🚀",
        "welcome": "مرحباً يا", "day": "اليوم", "of": "من", "weather": "الجو في الرياض",
        "interests_q": "🌟 ما هي اهتماماتك المفضلة لليوم؟",
        "analyze": "تحليل الوجهات الأنسب لهذا اليوم 🔍",
        "transport_q": "🚕 كيف تفضل الوصول لوجهاتك اليوم؟",
        "metro": "🚇 مترو الرياض", "car": "🚗 سيارتي", "taxi": "🚕 تاكسي",
        "time_est": "⏱️ الوقت المقدر:",
        "reset": "🔄 ضبط جديد", "lang_btn": "English 🌐"
    },
    "en": {
        "title": "📍 Path7 | Smart Journey",
        "subtitle": "Real-time Smart Tourism Compatibility System",
        "name_label": "Tourist Name",
        "budget_label": "Select Trip Budget",
        "eco": "Economy", "lux": "Luxury",
        "start_btn": "Explore Your Path Now 🚀",
        "welcome": "Welcome", "day": "Day", "of": "of", "weather": "Riyadh Weather",
        "interests_q": "🌟 What are your interests for today?",
        "analyze": "Analyze Best Destinations 🔍",
        "transport_q": "🚕 How do you prefer to get there?",
        "metro": "🚇 Riyadh Metro", "car": "🚗 My Car", "taxi": "🚕 Taxi",
        "time_est": "⏱️ Estimated Time:",
        "reset": "🔄 Reset", "lang_btn": "العربية 🌐"
    }
}

# 3. البيانات المحدثة (من ملف الميزانية المعدلة)
PLACES_DB = {
    "اقتصادية": [
        {"الوجهة": "أسواق المعيقلية", "الفئة": "تسوق", "وصف": "مركز تقليدي للبخور والعود.", "base_time": 25, "metro": True},
        {"الوجهة": "حصن المصمك", "الفئة": "تاريخ وآثار", "وصف": "رمز لتوحيد المملكة وتأسيسها.", "base_time": 28, "metro": True},
        {"الوجهة": "سوق الزل", "الفئة": "تسوق", "وصف": "أقدم سوق مليء بالتاريخ والتحف النادرة.", "base_time": 27, "metro": True},
        {"الوجهة": "مركز الملك عبدالله المالي (KAFD)", "الفئة": "طبيعة", "وصف": "أيقونة اقتصادية حديثة.", "base_time": 10, "metro": True},
        {"الوجهة": "مركز الملك عبدالله المالي (KAFD)", "الفئة": "تسوق", "وصف": "أيقونة اقتصادية حديثة.", "base_time": 10, "metro": True},
        {"الوجهة": "مركز الملك عبدالله المالي (KAFD)", "الفئة": "مطاعم ومقاهي", "وصف": "أيقونة اقتصادية حديثة.", "base_time": 10, "metro": True},
        {"الوجهة": "وادي حنيفة / نمار", "الفئة": "طبيعة", "وصف": "مساحات خضراء وبحيرات مثالية.", "base_time": 35, "metro": False},
        {"الوجهة": "منتزه الملك عبد الله", "الفئة": "طبيعة", "وصف": "نافورات راقصة ومساحات خضراء.", "base_time": 30, "metro": False},
        {"الوجهة": "حافة العالم", "الفئة": "طبيعة", "وصف": "إطلالات منحدرة تخطف الأنفاس.", "base_time": 90, "metro": False}
    ],
    "فاخرة": [
        {"الوجهة": "حي الطريف", "الفئة": "تاريخ وآثار", "وصف": "موقع اليونسكو وقلب التاريخ.", "base_time": 18, "metro": True},
        {"الوجهة": "فيا رياض", "الفئة": "ترفيه", "وصف": "عمارة سلمية ومطاعم عالمية.", "base_time": 15, "metro": False},
        {"الوجهة": "بوليفارد سيتي", "الفئة": "ترفيه", "وصف": "أكبر منطقة للثقافات والألعاب.", "base_time": 12, "metro": False},
        {"الوجهة": "مطل البجيري", "الفئة": "تاريخ وآثار", "وصف": "مطاعم راقية بإطلالات تاريخية.", "base_time": 18, "metro": True},
        {"الوجهة": "مطل البجيري", "الفئة": "مطاعم ومقاهي", "وصف": "مطاعم راقية بإطلالات تاريخية.", "base_time": 18, "metro": True}
    ]
}

# 4. إدارة الحالة
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

T = TRANSLATIONS[st.session_state.lang]

# 5. التنسيق الجمالي (ثابت كما في ملفك)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if st.session_state.lang == "ar" else "ltr"}; text-align: {"right" if st.session_state.lang == "ar" else "left"}; }}
    .stApp {{ background-color: #F0F9FF !important; }}
    .highlight-box {{ background-color: #E0F2FE; padding: 20px; border-radius: 18px; border-right: 10px solid #0EA5E9; margin-bottom: 20px; }}
    .main-card {{ background: white; padding: 25px; border-radius: 25px; border-top: 12px solid #0284C7; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }}
    .info-box {{ background: white; padding: 20px; border-radius: 20px; border: 1px solid #BAE6FD; border-right: 8px solid #38BDF8; margin-bottom: 15px; }}
    .stButton>button {{ background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important; color: white !important; border-radius: 15px !important; height: 3.5em !important; font-weight: bold !important; width: 100%; }}
    [data-testid="stSidebar"] {{ display: none !important; }}
    </style>
''', unsafe_allow_html=True)

# زر تبديل اللغة
col_l1, col_l2 = st.columns([0.85, 0.15])
if col_l2.button(T["lang_btn"]):
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
    st.rerun()

# --- الصفحة الأولى: الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.form("welcome_form"):
        st.markdown(f'<h1 style="text-align: center; color: #0369A1;">{T["title"]}</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; color: #64748B;">{T["subtitle"]}</p>', unsafe_allow_html=True)
        u_name = st.text_input(T["name_label"], "") # شلت اسمك وخليته فاضي
        u_budget = st.radio(T["budget_label"], [T["eco"], T["lux"]], horizontal=True)
        if st.form_submit_button(T["start_btn"]):
            st.session_state.user_name = u_name
            st.session_state.user_budget = "اقتصادية" if u_budget in ["اقتصادية", "Economy"] else "فاخرة"
            st.session_state.page = 'system'
            st.rerun()

# --- الصفحة الثانية: لوحة التحكم ---
else:
    st.markdown(f'''<div class="main-card"><h3>📅 {T["day"]} {st.session_state.current_day} {T["of"]} 3</h3>
    <p>{T["welcome"]} <b>{st.session_state.user_name}</b></p></div>''', unsafe_allow_html=True)
    
    st.markdown(f'<br><div class="highlight-box"><h4>{T["interests_q"]}</h4></div>', unsafe_allow_html=True)
    
    # خيارات الاهتمامات
    options = ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"]
    u_interests = st.multiselect("", options, key="daily_int", label_visibility="collapsed")

    if st.button(T["analyze"]):
        if not u_interests:
            st.warning("الرجاء اختيار اهتمام واحد على الأقل")
        else:
            db = PLACES_DB[st.session_state.user_budget]
            # تعديل جوهري: الآن يختار وجهة واحدة عشوائية لكل اهتمام تم اختياره
            st.session_state.suggestions = []
            for interest in u_interests:
                matches = [p for p in db if p["الفئة"] == interest]
                if matches:
                    st.session_state.suggestions.append(random.choice(matches))
            st.session_state.transport_choice = None

    if st.session_state.suggestions:
        st.markdown(f'<br><div class="highlight-box"><h4>{T["transport_q"]}</h4></div>', unsafe_allow_html=True)
        t_col1, t_col2, t_col3 = st.columns(3)
        
        # فحص توفر المترو لكل الوجهات المختارة
        can_metro = all(p.get('metro', False) for p in st.session_state.suggestions)
        
        if can_metro:
            if t_col1.button(T["metro"]): st.session_state.transport_choice = "metro"
        else:
            t_col1.markdown('<p style="text-align:center; color:gray; font-size:0.8em;">المترو غير متاح للكل ❌</p>', unsafe_allow_html=True)
            
        if t_col2.button(T["car"]): st.session_state.transport_choice = "car"
        if t_col3.button(T["taxi"]): st.session_state.transport_choice = "taxi"

        for p in st.session_state.suggestions:
            st.markdown(f'''<div class="info-box"><h4>📍 {p["الوجهة"]}</h4>
            <p>{p["وصف"]}</p><p><b>{T["time_est"]}</b> {p["base_time"]} min</p></div>''', unsafe_allow_html=True)

    if st.button(T["reset"]):
        st.session_state.clear()
        st.rerun()
