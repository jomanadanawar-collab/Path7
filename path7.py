import streamlit as st
import random
import json
from datetime import datetime
import pytz

# وظيفة لقراءة ملف JSON
def load_data():
    with open('path7_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

DATA_ALL = load_data()

# إعدادات الوقت
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
formatted_time = now_riyadh.strftime('%I:%M %p')
current_hour = now_riyadh.hour

st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# إدارة الحالة
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'day' not in st.session_state: st.session_state.day = 1
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'rated' not in st.session_state: st.session_state.rated = False
if 'suggestions' not in st.session_state: st.session_state.suggestions = []

T = DATA_ALL[st.session_state.lang]

# الستايل البصري (Glassmorphism)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if st.session_state.lang == "العربية" else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); background-attachment: fixed; }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 35px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 15px 35px rgba(0,0,0,0.1); margin-bottom: 20px; }}
    .dest-card {{ background: white; padding: 20px; border-radius: 20px; border-{"right" if st.session_state.lang == "العربية" else "left"}: 12px solid #0EA5E9; margin-bottom: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }}
    .map-btn {{ background-color: #0284C7; color: white !important; padding: 8px 16px; border-radius: 10px; text-decoration: none; font-size: 0.9em; font-weight: bold; display: inline-block; margin-top: 10px; transition: 0.3s; }}
    .map-btn:hover {{ background-color: #0369A1; opacity: 0.9; }}
    .stButton>button {{ background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important; color: white !important; border-radius: 12px !important; border: none !important; font-weight: 700 !important; }}
    </style>
''', unsafe_allow_html=True)

# تبديل اللغة
col_l1, col_l2 = st.columns([12, 1])
if col_l2.button("عربي/EN"):
    st.session_state.lang = "English" if st.session_state.lang == "العربية" else "العربية"
    st.session_state.suggestions = []
    st.rerun()

if st.session_state.page == 'welcome':
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown(f'''<div class="glass-card" style="text-align: center;">
        <h1 style="color: #0369A1; margin-bottom: 0;">{T["p_name"]} 📍</h1>
        <p style="color: #64748B; font-size: 1.2em;">{T["subtitle"]}</p>
    </div>''', unsafe_allow_html=True)
    
    with st.container():
        st.session_state.user_name = st.text_input(T["visitor_name"], placeholder="...")
        u_budget = st.radio(T["budget_q"], [T["eco"], T["lux"]], horizontal=True)
        if st.button(T["start_btn"]):
            st.session_state.budget_key = "Luxury" if u_budget in [T["lux"], "فاخرة", "Luxury"] else "Economy"
            st.session_state.traffic_factor = random.uniform(1.2, 1.7)
            st.session_state.page = 'system'
            st.rerun()

else:
    col_m, col_s = st.columns([2, 1])
    with col_m:
        st.markdown(f'''<div class="glass-card">
            <h3 style="margin:0; color:#0369A1;">📅 {T["day"]} {st.session_state.day} {T["of"]} 3</h3>
            <p>👤 {st.session_state.user_name} | 🕒 {formatted_time} | {T["weather"]}: <b>{T["sunny"] if 5 <= current_hour <= 17 else T["night"]}</b></p>
        </div>''', unsafe_allow_html=True)

        st.subheader(T["interests_q"])
        selected_interests = st.multiselect("", T["interests_list"], label_visibility="collapsed")
        
        if st.button(T["analyze_btn"]):
            # تصفية الوجهات بناءً على الاهتمامات المختارة
            all_options = T["db"][st.session_state.budget_key]
            if selected_interests:
                st.session_state.suggestions = [p for p in all_options if p.get('الفئة') in selected_interests]
                if not st.session_state.suggestions: st.session_state.suggestions = random.sample(all_options, min(2, len(all_options)))
            else:
                st.session_state.suggestions = random.sample(all_options, min(2, len(all_options)))
            st.session_state.transport_choice = None
            st.rerun()

        if st.session_state.suggestions:
            st.markdown(f"### {T['transport_q']}")
            no_metro = any(not p['metro'] for p in st.session_state.suggestions)
            t_cols = st.columns(3)
            if not no_metro and t_cols[0].button(T["m_btn"]): st.session_state.transport_choice = "metro"
            if t_cols[1].button(T["c_btn"]): st.session_state.transport_choice = "car"
            if t_cols[2].button(T["t_btn"]): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                time_display = f"⏱️ {T['est_time']}: {int(p['b_time'] * st.session_state.traffic_factor)} {T['min']}" if st.session_state.transport_choice else f"⏳ {T['wait_choice']}"
                
                st.markdown(f'''<div class="dest-card">
                    <h4 style="color:#0284C7; margin:0;">{p['الوجهة']}</h4>
                    <p style="color:#64748B; margin:5px 0;">{p['وصف']}</p>
                    <p style="font-weight:bold; color:#0369A1; margin-bottom:10px;">{time_display}</p>
                    <a href="{p['map_url']}" target="_blank" class="map-btn">{T["map_btn"]}</a>
                </div>''', unsafe_allow_html=True)

    with col_s:
        st.markdown(f'<div class="glass-card" style="text-align: center;"><h4>{T["rating_q"]}</h4>', unsafe_allow_html=True)
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐", key=f"s{i}"): st.session_state.rated = True
        
        if st.session_state.rated:
            if st.session_state.day < 3 and st.button(T["next_day"]):
                st.session_state.day += 1
                st.session_state.suggestions = []; st.session_state.transport_choice = None; st.session_state.rated = False
                st.rerun()
            elif st.session_state.day >= 3: st.success(T["finish"])
        
        if st.button("🔄 Reset"): st.session_state.clear(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.8em; margin-top: 30px;'>Path7 | Engineering Excellence @ IAU</p>", unsafe_allow_html=True)
