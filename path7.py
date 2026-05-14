import streamlit as st
import json
from datetime import datetime
import pytz

# 1. تحميل البيانات كما هي
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

DATA_ALL = load_data()

# 2. إعدادات الوقت واللغة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
hour = now_riyadh.hour

if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

IS_AR = st.session_state.lang == "العربية"

# قاموس نصوصك الأصلية
strings = {
    "title": "Path7 📍",
    "sub": "نظام التوافق اللحظي للسياحة الذكية" if IS_AR else "Real-time Smart Tourism System",
    "name_q": "مرحباً بك، ما هو اسمك؟" if IS_AR else "Welcome, what is your name?",
    "budget_q": "حدد طابع رحلتك اليوم:" if IS_AR else "Choose your trip style:",
    "budgets": ["اقتصادية", "فاخرة"] if IS_AR else ["Economy", "Luxury"],
    "start_btn": "انطلق لاستكشاف الرياض 🚀" if IS_AR else "Explore Riyadh 🚀",
    "interests_q": "ما هي اهتماماتك المفضلة اليوم؟" if IS_AR else "What are your interests today?",
    "interests_list": ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"] if IS_AR else ["History", "Entertainment", "Nature", "Shopping", "Dining"],
    "analyze_btn": "تحليل المسار الذكي 🔍" if IS_AR else "Smart Path Analysis 🔍",
    "trans_q": "وسيلة النقل المفضلة" if IS_AR else "Preferred Transport",
    "metro": "🚇 المترو" if IS_AR else "🚇 Metro",
    "car": "🚗 السيارة" if IS_AR else "🚗 Car",
    "taxi": "🚕 التاكسي" if IS_AR else "🚕 Taxi",
    "map_btn": "📍 فتح في الخرائط" if IS_AR else "📍 Open Maps",
    "select_trans": "⏳ حدد وسيلة النقل لمعرفة المسار" if IS_AR else "⏳ Select transport to see path",
    "reset": "إعادة ضبط 🔄" if IS_AR else "Reset 🔄"
}

# 3. تصميمك الأصلي (CSS)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if IS_AR else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 25px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.3); margin-bottom: 20px; text-align: {"right" if IS_AR else "left"}; }}
    .dest-card {{ background: white; padding: 20px; border-radius: 20px; border-{"right" if IS_AR else "left"}: 10px solid #0EA5E9; margin-bottom: 15px; color: black; }}
    .stButton>button {{ background: linear-gradient(90deg, #0284C7, #38BDF8) !important; color: white !important; border-radius: 10px !important; }}
    
    /* النجوم المربعة كما طلبتِ */
    div[data-testid="stHorizontalBlock"] button[key^="s"] {{
        aspect-ratio: 1/1 !important; width: 55px !important; height: 55px !important; border-radius: 12px !important;
    }}
    </style>
''', unsafe_allow_html=True)

# تبديل اللغة
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
        st.markdown(f'<div class="glass-card"><h3>📅 اليوم {st.session_state.get("day", 1)}</h3><p>👤 {st.session_state.user_name}</p></div>', unsafe_allow_html=True)
        
        st.subheader(strings["interests_q"])
        selected = st.multiselect("", strings["interests_list"], label_visibility="collapsed")
        
        if st.button(strings["analyze_btn"]):
            # الحل التقني لمشكلة الإنجليزي
            db = []
            for k in DATA_ALL.keys():
                if k.lower() == st.session_state.lang.lower() or (not IS_AR and k.lower().startswith('en')):
                    db = DATA_ALL[k].get("db", {}).get(st.session_state.budget_key, [])
            
            # تحويل الاهتمامات من إنجليزي لعربي عشان تطابق ملف الـ JSON
            mapping = {"History": "تاريخ وآثار", "Entertainment": "ترفيه", "Nature": "طبيعة", "Shopping": "تسوق", "Dining": "مطاعم ومقاهي"}
            search_vals = [mapping.get(s, s) for s in selected] if not IS_AR else selected
            
            # حفظ النتائج في الـ session_state عشان ما تختفي
            st.session_state.suggestions = [p for p in db if p.get('الفئة') in search_vals] or db[:2]
            st.session_state.transport_choice = None
            st.rerun()

        # عرض النتائج (خارج زر التحليل)
        if st.session_state.suggestions:
            st.markdown(f"### {strings['trans_q']}")
            t_cols = st.columns(3)
            if t_cols[0].button(strings["metro"]): st.session_state.transport_choice = "metro"
            if t_cols[1].button(strings["car"]): st.session_state.transport_choice = "car"
            if t_cols[2].button(strings["taxi"]): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                info_text = f"<p style='color:gray;'>{strings['select_trans']}</p>"
                if st.session_state.transport_choice:
                    info_text = f"<a href='#' style='color:#0284C7; font-weight:bold;'>{strings['map_btn']}</a>"
                
                st.markdown(f'''
                    <div class="dest-card">
                        <h4>{p["الوجهة"]}</h4>
                        <p>{p["وصف"]}</p>
                        {info_text}
                    </div>
                ''', unsafe_allow_html=True)

    with col_s:
        st.markdown('<div class="glass-card" style="text-align: center;"><h4>⭐ التقييم</h4>', unsafe_allow_html=True)
        stars = st.columns(5)
        for i in range(1, 6):
            stars[i-1].button(f"{i}", key=f"s{i}")
        if st.button(strings["reset"]): st.session_state.clear(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
