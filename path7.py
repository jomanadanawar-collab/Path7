import streamlit as st
import json
from datetime import datetime
import pytz

# 1. تحميل البيانات لمرة واحدة فقط
@st.cache_data
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

DATA_ALL = load_data()

# 2. الوقت واللغة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
hour = now_riyadh.hour

if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

IS_AR = st.session_state.lang == "العربية"

# قاموس ترجمة الواجهة
strings = {
    "title": "Path7 📍",
    "interests_list": ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"] if IS_AR else ["History", "Entertainment", "Nature", "Shopping", "Dining"],
    "analyze_btn": "تحليل المسار الذكي 🔍" if IS_AR else "Smart Path Analysis 🔍",
    "trans_q": "وسيلة النقل المفضلة" if IS_AR else "Preferred Transport",
    "metro": "🚇 المترو" if IS_AR else "🚇 Metro",
    "car": "🚗 السيارة" if IS_AR else "🚗 Car",
    "taxi": "🚕 التاكسي" if IS_AR else "🚕 Taxi"
}

# 3. التنسيق (النجوم المربعة 1:1)
st.markdown(f'''
    <style>
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 20px; border-radius: 20px; }}
    /* رأي اللجنة: النجوم مربعة تماماً */
    div[data-testid="stHorizontalBlock"] button[key^="s"] {{
        aspect-ratio: 1/1 !important;
        width: 55px !important;
        height: 55px !important;
        min-width: 55px !important;
        border-radius: 10px !important;
    }}
    </style>
''', unsafe_allow_html=True)

# --- منطق الصفحة الرئيسية ---
if st.session_state.page == 'system':
    col_m, col_s = st.columns([2.2, 1])
    
    with col_m:
        st.markdown(f'<div class="glass-card"><h3>📅 اليوم {st.session_state.get("day", 1)}</h3></div>', unsafe_allow_html=True)
        
        selected = st.multiselect(strings["interests_q"] if "interests_q" in strings else "Interests", strings["interests_list"])
        
        # الضغطة هنا هي المحرك الرئيسي
        if st.button(strings["analyze_btn"]):
            # البحث عن البيانات: نحاول نلاقي اللغة في الـ JSON بأي شكل (English أو العربية)
            db = []
            for k in DATA_ALL.keys():
                if k.lower() == st.session_state.lang.lower() or (not IS_AR and k.lower().startswith('en')):
                    db = DATA_ALL[k].get("db", {}).get(st.session_state.get("budget_key", "Economy"), [])
            
            # فلترة ذكية: إذا الواجهة إنجليزي والبيانات عربي
            map_dict = {"History": "تاريخ وآثار", "Entertainment": "ترفيه", "Nature": "طبيعة", "Shopping": "تسوق", "Dining": "مطاعم ومقاهي"}
            criteria = [map_dict.get(s, s) for s in selected] if not IS_AR else selected
            
            st.session_state.suggestions = [p for p in db if p.get('الفئة') in criteria] or db[:2]
            st.rerun()

        # عرض النتائج ووسائل النقل (يجب أن تكون خارج الـ IF الخاص بالزر لتبقى ظاهرة)
        if st.session_state.suggestions:
            st.markdown(f"### {strings['trans_q']}")
            t_cols = st.columns(3)
            if t_cols[0].button(strings["metro"]): st.session_state.transport_choice = "metro"
            if t_cols[1].button(strings["car"]): st.session_state.transport_choice = "car"
            if t_cols[2].button(strings["taxi"]): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                st.markdown(f'<div style="background:white; padding:15px; border-radius:15px; margin-bottom:10px; color:black;"><h4>{p["الوجهة"]}</h4><p>{p["وصف"]}</p></div>', unsafe_allow_html=True)
