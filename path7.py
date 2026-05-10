import streamlit as st
import random
from datetime import datetime
import pytz

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
formatted_time = now_riyadh.strftime('%I:%M %p')
current_hour = now_riyadh.hour

st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# 2. القاموس الموحد (عربي مذكر / إنجليزي رسمي)
LANG = {
    "العربية": {
        "title": "📍 Path7 | مسار 7",
        "subtitle": "نظام التوافق اللحظي للسياحة الذكية",
        "welcome_main": "مرحباً بك في الرياض",
        "budget_q": "حدد الميزانية المناسبة للرحلة",
        "start_btn": "استكشف مسارك الآن 🚀",
        "day": "اليوم", "of": "من",
        "weather": "الجو في الرياض", "sunny": "مشمس ☀️", "night": "ليل صافي 🌙",
        "interests_q": "🌟 ما هي اهتماماتك المفضلة لليوم؟",
        "analyze_btn": "تحليل الوجهات الأنسب لهذا اليوم 🔍",
        "transport_q": "كيف تفضل الوصول لوجهاتك؟",
        "metro_fail": "المترو غير متاح لهذه الوجهات ❌",
        "m_btn": "🚇 مترو الرياض", "c_btn": "🚗 سيارتي", "t_btn": "🚕 تاكسي",
        "min": "دقيقة", "est_time": "الوقت المتوقع (توافق لحظي)",
        "rating_q": "⭐ تقييمك لليوم",
        "next_day": "التوجه نحو مسار اليوم التالي ⏩",
        "finish": "✨ نتمنى لك ذكريات لا تُنسى في الرياض! ✨",
        "eco": "اقتصادية", "lux": "فاخرة",
        "reset": "🔄 ضبط جديد"
    },
    "English": {
        "title": "📍 Path7 | Smart Journey",
        "subtitle": "Real-time Compatibility System for Smart Tourism",
        "welcome_main": "Welcome to Riyadh",
        "budget_q": "Select Trip Budget",
        "start_btn": "Explore Now 🚀",
        "day": "Day", "of": "of",
        "weather": "Riyadh Weather", "sunny": "Sunny ☀️", "night": "Clear Night 🌙",
        "interests_q": "🌟 Your interests today?",
        "analyze_btn": "Analyze Destinations 🔍",
        "transport_q": "How would you like to travel?",
        "metro_fail": "Metro unavailable for these destinations ❌",
        "m_btn": "🚇 Riyadh Metro", "c_btn": "🚗 My Car", "t_btn": "🚕 Taxi",
        "min": "min", "est_time": "Real-time Arrival",
        "rating_q": "⭐ Rate Your Day",
        "next_day": "Move to Next Day ⏩",
        "finish": "✨ Wish you unforgettable memories in Riyadh! ✨",
        "eco": "Economy", "lux": "Luxury",
        "reset": "🔄 Reset"
    }
}

# 3. إدارة الحالة (Session State)
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'day' not in st.session_state: st.session_state.day = 1
if 'rated' not in st.session_state: st.session_state.rated = False
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = "car"

T = LANG[st.session_state.lang]

