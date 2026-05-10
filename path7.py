import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# 2. قاموس اللغات الشامل (حل مشكلة "العيب" اللغوي)
TRANSLATIONS = {
    "ar": {
        "welcome": "مرحباً يا", "weather_val": "ليل صافي 🌙" if current_hour > 18 else "مشمس ☀️",
        "weather_label": "الجو في الرياض", "interests_list": ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"],
        "eco": "اقتصادية", "lux": "فاخرة", "analyze": "تحليل الوجهات الأنسب 🔍",
        "metro_no": "المترو غير متاح للكل ❌", "time_est": "⏱️ الوقت المقدر:",
        "dir": "rtl", "align": "right"
    },
    "en": {
        "welcome": "Welcome", "weather_val": "Clear Night 🌙" if current_hour > 18 else "Sunny ☀️",
        "weather_label": "Riyadh Weather", "interests_list": ["History", "Entertainment", "Shopping", "Dining", "Nature"],
        "eco": "Economy", "lux": "Luxury", "analyze": "Analyze Destinations 🔍",
        "metro_no": "Metro not available for all ❌", "time_est": "⏱️ Estimated Time:",
        "dir": "ltr", "align": "left"
    }
}

# 3. قاعدة بيانات مزدوجة اللغة (لضمان عدم ظهور نصوص عربية في النسخة الإنجليزية)
PLACES_DB = {
    "ar": {
        "اقتصادية": [
            {"الوجهة": "حصن المصمك", "الفئة": "تاريخ وآثار", "وصف": "رمز لتوحيد المملكة وتأسيسها.", "base_time": 28, "metro_access": True}
        ],
        "فاخرة": [
            {"الوجهة": "فيا رياض", "الفئة": "ترفيه", "وصف": "بوتيكات عالمية فاخرة.", "base_time": 15, "metro_access": False},
            {"الوجهة": "بوليفارد سيتي", "الفئة": "ترفيه", "وصف": "أكبر منطقة للثقافات والألعاب.", "base_time": 12, "metro_access": False}
        ]
    },
    "en": {
        "Economy": [
            {"الوجهة": "Masmak Fortress", "الفئة": "History", "وصف": "A symbol of Saudi unification.", "base_time": 28, "metro_access": True}
        ],
        "Luxury": [
            {"الوجهة": "Via Riyadh", "الفئة": "Entertainment", "وصف": "World-class luxury boutiques.", "base_time": 15, "metro_access": False},
            {"الوجهة": "Boulevard City", "الفئة": "Entertainment", "وصف": "The largest entertainment hub.", "base_time": 12, "metro_access": False}
        ]
    }
}

# 4. إدارة الحالة
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
T = TRANSLATIONS[st.session_state.lang]

# 5. التنسيق (CSS)
st.markdown(f'''
    <style>
    html, body, [class*="css"] {{ direction: {T["dir"]}; text-align: {T["align"]}; font-family: 'Inter', sans-serif; }}
    .info-box {{ background: white; padding: 15px; border-radius: 15px; border-{T["align"]}: 8px solid #38BDF8; margin-bottom: 10px; border: 1px solid #E2E8F0; }}
    </style>
''', unsafe_allow_html=True)

# زر اللغة
if st.button("English 🌐" if st.session_state.lang == 'ar' else "العربية 🌐"):
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
    st.rerun()

# --- عرض البيانات المصححة ---
st.subheader(f"{T['welcome']}  | {T['weather_label']}: {T['weather_val']}")

# استخدام قائمة الاهتمامات المترجمة
u_interests = st.multiselect("", T["interests_list"])

if st.button(T["analyze"]):
    # جلب البيانات بناءً على لغة النظام الحالية فقط
    current_db = PLACES_DB[st.session_state.lang][st.session_state.user_budget]
    # (هنا يوضع منطق الفلترة)
    for p in current_db:
        st.markdown(f'''
            <div class="info-box">
                <h4>📍 {p["الوجهة"]}</h4>
                <p>{p["وصف"]}</p>
                <b>{T["time_est"]} {p["base_time"]} min</b>
            </div>
        ''', unsafe_allow_html=True)
