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

# 3. تنسيق CSS شامل ودقيق جداً (لإجبار النمط الفاتح وتوضيح دائرة التقييم بالكحلي)
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;600;700&display=swap');
    
    /* إجبار الألوان الفاتحة وتحديد الخط */
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right; color: #2D3748 !important;
    }
    .stApp { background-color: #F8F9FB !important; }

    /* تنسيق البوكس الترحيبي (الفورم) */
    [data-testid="stForm"] {
        background: white !important;
        padding: 30px !important;
        border-radius: 25px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08) !important;
        border-top: 12px solid #1A365D !important;
        border-left: none !important; border-right: none !important; border-bottom: none !important;
        max-width: 650px;
        margin: auto;
    }

    /* === تعديل السلايدر (التقييم) ليكون كحلي وواضح جداً === */
    
    /* 1. لون الخط الخلفي (الرمادي الفاتح) */
    div[data-baseweb="slider"] > div > div {
        background-color: #EDF2F7 !important;
    }
    
    /* 2. لون الجزء النشط من الخط (الكحلي) */
    div[data-baseweb="slider"] > div > div > div {
        background-color: #1A365D !important;
    }
    
    /* 3. تنسيق الدائرة نفسها (جعلها كحلي غامق وبارز) */
    div[role="slider"] { 
        background-color: #1A365D !important; 
        border: 3px solid #FFFFFF !important; /* حدود بيضاء سميكة لتبرز */
        box-shadow: 0 2px 6px rgba(0,0,0,0.3) !important; /* ظل قوي لتوضيح المكان */
        width: 24px !important; 
        height: 24px !important;
        margin-top: -10px !important; /* موازنة وضعية الدائرة على الخط */
    }

    /* إخفاء القوائم الجانبية */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    </style>
''', unsafe_allow_html=True)

# 4. إدارة الحالة (Session State) لمنع تغير الزحمة
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'dest_result' not in st.session_state: st.session_state.dest_result = None
if 'traffic_val' not in st.session_state: st.session_state.traffic_val = None

# --- الصفحة الأولى: البوكس الكحلي (كل شيء بالداخل) ---
if st.session_state.page == 'welcome':
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        with st.form("welcome_form"):
            st.markdown('<h1 style="color: #1A365D; text-align: center;">📍 Path7</h1>', unsafe_allow_html=True)
            st.markdown('<p style="font-size: 1.1em; text-align: center;">مرحباً بك في دليلك الذكي لاستكشاف الرياض.<br>أدخل تفضيلاتك لنبدأ التحليل اللحظي.</p>', unsafe_allow_html=True)
            st.markdown('---')
            
            u_name = st.text_input("الاسم", "زائر")
            u_interest = st.selectbox("بماذا تهتم اليوم؟", ["تاريخ", "ترفيه", "طبيعة"])
            u_budget = st.radio("الميزانية", ["اقتصادية (Low)", "فاخرة (High)"], horizontal=True)
            
            submit = st.form_submit_button("توليد المسار اللحظي 🚀", use_container_width=True)
            
            if submit:
                st.session_state.user_name = u_name
                st.session_state.user_interest = u_interest
                st.session_state.user_budget = u_budget
                st.session_state.page = 'system'
                st.session_state.dest_result = None
                st.rerun()

# --- الصفحة الثانية: النتائج ---
else:
    c1, c2 = st.columns([5, 1])
    with c1: st.markdown("<h2>📍 تحليل المسار اللحظي</h2>", unsafe_allow_html=True)
    with c2:
        if st.button("🔄 تعديل"):
            st.session_state.page = 'welcome'
            st.rerun()

    col_main, col_stats = st.columns([2, 1])
    
    with col_main:
        st.markdown(f'''
            <div style="background: white; padding: 20px; border-radius: 15px; border-right: 8px solid #3182CE; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;">
                <h3>أهلاً بك {st.session_state.user_name} ✨</h3>
                <p>توقيت الرياض الآن: {now_riyadh.strftime("%I:%M %p")}</p>
            </div>
        ''', unsafe_allow_html=True)

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
                st.warning(f"⚠️ تنبيه: الطريق مزدحم ({st.session_state.traffic_val}%)")
            else:
                st.success(f"✅ الطريق سالك ({st.session_state.traffic_val}%)")

        st.markdown("---")
        
        # التقييم (الدائرة الآن كحلي غامق وواضحة جداً وتغييرها لا يغير الزحمة)
        stars = st.select_slider("قيم تجربتك (اسحب الدائرة الكحلية):", options=[1, 2, 3, 4, 5], value=5)
        st.markdown(f"<h2 style='text-align: center; color: #1A365D;'>{'⭐' * stars}</h2>", unsafe_allow_html=True)

    with col_stats:
        st.subheader("📊 مؤشرات")
        st.metric("الطقس", "صافي", "🌙" if current_hour > 18 or current_hour < 6 else "☀️")
        t_text = f"{st.session_state.traffic_val}%" if st.session_state.traffic_val else "--"
        st.metric("الازدحام", t_text)

st.markdown("<br><p style='text-align: center; color: #A0AEC0; font-size: 0.8em;'>Path7 | IAU Engineering</p>", unsafe_allow_html=True)
