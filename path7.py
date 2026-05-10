import streamlit as st
import random
from datetime import datetime
import pytz

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)

# 2. القاموس الشامل للترجمة
TRANSLATIONS = {
    "ar": {
        "title": "📍 Path7 | المسار الذكي",
        "subtitle": "نظام التوافق اللحظي للسياحة الذكية",
        "u_name_label": "اسم السائح الموقر",
        "start_btn": "استكشف مسارك الآن 🚀",
        "budget_label": "الميزانية المرصودة",
        "interests_q": "🌟 ما هي اهتماماتك المفضلة لليوم؟",
        "analyze_btn": "تحليل الوجهات الأنسب لهذا اليوم 🔍",
        "transport_q": "🚕 كيف تفضل الوصول لوجهاتك اليوم؟",
        "metro": "مترو الرياض", "car": "سيارتي", "taxi": "تاكسي",
        "time_text": "الوقت المقدر من المروج:",
        "eco": "اقتصادية / متوسطة", "lux": "فاخرة",
        "reset": "🔄 ضبط جديد", "lang_btn": "English 🌐",
        "dir": "rtl", "align": "right"
    },
    "en": {
        "title": "📍 Path7 | Smart Journey",
        "subtitle": "Real-time Smart Tourism System",
        "u_name_label": "Tourist Name",
        "start_btn": "Explore Your Path Now 🚀",
        "budget_label": "Planned Budget",
        "interests_q": "🌟 What are your interests for today?",
        "analyze_btn": "Analyze Best Destinations 🔍",
        "transport_q": "🚕 How do you prefer to get there?",
        "metro": "Riyadh Metro", "car": "My Car", "taxi": "Taxi",
        "time_text": "Est. time from Al-Murooj:",
        "eco": "Economy / Medium", "lux": "Luxury",
        "reset": "🔄 Reset", "lang_btn": "العربية 🌐",
        "dir": "ltr", "align": "left"
    }
}

# خريطة ترجمة الأماكن والبيانات (Data Map)
DATA_MAP = {
    "أسواق المعيقلية": "Al-Mueaqilia Markets", "حصن المصمك": "Masmak Fortress", 
    "سوق الزل": "Souq Al-Zal", "مركز الملك عبدالله المالي (KAFD)": "KAFD",
    "واجهة روشن": "ROSHN Front", "وادي حنيفة / نمار": "Wadi Hanifa",
    "منتزه الملك عبد الله": "King Abdullah Park", "حافة العالم": "Edge of the World",
    "حي الطريف": "At-Turaif", "فيا الرياض": "VIA Riyadh",
    "بوليفارد ستي": "Boulevard City", "مطل البجيري": "Al-Bujairi Terrace",
    "تاريخ وآثار": "History", "تسوق": "Shopping", "ترفيه": "Entertainment",
    "طبيعة": "Nature", "مطاعم ومقاهي": "Dining", "اقتصادية / متوسطة": "Economy"
}

# 3. إدارة الحالة (Session State) وتجنب خطأ AttributeError
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'user_name' not in st.session_state: st.session_state.user_name = ""

T = TRANSLATIONS[st.session_state.lang]

