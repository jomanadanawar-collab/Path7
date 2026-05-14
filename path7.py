import streamlit as st
import json
from datetime import datetime
import pytz

# 1. تحميل البيانات
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

DATA_ALL = load_data()

# 2. التوافق اللحظي
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
hour = now_riyadh.hour

# 3. إدارة الحالة واللغة
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'day' not in st.session_state: st.session_state.day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'rated' not in st.session_state: st.session_state.rated = False

IS_AR = st.session_state.lang == "العربية"

# 4. قاموس الترجمة الشامل (لحل مشكلة ترجمة محتوى الـ JSON)
# هنا تحطين الكلمات اللي في ملفك عشان تترجم تلقائياً
translation_dict = {
    # الاهتمامات
    "تاريخ وآثار": "History",
    "ترفيه": "Entertainment",
    "طبيعة": "Nature",
    "تسوق": "Shopping",
    "مطاعم ومقاهي": "Dining",
    # أمثلة لأسماء أماكن (أضيفي أسماء أماكنك هنا)
    "المصمك": "Al Masmak",
    "الدرعية": "Diriyah",
    "بوليفارد": "Boulevard",
    # أوصاف عامة (أمثلة)
    "مكان تاريخي رائع": "A wonderful historical place",
    "حديقة جميلة": "A beautiful park"
}

# عكس القاموس للبحث العكسي
rev_trans = {v: k for k, v in translation_dict.items()}

# نصوص الواجهة ثابتة
strings = {
    "title": "Path7 📍",
    "sub": "نظام التوافق اللحظي للسياحة الذكية" if IS_AR else "Real-time Smart Tourism System",
    "name_q": "مرحباً بك، ما هو اسمك؟" if IS_AR else "Welcome, what is your name?",
    "budget_q": "حدد طابع رحلتك اليوم:" if IS_AR else "Choose your trip style:",
    "budgets": ["اقتصادية", "فاخرة"] if IS_AR else ["Economy", "Luxury"],
    "start_btn": "انطلق لاستكشاف الرياض 🚀" if IS_AR else "Explore Riyadh 🚀",
    "day_lbl": f"📅 يوم {st.session_state.day} من 3" if IS_AR else f"📅 Day {st.session_state.day} of 3",
    "weather": ("مشمس ☀️" if 5 <= hour <= 17 else "صافي 🌙") if IS_AR else ("Sunny ☀️" if 5 <= hour <= 17 else "Clear 🌙"),
    "interests_q": "ما هي اهتماماتك المفضلة اليوم؟" if IS_AR else "What are your interests today?",
    "interests_list": list(translation_dict.keys()) if IS_AR else list(translation_dict.values()),
    "analyze_btn": "تحليل المسار الذكي 🔍" if IS_AR else "Analyze Smart Path 🔍",
    "rating_t": "تقييمك للتجربة ⭐" if IS_AR else "Rate your experience ⭐",
    "final_msg": "شكرًا لثقتك بـ Path7.. نتمنى لك رحلة سعيدة! ✨" if IS_AR else "Thank you for trusting Path7! ✨"
}

# 5. التنسيق (الأصلي + أزرار مربعة)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if IS_AR else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); background-attachment: fixed; }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 25px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.3); margin-bottom: 20px; text-align: {"right" if IS_AR else "left"}; }}
    
    /* أزرار النجوم مربعة كما طلبتِ */
    div[data-testid="stHorizontalBlock"] button[key^="s"] {{
        width: 50px !important; height: 50px !important; border-radius: 8px !important;
        background-color: white !important; color: #0284C7 !important; border: 1px solid #E2E8F0 !important;
    }}
    .stButton>button {{ background: linear-gradient(90deg, #0284C7, #38BDF8) !important; color: white !important; border-radius: 10px !important; width: 100%; }}
    </style>
''', unsafe_allow_html=True)

# زر اللغة
if st.sidebar.button("العربية / EN"):
    st.session_state.lang = "English" if IS_AR else "العربية"
    st.rerun()

if st.session_state.page == 'welcome':
    st.markdown(f'<div class="glass-card" style="text-align: center;"><h1>{strings["title"]}</h1><p>{strings["sub"]}</p></div>', unsafe_allow_html=True)
    st.session_state.user_name = st.text_input(strings["name_q"])
    u_budget = st.radio(strings["budget_q"], strings["budgets"], horizontal=True)
    if st.button(strings["start_btn"]):
        st.session_state.budget_key = "Luxury" if (u_budget in ["Luxury", "فاخرة"]) else "Economy"
        st.session_state.page = 'system'; st.rerun()

else:
    st.markdown(f'<div class="glass-card"><h3>{strings["day_lbl"]}</h3><p>👤 {st.session_state.user_name} | 🕒 {now_riyadh.strftime("%I:%M %p")} | 🌤️ {strings["weather"]}</p></div>', unsafe_allow_html=True)
    
    selected = st.multiselect(strings["interests_q"], strings["interests_list"])
    
    if st.button(strings["analyze_btn"]):
        # البحث دائماً بالمفتاح العربي في الـ JSON
        db = DATA_ALL.get("العربية", {}).get("db", {}).get(st.session_state.budget_key, [])
        search_terms = [rev_trans.get(i, i) for i in selected]
        st.session_state.suggestions = [p for p in db if p.get('الفئة') in search_terms] or db[:2]
        st.rerun()

    if st.session_state.suggestions:
        for p in st.session_state.suggestions:
            # ترجمة المحتوى لحظياً إذا كانت اللغة إنجليزية
            display_name = translation_dict.get(p["الوجهة"], p["الوجهة"]) if not IS_AR else p["الوجهة"]
            display_desc = translation_dict.get(p["وصف"], p["وصف"]) if not IS_AR else p["وصف"]
            
            st.markdown(f'<div class="dest-card" style="background:white; padding:15px; border-radius:15px; margin-bottom:10px; color:black;">'
                        f'<h4 style="color:#0284C7;">{display_name}</h4><p>{display_desc}</p></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.write(strings["rating_t"])
        cols = st.columns(5)
        for i in range(1, 6):
            if cols[i-1].button(f"{i}⭐", key=f"s{i}"): st.session_state.rated = True
        if st.session_state.rated: st.success(strings["final_msg"])
