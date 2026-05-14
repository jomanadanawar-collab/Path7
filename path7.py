import streamlit as st
import json
from datetime import datetime
import pytz

# 1. تحميل البيانات
@st.cache_data
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

DATA_ALL = load_data()

# 2. الوقت والإعدادات
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
hour = now_riyadh.hour

if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

IS_AR = st.session_state.lang == "العربية"

# قاموس الواجهة (تصميمك الأصلي)
strings = {
    "title": "Path7 📍",
    "sub": "نظام التوافق اللحظي للسياحة الذكية" if IS_AR else "Real-time Smart Tourism System",
    "interests_list": ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"] if IS_AR else ["History", "Entertainment", "Nature", "Shopping", "Dining"],
    "analyze_btn": "تحليل المسار الذكي 🔍" if IS_AR else "Smart Path Analysis 🔍",
    "trans_q": "وسيلة النقل المفضلة" if IS_AR else "Preferred Transport",
    "metro": "🚇 المترو" if IS_AR else "🚇 Metro",
    "car": "🚗 السيارة" if IS_AR else "🚗 Car",
    "taxi": "🚕 التاكسي" if IS_AR else "🚕 Taxi",
    "map_btn": "📍 فتح في الخرائط" if IS_AR else "📍 Open Maps",
    "select_trans": "⏳ حدد وسيلة النقل لمعرفة المسار" if IS_AR else "⏳ Select transport to see path"
}

# 3. التنسيق (Glassmorphism اللي تحبينه)
st.markdown(f'''
    <style>
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 20px; border-radius: 20px; text-align: {"right" if IS_AR else "left"}; }}
    .dest-card {{ background: white; padding: 15px; border-radius: 15px; margin-bottom: 10px; color: black; border-left: 5px solid #0284C7; }}
    /* النجوم مربعة 1:1 للهندسة */
    div[data-testid="stHorizontalBlock"] button[key^="s"] {{
        aspect-ratio: 1/1 !important; width: 55px !important; height: 55px !important;
    }}
    </style>
''', unsafe_allow_html=True)

# تبديل اللغة
if st.sidebar.button("AR / EN"):
    st.session_state.lang = "English" if IS_AR else "العربية"
    st.rerun()

if st.session_state.page == 'system':
    col_m, col_s = st.columns([2.2, 1])
    
    with col_m:
        st.markdown(f'<div class="glass-card"><h3>📅 اليوم {st.session_state.get("day", 1)}</h3></div>', unsafe_allow_html=True)
        
        selected = st.multiselect(strings["interests_q"] if "interests_q" in strings else "Interests", strings["interests_list"])
        
        # --- الزر: وظيفته فقط جلب البيانات وحفظها ---
        if st.button(strings["analyze_btn"]):
            # 1. تحديد مفتاح اللغة في الـ JSON (تعامل مرن مع الأحرف)
            db = []
            for k in DATA_ALL.keys():
                if k.lower() == st.session_state.lang.lower() or (not IS_AR and k.lower().startswith('en')):
                    db = DATA_ALL[k].get("db", {}).get(st.session_state.get("budget_key", "Economy"), [])
            
            # 2. الربط (Mapping) إذا كانت الاختيارات بالإنجليزي والبيانات بالعربي
            map_dict = {"History": "تاريخ وآثار", "Entertainment": "ترفيه", "Nature": "طبيعة", "Shopping": "تسوق", "Dining": "مطاعم ومقاهي"}
            final_interests = [map_dict.get(s, s) for s in selected] if not IS_AR else selected
            
            # 3. الحفظ في الـ session_state (هذا هو السر!)
            st.session_state.suggestions = [p for p in db if p.get('الفئة') in final_interests] or db[:2]
            st.session_state.transport_choice = None # تصفير وسيلة النقل عند البحث الجديد
            st.rerun()

        # --- العرض: خارج بلوك الزر عشان ما يختفي ---
        if st.session_state.suggestions:
            st.markdown(f"### {strings['trans_q']}")
            t_cols = st.columns(3)
            if t_cols[0].button(strings["metro"]): st.session_state.transport_choice = "metro"
            if t_cols[1].button(strings["car"]): st.session_state.transport_choice = "car"
            if t_cols[2].button(strings["taxi"]): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                trans_info = f"<p style='color:gray;'>{strings['select_trans']}</p>"
                if st.session_state.transport_choice:
                    trans_info = f"<a href='#' class='map-btn' style='color:#0284C7; font-weight:bold;'>{strings['map_btn']}</a>"
                
                st.markdown(f'''
                    <div class="dest-card">
                        <h4 style="margin:0;">{p["الوجهة"]}</h4>
                        <p style="font-size:0.9em;">{p["وصف"]}</p>
                        {trans_info}
                    </div>
                ''', unsafe_allow_html=True)

    with col_s:
        # قسم التقييم والنجوم المربعة
        st.markdown('<div class="glass-card" style="text-align:center;"><h4>⭐ التقييم</h4>', unsafe_allow_html=True)
        stars = st.columns(5)
        for i in range(1, 6):
            stars[i-1].button(f"{i}", key=f"s{i}")
        st.markdown('</div>', unsafe_allow_html=True)
