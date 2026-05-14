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

# 2. التوافق اللحظي
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)

# 3. إدارة الحالة واللغة
if 'lang' not in st.session_state: st.session_state.lang = "English"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'day' not in st.session_state: st.session_state.day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'rated' not in st.session_state: st.session_state.rated = False

IS_AR = st.session_state.lang == "العربية"

# قاموس الترجمة الشامل (تأكدي من إضافة كل أماكنك هنا)
translation_dict = {
    "تاريخ وآثار": "History & Heritage",
    "ترفيه": "Entertainment",
    "طبيعة": "Nature",
    "تسوق": "Shopping",
    "مطاعم ومقاهي": "Dining & Cafes",
    "فيا الرياض": "Via Riyadh",
    "فخامة السينما والمطاعم": "Luxury cinema and dining",
    "البوليفارد": "Boulevard",
    "روح الترفيه العالمية": "The spirit of global entertainment",
    "مطل البجيري": "Bujairi Terrace",
    "إطلالة ساحرة ومطاعم فاخرة": "Stunning views and luxury dining"
}
rev_trans = {v: k for k, v in translation_dict.items()}

strings = {
    "title": "Path7 📍",
    "sub": "Real-time Smart Tourism System" if not IS_AR else "نظام التوافق اللحظي للسياحة الذكية",
    "name_q": "Welcome, what is your name?" if not IS_AR else "مرحباً بك، ما هو اسمك؟",
    "budget_q": "Choose your trip style:" if not IS_AR else "حدد طابع رحلتك اليوم:",
    "budgets": ["Economy", "Luxury"] if not IS_AR else ["اقتصادية", "فاخرة"],
    "start_btn": "Explore Riyadh 🚀" if not IS_AR else "انطلق لاستكشاف الرياض 🚀",
    "day_lbl": f"📅 Day {st.session_state.day} of 3" if not IS_AR else f"📅 يوم {st.session_state.day} من 3",
    "interests_q": "What are your interests today?" if not IS_AR else "ما هي اهتماماتك المفضلة اليوم؟",
    "interests_list": list(translation_dict.values()) if not IS_AR else list(translation_dict.keys()),
    "analyze_btn": "Analyze Smart Path 🔍" if not IS_AR else "تحليل المسار الذكي 🔍",
    "trans_q": "Preferred Transport" if not IS_AR else "وسيلة النقل المفضلة",
    "metro": "🚇 Metro" if not IS_AR else "🚇 المترو",
    "car": "🚗 Car" if not IS_AR else "🚗 السيارة",
    "taxi": "🚕 Taxi" if not IS_AR else "🚕 التاكسي",
    "est_time": "Est. Time:" if not IS_AR else "الوقت المقدر:",
    "mins": "mins" if not IS_AR else "دقيقة",
    "map_btn": "📍 Open in Maps" if not IS_AR else "📍 فتح في الخرائط",
    "select_trans": "⏳ Select transport to see path" if not IS_AR else "⏳ حدد وسيلة النقل لمعرفة المسار",
    "rating_t": "Rate your experience ⭐" if not IS_AR else "تقييمك للتجربة ⭐",
    "next_day": "Next Day ⏭️" if not IS_AR else "اليوم التالي ⏭️",
    "reset": "Reset 🔄" if not IS_AR else "إعادة ضبط 🔄"
}

# 4. التنسيق البصري (الأصلي + أزرار مربعة قسرية)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if IS_AR else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); background-attachment: fixed; }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 25px; border-radius: 25px; margin-bottom: 20px; }}
    .dest-card {{ background: white; padding: 20px; border-radius: 20px; margin-bottom: 5px; color: black; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
    
    /* إجبار أزرار النجوم لتكون مربعة تماماً */
    [data-testid="stHorizontalBlock"] button[key^="s"] {{
        width: 55px !important; height: 55px !important; min-width: 55px !important;
        aspect-ratio: 1/1 !important; border-radius: 10px !important;
        background-color: #0284C7 !important; color: white !important; border: none !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
    }}
    
    .stButton>button {{ background: #0284C7 !important; color: white !important; border-radius: 10px !important; }}
    </style>
''', unsafe_allow_html=True)

# زر تبديل اللغة
if st.sidebar.button("Switch Language 🌐"):
    st.session_state.lang = "العربية" if not IS_AR else "English"
    st.rerun()

if st.session_state.page == 'welcome':
    st.markdown(f'<div class="glass-card" style="text-align: center;"><h1>{strings["title"]}</h1><p>{strings["sub"]}</p></div>', unsafe_allow_html=True)
    st.session_state.user_name = st.text_input(strings["name_q"])
    u_budget = st.radio(strings["budget_q"], strings["budgets"], horizontal=True)
    if st.button(strings["start_btn"]):
        st.session_state.budget_key = "Luxury" if (u_budget in ["Luxury", "فاخرة"]) else "Economy"
        st.session_state.page = 'system'; st.rerun()

else:
    col_m, col_s = st.columns([2.2, 1.2])
    with col_m:
        st.markdown(f'<div class="glass-card"><h3>{strings["day_lbl"]}</h3><p>👤 {st.session_state.user_name}</p></div>', unsafe_allow_html=True)
        selected = st.multiselect(strings["interests_q"], strings["interests_list"])
        
        if st.button(strings["analyze_btn"]):
            db = DATA_ALL.get("العربية", {}).get("db", {}).get(st.session_state.budget_key, [])
            search_terms = [rev_trans.get(i, i) for i in selected]
            st.session_state.suggestions = [p for p in db if p.get('الفئة') in search_terms] or db[:2]
            st.rerun()

        if st.session_state.suggestions:
            st.markdown(f"### {strings['trans_q']}")
            t1, t2, t3 = st.columns(3)
            if t1.button(strings["metro"]): st.session_state.transport_choice = "metro"
            if t2.button(strings["car"]): st.session_state.transport_choice = "car"
            if t3.button(strings["taxi"]): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                # ترجمة الأسماء والأوصاف بناءً على اللغة المختارة
                d_name = translation_dict.get(p["الوجهة"], p["الوجهة"]) if not IS_AR else p["الوجهة"]
                d_desc = translation_dict.get(p["وصف"], p["وصف"]) if not IS_AR else p["وصف"]
                
                # البطاقة البيضاء
                st.markdown(f'<div class="dest-card"><h3>{d_name}</h3><p>{d_desc}</p></div>', unsafe_allow_html=True)
                
                # إظهار الوقت والخرائط تحت البطاقة مباشرة (الشكل القديم)
                if st.session_state.transport_choice:
                    t_val = p.get('b_time', 20)
                    st.markdown(f"<p style='color: #555; font-size: 0.9em; margin-bottom: 5px;'>{strings['est_time']} {t_val} {strings['mins']}</p>", unsafe_allow_html=True)
                    st.link_button(strings["map_btn"], f"https://www.google.com/maps/search/?api=1&query={d_name}")
                else:
                    st.info(strings["select_trans"])

    with col_s:
        st.markdown(f'<div class="glass-card"><h4>{strings["rating_t"]}</h4>', unsafe_allow_html=True)
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐", key=f"s{i}"): st.session_state.rated = True
        
        if st.session_state.rated:
            if st.button(strings["next_day"]):
                st.session_state.day += 1; st.session_state.rated = False; st.rerun()
        
        if st.button(strings["reset"]): st.session_state.clear(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
