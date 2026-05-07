import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

# تحديد حالة الجو اللحظية بناءً على الساعة
if 5 <= current_hour <= 17:
    initial_weather = "مشمس ☀️"
else:
    initial_weather = "ليل صافي 🌙"

st.set_page_config(page_title="Path7 | Smart Journey", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS) - نسخة الحصن الحصين
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }
    .stApp { background-color: #F4F7F9 !important; }
    
    [data-testid="stForm"] {
        background: white !important;
        padding: 50px !important;
        border-radius: 30px !important;
        border-top: 18px solid #1A365D !important;
        box-shadow: 0 25px 60px rgba(0,0,0,0.12) !important;
        max-width: 650px !important;
        margin: auto !important;
    }
    [data-testid="stForm"] > div { border: none !important; }

    .main-card {
        background: white; padding: 25px; border-radius: 20px;
        border-top: 10px solid #1A365D; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .info-box {
        background: #EBF8FF; padding: 20px; border-radius: 15px;
        border-right: 6px solid #3182CE; margin-bottom: 20px;
    }
    .farewell-box {
        background: #F0FFF4; padding: 30px; border-radius: 20px;
        border: 2px dashed #38A169; text-align: center; margin-top: 25px;
    }
    .stButton>button { 
        border-radius: 15px; height: 3.5em; 
        background-color: #1A365D !important; 
        color: white !important; font-weight: bold !important; width: 100%;
    }
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    </style>
''', unsafe_allow_html=True)

# 3. إدارة الحالة (Session State)
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'dest' not in st.session_state: st.session_state.dest = None
if 'star_rating' not in st.session_state: st.session_state.star_rating = 0
if 'weather' not in st.session_state: st.session_state.weather = initial_weather

# --- المشهد الأول: صفحة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.form("main_welcome_form"):
        st.markdown('<h1 style="text-align: center; color: #1A365D; margin-bottom:0; font-size: 3em;">📍 Path7</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #718096; margin-top:5px; font-size: 1.2em;">نظام التوافق اللحظي للسياحة الذكية</p>', unsafe_allow_html=True)
        st.markdown('<hr style="margin: 30px 0; opacity: 0.1;">', unsafe_allow_html=True)
        u_name = st.text_input("اسم السائح الموقر", "جُمانة")
        u_budget = st.radio("حدد نوع الميزانية المرصودة للرحلة", ["اقتصادية", "فاخرة"], horizontal=True)
        st.info("📌 مكان الإقامة مثبت: حي المروج (نقطة الانطلاق)")
        if st.form_submit_button("بدء المسار الذكي 🚀"):
            st.session_state.user_name = u_name
            st.session_state.user_budget = u_budget
            st.session_state.page = 'system'
            st.rerun()

# --- المشهد الثاني: لوحة التحكم ---
else:
    col_main, col_stats = st.columns([2, 1])
    
    with col_main:
        st.markdown(f'''
            <div class="main-card">
                <h3 style="margin:0; color: #1A365D;">اليوم {st.session_state.current_day} من 3</h3>
                <p>مرحباً بك يا <b>{st.session_state.user_name}</b> | الجو الآن: <b>{st.session_state.weather}</b></p>
            </div>
        ''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("تحليل الوجهة الأنسب للوقت الحالي 🔍"):
            dests = ["بوليفارد وورلد (ترفيه)", "حي الطريف التاريخي (تاريخ)", "سوق الزل وقصر المصمك"]
            st.session_state.dest = dests[st.session_state.current_day - 1]
            st.session_state.traffic = random.randint(20, 60)
        
        if st.session_state.dest:
            st.markdown(f'''
                <div class="info-box">
                    <h4 style="margin:0; color:#2B6CB0;">📍 الوجهة: {st.session_state.dest}</h4>
                    <p style="margin-top:5px;">حالة الزحمة: <b>{st.session_state.traffic}%</b></p>
                </div>
            ''', unsafe_allow_html=True)
            
            transport = st.selectbox("اختر وسيلة النقل:", ["-- اختر --", "مترو الرياض (كافد)", "سيارتي الخاصة", "تاكسي"])
            if "مترو" in transport:
                st.info("🚇 المترو: وصول خلال 18 دقيقة.")
            elif "سيارتي" in transport:
                st.warning(f"🚗 السيارة: الوصول المتوقع خلال {25 + st.session_state.traffic//4} دقيقة.")

        st.markdown("<br><hr>")
        st.subheader("⭐ تقييمك لتجربة اليوم")
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐", key=f"s{i}"):
                st.session_state.star_rating = i
        
        if st.session_state.star_rating > 0:
            st.markdown(f"<h1 style='text-align: center; color: #FFD700;'>{'⭐' * st.session_state.star_rating}</h1>", unsafe_allow_html=True)
            
            if st.session_state.current_day < 3:
                if st.button("الانتقال لليوم التالي ⏩"):
                    st.session_state.current_day += 1
                    st.session_state.dest = None
                    st.session_state.star_rating = 0
                    # في المحاكاة، نغير الجو لعشوائي منطقي لليوم الجديد
                    st.session_state.weather = random.choice(["مشمس ☀️", "غائم جزئياً ⛅", "لطيف 🍃"])
                    st.rerun()
            else:
                st.markdown('''
                    <div class="farewell-box">
                        <h2 style="color: #2D3748; margin:0;">✨ وصلنا لنهاية الاجازة! نشوفك على خير ✨</h2>
                        <p style="margin-top:10px; color: #4A5568;">نتمنى أن تكون رحلتك في الرياض عبر Path7 كانت استثنائية ومريحة.</p>
                    </div>
                ''', unsafe_allow_html=True)

    with col_stats:
        st.subheader("⚙️ إدارة النظام")
        if st.button("🔄 إعادة ضبط"):
            st.session_state.clear()
            st.rerun()
        st.markdown(f"**توقيت الرياض اللحظي:** {now_riyadh.strftime('%I:%M %p')}")

st.markdown("<br><p style='text-align: center; color: #A0AEC0; font-size: 0.8em;'>Path7 | Engineering @ IAU</p>", unsafe_allow_html=True)
