import streamlit as st
import random
from datetime import datetime
import pandas as pd

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Path7 - Intelligent System", layout="wide")

# --- قاعدة بيانات الوجهات مع "بيانات الازدحام المحاكة" ---
riyadh_destinations = {
    "تاريخ": {
        "Low": [{"name": "قصر المصمك", "start": 8, "end": 21}, {"name": "المتحف الوطني", "start": 9, "end": 19}],
        "High": [{"name": "حي الطريف بالدرعية", "start": 10, "end": 24}, {"name": "مطل البجيري", "start": 10, "end": 24}]
    },
    "ترفيه": {
        "Low": [{"name": "حديقة السويدي", "start": 16, "end": 23}],
        "High": [{"name": "بوليفارد وورلد", "start": 16, "end": 23}, {"name": "ڤيا رياض", "start": 10, "end": 23}]
    },
    "طبيعة": {
        "Low": [{"name": "وادي حنيفة", "start": 0, "end": 24}],
        "High": [{"name": "منتجع نوفا", "start": 9, "end": 18}]
    }
}

# --- التنسيق الجمالي (IBM Plex Sans Arabic) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;600;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }
    .stApp { background-color: #F4F7F9; }
    .status-card {
        background-color: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- القائمة الجانبية (المدخلات الذكية) ---
with st.sidebar:
    st.header("🛂 لوحة التحكم")
    gender = st.radio("الجنس", ["أنثى", "ذكر"], horizontal=True)
    name = st.text_input("اسم المسافر", "جُمانة")
    st.markdown("---")
    budget = st.radio("الميزانية", ["اقتصادية (Low)", "فاخرة (High)"])
    budget_key = "Low" if "اقتصادية" in budget else "High"
    
    # محاكاة الوقت واليوم
    selected_day = st.selectbox("اختر يوم الزيارة:", ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"])
    sim_hour = st.select_slider("ساعة الزيارة المحاكة:", options=list(range(24)), value=datetime.now().hour)
    interest = st.selectbox("الاهتمام الرئيسي", ["تاريخ", "ترفيه", "طبيعة"])

# --- واجهة النظام ---
st.markdown(f"<h1>📍 نظام Path7 </h1>", unsafe_allow_html=True)

col_main, col_stats = st.columns([2, 1])

with col_main:
    # 1. الترحيب الذكي
    welcome_msg = f"أهلاً بكِ يا  {name} ✨" if gender == "أنثى" else f"أهلاً بك يا مهندس {name} ✨"
    st.markdown(f'<div class="status-card"><h3>{welcome_msg}</h3><p>النظام الآن يحلل المسارات ليوم {selected_day} الساعة {sim_hour}:00</p></div>', unsafe_allow_html=True)

    # 2. منطق المطابقة والازدحام (The Core Logic)
    st.subheader("🗓️ المسار المقترح اللحظي")
    
    if st.button("تحديث وتحليل المسار الذكي"):
        options = riyadh_destinations[interest][budget_key]
        
        # محاكاة فحص الازدحام (Random Traffic Simulation)
        traffic_level = random.randint(1, 100) 
        
        # اختيار وجهة عشوائية
        selected_place = random.choice(options)
        
        st.write(f"### فحص الوجهة: {selected_place['name']}")
        
        # شرط 1: هل المكان مفتوح؟
        is_open = selected_place['start'] <= sim_hour < selected_place['end']
        
        # شرط 2: هل الطريق مزدحم؟ (إذا فوق 80% يعتبر زحمة)
        is_crowded = traffic_level > 80

        if is_open and not is_crowded:
            st.success(f"✅ الوجهة مثالية الآن! (الازدحام: {traffic_level}%)")
            st.balloons()
        elif is_open and is_crowded:
            st.warning(f"⚠️ {selected_place['name']} مفتوح، لكن الطريق مزدحم جداً ({traffic_level}%).")
            # اقتراح بديل فوراً من فئة أخرى أو نفس الفئة
            st.info("🔄 اقتراح بديل لتجنب الزحمة: جربي 'وادي حنيفة' أو مكان مفتوح قريب.")
        else:
            st.error(f"⏳ الوجهة مغلقة حالياً. تفتح من {selected_place['start']}:00")

    # 3. جدول ترتيب الأماكن (حسب اليوم)
    st.markdown("---")
    st.subheader(f"📅 جدول مقترحات يوم {selected_day}")
    
    # بناء جدول بيانات (DataFrame)
    schedule_data = {
        "الفترة": ["صباحاً", "ظهراً", "مساءً"],
        "الوجهة المقترحة": [
            riyadh_destinations["تاريخ"][budget_key][0]["name"],
            riyadh_destinations["طبيعة"][budget_key][0]["name"],
            riyadh_destinations["ترفيه"][budget_key][0]["name"]
        ],
        "حالة الازدحام المتوقعة": ["منخفضة", "متوسطة", "عالية"]
    }
    df = pd.DataFrame(schedule_data)
    st.table(df) # عرض جدول مرتب

with col_stats:
    st.subheader("📊 مؤشرات النظام")
    
    # محاكاة حية للازدحام بناءً على ساعة السلايدر
    traffic_sim = "مرتفع 🚩" if (7 <= sim_hour <= 9 or 16 <= sim_hour <= 19) else "منخفض ✅"
    
    st.metric("نسبة الازدحام المروري", traffic_sim)
    
    # الطقس التفاعلي
    icon, desc = ("☀️", "نهار مشرق") if 6 <= sim_hour <= 17 else ("🌙", "ليل هادئ")
    st.metric("حالة الجو", desc, icon)
    
    st.markdown("---")
    st.write("⭐ **تقييم النظام**")
    stars = st.select_slider("", options=[1,2,3,4,5], value=5, key="stars_val")
    st.write("⭐" * stars)

st.caption("Path7 Project | College of Engineering - IAU 2026")
