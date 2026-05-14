import streamlit as st
import random
import json
from datetime import datetime
import pytz

# وظيفة لقراءة ملف JSON
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

st.set_page_config(page_title="Path7 | مسار 7", layout="wide", initial_sidebar_state="collapsed")

# إدارة الحالة
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'day' not in st.session_state: st.session_state.day = 1
if 'rated' not in st.session_state: st.session_state.rated = False
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'rating_value' not in st.session_state: st.session_state.rating_value = 0

T = DATA_ALL.get(st.session_state.lang, {})

# واجهة Glassmorphism مطورة لزيادة الجمالية وحل مشاكل التباين
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if st.session_state.lang == "العربية" else "ltr"}; }}
    
    /* حل مشكلة تباين الخلفية والنص - تدرج ديناميكي غامق */
    .stApp {{ 
        background: linear-gradient(145deg, #075985 0%, #03456F 100%); 
        color: white !important; /* فرض لون النص أبيض */
    }}
    
    /* فرض لون النص ليكون أبيض للأسئلة الافتراضية */
    div.stSelectbox div.stMarkdown, div.stRadio div.stMarkdown, div.stTextInput div.stMarkdown {{
        color: white !important;
    }}
    
    .glass-card {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); padding: 30px; border-radius: 30px; border: 1px solid rgba(255,255,255,0.1); color: white; margin-bottom: 20px; }}
    .dash-panel {{ background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); padding: 15px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; text-align: center; }}
    .dest-card {{ background: white; padding: 20px; border-radius: 20px; border-{"right" if st.session_state.lang == "العربية" else "left"}: 12px solid #0EA5E9; margin-bottom: 15px; color: #1E293B; }}
    .map-btn {{ background-color: #0284C7; color: white !important; padding: 8px 16px; border-radius: 50px; text-decoration: none; font-weight: bold; font-size: 0.9em; }}
    .next-day-btn {{ background: linear-gradient(90deg, #10B981 0%, #34D399 100%) !important; color: white !important; }}
    </style>
''', unsafe_allow_html=True)

# تبديل اللغة
col_l1, col_l2 = st.columns([12, 1])
if col_l2.button("عربي/EN"):
    st.session_state.lang = "English" if st.session_state.lang == "العربية" else "العربية"
    st.session_state.suggestions = []
    st.rerun()

# --- حل مشكلة الصفحة الترحيبية (ألوان واضحة) ---
if st.session_state.page == 'welcome':
    st.markdown(f'<div class="glass-card" style="text-align: center; margin-top: 10vh;">', unsafe_allow_html=True)
    st.title(f"📍 {T.get('p_name', '')}")
    st.subheader(T.get('subtitle', ''))
    
    with st.container():
        st.session_state.user_name = st.text_input(T.get("visitor_name", ""), placeholder="أدخل اسمك هنا")
        u_budget = st.radio(T.get("budget_q", ""), [T.get("eco", ""), T.get("lux", "")], horizontal=True)
        if st.button(T.get("start_btn", ""), use_container_width=True):
            st.session_state.budget_key = "Luxury" if u_budget in [T.get("lux", ""), "Luxury"] else "Economy"
            st.session_state.page = 'main'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- حل مشكلة الصفحة الرئيسية (إعادة هيكلة واجهة المستخدم) ---
else:
    # 1. لوحة المعلومات الذكية (تحل مشكلة القائمة المكدسة)
    with st.container():
        weather_info = T.get("sunny", "") if 5 <= current_hour <= 17 else T.get("night", "")
        st.markdown(f'''
        <div class="dash-panel">
            <h2>{greeting}، {st.session_state.user_name}</h2>
            <p>🕒 {formatted_time} | {T.get("weather", "")}: <b>{weather_info}</b></p>
            <p style="font-weight:bold; color:#0EA5E9;">📅 {T.get("day", "")} {st.session_state.day} {T.get("of", "")} 3</p>
        </div>
        ''', unsafe_allow_html=True)

    # 2. منطقة التحليل
    with st.container():
        st.subheader(T.get("interests_q", ""))
        selected_ints = st.multiselect("", T.get("interests_list", []), label_visibility="collapsed")
        
        if st.button(T.get("analyze_btn", ""), use_container_width=True):
            all_options = T.get("db", {}).get(st.session_state.budget_key, [])
            st.session_state.suggestions = [p for p in all_options if p.get('الفئة') in selected_ints] if selected_ints else random.sample(all_options, 2)
            st.session_state.transport_choice = None
            st.session_state.traffic_factor = random.uniform(1.2, 1.8)
            st.session_state.rated = False # تصفير حالة التقييم ليوم جديد
            st.rerun()

        if st.session_state.suggestions:
            st.markdown(f"### {T.get('transport_q', '')}")
            tc = st.columns(3)
            if tc[0].button(T.get("m_btn", "")): st.session_state.transport_choice = "metro"
            if tc[1].button(T.get("c_btn", "")): st.session_state.transport_choice = "car"
            if tc[2].button(T.get("t_btn", "")): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                # منطق حساب الوقت الذكي
                if st.session_state.transport_choice == "metro":
                    f_time = p['b_time'] + 5
                    icon = "🚇"
                elif st.session_state.transport_choice in ["car", "taxi"]:
                    f_time = int(p['b_time'] * st.session_state.traffic_factor)
                    icon = "🚗" if st.session_state.transport_choice == "car" else "🚕"
                else:
                    time_display = f"⏳ {T.get('wait_choice', '')}"

                time_display = f"⏱️ {T.get('est_time', '')}: {f_time} {T.get('min', '')}" if st.session_state.transport_choice else f"⏳ {T.get('wait_choice', '')}"

                st.markdown(f'''<div class="dest-card">
                    <h4>{p['الوجهة']}</h4>
                    <p>{p['وصف']}</p>
                    <p style="font-weight:bold; color:#0369A1; margin-bottom:10px;">{time_display}</p>
                    <a href="{p['map_url']}" target="_blank" class="map-btn">{T.get("map_btn", "")}</a>
                </div>''', unsafe_allow_html=True)
                
            # --- حل مشكلة التقييم والانتقال لليوم التالي (نظام فوري بالنجوم ⭐) ---
            st.markdown(f'<div class="dash-panel" style="margin-top:30px; text-align:right;"><h4>⭐ {T.get("rating_q", "")}</h4>', unsafe_allow_html=True)
            stars_cols = st.columns(5)
            for i in range(1, 6):
                if stars_cols[i-1].button(f"{i}⭐", key=f"s{i}"):
                    st.session_state.rating_value = i
                    st.session_state.rated = True
            
            # إذا تم التقييم، أظهر زر اليوم التالي أو رسالة النهاية
            if st.session_state.rated:
                st.write(f"✅ شكراً لتقييمك: {st.session_state.rating_value}/5")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.session_state.day < 3:
                    # زر اليوم التالي بتصميم بارز وواضح
                    if st.button(T.get("next_day", ""), key="next_day_btn", use_container_width=True):
                        st.session_state.day += 1
                        st.session_state.suggestions = []
                        st.session_state.transport_choice = None
                        st.session_state.rated = False
                        st.rerun()
                else:
                    st.success(T.get("finish", ""))

st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.4); margin-top: 50px;'>Path7 | Intelligent Tourism Framework</p>", unsafe_allow_html=True)
