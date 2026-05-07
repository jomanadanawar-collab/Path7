import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. ضبط التوقيت المباشر لمدينة الرياض
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

# 2. إعدادات الصفحة (جعل القائمة الجانبية مفتوحة دائمًا)
st.set_page_config(
    page_title="Path7", 
    layout="wide", 
    initial_sidebar_state="expanded" # هذا السطر يثبت القائمة
)

# 3. التنسيق الجمالي
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

# 4. العنوان والترحيب
st.markdown("<h1>📍 Path7</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #718096;'>نظام إدارة المسارات الذكية | جامعة الإمام عبدالرحمن بن فيصل</p>", unsafe_allow_html=True)

with st.sidebar:
    st.header("🛂 تفاصيل الرحلة")
    name = st.text_input("اسم المستخدم", "زائر")
    st.markdown("---")
    budget = st.radio("الميزانية", ["اقتصادية (Low)", "فاخرة (High)"])
    budget_key = "Low" if "اقتصادية" in budget else "High"
    sim_hour = st.select_slider("ساعة الزيارة", options=list(range(24)), value=current_hour)
    interest = st.selectbox("الاهتمامات", ["تاريخ", "ترفيه", "طبيعة"])

col_main, col_stats = st.columns([2, 1])

with col_main:
    # الترحيب بصيغة المذكر العامة وبدون ألقاب
    st.markdown(f'''
        <div class="welcome-card">
            <h3>أهلاً بك {name} ✨</h3>
            <p>نساعدك في تخطيط مسار ذكي يوافق تطلعاتك. التوقيت الحالي في الرياض {now_riyadh.strftime('%I:%M %p')}.</p>
        </div>
    ''', unsafe_allow_html=True)

    st.subheader("🗓️ المسار المقترح")
    if st.button("تحديث وتحليل المسار"):
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
            st.success(f"✅ الطريق سالك ({traffic}%). استمتع بوقتك!")

    st.markdown("---")
    st.subheader("⭐ تقييم التجربة")
    stars = st.select_slider("قيم النظام:", options=[1, 2, 3, 4, 5], value=5)
    st.markdown(f"<h2 style='text-align: center;'>{'⭐' * stars}</h2>", unsafe_allow_html=True)

with col_stats:
    st.subheader("📊 مؤشرات لحظية")
    weather_icon = "☀️" if 6 <= sim_hour <= 17 else "🌙"
    st.metric("حالة الجو", "صافي", weather_icon)
    st.metric("الازدحام المروري", "متوسط", "-5%")

st.markdown("<br><p style='text-align: center; color: #A0AEC0;'>Path7 Project | College of Engineering - IAU</p>", unsafe_allow_html=True)
