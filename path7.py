import streamlit as st
import random
import json
from datetime import datetime
import pytz

# --- وظيفة لقراءة ملف JSON ---
def load_data():
    with open('path7_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

DATA_ALL = load_data()

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
formatted_time = now_riyadh.strftime('%I:%M %p')
current_hour = now_riyadh.hour

st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (Session State)
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'day' not in st.session_state: st.session_state.day = 1
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'rated' not in st.session_state: st.session_state.rated = False
if 'suggestions' not in st.session_state: st.session_state.suggestions = []

# اختيار القاموس بناءً على اللغة من الملف المحمل
T = DATA_ALL[st.session_state.lang]

# 3. الستايل البصري (لم يتغير)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if st.session_state.lang == "العربية" else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); background-attachment: fixed; }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 35px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 15px 35px rgba(0,0,0,0.1); margin-bottom: 20px; }}
    .dest-card {{ background: white; padding: 20px; border-radius: 20px; border-{"right" if st.session_state.lang == "العربية" else "left"}: 12px solid #0EA5E9; margin-bottom: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }}
    .stButton>button {{ background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important; color: white !important; border-radius: 12px !important; border: none !important; font-weight: 700 !important; transition: 0.3s !important; }}
    [data-testid="stSidebar"] {{ display: none !important; }}
    </style>
''', unsafe_allow_html=True)

# تبديل اللغة
col_l1, col_l2 = st.columns([12, 1])
if col_l2.button("عربي/EN"):
    st.session_state.lang = "English" if st.session_state.lang == "العربية" else "العربية"
    st.session_state.suggestions = []
    st.rerun()

# --- صفحة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown(f'''<div class="glass-card" style="text-align: center;">
        <h1 style="color: #0369A1; margin-bottom: 0;">{T["p_name"]} 📍</h1>
        <p style="color: #64748B; font-size: 1.2em;">{T["subtitle"]}</p>
        <hr style="opacity: 0.1; margin: 25px 0;">
    </div>''', unsafe_allow_html=True)
    
    with st.container():
        st.session_state.user_name = st.text_input(T["visitor_name"], placeholder="...")
        u_budget = st.radio(T["budget_q"], [T["eco"], T["lux"]], horizontal=True)
        if st.button(T["start_btn"]):
            # تخزين نوع الميزانية (Economy أو Luxury) بشكل موحد لاستخدامه في جلب البيانات
            st.session_state.budget_key = "Luxury" if u_budget in [T["lux"], "فاخرة", "Luxury"] else "Economy"
            st.session_state.traffic_factor = random.uniform(1.2, 1.7)
            st.session_state.page = 'system'
            st.rerun()

# --- صفحة النظام ---
else:
    col_m, col_s = st.columns([2, 1])
    with col_m:
        st.markdown(f'''<div class="glass-card">
            <h3 style="margin:0; color:#0369A1;">📅 {T["day"]} {st.session_state.day} {T["of"]} 3</h3>
            <p>👤 {st.session_state.user_name} | 🕒 {formatted_time} | {T["weather"]}: <b>{T["sunny"] if 5 <= current_hour <= 17 else T["night"]}</b></p>
        </div>''', unsafe_allow_html=True)

        st.subheader(T["interests_q"])
        st.multiselect("", T["interests_list"], label_visibility="collapsed")
        
        if st.button(T["analyze_btn"]):
            # جلب البيانات من القاموس الذي تم تحميله من الملف
            st.session_state.suggestions = T["db"][st.session_state.budget_key]
            st.session_state.transport_choice = None
            st.rerun()

        if st.session_state.suggestions:
            st.markdown(f"### {T['transport_q']}")
            no_metro = any(not p['metro'] for p in st.session_state.suggestions)
            t_cols = st.columns(3)
            
            if not no_metro:
                if t_cols[0].button(T["m_btn"]): st.session_state.transport_choice = "metro"
            else:
                t_cols[0].markdown(f'<p style="color:#ef4444; font-size:0.8em; text-align:center;">{T["metro_fail"]}</p>', unsafe_allow_html=True)
            
            if t_cols[1].button(T["c_btn"]): st.session_state.transport_choice = "car"
            if t_cols[2].button(T["t_btn"]): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                if st.session_state.transport_choice:
                    base = p['b_time']
                    if st.session_state.transport_choice == "metro": f_time = f"{base + 5} {T['min']}"
                    elif st.session_state.transport_choice == "car": f_time = f"{int(base * st.session_state.traffic_factor)} {T['min']}"
                    else: f_time = f"{int(base * st.session_state.traffic_factor) + 5} {T['min']}"
                    time_display = f"⏱️ {T['est_time']}: {f_time}"
                else:
                    time_display = f"⏳ {T['wait_choice']}"

                st.markdown(f'''<div class="dest-card">
                    <h4 style="color:#0284C7; margin:0;">{p['الوجهة']}</h4>
                    <p style="color:#64748B;">{p['وصف']}</p>
                    <p style="font-weight:bold; color:#0369A1;">{time_display}</p>
                </div>''', unsafe_allow_html=True)

    with col_s:
        st.markdown(f'<div class="glass-card" style="text-align: center;"><h4>{T["rating_q"]}</h4>', unsafe_allow_html=True)
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐", key=f"s{i}"):
                st.session_state.rated = True
        
        if st.session_state.rated:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.session_state.day < 3:
                if st.button(T["next_day"]):
                    st.session_state.day += 1
                    st.session_state.suggestions = []
                    st.session_state.transport_choice = None
                    st.session_state.rated = False
                    st.rerun()
            else: st.success(T["finish"])
        
        if st.button("🔄 Reset"): st.session_state.clear(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.8em; margin-top: 30px;'>Path7 | Engineering Excellence @ IAU</p>", unsafe_allow_html=True)
