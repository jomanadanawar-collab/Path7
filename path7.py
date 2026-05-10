import streamlit as st
from datetime import datetime
import pytz 

# 1. الإعدادات والوقت
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# 2. تهيئة الجلسة (Session State) - مع إضافة نظام الأيام
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'u_name' not in st.session_state: st.session_state.u_name = ''
if 'u_budget' not in st.session_state: st.session_state.u_budget = 'Economy'
if 'day_number' not in st.session_state: st.session_state.day_number = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = 'none'
if 'rated' not in st.session_state: st.session_state.rated = False

# 3. القاموس (مُحدث ليشمل زر اليوم التالي)
TRANSLATIONS = {
    "ar": {
        "title": "📍 Path7 | المسار الذكي", "name_label": "اسم السائح الموقر", "start": "استكشف مسارك الآن 🚀",
        "welcome": "مرحباً يا", "day": "اليوم", "weather": "الجو في الرياض",
        "weather_val": "ليل صافي 🌙" if current_hour > 18 or current_hour < 5 else "مشمس ☀️",
        "interests_q": "🌟 ما هي اهتماماتك المفضلة لليوم؟", "analyze": "تحليل الوجهات 🔍",
        "m_no": "المترو غير متاح ❌", "m_btn": "🚇 مترو", "c_btn": "🚗 سيارة", "t_btn": "🚕 تاكسي",
        "rating_q": "⭐ تقييمك لليوم", "next_day": "الانتقال لليوم التالي ➡️", "reset": "🔄 إعادة ضبط",
        "lang_btn": "English 🌐", "dir": "rtl", "align": "right", "eco": "اقتصادية", "lux": "فاخرة"
    },
    "en": {
        "title": "📍 Path7 | Smart Journey", "name_label": "Tourist Name", "start": "Explore Now 🚀",
        "welcome": "Welcome", "day": "Day", "weather": "Riyadh Weather",
        "weather_val": "Clear Night 🌙" if current_hour > 18 or current_hour < 5 else "Sunny ☀️",
        "interests_q": "🌟 Your interests today?", "analyze": "Analyze 🔍",
        "m_no": "No Metro ❌", "m_btn": "🚇 Metro", "c_btn": "🚗 Car", "t_btn": "🚕 Taxi",
        "rating_q": "⭐ Rate Your Day", "next_day": "Next Day ➡️", "reset": "🔄 Reset",
        "lang_btn": "العربية 🌐", "dir": "ltr", "align": "left", "eco": "Economy", "lux": "Luxury"
    }
}
T = TRANSLATIONS[st.session_state.lang]

# 4. التنسيق (CSS)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {T["dir"]}; text-align: {T["align"]}; }}
    .stApp {{ background-color: #F8FAFC !important; }}
    .main-card {{ background: white; padding: 25px; border-radius: 20px; border-top: 10px solid #0284C7; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; }}
    .info-box {{ background: white; padding: 15px; border-radius: 15px; border-{"right" if st.session_state.lang == "ar" else "left"}: 6px solid #38BDF8; margin-bottom: 10px; border: 1px solid #E2E8F0; }}
    .stButton>button {{ width: 100%; border-radius: 10px !important; font-weight: bold; transition: 0.3s; }}
    .next-btn>button {{ background: #10B981 !important; color: white !important; border: none !important; height: 3em; font-size: 1.1em !important; }}
    </style>
''', unsafe_allow_html=True)

# 5. منطق الصفحات
if st.session_state.page == 'welcome':
    if st.button(T["lang_btn"]): st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'; st.rerun()
    with st.form("w"):
        st.markdown(f"<h1 style='text-align:center;'>{T['title']}</h1>", unsafe_allow_html=True)
        u_name = st.text_input(T["name_label"])
        u_budget = st.radio("", [T["eco"], T["lux"]], horizontal=True)
        if st.form_submit_button(T["start"]):
            st.session_state.u_name = u_name if u_name else "Jomanah"
            # حل مشكلة الـ KeyError بتوحيد المسميات
            st.session_state.u_budget = 'Luxury' if (u_budget in ['فاخرة', 'Luxury']) else 'Economy'
            st.session_state.page = 'system'
            st.rerun()

else:
    col_m, col_s = st.columns([2, 1])
    with col_m:
        st.markdown(f'''<div class="main-card">
            <h2>📅 {T["day"]} {st.session_state.day_number} | {T["welcome"]} {st.session_state.u_name}</h2>
            <p>{T["weather"]}: <b>{T["weather_val"]}</b> | الميزانية: <b>{st.session_state.u_budget}</b></p>
        </div>''', unsafe_allow_html=True)
        
        cats = ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"] if st.session_state.lang == 'ar' else ["History", "Entertainment", "Shopping", "Dining", "Nature"]
        st.multiselect(T["interests_q"], cats)
        
        if st.button(T["analyze"]):
            # محاكاة لبيانات اليوم (يمكنك استبدالها بـ Database حقيقية)
            st.session_state.suggestions = [
                {'name': 'حصن المصمك' if st.session_state.lang == 'ar' else 'Masmak Fortress', 'm': True},
                {'name': 'بوليفارد سيتي' if st.session_state.lang == 'ar' else 'Boulevard City', 'm': False}
            ]
            st.rerun()

        if st.session_state.suggestions:
            c1, c2, c3 = st.columns(3)
            if c1.button(T["m_btn"]): st.session_state.transport_choice = "مترو"
            if c2.button(T["c_btn"]): st.session_state.transport_choice = "سيارة"
            if c3.button(T["t_btn"]): st.session_state.transport_choice = "تاكسي"

            for p in st.session_state.suggestions:
                st.markdown(f'<div class="info-box"><h4>📍 {p["name"]}</h4><p>وسيلة النقل: {st.session_state.transport_choice}</p></div>', unsafe_allow_html=True)

    with col_s:
        st.markdown("---")
        st.subheader(T["rating_q"])
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐"):
                st.session_state.rated = True
                st.success(f"شكراً لتقييمك!")
        
        # --- الزر الذي سيقودك للفوز (الانتقال لليوم التالي) ---
        if st.session_state.rated:
            st.markdown('<div class="next-btn">', unsafe_allow_html=True)
            if st.button(T["next_day"]):
                if st.session_state.day_number < 3:
                    st.session_state.day_number += 1
                    st.session_state.suggestions = []
                    st.session_state.rated = False
                    st.session_state.transport_choice = 'none'
                    st.rerun()
                else:
                    st.balloons()
                    st.success("أتممت رحلة الـ 3 أيام بنجاح!")
            st.markdown('</div>', unsafe_allow_html=True)

        if st.button(T["reset"]): st.session_state.clear(); st.rerun()
