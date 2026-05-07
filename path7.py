import streamlit as st
import random
from datetime import datetime
import pytz 

# --- 1. ضبط التوقيت المباشر لمدينة الرياض (دقة 100%) ---
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)

days_ar = {
    "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء",
    "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت", "Sunday": "الأحد"
}
current_day = days_ar[now_riyadh.strftime("%A")]
current_hour = now_riyadh.hour

# --- 2. إعدادات الصفحة الفخمة ---
st.set_page_config(page_title="Path7 | Smart Navigation", layout="wide")

# --- 3. التنسيق الجمالي (اللي حبيناه في الأول) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;600;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }
    .stApp { background-color: #F8F9FB; }
    .hero-section {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white; padding: 40px; border-radius: 25px;
        margin-bottom: 30px; box-shadow: 0 15px 35px rgba(30, 60, 114, 0.2);
    }
    .status-box {
        background: white; padding: 20px; border-radius: 15px;
        border-right: 8px solid #3182CE; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. واجهة العرض ---
st.markdown(f"""
    <div class="hero-section">
        <h1 style='color: white; margin-bottom: 10px;'>📍 Path7 Live</h1>
        <h3 style='color: #e0e0e0;'>أهلاً بكِ يا مهندسة جُمانة ✨</h3>
        <p style='font-size: 1.2em; font-weight: bold;'>📅 اليوم: {current_day} | ⏰ الساعة الآن بتوقيت الرياض: {now_riyadh.strftime('%I:%M %p')}</p>
    </div>
""", unsafe_allow_html=True)

# --- 5. قاعدة البيانات ---
destinations = {
    "تاريخ": {"Low": ["قصر المصمك", "المتحف الوطني"], "High": ["حي الطريف", "مطل البجيري"]},
    "ترفيه": {"Low": ["حديقة السويدي"], "High": ["بوليفارد وورلد", "ڤيا رياض"]},
    "طبيعة": {"Low": ["وادي حنيفة"], "High": ["منتجع نوفا"]}
}

col_main, col_side = st.columns([2, 1])

with col_side:
    st.markdown("### 🛂 التحكم")
    interest = st.selectbox("نوع النشاط", ["تاريخ", "ترفيه", "طبيعة"])
    budget = st.radio("الميزانية", ["اقتصادية (Low)", "فاخرة (High)"], horizontal=True)
    budget_key = "Low" if "اقتصادية" in budget else "High"
    st.markdown("---")
    stars = st.select_slider("تقييمك للنظام", options=[1, 2, 3, 4, 5], value=5)
    st.markdown(f"<h2 style='text-align: center;'>{'⭐' * stars}</h2>", unsafe_allow_html=True)

with col_main:
    st.subheader("🗓️ تحليل المسار المعتمد على الوقت")
    
    # محاكاة الزحمة بناءً على اليوم والوقت الفعلي في الرياض
    is_rush = current_day in ["الخميس", "الجمعة"] and (16 <= current_hour <= 23)
    traffic_score = random.randint(85, 99) if is_rush else random.randint(15, 40)
    
    if st.button("توليد المسار اللحظي 🚀"):
        place = random.choice(destinations[interest][budget_key])
        st.markdown(f"""
            <div class="status-box">
                <h2 style='color: #1A365D;'>📍 الوجهة: {place}</h2>
                <p>حالة الطريق الآن: {'🔴 مزدحم جداً' if traffic_score > 80 else '🟢 سالك'}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if traffic_score > 80:
            st.error(f"تنبيه: اليوم {current_day} والزحمة {traffic_score}%، يفضل اختيار مسار بديل.")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1: st.metric("الطقس", "صافي 🌙" if current_hour > 18 or current_hour < 6 else "مشمس ☀️")
    with c2: st.metric("الازدحام اللحظي", f"{traffic_score}%")

st.caption(f"Path7 Intelligence | College of Engineering - IAU | Precise Riyadh Time Sync")
