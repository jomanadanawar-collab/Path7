import streamlit as st
import json
from datetime import datetime
import pytz

# 1. تحميل البيانات بذكاء
@st.cache_data
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

DATA_ALL = load_data()

# 2. إعدادات الحالة (Session State) - لضمان عدم اختفاء البيانات
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'page' not in st.session_state: st.session_state.page = 'welcome'

IS_AR = st.session_state.lang == "العربية"

# قاموس ترجمة الاهتمامات (هذا هو مفتاح الحل)
INTEREST_MAP = {
    "History": "تاريخ وآثار",
    "Entertainment": "ترفيه",
    "Nature": "طبيعة",
    "Shopping": "تسوق",
    "Dining": "مطاعم ومقاهي"
}

# نصوص الواجهة
strings = {
    "title": "Path7 📍",
    "interests_list": ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"] if IS_AR else list(INTEREST_MAP.keys()),
    "analyze_btn": "تحليل المسار الذكي 🔍" if IS_AR else "Smart Path Analysis 🔍",
    "trans_q": "وسيلة النقل المفضلة" if IS_AR else "Preferred Transport",
    "map_btn": "📍 فتح في الخرائط" if IS_AR else "📍 Open Maps"
}

# 3. تصميمك الأصلي (Glassmorphism)
st.markdown(f'''
    <style>
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 25px; border-radius: 25px; text-align: {"right" if IS_AR else "left"}; }}
    .dest-card {{ background: white; padding: 15px; border-radius: 15px; margin-bottom: 10px; color: black; border-left: 5px solid #0284C7; }}
    /* أزرار النجوم المربعة */
    div[data-testid="stHorizontalBlock"] button[key^="s"] {{ aspect-ratio: 1/1 !important; width: 55px !important; }}
    </style>
''', unsafe_allow_html=True)

# زر تبديل اللغة (Sidebar ليكون أهيب وأوضح)
if st.sidebar.button("Switch Language / تغيير اللغة"):
    st.session_state.lang = "English" if IS_AR else "العربية"
    st.rerun()

# --- منطق النظام ---
if st.session_state.page == 'system':
    col_m, col_s = st.columns([2.2, 1])
    
    with col_m:
        st.markdown(f'<div class="glass-card"><h3>📅 Path7 - {st.session_state.lang}</h3></div>', unsafe_allow_html=True)
        
        selected = st.multiselect("Select Interests:", strings["interests_list"])
        
        if st.button(strings["analyze_btn"]):
            # الخطوة 1: العثور على قاعدة البيانات الصحيحة في ملفك
            db = []
            for key in DATA_ALL.keys():
                if key.lower() == st.session_state.lang.lower() or (not IS_AR and key.lower().startswith('en')):
                    db = DATA_ALL[key].get("db", {}).get(st.session_state.get("budget_key", "Economy"), [])
                    break
            
            # الخطوة 2: تحويل الاختيارات الإنجليزية إلى كلمات مطابقة لملف الـ JSON
            # إذا كانت الواجهة إنجليزية، نحول الاختيارات للعربي للبحث في الـ JSON
            search_terms = [INTEREST_MAP.get(s, s) for s in selected] if not IS_AR else selected
            
            # الخطوة 3: الفلترة والحفظ في الـ session_state
            st.session_state.suggestions = [p for p in db if p.get('الفئة') in search_terms]
            st.session_state.transport_choice = None
            st.rerun()

        # عرض النتائج خارج بلوك الزر لضمان استمراريتها
        if st.session_state.suggestions:
            st.markdown(f"### {strings['trans_q']}")
            t_cols = st.columns(3)
            if t_cols[0].button("🚇 Metro"): st.session_state.transport_choice = "metro"
            if t_cols[1].button("🚗 Car"): st.session_state.transport_choice = "car"
            if t_cols[2].button("🚕 Taxi"): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                map_link = f"<a href='https://maps.google.com/?q={p['الوجهة']}' target='_blank' style='color:#0284C7;'>{strings['map_btn']}</a>" if st.session_state.transport_choice else ""
                st.markdown(f'''
                    <div class="dest-card">
                        <h4>{p["الوجهة"]}</h4>
                        <p>{p["وصف"]}</p>
                        {map_link}
                    </div>
                ''', unsafe_allow_html=True)
    
    with col_s:
        # قسم التقييم
        st.markdown('<div class="glass-card"><h4>⭐ Rate</h4>', unsafe_allow_html=True)
        st.columns(5)[0].button("1", key="s1") # مثال لزر نجمة واحدة
        if st.button("Reset 🔄"): 
            st.session_state.suggestions = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # صفحة الترحيب البسيطة
    if st.button("Start / ابدأ"):
        st.session_state.page = 'system'
        st.rerun()
