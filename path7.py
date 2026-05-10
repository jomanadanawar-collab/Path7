import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. الإعدادات
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'star_rating' not in st.session_state: st.session_state.star_rating = 0
if 'transport' not in st.session_state: st.session_state.transport = None

# 3. الـ "ستايل" الفخم (مستوحى من صورك)
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: rtl; text-align: right; }
    .stApp { background-color: #FFFFFF !important; }

    /* الهيدر النظيف */
    .header-box {
        background: #F8FAFC;
        padding: 2rem;
        border-radius: 20px;
        border-bottom: 5px solid #0EA5E9;
        margin-bottom: 2rem;
    }

    /* الكروت "الرشيقة" */
    .card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-right: 6px solid #0EA5E9;
    }

    /* الأزرار الاحترافية */
    .stButton>button {
        background-color: #0EA5E9 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 0.6rem 1rem !important;
        font-weight: 600 !important;
        transition: 0.2s;
    }
    .stButton>button:hover { background-color: #0284C7 !important; transform: translateY(-1px); }

    /* إخفاء الزوائد */
    [data-testid="stSidebar"] { display: none !important; }
    </style>
''', unsafe_allow_html=True)

# 4. محتوى الصفحات
if st.session_state.page == 'welcome':
    st.markdown('<div class="header-box" style="text-align:center;">', unsafe_allow_html=True)
    st.title("📍 Path7 | Smart Journey")
    st.write("نظام التوافق اللحظي للسياحة الذكية")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        u_name = st.text_input("الاسم", "جُمانة")
        u_budget = st.selectbox("الميزانية", ["اقتصادية", "فاخرة"])
        if st.button("بدء المسار"):
            st.session_state.u_name = u_name
            st.session_state.u_budget = u_budget
            st.session_state.page = 'system'
            st.rerun()

else:
    # الصفحة الرئيسية للنظام
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.markdown(f'''<div class="header-box">
            <h3>اليوم {st.session_state.current_day} من 3 | مرحباً {st.session_state.u_name}</h3>
            <p style="color: #64748B;">الجو في الرياض: <b>مشمس ☀️</b></p>
        </div>''', unsafe_allow_html=True)

        st.subheader("🌟 اهتماماتك المفضلة")
        st.multiselect("", ["تاريخ وآثار", "ترفيه", "طبيعة"], label_visibility="collapsed")
        
        if st.button("تحليل الوجهات"):
            st.session_state.suggestions = [{"name": "حصن المصمك", "desc": "معلم تاريخي بارز", "time": 25}]
        
        if st.session_state.suggestions:
            st.markdown("---")
            st.write("🚕 اختر وسيلة النقل:")
            t_cols = st.columns(3)
            if t_cols[0].button("🚇 مترو"): st.session_state.transport = "مترو"
            if t_cols[1].button("🚗 سيارة"): st.session_state.transport = "سيارة"
            if t_cols[2].button("🚕 تاكسي"): st.session_state.transport = "تاكسي"

            for p in st.session_state.suggestions:
                st.markdown(f'''<div class="card">
                    <h4 style="margin:0; color:#0369A1;">📍 {p["name"]}</h4>
                    <p style="color:#64748B; font-size:0.9em;">{p["desc"]}</p>
                    <p style="font-weight:bold; color:#0EA5E9; margin-top:10px;">⏱️ الوقت: {p["time"]} دقيقة</p>
                </div>''', unsafe_allow_html=True)

    with col_side:
        st.markdown('<div class="header-box">', unsafe_allow_html=True)
        st.subheader("⭐ التقييم")
        stars = st.columns(5)
        for i in range(5):
            if stars[i].button(f"{i+1}"): st.session_state.star_rating = i+1
        
        if st.session_state.star_rating > 0:
            if st.button("اليوم التالي ➡️"):
                st.session_state.current_day += 1
                st.session_state.suggestions = []
                st.session_state.star_rating = 0
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#94A3B8; margin-top:3rem;'>Path7 | Engineering Excellence @ IAU</p>", unsafe_allow_html=True)
