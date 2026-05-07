import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. ضبط التوقيت (الرياض 100%)
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

# 2. إعدادات الصفحة
st.set_page_config(page_title="Path7", layout="wide", initial_sidebar_state="collapsed")

# 3. تنسيق CSS (لإجبار كل شيء داخل البوكس الكحلي)
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;600;700&display=swap');
    
    :root { --primary-color: #1A365D; --background-color: #F8F9FB; }

    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right; color: #2D3748 !important;
    }

    .stApp { background-color: #F8F9FB !important; }

    /* البوكس الكحلي الرئيسي */
    .letter-container {
        background: white !important;
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border-top: 12px solid #1A365D;
        max-width: 650px;
        margin: 20px auto;
    }

    .system-card {
        background-color: white !important; padding: 20px; border-radius: 15px;
        border-right: 8px solid #3182CE; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* تنسيق السلايدر (الدائرة) */
    div[role="slider"] { 
        background-color: #1A365D !important; border: 2px solid white !important;
        width: 22px !important; height: 22px !important;
    }

    /* إخفاء أي قوائم جانبية */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    </style>
''', unsafe_allow_html=True)

# 4. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'dest_result' not in st.session_state: st.session_state.dest_result = None
if 'traffic_val' not in st.session_state: st.session_state.traffic_val = None

# --- المشهد الأول: البوكس الكحلي ---
if st.session_state.page == 'welcome':
    # نستخدم st.container() مع CSS مخصص لضمان دخول العناصر داخل البوكس
    with st.container():
        st.markdown('<div class="letter-container">', unsafe_allow_html=True)
        
        # كل هذه العناصر ستظهر "داخل" حدود البوكس
        st.markdown('<h1 style="color: #1A365D; text-align: center; margin-bottom: 0;">📍 Path7</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 1.1em; color: #4A5568; text-align: center; margin-top: 10px;">مرحباً بك في دليلك الذكي لاستكشاف الرياض.<br>فضلاً زودنا بتفضيلاتك لنبدأ التحليل:</p>', unsafe_allow_html=True)
        st.markdown('<hr style="border: 0.5px solid #EDF2F7; margin: 15px 0;">', unsafe_allow_html=True)
        
        # خانات إدخال البيانات (الآن أصبحت تابعة للحاوية المرئية داخل البوكس)
        st.session_state.user_name = st.text_input("الاسم", "زائر")
        st.session_state.user_interest = st.selectbox("بماذا تهتم اليوم؟", ["تاريخ", "ترفيه", "طبيعة"])
        st.session_state.user_budget = st.radio("الميزانية", ["اقتصادية (Low)", "فاخرة (High)"], horizontal=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("توليد المسار اللحظي 🚀", use_container_width=True):
            st.session_state.page = 'system'
            st.session_state.dest_result = None
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

# --- المشهد الثاني: صفحة النتائج ---
else:
    col_h1, col_h2 = st.columns([5, 1])
    with col_h1: st.markdown("<h2 style='margin:0;'>📍 تحليل المسار اللحظي</h2>", unsafe_allow_html=True)
    with col_h2:
        if st.button("🔄 تعديل"):
            st.session_state.page = 'welcome'
            st.rerun()

    col_main, col_stats = st.columns([2, 1])
    
    with col_main:
        st.markdown(f'<div class="system-card"><h3>أهلاً بك {st.session_state.user_name} ✨</h3><p>توقيت الرياض الآن: {now_riyadh.strftime("%I:%M %p")}</p></div>', unsafe_allow_html=True)

        if st.button("تحديث وتحليل الوجهة"):
            destinations = {
                "تاريخ": {"Low": ["قصر المصمك"], "High": ["حي الطريف"]},
                "ترفيه": {"Low": ["حديقة السويدي"], "High": ["بوليفارد وورلد"]},
                "طبيعة": {"Low": ["وادي حنيفة"], "High": ["منتجع نوفا"]}
            }
            b_key = "Low" if "اقتصادية" in st.session_state.user_budget else "High"
            st.session_state.dest_result = random.choice(destinations[st.session_state.user_interest][b_key])
            st.session_state.traffic_val = random.randint(15, 95)

        if st.session_state.dest_result:
            st.info(f"📍 الوجهة المقترحة: {st.session_state.dest_result}")
            if st.session_state.traffic_val > 80:
                st.warning(f"⚠️ تنبيه: الطريق مزدحم جداً ({st.session_state.traffic_val}%)")
            else:
                st.success(f"✅ الطريق سالك ومناسب ({st.session_state.traffic_val}%)")

        st.markdown("---")
        stars = st.select_slider("قيم تجربتك:", options=[1, 2, 3, 4, 5], value=5)
        st.markdown(f"<h2 style='text-align: center;'>{'⭐' * stars}</h2>", unsafe_allow_html=True)

    with col_stats:
        st.subheader("📊 مؤشرات")
        st.metric("الطقس", "صافي", "🌙" if current_hour > 18 or current_hour < 6 else "☀️")
        t_val = f"{st.session_state.traffic_val}%" if st.session_state.traffic_val else "--"
        st.metric("الازدحام", t_val)

st.markdown("<br><p style='text-align: center; color: #A0AEC0; font-size: 0.8em;'>Path7 | IAU Engineering</p>", unsafe_allow_html=True)
