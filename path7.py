import streamlit as st
import random
from datetime import datetime
import pytz # عشان تضبط الساعة بدون ما نغير شي في الشكل

# 1. ضبط التوقيت (الرياض 100%)
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

# 2. إعدادات الصفحة (نفس اللي حبيتيها بالضبط)
st.set_page_config(page_title="Path7", layout="wide")

# 3. التنسيق الجمالي (رجعنا لكل التفاصيل الأصلية والخطوط الفخمة)
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;600;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }
    .stApp { background-color: #F8F9FB; }
    h1 { color: #1A365D; font-weight: 700; text-align: center; }
    .welcome-card {
        background-color: white; padding: 25px; border-radius: 15px;
        border-right: 8px solid #3182CE; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
''', unsafe_allow_html=True)

# 4. العنوان والترحيب اللي فيه "الفضفضة" والروح
st.markdown("<h1>📍 Path7</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #718096;'>نظام إدارة المسارات الذكية | جامعة الإمام عبدالرحمن بن فيصل</p>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🛂 تفاصيل الرحلة")
    gender = st.radio("الجنس", ["أنثى", "ذكر"], horizontal=True)
    name = st.text_input("اسم المسافر", "جُمانة")
    st.markdown("---")
    budget = st.radio("الميزانية", ["اقتصادية (Low)", "فاخرة (High)"])
    budget_key = "Low" if "اقتصادية" in budget else "High"
    # هنا يقرأ الساعة الحالية تلقائياً
    sim_hour = st.select_slider("ساعة الزيارة المحاكة", options=list(range(24)), value=current_hour)
    interest = st.selectbox("الاهتمامات", ["تاريخ", "ترفيه", "طبيعة"])

col_main, col_stats = st.columns([2, 1])

with col_main:
    # الترحيب اللي يعزز ثقتك (النسخة اللي حبيتيها)
    welcome_msg = f"أهلاً بكِ يا مهندسة {name} ✨" if gender == "أنثى" else f"أهلاً بك يا مهندس {name} ✨"
    st.markdown(f'''
        <div class="welcome-card">
            <h3>{welcome_msg}</h3>
            <p>دعينا نخطط لكِ مساراً هندسياً يوافق تطلعاتكِ، الساعة الآن بتوقيتنا المحلي {current_hour}:00.</p>
        </div>
    ''', unsafe_allow_html=True)

    st.subheader("🗓️ المسار المقترح")
    if st.button("تحديث وتحليل المسار"):
        # نفس منطق الأماكن والزحمة
        destinations = {
            "تاريخ": {"Low": ["قصر المصمك"], "High": ["حي الطريف"]},
            "ترفيه": {"Low": ["حديقة السويدي"], "High": ["بوليفارد وورلد"]},
            "طبيعة": {"Low": ["وادي حنيفة"], "High": ["منتجع نوفا"]}
        }
        place = random.choice(destinations[interest][budget_key])
        
        # محاكاة الزحمة
        traffic = random.randint(10, 95)
        st.info(f"📍 الوجهة المقترحة: {place}")
        
        if traffic > 80:
            st.warning(f"⚠️ تنبيه: الطريق مزدحم حالياً ({traffic}%). يفضل الانتظار.")
        else:
            st.success(f"✅ الطريق سالك ({traffic}%). استمتعي بوقتك!")

    st.markdown("---")
    st.subheader("⭐ تقييم التجربة")
    stars = st.select_slider("قيمينا:", options=[1, 2, 3, 4, 5], value=5)
    st.markdown(f"<h2 style='text-align: center;'>{'⭐' * stars}</h2>", unsafe_allow_html=True)

with col_stats:
    st.subheader("📊 مؤشرات")
    # الطقس والزحمة اللي كانت عاجبتك
    weather_icon = "☀️" if 6 <= sim_hour <= 17 else "🌙"
    st.metric("حالة الجو", "صافي", weather_icon)
    st.metric("الازدحام المروري", "متوسط", "-5%")

st.markdown("<br><p style='text-align: center; color: #A0AEC0;'>Path7 Project | IAU</p>", unsafe_allow_html=True)
