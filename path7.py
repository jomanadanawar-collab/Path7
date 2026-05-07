import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)

st.set_page_config(page_title="Path7 | Smart Tourism", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS)
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }
    .stApp { background-color: #F4F7F9 !important; }
    .main-card {
        background: white; padding: 30px; border-radius: 20px;
        border-top: 10px solid #1A365D; box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .calendar-sync {
        background: #E8F0FE; padding: 15px; border-radius: 12px;
        border: 1px solid #4285F4; color: #1967D2; margin-top: 15px;
    }
    .day-badge {
        background: #1A365D; color: white; padding: 5px 15px;
        border-radius: 20px; font-size: 0.8em;
    }
    .update-box {
        background: #FFF9C4; padding: 15px; border-radius: 12px;
        border: 1px solid #FBC02D; margin-bottom: 20px;
    }
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    </style>
''', unsafe_allow_html=True)

# 3. إدارة الحالة (Session State)
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'star_rating' not in st.session_state: st.session_state.star_rating = 0
if 'dest' not in st.session_state: st.session_state.dest = None

# --- المشهد الأول: صفحة الحجز ---
if st.session_state.page == 'welcome':
    col_l, col_m, col_r = st.columns([1, 4, 1])
    with col_m:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align: center; color: #1A365D;">🔗 Path7 📍</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #64748b;">نظام التوافق اللحظي للسياحة الذكية</p>', unsafe_allow_html=True)
        
        with st.form("booking_form"):
            u_name = st.text_input("اسم السائح", "جُمانة")
            u_budget = st.radio("فئة الميزانية", ["اقتصادية (Low)", "فاخرة (High)"], horizontal=True)
            st.info("📍 مكان الإقامة المثبت: حي المروج (شمال الرياض)")
            
            if st.form_submit_button("تفعيل المسار السياحي الذكي 🚀", use_container_width=True):
                st.session_state.user_name = u_name
                st.session_state.user_budget = u_budget
                st.session_state.page = 'system'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- المشهد الثاني: لوحة النتائج ---
else:
    col_main, col_stats = st.columns([2, 1])
    
    with col_main:
        st.markdown(f'''
            <div class="main-card" style="padding: 20px;">
                <span class="day-badge">اليوم {st.session_state.current_day} من 3</span>
                <h3 style="margin:10px 0; color: #1A365D;">🕒 توقيت الرياض: {now_riyadh.strftime("%I:%M %p")}</h3>
                <p>مرحباً <b>{st.session_state.user_name}</b>، نظام Path7 جاهز للمزامنة.</p>
            </div>
        ''', unsafe_allow_html=True)

        # زر جوجل كالندر
        if st.button("🔗 ربط بـ Google Calendar (تفعيل التنبيهات)", use_container_width=True):
            st.markdown(f'''
                <div class="calendar-sync">
                    <b>📅 تم الربط بنجاح!</b><br>
                    سيصلك إشعار غداً صباحاً بمسار اليوم الجديد بناءً على الزحمة اللحظية.
                </div>
            ''', unsafe_allow_html=True)
            st.balloons()

        st.markdown("---")
        
        if st.session_state.current_day == 2:
            st.markdown('<div class="update-box"><b>🔔 إشعار متابعة:</b><br>هاه لسا جالتنا بالرياض؟ اليوم الجو مثالي لحي الطريف!</div>', unsafe_allow_html=True)

        if st.button("تحليل الوجهة الأنسب بناءً على الزحمة 🔍", use_container_width=True):
            destinations = ["بوليفارد وورلد", "حي الطريف التاريخي", "سوق الزل وقصر المصمك"]
            st.session_state.dest = destinations[st.session_state.current_day - 1]
            st.session_state.traffic = random.randint(20, 60)
        
        if st.session_state.dest:
            st.success(f"📍 الوجهة المقترحة لليوم: {st.session_state.dest}")
            transport = st.selectbox("وسيلة النقل:", ["-- اختر --", "مترو الرياض (كافد)", "تاكسي"])
            if "مترو" in transport:
                st.info("🚇 الوصول خلال 18 دقيقة (مسار سالك).")
            elif "تاكسي" in transport:
                st.warning(f"🚕 الوصول خلال {20 + st.session_state.traffic//5} دقيقة.")

        st.markdown("<br>---")
        st.subheader("⭐ تقييمك")
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐", key=f"s{i}"): st.session_state.star_rating = i
        if st.session_state.star_rating > 0:
            st.markdown(f"<h1 style='text-align: center; color: #FFD700;'>{'⭐' * st.session_state.star_rating}</h1>", unsafe_allow_html=True)

    with col_stats:
        st.subheader("⚙️ الإدارة")
        if st.button("⏩ اليوم التالي"):
            if st.session_state.current_day < 3:
                st.session_state.current_day += 1
                st.session_state.dest = None
                st.rerun()
        if st.button("🔄 تصفير"):
            st.session_state.clear()
            st.rerun()
