import streamlit as st
import random
from datetime import datetime
import pytz

# 1. الإعدادات الأساسية
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)

# جعل العرض واسع والخط عربي كما كان في نسختك المفضلة
st.set_page_config(page_title="Path7 | Smart Journey", layout="wide", initial_sidebar_state="collapsed")

# 2. منع الأخطاء البرمجية (الجلسة)
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

# 3. التنسيق الجمالي السماوي (النسخة التي أعجبتكِ 100%)
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"], p, label, button, input {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }
    .stApp { background-color: #F0F9FF !important; }
    .highlight-box {
        background-color: #E0F2FE; padding: 20px; border-radius: 18px;
        border-right: 10px solid #0EA5E9; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .main-card { 
        background: white; padding: 25px; border-radius: 25px; 
        border-top: 12px solid #0284C7; box-shadow: 0 10px 30px rgba(0,0,0,0.08); 
    }
    .info-box { 
        background: white; padding: 20px; border-radius: 20px; 
        border: 1px solid #BAE6FD; border-right: 8px solid #38BDF8; margin-bottom: 15px; 
    }
    .stButton>button {
        background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important;
        color: white !important; border: none !important; border-radius: 15px !important;
        height: 3.8em !important; font-weight: bold !important; width: 100% !important;
    }
    </style>
''', unsafe_allow_html=True)

# 4. بياناتك من ملف (الميزانية معدلة.docx)
PLACES_DB = {
    "اقتصادية": [
        {"الوجهة": "أسواق المعيقلية", "الفئة": "تسوق", "وصف": "مركز تسوق تقليدي للبخور والعود والبشوت.", "time": 25, "metro": True},
        {"الوجهة": "حصن المصمك", "الفئة": "تاريخ وآثار", "وصف": "رمز توحيد المملكة وتأسيسها.", "time": 28, "metro": True},
        {"الوجهة": "سوق الزل", "الفئة": "تسوق", "وصف": "أقدم سوق مليء بالتاريخ والتحف النادرة.", "time": 27, "metro": True},
        {"الوجهة": "مركز الملك عبدالله المالي (KAFD)", "الفئة": "طبيعة", "وصف": "أعجوبة معمارية وأيقونة اقتصادية حديثة.", "time": 10, "metro": True},
        {"الوجهة": "وادي حنيفة / نمار", "الفئة": "طبيعة", "وصف": "مساحات خضراء خلابة وبحيرات مثالية للنزهات.", "time": 35, "metro": False},
        {"الوجهة": "منتزه الملك عبد الله", "الفئة": "طبيعة", "وصف": "نافورات راقصة ومساحات خضراء شاسعة.", "time": 30, "metro": False},
        {"الوجهة": "حافة العالم", "الفئة": "طبيعة", "وصف": "إطلالات منحدرة تخطف الأنفاس.", "time": 90, "metro": False}
    ],
    "فاخرة": [
        {"الوجهة": "حي الطريف", "الفئة": "تاريخ وآثار", "وصف": "موقع اليونسكو وقلب التاريخ السعودي.", "time": 18, "metro": True},
        {"الوجهة": "فيا رياض", "الفئة": "ترفيه", "وصف": "عمارة سلمية مع مطاعم وسينما عالمية.", "time": 15, "metro": False},
        {"الوجهة": "بوليفارد ستي", "الفئة": "ترفيه", "وصف": "أكبر منطقة في العاصمة للثقافات العالمية.", "time": 12, "metro": False},
        {"الوجهة": "مطل البجيري", "الفئة": "مطاعم ومقاهي", "وصف": "مطاعم راقية بإطلالات تاريخية ساحرة.", "time": 18, "metro": True}
    ]
}

# --- صفحة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.form("welcome_form"):
        st.markdown('<h1 style="text-align: center; color: #0369A1;">📍 Path7</h1>', unsafe_allow_html=True)
        u_name = st.text_input("اسم السائح الموقر", value="") # فارغ كما طلبتِ
        u_budget = st.radio("حدد الميزانية", ["اقتصادية", "فاخرة"], horizontal=True)
        if st.form_submit_button("استكشف مسارك الآن 🚀"):
            st.session_state.user_name = u_name
            st.session_state.user_budget = u_budget
            st.session_state.page = 'system'
            st.rerun()

# --- صفحة النظام ---
else:
    st.markdown(f'<div class="main-card"><h3>📅 اليوم 1 من 3</h3><p>مرحباً يا <b>{st.session_state.user_name}</b></p></div><br>', unsafe_allow_html=True)
    
    st.markdown('<div class="highlight-box"><h4>🌟 ما هي اهتماماتك لليوم؟</h4></div>', unsafe_allow_html=True)
    u_interests = st.multiselect("", ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"], label_visibility="collapsed")

    if st.button("تحليل الوجهات الأنسب لهذا اليوم 🔍"):
        # حل مشكلة التضارب (الآن يظهر كل الاهتمامات المختارة معاً)
        available = PLACES_DB[st.session_state.user_budget]
        st.session_state.suggestions = [p for p in available if p['الفئة'] in u_interests]
        st.session_state.transport_choice = None

    if st.session_state.suggestions:
        st.markdown('<br><div class="highlight-box"><h4>🚕 كيف تفضل الوصول؟</h4></div>', unsafe_allow_html=True)
        t1, t2, t3 = st.columns(3)
        if all(p['metro'] for p in st.session_state.suggestions):
            if t1.button("🚇 المترو"): st.session_state.transport_choice = "metro"
        if t2.button("🚗 سيارتي"): st.session_state.transport_choice = "car"
        if t3.button("🚕 تاكسي"): st.session_state.transport_choice = "taxi"

        for p in st.session_state.suggestions:
            st.markdown(f'<div class="info-box"><h4>📍 {p["الوجهة"]}</h4><p>{p["وصف"]}</p><p>⏱️ الوقت: {p["time"]} دقيقة</p></div>', unsafe_allow_html=True)

    if st.button("🔄 إعادة ضبط"):
        st.session_state.clear()
        st.rerun()
