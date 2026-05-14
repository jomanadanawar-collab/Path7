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

# --- CSS النهائي لإصلاح مشكلة الأزرار واللغة ---
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    :root {{
        --primary-bg: #075985;
        --secondary-bg: #03456F;
        --accent-blue: #0EA5E9;
    }}
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if st.session_state.lang == "العربية" else "ltr"}; }}
    
    /* الخلفية الثابتة */
    .stApp {{ background: linear-gradient(145deg, var(--primary-bg) 0%, var(--secondary-bg) 100%) !important; color: white !important; }}
    
    /* إصلاح الأزرار: النص أسود داخل الأزرار البيضاء ليكون واضحاً */
    .stButton>button {{ 
        background-color: white !important; 
        color: #075985 !important; 
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
    }}
    
    /* زر اللغة المميز */
    .lang-btn button {{
        background-color: rgba(255,255,255,0.2) !important;
        color: white !important;
        border: 1px solid white !important;
    }}

    .glass-card {{ background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(15px); padding: 25px; border-radius: 25px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; }}
    .dash-panel {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); padding: 15px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; text-align: center; }}
    
    /* بطاقة الوجهة */
    .dest-card {{ background: white !important; padding: 20px; border-radius: 20px; border-{"right" if st.session_state.lang == "العربية" else "left"}: 10px solid var(--accent-blue); margin-bottom: 15px; color: #1E293B !important; }}
    .dest-card h4, .dest-card p, .dest-card b, .dest-card span {{ color: #1E293B !important; }}

    /* تذكرة المترو */
    .metro-ticket {{ 
        background: linear-gradient(90deg, #DC2626 0%, #991B1B 100%); 
        color: white !important; padding: 10px; border-radius: 10px; 
        font-size: 0.8em; margin-bottom: 10px; border-left: 5px dashed white;
    }}
    
    .map-link {{ background-color: #0284C7; color: white !important; padding: 8px 16px; border-radius: 50px; text-decoration: none !important; font-size: 0.85em; display: inline-block; }}
    </style>
''', unsafe_allow_html=True)

# --- خيار اللغة (واضح جداً في البداية) ---
col_lang, _ = st.columns([1, 10])
with col_lang:
    if st.button("EN / عربي", key="lang_toggle"):
        st.session_state.lang = "English" if st.session_state.lang == "العربية" else "العربية"
        st.rerun()

if st.session_state.page == 'welcome':
    st.markdown(f'<div class="glass-card" style="text-align: center; margin-top: 5vh;">', unsafe_allow_html=True)
    st.title(f"📍 Path7 | مسار 7")
    st.subheader(T.get('subtitle', 'نظام التوافق اللحظي للسياحة الذكية'))
    st.session_state.user_name = st.text_input(T.get("visitor_name", "اسم السائح"), placeholder="أدخل اسمك هنا")
    u_budget = st.radio(T.get("budget_q", "الميزانية"), ["اقتصادية", "فاخرة"], horizontal=True)
    if st.button(T.get("start_btn", "ابدأ الرحلة"), use_container_width=True):
        st.session_state.budget_key = "Luxury" if u_budget == "فاخرة" else "Economy"
        st.session_state.page = 'main'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # لوحة المعلومات
    st.markdown(f'''<div class="dash-panel">
        <h2 style="margin:0; color:white !important;">{st.session_state.user_name}، طاب يومك</h2>
        <p style="color:white !important;">🕒 {formatted_time} | اليوم {st.session_state.day} من 3</p>
    </div>''', unsafe_allow_html=True)

    selected_ints = st.multiselect("🌟 اختر اهتماماتك:", ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"])
    
    if st.button("🔍 تحليل المسار", use_container_width=True):
        db = T.get("db", {}).get(st.session_state.budget_key, [])
        st.session_state.suggestions = [p for p in db if p.get('الفئة') in selected_ints] if selected_ints else random.sample(db, 2)
        st.session_state.transport_choice = None
        st.session_state.rated = False
        st.rerun()

    if st.session_state.suggestions:
        st.write("### وسيلة النقل:")
        tc = st.columns(3)
        if tc[0].button("🚇 المترو"): st.session_state.transport_choice = "metro"
        if tc[1].button("🚗 السيارة"): st.session_state.transport_choice = "car"
        if tc[2].button("🚕 التاكسي"): st.session_state.transport_choice = "taxi"

        for i, p in enumerate(st.session_state.suggestions):
            st.markdown(f'''
            <div class="dest-card">
                {f'<div class="metro-ticket">🎫 تذكرة المترو - المسار المعتمد</div>' if st.session_state.transport_choice == "metro" and p.get('metro') else ''}
                <h4>{i+1}. {p["الوجهة"]}</h4>
                <p>{p["وصف"]}</p>
                <p style="font-size:0.8em;">🕒 ساعات العمل: {p.get('ساعات العمل', '24 ساعة')}</p>
                <b>⏱️ الوقت: {p['b_time'] if st.session_state.transport_choice else "--"} دقيقة</b><br>
                <a href="{p['map_url']}" target="_blank" class="map-link">📍 الموقع على الخريطة</a>
            </div>
            ''', unsafe_allow
