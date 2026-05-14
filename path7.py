import streamlit as st
import json
from datetime import datetime
import pytz

# 1. تحميل البيانات
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

DATA_ALL = load_data()

# 2. التوافق اللحظي
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
hour = now_riyadh.hour

# 3. إدارة الحالة واللغة
if 'lang' not in st.session_state: st.session_state.lang = "العربية"
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'day' not in st.session_state: st.session_state.day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'rated' not in st.session_state: st.session_state.rated = False

IS_AR = st.session_state.lang == "العربية"

# خريطة ربط الاهتمامات لضمان ظهور النتائج باللغتين
interest_map = {
    "History": "تاريخ وآثار",
    "Entertainment": "ترفيه",
    "Nature": "طبيعة",
    "Shopping": "تسوق",
    "Dining": "مطاعم ومقاهي"
}

# قاموس نصوص الواجهة
strings = {
    "title": "Path7 | مسار 7 📍",
    "sub": "الذكاء الاصطناعي في خدمة سياحتك" if IS_AR else "AI at your tourism service",
    "name_q": "مرحباً بك، ما هو اسمك؟" if IS_AR else "Welcome, what is your name?",
    "budget_q": "حدد طابع رحلتك اليوم:" if IS_AR else "Choose your trip style:",
    "budgets": ["اقتصادية", "فاخرة"] if IS_AR else ["Economy", "Luxury"],
    "start_btn": "انطلق لاستكشاف الرياض 🚀" if IS_AR else "Explore Riyadh 🚀",
    "day_lbl": f"📅 يوم {st.session_state.day} من 3" if IS_AR else f"📅 Day {st.session_state.day} of 3",
    "weather": ("صافي 🌙" if hour >= 18 or hour < 5 else "مشمس ☀️") if IS_AR else ("Clear 🌙" if hour >= 18 or hour < 5 else "Sunny ☀️"),
    "interests_q": "ما هي اهتماماتك المفضلة اليوم؟" if IS_AR else "What are your interests today?",
    "interests_list": ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"] if IS_AR else ["History", "Entertainment", "Nature", "Shopping", "Dining"],
    "analyze_btn": "تحليل المسار الذكي 🔍" if IS_AR else "Analyze Smart Path 🔍",
    "trans_q": "وسيلة النقل المفضلة" if IS_AR else "Preferred Transport",
    "metro": "🚇 المترو" if IS_AR else "🚇 Metro",
    "car": "🚗 السيارة" if IS_AR else "🚗 Car",
    "taxi": "🚕 التاكسي" if IS_AR else "🚕 Taxi",
    "est_time": "الوقت المقدر:" if IS_AR else "Est. Time:",
    "mins": "دقيقة" if IS_AR else "mins",
    "map_btn": "📍 فتح في الخرائط" if IS_AR else "📍 Open Maps",
    "metro_msg": "محطة المترو قريبة منك." if IS_AR else "Metro station is nearby.",
    "select_trans": "⏳ حدد وسيلة النقل لمعرفة المسار" if IS_AR else "⏳ Select transport to see path",
    "rating_t": "تقييمك للتجربة ⭐" if IS_AR else "Rate your experience ⭐",
    "next_day": "اليوم التالي ⏭️" if IS_AR else "Next Day ⏭️",
    "reset": "Reset 🔄"
}

