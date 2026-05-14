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

# 2. إدارة الحالة (بداية بصفحة اللغة)
if 'page' not in st.session_state: st.session_state.page = 'lang_selection'
if 'lang' not in st.session_state: st.session_state.lang = None
if 'day' not in st.session_state: st.session_state.day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'rated' not in st.session_state: st.session_state.rated = False

IS_AR = st.session_state.lang == "العربية"

# 3. قاموس الترجمة (تأكدي من مطابقة الكلمات لملف الـ JSON عندك)
translation_dict = {
    "تاريخ وآثار": "History & Heritage", "ترفيه": "Entertainment", 
    "طبيعة": "Nature", "تسوق": "Shopping", "مطاعم ومقاهي": "Dining & Cafes",
    "فيا الرياض": "Via Riyadh", "فخامة السينما والمطاعم": "Luxury cinema and dining",
    "البوليفارد": "Boulevard", "روح الترفيه العالمية": "The spirit of global entertainment",
    "مطل البجيري": "Bujairi Terrace", "إطلالة ساحرة ومطاعم فاخرة": "Stunning views and luxury dining",
    "واجهة روشن": "ROSHN Front", "تسوق ومطاعم مفتوحة": "Open-air shopping and dining",
    "أسواق المعيقلية": "Al-Mu'aiqiliyah Markets", "بخور وعطور أصيلة": "Authentic incense and perfumes",
    "سوق الزل": "Souq Al-Zal", "تاريخ وتحف نادرة": "History and rare antiques"
}
rev_trans = {v: k for k, v in translation_dict.items()}

# نصوص الواجهة
strings = {
    "welcome": "Welcome to Path7" if not IS_AR else "مرحباً بك في Path7",
    "select_l": "Choose your language / اختر لغتك" if st.session_state.lang is None else "",
    "name_q": "What is your name?" if not IS_AR else "ما هو اسمك؟",
    "budget_q": "Trip Style:" if not IS_AR else "طابع الرحلة:",
    "budgets": ["Economy", "Luxury"] if not IS_AR else ["اقتصادية", "فاخرة"],
    "start_btn": "Start Journey 🚀" if not IS_AR else "ابدأ الرحلة 🚀",
    "day_lbl": f"📅 Day {st.session_state.day}" if not IS_AR else f"📅 يوم {st.session_state.day}",
    "interests_q": "Your Interests:" if not IS_AR else "اهتماماتك:",
    "interests_list": list(translation_dict.values()) if not IS_AR else list(translation_dict.keys()),
    "analyze_btn": "Analyze Path 🔍" if not IS_AR else "تحليل المسار 🔍",
    "trans_q": "Transport:" if not IS_AR else "وسيلة النقل:",
    "map_btn": "📍 Open Maps" if not IS_AR else "📍 فتح في الخرائط",
    "est_time": "Est. Time:" if not IS_AR else "الوقت المقدر:",
    "mins": "mins" if not IS_AR else "دقيقة"
}

# 4. التنسيق (أزرار مربعة 1:1 + الشكل القديم)
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    * {{ font-family: 'IBM Plex Sans Arabic', sans-serif !important; direction: {"rtl" if IS_AR else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); }}
    .glass-card {{ background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); padding: 20px; border-radius: 20px; margin-bottom: 20px; }}
    .dest-card {{ background: white; padding: 20px; border-radius: 20px; margin-bottom: 5px; color: black; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
    
    /* إجبار أزرار النجوم على المربع تماماً */
    [data-testid="stHorizontalBlock"] button[key^="s"] {{
        width: 60px !important; height: 60px !important; 
        aspect-ratio: 1/1 !important; border-radius: 12px !important;
        background-color: #0284C7 !important; color: white !important;
    }}
    .stButton>button {{ background: #0284C7 !important; color: white !important; border-radius: 10px !important; }}
    </style>
''', unsafe_allow_html=True)

# --- نظام الصفحات ---

# صفحة 1: اختيار اللغة
if st.session_state.page == 'lang_selection':
    st.markdown('<div class="glass-card" style="text-align:center;"><h1>Path7 📍</h1><h3>Choose Language / اختر اللغة</h3></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("English 🇬🇧"): 
        st.session_state.lang = "English"; st.session_state.page = 'welcome'; st.rerun()
    if c2.button("العربية 🇸🇦"): 
        st.session_state.lang = "العربية"; st.session_state.page = 'welcome'; st.rerun()

# صفحة 2: الترحيب والبيانات
elif st.session_state.page == 'welcome':
    st.markdown(f'<div class="glass-card" style="text-align:center;"><h1>{strings["welcome"]}</h1></div>', unsafe_allow_html=True)
    st.session_state.user_name = st.text_input(strings["name_q"])
    u_budget = st.radio(strings["budget_q"], strings["budgets"], horizontal=True)
    if st.button(strings["start_btn"]):
        st.session_state.budget_key = "Luxury" if (u_budget in ["Luxury", "فاخرة"]) else "Economy"
        st.session_state.page = 'main'; st.rerun()

# صفحة 3: النظام الرئيسي
else:
    col_m, col_s = st.columns([2.2, 1.2])
    with col_m:
        st.markdown(f'<div class="glass-card"><h3>{strings["day_lbl"]}</h3><p>👤 {st.session_state.user_name}</p></div>', unsafe_allow_html=True)
        selected = st.multiselect(strings["interests_q"], strings["interests_list"])
        
        if st.button(strings["analyze_btn"]):
            # البحث دائماً بالعربي في الخلفية لضمان النتائج من الـ JSON
            db = DATA_ALL.get("العربية", {}).get("db", {}).get(st.session_state.budget_key, [])
            search_terms = [rev_trans.get(i, i) for i in selected]
            st.session_state.suggestions = [p for p in db if p.get('الفئة') in search_terms] or db[:2]
            st.rerun()

        if st.session_state.suggestions:
            st.write(strings["trans_q"])
            t_cols = st.columns(3)
            if t_cols[0].button("🚇"): st.session_state.transport_choice = "metro"
            if t_cols[1].button("🚗"): st.session_state.transport_choice = "car"
            if t_cols[2].button("🚕"): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                # ترجمة الأسماء والأوصاف فوراً إذا اللغة إنجليزية
                d_name = translation_dict.get(p["الوجهة"], p["الوجهة"]) if not IS_AR else p["الوجهة"]
                d_desc = translation_dict.get(p["وصف"], p["وصف"]) if not IS_AR else p["وصف"]
                
                st.markdown(f'<div class="dest-card"><h3>{d_name}</h3><p>{d_desc}</p></div>', unsafe_allow_html=True)
                
                # الشكل القديم: الوقت والخرائط تحت البطاقة
                if st.session_state.transport_choice:
                    st.markdown(f"<p style='color:#555;'>{strings['est_time']} {p.get('b_time', 20)} {strings['mins']}</p>", unsafe_allow_html=True)
                    st.link_button(strings["map_btn"], f"http://googleusercontent.com/maps.google.com/4{d_name}")
                st.markdown("<br>", unsafe_allow_html=True)

    with col_s:
        # أزرار التقييم المربعة
        st.markdown(f'<div class="glass-card"><h4>Rate ⭐</h4>', unsafe_allow_html=True)
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}", key=f"s{i}"): st.session_state.rated = True
        
        if st.session_state.rated and st.button("Next Day"):
            st.session_state.day += 1; st.session_state.rated = False; st.rerun()
        
        if st.button("Reset 🔄"): st.session_state.clear(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
