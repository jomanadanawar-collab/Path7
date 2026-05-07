import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. ضبط التوقيت
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

# 2. إعدادات الصفحة
st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# 3. CSS احترافي (تركيز كامل على الدائرة الكحلية وتنسيق البوكس)
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right; color: #2D3748 !important;
    }
    .stApp { background-color: #F8F9FB !important; }

    /* البوكس الكحلي الترحيبي (الفورم) */
    [data-testid="stForm"] {
        background: white !important;
        padding: 30px !important;
        border-radius: 25px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08) !important;
        border-top: 12px solid #1A365D !important;
        border-left: none !important; border-right: none !important; border-bottom: none !important;
        max-width: 650px; margin: auto;
    }

    /* === إجبار الدائرة والخط على اللون الكحلي ومنع الأحمر تماماً === */
    /* الدائرة (المقبض) */
    div[role="slider"] {
        background-color: #1A365D !important;
        border: 3px solid #FFFFFF !important;
        box-shadow: 0 2px 8px rgba(26, 54, 93, 0.5) !important;
        width: 26px !important; height: 26px !important;
        cursor: pointer !important;
    }
    /* الخط النشط (الذي يتم سحبه) */
    div[data-baseweb="slider"] div[style*="background-color: rgb(255, 75, 75)"],
    div[data-baseweb="slider"] div[style*="background-color: rgb(255, 131, 131)"],
    div[data-baseweb="slider"] > div > div > div {
        background-color: #1A365D !important;
    }
    /* إخفاء أي خطوط حمراء عند الأطراف */
    div[data-baseweb="slider"] > div::before, div[data-baseweb="slider"] > div::after {
        background-color: #1A365D !important;
    }
    
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    </style>
''', unsafe_allow_html=True)

# 4. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'dest_result' not in st.session_state: st.session_state.dest_result = None
if 'traffic_val' not in st.session_state: st.session_state.traffic_val = None

# --- الصفحة الأولى: البوكس الكحلي ---
if st.session_state.page == 'welcome':
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        with st.form("welcome_form"):
            st.markdown('<h1 style="color: #1A365D; text-align: center;">📍 Path7</h1>', unsafe_allow_html=True)
            st.markdown('<p style="font-size: 1.1em; text-align: center;">مرحباً بك في دليلك الذكي لاستكشاف الرياض.</p>', unsafe_allow_html=True)
            st.markdown('---')
            u_name = st.text_input("الاسم", "زائر")
            u_interest = st.selectbox("الاهتمام", ["تاريخ", "ترفيه", "طبيعة"])
            u_budget = st.radio("الميزانية", ["اقتصادية (Low)", "فاخرة (High)"], horizontal=True)
            submit = st.form_submit_button("توليد المسار اللحظي 🚀", use_container_width=True)
            if submit:
                st.session_state.user_name, st.session_state.user_interest, st.session_state.user_budget = u_name, u_interest, u_budget
                st.session_state.page, st.session_state.dest_result = 'system', None
                st.rerun()

# --- الصفحة الثانية: النتائج ---
else:
    c1, c2 = st.columns([5, 1])
    with c1: st.markdown("<h2>📍 تحليل المسار اللحظي</h2>", unsafe_allow_html=True)
    with c2: 
        if st.button("🔄 تعديل"): 
            st.session_state.page = 'welcome'
            st.rerun()

    col_main, col_stats = st.columns([2, 1])
    with col_main:
        st.markdown(f'<div style="background: white; padding: 20px; border-radius: 15px; border-right: 8px solid #1A365D; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;"><h3>أهلاً بك {st.session_state.user_name} ✨</h3><p>توقيت الرياض: {now_riyadh.strftime("%I:%M %p")}</p></div>', unsafe_allow_html=True)

        if st.button("تحديث وتحليل الوجهة"):
            destinations = {"تاريخ": {"Low": ["قصر المصمك"], "High": ["حي الطريف"]}, "ترفيه": {"Low": ["حديقة السويدي"], "High": ["بوليفارد وورلد"]}, "طبيعة": {"Low": ["وادي حنيفة"], "High": ["منتجع نوفا"]}}
            b_key = "Low" if "اقتصادية" in st.session_state.user_budget else "High"
            st.session_state.dest_result = random.choice(destinations[st.session_state.user_interest][b_key])
            st.session_state.traffic_val = random.randint(15, 95)

        if st.session_state.dest_result:
            st.info(f"📍 الوجهة المقترحة: {st.session_state.dest_result}")
            st.metric("نسبة الازدحام", f"{st.session_state.traffic_val}%")

        st.markdown("---")
        # حل مشكلة دقة النجوم: عرض القيم من 1 لـ 5 وضمان تطابقها
        rating = st.select_slider("قيم تجربتك (اسحب الدائرة الكحلية):", options=[1, 2, 3, 4, 5], value=5)
        # عرض النجوم بناءً على الرقم المختار فعلياً
        st.markdown(f"<h1 style='text-align: center; color: #FFD700;'>{'⭐' * rating}</h1>", unsafe_allow_html=True)

    with col_stats:
        st.subheader("📊 مؤشرات")
        st.metric("الطقس", "صافي", "☀️")
        st.metric("الحالة", "نشط")

st.markdown("<br><p style='text-align: center; color: #A0AEC0; font-size: 0.8em;'>Path7 | IAU Engineering</p>", unsafe_allow_html=True)
