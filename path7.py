import streamlit as st
import random
import json
from datetime import datetime
import pytz

# تحميل البيانات
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("ملف البيانات غير موجود!")
        return {}

DATA_ALL = load_data()
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
formatted_time = now_riyadh.strftime('%I:%M %p')

st.set_page_config(page_title="Path7", layout="wide")

# إدارة الحالة
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'day' not in st.session_state: st.session_state.day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

T = DATA_ALL.get(st.session_state.lang, {})

# التنسيق البصري
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if st.session_state.lang == "العربية" else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); }}
    .glass-card {{ background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 20px; }}
    .dest-card {{ background: white; padding: 20px; border-radius: 15px; border-{"right" if st.session_state.lang == "العربية" else "left"}: 10px solid #0EA5E9; margin-bottom: 15px; }}
    .map-btn {{ background-color: #0284C7; color: white !important; padding: 8px 15px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 10px; }}
    </style>
''', unsafe_allow_html=True)

if st.session_state.page == 'welcome':
    st.markdown(f'<div class="glass-card" style="text-align: center;"><h1>{T.get("p_name", "")} 📍</h1><p>{T.get("subtitle", "")}</p></div>', unsafe_allow_html=True)
    u_name = st.text_input(T.get("visitor_name", ""))
    u_budget = st.radio(T.get("budget_q", ""), [T.get("eco", ""), T.get("lux", "")], horizontal=True)
    if st.button(T.get("start_btn", "")):
        st.session_state.user_name = u_name
        st.session_state.budget_key = "Luxury" if u_budget in [T.get("lux", ""), "Luxury"] else "Economy"
        st.session_state.traffic_factor = random.uniform(1.2, 1.8)
        st.session_state.page = 'main'
        st.rerun()

else:
    col_main, col_side = st.columns([2, 1])
    with col_main:
        st.markdown(f'<div class="glass-card"><h3>📅 {T.get("day", "")} {st.session_state.day} | {formatted_time}</h3></div>', unsafe_allow_html=True)
        selected_ints = st.multiselect(T.get("interests_q", ""), T.get("interests_list", []))
        
        if st.button(T.get("analyze_btn", "")):
            all_options = T.get("db", {}).get(st.session_state.budget_key, [])
            st.session_state.suggestions = [p for p in all_options if p.get('الفئة') in selected_ints] if selected_ints else random.sample(all_options, 2)
            st.session_state.transport_choice = None
            st.rerun()

        if st.session_state.suggestions:
            st.markdown(f"### {T.get('transport_q', '')}")
            tc = st.columns(3)
            if tc[0].button(T.get("m_btn", "")): st.session_state.transport_choice = "metro"
            if tc[1].button(T.get("c_btn", "")): st.session_state.transport_choice = "car"
            if tc[2].button(T.get("t_btn", "")): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                # منطق المترو (ثابت) مقابل السيارة (زحام)
                if st.session_state.transport_choice == "metro":
                    f_time = p['b_time'] + 5
                    icon = "🚇"
                elif st.session_state.transport_choice in ["car", "taxi"]:
                    f_time = int(p['b_time'] * st.session_state.traffic_factor)
                    icon = "🚗" if st.session_state.transport_choice == "car" else "🚕"
                else:
                    f_time = "--"; icon = "⏳"

                st.markdown(f'''<div class="dest-card">
                    <h4>{p['الوجهة']}</h4>
                    <p>{p['وصف']}</p>
                    <p><b>{icon} {T.get("est_time", "")}: {f_time} {T.get("min", "")}</b></p>
                    <a href="{p['map_url']}" target="_blank" class="map-btn">{T.get("map_btn", "")}</a>
                </div>''', unsafe_allow_html=True)

    with col_side:
        if st.button("🔄 Reset"): st.session_state.clear(); st.rerun()
