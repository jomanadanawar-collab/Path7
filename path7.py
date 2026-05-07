import streamlit as st
import random
from datetime import datetime
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Path7 - Live Sync", layout="wide")

# 2. الحصول على الوقت الفعلي (دقة 100%)
now = datetime.now()
days_map = {
    "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء",
    "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت", "Sunday": "الأحد"
}
current_day_ar = days_map[now.strftime("%A")]
current_hour = now.hour

# 3. قاعدة البيانات
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

# 4. التنسيق الجمالي (IBM Plex Sans Arabic)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;600;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }
    .stApp { background-color: #F8F9FB; }
    .live-status {
        background: linear-gradient(135deg, #1A365D 0%, #2B6CB0 100%);
        color: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1); margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 5. واجهة النظام اللحظية
st.markdown("<h1>📍 Path7: Live System</h1>", unsafe_allow_html=True)

# شريط الحالة العلوي (يربط الوقت الفعلي)
st.markdown(f"""
    <div class="live-status">
        <h2 style='color: white;'>أهلاً بكِ يا  {st.sidebar.text_input("اسمكِ", "جُمانة")} ✨</h2>
        <p style='font-size: 1.2em;'>📅 اليوم: {current_day_ar} | ⏰ الساعة الآن: {current_hour}:00</p>
    
    </div>
""", unsafe_allow_html=True)

col_main, col_stats = st.columns([2, 1])

with col_main:
    with st.expander("🛂 إعدادات التفضيلات", expanded=True):
        interest = st.selectbox("بماذا تشعرين اليوم؟", ["تاريخ", "ترفيه", "طبيعة"])
        budget_key = st.radio("الميزانية", ["Low", "High"], horizontal=True)

    st.subheader("🗓️ التحليل اللحظي للمسار")
    if st.button("توليد مسار متوافق مع الوقت الحالي"):
        options = riyadh_destinations[interest][budget_key]
        place = random.choice(options)
        
        # منطق الزحمة التلقائي (الخميس والجمعة مساءً = زحمة)
        is_busy_time = current_day_ar in ["الخميس", "الجمعة"] and (16 <= current_hour <= 23)
        traffic_val = random.randint(80, 98) if is_busy_time else random.randint(15, 45)
        
        st.write(f"### المقترح: {place['name']}")
        
        if traffic_val > 75:
            st.error(f"🔴 الازدحام شديد جداً ({traffic_val}%). لا ننصح بالتوجه إلى {place['name']} حالياً.")
            st.info("🔄 جاري البحث عن بدائل في مناطق أقل ازدحاماً...")
        else:
            st.success(f"✅ الطريق ممتاز ({traffic_val}%). الوجهة متاحة وتنتظرك!")

    # الجدول الزمني لليوم الحالي فقط
    st.markdown("---")
    st.subheader(f"📅 خطة يوم {current_day_ar} المقترحة")
    plan = {
        "الفترة": ["الصباح", "الظهر", "المساء"],
        "النشاط": ["زيارة ثقافية", "غداء عمل", "ترفيه/استرخاء"],
        "حالة الازدحام": ["🟢 خفيف", "🟡 متوسط", "🔴 مرتفع" if is_busy_time else "🟢 خفيف"]
    }
    st.table(pd.DataFrame(plan))

with col_stats:
    st.subheader("📊 مؤشرات حية")
    
    # عداد الازدحام التلقائي
    traffic_status = "مرتفع جداً 🔴" if is_busy_time else "انسيابي ✅"
    st.metric("حالة الطرق الآن", traffic_status)
    
    # حالة الجو (تتغير تلقائياً)
    weather_icon, weather_desc = ("☀️", "مشمس") if 6 <= current_hour <= 17 else ("🌙", "صافي")
    st.metric("الطقس في الرياض", weather_desc, weather_icon)
    
    st.markdown("---")
    st.write("⭐ **تقييم النظام الذكي**")
    stars = st.select_slider("", options=[1,2,3,4,5], value=5)
    st.write("⭐" * stars)

st.caption(f"Path7 Intelligence System | Sync Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
