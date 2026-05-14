import streamlit as st
import json
from datetime import datetime
import pytz

# 1. تحميل البيانات مع خاصية التخزين المؤقت لسرعة الاستجابة
@st.cache_data
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

DATA_ALL = load_data()

# 2. إعدادات الوقت والمنطقة الزمنية
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
hour = now_riyadh.hour

# تهيئة متغيرات الحالة (Session State)
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'day' not in st.session_state: st.session_state.day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'rated' not in st.session_state: st.session_state.rated = False

IS_AR = st.session_state.lang == "العربية"

# قاموس نصوص الواجهة
strings = {
    "title": "Path7 📍",
    "sub": "نظام التوافق اللحظي للسياحة الذكية" if IS_AR else "Real-time Smart Tourism System",
    "name_q": "مرحباً بك، ما هو اسمك؟" if IS_AR else "Welcome, what is your name?",
    "budget_q": "حدد طابع رحلتك اليوم:" if IS_AR else "Choose your trip style:",
    "budgets": ["اقتصادية", "فاخرة"] if IS_AR else ["Economy", "Luxury"],
    "start_btn": "انطلق لاستكشاف الرياض 🚀" if IS_AR else "Explore Riyadh 🚀",
    "day_lbl": f"📅 يوم {st.session_state.day} من 3" if IS_AR else f"📅 Day {st.session_state.day} of 3",
    "weather": ("مشمس ☀️" if 5 <= hour <= 17 else "صافي 🌙") if IS_AR else ("Sunny ☀️" if 5 <= hour <= 17 else "Clear 🌙"),
    "interests_q": "ما هي اهتماماتك المفضلة اليوم؟" if IS_AR else "What are your interests today?",
    "interests_list": ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"] if IS_AR else ["History", "Entertainment", "Nature", "Shopping", "Dining"],
    "analyze_btn": "تحليل المسار الذكي 🔍" if IS_AR else "Smart Path Analysis 🔍",
    "trans_q": "وسيلة النقل المفضلة" if IS_AR else "Preferred Transport",
    "metro": "🚇 المترو" if IS_AR else "🚇 Metro",
    "car": "🚗 السيارة" if IS_AR else "🚗 Car",
    "taxi": "🚕 التاكسي" if IS_AR else "🚕 Taxi",
    "est_time": "الوقت المقدر:" if IS_AR else "Est. Time:",
    "mins": "دقيقة" if IS_AR else "mins",
    "map_btn": "📍 فتح في الخرائط" if IS_AR else "📍 Open Maps",
    "metro_msg": "محطة المترو قريبة منك." if IS_AR else "Metro station is nearby.",
    "select_trans": "⏳ حدد وسيلة النقل لمعرفة المسار" if IS_AR else "⏳ Select transport to see path",
    "rating_t": "تقييمك للتجربة ⭐" if IS_AR else "Rate your experience ⭐",
    "next_day": "اليوم التالي ⏭️" if IS_AR else "Next Day ⏭️",
    "reset": "إعادة ضبط 🔄" if IS_AR else "Reset 🔄"
}

