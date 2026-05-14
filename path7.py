import streamlit as st
import random
import json
from datetime import datetime
import pytz

# وظيفة لقراءة ملف JSON
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

DATA_ALL = load_data()
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour
formatted_time = now_riyadh.strftime('%I:%M %p')

greeting = "صباح الخير" if 5 <= current_hour < 12 else "مساء الخير"

st.set_page_config(page_title="Path7 | مسار 7", layout="wide", initial_sidebar_state="collapsed")

# إدارة الحالة
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'day' not in st.session_state: st.session_state.day = 1
if 'rated' not in st.session_state: st.session_state.rated = False
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

T = DATA_ALL.get(st.session_state.lang, {})

# --- CSS التنسيق النهائي والثابت ---
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    :root {{
        --primary-bg: #075985;
        --secondary-bg: #03456F;
        --accent-blue: #0EA5E9;
    }}
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if st.session_state.lang == "العربية" else "ltr"}; }}
    .stApp {{ background: linear-gradient(145deg, var(--primary-bg) 0%, var(--secondary-bg) 100%) !important; color: white !important; }}
    
    .glass-card {{ background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(15px); padding: 25px; border-radius: 25px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; }}
    .dash-panel {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); padding: 15px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; text-align: center; }}
    
    /* بطاقة الوجهة */
    .dest-card {{ background: white !important; padding: 20px; border-radius: 20px; border-{"right" if st.session_state.lang == "العربية" else "left"}: 10px solid var(--accent-blue); margin-bottom: 15px; color: #1E293B !important; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }}
    
    /* تذكرة المترو الرهيبة */
    .metro-ticket {{ 
        background: linear-gradient(90deg, #DC2626 0%, #991B1B 100%); 
        color: white !important; padding: 10px; border-radius: 10px; 
        font-size: 0.8em; margin-bottom: 10px; border-left: 5px dashed white;
        display: flex; justify-content: space-between; align-items: center;
    }}
    
    .map-link {{ 
        background-color: #0284C7; color: white !important; padding: 10px 20px; 
        border-radius: 50px; text-decoration: none !important; font-weight: bold; 
        display: inline-block; font-size: 0.9em; margin-top: 10px;
    }}
    
    h1, h2, h3, h4, label, p {{ color: white !important; }}
    .dest-card h4, .dest-card p, .dest-card b, .dest-card span {{ color: #1E293B !important; }}
    </style>
''', unsafe_allow_html=True)

if st.session_state.page == 'welcome':
    st.markdown(f'<div class="glass-card" style="text-align: center; margin-top: 10vh;">', unsafe_allow_html=True)
    st.title(f"📍 {T.get('p_name', 'Path7')}")
    st.subheader(T.get('subtitle', 'نظام التوافق اللحظي للسياحة الذكية'))
    st.session_state.user_name = st.text_input(T.get("visitor_name", "اسم السائح"), placeholder="أدخل اسمك هنا")
    u_budget = st.radio(T.get("budget_q", "الميزانية"), ["اقتصادية", "فاخرة"], horizontal=True)
    if st.button(T.get("start_btn", "ابدأ الرحلة"), use_container_width=True):
        st.session_state.budget_key = "Luxury" if u_budget == "فاخرة" else "Economy"
        st.session_state.page = 'main'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # لوحة المعلومات العلوية
    st.markdown(f'''<div class="dash-panel">
        <h2 style="margin:0;">{greeting}، {st.session_state.user_name}</h2>
        <p>🕒 {formatted_time} | {T.get("weather", "الطقس")}: {"مشمس ☀️" if 5 <= current_hour <= 17 else "ليل صافي 🌙"}</p>
        <span style="background:var(--accent-blue); padding:3px 15px; border-radius:50px; font-size:0.9em;">📅 اليوم {st.session_state.day} من 3</span>
    </div>''', unsafe_allow_html=True)

    st.subheader("🌟 ما هي اهتماماتك المفضلة اليوم؟")
    selected_ints = st.multiselect("", ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"], label_visibility="collapsed")
    
    if st.button("تحليل المسار الذكي 🔍", use_container_width=True):
        db = T.get("db", {}).get(st.session_state.budget_key, [])
        st.session_state.suggestions = [p for p in db if p.get('الفئة') in selected_ints] if selected_ints else random.sample(db, 2)
        st.session_state.transport_choice = None
        st.session_state.traffic_factor = random.uniform(1.2, 1.8)
        st.session_state.rated = False
        st.rerun()

    if st.session_state.suggestions:
        st.markdown(f"### وسيلة النقل المفضلة")
        tc = st.columns(3)
        if tc[0].button("🚇 المترو"): st.session_state.transport_choice = "metro"
        if tc[1].button("🚗 السيارة"): st.session_state.transport_choice = "car"
        if tc[2].button("🚕 التاكسي"): st.session_state.transport_choice = "taxi"

        for i, p in enumerate(st.session_state.suggestions):
            # حساب الوقت
            if st.session_state.transport_choice == "metro":
                f_time = p['b_time'] + 5
                icon = "🚇"
            elif st.session_state.transport_choice:
                f_time = int(p['b_time'] * getattr(st.session_state, 'traffic_factor', 1.5))
                icon = "🚗" if st.session_state.transport_choice == "car" else "🚕"
            else:
                f_time = "--"; icon = "⏳"

            # عرض الوجهة
            st.markdown(f'''
            <div class="dest-card">
                {f'<div class="metro-ticket"><span>🎫 تذكرة مترو الرياض رقم #{random.randint(1000,9999)}</span> <span>المسار الأحمر ✅</span></div>' if st.session_state.transport_choice == "metro" and p.get('metro') else ''}
                <h4>{i+1}. {p["الوجهة"]}</h4>
                <p style="margin:5px 0;">{p["وصف"]}</p>
                <p style="font-size:0.85em; color:#64748B !important;">🕒 ساعات العمل: {p.get('ساعات العمل', '24 ساعة')}</p>
                <b>{icon} الوقت المتوقع: {f_time} دقيقة</b><br>
                <a href="{p['map_url']}" target="_blank" class="map-link">📍 فتح في خرائط جوجل</a>
            </div>
            ''', unsafe_allow_html=True)
            if i < len(st.session_state.suggestions)-1:
                st.markdown('<div style="text-align:center; margin:-10px 0 5px 0;">⬇️</div>', unsafe_allow_html=True)

        # نظام التقييم
        st.markdown(f'<div class="dash-panel"><h4>⭐ تقييمك لليوم {st.session_state.day}</h4>', unsafe_allow_html=True)
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐", key=f"star_{st.session_state.day}_{i}"): st.session_state.rated = True
        
        if st.session_state.rated:
            if st.session_state.day < 3:
                if st.button("انتقل لمسار اليوم التالي ⏩", use_container_width=True):
                    st.session_state.day += 1; st.session_state.suggestions = []; st.session_state.transport_choice = None; st.session_state.rated = False; st.rerun()
            else:
                st.success("✨ اكتملت رحلتك في مسار 7.. نأمل أنك استمتعت بجمال الرياض! ✨")
                if st.button("🔄 رحلة جديدة"): st.session_state.clear(); st.rerun()
