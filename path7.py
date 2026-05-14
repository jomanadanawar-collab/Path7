import streamlit as st
import random
import json
from datetime import datetime
import pytz

# 1. تحميل البيانات من ملف JSON
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("ملف البيانات غير موجود! تأكدي من رفع path7_data.json بجانب هذا الكود.")
        return {}

DATA_ALL = load_data()

# 2. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
formatted_time = now_riyadh.strftime('%I:%M %p')
current_hour = now_riyadh.hour

st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# 3. إدارة الحالة (Session State)
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'day' not in st.session_state: st.session_state.day = 1
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'rated' not in st.session_state: st.session_state.rated = False
if 'suggestions' not in st.session_state: st.session_state.suggestions = []

T = DATA_ALL.get(st.session_state.lang, {})

# 4. التنسيق البصري المحسن (CSS Animations & Layout)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    
    /* أنيميشن الدخول الانسيابي */
    @keyframes fadeInSlide {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if st.session_state.lang == "العربية" else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); background-attachment: fixed; }}
    
    /* الكروت الزجاجية مع أنيميشن */
    .glass-card {{ 
        background: rgba(255, 255, 255, 0.75); 
        backdrop-filter: blur(12px); 
        padding: 35px; 
        border-radius: 25px; 
        border: 1px solid rgba(255, 255, 255, 0.3); 
        box-shadow: 0 15px 35px rgba(0,0,0,0.1); 
        margin-bottom: 20px;
        animation: fadeInSlide 0.6s ease-out;
    }}
    
    .dest-card {{ 
        background: white; 
        padding: 20px; 
        border-radius: 20px; 
        border-{"right" if st.session_state.lang == "العربية" else "left"}: 12px solid #0EA5E9; 
        margin-bottom: 15px; 
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInSlide 0.8s ease-out;
    }}
    
    .dest-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.12);
    }}

    /* الأزرار المطورة */
    .stButton>button {{ 
        background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important; 
        color: white !important; 
        border-radius: 12px !important; 
        border: none !important; 
        font-weight: 700 !important;
        transition: 0.3s !important;
    }}
    .stButton>button:hover {{
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.6) !important;
        transform: scale(1.02);
    }}
    
    .map-btn {{ 
        background-color: #0284C7; 
        color: white !important; 
        padding: 10px 20px; 
        border-radius: 12px; 
        text-decoration: none; 
        font-size: 0.9em; 
        font-weight: bold; 
        display: inline-block; 
        margin-top: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    </style>
''', unsafe_allow_html=True)

# تبديل اللغة (كما هو بطلبك)
col_l1, col_l2 = st.columns([12, 1])
if col_l2.button("عربي/EN"):
    st.session_state.lang = "English" if st.session_state.lang == "العربية" else "العربية"
    st.session_state.suggestions = []
    st.rerun()

# --- صفحة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown(f'''<div class="glass-card" style="text-align: center;">
        <h1 style="color: #0369A1; margin-bottom: 0;">{T.get("p_name", "Path7")} 📍</h1>
        <p style="color: #64748B; font-size: 1.2em;">{T.get("subtitle", "")}</p>
        <hr style="opacity: 0.1; margin: 25px 0;">
    </div>''', unsafe_allow_html=True)
    
    with st.container():
        st.session_state.user_name = st.text_input(T.get("visitor_name", ""), placeholder="...")
        u_budget = st.radio(T.get("budget_q", ""), [T.get("eco", ""), T.get("lux", "")], horizontal=True)
        if st.button(T.get("start_btn", "انطلق")):
            st.session_state.budget_key = "Luxury" if u_budget in [T.get("lux", ""), "فاخرة", "Luxury"] else "Economy"
            st.session_state.traffic_factor = random.uniform(1.2, 1.7)
            st.session_state.page = 'system'
            st.rerun()

# --- صفحة النظام ---
else:
    # الهيدر العلوي
    st.markdown(f'''<div class="glass-card">
        <h3 style="margin:0; color:#0369A1;">📅 {T.get("day", "")} {st.session_state.day} {T.get("of", "")} 3</h3>
        <p>👤 {st.session_state.user_name} | 🕒 {formatted_time} | {T.get("weather", "")}: <b>{T.get("sunny", "") if 5 <= current_hour <= 17 else T.get("night", "")}</b></p>
    </div>''', unsafe_allow_html=True)

    # قسم الاهتمامات
    st.subheader(T.get("interests_q", ""))
    selected_interests = st.multiselect("", T.get("interests_list", []), label_visibility="collapsed")
    
    if st.button(T.get("analyze_btn", "تحليل المسار")):
        all_options = T.get("db", {}).get(st.session_state.budget_key, [])
        if selected_interests:
            st.session_state.suggestions = [p for p in all_options if p.get('الفئة') in selected_interests]
            if not st.session_state.suggestions: st.session_state.suggestions = random.sample(all_options, min(2, len(all_options)))
        else:
            st.session_state.suggestions = random.sample(all_options, min(2, len(all_options)))
        st.session_state.transport_choice = None
        st.rerun()

    # عرض المقترحات والتقييم تحتها مباشرة
    if st.session_state.suggestions:
        st.markdown(f"### {T.get('transport_q', '')}")
        t_cols = st.columns(3)
        if t_cols[0].button(T.get("m_btn", "🚇 مترو")): st.session_state.transport_choice = "metro"
        if t_cols[1].button(T.get("c_btn", "🚗 سيارة")): st.session_state.transport_choice = "car"
        if t_cols[2].button(T.get("t_btn", "🚕 تاكسي")): st.session_state.transport_choice = "taxi"

        # عرض البطاقات
        for p in st.session_state.suggestions:
            base = p.get('b_time', 25)
            time_display = f"⏳ تقدير الوقت: {base} دقيقة" # منطق مبسط للحفاظ على استقرار الكود
            
            st.markdown(f'''<div class="dest-card">
                <h4 style="color:#0284C7; margin:0;">{p['الوجهة']}</h4>
                <p style="color:#64748B; margin:5px 0;">{p['وصف']}</p>
                <p style="font-weight:bold; color:#0369A1; margin-bottom:10px;">{time_display}</p>
                <a href="https://www.google.com/maps/search/?api=1&query={p['الوجهة'].replace(' ', '+')}" target="_blank" class="map-btn">📍 فتح في خرائط جوجل</a>
            </div>''', unsafe_allow_html=True)

        # --- قسم التقييم (تم نقله هنا ليكون تحت الأماكن مباشرة) ---
        st.markdown(f'''<div class="glass-card" style="text-align: center; margin-top: 30px;">
            <h4>{T.get("rating_q", "تقييمك لتجربة اليوم")} ⭐</h4>''', unsafe_allow_html=True)
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}★", key=f"star_{i}"): st.session_state.rated = True
        
        if st.session_state.rated:
            if st.session_state.day < 3 and st.button(T.get("next_day", "انتقل لليوم التالي")):
                st.session_state.day += 1
                st.session_state.suggestions = []; st.session_state.transport_choice = None; st.session_state.rated = False
                st.rerun()
            elif st.session_state.day >= 3: st.success(T.get("finish", "لقد أتممت مسار 3 أيام بنجاح!"))
        
        if st.button("🔄 إعادة البدء"): st.session_state.clear(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.8em; margin-top: 30px;'>Path7 | Engineering Excellence @ IAU</p>", unsafe_allow_html=True)
