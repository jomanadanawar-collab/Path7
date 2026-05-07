import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)

st.set_page_config(page_title="Path7 | Smart Journey", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS) - تصميم هندسي نظيف
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }
    .stApp { background-color: #F4F7F9 !important; }
    
    /* كارت الصفحة الرئيسية */
    .main-card {
        background: white; padding: 35px; border-radius: 25px;
        border-top: 12px solid #1A365D; box-shadow: 0 15px 35px rgba(0,0,0,0.07);
        margin-bottom: 25px;
    }
    
    /* كارت التنبيهات والنتائج */
    .info-box {
        background: #EBF8FF; padding: 20px; border-radius: 15px;
        border-right: 6px solid #3182CE; margin-bottom: 20px;
    }
    
    .farewell-box {
        background: #F0FFF4; padding: 30px; border-radius: 20px;
        border: 2px dashed #38A169; text-align: center; margin-top: 25px;
    }
    
    .day-badge {
        background: #1A365D; color: white; padding: 6px 18px; border-radius: 30px; font-weight: bold;
    }
    
    /* إخفاء القوائم الجانبية لتركيز اللجنة على المحتوى */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    </style>
''', unsafe_allow_html=True)

# 3. إدارة الحالة (Session State)
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'dest' not in st.session_state: st.session_state.dest = None
if 'star_rating' not in st.session_state: st.session_state.star_rating = 0

# --- المشهد الأول: صفحة الدخول ---
if st.session_state.page == 'welcome':
    col_l, col_m, col_r = st.columns([1, 4, 1])
    with col_m:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align: center; color: #1A365D; margin-bottom:0;">📍 Path7</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #718096;">نظام التوافق اللحظي للسياحة الذكية</p>', unsafe_allow_html=True)
        st.markdown('<hr>', unsafe_allow_html=True)
        
        with st.form("booking_form"):
            st.session_state.user_name = st.text_input("اسم السائح", "جُمانة")
            st.session_state.user_budget = st.radio("نوع الميزانية", ["اقتصادية", "فاخرة"], horizontal=True)
            st.info("📍 الفندق المختار: حي المروج (نقطة الانطلاق)")
            
            if st.form_submit_button("بدء المسار الذكي 🚀", use_container_width=True):
                st.session_state.page = 'system'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- المشهد الثاني: لوحة التحكم والنتائج ---
else:
    col_main, col_stats = st.columns([2, 1])
    
    with col_main:
        # الهيدر اللحظي
        st.markdown(f'''
            <div class="main-card" style="padding: 25px;">
                <span class="day-badge">اليوم {st.session_state.current_day} من 3</span>
                <h3 style="margin:15px 0 5px 0; color: #1A365D;">🕒 توقيت الرياض: {now_riyadh.strftime("%I:%M %p")}</h3>
                <p style="color: #4A5568;">مرحباً بك يا <b>{st.session_state.user_name}</b>، نظام Path7 يرافقك في رحلتك.</p>
            </div>
        ''', unsafe_allow_html=True)

        # زر التقويم
        if st.button("🔗 ربط بـ Google Calendar", use_container_width=True):
            st.success("تمت المزامنة بنجاح! سيصلك إشعار غداً صباحاً.")
            st.balloons()

        st.markdown("<br>", unsafe_allow_html=True)
        
        # تحليل الوجهة
        if st.button("تحليل الوجهة الأنسب للوقت الحالي 🔍", use_container_width=True):
            dests = ["بوليفارد وورلد (ترفيه)", "حي الطريف التاريخي (تاريخ)", "سوق الزل وقصر المصمك"]
            st.session_state.dest = dests[st.session_state.current_day - 1]
            st.session_state.traffic = random.randint(20, 60)
        
        if st.session_state.dest:
            st.markdown(f'''
                <div class="info-box">
                    <h4 style="margin:0; color:#2B6CB0;">📍 الوجهة المقترحة: {st.session_state.dest}</h4>
                    <p style="margin:10px 0 0 0; font-size: 0.9em;">نسبة الزحمة في الطريق من حي المروج: <b>{st.session_state.traffic}%</b></p>
                </div>
            ''', unsafe_allow_html=True)
            
            transport = st.selectbox("اختر وسيلة النقل المناسبة:", ["-- اختر --", "مترو الرياض (كافد)", "تاكسي"])
            if "مترو" in transport:
                st.info("🚇 المترو هو الخيار الأسرع حالياً (وصول خلال 18 دقيقة).")
            elif "تاكسي" in transport:
                st.warning(f"🚕 الوصول المتوقع خلال {20 + st.session_state.traffic//5} دقيقة.")

        # التقييم والوداع
        st.markdown("<br><hr>")
        st.subheader("⭐ تقييمك لتجربة اليوم")
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐", key=f"s{i}"):
                st.session_state.star_rating = i
        
        if st.session_state.star_rating > 0:
            st.markdown(f"<h1 style='text-align: center; color: #FFD700;'>{'⭐' * st.session_state.star_rating}</h1>", unsafe_allow_html=True)
            
            if st.session_state.current_day == 3:
                st.markdown('''
                    <div class="farewell-box">
                        <h2 style="color: #2D3748; margin:0;">✨ وصلنا لنهاية الاجازة! نشوفك على خير ✨</h2>
                        <p style="margin-top:10px; color: #4A5568;">نتمنى أن تكون رحلتك في الرياض عبر Path7 كانت استثنائية ومريحة.</p>
                    </div>
                ''', unsafe_allow_html=True)

    with col_stats:
        st.subheader("⚙️ محاكاة")
        if st.button("⏩ اليوم التالي"):
            if st.session_state.current_day < 3:
                st.session_state.current_day += 1
                st.session_state.dest = None
                st.session_state.star_rating = 0
                st.rerun()
        
        if st.session_state.current_day == 2:
            st.warning("🔔 تنبيه الصباح: هاه لسا بالرياض؟ اليوم الجو جميل!")

        if st.button("🔄 إعادة ضبط"):
            st.session_state.clear()
            st.rerun()

st.markdown("<br><p style='text-align: center; color: #A0AEC0; font-size: 0.8em;'>Path7 | Engineering @ IAU</p>", unsafe_allow_html=True)
