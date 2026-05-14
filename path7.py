import streamlit as st
import random
from datetime import datetime
import pytz

# إعدادات الصفحة الأساسية وإخفاء القوائم المزعجة
st.set_page_config(page_title="Path7 | مسار 7", layout="wide", initial_sidebar_state="collapsed")

# --- CSS التحريك والانسيابية (Motion & Glow) ---
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    
    /* إخفاء أيقونات الـ Streamlit الافتراضية المزعجة */
    #MainMenu, footer, header {{visibility: hidden;}}
    
    :root {{
        --bg: #0f172a;
        --accent: #38bdf8;
    }}

    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; }}
    
    .stApp {{ background: radial-gradient(circle at top right, #1e293b, #0f172a) !important; color: white !important; }}

    /* أنيميشن الدخول الانسيابي */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* تصميم البطاقة مع حركة عند الدخول وحركة عند التمرير */
    .dest-card {{
        background: white !important;
        padding: 25px;
        border-radius: 24px;
        color: #1e293b !important;
        margin-bottom: 25px;
        border-right: 8px solid var(--accent);
        box-shadow: 0 15px 30px rgba(0,0,0,0.2);
        animation: fadeInUp 0.8s ease-out; /* حركة الدخول */
        transition: transform 0.3s ease;
    }}
    .dest-card:hover {{ transform: scale(1.02); }}

    /* حركة نبض بسيطة لتذكرة المترو */
    @keyframes pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }}
        70% {{ box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
    }}
    .metro-ticket {{
        background: #ef4444;
        color: white !important;
        padding: 12px;
        border-radius: 12px;
        font-weight: bold;
        margin-bottom: 15px;
        border: 2px dashed white;
        animation: pulse 2s infinite; /* نبض مستمر */
    }}

    /* الأزرار التفاعلية */
    .stButton>button {{
        background: linear-gradient(90deg, #38bdf8, #0ea5e9) !important;
        color: white !important;
        border-radius: 15px !important;
        border: none !important;
        transition: all 0.2s active;
    }}
    .stButton>button:active {{ transform: scale(0.95); }}
    
    .map-link {{
        color: #0ea5e9 !important;
        text-decoration: none;
        font-weight: bold;
        border: 1px solid #0ea5e9;
        padding: 5px 15px;
        border-radius: 50px;
        transition: 0.3s;
    }}
    .map-link:hover {{ background: #0ea5e9; color: white !important; }}
    </style>
''', unsafe_allow_html=True)

# إدارة الحالة (State)
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'suggestions' not in st.session_state: st.session_state.suggestions = []

if st.session_state.page == 'welcome':
    st.markdown('<div style="text-align: center; padding-top: 10vh; animation: fadeInUp 1s ease;">', unsafe_allow_html=True)
    st.title("📍 Path7 | مسار 7")
    st.subheader("نظام التوافق اللحظي للسياحة الذكية")
    name = st.text_input("ما هو اسمك؟")
    budget = st.radio("حدد الميزانية:", ["اقتصادية", "فاخرة"], horizontal=True)
    if st.button("ابدأ الرحلة ✨"):
        st.session_state.user_name = name
        st.session_state.budget = budget
        st.session_state.page = 'main'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown(f'<div style="animation: fadeInUp 0.5s ease;"><h2>أهلاً {st.session_state.user_name}</h2></div>', unsafe_allow_html=True)
    
    # اختيار الاهتمامات
    ints = st.multiselect("🌟 اختر ما يستهويك اليوم:", ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"])
    
    if st.button("تحليل المسار الذكي"):
        # بيانات مستلهمة من ملفك "الميزانية معدلة"
        all_data = [
            {"الوجهة": "حصن المصمك", "وصف": "رمز توحيد المملكة وتأسيسها", "ساعات": "8:00ص—9:00م", "فئة": "تاريخ وآثار", "budget": "اقتصادية", "url": "https://maps.app.goo.gl/9Z1"},
            {"الوجهة": "فيا الرياض", "وصف": "عمارة سلمية ومطاعم عالمية", "ساعات": "10:00ص—12:00ص", "فئة": "ترفيه", "budget": "فاخرة", "url": "https://maps.app.goo.gl/9Z2"},
            {"الوجهة": "وادي حنيفة", "وصف": "مساحات خضراء وبحيرات خلابة", "ساعات": "24 ساعة", "فئة": "طبيعة", "budget": "اقتصادية", "url": "https://maps.app.goo.gl/9Z3"}
        ]
        st.session_state.suggestions = [d for d in all_data if d['budget'] == st.session_state.budget and (d['فئة'] in ints or not ints)]
        st.session_state.transport = None
        st.rerun()

    if st.session_state.suggestions:
        st.write("### اختر وسيلة النقل:")
        c1, c2, c3 = st.columns(3)
        if c1.button("🚇 المترو"): st.session_state.transport = "metro"
        if c2.button("🚗 السيارة"): st.session_state.transport = "car"
        if c3.button("🚕 التاكسي"): st.session_state.transport = "taxi"

        for p in st.session_state.suggestions:
            st.markdown(f'''
            <div class="dest-card">
                {f'<div class="metro-ticket">🎫 تذكرة المترو الذكية - الخط الفضي</div>' if st.session_state.transport == "metro" else ''}
                <h4>{p["الوجهة"]}</h4>
                <p>{p["وصف"]}</p>
                <div style="display:flex; justify-content: space-between; align-items:center; margin-top:15px;">
                    <span style="font-size:0.8em; color:#64748b;">🕒 {p["ساعات"]}</span>
                    <a href="{p["url"]}" target="_blank" class="map-link">📍 الموقع</a>
                </div>
            </div>
            ''', unsafe_allow_html=True)
