import streamlit as st
import json
from datetime import datetime
import pytz
import random
import time
import requests

# =========================
# تحميل البيانات
# =========================
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

DATA_ALL = load_data()

# =========================
# الوقت الحالي
# =========================
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
hour = now_riyadh.hour

# =========================
# Session State
# =========================
if 'lang' not in st.session_state:
    st.session_state.lang = "العربية"

if 'lang_selected' not in st.session_state:
    st.session_state.lang_selected = False

if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

if 'day' not in st.session_state:
    st.session_state.day = 1

if 'suggestions' not in st.session_state:
    st.session_state.suggestions = []

if 'transport_choice' not in st.session_state:
    st.session_state.transport_choice = None

if 'rated' not in st.session_state:
    st.session_state.rated = False

# =========================
# اللغة
# =========================
IS_AR = st.session_state.lang == "العربية"

# =========================
# الطقس API
# =========================
try:
    API_KEY = "YOUR_API_KEY"

    city = "Riyadh"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url).json()

    temp = round(response['main']['temp'])
    weather_desc = response['weather'][0]['description']

    WEATHER_NOW = f"🌡️ {temp}°C | {weather_desc}"

except:
    WEATHER_NOW = (
        "مشمس ☀️" if 5 <= hour <= 17 else "صافي 🌙"
    ) if IS_AR else (
        "Sunny ☀️" if 5 <= hour <= 17 else "Clear 🌙"
    )

# =========================
# النصوص
# =========================
strings = {

    "title": "Path7 📍",

    "sub":
    "نظام التوافق اللحظي للسياحة الذكية"
    if IS_AR else
    "Real-time Smart Tourism System",

    "name_q":
    "مرحباً بك، ما هو اسمك؟"
    if IS_AR else
    "Welcome, what is your name?",

    "budget_q":
    "حدد طابع رحلتك اليوم:"
    if IS_AR else
    "Choose your trip style:",

    "budgets":
    ["اقتصادية", "فاخرة"]
    if IS_AR else
    ["Economy", "Luxury"],

    "start_btn":
    "انطلق لاستكشاف الرياض 🚀"
    if IS_AR else
    "Explore Riyadh 🚀",

    "day_lbl":
    f"📅 يوم {st.session_state.day} من 3"
    if IS_AR else
    f"📅 Day {st.session_state.day} of 3",

    "interests_q":
    "ما هي اهتماماتك المفضلة اليوم؟"
    if IS_AR else
    "What are your interests today?",

    "interests_list":
    ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"]
    if IS_AR else
    ["History", "Entertainment", "Nature", "Shopping", "Dining"],

    "analyze_btn":
    "تحليل المسار الذكي 🔍"
    if IS_AR else
    "Smart Path Analysis 🔍",

    "trans_q":
    "وسيلة النقل المفضلة"
    if IS_AR else
    "Preferred Transport",

    "metro":
    "🚇 المترو"
    if IS_AR else
    "🚇 Metro",

    "car":
    "🚗 السيارة"
    if IS_AR else
    "🚗 Car",

    "taxi":
    "🚕 التاكسي"
    if IS_AR else
    "🚕 Taxi",

    "est_time":
    "الوقت المقدر:"
    if IS_AR else
    "Est. Time:",

    "mins":
    "دقيقة"
    if IS_AR else
    "mins",

    "map_btn":
    "📍 فتح في الخرائط"
    if IS_AR else
    "📍 Open Maps",

    "metro_msg":
    "محطة المترو قريبة منك."
    if IS_AR else
    "Metro station is nearby.",

    "select_trans":
    "⏳ حدد وسيلة النقل لمعرفة المسار"
    if IS_AR else
    "⏳ Select transport to see path",

    "rating_t":
    "تقييمك للتجربة ⭐"
    if IS_AR else
    "Rate your experience ⭐",

    "next_day":
    "اليوم التالي ⏭️"
    if IS_AR else
    "Next Day ⏭️",

    "reset":
    "إعادة ضبط 🔄"
    if IS_AR else
    "Reset 🔄",

    "final_msg":
    "شكرًا لثقتك بـ Path7.. نتمنى لك رحلة سعيدة! ✨"
    if IS_AR else
    "Thank you for trusting Path7.. Have a great trip! ✨"
}

