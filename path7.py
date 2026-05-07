import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)

st.set_page_config(page_title="Path7 | Live Sync", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS)
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right; color: #2D3748 !important;
    }
    .stApp { background-color: #F8F9FB !important; }
    [data-testid="stForm"] {
        background: white !important; padding: 40px !important; border-radius: 25px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08) !important; border-top: 12px solid #1A365D !important;
        max-width: 750px; margin: auto;
    }
    .result-card {
        background: white; padding: 20px; border-radius: 15px;
        border-right: 8px solid #1A365D; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .sms-alert {
        background: #DCF8C6; padding: 15px; border-radius: 10px;
        border-right: 5px solid #25D366; margin-top: 10px; animation: pulse 2s infinite;
    }
    @keyframes pulse { 0% {opacity: 0.8;} 50% {opacity: 1;} 100% {opacity: 0.8;} }
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    </style>
''', unsafe_allow_html=True)

# 3. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'user_hotel' not in st.session_state: st.session_state.user_hotel = None
if 'dest_result' not in st.session_state: st.session_state.dest_result = None
if 'traffic_val' not in st.session_state: st.session_state.traffic_val = 0
if 'star_rating' not in st.session_state: st.session_state.star_rating = 0
if 'sms_sent' not in st.session_state: st.session_state.sms_sent = False

# --- المشهد الأول: البوكس الترحيبي ---
if st.session_state.page == 'welcome':
    col_l, col_m, col_r = st.columns([1, 6, 1])
    with col_m:
        with st.form("travel_form"):
            st.markdown('<h1 style="color: #1A365D; text-align: center;">📍 Path7</h1>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center;">أهلاً بكِ جُمانة.. حددي تفاصيل رحلتكِ</p>', unsafe_allow_html=True)
            st.markdown('---')
            u_name = st.text_input("اسم المسافر", "جُمانة")
            u_budget = st.radio("الميزانية", ["اقتصادية (Low)", "فاخرة (High)"], horizontal=True)
            
            hotels_list = {
                "اقتصادية (Low)": ["أجنحة المروج", "بودل المروج"],
                "فاخرة (High)": ["موفنبيك الرياض", "دبل تري"]
            }
            
            selected_hotel = st.selectbox("فندق الإقامة (حي المروج):", hotels_list[u_budget])
            u_interest = st.selectbox("الاهتمام اليوم:", ["تاريخ", "ترفيه", "طبيعة"])
            
            if st.form_submit_button("تثبيت البيانات وبدء الرحلة 🚀", use_container_width=True):
                st.session_state.user_name, st.session_state.user_budget = u_name, u_budget
                st.session_state.user_hotel, st.session_state.user_interest = selected_hotel, u_interest
                st.session_state.page = 'system'
                st.rerun()

# --- المشهد الثاني: النتائج والإشعارات ---
else:
    col_main, col_stats = st.columns([2, 1])
    
    with col_main:
        st.markdown(f'''
            <div class="result-card">
                <h3 style="margin:0; color:#1A365D;">🕒 توقيت الرياض: {now_riyadh.strftime("%I:%M %p")}</h3>
                <p>الفندق الحالي: <b>🏨 {st.session_state.user_hotel}</b></p>
            </div>
        ''', unsafe_allow_html=True)

        if st.button("تحليل الوجهة الأنسب 🔍", use_container_width=True):
            st.session_state.traffic_val = random.randint(20, 95)
            st.session_state.dest_result = random.choice(["قصر المصمك", "حي الطريف", "بوليفارد وورلد", "وادي حنيفة"])
            st.session_state.sms_sent = False # إعادة تعيين حالة الإشعار عند كل تحليل جديد

        if st.session_state.dest_result:
            st.success(f"📍 الوجهة المقترحة: {st.session_state.dest_result}")
            
            # --- ميزة إرسال الإشعار الجديدة ---
            st.markdown("---")
            st.subheader("📲 مزامنة المسار مع الجوال")
            col_sms1, col_sms2 = st.columns(2)
            
            with col_sms1:
                if st.button("إرسال عبر SMS 📱", use_container_width=True):
                    st.session_state.sms_sent = True
            
            with col_sms2:
                # رابط واتساب حقيقي يفتح رسالة جاهزة
                wa_msg = f"مرحباً جمانة، مسارك اللحظي إلى {st.session_state.dest_result} جاهز! الزحمة الحالية {st.session_state.traffic_val}%."
                wa_url = f"https://wa.me/?text={wa_msg}"
                st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; height:38px; background-color:#25D366; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold;">إرسال WhatsApp ✅</button></a>', unsafe_allow_html=True)

            if st.session_state.sms_sent:
                st.markdown(f'''
                    <div class="sms-alert">
                        <b>💬 إشعار جديد:</b><br>
                        تم إرسال رابط المسار اللحظي لرحلتك إلى {st.session_state.dest_result} بنجاح!
                    </div>
                ''', unsafe_allow_html=True)

    with col_stats:
        st.subheader("📊 مؤشرات")
        st.metric("الازدحام اللحظي", f"{st.session_state.traffic_val}%")
        if st.button("🔄 تغيير الفندق"):
            st.session_state.page, st.session_state.dest_result = 'welcome', None
            st.rerun()

        st.markdown("---")
        st.subheader("⭐ التقييم")
        s_cols = st.columns(5)
        for i in range(1, 6):
            if s_cols[i-1].button(f"{i}", key=f"s_{i}"): st.session_state.star_rating = i
        if st.session_state.star_rating > 0:
            st.markdown(f"<p style='text-align: center; font-size: 2em;'>{'⭐' * st.session_state.star_rating}</p>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #A0AEC0;'>Path7 | Engineering @ IAU</p>", unsafe_allow_html=True)
