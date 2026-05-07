import streamlit as st
import random
from datetime import datetime

# --- 1. إعداد الوقت الفعلي بدقة (Real-time Sync) ---
now = datetime.now()
days_ar = {
    "Monday": "الاثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء",
    "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت", "Sunday": "الأحد"
}
current_day = days_ar[now.strftime("%A")]
current_hour = now.hour

# --- 2. إعدادات الصفحة الفخمة ---
st.set_page_config(page_title="Path7 | Smart Navigation", layout="wide")

# --- 3. التنسيق الجمالي (IBM Plex + ألوان هادئة) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }
    
    .stApp { background-color: #F8F9FB; }
    
    /* بطاقة الترحيب العلوية */
    .hero-section {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 40px;
        border-radius: 25px;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(30, 60, 114, 0.2);
    }
    
    .status-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-right: 8px solid #3182CE;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. الهيدر (Header) ---
st.markdown(f"""
    <div class="hero-section">
        <h1 style='color: white; margin-bottom: 10px;'>📍 Path7</h1>
        <h3 style='color: #e0e0e0;'>مرحباً بكِ يا مهندسة {st.sidebar.text_input("الاسم", "جُمانة")} ✨</h3>
        <p style='font-size: 1.1em;'>اليوم: {current_day} | الساعة: {current_hour}:00 (توقيت الرياض المباشر)</p>
    </div>
""", unsafe_allow_html=True)

# --- 5. قاعدة البيانات ---
destinations = {
    "تاريخ": {"Low": ["قصر المصمك", "المتحف الوطني"], "High": ["حي الطريف", "مطل البجيري"]},
    "ترفيه": {"Low": ["حديقة السويدي"], "High": ["بوليفارد وورلد", "ڤيا رياض"]},
    "طبيعة": {"Low": ["وادي حنيفة"], "High": ["منتجع نوفا"]}
}

# --- 6. المحتوى الرئيسي ---
col_main, col_side = st.columns([2, 1])

with col_side:
    st.markdown("### 🛂 التفضيلات")
    interest = st.selectbox("الاهتمام", ["تاريخ", "ترفيه", "طبيعة"])
    budget = st.radio("الميزانية", ["اقتصادية (Low)", "فاخرة (High)"], horizontal=True)
    budget_key = "Low" if "اقتصادية" in budget else "High"
    
    st.markdown("---")
    # نظام النجوم اللي تحبينه
    st.write("⭐ **تقييمك للنظام**")
    stars = st.select_slider("", options=[1, 2, 3, 4, 5], value=5)
    st.markdown(f"<h2 style='text-align: center;'>{'⭐' * stars}</h2>", unsafe_allow_html=True)

with col_main:
    st.markdown("### 🗓️ التحليل الذكي للمسار")
    
    # محاكاة ذكية للزحمة بناءً على "اليوم والوقت الفعلي"
    is_weekend_rush = current_day in ["الخميس", "الجمعة", "السبت"] and (16 <= current_hour <= 23)
    traffic_score = random.randint(85, 98) if is_weekend_rush else random.randint(20, 45)
    
    if st.button("توليد المسار اللحظي 🚀"):
        place = random.choice(destinations[interest][budget_key])
        
        st.markdown(f"""
            <div class="status-box">
                <h2 style='color: #1A365D;'>📍 الوجهة المقترحة: {place}</h2>
                <p style='font-size: 1.2em;'>حالة الطريق الآن: {'🔴 مزدحم جداً' if traffic_score > 80 else '🟢 سالك وجميل'}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if traffic_score > 80:
            st.error(f"تنبيه: نسبة الازدحام {traffic_score}% - بما أن اليوم {current_day}، ننصحكِ بتأجيل الانطلاق قليلاً.")
        else:
            st.success("الوقت مثالي للانطلاق! استمتعي برحلتكِ.")

    st.markdown("---")
    # مؤشرات سريعة (بدون جداول معقدة)
    c1, c2 = st.columns(2)
    with c1:
        st.metric("حالة الجو الآن", "صافي 🌙" if current_hour > 18 else "مشمس ☀️")
    with c2:
        st.metric("نسبة الازدحام", f"{traffic_score}%", delta="-5%" if traffic_score < 50 else "+12%")

st.caption(f"Path7 Intelligence | Developed for IAU Engineering | Last Sync: {now.strftime('%H:%M')}")
