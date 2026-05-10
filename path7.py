import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
current_hour = now_riyadh.hour

st.set_page_config(page_title="Path7 | Smart Journey", layout="wide", initial_sidebar_state="collapsed")
default_weather = "مشمس ☀️" if 5 <= current_hour <= 17 else "ليل صافي 🌙"

# 2. قاموس اللغات الشامل (Dictionary)
TRANSLATIONS = {
    "ar": {
        "title": "📍 Path7 | المسار الذكي",
        "subtitle": "نظام التوافق اللحظي للسياحة الذكية",
        "name_label": "اسم السائح الموقر",
        "budget_label": "حدد نوع الميزانية للرحلة",
        "eco": "اقتصادية", "lux": "فاخرة",
        "start_btn": "استكشف مسارك الآن 🚀",
        "welcome": "مرحباً يا", "day": "اليوم", "of": "من", "weather": "الجو في الرياض",
        "interests_q": "🌟 ما هي اهتماماتك المفضلة لليوم؟",
        "analyze": "تحليل الوجهات الأنسب لهذا اليوم 🔍",
        "transport_q": "🚕 كيف تفضل الوصول لوجهاتك اليوم؟",
        "metro": "🚇 مترو الرياض", "car": "🚗 سيارتي", "taxi": "🚕 تاكسي",
        "time_est": "⏱️ الوقت المقدر:",
        "rating_title": "⭐ تقييمك لمسار اليوم",
        "next_day_btn": "التوجه نحو مسار اليوم التالي ⏩",
        "finish_msg": "✨ شكراً لاستخدامك Path7.. نتمنى لك ذكريات لا تُنسى في الرياض! ✨",
        "reset_btn": "🔄 ضبط جديد", "lang_btn": "English 🌐",
        "interests_list": ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"],
        "no_match": "عذراً، لا توجد وجهات تطابق هذه الاهتمامات في ميزانيتك.",
        "metro_no": "المترو غير متاح للكل ❌",
        "dir": "rtl", "align": "right"
    },
    "en": {
        "title": "📍 Path7 | Smart Journey",
        "subtitle": "Real-time Smart Tourism Compatibility System",
        "name_label": "Tourist Name",
        "budget_label": "Select Trip Budget",
        "eco": "Economy", "lux": "Luxury",
        "start_btn": "Explore Your Path Now 🚀",
        "welcome": "Welcome", "day": "Day", "of": "of", "weather": "Riyadh Weather",
        "interests_q": "🌟 What are your interests for today?",
        "analyze": "Analyze Best Destinations 🔍",
        "transport_q": "🚕 How do you prefer to get there?",
        "metro": "🚇 Riyadh Metro", "car": "🚗 My Car", "taxi": "🚕 Taxi",
        "time_est": "⏱️ Estimated Time:",
        "rating_title": "⭐ Rate Today's Path",
        "next_day_btn": "Proceed to Next Day ⏩",
        "finish_msg": "✨ Thanks for using Path7.. Have a great stay! ✨",
        "reset_btn": "🔄 Reset", "lang_btn": "العربية 🌐",
        "interests_list": ["History", "Entertainment", "Shopping", "Dining", "Nature"],
        "no_match": "Sorry, no matches found for these interests in your budget.",
        "metro_no": "Metro not available for all ❌",
        "dir": "ltr", "align": "left"
    }
}

# 3. قاعدة البيانات (موحدة للبحث)
PLACES_DB = {
    "اقتصادية": [
        {"الوجهة": "أسواق المعيقلية", "الفئة": "تسوق", "وصف": "مركز تقليدي للبخور والعود.", "base_time": 25, "metro_access": True},
        {"الوجهة": "حصن المصمك", "الفئة": "تاريخ وآثار", "وصف": "رمز لتوحيد المملكة وتأسيسها.", "base_time": 28, "metro_access": True},
        {"الوجهة": "مركز الملك عبدالله المالي (KAFD)", "الفئة": "طبيعة", "وصف": "أيقونة اقتصادية حديثة.", "base_time": 10, "metro_access": True},
        {"الوجهة": "وادي حنيفة", "الفئة": "طبيعة", "وصف": "مساحات خضراء وبحيرات.", "base_time": 35, "metro_access": False}
    ],
    "فاخرة": [
        {"الوجهة": "حي الطريف", "الفئة": "تاريخ وآثار", "وصف": "موقع اليونسكو وقلب التاريخ.", "base_time": 18, "metro_access": True},
        {"الوجهة": "فيا رياض", "الفئة": "ترفيه", "وصف": "عمارة سلمية ومطاعم عالمية.", "base_time": 15, "metro_access": False},
        {"الوجهة": "فيا رياض", "الفئة": "تسوق", "وصف": "بوتيكات عالمية فاخرة.", "base_time": 15, "metro_access": False},
        {"الوجهة": "بوليفارد سيتي", "الفئة": "ترفيه", "وصف": "أكبر منطقة للثقافات والألعاب.", "base_time": 12, "metro_access": False},
        {"الوجهة": "مطل البجيري", "الفئة": "مطاعم ومقاهي", "وصف": "مطاعم حائزة على نجوم ميشلان.", "base_time": 18, "metro_access": True}
    ]
}

# خريطة لترجمة الفئات داخلياً
CAT_MAP = {
    "History": "تاريخ وآثار", "Entertainment": "ترفيه", "Shopping": "تسوق",
    "Dining": "مطاعم ومقاهي", "Nature": "طبيعة"
}

# 4. إدارة الحالة
if 'lang' not in st.session_state: st.session_state.lang = 'ar'
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'weather' not in st.session_state: st.session_state.weather = default_weather
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'star_rating' not in st.session_state: st.session_state.star_rating = 0
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'user_name' not in st.session_state: st.session_state.user_name = "Guest"

