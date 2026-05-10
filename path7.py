import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# 2. القاموس (عربي/إنجليزي)
TRANSLATIONS = {
    "ar": {
        "title": "📍 Path7 | المسار الذكي",
        "name_label": "اسم السائح الموقر",
        "welcome": "مرحباً يا",
        "weather_label": "الجو في الرياض",
        "weather_val": "ليل صافي 🌙" if current_hour > 18 or current_hour < 5 else "مشمس ☀️",
        "eco": "اقتصادية", "lux": "فاخرة",
        "start_btn": "استكشف مسارك الآن 🚀",
        "interests_q": "🌟 ما هي اهتماماتك المفضلة لليوم؟",
        "analyze": "تحليل الوجهات الأنسب 🔍",
        "trans_q": "🚕 اختر وسيلة المواصلات (تحديث لحظي):",
        "metro_btn": "🚇 مترو الرياض", "car_btn": "🚗 سيارتي", "taxi_btn": "🚕 تاكسي",
        "metro_no": "المترو غير متاح لهذه الوجهات ❌",
        "rating_title": "⭐ تقييمك لليوم",
        "reset": "🔄 إعادة ضبط",
        "lang_btn": "English 🌐",
        "dir": "rtl", "align": "right"
    },
    "en": {
        "title": "📍 Path7 | Smart Journey",
        "name_label": "Tourist Name",
        "welcome": "Welcome",
        "weather_label": "Riyadh Weather",
        "weather_val": "Clear Night 🌙" if current_hour > 18 or current_hour < 5 else "Sunny ☀️",
        "eco": "Economy", "lux": "Luxury",
        "start_btn": "Explore Now 🚀",
        "interests_q": "🌟 What are your interests today?",
        "analyze": "Analyze Destinations 🔍",
        "trans_q": "🚕 Choose Transport (Real-time):",
        "metro_btn": "🚇 Riyadh Metro", "car_btn": "🚗 My Car", "taxi_btn": "🚕 Taxi",
        "metro_no": "Metro unavailable for these places ❌",
        "rating_title": "⭐ Rate Your Day",
        "reset": "🔄 Reset",
        "lang_btn": "العربية 🌐",
        "dir": "ltr", "align": "left"
    }
}

# 3. قاعدة البيانات مع تفاصيل المترو
DB = {
    "Economy": {
        "ar": [
            {"الوجهة": "حصن المصمك", "الفئة": "تاريخ وآثار", "وصف": "رمز توحيد المملكة.", "base_time": 25, "metro_access": True},
            {"الوجهة": "وادي حنيفة", "الفئة": "طبيعة", "وصف": "مساحات خضراء خلابة.", "base_time": 40, "metro_access": False}
        ],
        "en": [
            {"الوجهة": "Masmak Fortress", "الفئة": "History", "وصف": "Symbol of unification.", "base_time": 25, "metro_access": True},
            {"الوجهة": "Hanifa Valley", "الفئة": "Nature", "وصف": "Beautiful landscapes.", "base_time": 40, "metro_access": False}
        ]
    },
    "Luxury": {
        "ar": [
            {"الوجهة": "فيا رياض", "الفئة": "ترفيه", "وصف": "مطاعم وسينما فاخرة.", "base_time": 15, "metro_access": False},
            {"الوجهة": "مطل البجيري", "الفئة": "مطاعم ومقاهي", "وصف": "إطلالة تاريخية فاخرة.", "base_time": 20, "metro_access": True}
        ],
        "en": [
            {"الوجهة": "Via Riyadh", "الفئة": "Entertainment", "وصف": "Luxury dining & cinema.", "base_time": 15, "metro_access": False},
            {"الوجهة": "Bujairi Terrace", "الفئة": "Dining", "وصف": "Premium historic views.", "base_time": 20, "metro_access": True}
        ]
    }
}

# 4. الحالة
for key, val in [('lang','ar'),('page','welcome'),('u_name',''),('u_budget','Economy'),('suggestions',[]),('transport_choice','none'),('traffic_factor',1.2)]:
    if key not in st.session_state: st.session_state[key] = val

T = TRANSLATIONS[st.session_state.lang]

