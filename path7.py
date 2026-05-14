import streamlit as st
import json
from datetime import datetime
import pytz

# 1. تحميل البيانات
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

DATA_ALL = load_data()

# 2. الوقت (الساعة)
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz).strftime("%I:%M %p")
hour = datetime.now(riyadh_tz).hour

# 3. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'lang_selection'
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'day' not in st.session_state: st.session_state.day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'rated' not in st.session_state: st.session_state.rated = False

IS_AR = st.session_state.lang == "العربية"

# خريطة ربط الاهتمامات لضمان عمل التحليل في الإنجليزية
category_map = {
    "History": "تاريخ وآثار", "Entertainment": "ترفيه", 
    "Nature": "طبيعة", "Shopping": "تسوق", "Dining": "مطاعم ومقاهي"
}

strings = {
    "title": "Path7 📍",
    "sub": "نظام التوافق اللحظي للسياحة الذكية" if IS_AR else "Real-time Smart Tourism System",
    "name_q": "مرحباً بك، ما هو اسمك؟" if IS_AR else "Welcome, what is your name?",
    "budget_q": "حدد طابع رحلتك اليوم:" if IS_AR else "Choose your trip style:",
    "budgets": ["اقتصادية", "فاخرة"] if IS_AR else ["Economy", "Luxury"],
    "start_btn": "انطلق 🚀" if IS_AR else "Explore 🚀",
    "day_lbl": f"📅 يوم {st.session_state.day}" if IS_AR else f"📅 Day {st.session_state.day}",
    "interests_q": "ما هي اهتماماتك؟" if IS_AR else "Interests:",
    "interests_list": ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"] if IS_AR else ["History", "Entertainment", "Nature", "Shopping", "Dining"],
    "analyze_btn": "تحليل المسار 🔍" if IS_AR else "Analyze Path 🔍",
    "trans_q": "وسيلة النقل" if IS_AR else "Transport",
    "metro": "🚇 المترو" if IS_AR else "🚇 Metro",
    "car": "🚗 السيارة" if IS_AR else "🚗 Car",
    "taxi": "🚕 التاكسي" if IS_AR else "🚕 Taxi",
    "est_time": "الوقت المقدر:" if IS_AR else "Est. Time:",
    "mins": "دقيقة" if IS_AR else "mins",
    "map_btn": "📍 فتح في الخرائط" if IS_AR else "📍 Open Maps",
    "select_trans": "⏳ حدد وسيلة النقل" if IS_AR else "⏳ Select transport",
    "rating_t": "تقييمك ⭐" if IS_AR else "Rate ⭐"
}

# 4. التنسيق (إجبار المربعات 1:1)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if IS_AR else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 25px; border-radius: 25px; margin-bottom: 20px; }}
    .dest-card {{ background: white; padding: 20px; border-radius: 20px; border-{"right" if IS_AR else "left"}: 10px solid #0EA5E9; margin-bottom: 15px; color: black; }}
    
    /* إجبار أزرار النجوم على أن تكون مربعة تماماً */
    div[data-testid="stHorizontalBlock"] div[data-testid="column"] button {{
        width: 60px !important;
        height: 60px !important;
        min-width: 60px !important;
        max-width: 60px !important;
        aspect-ratio: 1/1 !important;
        padding: 0 !important;
        border-radius: 10px !important;
        background-color: #0284C7 !important;
        color: white !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    .stButton>button {{ background: linear-gradient(90deg, #0284C7, #38BDF8) !important; color: white !important; border-radius: 10px !important; }}
    </style>
''', unsafe_allow_html=True)

# --- الصفحات ---
if st.session_state.page == 'lang_selection':
    st.markdown('<div class="glass-card" style="text-align: center;"><h1>Path7 📍</h1><p>Choose Language / اختر اللغة</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("English 🇬🇧"):
        st.session_state.lang = "English"; st.session_state.page = 'welcome'; st.rerun()
    if c2.button("العربية 🇸🇦"):
        st.session_state.lang = "العربية"; st.session_state.page = 'welcome'; st.rerun()

elif st.session_state.page == 'welcome':
    st.markdown(f'<div class="glass-card" style="text-align: center;"><h1>{strings["title"]}</h1><p>{strings["sub"]}</p></div>', unsafe_allow_html=True)
    st.session_state.user_name = st.text_input(strings["name_q"])
    u_budget = st.radio(strings["budget_q"], strings["budgets"], horizontal=True)
    if st.button(strings["start_btn"]):
        st.session_state.budget_key = "Luxury" if (u_budget in ["Luxury", "فاخرة"]) else "Economy"
        st.session_state.page = 'system'; st.rerun()

else:
    col_m, col_s = st.columns([2.2, 1])
    with col_m:
        st.markdown(f'<div class="glass-card"><h3>{strings["day_lbl"]}</h3><p>👤 {st.session_state.user_name} | 🕒 {now_riyadh}</p></div>', unsafe_allow_html=True)
        selected = st.multiselect(strings["interests_q"], strings["interests_list"])
        
        if st.button(strings["analyze_btn"]):
            # التحقق من اللغة وجلب البيانات الصحيحة
            lang_key = "العربية" if IS_AR else "English"
            db = DATA_ALL.get(lang_key, {}).get("db", {}).get(st.session_state.budget_key, [])
            
            # معالجة الاهتمامات المترجمة للبحث في الـ JSON
            search_terms = [category_map.get(s, s) for s in selected] if not IS_AR else selected
            st.session_state.suggestions = [p for p in db if p.get('الفئة') in search_terms] or db[:2]
            st.session_state.transport_choice = None; st.rerun()

        if st.session_state.suggestions:
            st.markdown(f"### {strings['trans_q']}")
            t_cols = st.columns(3)
            if t_cols[0].button(strings["metro"]): st.session_state.transport_choice = "metro"
            if t_cols[1].button(strings["car"]): st.session_state.transport_choice = "car"
            if t_cols[2].button(strings["taxi"]): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                d_name, d_desc = p["الوجهة"], p["وصف"]
                action_html = f"<p style='color:#94A3B8;'>{strings['select_trans']}</p>"
                if st.session_state.transport_choice:
                    t_val = p.get('b_time', 20)
                    action_html = f"<b>{strings['est_time']} {t_val} {strings['mins']}</b><br><a href='http://maps.google.com/?q={d_name}' target='_blank' style='background-color:#0284C7; color:white; padding:8px 15px; border-radius:10px; text-decoration:none; display:inline-block; margin-top:10px;'>{strings['map_btn']}</a>"
                st.markdown(f'<div class="dest-card"><h4>{d_name}</h4><p>{d_desc}</p>{action_html}</div>', unsafe_allow_html=True)

    with col_s:
        st.markdown(f'<div class="glass-card" style="text-align:center;"><h4>{strings["rating_t"]}</h4>', unsafe_allow_html=True)
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}", key=f"s{i}"): st.session_state.rated = True
        if st.session_state.rated and st.button("Next Day"):
            st.session_state.day += 1; st.session_state.rated = False; st.rerun()
        if st.button("Reset 🔄"): st.session_state.clear(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
