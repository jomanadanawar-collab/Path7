import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)

st.set_page_config(page_title="Path7 | Smart Journey", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS) - النسخة "الحصن الحصين"
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }
    .stApp { background-color: #F4F7F9 !important; }
    
    /* تصميم الفورم ليصبح هو البوكس الواحد الموحد */
    [data-testid="stForm"] {
        background: white !important;
        padding: 50px !important;
        border-radius: 30px !important;
        border-top: 18px solid #1A365D !important;
        box-shadow: 0 25px 60px rgba(0,0,0,0.12) !important;
        max-width: 650px !important;
        margin: auto !important;
        border-left: none !important;
        border-right: none !important;
        border-bottom: none !important;
    }

    /* إخفاء الحدود الافتراضية للفورم */
    [data-testid="stForm"] > div { border: none !important; }

    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    
    /* تنسيق الأزرار */
    .stButton>button { 
        border-radius: 15px; height: 3.8em; 
        background-color: #1A365D !important; 
        color: white !important; font-weight: bold !important; width: 100%;
        margin-top: 20px;
    }
    </style>
''', unsafe_allow_html=True)

# 3. إدارة الحالة (Session State)
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'dest' not in st.session_state: st.session_state.dest = None
if 'star_rating' not in st.session_state: st.session_state.star_rating = 0

# --- المشهد الأول: صفحة الترحيب (البوكس الواحد المطلق) ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # كل شيء داخل الفورم = كل شيء داخل البوكس الكحلي
    with st.form("ultimate_unified_form"):
        # العنوان والوصف داخل البوكس
        st.markdown('<h1 style="text-align: center; color: #1A365D; margin-bottom:0; font-size: 3em;">📍 Path7</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #718096; margin-top:5px; font-size: 1.2em;">نظام التوافق اللحظي للسياحة الذكية</p>', unsafe_allow_html=True)
        st.markdown('<hr style="margin: 30px 0; opacity: 0.1;">', unsafe_allow_html=True)
        
        # المدخلات
        u_name = st.text_input("اسم السائح الموقر", "جُمانة")
        st.markdown("<br>", unsafe_allow_html=True)
        u_budget = st.radio("حدد نوع الميزانية المرصودة للرحلة", ["اقتصادية", "فاخرة"], horizontal=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("📌 مكان الإقامة مثبت: حي المروج (نقطة الانطلاق)")
        
        # الزر (نهايته هي نهاية البوكس)
        submit = st.form_submit_button("بدء المسار الذكي 🚀")
        
        if submit:
            st.session_state.user_name = u_name
            st.session_state.user_budget = u_budget
            st.session_state.page = 'system'
            st.rerun()

# --- المشهد الثاني: لوحة التحكم ---
else:
    col_main, col_stats = st.columns([2, 1])
    with col_main:
        st.markdown(f'''
            <div style="background: white; padding: 25px; border-radius: 20px; border-top: 10px solid #1A365D; box-shadow: 0 10px 30px rgba(0,0,0,0.05);">
                <h3 style="color: #1A365D;">اليوم {st.session_state.current_day} من 3</h3>
                <p>مرحباً بك يا <b>{st.session_state.user_name}</b></p>
            </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("تحليل الوجهة الأنسب 🔍"):
            dests = ["بوليفارد وورلد", "حي الطريف", "سوق الزل"]
            st.session_state.dest = dests[st.session_state.current_day - 1]
        
        if st.session_state.dest:
            st.success(f"📍 الوجهة المقترحة: {st.session_state.dest}")

    with col_stats:
        if st.button("⏩ اليوم التالي"):
            if st.session_state.current_day < 3:
                st.session_state.current_day += 1
                st.session_state.dest = None
                st.rerun()
        if st.button("🔄 إعادة ضبط"):
            st.session_state.clear()
            st.rerun()

st.markdown("<br><p style='text-align: center; color: #A0AEC0;'>Path7 | Engineering @ IAU</p>", unsafe_allow_html=True)