T = TRANSLATIONS[st.session_state.lang]

# 5. التنسيق الجمالي
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {{
        font-family: 'IBM Plex Sans Arabic', sans-serif !important; 
        direction: {T["dir"]}; text-align: {T["align"]};
    }}
    .stApp {{ background-color: #F0F9FF !important; }}
    .highlight-box {{
        background-color: #E0F2FE; padding: 20px; border-radius: 18px;
        border-{"right" if st.session_state.lang == 'ar' else "left"}: 10px solid #0EA5E9; margin-bottom: 20px;
    }}
    .main-card {{ background: white; padding: 25px; border-radius: 25px; border-top: 12px solid #0284C7; }}
    .info-box {{ background: white; padding: 20px; border-radius: 20px; border-{"right" if st.session_state.lang == 'ar' else "left"}: 8px solid #38BDF8; margin-bottom: 15px; border: 1px solid #BAE6FD; }}
    .stButton>button {{
        background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important;
        color: white !important; border-radius: 15px !important; height: 3.5em !important; font-weight: bold !important; width: 100%;
    }}
    </style>
''', unsafe_allow_html=True)

# زر اللغة
col_l1, col_l2 = st.columns([0.85, 0.15])
if col_l2.button(T["lang_btn"]):
    st.session_state.lang = 'en' if st.session_state.lang == 'ar' else 'ar'
    st.rerun()

# --- الصفحة الأولى ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.form("welcome_form"):
        st.markdown(f'<h1 style="text-align: center; color: #0369A1;">{T["title"]}</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; color: #64748B;">{T["subtitle"]}</p>', unsafe_allow_html=True)
        u_name = st.text_input(T["name_label"], value="Jumanah") 
        u_budget_display = st.radio(T["budget_label"], [T["eco"], T["lux"]], horizontal=True)
        
        if st.form_submit_button(T["start_btn"]):
            st.session_state.user_name = u_name if u_name else "Guest"
            st.session_state.user_budget = "اقتصادية" if u_budget_display in ["اقتصادية", "Economy"] else "فاخرة"
            st.session_state.page = 'system'
            st.rerun()

# --- الصفحة الثانية ---
else:
    col_main, col_stats = st.columns([2, 1])
    with col_main:
        st.markdown(f'''<div class="main-card">
            <h3>📅 {T["day"]} {st.session_state.current_day} {T["of"]} 3</h3>
            <p>{T["welcome"]} <b>{st.session_state.user_name}</b> | {T["weather"]}: <b>{st.session_state.weather}</b></p>
        </div>''', unsafe_allow_html=True)
        
        st.markdown(f'<br><div class="highlight-box"><h4>{T["interests_q"]}</h4></div>', unsafe_allow_html=True)
        u_interests = st.multiselect("", T["interests_list"], key="m_int", label_visibility="collapsed")

        if st.button(T["analyze"]):
            if not u_interests:
                st.error("⚠️")
            else:
                db = PLACES_DB[st.session_state.user_budget]
                found = []
                for inter in u_interests:
                    # تحويل الاسم للبحث في الداتابيز العربية
                    search_key = CAT_MAP.get(inter, inter)
                    matches = [p for p in db if p["الفئة"] == search_key]
                    if matches: found.append(random.choice(matches))
                
                if found:
                    st.session_state.suggestions = found
                    st.session_state.traffic_factor = random.uniform(1.2, 1.6)
                    st.session_state.transport_choice = None
                else:
                    st.warning(T["no_match"])

        if st.session_state.suggestions:
            st.markdown(f"<br><div class='highlight-box'><h4>{T['transport_q']}</h4></div>", unsafe_allow_html=True)
            t_col1, t_col2, t_col3 = st.columns(3)
            
            can_metro = all(p.get('metro_access') for p in st.session_state.suggestions)
            if can_metro:
                if t_col1.button(T["metro"]): st.session_state.transport_choice = "metro"
            else:
                t_col1.markdown(f'<p style="text-align:center; color:#94A3B8; font-size:0.8em; margin-top:15px;">{T["metro_no"]}</p>', unsafe_allow_html=True)
            
            if t_col2.button(T["car"]): st.session_state.transport_choice = "car"
            if t_col3.button(T["taxi"]): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                t = p['base_time']
                if st.session_state.transport_choice == "metro": res = f"{t+5} min"
                elif st.session_state.transport_choice == "car": res = f"{int(t*st.session_state.traffic_factor)} min"
                elif st.session_state.transport_choice == "taxi": res = f"{int(t*st.session_state.traffic_factor)+3} min"
                else: res = "..."
                
                st.markdown(f'''<div class="info-box"><h4>📍 {p["الوجهة"]}</h4><p>{p["وصف"]}</p><b>{T["time_est"]} {res}</b></div>''', unsafe_allow_html=True)

            st.markdown("---")
            st.subheader(T["rating_title"])
            stars = st.columns(5)
            for i in range(1, 6):
                if stars[i-1].button(f"{i}⭐", key=f"s_{i}"): st.session_state.star_rating = i

            if st.session_state.star_rating > 0:
                if st.session_state.current_day < 3:
                    if st.button(T["next_day_btn"]):
                        st.session_state.current_day += 1
                        st.session_state.suggestions = []
                        st.session_state.star_rating = 0
                        st.session_state.transport_choice = None
                        st.rerun()
                else: st.success(T["finish_msg"])

    with col_stats:
        st.subheader("⚙️")
        if st.button(T["reset_btn"]):
            st.session_state.clear()
            st.rerun()