# 5. التنسيق
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {T["dir"]}; text-align: {T["align"]}; }}
    .main-card {{ background: white; padding: 20px; border-radius: 20px; border-top: 10px solid #0284C7; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }}
    .info-box {{ background: #F8FAFC; padding: 15px; border-radius: 15px; border-{T["align"]}: 5px solid #38BDF8; margin-bottom: 10px; border: 1px solid #E2E8F0; }}
    .stButton>button {{ border-radius: 10px !important; }}
    </style>
''', unsafe_allow_html=True)

if st.button(T["lang_btn"]):
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
    st.rerun()

# --- الصفحة الأولى ---
if st.session_state.page == 'welcome':
    with st.form("w_form"):
        st.title(T["title"])
        n_in = st.text_input(T["name_label"], value=st.session_state.u_name)
        b_in = st.radio("", [T["eco"], T["lux"]], horizontal=True)
        if st.form_submit_button(T["start_btn"]):
            st.session_state.u_name = n_in if n_in else "Guest"
            st.session_state.u_budget = "Economy" if b_in in [T["eco"], "اقتصادية"] else "Luxury"
            st.session_state.page = 'system'
            st.rerun()

# --- الصفحة الثانية ---
else:
    st.markdown(f'''<div class="main-card">
        <h3>📅 اليوم 1 | {T["welcome"]} {st.session_state.u_name}</h3>
        <p>{T["weather_label"]}: <b>{T["weather_val"]}</b></p>
    </div>''', unsafe_allow_html=True)

    cats = ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"] if st.session_state.lang == 'ar' else ["History", "Entertainment", "Shopping", "Dining", "Nature"]
    u_interests = st.multiselect(T["interests_q"], cats)

    if st.button(T["analyze"]):
        st.session_state.suggestions = DB[st.session_state.u_budget][st.session_state.lang]
        st.rerun()

    if st.session_state.suggestions:
        st.write(T["trans_q"])
        # منطق المواصلات (اللي طلبتيه بالحرف)
        no_metro_places = [p['الوجهة'] for p in st.session_state.suggestions if not p['metro_access']]
        t_col1, t_col2, t_col3 = st.columns(3)
        
        if not no_metro_places:
            if t_col1.button(T["metro_btn"]): st.session_state.transport_choice = "مترو"
        else:
            t_col1.markdown(f'<p style="text-align:center; color:#94A3B8; font-size:0.8em; margin-top:15px;">{T["metro_no"]}</p>', unsafe_allow_html=True)
            
        if t_col2.button(T["car_btn"]): st.session_state.transport_choice = "سيارة"
        if t_col3.button(T["taxi_btn"]): st.session_state.transport_choice = "تاكسي"

        # عرض الوجهات وحساب الوقت
        for place in st.session_state.suggestions:
            base = place['base_time']
            if st.session_state.transport_choice == "مترو":
                final_time = f"{base + 5} دقيقة" ; icon = "🚇"
            elif st.session_state.transport_choice == "سيارة":
                final_time = f"{int(base * st.session_state.traffic_factor)} دقيقة" ; icon = "🚗"
            elif st.session_state.transport_choice == "تاكسي":
                final_time = f"{int(base * st.session_state.traffic_factor) + 3} دقيقة" ; icon = "🚕"
            else:
                final_time = "بانتظار اختيارك..." ; icon = "📍"

            st.markdown(f'''
                <div class="info-box">
                    <h4 style="margin:0; color:#0284C7;">{icon} {place['الوجهة']}</h4>
                    <p style="margin:2px 0; font-size:0.9em; color:#475569;">{place['وصف']}</p>
                    <p style="margin:10px 0 0 0; font-weight:bold; color:#0369A1;">⏱️ الوقت المقدر: {final_time}</p>
                </div>
            ''', unsafe_allow_html=True)

        # منطق النجوم (اللي طلبتيه بالحرف)
        st.markdown("---")
        st.subheader(T["rating_title"])
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐", key=f"s{i}"):
                st.session_state.star_rating = i
                st.success(f"شكراً لتقييمك: {i} نجوم!")

    if st.button(T["reset"]):
        st.session_state.clear() ; st.rerun()