# =========================
# اتجاه النص
# =========================
text_align = "right" if IS_AR else "left"

# =========================
# تصميم CSS
# =========================
st.markdown(f'''
<style>

@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');

* {{
    font-family: 'IBM Plex Sans Arabic', sans-serif !important;
    direction: {"rtl" if IS_AR else "ltr"};
}}

.stApp {{
    background:
    linear-gradient(rgba(255,255,255,0.82), rgba(255,255,255,0.82)),
    url('https://images.unsplash.com/photo-1580674285054-bed31e145f59');

    background-size: cover;
    background-attachment: fixed;
}}

.glass-card {{
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(12px);
    padding: 25px;
    border-radius: 25px;
    border: 1px solid rgba(255,255,255,0.3);
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    text-align: {text_align};
}}

.center-rating {{
    text-align: center !important;
}}

.dest-card {{
    background: white;
    padding: 20px;
    border-radius: 20px;
    border-{"right" if IS_AR else "left"}: 10px solid #0EA5E9;
    margin-bottom: 15px;
    text-align: {text_align};
}}

.map-btn {{
    background-color: #0284C7;
    color: white !important;
    padding: 8px 16px;
    border-radius: 10px;
    text-decoration: none;
    font-weight: bold;
    display: inline-block;
    margin-top: 10px;
}}

.stButton>button {{
    background: linear-gradient(90deg, #0284C7, #38BDF8) !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
}}

</style>
''', unsafe_allow_html=True)

# =========================
# صفحة اختيار اللغة
# =========================
if not st.session_state.lang_selected:

    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:60px;">
        <h1 style="font-size:60px;">Path7 📍</h1>
        <p style="font-size:22px;">
        Choose Your Language | اختر لغتك
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("العربية 🇸🇦"):
            st.session_state.lang = "العربية"
            st.session_state.lang_selected = True
            st.rerun()

    with col2:
        if st.button("English 🇬🇧"):
            st.session_state.lang = "English"
            st.session_state.lang_selected = True
            st.rerun()

    st.stop()

# =========================
# صفحة البداية
# =========================
if st.session_state.page == 'welcome':

    st.markdown(f'''
    <div class="glass-card" style="text-align:center;">
        <h1>{strings["title"]}</h1>
        <p>{strings["sub"]}</p>
    </div>
    ''', unsafe_allow_html=True)

    col_w1, col_w2, col_w3 = st.columns([1,2,1])

    with col_w2:

        st.session_state.user_name = st.text_input(strings["name_q"])

        u_budget = st.radio(
            strings["budget_q"],
            strings["budgets"],
            horizontal=True
        )

        if st.button(strings["start_btn"]):

            st.session_state.budget_key = (
                "Luxury"
                if (u_budget == "فاخرة" or u_budget == "Luxury")
                else "Economy"
            )

            st.session_state.page = 'system'

            st.rerun()

