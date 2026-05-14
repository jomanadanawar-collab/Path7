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
    except:
        return {}

DATA_ALL = load_data()
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour
formatted_time = now_riyadh.strftime('%I:%M %p')

# منطق تحية الوقت
greeting = "صباح الخير" if 5 <= current_hour < 12 else "مساء الخير"

st.set_page_config(page_title="Path7 | مسار 7", layout="wide")

if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

T = DATA_ALL.get(st.session_state.lang, {})

# واجهة Glassmorphism مطورة لزيادة الجمالية
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if st.session_state.lang == "العربية" else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #075985 0%, #0C4A6E 100%); }}
    .main-card {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); padding: 30px; border-radius: 30px; border: 1px solid rgba(255,255,255,0.1); color: white; margin-bottom: 20px; }}
    .dest-card {{ background: white; padding: 0; border-radius: 20px; overflow: hidden; margin-bottom: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.2); color: #1E293B; border-bottom: 5px solid #0EA5E9; }}
    .dest-content {{ padding: 15px; }}
    .map-btn {{ background: #0284C7; color: white !important; padding: 8px 20px; border-radius: 50px; text-decoration: none; font-weight: bold; display: inline-block; font-size: 0.8em; }}
    .metro-badge {{ background: #DC2626; color: white; padding: 2px 10px; border-radius: 5px; font-size: 0.7em; margin-bottom: 5px; display: inline-block; }}
    </style>
''', unsafe_allow_html=True)

if st.session_state.page == 'welcome':
    st.markdown(f'<div style="text-align: center; margin-top: 10vh; color: white;">', unsafe_allow_html=True)
    st.title(f"📍 {T.get('p_name', '')}")
    st.subheader(T.get('subtitle', ''))
    
    with st.container():
        col_c, _ = st.columns([1, 2])
        with col_c:
            name = st.text_input(T.get("visitor_name", ""), placeholder="أدخل اسمك هنا")
            budget = st.selectbox(T.get("budget_q", ""), [T.get("eco", ""), T.get("lux", "")])
            if st.button(T.get("start_btn", ""), use_container_width=True):
                st.session_state.user_name = name
                st.session_state.budget_key = "Luxury" if "فاخرة" in budget or "Luxury" in budget else "Economy"
                st.session_state.page = 'main'
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # الشريط الجانبي الذكي
    with st.sidebar:
        st.markdown(f"### {greeting}، {st.session_state.user_name}")
        st.write(f"🕒 {formatted_time}")
        weather_info = T.get("sunny", "") if 7 <= current_hour <= 17 else T.get("night", "")
        st.info(f"{T.get('weather', '')}: {weather_info}")
        if st.button("🔄 إقلاع جديد"): st.session_state.clear(); st.rerun()

    # محتوى الصفحة الرئيسي
    st.markdown(f'<div class="main-card"><h2>{T.get("interests_q", "")}</h2></div>', unsafe_allow_html=True)
    selected = st.multiselect("", T.get("interests_list", []), label_visibility="collapsed")
    
    if st.button(T.get("analyze_btn", ""), use_container_width=True):
        db = T.get("db", {}).get(st.session_state.budget_key, [])
        st.session_state.suggestions = [p for p in db if p.get('الفئة') in selected] if selected else random.sample(db, 2)
        st.session_state.transport_choice = None
        st.session_state.traffic = random.uniform(1.2, 1.9)
        st.rerun()

    if st.session_state.suggestions:
        st.markdown(f'<h3 style="color:white;">{T.get("transport_q", "")}</h3>', unsafe_allow_html=True)
        t_cols = st.columns(3)
        if t_cols[0].button(T.get("m_btn", "")): st.session_state.transport_choice = "metro"
        if t_cols[1].button(T.get("c_btn", "")): st.session_state.transport_choice = "car"
        if t_cols[2].button(T.get("t_btn", "")): st.session_state.transport_choice = "taxi"

        # عرض المسار بشكل متسلسل (ليظهر كـ Route)
        for i, p in enumerate(st.session_state.suggestions):
            if st.session_state.transport_choice == "metro":
                f_time = p['b_time'] + 5
                icon = "🚇"
            else:
                f_time = int(p['b_time'] * st.session_state.traffic)
                icon = "🚗" if st.session_state.transport_choice == "car" else "🚕"
            
            # عرض البطاقة
            with st.container():
                st.markdown(f'''
                <div class="dest-card">
                    <div class="dest-content">
                        {f'<span class="metro-badge">متوفر عبر المترو ✅</span>' if p['metro'] else ''}
                        <h3 style="margin:0; color:#0369A1;">{i+1}. {p['الوجهة']}</h3>
                        <p style="font-size:0.9em; color:#64748B;">{p['وصف']}</p>
                        <p style="font-weight:bold;">{icon} {T.get("est_time", "")}: {f_time if st.session_state.transport_choice else "--"} {T.get("min", "")}</p>
                        <a href="{p['map_url']}" target="_blank" class="map-btn">{T.get("map_btn", "")}</a>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                if i < len(st.session_state.suggestions)-1:
                    st.markdown('<div style="text-align:center; color:white; font-size:1.5em;">⬇️</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:rgba(255,255,255,0.4); margin-top:50px;'>Path7 | Intelligent Tourism Framework</p>", unsafe_allow_html=True)
