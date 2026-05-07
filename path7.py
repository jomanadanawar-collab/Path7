import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)

st.set_page_config(page_title="Path7 | Smart Journey", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS) - النسخة المحصنة
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }
    .stApp { background-color: #F4F7F9 !important; }
    
    /* التصميم الجديد للصندوق بحيث يحتوي كل شيء برمجياً */
    .stColumn > div > div > div > div {
        background: white;
        padding: 40px !important;
        border-radius: 30px !important;
        border-top: 18px solid #1A365D !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.1) !important;
    }

    .farewell-box {
        background: #F0FFF4; padding: 30px; border-radius: 20px;
        border: 2px dashed #38A169; text-align: center; margin-top: 25px;
    }

    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    
    /* تمييز الأزرار */
    .stButton>button { 
        border-radius: 15px; height: 3.5em; 
        background-color: #1A365D !important; 
        color: white !important; font-weight: bold !important; width: 100%;
    }
    </style>
''', unsafe_allow_html=True)

# 3. إدارة الحالة (Session State)
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'dest' not in st.session_state: st.session_state.dest = None
if 'star_rating' not in st.session_state: st.session_state.star_rating = 0

# --- المشهد الأول: صفحة الترحيب ---
if st.session_state.page == 'welcome':
    # نستخدم Columns لتوسيط البوكس في الشاشة
    empty_l, mid_col, empty_r = st.columns([1, 2, 1])
    
    with mid_col:
        # هنا استخدمنا حاوية Streamlit اللي ربطناها بالـ CSS فوق
        with st.container():
            st.markdown('<h1 style="text-align: center; color: #1A365D; margin-bottom:0; font-size: 3em;">📍 Path7</h1>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; color: #718096; margin-top:5px; font-size: 1.2em;">نظام التوافق اللحظي للسياحة الذكية</p>', unsafe_allow_html=True)
            st.markdown('<hr style="margin: 25px 0; opacity: 0.2;">', unsafe_allow_html=True)
            
            with st.form("main_form"):
                u_name = st.text_input("اسم السائح الموقر", "جُمانة")
                st.markdown("<br>", unsafe_allow_html=True)
                u_budget = st.radio("حدد نوع الميزانية المرصودة للرحلة", ["اقتصادية", "فاخرة"], horizontal=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.info("📌 مكان الإقامة مثبت: حي المروج")
                
                # زر البدء
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
        with st.container():
            st.markdown(f'''
                <h3 style="color: #1A365D;">اليوم {st.session_state.current_day} من 3</h3>
                <p>مرحباً بك يا <b>{st.session_state.user_name}</b></p>
            ''', unsafe_allow_html=True)

            if st.button("🔗 ربط بـ Google Calendar"):
                st.success("تمت المزامنة!")
                st.balloons()

            st.markdown("---")
            if st.button("تحليل الوجهة الأنسب 🔍"):
                dests = ["بوليفارد وورلد", "حي الطريف", "سوق الزل"]
                st.session_state.dest = dests[st.session_state.current_day - 1]
            
            if st.session_state.dest:
                st.info(f"📍 الوجهة: {st.session_state.dest}")

            st.markdown("<br><hr>")
            st.subheader("⭐ تقييم التجربة")
            stars = st.columns(5)
            for i in range(1, 6):
                if stars[i-1].button(f"{i}⭐", key=f"s{i}"): st.session_state.star_rating = i
            
            if st.session_state.star_rating > 0 and st.session_state.current_day == 3:
                st.markdown('<div class="farewell-box"><h2>✨ وصلنا لنهاية الاجازة! نشوفك على خير ✨</h2></div>', unsafe_allow_html=True)

    with col_stats:
        if st.button("⏩ اليوم التالي"):
            if st.session_state.current_day < 3:
                st.session_state.current_day += 1
                st.session_state.dest = None
                st.session_state.star_rating = 0
                st.rerun()
        if st.button("🔄 إعادة ضبط"):
            st.session_state.clear()
            st.rerun()

st.markdown("<br><p style='text-align: center; color: #A0AEC0;'>Path7 | Engineering @ IAU</p>", unsafe_allow_html=True)
