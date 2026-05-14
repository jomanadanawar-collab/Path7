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
if 'lang' not in st.session_state: st.session_state.lang = "English" # جعل الافتراضي إنجليزي بناءً على طلبك
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'day' not in st.session_state: st.session_state.day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'rated' not in st.session_state: st.session_state.rated = False

IS_AR = st.session_state.lang == "العربية"

# قاموس الترجمة الشامل للمحتوى والواجهة
translation_dict = {
    "تاريخ وآثار": "History & Heritage",
    "ترفيه": "Entertainment",
    "طبيعة": "Nature",
    "تسوق": "Shopping",
    "مطاعم ومقاهي": "Dining & Cafes",
    # أضيفي ترجمات أسماء الأماكن من ملف الـ JSON هنا
    "مطل البجيري": "Bujairi Terrace",
    "إطلالة ساحرة ومطاعم فاخرة": "Stunning views and luxury dining",
    "أسواق المعيقلية": "Al-Mu'aiqiliyah Markets",
    "بخور وعطور أصيلة": "Authentic incense and perfumes",
    "سوق الزل": "Souq Al-Zal",
    "تاريخ وتحف نادرة": "History and rare antiques",
    "واجهة روشن": "ROSHN Front",
    "تسوق ومطاعم مفتوحة": "Open-air shopping and dining"
}

rev_trans = {v: k for k, v in translation_dict.items()}

# نصوص الواجهة باللغتين
strings = {
    "title": "Path7 📍",
    "sub": "Real-time Smart Tourism System" if not IS_AR else "نظام التوافق اللحظي للسياحة الذكية",
    "name_q": "Welcome, what is your name?" if not IS_AR else "مرحباً بك، ما هو اسمك؟",
    "budget_q": "Choose your trip style:" if not IS_AR else "حدد طابع رحلتك اليوم:",
    "budgets": ["Economy", "Luxury"] if not IS_AR else ["اقتصادية", "فاخرة"],
    "start_btn": "Explore Riyadh 🚀" if not IS_AR else "انطلق لاستكشاف الرياض 🚀",
    "day_lbl": f"📅 Day {st.session_state.day} of 3" if not IS_AR else f"📅 يوم {st.session_state.day} من 3",
    "weather": ("Sunny ☀️" if 5 <= hour <= 17 else "Clear 🌙") if not IS_AR else ("مشمس ☀️" if 5 <= hour <= 17 else "صافي 🌙"),
    "interests_q": "What are your interests today?" if not IS_AR else "ما هي اهتماماتك المفضلة اليوم؟",
    "interests_list": list(translation_dict.values()) if not IS_AR else list(translation_dict.keys()),
    "analyze_btn": "Analyze Smart Path 🔍" if not IS_AR else "تحليل المسار الذكي 🔍",
    "trans_q": "Preferred Transport" if not IS_AR else "وسيلة النقل المفضلة",
    "metro": "🚇 Metro" if not IS_AR else "🚇 المترو",
    "car": "🚗 Car" if not IS_AR else "🚗 السيارة",
    "taxi": "🚕 Taxi" if not IS_AR else "🚕 التاكسي",
    "est_time": "Est. Time:" if not IS_AR else "الوقت المقدر:",
    "mins": "mins" if not IS_AR else "دقيقة",
    "map_btn": "📍 Open Maps" if not IS_AR else "📍 فتح في الخرائط",
    "metro_msg": "Metro station is nearby." if not IS_AR else "محطة المترو قريبة منك.",
    "select_trans": "⏳ Select transport to see path" if not IS_AR else "⏳ حدد وسيلة النقل لمعرفة المسار",
    "rating_t": "Rate your experience ⭐" if not IS_AR else "تقييمك للتجربة ⭐",
    "next_day": "Next Day ⏭️" if not IS_AR else "اليوم التالي ⏭️",
    "reset": "Reset 🔄" if not IS_AR else "إعادة ضبط 🔄",
    "final_msg": "Thank you for using Path7! ✨" if not IS_AR else "شكرًا لثقتك بـ Path7.. نتمنى لك رحلة سعيدة! ✨"
}

