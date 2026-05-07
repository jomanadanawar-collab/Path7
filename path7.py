import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

if 5 <= current_hour <= 17:
    initial_weather = "مشمس ☀️"
else:
    initial_weather = "ليل صافي 🌙"

st.set_page_config(page_title="Path7 | Smart Journey", layout="wide", initial_sidebar_state="collapsed")

# 2. البيانات من الملف (قاعدة بيانات المسار)
# تم استخراجها من 
PLACES_DB = {
    "اقتصادية": [
        {"الوجهة": "أسواق المعيقيلة", "الفئة": "تسوق", "وصف": "مركز تسوق تقليدي للبخور والعود والبشوت."},
        {"الوجهة": "حصن المصمك", "الفئة": "تاريخ وآثار", "وصف": "رمز لتوحيد المملكة وتأسيسها."},
        {"الوجهة": "سوق الزل", "الفئة": "تاريخ وآثار", "وصف": "أقدم سوق مليء بالتاريخ والتحف النادرة."},
        {"الوجهة": "مركز الملك عبد الله المالي (KAFD)", "الفئة": "مطاعم ومقاهي", "وصف": "أيقونة اقتصادية حديثة."},
        {"الوجهة": "واجهة روشن", "الفئة": "تسوق", "وصف": "ممشى مفتوح للتسوق والمطاعم العصرية."},
        {"الوجهة": "وادي حنيفة / نمار", "الفئة": "طبيعة", "وصف": "مساحات خضراء خلابة وبحيرات مثالية للنزهات."},
        {"الوجهة": "منتزه الملك عبد الله", "الفئة": "طبيعة", "وصف": "نافورات راقصة ومساحات خضراء شاسعة."},
        {"الوجهة": "حافة العالم", "الفئة": "طبيعة", "وصف": "إطلالات منحدرة تخطف الأنفاس."}
    ],
    "فاخرة": [
        {"الوجهة": "حي الطريف", "الفئة": "تاريخ وآثار", "وصف": "موقع اليونسكو وقلب التاريخ السعودي."},
        {"الوجهة": "فيا رياض", "الفئة": "ترفيه", "وصف": "عمارة سلمية مع مطاعم وسينما عالمية."},
        {"الوجهة": "بوليفارد سيتي", "الفئة": "ترفيه", "وصف": "أكبر منطقة للثقافات العالمية والألعاب."},
        {"الوجهة": "مطل البجيري", "الفئة": "مطاعم ومقاهي", "وصف": "مطاعم راقية بإطلالات على وادي حنيفة."}
    ]
}

