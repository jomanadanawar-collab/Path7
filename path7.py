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

# 2. البيانات المحدثة (واقعية المترو)
# [cite: 1, 2]
PLACES_DB = {
    "اقتصادية": [
        {"الوجهة": "أسواق المعيقيلة", "الفئة": "تسوق", "وصف": "مركز تقليدي للبخور والعود.", "base_time": 25, "metro_access": True},
        {"الوجهة": "حصن المصمك", "الفئة": "تاريخ وآثار", "وصف": "رمز لتوحيد المملكة وتأسيسها.", "base_time": 28, "metro_access": True},
        {"الوجهة": "سوق الزل", "الفئة": "تاريخ وآثار", "وصف": "أقدم سوق مليء بالتحف.", "base_time": 27, "metro_access": True},
        {"الوجهة": "مركز الملك عبد الله المالي (KAFD)", "الفئة": "مطاعم ومقاهي", "وصف": "أيقونة اقتصادية حديثة.", "base_time": 10, "metro_access": True},
        {"الوجهة": "واجهة روشن", "الفئة": "تسوق", "وصف": "ممشى مفتوح للتسوق والمطاعم.", "base_time": 22, "metro_access": False},
        {"الوجهة": "وادي حنيفة / نمار", "الفئة": "طبيعة", "وصف": "مساحات خضراء وبحيرات.", "base_time": 35, "metro_access": False},
        {"الوجهة": "منتزه الملك عبد الله", "الفئة": "طبيعة", "وصف": "نافورات راقصة ومساحات خضراء.", "base_time": 30, "metro_access": False},
        {"الوجهة": "حافة العالم", "الفئة": "طبيعة", "وصف": "إطلالات منحدرة تخطف الأنفاس.", "base_time": 90, "metro_access": False}
    ],
    "فاخرة": [
        {"الوجهة": "حي الطريف", "الفئة": "تاريخ وآثار", "وصف": "موقع اليونسكو وقلب التاريخ.", "base_time": 18, "metro_access": True},
        {"الوجهة": "فيا رياض", "الفئة": "ترفيه", "وصف": "عمارة سلمية ومطاعم عالمية.", "base_time": 15, "metro_access": False},
        {"الوجهة": "بوليفارد سيتي", "الفئة": "ترفيه", "وصف": "أكبر منطقة للثقافات والألعاب.", "base_time": 12, "metro_access": False},
        {"الوجهة": "مطل البجيري", "الفئة": "مطاعم ومقاهي", "وصف": "مطاعم راقية بإطلالات تاريخية.", "base_time": 18, "metro_access": True}
    ]
}