# 4. التنسيق (CSS) - استرجاع شكل الأزرار الأصلية
text_align = "right" if IS_AR else "left"
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if IS_AR else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); background-attachment: fixed; }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 25px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 15px 35px rgba(0,0,0,0.1); margin-bottom: 20px; text-align: center; }}
    .info-card {{ text-align: {text_align}; }}
    .dest-card {{ background: white; padding: 20px; border-radius: 20px; border-{"right" if IS_AR else "left"}: 12px solid #0EA5E9; margin-bottom: 15px; text-align: {text_align}; }}
    .map-btn {{ background-color: #0284C7; color: white !important; padding: 8px 16px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 10px; }}
    /* أزرار النجوم الأصلية */
    .stButton>button {{ 
        background: linear-gradient(180deg, #38BDF8 0%, #0284C7 100%) !important; 
        color: white !important; 
        border-radius: 12px !important; 
        border: none !important;
        box-shadow: 0 4px 10px rgba(2, 132, 199, 0.3);
    }}
    .stButton>button:hover {{ transform: translateY(-2px); }}
    </style>
''', unsafe_allow_html=True)

# زر اللغة
col_l1, col_l2 = st.columns([10, 2])
if col_l2.button("عربي/EN"):
    st.session_state.lang = "English" if IS_AR else "العربية"
    st.rerun()

# --- الصفحات ---
if st.session_state.page == 'welcome':
    st.markdown(f'''<div class="glass-card">
        <h1 style="color: #0369A1; font-size: 2.5em;">{strings["title"]}</h1>
        <p style="color: #64748B; font-size: 1.2em;">{strings["sub"]}</p>
    </div>''', unsafe_allow_html=True)
    
    col_w1, col_w2, col_w3 = st.columns([1, 2, 1])
    with col_w2:
        st.session_state.user_name = st.text_input(strings["name_q"], placeholder="أدخل اسمك هنا" if IS_AR else "Enter your name")
        u_budget = st.radio(strings["budget_q"], strings["budgets"], horizontal=True)
        if st.button(strings["start_btn"]):
            st.session_state.budget_key = "Luxury" if (u_budget in ["فاخرة", "Luxury"]) else "Economy"
            st.session_state.page = 'system'; st.rerun()

else:
    col_m, col_s = st.columns([2.2, 1])
    with col_m:
        st.markdown(f'''<div class="glass-card info-card">
            <h2 style="color:#0369A1;">{strings["day_lbl"]}</h2>
            <p>👤 {st.session_state.user_name} | 🕒 {now_riyadh.strftime("%I:%M %p")} | 🌤️ {strings["weather"]}</p>
        </div>''', unsafe_allow_html=True)
        
        st.subheader(strings["interests_q"])
        selected = st.multiselect("", strings["interests_list"], label_visibility="collapsed")
        
        if st.button(strings["analyze_btn"]):
            # جلب البيانات لضمان عدم حدوث Key-Error
            data_source = DATA_ALL.get("العربية", DATA_ALL.get("English", {}))
            db = data_source.get("db", {}).get(st.session_state.budget_key, [])
            
            # فلترة ذكية للاهتمامات باللغتين
            search_terms = [interest_map.get(i, i) for i in selected]
            if search_terms:
                st.session_state.suggestions = [p for p in db if p.get('الفئة') in search_terms]
            else:
                st.session_state.suggestions = db[:2]
            st.session_state.transport_choice = None; st.rerun()

        if st.session_state.suggestions:
            st.markdown(f"### {strings['trans_q']}")
            t_cols = st.columns(3)
            if t_cols[0].button(strings["metro"]): st.session_state.transport_choice = "metro"
            if t_cols[1].button(strings["car"]): st.session_state.transport_choice = "car"
            if t_cols[2].button(strings["taxi"]): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                # ترجمة الوصف لو اللغة إنجليزية (اختياري)
                action_html = f"<p style='color:#94A3B8;'>{strings['select_trans']}</p>"
                if st.session_state.transport_choice:
                    base = p.get('b_time', 20)
                    t_val = base + 10 if st.session_state.transport_choice == "metro" else int(base * 1.4)
                    action_html = f"<b>{strings['est_time']} {t_val} {strings['mins']}</b>"
                    if st.session_state.transport_choice == "metro":
                        action_html += f"<p style='color:#0284C7;'>{strings['metro_msg']}</p>"
                    else:
                        action_html += f"<br><a href='http://maps.google.com/?q={p['الوجهة']}' target='_blank' class='map-btn'>{strings['map_btn']}</a>"

                st.markdown(f'''<div class="dest-card">
                    <h4 style="color:#0284C7;margin:0;">{p["الوجهة"]}</h4>
                    <p style="color:#64748B;">{p["وصف"]}</p>
                    {action_html}
                </div>''', unsafe_allow_html=True)

    with col_s:
        st.markdown(f'<div class="glass-card"><h4>{strings["rating_t"]}</h4>', unsafe_allow_html=True)
        stars = st.columns(5)
        for i in range(5, 0, -1): # ترتيب النجوم كما في صورتك
            if stars[5-i].button(f"⭐{i}", key=f"star_{i}"): st.session_state.rated = True
        
        if st.session_state.rated:
            if st.session_state.day < 3:
                st.write("")
                if st.button(strings["next_day"]):
                    st.session_state.day += 1; st.session_state.suggestions = []; st.session_state.transport_choice = None; st.session_state.rated = False; st.rerun()
            else:
                st.success("Thank you! ✨" if not IS_AR else "شكرًا لك! ✨")
        
        st.markdown("<hr style='opacity:0.2;'>", unsafe_allow_html=True)
        if st.button(strings["reset"]): st.session_state.clear(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.8em;'>Path7 | Engineering Excellence @ IAU</p>", unsafe_allow_html=True)
