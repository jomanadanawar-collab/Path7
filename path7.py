# 1. تثبيت المكتبات (بسرعة وبدون إزعاج)
!pip install streamlit -q

# 2. طباعة الساعة الحالية عشان تعرفينها قبل يفتح الموقع
from datetime import datetime
h = datetime.now().hour
print(f"⏰ ساعة النظام الآن هي: {h}:00")

# 3. كتابة الكود داخل ملف app.py
with open("app.py", "w", encoding="utf-8") as f:
    f.write(f"""
import streamlit as st
import random

riyadh_destinations = {{
    "تاريخ": {{
        "Low": [{"name": "قصر المصمك", "start": 8, "end": 21}, {"name": "المتحف الوطني", "start": 9, "end": 19}],
        "High": [{"name": "حي الطريف بالدرعية", "start": 10, "end": 24}, {"name": "مطل البجيري", "start": 10, "end": 24}]
    }},
    "ترفيه": {{
        "Low": [{"name": "حديقة السويدي", "start": 16, "end": 23}],
        "High": [{"name": "بوليفارد وورلد", "start": 16, "end": 23}, {"name": "ڤيا رياض", "start": 10, "end": 23}]
    }},
    "طبيعة": {{
        "Low": [{"name": "وادي حنيفة", "start": 0, "end": 24}],
        "High": [{"name": "منتجع نوفا", "start": 9, "end": 18}]
    }}
}}

st.set_page_config(page_title="Path7", layout="wide")

# التنسيق العربي وخط IBM
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {{
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }}
    .stApp {{ background-color: #F8F9FB; }}
    .welcome-card {{
        background-color: white; padding: 20px; border-radius: 15px;
        border-right: 8px solid #3182CE; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    </style>
''', unsafe_allow_html=True)

st.markdown("<h1>📍 Path7</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🛂 تفاصيل الرحلة")
    gender = st.radio("الجنس", ["أنثى", "ذكر"], horizontal=True)
    name = st.text_input("اسم المسافر", "جُمانة")
    budget = st.radio("الميزانية", ["اقتصادية (Low)", "فاخرة (High)"])
    budget_key = "Low" if "اقتصادية" in budget else "High"
    # شريط اختيار الساعة (محاكة)
    sim_hour = st.select_slider("اختر ساعة الزيارة الآن:", options=list(range(24)), value={h})
    interest = st.selectbox("الاهتمام", ["تاريخ", "ترفيه", "طبيعة"])

col_main, col_stats = st.columns([2, 1])

with col_main:
    welcome_msg = f"أهلاً بكِ يا مهندسة {{name}} ✨" if gender == "أنثى" else f"أهلاً بك يا مهندس {{name}} ✨"
    st.markdown(f'<div class="welcome-card"><h3>{{welcome_msg}}</h3><p>دعينا نخطط لكِ مساراً مذهلاً لجامعة IAU بناءً على وقتك المختار.</p></div>', unsafe_allow_html=True)

    if st.button("توليد المسار"):
        options = riyadh_destinations[interest][budget_key]
        event = random.choice(options)
        st.info(f"📍 الوجهة المقترحة: {{event['name']}}")

    st.markdown("---")
    st.subheader("⭐ التقييم")
    stars = st.select_slider("قيم تجربتك:", options=[1,2,3,4,5], value=5)
    st.markdown(f"<h2 style='text-align:center;'>{{'⭐' * stars}}</h2>", unsafe_allow_html=True)

with col_stats:
    st.subheader("📉 بيانات الجو")
    icon, desc = ("☀️", "نهار مشرق") if 6 <= sim_hour <= 17 else ("🌙", "ليل هادئ")
    st.metric("حالة الجو", desc, icon)
""")

# 4. تشغيل الموقع بدون نفق IP (باستخدام خادم ستريمليت المدمج)
!npx localtunnel --port 8501 & streamlit run app.py
