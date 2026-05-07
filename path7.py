content = """
import streamlit as st
import random
from datetime import datetime

# 1. قاعدة بيانات الوجهات
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

st.set_page_config(page_title="Path7", layout="wide")

# 2. التنسيق الجمالي (تعديل الأخطاء السابقة)
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;600;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    .stApp { background-color: #F8F9FB; }
    h1 { color: #1A365D; font-weight: 700; text-align: center; }
    .welcome-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-right: 8px solid #3182CE;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
    ''', unsafe_allow_html=True)

# 3. العنوان الرئيسي
st.markdown("<h1>📍 Path7</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #718096;'>نظام إدارة المسارات الذكية | جامعة الإمام عبدالرحمن بن فيصل</p>", unsafe_allow_html=True)

# 4. القائمة الجانبية
with st.sidebar:
    st.header("🛂 تفاصيل الرحلة")
    gender = st.radio("الجنس", ["أنثى", "ذكر"], horizontal=True)
    name = st.text_input("اسم المسافر", "جُمانة")
    
    st.markdown("---")
    budget = st.radio("مستوى الميزانية", ["اقتصادية (Low)", "فاخرة (High)"])
    budget_key = "Low" if "اقتصادية" in budget else "High"
    sim_hour = st.select_slider("ساعة اليوم المحاكة", options=list(range(24)), value=datetime.now().hour)
    interest = st.selectbox("الاهتمامات الرئيسية", ["تاريخ", "ترفيه", "طبيعة"])

# 5. توزيع المحتوى
col_main, col_stats = st.columns([2, 1])

with col_main:
    # الترحيب المخصص
    if gender == "أنثى":
        welcome_msg = f"أهلاً بكِ يا مهندسة {name} ✨"
        sub_text = "دعينا نخطط لكِ مساراً يوافق تطلعاتكِ."
    else:
        welcome_msg = f"أهلاً بك يا مهندس {name} ✨"
        sub_text = "دعنا نخطط لك مساراً يوافق تطلعاتك."
    
    st.markdown(f'''
        <div class="welcome-card">
            <h3>{welcome_msg}</h3>
            <p>{sub_text}</p>
        </div>
        ''', unsafe_allow_html=True)

    st.subheader("🗓️ المسار المقترح اللحظي")
    if st.button("تحديث وتحليل المسار"):
        options = riyadh_destinations[interest][budget_key]
        event = random.choice(options)
        container = st.container(border=True)
        container.markdown(f"### 📍 {event['name']}")

        if event['start'] <= sim_hour < event['end']:
            container.success(f"✅ متاح الآن: استمتعي بزيارتك!")
        else:
            container.warning(f"⏳ مغلق حالياً: يفتح من {event['start']}:00 إلى {event['end']}:00")

    # النجوم التفاعلية
    st.markdown("---")
    st.subheader("⭐ تقييم تجربتك")
    star_rating = st.select_slider("قيم جودة المقترح:", options=[1, 2, 3, 4, 5], value=5)
    st.markdown(f"<h2 style='text-align: center;'>{'⭐' * star_rating}</h2>", unsafe_allow_html=True)

with col_stats:
    st.subheader("📉 بيانات النظام")
    # الطقس التفاعلي
    if 6 <= sim_hour <= 17:
        weather_icon, weather_desc = "☀️", "نهار مشرق"
    else:
        weather_icon, weather_desc = "🌙", "ليل هادئ"
        
    st.metric("حالة الجو", weather_desc, weather_icon)
    st.metric("الازدحام المروري", "متوسط", "-5%")
    st.metric("دقة المطابقة", "98%")

st.markdown("<br><br><p style='text-align: center; color: #A0AEC0; font-size: 0.8em;'>Path7 Project | College of Engineering - IAU</p>", unsafe_allow_html=True)
"""

with open("app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ تم التحديث بنجاح يا جُمانة! الآن شغلي خلية الـ Tunnel وشوفي النتيجة.")