# 4. التنسيق الجمالي (تدرجات الأزرق والسماوي)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {T["dir"]}; text-align: {T["align"]}; }}
    .stApp {{ background-color: #F0F9FF !important; }}
    .highlight-box {{ background-color: #E0F2FE; padding: 20px; border-radius: 18px; border-{"right" if st.session_state.lang=="ar" else "left"}: 10px solid #0EA5E9; margin-bottom: 20px; }}
    .main-card {{ background: white; padding: 25px; border-radius: 25px; border-top: 12px solid #0284C7; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }}
    .info-box {{ background: white; padding: 20px; border-radius: 20px; border-{"right" if st.session_state.lang=="ar" else "left"}: 8px solid #38BDF8; border: 1px solid #BAE6FD; margin-bottom: 15px; }}
    .stButton>button {{ background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important; color: white !important; border-radius: 15px !important; font-weight: bold !important; border:none !important; height: 3.5em !important; width: 100% !important; }}
    </style>
''', unsafe_allow_html=True)

# زر تبديل اللغة
if st.button(T["lang_btn"]):
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
    st.rerun()

# 5. قاعدة البيانات المحدثة بناءً على ملف (الأماكن حسب الفئة والميزانية)
PLACES_DB = {
    "اقتصادية / متوسطة": [
        {"الوجهة": "أسواق المعيقلية", "الفئة": "تسوق", "وصف": "مركز تسوق تقليدي للبخور والعود والبشوت.", "base_time": 25, "metro": True},
        {"الوجهة": "حصن المصمك", "الفئة": "تاريخ وآثار", "وصف": "رمز توحيد المملكة وتأسيسها.", "base_time": 28, "metro": True},
        {"الوجهة": "سوق الزل", "الفئة": "تسوق", "وصف": "أقدم سوق مليء بالتاريخ والتحف النادرة.", "base_time": 27, "metro": True},
        {"الوجهة": "مركز الملك عبدالله المالي (KAFD)", "الفئة": "مطاعم ومقاهي", "وصف": "أعجوبة معمارية وأيقونة اقتصادية حديثة.", "base_time": 10, "metro": True},
        {"الوجهة": "مركز الملك عبدالله المالي (KAFD)", "الفئة": "تسوق", "وصف": "أعجوبة معمارية وأيقونة اقتصادية حديثة.", "base_time": 10, "metro": True},
        {"الوجهة": "واجهة روشن", "الفئة": "تسوق", "وصف": "ممشى مفتوح للتسوق والمطاعم العصرية.", "base_time": 22, "metro": False},
        {"الوجهة": "وادي حنيفة / نمار", "الفئة": "طبيعة", "وصف": "مساحات خضراء خلابة وبحيرات مثالية للنزهات.", "base_time": 35, "metro": False},
        {"الوجهة": "منتزه الملك عبد الله", "الفئة": "طبيعة", "وصف": "نافورات راقصة ومساحات خضراء شاسعة للعائلات.", "base_time": 30, "metro": False},
        {"الوجهة": "حافة العالم", "الفئة": "طبيعة", "وصف": "إطلالات منحدرة تخطف الأنفاس لعشاق الطبيعة.", "base_time": 90, "metro": False}
    ],
    "فاخرة": [
        {"الوجهة": "حي الطريف", "الفئة": "تاريخ وآثار", "وصف": "موقع اليونسكو وقلب التاريخ السعودي.", "base_time": 18, "metro": True},
        {"الوجهة": "فيا الرياض", "الفئة": "ترفيه", "وصف": "عمارة سلمية مع مطاعم وسينما عالمية.", "base_time": 15, "metro": False},
        {"الوجهة": "فيا الرياض", "الفئة": "تسوق", "وصف": "عمارة سلمية مع مطاعم وسينما عالمية.", "base_time": 15, "metro": False},
        {"الوجهة": "بوليفارد ستي", "الفئة": "ترفيه", "وصف": "أكبر منطقة في العاصمة للثقافات العالمية والألعاب.", "base_time": 12, "metro": False},
        {"الوجهة": "مطل البجيري", "الفئة": "تاريخ وآثار", "وصف": "مطاعم راقية بإطلالات على وادي حنيفة.", "base_time": 18, "metro": True},
        {"الوجهة": "مطل البجيري", "الفئة": "مطاعم ومقاهي", "وصف": "مطاعم راقية بإطلالات على وادي حنيفة.", "base_time": 18, "metro": True}
    ]
}

# --- الصفحة الأولى: الترحيب ---
if st.session_state.page == 'welcome':
    with st.form("welcome_form"):
        st.markdown(f'<h1 style="text-align: center; color: #0369A1;">{T["title"]}</h1>', unsafe_allow_html=True)
        u_name = st.text_input(T["u_name_label"], value="") # الاسم فارغ الآن
        u_budget = st.radio(T["budget_label"], [T["eco"], T["lux"]], horizontal=True)
        if st.form_submit_button(T["start_btn"]):
            st.session_state.user_name = u_name
            st.session_state.user_budget = "اقتصادية / متوسطة" if u_budget in ["Economy / Medium", "اقتصادية / متوسطة"] else "فاخرة"
            st.session_state.page = 'system'
            st.rerun()

# --- الصفحة الثانية: لوحة التحكم ---
else:
    st.markdown(f'<div class="main-card"><h3>📅 {T["day"]} {st.session_state.current_day}</h3><p>{T["welcome"]} <b>{st.session_state.user_name}</b></p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="highlight-box"><h4>{T["interests_q"]}</h4></div>', unsafe_allow_html=True)
    
    # قائمة الاهتمامات
    interest_options = ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"]
    if st.session_state.lang == "en":
        interest_options = [DATA_MAP.get(i, i) for i in interest_options]

    u_interests = st.multiselect("", interest_options, label_visibility="collapsed")

    if st.button(T["analyze_btn"]):
        available = PLACES_DB[st.session_state.user_budget]
        final = []
        # إصلاح منطق البحث: عرض كل ما يطابق أي اهتمام مختار من الملف المحدث
        for item in available:
            item_cat_en = DATA_MAP.get(item['الفئة'], item['الفئة'])
            if item['الفئة'] in u_interests or item_cat_en in u_interests:
                if item not in final: # منع تكرار الوجهة إذا كانت تتبع فئتين مختلفتين
                    final.append(item)
        st.session_state.suggestions = final

    if st.session_state.suggestions:
        # عرض الوجهات مع مساحة الصور
        for p in st.session_state.suggestions:
            display_name = DATA_MAP.get(p['الوجهة'], p['الوجهة']) if st.session_state.lang == "en" else p['الوجهة']
            st.markdown(f'<div class="info-box"><h4>📍 {display_name}</h4><p>{p["وصف"]}</p></div>', unsafe_allow_html=True)

    if st.button(T["reset"]):
        st.session_state.clear()
        st.rerun()
