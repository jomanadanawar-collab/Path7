import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. الإعدادات الأساسية (Time & Page)
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# 2. تهيئة الجلسة (Session State) - الدرع الواقي من الايرورات
state_defaults = {
    'lang': 'ar', 'page': 'welcome', 'u_name': '', 'u_budget': 'Economy',
    'suggestions': [], 'transport_choice': 'none', 'traffic_factor': 1.2, 'star_rating': 0
}
for key, val in state_defaults.items():
    if key not in st.session_state: st.session_state[key] = val

# 3. القاموس (Translations)
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

# 4. التصميم البصري (CSS) - الحركات والبركات
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {T["dir"]}; text-align: {T["align"]}; }}
    .stApp {{ background-color: #F0F9FF !important; }}
    .main-card {{ background: white; padding: 25px; border-radius: 25px; border-top: 12px solid #0284C7; box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin-bottom: 20px; border: 1px solid #E2E8F0; }}
    .info-box {{ background: white; padding: 20px; border-radius: 20px; border-{"right" if st.session_state.lang == "ar" else "left"}: 8px solid #38BDF8; margin-bottom: 15px; border: 1px solid #BAE6FD; box-shadow: 0 5px 15px rgba(0,0,0,0.05); transition: 0.3s; }}
    .info-box:hover {{ transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.1); }}
    .stButton>button {{ background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important; color: white !important; border-radius: 12px !important; border: none; font-weight: bold; transition: 0.3s; height: 3.5em; }}
    .stButton>button:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px rgba(2, 132, 199, 0.4) !important; }}
    </style>
''', unsafe_allow_html=True)

# 5. التحكم باللغة
col_l1, col_l2 = st.columns([0.85, 0.15])
if col_l2.button(T["lang_btn"]):
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
    st.rerun()

# --- الصفحة الأولى (Welcome) ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.form("w_form"):
        st.markdown(f"<h1 style='text-align:center; color:#0369A1;'>{T['title']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; color:#64748B;'>{T['subtitle']}</p>", unsafe_allow_html=True)
        u_name = st.text_input(T["name_label"], value=st.session_state.u_name)
        u_budget = st.radio("", [T["eco"], T["lux"]], horizontal=True)
        if st.form_submit_button(T["start"]):
            st.session_state.u_name = u_name if u_name else "Jomanah"
            st.session_state.u_budget = "Economy" if u_budget in [T["eco"], "اقتصادية", "Economy"] else "Luxury"
            st.session_state.page = 'system'
            st.rerun()

# --- الصفحة الثانية (System) ---
else:
    col_main, col_side = st.columns([2, 1])
    with col_main:
        st.markdown(f'''<div class="main-card">
            <h3>📅 اليوم 1 | {T["welcome"]} {st.session_state.u_name}</h3>
            <p>{T["weather"]}: <b>{T["weather_val"]}</b></p>
        </div>''', unsafe_allow_html=True)
        
        cats = ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"] if st.session_state.lang == 'ar' else ["History", "Entertainment", "Shopping", "Dining", "Nature"]
        u_interests = st.multiselect(T["interests_q"], cats)
        
        if st.button(T["analyze"]):
            # قاعدة بيانات ديناميكية (تتغير حسب الميزانية واللغة)
            st.session_state.suggestions = [
                {'الوجهة': 'حصن المصمك' if st.session_state.lang == 'ar' else 'Masmak Fortress', 'وصف': 'رمز توحيد المملكة' if st.session_state.lang == 'ar' else 'Symbol of Unity', 'base_time': 25, 'metro_access': True},
                {'الوجهة': 'وادي حنيفة' if st.session_state.lang == 'ar' else 'Hanifa Valley', 'وصف': 'طبيعة خلابة' if st.session_state.lang == 'ar' else 'Stunning Nature', 'base_time': 40, 'metro_access': False}
            ]
            st.rerun()

        if st.session_state.suggestions:
            st.markdown(f"<h5>{T['m_btn'].split(' ')[0]} وسيلة الوصول:</h5>", unsafe_allow_html=True)
            no_metro = [p['الوجهة'] for p in st.session_state.suggestions if not p['metro_access']]
            t_col1, t_col2, t_col3 = st.columns(3)
            
            # منطق المواصلات (جمانة الأصلي)
            if not no_metro:
                if t_col1.button(T["m_btn"]): st.session_state.transport_choice = "مترو"
            else:
                t_col1.markdown(f'<p style="text-align:center; color:#94A3B8; font-size:0.8em; margin-top:15px;">{T["m_no"]}</p>', unsafe_allow_html=True)
                
            if t_col2.button(T["c_btn"]): st.session_state.transport_choice = "سيارة"
            if t_col3.button(T["t_btn"]): st.session_state.transport_choice = "تاكسي"

            for place in st.session_state.suggestions:
                base = place['base_time']
                choice = st.session_state.transport_choice
                if choice == "مترو": f_time = f"{base + 5} دقيقة" ; icon = "🚇"
                elif choice == "سيارة": f_time = f"{int(base * st.session_state.traffic_factor)} دقيقة" ; icon = "🚗"
                elif choice == "تاكسي": f_time = f"{int(base * st.session_state.traffic_factor) + 3} دقيقة" ; icon = "🚕"
                else: f_time = "..." ; icon = "📍"

                st.markdown(f'''<div class="info-box">
                    <h4 style="margin:0; color:#0284C7;">{icon} {place['الوجهة']}</h4>
                    <p style="margin:5px 0; color:#475569; font-size:0.9em;">{place['وصف']}</p>
                    <p style="margin:10px 0 0 0; font-weight:bold; color:#0369A1;">⏱️ الوقت المقدر: {f_time}</p>
                </div>''', unsafe_allow_html=True)

    with col_side:
        st.markdown("---")
        st.subheader(T["rating_q"])
        stars_cols = st.columns(5)
        for i in range(1, 6):
            if stars_cols[i-1].button(f"{i}⭐", key=f"s{i}"):
                st.session_state.star_rating = i
                st.toast(f"تم تسجيل تقييمك: {i} نجوم", icon="⭐")
        
        st.markdown(f"<br><p style='font-size:0.8em; color:#94A3B8; text-align:center;'>Path7 | Engineering Excellence @ IAU</p>", unsafe_allow_html=True)
        if st.button(T["reset"]):
            st.session_state.clear()
            st.rerun()