# 4. التنسيق البصري (أزرار مربعة ونظام إنجليزي)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if IS_AR else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); background-attachment: fixed; }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 25px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.3); margin-bottom: 20px; text-align: {"right" if IS_AR else "left"}; }}
    .dest-card {{ background: white; padding: 20px; border-radius: 20px; border-{"right" if IS_AR else "left"}: 10px solid #0EA5E9; margin-bottom: 15px; color: black; }}
    .map-btn {{ background-color: #0284C7; color: white !important; padding: 8px 16px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 10px; }}
    
    /* أزرار النجوم المربعة */
    div[data-testid="stHorizontalBlock"] button[key^="s"] {{
        width: 50px !important; height: 50px !important; border-radius: 8px !important;
        background-color: white !important; color: #0284C7 !important; border: 1px solid #E2E8F0 !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
    }}
    .stButton>button {{ background: linear-gradient(90deg, #0284C7, #38BDF8) !important; color: white !important; border-radius: 10px !important; width: 100%; }}
    </style>
''', unsafe_allow_html=True)

# زر تبديل اللغة (في الجانب)
if st.sidebar.button("Switch to العربية" if not IS_AR else "Switch to English"):
    st.session_state.lang = "العربية" if not IS_AR else "English"
    st.rerun()

# --- الصفحات ---
if st.session_state.page == 'welcome':
    st.markdown(f'<div class="glass-card" style="text-align: center;"><h1>{strings["title"]}</h1><p>{strings["sub"]}</p></div>', unsafe_allow_html=True)
    col_w1, col_w2, col_w3 = st.columns([1, 2, 1])
    with col_w2:
        st.session_state.user_name = st.text_input(strings["name_q"])
        u_budget = st.radio(strings["budget_q"], strings["budgets"], horizontal=True)
        if st.button(strings["start_btn"]):
            st.session_state.budget_key = "Luxury" if (u_budget in ["Luxury", "فاخرة"]) else "Economy"
            st.session_state.page = 'system'; st.rerun()

else:
    col_m, col_s = st.columns([2.2, 1.2])
    with col_m:
        st.markdown(f'<div class="glass-card"><h3>{strings["day_lbl"]}</h3><p>👤 {st.session_state.user_name} | 🕒 {now_riyadh.strftime("%I:%M %p")} | 🌤️ {strings["weather"]}</p></div>', unsafe_allow_html=True)
        
        selected = st.multiselect(strings["interests_q"], strings["interests_list"])
        
        if st.button(strings["analyze_btn"]):
            db = DATA_ALL.get("العربية", {}).get("db", {}).get(st.session_state.budget_key, [])
            search_terms = [rev_trans.get(i, i) for i in selected]
            st.session_state.suggestions = [p for p in db if p.get('الفئة') in search_terms] or db[:2]
            st.session_state.transport_choice = None; st.rerun()

        if st.session_state.suggestions:
            st.markdown(f"### {strings['trans_q']}")
            t_cols = st.columns(3)
            if t_cols[0].button(strings["metro"]): st.session_state.transport_choice = "metro"
            if t_cols[1].button(strings["car"]): st.session_state.transport_choice = "car"
            if t_cols[2].button(strings["taxi"]): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                # ترجمة المحتوى لحظياً
                display_name = translation_dict.get(p["الوجهة"], p["الوجهة"]) if not IS_AR else p["الوجهة"]
                display_desc = translation_dict.get(p["وصف"], p["وصف"]) if not IS_AR else p["وصف"]
                
                action_html = f"<p style='color:#94A3B8;'>{strings['select_trans']}</p>"
                if st.session_state.transport_choice:
                    base = p.get('b_time', 20)
                    t_val = base + 10 if st.session_state.transport_choice == "metro" else int(base * 1.4)
                    time_str = f"<b>{strings['est_time']} {t_val} {strings['mins']}</b>"
                    if st.session_state.transport_choice == "metro":
                        action_html = f"{time_str}<p style='color:#0284C7;'>{strings['metro_msg']}</p>"
                    else:
                        action_html = f"{time_str}<br><a href='https://www.google.com/maps/search/{p['الوجهة']}' target='_blank' class='map-btn'>{strings['map_btn']}</a>"

                st.markdown(f'<div class="dest-card"><h4>{display_name}</h4><p>{display_desc}</p>{action_html}</div>', unsafe_allow_html=True)

    with col_s:
        st.markdown(f'<div class="glass-card center-rating"><h4>{strings["rating_t"]}</h4>', unsafe_allow_html=True)
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐", key=f"s{i}"): st.session_state.rated = True
        
        if st.session_state.rated:
            if st.session_state.day < 3:
                if st.button(strings["next_day"]):
                    st.session_state.day += 1; st.session_state.suggestions = []; st.session_state.transport_choice = None; st.session_state.rated = False; st.rerun()
            else: st.success(strings["final_msg"])
        
        st.markdown("<hr style='opacity:0.2;'>", unsafe_allow_html=True)
        if st.button(strings["reset"]): st.session_state.clear(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.8em; margin-top: 20px;'>Path7 | Engineering Excellence @ IAU</p>", unsafe_allow_html=True)
