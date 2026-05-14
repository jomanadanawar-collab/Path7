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

st.set_page_config(page_title="Path7 | مسار 7", layout="wide", initial_sidebar_state="collapsed")

# إدارة الحالة
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'day' not in st.session_state: st.session_state.day = 1
if 'rated' not in st.session_state: st.session_state.rated = False
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

T = DATA_ALL.get(st.session_state.lang, {})

# --- CSS هندسي متطور (Luxury UX) لكسر العادية ---
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    
    :root {{
        --main-gradient: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        --accent: #0ea5e9;
    }}

    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if st.session_state.lang == "العربية" else "ltr"}; }}
    
    .stApp {{ background: var(--main-gradient) !important; color: white !important; }}
    
    /* جعل الأزرار تبدو احترافية وغير عادية */
    .stButton>button {{
        background: white !important;
        color: #1e293b !important;
        border-radius: 50px !important;
        border: none !important;
        font-weight: 700 !important;
        transition: 0.3s all ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    .stButton>button:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(14, 165, 233, 0.4); }}

    /* بطاقة الوجهة السينمائية */
    .dest-card {{
        background: white !important;
        padding: 25px;
        border-radius: 25px;
        color: #1e293b !important;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        border-left: 8px solid var(--accent);
    }}
    
    .dest-card h4 {{ color: #0f172a !important; margin-bottom: 10px; font-weight: 700; }}
    .dest-card p {{ color: #475569 !important; font-size: 0.95em; }}
    
    /* تذكرة المترو */
    .metro-ticket {{
        background: #ef4444;
        color: white !important;
        padding: 10px 15px;
        border-radius: 12px;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
        margin-bottom: 15px;
        border: 2px dashed rgba(255,255,255,0.4);
    }}

    /* هيدر الصفحة */
    .header-panel {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-bottom: 30px;
    }}
    </style>
''', unsafe_allow_html=True)

# شريط اللغة العلوي
l_col1, l_col2 = st.columns([1, 8])
with l_col1:
    if st.button("EN / عربي"):
        st.session_state.lang = "English" if st.session_state.lang == "العربية" else "العربية"
        st.rerun()

if st.session_state.page == 'welcome':
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    st.markdown('''
        <div class="header-panel">
            <h1 style="font-size: 3em; margin:0;">📍 Path7 | مسار 7</h1>
            <p style="opacity: 0.8;">الذكاء الاصطناعي في خدمة سياحتك</p>
        </div>
    ''', unsafe_allow_html=True)
    
    with st.container():
        st.session_state.user_name = st.text_input("مرحباً بك، ما هو اسمك؟", placeholder="أدخل اسمك الكريم هنا")
        u_budget = st.radio("حدد طابع رحلتك اليوم:", ["اقتصادية", "فاخرة"], horizontal=True)
        if st.button("انطلق لاستكشاف الرياض 🚀", use_container_width=True):
            st.session_state.budget_key = "Luxury" if u_budget == "فاخرة" else "Economy"
            st.session_state.page = 'main'
            st.rerun()
else:
    # واجهة العرض الرئيسية
    st.markdown(f'''
        <div class="header-panel">
            <h2 style="margin:0;">{st.session_state.user_name}، الرياض بانتظارك</h2>
            <p>🕒 {formatted_time} | اليوم {st.session_state.day} من 3</p>
        </div>
    ''', unsafe_allow_html=True)

    selected_ints = st.multiselect("🌟 ماذا تود أن تكتشف الآن؟", ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"])
    
    if st.button("توليد المسار الذكي ✨", use_container_width=True):
        db = T.get("db", {}).get(st.session_state.budget_key, [])
        st.session_state.suggestions = [p for p in db if p.get('الفئة') in selected_ints] if selected_ints else random.sample(db, 2)
        st.session_state.transport_choice = None
        st.rerun()

    if st.session_state.suggestions:
        st.write("---")
        st.markdown("### اختر وسيلة النقل المناسبة:")
        t_cols = st.columns(3)
        if t_cols[0].button("🚇 المترو"): st.session_state.transport_choice = "metro"
        if t_cols[1].button("🚗 السيارة"): st.session_state.transport_choice = "car"
        if t_cols[2].button("🚕 التاكسي"): st.session_state.transport_choice = "taxi"

        for i, p in enumerate(st.session_state.suggestions):
            st.markdown(f'''
            <div class="dest-card">
                {f'<div class="metro-ticket"><span>🎫 تذكرة مترو الرياض</span> <span>{random.randint(200,900)}-RT</span></div>' if st.session_state.transport_choice == "metro" else ''}
                <h4>{i+1}. {p["الوجهة"]}</h4>
                <p>{p["وصف"]}</p>
                <div style="display:flex; justify-content: space-between; align-items:center; margin-top:15px;">
                    <span style="font-size:0.85em; background:#f1f5f9; padding:5px 12px; border-radius:50px; color:#1e293b;">🕒 ساعات العمل: {p.get('ساعات العمل', '24 ساعة')}</span>
                    <a href="{p.get('map_url', '#')}" target="_blank" style="color:var(--accent); text-decoration:none; font-weight:700;">📍 فتح الخرائط</a>
                </div>
            </div>
            ''', unsafe_allow_html=True)

        # التقييم
        st.markdown(f'<div class="header-panel" style="margin-top:40px;"><h4>كيف كانت تجربتك؟</h4>', unsafe_allow_html=True)
        s_cols = st.columns(5)
        for i in range(1, 6):
            if s_cols[i-1].button(f"{i}★", key=f"s_{i}"): st.session_state.rated = True
        
        if st.session_state.rated and st.session_state.day < 3:
            if st.button("استكشف مسار اليوم التالي ⏭️", use_container_width=True):
                st.session_state.day += 1; st.session_state.suggestions = []; st.session_state.transport_choice = None; st.session_state.rated = False; st.rerun()
