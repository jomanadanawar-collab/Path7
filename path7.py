import streamlit as st
import json
from datetime import datetime
import pytz

# 1. تحميل البيانات
@st.cache_data
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

DATA_ALL = load_data()

# 2. إعدادات الوقت واللغة والحالة (لضمان ثبات النتائج)
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
hour = now_riyadh.hour

if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'budget_key' not in st.session_state: st.session_state.budget_key = "Economy"

IS_AR = st.session_state.lang == "العربية"

# القاموس السحري لحل مشكلة الإنجليزي (Mapping)
# يربط ما يختاره المستخدم باللغة الإنجليزية بما هو مخزن فعلياً في ملف الـ JSON
INTEREST_MAP = {
    "History": "تاريخ وآثار",
    "Entertainment": "ترفيه",
    "Nature": "طبيعة",
    "Shopping": "تسوق",
    "Dining": "مطاعم ومقاهي"
}

# نصوص الواجهة الأصلية
strings = {
    "title": "Path7 📍",
    "sub": "نظام التوافق اللحظي للسياحة الذكية" if IS_AR else "Real-time Smart Tourism System",
    "name_q": "مرحباً بك، ما هو اسمك؟" if IS_AR else "Welcome, what is your name?",
    "budget_q": "حدد طابع رحلتك اليوم:" if IS_AR else "Choose your trip style:",
    "budgets": ["اقتصادية", "فاخرة"] if IS_AR else ["Economy", "Luxury"],
    "start_btn": "انطلق لاستكشاف الرياض 🚀" if IS_AR else "Explore Riyadh 🚀",
    "day_lbl": f"📅 اليوم 1 من 3" if IS_AR else f"📅 Day 1 of 3",
    "interests_q": "ما هي اهتماماتك المفضلة اليوم؟" if IS_AR else "What are your interests today?",
    "interests_list": ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"] if IS_AR else list(INTEREST_MAP.keys()),
    "analyze_btn": "تحليل المسار الذكي 🔍" if IS_AR else "Smart Path Analysis 🔍",
    "trans_q": "وسيلة النقل المفضلة" if IS_AR else "Preferred Transport",
    "metro": "🚇 المترو" if IS_AR else "🚇 Metro",
    "car": "🚗 السيارة" if IS_AR else "🚗 Car",
    "taxi": "🚕 التاكسي" if IS_AR else "🚕 Taxi",
    "map_btn": "📍 فتح في الخرائط" if IS_AR else "📍 Open Maps",
    "select_trans": "⏳ حدد وسيلة النقل لمعرفة المسار" if IS_AR else "⏳ Select transport to see path",
    "reset": "إعادة ضبط 🔄" if IS_AR else "Reset 🔄"
}

# 3. التصميم الأصلي (CSS) - Glassmorphism
text_align = "right" if IS_AR else "left"
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if IS_AR else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 25px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.3); margin-bottom: 20px; text-align: {text_align}; }}
    .dest-card {{ background: white; padding: 20px; border-radius: 20px; border-{"right" if IS_AR else "left"}: 10px solid #0EA5E9; margin-bottom: 15px; color: black; }}
    .stButton>button {{ background: linear-gradient(90deg, #0284C7, #38BDF8) !important; color: white !important; border-radius: 10px !important; }}
    
    /* النجوم مربعة 1:1 كما في طلبك للجنة */
    div[data-testid="stHorizontalBlock"] button[key^="s"] {{
        aspect-ratio: 1/1 !important; width: 55px !important; height: 55px !important; border-radius: 12px !important;
    }}
    </style>
''', unsafe_allow_html=True)

# زر تبديل اللغة (Sidebar لضمان عدم تداخل التصميم)
if st.sidebar.button("AR/EN"):
    st.session_state.lang = "English" if IS_AR else "العربية"
    st.rerun()

# --- محتوى الصفحات ---
if st.session_state.page == 'welcome':
    st.markdown(f'<div class="glass-card" style="text-align: center;"><h1>{strings["title"]}</h1><p>{strings["sub"]}</p></div>', unsafe_allow_html=True)
    col_w1, col_w2, col_w3 = st.columns([1, 2, 1])
    with col_w2:
        st.session_state.user_name = st.text_input(strings["name_q"])
        u_budget = st.radio(strings["budget_q"], strings["budgets"], horizontal=True)
        if st.button(strings["start_btn"]):
            st.session_state.budget_key = "Luxury" if (u_budget in ["فاخرة", "Luxury"]) else "Economy"
            st.session_state.page = 'system'; st.rerun()

else:
    col_m, col_s = st.columns([2.2, 1])
    with col_m:
        st.markdown(f'<div class="glass-card"><h3>{strings["day_lbl"]}</h3><p>👤 {st.session_state.user_name} | 🕒 {now_riyadh.strftime("%I:%M %p")}</p></div>', unsafe_allow_html=True)
        
        st.subheader(strings["interests_q"])
        selected = st.multiselect("", strings["interests_list"], label_visibility="collapsed")
        
        # الزر الآن يقوم بالمعالجة ويحفظ النتائج في الـ session_state لضمان ثباتها
        if st.button(strings["analyze_btn"]):
            # البحث عن البيانات الصحيحة
            db = []
            for key in DATA_ALL.keys():
                if key.lower() == st.session_state.lang.lower() or (not IS_AR and key.lower().startswith('en')):
                    db = DATA_ALL[key].get("db", {}).get(st.session_state.budget_key, [])
            
            # حل مشكلة الإنجليزي: تحويل المدخلات لمطابقة كلمات الـ JSON
            search_terms = [INTEREST_MAP.get(s, s) for s in selected] if not IS_AR else selected
            
            # الفلترة والحفظ
            st.session_state.suggestions = [p for p in db if p.get('الفئة') in search_terms] or db[:2]
            st.session_state.transport_choice = None
            st.rerun()

        # عرض النتائج خارج الـ IF لضمان استمراريتها عند ضغط أزرار المواصلات
        if st.session_state.suggestions:
            st.markdown(f"### {strings['trans_q']}")
            t_cols = st.columns(3)
            if t_cols[0].button(strings["metro"]): st.session_state.transport_choice = "metro"
            if t_cols[1].button(strings["car"]): st.session_state.transport_choice = "car"
            if t_cols[2].button(strings["taxi"]): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                info_html = f"<p style='color:gray;'>{strings['select_trans']}</p>"
                if st.session_state.transport_choice:
                    info_html = f"<a href='#' style='color:#0284C7; font-weight:bold; text-decoration:none;'>{strings['map_btn']}</a>"
                
                st.markdown(f'''
                    <div class="dest-card">
                        <h4>{p["الوجهة"]}</h4>
                        <p>{p["وصف"]}</p>
                        {info_html}
                    </div>
                ''', unsafe_allow_html=True)

    with col_s:
        st.markdown('<div class="glass-card" style="text-align: center;"><h4>⭐ التقييم</h4>', unsafe_allow_html=True)
        stars = st.columns(5)
        for i in range(1, 6):
            stars[i-1].button(f"{i}", key=f"s{i}")
        if st.button(strings["reset"]): st.session_state.clear(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