# 3. التنسيق الجمالي المطور (تدرجات الأزرق والسماوي)
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }

    .stApp { background-color: #F0F9FF !important; } /* خلفية سماوية فاتحة جداً */

    /* صناديق العناوين والأسئلة البارزة */
    .highlight-box {
        background-color: #E0F2FE; /* سماوي فاتح */
        padding: 20px; border-radius: 18px;
        border-right: 10px solid #0EA5E9; /* أزرق سماوي غامق */
        margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .main-card { 
        background: white; padding: 25px; border-radius: 25px; 
        border-top: 12px solid #0284C7; box-shadow: 0 10px 30px rgba(0,0,0,0.08); 
    }

    .info-box { 
        background: white; padding: 20px; border-radius: 20px; 
        border: 1px solid #BAE6FD; border-right: 8px solid #38BDF8; 
        margin-bottom: 15px; 
    }

    /* توحيد تصميم الأزرار */
    .stButton>button {
        background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important;
        color: white !important; border: none !important;
        border-radius: 15px !important; height: 3.8em !important; 
        font-weight: bold !important; font-size: 1.1em !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px); box-shadow: 0 5px 15px rgba(2, 132, 199, 0.3);
    }

    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    </style>
''', unsafe_allow_html=True)

# 4. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'weather' not in st.session_state: st.session_state.weather = default_weather
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'star_rating' not in st.session_state: st.session_state.star_rating = 0
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

# --- الصفحة الأولى: الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.form("main_welcome_form"):
        st.markdown('<h1 style="text-align: center; color: #0369A1; margin-bottom:0; font-size: 3.5em;">📍 Path7</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #64748B; margin-top:5px; font-size: 1.3em;">نظام التوافق اللحظي للسياحة الذكية</p>', unsafe_allow_html=True)
        st.markdown('<hr style="margin: 30px 0; opacity: 0.1;">', unsafe_allow_html=True)
        u_name = st.text_input("اسم السائح الموقر", "جُمانة")
        u_budget = st.radio("حدد نوع الميزانية للرحلة", ["اقتصادية", "فاخرة"], horizontal=True)
        if st.form_submit_button("استكشف مسارك الآن 🚀"):
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
                <h3 style="margin:0; color: #0369A1;">📅 اليوم {st.session_state.current_day} من 3</h3>
                <p style="color: #475569;">مرحباً يا <b>{st.session_state.user_name}</b> | الجو في الرياض: <b>{st.session_state.weather}</b></p>
            </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # إبراز سؤال الاهتمامات
        st.markdown(f'''
            <div class="highlight-box">
                <h4 style="margin:0; color: #0369A1;">🌟 ما هي اهتماماتك المفضلة لليوم {st.session_state.current_day}؟</h4>
                <p style="font-size: 0.9em; color: #64748B; margin: 5px 0 0 0;">(يمكنك اختيار أكثر من خيار لرسم مسار متنوع)</p>
            </div>
        ''', unsafe_allow_html=True)
        
        u_daily_interests = st.multiselect(
            "", 
            ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"],
            key=f"interests_day_{st.session_state.current_day}",
            label_visibility="collapsed"
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
                st.session_state.traffic_factor = random.uniform(1.0, 1.8)
                st.session_state.transport_choice = None # تصفير الوسيلة عند تغيير الوجهات

        if st.session_state.suggestions:
            st.markdown("<br>", unsafe_allow_html=True)
            # إبراز اختيار وسيلة النقل
            st.markdown(f'''
                <div class="highlight-box">
                    <h4 style="margin:0; color: #0369A1;">🚕 كيف تفضل الوصول لوجهاتك اليوم؟</h4>
                    <p style="font-size: 0.9em; color: #64748B; margin: 5px 0 0 0;">اختر الوسيلة لتحديث أوقات الوصول في البطاقات أدناه</p>
                </div>
            ''', unsafe_allow_html=True)
            
            # فحص إمكانية المترو
            no_metro_places = [p['الوجهة'] for p in st.session_state.suggestions if not p['metro_access']]
            
            t_col1, t_col2, t_col3 = st.columns(3)
            
            if not no_metro_places:
                if t_col1.button("🚇 مترو الرياض"): st.session_state.transport_choice = "مترو"
            else:
                t_col1.markdown('<p style="text-align:center; color:#94A3B8; font-size:0.8em; margin-top:15px;">المترو غير متاح لهذه الوجهات ❌</p>', unsafe_allow_html=True)
                
            if t_col2.button("🚗 سيارتي"): st.session_state.transport_choice = "سيارة"
            if t_col3.button("🚕 تاكسي"): st.session_state.transport_choice = "تاكسي"

            for place in st.session_state.suggestions:
                base = place['base_time']
                if st.session_state.transport_choice == "مترو":
                    final_time = f"{base + 5} دقيقة"
                    icon = "🚇"
                elif st.session_state.transport_choice == "سيارة":
                    final_time = f"{int(base * st.session_state.traffic_factor)} دقيقة"
                    icon = "🚗"
                elif st.session_state.transport_choice == "تاكسي":
                    final_time = f"{int(base * st.session_state.traffic_factor) + 3} دقيقة"
                    icon = "🚕"
                else:
                    final_time = "بانتظار اختيارك..."
                    icon = "📍"

                st.markdown(f'''
                    <div class="info-box">
                        <h4 style="margin:0; color:#0284C7;">{icon} {place['الوجهة']}</h4>
                        <p style="margin:2px 0; font-size:0.9em; color:#475569;">{place['وصف']}</p>
                        <p style="margin:10px 0 0 0; font-weight:bold; color:#0369A1;">⏱️ الوقت المقدر: {final_time}</p>
                    </div>
                ''', unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("⭐ تقييمك لليوم")
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐", key=f"s{i}"): st.session_state.star_rating = i
        
        if st.session_state.star_rating > 0:
            if st.session_state.current_day < 3:
                if st.button("التوجه نحو مسار اليوم التالي ⏩"):
                    st.session_state.current_day += 1
                    st.session_state.suggestions = []
                    st.session_state.star_rating = 0
                    st.session_state.transport_choice = None
                    st.session_state.weather = random.choice(["مشمس ☀️", "غائم ⛅", "لطيف 🍃"])
                    st.rerun()
            else:
                st.success("✨ شكراً لاستخدامك Path7.. نتمنى لك ذكريات لا تُنسى في الرياض! ✨")

    with col_stats:
        st.subheader("⚙️ النظام")
        st.write(f"🕒 {now_riyadh.strftime('%I:%M %p')}")
        if st.button("🔄 ضبط جديد"):
            st.session_state.clear()
            st.rerun()

st.markdown("<br><p style='text-align: center; color: #94A3B8; font-size: 0.8em;'>Path7 | Engineering Excellence @ IAU</p>", unsafe_allow_html=True)
