import streamlit as st
import random
import json
from datetime import datetime
import pytz

# وظيفة لقراءة ملف JSON
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

DATA_ALL = load_data()
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour
formatted_time = now_riyadh.strftime('%I:%M %p')

greeting = "صباح الخير" if 5 <= current_hour < 12 else "مساء الخير"

st.set_page_config(page_title="Path7 | مسار 7", layout="wide", initial_sidebar_state="collapsed")

# إدارة الحالة
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'day' not in st.session_state: st.session_state.day = 1
if 'rated' not in st.session_state: st.session_state.rated = False
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

T = DATA_ALL.get(st.session_state.lang, {})

# --- توحيد الألوان ومنع التأثر بنمط الجهاز ---
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    
    /* تثبيت ألوان الخلفية والنصوص الأساسية */
    :root {{
        --primary-bg: #075985;
        --secondary-bg: #03456F;
        --text-white: #ffffff;
        --card-bg: #ffffff;
        --accent-blue: #0EA5E9;
    }}

    * {{ 
        font-family: 'IBM Plex Sans Arabic', sans-serif !important; 
        direction: {"rtl" if st.session_state.lang == "العربية" else "ltr"};
    }}

    /* منع تأثر التطبيق بالنمط الداكن للجهاز */
    .stApp {{ 
        background: linear-gradient(145deg, var(--primary-bg) 0%, var(--secondary-bg) 100%) !important;
        color: var(--text-white) !important;
    }}

    /* توحيد ألوان البطاقات */
    .glass-card {{ 
        background: rgba(255, 255, 255, 0.08); 
        backdrop-filter: blur(15px); 
        padding: 30px; 
        border-radius: 30px; 
        border: 1px solid rgba(255,255,255,0.1); 
        color: white !important; 
        margin-bottom: 20px; 
    }}

    .dash-panel {{ 
        background: rgba(255, 255, 255, 0.05); 
        backdrop-filter: blur(10px); 
        padding: 15px; 
        border-radius: 20px; 
        border: 1px solid rgba(255,255,255,0.1); 
        margin-bottom: 20px; 
        text-align: center;
        color: white !important;
    }}

    .dest-card {{ 
        background: white !important; 
        padding: 20px; 
        border-radius: 20px; 
        border-{"right" if st.session_state.lang == "العربية" else "left"}: 12px solid var(--accent-blue); 
        margin-bottom: 15px; 
        color: #1E293B !important; /* ضمان بقاء نص البطاقة غامق وواضح */
    }}

    /* تنسيق أزرار المترو والتاكسي والسيارة لتكون موحدة */
    .stButton>button {{
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
    }}

    .stButton>button:hover {{
        border-color: var(--accent-blue) !important;
        background: rgba(14, 165, 233, 0.2) !important;
    }}

    /* تنسيق الحقول المدخلة */
    div[data-baseweb="input"], div[data-baseweb="select"] {{
        background-color: white !important;
        border-radius: 10px !important;
    }}
    
    label, p, h1, h2, h3 {{ color: white !important; }}
    .dest-card h4, .dest-card p, .dest-card b {{ color: #1E293B !important; }}
    
    .map-btn {{ 
        background-color: #0284C7; 
        color: white !important; 
        padding: 8px 16px; 
        border-radius: 50px; 
        text-decoration: none; 
        font-weight: bold; 
        font-size: 0.85em; 
        display: inline-block;
    }}
    </style>
''', unsafe_allow_html=True)

# تبديل اللغة
col_l1, col_l2 = st.columns([12, 1])
if col_l2.button("عربي/EN"):
    st.session_state.lang = "English" if st.session_state.lang == "العربية" else "العربية"
    st.session_state.suggestions = []
    st.rerun()

if st.session_state.page == 'welcome':
    st.markdown(f'<div class="glass-card" style="text-align: center; margin-top: 10vh;">', unsafe_allow_html=True)
    st.title(f"📍 {T.get('p_name', 'Path7')}")
    st.subheader(T.get('subtitle', ''))
    
    with st.container():
        st.session_state.user_name = st.text_input(T.get("visitor_name", "اسم السائح"), placeholder="أدخل اسمك هنا")
        u_budget = st.radio(T.get("budget_q", "الميزانية"), [T.get("eco", "اقتصادية"), T.get("lux", "فاخرة")], horizontal=True)
        if st.button(T.get("start_btn", "ابدأ"), use_container_width=True):
            st.session_state.budget_key = "Luxury" if u_budget in [T.get("lux", ""), "Luxury", "فاخرة"] else "Economy"
            st.session_state.page = 'main'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # لوحة المعلومات العلوية الموحدة
    weather_info = T.get("sunny", "مشمس") if 5 <= current_hour <= 17 else T.get("night", "ليل")
    st.markdown(f'''
    <div class="dash-panel">
        <h2 style="margin:0;">{greeting}، {st.session_state.user_name}</h2>
        <p style="margin:5px 0;">🕒 {formatted_time} | {T.get("weather", "الطقس")}: <b>{weather_info}</b></p>
        <span style="background:var(--accent-blue); padding:2px 15px; border-radius:50px; font-size:0.9em;">
            📅 {T.get("day", "اليوم")} {st.session_state.day} {T.get("of", "من")} 3
        </span>
    </div>
    ''', unsafe_allow_html=True)

    st.subheader(T.get("interests_q", "ما هي اهتماماتك؟"))
    selected_ints = st.multiselect("", T.get("interests_list", []), label_visibility="collapsed")
    
    if st.button(T.get("analyze_btn", "تحليل المسار"), use_container_width=True):
        db = T.get("db", {}).get(st.session_state.budget_key, [])
        st.session_state.suggestions = [p for p in db if p.get('الفئة') in selected_ints] if selected_ints else random.sample(db, 2)
        st.session_state.transport_choice = None
        st.session_state.traffic_factor = random.uniform(1.2, 1.8)
        st.session_state.rated = False
        st.rerun()

    if st.session_state.suggestions:
        st.markdown(f"### {T.get('transport_q', 'وسيلة النقل')}")
        tc = st.columns(3)
        if tc[0].button(T.get("m_btn", "المترو")): st.session_state.transport_choice = "metro"
        if tc[1].button(T.get("c
