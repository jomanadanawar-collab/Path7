import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)

st.set_page_config(page_title="Path7 | Smart Journey", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS)
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }
    .stApp { background-color: #F8FAFC !important; }
    .main-card {
        background: white; padding: 30px; border-radius: 20px;
        border-top: 10px solid #1A365D; box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .farewell-box {
        background: #E2E8F0; padding: 25px; border-radius: 15px;
        border: 2px solid #1A365D; text-align: center; margin-top: 20px;
    }
    .day-badge {
        background: #1A365D; color: white; padding: 5px 15px; border-radius: 20px;
    }
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    </style>
''', unsafe_allow_html=True)

# 3. إدارة الحالة (Session State)
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'dest' not in st.session_state: st.session_state.dest = None
if 'star_rating' not in st.session_state: st.session_state.star_rating = 0

# --- المشهد الأول: صفحة الحجز ---
if st.session_state.page == 'welcome':
    col_l, col_m, col_r = st.columns([1, 4, 1])
    with col_m:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align: center; color: #1A365D;">📍 Path7</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center;">نظام التوافق اللحظي - حي المروج</p>', unsafe_allow_html=True)
        
        with st.form("booking_form"):
            st.session_state.user_name = st.text_input("اسم السائح", "جُمانة")
            st.session_state.user_budget = st.radio("الميزانية", ["اقتصادية", "فاخرة"], horizontal=True)
            st.info("📍 الفندق المثبت: حي المروج (نقطة الانطلاق)")
            
            if st.form_submit_button("تفعيل المسار الذكي 🚀", use_container_width=True):
                st.session_state.page = 'system'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- المشهد الثاني: لوحة التحكم ---
else:
    col_main, col_stats = st.columns([2, 1])
    
    with col_main:
        st.markdown(f'''
            <div class="main-card" style="padding: 20px;">
                <span class="day-badge">اليوم {st.session_state.current_day} من 3</span>
                <h3 style="margin:10px 0; color: #1A365D;">🕒 الرياض: {now_riyadh.strftime("%I:%M %p")}</h3>
                <p>مرحباً بك يا <b>{st.session_state.user_name}</b>، نظام Path7 يرافقك في رحلتك.</p>
            </div>
        ''', unsafe_allow_html=True)

        if st.button("🔗 ربط بـ Google Calendar", use_container_width=True):
            st.success("تمت المزامنة بنجاح! سيصلك إشعار غداً صباحاً.")
            st.balloons()

        st.markdown("---")
        
        # تحليل الوجهة
        if st.button("تحليل الوجهة الأنسب لليوم 🔍", use_container_width=True):
            dests = ["بوليفارد وورلد", "حي الطريف التاريخي", "سوق الزل"]
            st.session_state.dest = dests[st.session_state.current_day - 1]
        
        if st.session_state.dest:
            st.success(f"📍 الوجهة المقترحة: {st.session_state.dest}")
            transport = st.selectbox("وسيلة النقل:", ["-- اختر --", "مترو الرياض", "تاكسي"])
            if transport != "-- اختر --":
                st.info("🚇 تم تحديد المسار الأسرع من حي المروج.")

        st.markdown("<br>---")
        st.subheader("⭐ تقييمك لتجربة اليوم")
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐", key=f"star_{i}"):
                st.session_state.star_rating = i
        
        # عرض رسالة الوداع عند التقييم في اليوم الأخير
        if st.session_state.star_rating > 0:
            st.markdown(f"<h1 style='text-align: center; color: #FFD700;'>{'⭐' * st.session_state.star_rating}</h1>", unsafe_allow_html=True)
            
            if st.session_state.current_day == 3:
                st.markdown('''
                    <div class="farewell-box">
                        <h2 style="color: #1A365D; margin:0;">✨ وصلنا لنهاية الاجازة! نشوفك على خير ✨</h2>
                        <p style="margin-top:10px;">نتمنى أن تكون رحلتك في الرياض عبر Path7 كانت استثنائية.</p>
                    </div>
                ''', unsafe_allow_html=True)

    with col_stats:
        st.subheader("إدارة السيناريو")
        if st.button("⏩ اليوم التالي"):
            if st.session_state.current_day < 3:
                st.session_state.current_day += 1
                st.session_state.dest = None
                st.session_state.star_rating = 0
                st.rerun()
        
        if st.session_state.current_day == 2:
            st.warning("🔔 تذكير اليوم الثاني: هاه لسا بالرياض؟")

        if st.button("🔄 تصفير الحجز"):
            st.session_state.clear()
            st.rerun()

st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.8em;'>Path7 | Engineering @ IAU</p>", unsafe_allow_html=True)
