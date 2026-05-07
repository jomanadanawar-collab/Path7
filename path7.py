import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. ضبط التوقيت (الرياض 100%)
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

# 2. إعدادات الصفحة (إخفاء القائمة الجانبية تماماً لمنع التكدس)
st.set_page_config(
    page_title="Path7", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 3. إجبار النمط الفاتح وتنسيق CSS الاحترافي
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;600;700&display=swap');
    
    /* إجبار الألوان الفاتحة */
    :root {
        --primary-color: #1A365D;
        --background-color: #F8F9FB;
        --secondary-background-color: #FFFFFF;
        --text-color: #2D3748;
    }

    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
        color: #2D3748 !important;
    }

    /* خلفية التطبيق بيضاء دائماً */
    .stApp { background-color: #F8F9FB !important; }

    /* تنسيق الحاويات */
    .letter-container {
        background: white !important;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border-top: 10px solid #1A365D;
        max-width: 600px;
        margin: 20px auto;
    }
    
    .system-card {
        background-color: white !important;
        padding: 20px;
        border-radius: 15px;
        border-right: 8px solid #3182CE;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* إلغاء القائمة الجانبية تماماً من العرض في الجوال */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    </style>
''', unsafe_allow_html=True)

# إدارة الحالة
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# --- المشهد الأول: الرسالة (المدخلات داخل البطاقة) ---
if st.session_state.page == 'welcome':
    st.markdown('<div class="letter-container">', unsafe_allow_html=True)
    st.markdown('<h1 style="color: #1A365D; text-align: center;">📍 Path7</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.1em;">مرحباً بك في دليلك الذكي لاستكشاف الرياض. فضلاً أدخل تفضيلاتك أدناه:</p>', unsafe_allow_html=True)
    
    st.session_state.user_name = st.text_input("الاسم", "زائر")
    st.session_state.user_interest = st.selectbox("الاهتمام", ["تاريخ", "ترفيه", "طبيعة"])
    st.session_state.user_budget = st.radio("الميزانية", ["اقتصادية (Low)", "فاخرة (High)"], horizontal=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("توليد المسار اللحظي 🚀", use_container_width=True):
        st.session_state.page = 'system'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- المشهد الثاني: صفحة النتائج (بدون Sidebar) ---
else:
    col_header1, col_header2 = st.columns([4, 1])
    with col_header1:
        st.markdown("<h2 style='margin:0;'>📍 تحليل المسار اللحظي</h2>", unsafe_allow_html=True)
    with col_header2:
        if st.button("🔄 تعديل"):
            st.session_state.page = 'welcome'
            st.rerun()

    col_main, col_stats = st.columns([2, 1])
    
    with col_main:
        st.markdown(f'''
            <div class="system-card">
                <h3 style="margin:0;">أهلاً بك {st.session_state.user_name} ✨</h3>
                <p>تم تحليل الوجهات بناءً على توقيت الرياض: {now_riyadh.strftime('%I:%M %p')}</p>
            </div>
        ''', unsafe_allow_html=True)

        destinations = {
            "تاريخ": {"Low": ["قصر المصمك"], "High": ["حي الطريف"]},
            "ترفيه": {"Low": ["حديقة السويدي"], "High": ["بوليفارد وورلد"]},
            "طبيعة": {"Low": ["وادي حنيفة"], "High": ["منتجع نوفا"]}
        }
        
        b_key = "Low" if "اقتصادية" in st.session_state.user_budget else "High"
        place = random.choice(destinations[st.session_state.user_interest][b_key])
        traffic = random.randint(15, 95)
        
        st.info(f"📍 الوجهة المقترحة: {place}")
        if traffic > 80:
            st.warning(f"⚠️ الطريق مزدحم حالياً ({traffic}%)")
        else:
            st.success(f"✅ الطريق سالك ({traffic}%)")

        st.markdown("---")
        stars = st.select_slider("قيم تجربتك:", options=[1, 2, 3, 4, 5], value=5)
        st.markdown(f"<h2 style='text-align: center;'>{'⭐' * stars}</h2>", unsafe_allow_html=True)

    with col_stats:
        st.subheader("📊 مؤشرات")
        st.metric("الطقس", "صافي", "🌙" if current_hour > 18 or current_hour < 6 else "☀️")
        st.metric("الازدحام", f"{traffic}%")

st.markdown("<br><p style='text-align: center; color: #A0AEC0; font-size: 0.8em;'>Path7 | IAU Engineering</p>", unsafe_allow_html=True)
