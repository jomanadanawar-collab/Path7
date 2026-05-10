import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# 2. التهيئة الآمنة (Session State) - عشان ما يطلع KeyError
for key, val in [('lang','ar'),('page','welcome'),('u_name',''),('u_budget','Economy'),
                ('suggestions',[]),('transport_choice','none'),('traffic_factor',1.2)]:
    if key not in st.session_state: st.session_state[key] = val

# 3. القاموس
TRANSLATIONS = {
    "ar": {
        "title": "📍 Path7 | المسار الذكي", "subtitle": "نظام التوافق اللحظي للسياحة الذكية",
        "name_label": "اسم السائح الموقر", "welcome": "مرحباً يا", "weather": "الجو في الرياض",
        "weather_val": "ليل صافي 🌙" if current_hour > 18 or current_hour < 5 else "مشمس ☀️",
        "eco": "اقتصادية", "lux": "فاخرة", "start": "استكشف مسارك الآن 🚀",
        "interests_q": "🌟 ما هي اهتماماتك المفضلة لليوم؟", "analyze": "تحليل الوجهات الأنسب لهذا اليوم 🔍",
        "m_no": "المترو غير متاح لهذه الوجهات ❌", "m_btn": "🚇 مترو الرياض", "c_btn": "🚗 سيارتي", "t_btn": "🚕 تاكسي",
        "rating_q": "⭐ تقييمك لليوم", "reset": "🔄 ضبط جديد", "lang_btn": "English 🌐", "dir": "rtl", "align": "right"
    },
    "en": {
        "title": "📍 Path7 | Smart Journey", "subtitle": "Real-time Smart Tourism System",
        "name_label": "Tourist Name", "welcome": "Welcome", "weather": "Riyadh Weather",
        "weather_val": "Clear Night 🌙" if current_hour > 18 or current_hour < 5 else "Sunny ☀️",
        "eco": "Economy", "lux": "Luxury", "start": "Explore Now 🚀",
        "interests_q": "🌟 Your interests today?", "analyze": "Analyze Destinations 🔍",
        "m_no": "Metro unavailable ❌", "m_btn": "🚇 Riyadh Metro", "c_btn": "🚗 My Car", "t_btn": "🚕 Taxi",
        "rating_q": "⭐ Rate Your Day", "reset": "🔄 Reset", "lang_btn": "العربية 🌐", "dir": "ltr", "align": "left"
    }
}
T = TRANSLATIONS[st.session_state.lang]

# 4. التنسيق (الألوان والبركات اللي عجبتك)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {T["dir"]}; text-align: {T["align"]}; }}
    .stApp {{ background-color: #F0F9FF !important; }}
    .main-card {{ background: white; padding: 25px; border-radius: 25px; border-top: 12px solid #0284C7; box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin-bottom: 20px; }}
    .info-box {{ background: white; padding: 20px; border-radius: 20px; border-{"right" if st.session_state.lang == 'ar' else "left"}: 8px solid #38BDF8; margin-bottom: 15px; border: 1px solid #BAE6FD; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }}
    .stButton>button {{ background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important; color: white !important; border-radius: 12px !important; border: none; font-weight: bold; transition: 0.3s; }}
    .stButton>button:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px rgba(2, 132, 199, 0.4) !important; }}
    </style>
''', unsafe_allow_html=True)

# 5. الصفحات
if st.session_state.page == 'welcome':
    if st.button(T["lang_btn"]): st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar' ; st.rerun()
    with st.form("w"):
        st.markdown(f"<h1 style='text-align:center;'>{T['title']}</h1>", unsafe_allow_html=True)
        n = st.text_input(T["name_label"], value=st.session_state.u_name)
        b = st.radio(T["budget_label"], [T["eco"], T["lux"]], horizontal=True)
        if st.form_submit_button(T["start"]):
            st.session_state.u_name = n if n else "JOMAN"
            st.session_state.u_budget = "Economy" if b in [T["eco"], "اقتصادية"] else "Luxury"
            st.session_state.page = 'system' ; st.rerun()
else:
    # --- منطق المواصلات والنجوم حق جمانة (بدون تغيير) ---
    col_m, col_s = st.columns([2, 1])
    with col_m:
        st.markdown(f'''<div class="main-card">
            <h3>📅 اليوم 1 | {T["welcome"]} {st.session_state.u_name}</h3>
            <p>{T["weather"]}: <b>{T["weather_val"]}</b></p>
        </div>''', unsafe_allow_html=True)
        
        cats = ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"] if st.session_state.lang == 'ar' else ["History", "Entertainment", "Shopping", "Dining", "Nature"]
        u_interests = st.multiselect(T["interests_q"], cats)
        
        if st.button(T["analyze"]):
            # قاعدة بيانات تجريبية للفحص
            st.session_state.suggestions = [
                {'الوجهة': 'حصن المصمك', 'وصف': 'رمز التوحيد', 'base_time': 25, 'metro_access': True},
                {'الوجهة': 'وادي حنيفة', 'وصف': 'طبيعة خلابة', 'base_time': 40, 'metro_access': False}
            ]
            st.rerun()

        if st.session_state.suggestions:
            no_metro_places = [p['الوجهة'] for p in st.session_state.suggestions if not p['metro_access']]
            t_col1, t_col2, t_col3 = st.columns(3)
            
            if not no_metro_places:
                if t_col1.button(T["m_btn"]): st.session_state.transport_choice = "مترو"
            else:
                t_col1.markdown(f'<p style="text-align:center; color:#94A3B8; font-size:0.8em; margin-top:15px;">{T["m_no"]}</p>', unsafe_allow_html=True)
                
            if t_col2.button(T["c_btn"]): st.session_state.transport_choice = "سيارة"
            if t_col3.button(T["t_btn"]): st.session_state.transport_choice = "تاكسي"

            for place in st.session_state.suggestions:
                base = place['base_time']
                choice = st.session_state.transport_choice
                if choice == "مترو": f_time = f"{base + 5} دقيقة" ; icon = "🚇"
                elif choice == "سيارة": f_time = f"{int(base * 1.2)} دقيقة" ; icon = "🚗"
                elif choice == "تاكسي": f_time = f"{int(base * 1.2) + 3} دقيقة" ; icon = "🚕"
                else: f_time = "بانتظار اختيارك..." ; icon = "📍"

                st.markdown(f'''<div class="info-box">
                    <h4 style="margin:0; color:#0284C7;">{icon} {place['الوجهة']}</h4>
                    <p style="margin:10px 0 0 0; font-weight:bold; color:#0369A1;">⏱️ الوقت المقدر: {f_time}</p>
                </div>''', unsafe_allow_html=True)

    with col_s:
        st.markdown("---")
        st.subheader(T["rating_q"])
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐", key=f"s{i}"): st.session_state.star_rating = i
        if st.button(T["reset"]): st.session_state.clear() ; st.rerun()