# 4. الستايل البصري (Glassmorphism & Gradient)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if st.session_state.lang == "العربية" else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); background-attachment: fixed; }}
    
    .glass-card {{ background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); padding: 30px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 15px 35px rgba(0,0,0,0.1); margin-bottom: 20px; }}
    .dest-card {{ background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 20px; border-{"right" if st.session_state.lang == "العربية" else "left"}: 12px solid #0EA5E9; margin-bottom: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.02); }}
    
    .stButton>button {{ background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important; color: white !important; border-radius: 12px !important; border: none !important; font-weight: 700 !important; font-size: 1.1em !important; height: 3.5em !important; transition: 0.3s !important; }}
    .stButton>button:hover {{ transform: translateY(-3px); box-shadow: 0 8px 25px rgba(2, 132, 199, 0.4) !important; }}
    [data-testid="stSidebar"] {{ display: none !important; }}
    </style>
''', unsafe_allow_html=True)

# زر تبديل اللغة
col_l1, col_l2 = st.columns([12, 1])
if col_l2.button("عربي/EN"):
    st.session_state.lang = "English" if st.session_state.lang == "العربية" else "العربية"
    st.rerun()

# البيانات
PLACES_DB = {
    "اقتصادية": [
        {"الوجهة": "حصن المصمك", "وصف": "رمز لتوحيد المملكة", "b_time": 25, "metro": True},
        {"الوجهة": "وادي حنيفة", "وصف": "طبيعة خلابة ومساحات خضراء", "b_time": 40, "metro": False}
    ],
    "فاخرة": [
        {"الوجهة": "فيا رياض", "وصف": "مطاعم عالمية وفخامة معمارية", "b_time": 18, "metro": False},
        {"الوجهة": "حي الطريف", "وصف": "تاريخ نجد العريق", "b_time": 20, "metro": True}
    ]
}

# --- الصفحات ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    with st.form("w_form"):
        st.markdown(f'<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown(f'<h1 style="color: #0369A1;">{T["title"]}</h1><p style="color:#64748B;">{T["subtitle"]}</p>', unsafe_allow_html=True)
        st.markdown("<hr style='opacity:0.1;'>", unsafe_allow_html=True)
        u_budget = st.radio(T["budget_q"], [T["eco"], T["lux"]], horizontal=True)
        if st.form_submit_button(T["start_btn"]):
            st.session_state.budget_choice = "اقتصادية" if u_budget in [T["eco"], "اقتصادية"] else "فاخرة"
            st.session_state.traffic_factor = random.uniform(1.0, 1.8) # عامل الزحمة اللحظي
            st.session_state.page = 'system'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # صفحة النظام الرئيسية
    col_m, col_s = st.columns([2, 1])
    with col_m:
        st.markdown(f'''<div class="glass-card">
            <h3 style="margin:0; color:#0369A1;">📅 {T["day"]} {st.session_state.day} {T["of"]} 3</h3>
            <p style="color:#475569;">🕒 {formatted_time} | {T["weather"]}: <b>{T["sunny"] if 5 <= current_hour <= 17 else T["night"]}</b></p>
        </div>''', unsafe_allow_html=True)

        st.subheader(T["interests_q"])
        st.multiselect("", ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق"], label_visibility="collapsed")
        
        if st.button(T["analyze_btn"]):
            st.session_state.suggestions = PLACES_DB[st.session_state.budget_choice]
            st.session_state.rated = False # تصفير التقييم لليوم الجديد
            st.rerun()

        if st.session_state.suggestions:
            st.markdown(f"### {T['transport_q']}")
            no_metro = any(not p['metro'] for p in st.session_state.suggestions)
            t_col1, t_col2, t_col3 = st.columns(3)
            
            # أزرار المواصلات
            if not no_metro:
                if t_col1.button(T["m_btn"]): st.session_state.transport_choice = "metro"
            else:
                t_col1.markdown(f'<p style="color:gray; font-size:0.8em; margin-top:10px; text-align:center;">{T["metro_fail"]}</p>', unsafe_allow_html=True)
            if t_col2.button(T["c_btn"]): st.session_state.transport_choice = "car"
            if t_col3.button(T["t_btn"]): st.session_state.transport_choice = "taxi"

            # عرض الوجهات بوقت ديناميكي (توافق لحظي)
            for place in st.session_state.suggestions:
                base = place['b_time']
                if st.session_state.transport_choice == "metro":
                    f_time = f"{base + 5} {T['min']}" ; icon = "🚇"
                elif st.session_state.transport_choice == "car":
                    f_time = f"{int(base * st.session_state.traffic_factor)} {T['min']}" ; icon = "🚗"
                elif st.session_state.transport_choice == "taxi":
                    f_time = f"{int(base * st.session_state.traffic_factor) + 3} {T['min']}" ; icon = "🚕"
                else:
                    f_time = "بانتظار اختيارك..." ; icon = "📍"

                st.markdown(f'''<div class="dest-card">
                    <h4 style="color:#0284C7; margin:0;">{icon} {place['الوجهة']}</h4>
                    <p style="color:#64748B;">{place['وصف']}</p>
                    <p style="font-weight:bold; color:#0369A1;">⏱️ {T["est_time"]}: {f_time}</p>
                </div>''', unsafe_allow_html=True)

    with col_s:
        st.markdown(f'<div class="glass-card"><h4>{T["rating_q"]}</h4>', unsafe_allow_html=True)
        
        # أزرار النجوم الخمسة (جمانة الأصلية)
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐", key=f"star_{i}"):
                st.session_state.rated = True
                st.session_state.traffic_factor = random.uniform(1.0, 1.8) # محاكاة تغير الزحمة لليوم التالي

        # الانتقال لليوم التالي (يفتح فقط بعد التقييم)
        if st.session_state.rated:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.session_state.day < 3:
                if st.button(T["next_day"]):
                    st.session_state.day += 1
                    st.session_state.suggestions = []
                    st.rerun()
            else:
                st.balloons()
                st.success(T["finish"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(T["reset"]): st.session_state.clear(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.8em; margin-top: 30px;'>Path7 | Engineering Excellence @ IAU</p>", unsafe_allow_html=True)
