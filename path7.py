import streamlit as st
import random
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
formatted_time = now_riyadh.strftime('%I:%M %p')
hour = now_riyadh.hour
weather_status = "مشمس ☀️" if 5 <= hour <= 17 else "صافي 🌙"

st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# 3. إدارة الحالة
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'day' not in st.session_state: st.session_state.day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'rated' not in st.session_state: st.session_state.rated = False

T = DATA_ALL.get(st.session_state.lang, {})

# 4. CSS النسخة العظيمة مع إصلاح المسافات والأنيميشن
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    
    @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}

    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if st.session_state.lang == "العربية" else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); background-attachment: fixed; }}
    
    .glass-card {{ 
        background: rgba(255, 255, 255, 0.75); 
        backdrop-filter: blur(12px); 
        padding: 30px; border-radius: 25px; 
        border: 1px solid rgba(255, 255, 255, 0.3); 
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        animation: fadeIn 0.8s ease-out;
        margin-bottom: 20px;
    }}
    
    .dest-card {{ 
        background: white; padding: 20px; border-radius: 20px; 
        border-{"right" if st.session_state.lang == "العربية" else "left"}: 12px solid #0EA5E9; 
        margin-bottom: 15px; transition: 0.3s;
        animation: fadeIn 1s ease-out;
    }}

    .map-btn {{ background-color: #0284C7; color: white !important; padding: 8px 16px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 10px; }}
    
    /* تنسيق خاص لجعل النجوم تتنفس */
    .rating-title {{ margin-bottom: 25px !important; display: block; }}
    </style>
''', unsafe_allow_html=True)

# زر اللغة
col_l1, col_l2 = st.columns([12, 1])
if col_l2.button("عربي/EN"):
    st.session_state.lang = "English" if st.session_state.lang == "العربية" else "العربية"
    st.rerun()

# --- صفحة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown(f'''<div class="glass-card" style="text-align: center;">
        <h1 style="color: #0369A1; margin-bottom: 0;">Path7 📍</h1>
        <p style="color: #64748B; font-size: 1.2em;">نظام التوافق اللحظي للسياحة الذكية</p>
        <hr style="opacity: 0.1; margin: 25px 0;">
    </div>''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.session_state.user_name = st.text_input("مرحباً بك، ما هو اسمك؟", placeholder="أدخل اسمك الكريم هنا")
        u_budget = st.radio("حدد طابع رحلتك اليوم:", ["اقتصادية", "فاخرة"], horizontal=True)
        if st.button("انطلق لاستكشاف الرياض 🚀"):
            st.session_state.budget_key = "Luxury" if u_budget == "فاخرة" else "Economy"
            st.session_state.page = 'system'
            st.rerun()

# --- صفحة النظام ---
else:
    col_m, col_s = st.columns([2, 1])
    with col_m:
        st.markdown(f'''<div class="glass-card">
            <h3 style="margin:0; color:#0369A1;">📅 يوم {st.session_state.day} من 3</h3>
            <p>👤 {st.session_state.user_name} | 🕒 {formatted_time} | 🌤️ الجو: {weather_status}</p>
        </div>''', unsafe_allow_html=True)

        st.subheader("ما هي اهتماماتك المفضلة اليوم؟")
        selected_interests = st.multiselect("", ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"], label_visibility="collapsed")
        
        if st.button("تحليل المسار الذكي 🔍"):
            db = DATA_ALL.get(st.session_state.lang, {}).get("db", {}).get(st.session_state.budget_key, [])
            st.session_state.suggestions = [p for p in db if p.get('الفئة') in selected_interests] or db[:2]
            st.session_state.transport_choice = None
            st.rerun()

        if st.session_state.suggestions:
            st.markdown("### وسيلة النقل المفضلة")
            t_cols = st.columns(3)
            if t_cols[0].button("🚇 المترو"): st.session_state.transport_choice = "metro"
            if t_cols[1].button("🚗 السيارة"): st.session_state.transport_choice = "car"
            if t_cols[2].button("🚕 التاكسي"): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                if st.session_state.transport_choice:
                    base = p.get('b_time', 20)
                    if st.session_state.transport_choice == "metro":
                        time_display = f"🚇 الوقت المقدر: {base + 10} دقيقة"
                        action = "<p style='color:#0284C7; font-weight:bold;'>🚉 المترو متاح، توجه لأقرب محطة.</p>"
                    else:
                        time_display = f"🚗 الوقت المقدر: {int(base * 1.4)} دقيقة"
                        action = f'<a href="https://www.google.com/maps/search/{p["الوجهة"]}" target="_blank" class="map-btn">📍 الموقع في الخرائط</a>'
                else:
                    time_display = "⏳ حدد وسيلة النقل لمعرفة الوقت"
                    action = ""

                st.markdown(f'''<div class="dest-card">
                    <h4 style="color:#0284C7; margin:0;">{p['الوجهة']}</h4>
                    <p style="color:#64748B;">{p['وصف']}</p>
                    <p style="font-weight:bold; color:#0369A1;">{time_display}</p>
                    {action}
                </div>''', unsafe_allow_html=True)

    with col_s:
        # التقييم مع مساحة للتنفس
        st.markdown('<div class="glass-card" style="text-align: center;"><h4 class="rating-title">تقييمك للتجربة ⭐</h4>', unsafe_allow_html=True)
        st.write("") # مسافة إضافية
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐", key=f"star_{i}"): st.session_state.rated = True
        
        if st.session_state.rated and st.session_state.day < 3:
            st.write("") 
            if st.button("اليوم التالي ⏭️"):
                st.session_state.day += 1
                st.session_state.suggestions = []; st.session_state.transport_choice = None; st.session_state.rated = False
                st.rerun()
        
        st.write("---")
        if st.button("🔄 Reset"): st.session_state.clear(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.8em; margin-top: 30px;'>Path7 | Engineering Excellence @ IAU</p>", unsafe_allow_html=True)