# =========================
# النظام
# =========================
else:

    col_m, col_s = st.columns([2.2, 1])

    with col_m:

        st.progress(st.session_state.day / 3)

        st.markdown(f'''
        <div class="glass-card">
            <h3>{strings["day_lbl"]}</h3>

            <p>
            👤 {st.session_state.user_name}
            |
            🕒 {now_riyadh.strftime("%I:%M %p")}
            |
            {WEATHER_NOW}
            </p>

        </div>
        ''', unsafe_allow_html=True)

        st.subheader(strings["interests_q"])

        selected = st.multiselect(
            "",
            strings["interests_list"],
            label_visibility="collapsed"
        )

        if st.button(strings["analyze_btn"]):

            with st.spinner(
                "جاري تحليل المسار الذكي..."
                if IS_AR else
                "Analyzing Smart Route..."
            ):
                time.sleep(2)

            db = DATA_ALL.get(
                st.session_state.lang,
                {}
            ).get(
                "db",
                {}
            ).get(
                st.session_state.budget_key,
                []
            )

            filtered = [
                p for p in db
                if p.get('الفئة') in selected
            ]

            # =========================
            # التوافق اللحظي
            # =========================
            if hour >= 18:

                filtered = [
                    p for p in filtered
                    if (
                        "مول" in p["الوجهة"]
                        or
                        "بوليفارد" in p["الوجهة"]
                    )
                ] or filtered

            elif 6 <= hour <= 11:

                filtered = [
                    p for p in filtered
                    if (
                        "كافيه" in p["وصف"]
                        or
                        "فطور" in p["وصف"]
                    )
                ] or filtered

            st.session_state.suggestions = filtered or db[:2]

            st.session_state.transport_choice = None

            st.rerun()

        # =========================
        # عرض الاقتراحات
        # =========================
        if st.session_state.suggestions:

            st.markdown(f"### {strings['trans_q']}")

            t_cols = st.columns(3)

            if t_cols[0].button(strings["metro"]):
                st.session_state.transport_choice = "metro"

            if t_cols[1].button(strings["car"]):
                st.session_state.transport_choice = "car"

            if t_cols[2].button(strings["taxi"]):
                st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:

                crowd = random.choice([
                    "🟢 غير مزدحم",
                    "🟡 مزدحم جزئياً",
                    "🔴 مزدحم حالياً"
                ]) if IS_AR else random.choice([
                    "🟢 Not Crowded",
                    "🟡 Moderately Busy",
                    "🔴 Crowded"
                ])

                action_html = f"""
                <p style='color:#94A3B8;'>
                {strings['select_trans']}
                </p>
                """

                if st.session_state.transport_choice:

                    base = p.get('b_time', 20)

                    t_val = (
                        base + 10
                        if st.session_state.transport_choice == "metro"
                        else int(base * 1.4)
                    )

                    time_str = f"""
                    <b>
                    {strings['est_time']}
                    {t_val}
                    {strings['mins']}
                    </b>
                    """

                    if st.session_state.transport_choice == "metro":

                        action_html = f"""
                        {time_str}

                        <p style='color:#0284C7;'>
                        {strings['metro_msg']}
                        </p>
                        """

                    else:

                        action_html = f"""
                        {time_str}

                        <br>

                        <a href='http://maps.google.com/?q={p["الوجهة"]}'
                        target='_blank'
                        class='map-btn'>

                        {strings['map_btn']}

                        </a>
                        """

                st.markdown(f'''
                <div class="dest-card">

                    <h4 style="color:#0284C7;margin:0;">
                    {p["الوجهة"]}
                    </h4>

                    <p>{p["وصف"]}</p>

                    <p><b>{crowd}</b></p>

                    {action_html}

                </div>
                ''', unsafe_allow_html=True)

    # =========================
    # التقييم
    # =========================
    with col_s:

        st.markdown(f'''
        <div class="glass-card center-rating">

        <h4>{strings["rating_t"]}</h4>

        ''', unsafe_allow_html=True)

        stars = st.columns(5)

        for i in range(1, 6):

            if stars[i-1].button(f"{i}⭐", key=f"s{i}"):

                st.session_state.rated = True

        if st.session_state.rated:

            if st.session_state.day < 3:

                if st.button(strings["next_day"]):

                    st.session_state.day += 1

                    st.session_state.suggestions = []

                    st.session_state.transport_choice = None

                    st.session_state.rated = False

                    st.rerun()

            else:

                st.info(strings["final_msg"])

        st.markdown("<hr>", unsafe_allow_html=True)

        if st.button(strings["reset"]):

            st.session_state.clear()

            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Footer
# =========================
st.markdown("""
<p style='text-align:center;
color:#94A3B8;
font-size:0.8em;'>

Path7 | Engineering Excellence @ IAU

</p>
""", unsafe_allow_html=True)
