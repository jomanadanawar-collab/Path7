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
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'rated' not in st.session_state: st.session_state.rated = False

IS_AR = st.session_state.lang == "العربية"

# خريطة ربط لضمان عمل "تحليل المسار" باللغتين
interest_map = {
    "History": "تاريخ وآثار",
    "Entertainment": "ترفيه",
    "Nature": "طبيعة",
    "Shopping": "تسوق",
    "Dining": "مطاعم ومقاهي"
}

# نصوص الواجهة
strings = {
    "title": "Path7 | مسار 7 📍",
    "sub": "الذكاء الاصطناعي في خدمة سياحتك" if IS_AR else "AI at your tourism service",
    "name_q": "مرحباً بك، ما هو اسمك؟" if IS_AR else "Welcome, what is your name?",
    "budget_q": "حدد طابع رحلتك اليوم:" if IS_AR else "Choose your trip style:",
    "budgets": ["اقتصادية", "فاخرة"] if IS_AR else ["Economy", "Luxury"],
    "start_btn": "انطلق لاستكشاف الرياض 🚀" if IS_AR else "Explore Riyadh 🚀",
    "day_lbl": f"📅 يوم {st.session_state.day} من 3" if IS_AR else f"📅 Day {st.session_state.day} of 3",
    "weather": ("صافي 🌙" if hour >= 18 or hour < 5 else "مشمس ☀️") if IS_AR else ("Clear 🌙" if hour >= 18 or hour < 5 else "Sunny ☀️"),
    "interests_q": "ما هي اهتماماتك المفضلة اليوم؟" if IS_AR else "What are your interests today?",
    "analyze_btn": "تحليل المسار الذكي 🔍" if IS_AR else "Analyze Smart Path 🔍",
    "trans_q": "وسيلة النقل المفضلة" if IS_AR else "Preferred Transport",
    "rating_t": "تقييمك للتجربة ⭐" if IS_AR else "Rate your experience ⭐",
    "final_msg": "شكرًا لثقتك بـ Path7.. نتمنى لك رحلة سعيدة! ✨" if IS_AR else "Thank you for trusting Path7.. Happy travels! ✨"
}

# 4. التنسيق البصري (استعادة الهوية الأصلية الداكنة)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if IS_AR else "ltr"}; }}
    .stApp {{ background-color: #1A202C; }} /* الخلفية الداكنة الأصلية */
    .glass-card {{ 
        background: rgba(255, 255, 255, 0.05); 
        padding: 40px; 
        border-radius: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        text-align: center;
        margin-bottom: 30px;
    }}
    .stTextInput>div>div>input, .stButton>button {{
        background-color: white !important;
        color: #1A202C !important;
        border-radius: 30px !important;
        height: 50px !important;
        font-weight: bold !important;
    }}
    h1, h2, h3, p, label {{ color: white !important; }}
    .dest-card {{ 
        background: white; 
        padding: 20px; 
        border-radius: 15px; 
        margin-bottom: 10px; 
        text-align: {"right" if IS_AR else "left"};
    }}
    .dest-card h4, .dest-card p {{ color: #1A202C !important; }}
    </style>
''', unsafe_allow_html=True)

# زر اللغة (أبيض شفاف)
if st.button("عربي / EN", key="lang_btn"):
    st.session_state.lang = "English" if IS_AR else "العربية"
    st.rerun()

# --- الصفحات ---
if st.session_state.page == 'welcome':
    st.markdown(f'''<div class="glass-card">
        <h1 style="font-size: 3.5em;">{strings["title"]}</h1>
        <p style="font-size: 1.5em; opacity: 0.8;">{strings["sub"]}</p>
    </div>''', unsafe_allow_html=True)
    
    col_w1, col_w2, col_w3 = st.columns([1, 3, 1])
    with col_w2:
        st.session_state.user_name = st.text_input(strings["name_q"], placeholder="أدخل اسمك الكريم هنا")
        u_budget = st.radio(strings["budget_q"], strings["budgets"], horizontal=True)
        if st.button(strings["start_btn"]):
            st.session_state.budget_key = "Luxury" if (u_budget in ["فاخرة", "Luxury"]) else "Economy"
            st.session_state.page = 'system'; st.rerun()

else:
    # واجهة النظام (يوم 1 من 3)
    st.markdown(f'<h2 style="text-align:center;">{strings["day_lbl"]}</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; opacity:0.7;">👤 {st.session_state.user_name} | 🕒 {now_riyadh.strftime("%I:%M %p")} | 🌤️ {strings["weather"]}</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader(strings["interests_q"])
    interests = ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"] if IS_AR else ["History", "Entertainment", "Nature", "Shopping", "Dining"]
    selected = st.multiselect("", interests, label_visibility="collapsed")
    
    if st.button(strings["analyze_btn"]):
        # ضمان سحب البيانات باللغتين
        db = DATA_ALL.get("العربية", {}).get("db", {}).get(st.session_state.budget_key, [])
        search_terms = [interest_map.get(i, i) for i in selected]
        st.session_state.suggestions = [p for p in db if p.get('الفئة') in search_terms] or db[:2]
        st.rerun()

    if st.session_state.suggestions:
        for p in st.session_state.suggestions:
            st.markdown(f'''<div class="dest-card">
                <h4>{p["الوجهة"]}</h4>
                <p>{p["وصف"]}</p>
            </div>''', unsafe_allow_html=True)

    # قسم التقييم والعبارة اللطيفة
    st.markdown("---")
    st.write(strings["rating_t"])
    stars = st.columns(5)
    for i in range(1, 6):
        if stars[i-1].button(f"⭐{i}", key=f"s{i}"): st.session_state.rated = True
    
    if st.session_state.rated:
        if st.session_state.day < 3:
            if st.button("اليوم التالي ⏭️"):
                st.session_state.day += 1; st.session_state.rated = False; st.session_state.suggestions = []; st.rerun()
        else:
            # العبارة اللطيفة المطلوبة في اليوم الأخير
            st.success(strings["final_msg"])

st.markdown("<p style='text-align: center; color: gray; font-size: 0.8em; margin-top: 50px;'>Path7 | Engineering Excellence @ IAU</p>", unsafe_allow_html=True)
