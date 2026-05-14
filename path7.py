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

# إدارة حالة التطبيق
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'day' not in st.session_state: st.session_state.day = 1
if 'rated' not in st.session_state: st.session_state.rated = False
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

T = DATA_ALL.get(st.session_state.lang, {})

# --- CSS ثابت لإصلاح أخطاء التنسيق ووضوح النصوص ---
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    :root {{
        --primary-bg: #075985;
        --secondary-bg: #03456F;
    }}
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if st.session_state.lang == "العربية" else "ltr"}; }}
    .stApp {{ background: linear-gradient(145deg, var(--primary-bg) 0%, var(--secondary-bg) 100%) !important; color: white !important; }}
    
    /* تنسيق الأزرار لتكون واضحة (نص داكن على خلفية بيضاء) */
    .stButton>button {{ 
        background-color: white !important; 
        color: #075985 !important; 
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
    }}
    
    .dest-card {{ background: white !important; padding: 20px; border-radius: 20px; border-right: 10px solid #0EA5E9; margin-bottom: 15px; color: #1E293B !important; }}
    .dest-card h4, .dest-card p, .dest-card b {{ color: #1E293B !important; }}
    
    .metro-ticket {{ 
        background: linear-gradient(90deg, #DC2626 0%, #991B1B 100%); 
        color: white !important; padding: 8px; border-radius: 8px; 
        font-size: 0.8em; margin-bottom: 10px; border-left: 4px dashed white;
    }}
    
    .dash-panel {{ background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; text-align: center; }}
    </style>
''', unsafe_allow_html=True)

# زر تغيير اللغة في الأعلى
if st.button("EN / عربي"):
    st.session_state.lang = "English" if st.session_state.lang == "العربية" else "العربية"
    st.rerun()

if st.session_state.page == 'welcome':
    st.markdown('<div class="dash-panel"><h1>📍 Path7 | مسار 7</h1></div>', unsafe_allow_html=True)
    st.session_state.user_name = st.text_input("اسم السائح", placeholder="أدخل اسمك هنا")
    u_budget = st.radio("الميزانية المناسبة", ["اقتصادية", "فاخرة"], horizontal=True)
    if st.button("ابدأ استكشاف المسار"):
        st.session_state.budget_key = "Luxury" if u_budget == "فاخرة" else "Economy"
        st.session_state.page = 'main'
        st.rerun()

else:
    st.markdown(f'<div class="dash-panel"><h2>مرحباً {st.session_state.user_name}</h2><p>اليوم {st.session_state.day} من 3</p></div>', unsafe_allow_html=True)
    
    # اهتمامات بناءً على ملف الميزانية
    selected_ints = st.multiselect("🌟 اختر اهتماماتك:", ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"])
    
    if st.button("تحليل المسار الذكي"):
        db = T.get("db", {}).get(st.session_state.budget_key, [])
        st.session_state.suggestions = [p for p in db if p.get('الفئة') in selected_ints] if selected_ints else random.sample(db, 2)
        st.session_state.transport_choice = None
        st.rerun()

    if st.session_state.suggestions:
        st.write("### وسيلة النقل:")
        c1, c2, c3 = st.columns(3)
        if c1.button("🚇 المترو"): st.session_state.transport_choice = "metro"
        if c2.button("🚗 السيارة"): st.session_state.transport_choice = "car"
        if c3.button("🚕 التاكسي"): st.session_state.transport_choice = "taxi"

        for i, p in enumerate(st.session_state.suggestions):
            st.markdown(f'''
            <div class="dest-card">
                {f'<div class="metro-ticket">🎫 تذكرة المترو - مسار الرياض الذكي</div>' if st.session_state.transport_choice == "metro" else ''}
                <h4>{i+1}. {p["الوجهة"]}</h4>
                <p>{p["وصف"]}</p>
                <p style="font-size:0.8em;">🕒 ساعات العمل: {p.get('ساعات العمل', 'متوفر الآن')}</p>
                <a href="{p.get('map_url', '#')}" target="_blank" style="color:#0284C7; font-weight:bold;">📍 فتح في الخريطة</a>
            </div>
            ''', unsafe_allow_html=True)

        # نظام التقييم والانتقال لليوم التالي
        if st.button("⭐ تقييم اليوم وإظهار اليوم التالي"):
            st.session_state.rated = True
        
        if st.session_state.rated and st.session_state.day < 3:
            if st.button("انتقل لليوم التالي ⏩"):
                st.session_state.day += 1
                st.session_state.suggestions = []
                st.session_state.rated = False
                st.rerun()
