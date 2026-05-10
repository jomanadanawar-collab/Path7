import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

st.set_page_config(page_title="Path7 | Smart Journey", layout="wide", initial_sidebar_state="collapsed")

# 2. تهيئة الجلسة
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'star_rating' not in st.session_state: st.session_state.star_rating = 0
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

# 3. CSS "البركات والحركات" - تصميم Glassmorphism الفاخر
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: rtl; text-align: right; }
    .stApp { background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%) !important; }

    /* الكارت الرئيسي بتأثير زجاجي */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 30px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }

    /* العناوين الملونة */
    .title-text { color: #0369A1; font-weight: 800; font-size: 2.8em; text-shadow: 2px 2px 4px rgba(0,0,0,0.05); }
    
    /* صناديق الوجهات المضيئة */
    .dest-card {
        background: white;
        padding: 20px;
        border-radius: 22px;
        border-right: 12px solid #38BDF8;
        box-shadow: 0 10px 20px rgba(0,0,0,0.02);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .dest-card:hover { transform: scale(1.02); box-shadow: 0 15px 30px rgba(2, 132, 199, 0.1); }

    /* الأزرار العصرية */
    .stButton>button {
        background: linear-gradient(45deg, #0284C7, #38BDF8) !important;
        color: white !important;
        border: none !important;
        border-radius: 18px !important;
        font-weight: 700 !important;
        height: 3.5em !important;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.2) !important;
        transition: 0.3s !important;
    }
    .stButton>button:hover { transform: translateY(-3px) !important; box-shadow: 0 8px 25px rgba(2, 132, 199, 0.4) !important; }

    /* إخفاء السايدبار */
    [data-testid="stSidebar"] { display: none !important; }
    </style>
''', unsafe_allow_html=True)

# --- الصفحة الأولى ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="glass-card" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown('<h1 class="title-text">📍 Path7</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 1.4em; color: #64748B;">التخطيط الهندسي.. لرحلة سياحية لا تُنسى</p>', unsafe_allow_html=True)
        
        col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
        with col_c2:
            u_name = st.text_input("بمَ نناديكِ يا جُمانة؟", "جُمانة")
            u_budget = st.select_slider("ميزانية الرحلة", options=["اقتصادية", "متوازنة", "فاخرة"])
            if st.button("لنبدأ المسار 🚀"):
                st.session_state.user_name = u_name
                st.session_state.user_budget = u_budget
                st.session_state.page = 'system'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الثانية ---
else:
    col_main, col_stats = st.columns([2.5, 1])
    
    with col_main:
        st.markdown(f'''
            <div class="glass-card">
                <h2 style="color: #0369A1; margin:0;">🗓️ اليوم {st.session_state.current_day} من 3</h2>
                <p style="font-size: 1.1em; color: #475569;">مرحباً <b>{st.session_state.user_name}</b> | النمط المختارة: {st.session_state.user_budget}</p>
            </div>
        ''', unsafe_allow_html=True)

        st.markdown("### 🌟 اهتماماتك لهذا اليوم")
        interests = st.multiselect("", ["تاريخ", "ترفيه", "طبيعة", "تسوق"], label_visibility="collapsed")
        
        if st.button("رسم المسار الذكي 🔍"):
            st.session_state.suggestions = [{"name": "حي الطريف", "desc": "عبق التاريخ واليونسكو.", "time": 20}]
            st.session_state.transport_choice = None

        if st.session_state.suggestions:
            st.markdown("### 🚕 وسيلة الوصول")
            t_col = st.columns(3)
            if t_col[0].button("🚇 مترو"): st.session_state.transport_choice = "مترو"
            if t_col[1].button("🚗 سيارة"): st.session_state.transport_choice = "سيارة"
            if t_col[2].button("🚕 تاكسي"): st.session_state.transport_choice = "تاكسي"

            for p in st.session_state.suggestions:
                st.markdown(f'''
                    <div class="dest-card">
                        <h4 style="color:#0284C7; margin:0;">📍 {p["name"]}</h4>
                        <p style="color:#64748B;">{p["desc"]}</p>
                        <hr style="opacity:0.1">
                        <p style="font-weight:bold; color:#0369A1;">⏱️ وصول متوقع: {p["time"] if not st.session_state.transport_choice else p["time"]+5} دقيقة</p>
                    </div>
                ''', unsafe_allow_html=True)

    with col_stats:
        st.markdown('<div class="glass-card" style="padding: 20px;">', unsafe_allow_html=True)
        st.subheader("⭐ التقييم")
        s_cols = st.columns(5)
        for i in range(1, 6):
            if s_cols[i-1].button(f"{i}⭐", key=f"star_{i}"):
                st.session_state.star_rating = i
                st.toast(f"شكراً لتقييمك يا {st.session_state.user_name}!", icon="✨")
        
        if st.session_state.star_rating > 0:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("اليوم التالي ⏩"):
                st.session_state.current_day += 1
                st.session_state.suggestions = []
                st.session_state.star_rating = 0
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 تصفير"): st.session_state.clear(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #94A3B8; margin-top: 50px;'>Path7 | Engineering Perfection</p>", unsafe_allow_html=True)
