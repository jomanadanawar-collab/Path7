import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

default_weather = "مشمس ☀️" if 5 <= current_hour <= 17 else "ليل صافي 🌙"

st.set_page_config(page_title="Path7 | Smart Journey", layout="wide", initial_sidebar_state="collapsed")

# 2. البيانات مع إضافة "معامل الوقت" (Base Minutes من حي المروج)
PLACES_DB = {
    "اقتصادية": [
        {"الوجهة": "أسواق المعيقيلة", "الفئة": "تسوق", "وصف": "مركز تقليدي للبخور والعود.", "base_time": 25},
        {"الوجهة": "حصن المصمك", "الفئة": "تاريخ وآثار", "وصف": "رمز لتوحيد المملكة وتأسيسها.", "base_time": 28},
        {"الوجهة": "سوق الزل", "الفئة": "تاريخ وآثار", "وصف": "أقدم سوق مليء بالتحف.", "base_time": 27},
        {"الوجهة": "مركز الملك عبد الله المالي (KAFD)", "الفئة": "مطاعم ومقاهي", "وصف": "أيقونة اقتصادية حديثة.", "base_time": 10},
        {"الوجهة": "واجهة روشن", "الفئة": "تسوق", "وصف": "ممشى مفتوح للتسوق والمطاعم.", "base_time": 22},
        {"الوجهة": "وادي حنيفة / نمار", "الفئة": "طبيعة", "وصف": "مساحات خضراء وبحيرات.", "base_time": 35},
        {"الوجهة": "منتزه الملك عبد الله", "الفئة": "طبيعة", "وصف": "نافورات راقصة ومساحات خضراء.", "base_time": 30},
        {"الوجهة": "حافة العالم", "الفئة": "طبيعة", "وصف": "إطلالات منحدرة تخطف الأنفاس.", "base_time": 90}
    ],
    "فاخرة": [
        {"الوجهة": "حي الطريف", "الفئة": "تاريخ وآثار", "وصف": "موقع اليونسكو وقلب التاريخ.", "base_time": 18},
        {"الوجهة": "فيا رياض", "الفئة": "ترفيه", "وصف": "عمارة سلمية ومطاعم عالمية.", "base_time": 15},
        {"الوجهة": "بوليفارد سيتي", "الفئة": "ترفيه", "وصف": "أكبر منطقة للثقافات والألعاب.", "base_time": 12},
        {"الوجهة": "مطل البجيري", "الفئة": "مطاعم ومقاهي", "وصف": "مطاعم راقية بإطلالات تاريخية.", "base_time": 18}
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
    .main-card { background: white; padding: 25px; border-radius: 20px; border-top: 10px solid #1A365D; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .info-box { background: #EBF8FF; padding: 20px; border-radius: 15px; border-right: 6px solid #3182CE; margin-bottom: 15px; }
    .stButton>button { background-color: #1A365D !important; color: white !important; border-radius: 15px; height: 3.5em; width: 100%; }
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    </style>
''', unsafe_allow_html=True)

# 4. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'weather' not in st.session_state: st.session_state.weather = default_weather
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'star_rating' not in st.session_state: st.session_state.star_rating = 0

# --- الصفحة الأولى: الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.form("main_welcome_form"):
        st.markdown('<h1 style="text-align: center; color: #1A365D; margin-bottom:0; font-size: 3em;">📍 Path7</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #718096; margin-top:5px; font-size: 1.2em;">نظام التوافق اللحظي للسياحة الذكية</p>', unsafe_allow_html=True)
        st.markdown('<hr style="margin: 30px 0; opacity: 0.1;">', unsafe_allow_html=True)
        u_name = st.text_input("اسم السائح الموقر", "جُمانة")
        u_budget = st.radio("حدد نوع الميزانية المرصودة للرحلة", ["اقتصادية", "فاخرة"], horizontal=True)
        st.info("📌 سيتم تحديد اهتماماتك لكل يوم داخل اللوحة")
        if st.form_submit_button("بدء المسار الذكي 🚀"):
            st.session_state.user_name = u_name
            st.session_state.user_budget = u_budget
            st.session_state.page = 'system'
            st.rerun()

# --- الصفحة الثانية: لوحة التحكم ---
else:
    col_main, col_stats = st.columns([2, 1])
    with col_main:
        st.markdown(f'''
            <div class="main-card">
                <h3 style="margin:0; color: #1A365D;">اليوم {st.session_state.current_day} من 3</h3>
                <p>مرحباً يا <b>{st.session_state.user_name}</b> | الجو الآن: <b>{st.session_state.weather}</b></p>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        u_daily_interests = st.multiselect(
            f"ما هي اهتماماتك لليوم {st.session_state.current_day}؟", 
            ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"],
            key=f"interests_day_{st.session_state.current_day}"
        )

        if st.button("تحليل الوجهات الأنسب لهذا اليوم 🔍"):
            if not u_daily_interests:
                st.error("لطفاً، اختر اهتماماً واحداً على الأقل.")
            else:
                available = PLACES_DB[st.session_state.user_budget]
                final_list = []
                for interest in u_daily_interests:
                    matches = [p for p in available if p["الفئة"] == interest]
                    if matches: final_list.append(random.choice(matches))
                st.session_state.suggestions = final_list
                st.session_state.traffic_factor = random.uniform(1.0, 1.8) # معامل الزحمة العشوائي

        if st.session_state.suggestions:
            transport = st.selectbox("اختر وسيلة النقل لمعرفة الأوقات:", ["-- اختر --", "مترو الرياض", "سيارتي الخاصة", "تاكسي"])
            
            for place in st.session_state.suggestions:
                # منطق حساب الوقت المتغير بناءً على الوجهة
                base = place['base_time']
                if transport == "مترو الرياض":
                    final_time = f"{base + 5} دقيقة (عبر محطة كافد)"
                    icon = "🚇"
                elif transport == "سيارتي الخاصة":
                    final_time = f"{int(base * st.session_state.traffic_factor)} دقيقة"
                    icon = "🚗"
                elif transport == "تاكسي":
                    final_time = f"{int(base * st.session_state.traffic_factor) + 3} دقيقة"
                    icon = "🚕"
                else:
                    final_time = "يرجى اختيار وسيلة نقل"
                    icon = "📍"

                st.markdown(f'''
                    <div class="info-box">
                        <h4 style="margin:0; color:#2B6CB0;">{icon} {place['الوجهة']}</h4>
                        <p style="margin:2px 0; font-size:0.9em;">{place['وصف']}</p>
                        <hr style="margin:10px 0; opacity:0.1;">
                        <p style="margin:0; font-weight:bold; color:#2D3748;">الوقت المتوقع للوصول: {final_time}</p>
                    </div>
                ''', unsafe_allow_html=True)

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
                st.success("✨ نتمنى لك رحلة سعيدة في الرياض! ✨")

    with col_stats:
        st.subheader("⚙️ النظام")
        st.write(f"⏰ {now_riyadh.strftime('%I:%M %p')}")
        if st.button("🔄 إعادة ضبط"):
            st.session_state.clear()
            st.rerun()

st.markdown("<br><p style='text-align: center; color: #A0AEC0; font-size: 0.8em;'>Path7 | Engineering @ IAU</p>", unsafe_allow_html=True)
