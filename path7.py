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

# 3. التنسيق الجمالي (CSS)
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;600;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }
    .stApp { background-color: #F8F9FB; }
    
    .letter-container {
        background: white;
        padding: 40px;
        border-radius: 30px;
        box-shadow: 0 15px 50px rgba(0,0,0,0.05);
        border-top: 12px solid #1A365D;
        max-width: 700px;
        margin: 40px auto;
    }
    .system-card {
        background-color: white; padding: 25px; border-radius: 15px;
        border-right: 8px solid #3182CE; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    </style>
''', unsafe_allow_html=True)

# إدارة حالة الصفحة والبيانات
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# --- المشهد الأول: الرسالة التي تحتوي على القائمة (المدخلات) ---
if st.session_state.page == 'welcome':
    st.markdown('''
        <div class="letter-container">
            <h1 style="color: #1A365D; text-align: center;">📍 مرحباً بك في Path7</h1>
            <p style="font-size: 1.2em; color: #4A5568; text-align: center; line-height: 1.6;">
                نحن هنا لنرسم لك المسار الأمثل لاستكشاف الرياض.<br>
                فضلاً، زودنا بتفضيلاتك لنبدأ التحليل اللحظي.
            </p>
        </div>
    ''', unsafe_allow_html=True)
    
    # وضع المدخلات داخل حاوية الرسالة
    with st.container():
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            st.session_state.user_name = st.text_input("ما هو اسمك؟", "زائر")
            st.session_state.user_interest = st.selectbox("بماذا تهتم اليوم؟", ["تاريخ", "ترفيه", "طبيعة"])
            st.session_state.user_budget = st.radio("حدد ميزانيتك:", ["اقتصادية (Low)", "فاخرة (High)"], horizontal=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("توليد المسار والتوافق اللحظي 🚀", use_container_width=True):
                st.session_state.page = 'system'
                st.rerun()

# --- المشهد الثاني: صفحة التوافق اللحظي والنتائج ---
else:
    # زر العودة في القائمة الجانبية
    if st.sidebar.button("🏠 العودة لتعديل البيانات"):
        st.session_state.page = 'welcome'
        st.rerun()

    st.markdown("<h1 style='text-align: center;'>تحليل المسار اللحظي</h1>", unsafe_allow_html=True)
    
    col_main, col_stats = st.columns([2, 1])
    
    with col_main:
        st.markdown(f'''
            <div class="system-card">
                <h3>أهلاً بك {st.session_state.user_name} ✨</h3>
                <p>بناءً على اهتمامك بـ (<b>{st.session_state.user_interest}</b>)، إليك النتيجة:</p>
            </div>
        ''', unsafe_allow_html=True)

        # منطق التوافق اللحظي
        destinations = {
            "تاريخ": {"Low": ["قصر المصمك"], "High": ["حي الطريف"]},
            "ترفيه": {"Low": ["حديقة السويدي"], "High": ["بوليفارد وورلد"]},
            "طبيعة": {"Low": ["وادي حنيفة"], "High": ["منتجع نوفا"]}
        }
        
        budget_key = "Low" if "اقتصادية" in st.session_state.user_budget else "High"
        place = random.choice(destinations[st.session_state.user_interest][budget_key])
        traffic = random.randint(15, 95)
        
        st.info(f"📍 الوجهة المقترحة الآن: {place}")
        if traffic > 80:
            st.warning(f"⚠️ تنبيه ازدحام: الطريق مزدحم حالياً بنسبة ({traffic}%)")
        else:
            st.success(f"✅ الطريق سالك ({traffic}%) ومثالي للزيارة.")

        st.markdown("---")
        st.subheader("⭐ تقييم النظام")
        stars = st.select_slider("قيم تجربتك:", options=[1, 2, 3, 4, 5], value=5)
        st.markdown(f"<h2 style='text-align: center;'>{'⭐' * stars}</h2>", unsafe_allow_html=True)

    with col_stats:
        st.subheader("📊 مؤشرات الحظة")
        st.metric("توقيت الرياض", now_riyadh.strftime('%I:%M %p'))
        st.metric("حالة الجو", "صافي", "🌙" if current_hour > 18 or current_hour < 6 else "☀️")
        st.metric("الازدحام المتوقع", f"{traffic}%")

st.markdown("<br><p style='text-align: center; color: #A0AEC0;'>Path7 | IAU Engineering</p>", unsafe_allow_html=True)
