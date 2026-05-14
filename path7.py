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
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
formatted_time = now_riyadh.strftime('%I:%M %p')

st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# إدارة الحالة
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

T = DATA_ALL.get(st.session_state.lang, {})

# CSS المحسن مع الأنيميشن
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if st.session_state.lang == "العربية" else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); background-attachment: fixed; }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 30px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.3); margin-bottom: 20px; }}
    .dest-card {{ background: white; padding: 20px; border-radius: 20px; border-right: 12px solid #0EA5E9; margin-bottom: 15px; transition: 0.3s; }}
    .dest-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }}
    .map-btn {{ background-color: #0284C7; color: white !important; padding: 8px 16px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; }}
    .stButton>button {{ background: linear-gradient(90deg, #0284C7, #38BDF8) !important; color: white !important; border-radius: 12px !important; }}
    </style>
''', unsafe_allow_html=True)

if st.session_state.page == 'welcome':
    st.markdown("<br><br><div class='glass-card' style='text-align:center;'><h1>Path7 📍</h1><p>نظام التوافق اللحظي للسياحة الذكية</p></div>", unsafe_allow_html=True)
    st.session_state.user_name = st.text_input("ما هو اسمك؟")
    if st.button("استكشف الرياض"):
        st.session_state.page = 'system'
        st.rerun()

else:
    st.markdown(f"<div class='glass-card'><h3>📅 يوم {st.session_state.day} | 🕒 {formatted_time}</h3><p>أهلاً بك يا {st.session_state.user_name}</p></div>", unsafe_allow_html=True)
    
    selected_ints = st.multiselect("ما هي اهتماماتك اليوم؟", ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"])
    
    if st.button("تحليل المسار الذكي"):
        # محاكاة جلب البيانات من ملف "الميزانية معدلة" [cite: 1, 2]
        db = [{"الوجهة": "حصن المصمك", "وصف": "رمز تأسيس المملكة", "الفئة": "تاريخ وآثار", "b_time": 20},
              {"الوجهة": "فيا الرياض", "وصف": "عمارة سلمية فاخرة", "الفئة": "ترفيه", "b_time": 35}]
        st.session_state.suggestions = [p for p in db if p['الفئة'] in selected_ints] or db[:2]
        st.session_state.transport_choice = None # تصفير الوسيلة عند تغيير المسار
        st.rerun()

    if st.session_state.suggestions:
        st.write("### 🚗 حدد وسيلة النقل لمعرفة الوقت والمسار:")
        t_cols = st.columns(3)
        if t_cols[0].button("🚇 المترو"): st.session_state.transport_choice = "metro"
        if t_cols[1].button("🚗 السيارة"): st.session_state.transport_choice = "car"
        if t_cols[2].button("🚕 التاكسي"): st.session_state.transport_choice = "taxi"

        for p in st.session_state.suggestions:
            # حساب الوقت بناءً على الوسيلة المحددة فقط
            if st.session_state.transport_choice:
                if st.session_state.transport_choice == "metro":
                    time_info = f"🚇 الوقت المقدر بالمترو: {p['b_time'] + 5} دقيقة"
                    action_html = "<span style='color:#0284C7; font-weight:bold;'>🚉 توجه إلى أقرب محطة مترو للموقع.</span>"
                else:
                    emoji = "🚗" if st.session_state.transport_choice == "car" else "🚕"
                    time_info = f"{emoji} الوقت المقدر للطريق: {int(p['b_time'] * 1.4)} دقيقة"
                    action_html = f'<a href="https://www.google.com/maps/search/{p["الوجهة"]}" target="_blank" class="map-btn">📍 فتح المسار في الخرائط</a>'
            else:
                time_info = "🛑 الرجاء اختيار وسيلة نقل لإظهار الوقت"
                action_html = ""

            st.markdown(f'''
                <div class="dest-card">
                    <h4 style="margin:0; color:#0284C7;">{p['الوجهة']}</h4>
                    <p style="color:#64748B;">{p['وصف']}</p>
                    <p style="font-weight:bold;">{time_info}</p>
                    {action_html}
                </div>
            ''', unsafe_allow_html=True)

        # التقييم تحت المقترحات
        st.markdown("<div class='glass-card' style='text-align:center;'><h4>تقييمك للمسار ⭐</h4>", unsafe_allow_html=True)
        st.columns(5) # (أزرار النجوم هنا)
        if st.button("🔄 إعادة البدء"): st.session_state.clear(); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; font-size:0.8em; opacity:0.6;'>Path7 | Engineering Excellence @ IAU</p>", unsafe_allow_html=True)