# 3. التنسيق البصري (هوية Path7)
text_align = "right" if IS_AR else "left"
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if IS_AR else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); background-attachment: fixed; }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 25px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 15px 35px rgba(0,0,0,0.1); margin-bottom: 20px; text-align: {text_align}; }}
    .dest-card {{ background: white; padding: 20px; border-radius: 20px; border-{"right" if IS_AR else "left"}: 10px solid #0EA5E9; margin-bottom: 15px; color: black; }}
    .map-btn {{ background-color: #0284C7; color: white !important; padding: 8px 16px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 10px; }}
    
    /* تنسيق أزرار التقييم المربعة 1:1 */
    div[data-testid="stHorizontalBlock"] button[key^="s"] {{
        aspect-ratio: 1/1 !important;
        width: 55px !important; height: 55px !important;
        min-width: 55px !important; padding: 0 !important;
        border-radius: 12px !important;
    }}
    </style>
''', unsafe_allow_html=True)

# زر تبديل اللغة في الزاوية
col_l1, col_l2 = st.columns([12, 2])
if col_l2.button("AR/EN"):
    st.session_state.lang = "English" if IS_AR else "العربية"
    st.rerun()

# --- الصفحات ---
if st.session_state.page == 'welcome':
    st.markdown(f'<div class="glass-card" style="text-align: center;"><h1>{strings["title"]}</h1><p>{strings["sub"]}</p></div>', unsafe_allow_html=True)
    col_w1, col_w2, col_w3 = st.columns([1, 2, 1])
    with col_w2:
        st.session_state.user_name = st.text_input(strings["name_q"])
        u_budget = st.radio(strings["budget_q"], strings["budgets"], horizontal=True)
        if st.button(strings["start_btn"]):
            st.session_state.budget_key = "Luxury" if (u_budget in ["فاخرة", "Luxury"]) else "Economy"
            st.session_state.page = 'system'; st.rerun()

else:
    col_m, col_s = st.columns([2.2, 1])
    with col_m:
        st.markdown(f'<div class="glass-card"><h3>{strings["day_lbl"]}</h3><p>👤 {st.session_state.user_name} | 🕒 {now_riyadh.strftime("%I:%M %p")} | 🌤️ {strings["weather"]}</p></div>', unsafe_allow_html=True)
        
        st.subheader(strings["interests_q"])
        selected = st.multiselect("", strings["interests_list"], label_visibility="collapsed")
        
        if st.button(strings["analyze_btn"]):
            # الحل الجوهري: ربط اللغات برمجياً
            db = []
            # البحث عن مفتاح اللغة الصحيح في ملف الـ JSON
            for k in DATA_ALL.keys():
                if k.lower() == st.session_state.lang.lower() or (not IS_AR and k.lower().startswith('en')):
                    db = DATA_ALL[k].get("db", {}).get(st.session_state.budget_key, [])
            
            # خريطة الربط بين الاختيار الإنجليزي والقيمة العربية في الملف
            mapping = {"History": "تاريخ وآثار", "Entertainment": "ترفيه", "Nature": "طبيعة", "Shopping": "تسوق", "Dining": "مطاعم ومقاهي"}
            search_terms = [mapping.get(s, s) for s in selected] if not IS_AR else selected
            
            # تصفية النتائج بناءً على الاهتمامات
            st.session_state.suggestions = [p for p in db if p.get('الفئة') in search_terms] or db[:2]
            st.session_state.transport_choice = None; st.rerun()

        # عرض النتائج ووسائل النقل (خارج كتلة الـ if button لضمان استمرار ظهورها)
        if st.session_state.suggestions:
            st.markdown(f"### {strings['trans_q']}")
            t_cols = st.columns(3)
            if t_cols[0].button(strings["metro"]): st.session_state.transport_choice = "metro"
            if t_cols[1].button(strings["car"]): st.session_state.transport_choice = "car"
            if t_cols[2].button(strings["taxi"]): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                info_html = f"<p style='color:#94A3B8;'>{strings['select_trans']}</p>"
                if st.session_state.transport_choice:
                    base = p.get('b_time', 20)
                    t_val = base + 10 if st.session_state.transport_choice == "metro" else int(base * 1.2)
                    time_str = f"<b>{strings['est_time']} {t_val} {strings['mins']}</b>"
                    info_html = f"{time_str}<br><a href='https://www.google.com/maps/search/{p['الوجهة']}' target='_blank' class='map-btn'>{strings['map_btn']}</a>"

                st.markdown(f'<div class="dest-card"><h4>{p["الوجهة"]}</h4><p>{p["وصف"]}</p>{info_html}</div>', unsafe_allow_html=True)

    with col_s:
        st.markdown(f'<div class="glass-card" style="text-align: center;"><h4>{strings["rating_t"]}</h4>', unsafe_allow_html=True)
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}", key=f"s{i}"): st.session_state.rated = True
        
        if st.session_state.rated:
            if st.button(strings["next_day"]):
                if st.session_state.day < 3: st.session_state.day += 1
                st.session_state.suggestions = []; st.session_state.rated = False; st.rerun()
        
        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button(strings["reset"]): st.session_state.clear(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.8em;'>Path7 | IAU Engineering Excellence</p>", unsafe_allow_html=True)