# 3. التنسيق الجمالي (CSS)
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }
    .stApp { background-color: #F4F7F9 !important; }
    [data-testid="stForm"] {
        background: white !important; padding: 50px !important; border-radius: 30px !important;
        border-top: 18px solid #1A365D !important; box-shadow: 0 25px 60px rgba(0,0,0,0.12) !important;
        max-width: 650px !important; margin: auto !important;
    }
    .main-card { background: white; padding: 25px; border-radius: 20px; border-top: 10px solid #1A365D; }
    .info-box { background: #EBF8FF; padding: 20px; border-radius: 15px; border-right: 6px solid #3182CE; margin-bottom: 15px; }
    .stButton>button { background-color: #1A365D !important; color: white !important; border-radius: 15px; width: 100%; height: 3.5em; }
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    </style>
''', unsafe_allow_html=True)

# 4. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []

# --- المشهد الأول: صفحة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.form("main_welcome_form"):
        st.markdown('<h1 style="text-align: center; color: #1A365D; margin-bottom:0; font-size: 3em;">📍 Path7</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #718096; margin-top:5px; font-size: 1.2em;">نظام التوافق اللحظي للسياحة الذكية</p>', unsafe_allow_html=True)
        st.markdown('<hr style="margin: 30px 0; opacity: 0.1;">', unsafe_allow_html=True)
        
        u_name = st.text_input("اسم السائح الموقر", "جُمانة")
        u_budget = st.radio("حدد نوع الميزانية المرصودة للرحلة", ["اقتصادية", "فاخرة"], horizontal=True)
        u_interests = st.multiselect("ما هي اهتماماتك؟", ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"], default=["تاريخ وآثار"])
        
        st.info("📌 مكان الإقامة مثبت: حي المروج (نقطة الانطلاق)")
        if st.form_submit_button("بدء المسار الذكي 🚀"):
            st.session_state.user_name = u_name
            st.session_state.user_budget = u_budget
            st.session_state.user_interests = u_interests
            st.session_state.page = 'system'
            st.rerun()

# --- المشهد الثاني: لوحة التحكم ---
else:
    col_main, col_stats = st.columns([2, 1])
    with col_main:
        st.markdown(f'''
            <div class="main-card">
                <h3 style="margin:0; color: #1A365D;">اليوم {st.session_state.current_day} من 3</h3>
                <p>مرحباً يا <b>{st.session_state.user_name}</b> | الجو: <b>{st.session_state.weather}</b></p>
                <p style="font-size: 0.9em; color: #718096;">الميزانية: {st.session_state.user_budget} | الاهتمامات: {", ".join(st.session_state.user_interests)}</p>
            </div>
        ''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("تحليل الوجهات الأنسب لاختياراتك 🔍"):
            available = PLACES_DB[st.session_state.user_budget]
            final_list = []
            for interest in st.session_state.user_interests:
                matches = [p for p in available if p["الفئة"] == interest]
                if matches: final_list.append(random.choice(matches))
            st.session_state.suggestions = final_list
            st.session_state.traffic = random.randint(20, 60)

        if st.session_state.suggestions:
            for place in st.session_state.suggestions:
                st.markdown(f'''
                    <div class="info-box">
                        <h4 style="margin:0; color:#2B6CB0;">📍 {place['الوجهة']} ({place['الفئة']})</h4>
                        <p style="margin:5px 0;">{place['وصف']}</p>
                    </div>
                ''', unsafe_allow_html=True)
            
            transport = st.selectbox("اختر وسيلة النقل:", ["-- اختر --", "مترو الرياض (محطة كافد)", "سيارتي الخاصة", "تاكسي"])
            if "مترو" in transport:
                st.info("🚇 المترو: الانطلاق من محطة كافد (KAFD) والوصول المتوقع خلال 18 دقيقة.")
            elif "سيارتي" in transport:
                car_time = 25 + st.session_state.traffic // 4
                st.warning(f"🚗 السيارة: الوصول المتوقع للوجهة خلال {car_time} دقيقة.")
            elif "تاكسي" in transport:
                taxi_time = 28 + st.session_state.traffic // 4
                st.success(f"🚕 التاكسي: الوصول المتوقع للوجهة خلال {taxi_time} دقيقة.")

        st.markdown("---")
        st.subheader("⭐ تقييمك لليوم")
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐", key=f"s{i}"): st.session_state.star_rating = i
        
        if st.session_state.star_rating > 0:
            st.markdown(f"<h1 style='text-align: center; color: #FFD700;'>{'⭐' * st.session_state.star_rating}</h1>", unsafe_allow_html=True)
            if st.session_state.current_day < 3:
                if st.button("الانتقال لليوم التالي ⏩"):
                    st.session_state.current_day += 1
                    st.session_state.suggestions = []
                    st.session_state.star_rating = 0
                    st.session_state.weather = random.choice(["مشمس ☀️", "غائم جزئياً ⛅", "لطيف 🍃"])
                    st.rerun()
            else:
                st.success("✨ وصلنا لنهاية الرحلة! نتمنى لك وقتاً ممتعاً في الرياض ✨")

    with col_stats:
        st.subheader("⚙️ النظام")
        st.write(f"⏰ {now_riyadh.strftime('%I:%M %p')}")
        if st.button("🔄 إعادة ضبط"):
            st.session_state.clear()
            st.rerun()

st.markdown("<br><p style='text-align: center; color: #A0AEC0; font-size: 0.8em;'>Path7 | Engineering @ IAU</p>", unsafe_allow_html=True)
