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

# نصوص الواجهة
reset_label = "إعادة ضبط 🔄" if st.session_state.lang == "العربية" else "Reset 🔄"
rating_title = "تقييمك للتجربة ⭐" if st.session_state.lang == "العربية" else "Rate your experience ⭐"
text_align = "right" if st.session_state.lang == "العربية" else "left"

# 4. التنسيق البصري (نسخة المسابقات)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if st.session_state.lang == "العربية" else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); background-attachment: fixed; }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 30px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 15px 35px rgba(0,0,0,0.1); margin-bottom: 20px; }}
    .info-card {{ text-align: {text_align}; }}
    .center-rating {{ text-align: center !important; }}
    .dest-card {{ background: white; padding: 25px; border-radius: 20px; border-{"right" if st.session_state.lang == "العربية" else "left"}: 12px solid #0EA5E9; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }}
    .map-btn {{ background-color: #0284C7; color: white !important; padding: 10px 20px; border-radius: 12px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 15px; }}
    .stButton>button {{ background: linear-gradient(90deg, #0284C7, #38BDF8) !important; color: white !important; border-radius: 12px !important; border: none !important; }}
    </style>
''', unsafe_allow_html=True)

# زر اللغة
col_l1, col_l2 = st.columns([12, 1])
if col_l2.button("عربي/EN"):
    st.session_state.lang = "English" if st.session_state.lang == "العربية" else "العربية"
    st.rerun()

if st.session_state.page == 'welcome':
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown(f'''<div class="glass-card" style="text-align: center;">
        <h1 style="color: #0369A1;">Path7 📍</h1>
        <p style="color: #64748B; font-size: 1.2em;">نظام التوافق اللحظي للسياحة الذكية</p>
    </div>''', unsafe_allow_html=True)
    
    col_w1, col_w2, col_w3 = st.columns([1, 2, 1])
    with col_w2:
        st.session_state.user_name = st.text_input("مرحباً بك، ما هو اسمك؟", placeholder="أدخل اسمك هنا")
        u_budget = st.radio("حدد طابع رحلتك اليوم:", ["اقتصادية", "فاخرة"], horizontal=True)
        if st.button("انطلق لاستكشاف الرياض 🚀"):
            st.session_state.budget_key = "Luxury" if u_budget == "فاخرة" else "Economy"
            st.session_state.page = 'system'
            st.rerun()

else:
    col_m, col_s = st.columns([2.2, 1])
    with col_m:
        st.markdown(f'''<div class="glass-card info-card">
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
                # منطق صارم لمنع ظهور أي نصوص برمجية
                action_part = ""
                if st.session_state.transport_choice:
                    base = p.get('b_time', 20)
                    if st.session_state.transport_choice == "metro":
                        time_txt = f"🚇 الوقت المقدر: {base + 10} دقيقة"
                        info_txt = "🚉 المترو متاح لهذه الوجهة."
                        action_part = f"<p style='font-weight:bold; color:#0369A1;'>{time_txt}</p><p style='color:#0284C7; font-weight:bold;'>{info_txt}</p>"
                    else:
                        time_txt = f"🚗 الوقت المقدر: {int(base * 1.4)} دقيقة"
                        url = f"https://www.google.com/maps/search/?api=1&query={p['الوجهة']}"
                        action_part = f"<p style='font-weight:bold; color:#0369A1;'>{time_txt}</p><a href='{url}' target='_blank' class='map-btn'>📍 فتح في الخرائط</a>"
                else:
                    action_part = "<p style='color:#94A3B8;'>⏳ حدد وسيلة النقل لمعرفة المسار</p>"

                st.markdown(f'''<div class="dest-card">
                    <h4 style="color:#0284C7; margin:0;">{p['الوجهة']}</h4>
                    <p style="color:#64748B;">{p['وصف']}</p>
                    {action_part}
                </div>''', unsafe_allow_html=True)

    with col_s:
        st.markdown(f'<div class="glass-card center-rating"><h4 style="margin-bottom:20px;">{rating_title}</h4>', unsafe_allow_html=True)
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐", key=f"star_{i}"): st.session_state.rated = True
        
        if st.session_state.rated and st.session_state.day < 3:
            st.write("")
            if st.button("اليوم التالي ⏭️"):
                st.session_state.day += 1
                st.session_state.suggestions = []; st.session_state.transport_choice = None; st.session_state.rated = False
                st.rerun()
        
        st.markdown("<hr style='opacity:0.2;'>", unsafe_allow_html=True)
        if st.button(reset_label): st.session_state.clear(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.8em;'>Path7 | Engineering Excellence @ IAU</p>", unsafe_allow_html=True)
