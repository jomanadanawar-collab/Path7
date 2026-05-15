import streamlit as st
import json
from datetime import datetime
import pytz
import os

# 1. تحميل البيانات من ملف الـ JSON
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading JSON file: {e}")
        return {}

DATA_ALL = load_data()

# 2. التوافق اللحظي والوقت (توقيت الرياض)
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
hour = now_riyadh.hour

# 3. إدارة الحالة والصفحات (تعريف مبكر لمنع خطأ NameError)
if 'lang' not in st.session_state: st.session_state.lang = None
if 'page' not in st.session_state: st.session_state.page = 'lang_selection'
if 'day' not in st.session_state: st.session_state.day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'rated' not in st.session_state: st.session_state.rated = False

# قاموس ثابت لروابط الخرائط لضمان عملها للغتين العربية والإنجليزية
MAPS_REGISTRY = {
    "حي طريف التاريخي": "https://maps.app.goo.gl/csHoJWG4BMLkfRJW7?g_st=ipc",
    "at-turaif historic district": "https://maps.app.goo.gl/csHoJWG4BMLkfRJW7?g_st=ipc",
    "at-turaif": "https://maps.app.goo.gl/csHoJWG4BMLkfRJW7?g_st=ipc",
    
    "سوق المعيقلية": "https://maps.app.goo.gl/xy3hqb29ww3X3nkU9?g_st=ic",
    "al muaiqilia market": "https://maps.app.goo.gl/xy3hqb29ww3X3nkU9?g_st=ic",
    "al-muaiqilia": "https://maps.app.goo.gl/xy3hqb29ww3X3nkU9?g_st=ic",
    
    "قصر المصمك": "https://maps.app.goo.gl/FiaUHymd1jLTrN8AA?g_st=ic",
    "al masmak palace": "https://maps.app.goo.gl/FiaUHymd1jLTrN8AA?g_st=ic",
    "masmak fortress": "https://maps.app.goo.gl/FiaUHymd1jLTrN8AA?g_st=ic",
    
    "سوق الزل": "https://maps.app.goo.gl/QDoo5gevYDxsD5V79?g_st=iw",
    "souq al zal": "https://maps.app.goo.gl/QDoo5gevYDxsD5V79?g_st=iw",
    "al-zal market": "https://maps.app.goo.gl/QDoo5gevYDxsD5V79?g_st=iw",
    
    "ڤيا الرياض": "https://maps.app.goo.gl/yyM4HfYoa7nfYHSe7?g_st=ic",
    "via riyadh": "https://maps.app.goo.gl/yyM4HfYoa7nfYHSe7?g_st=ic",
    
    "البوليفارد": "https://maps.app.goo.gl/mPLomGHnZBAPQw1q7?g_st=ic",
    "boulevard": "https://maps.app.goo.gl/mPLomGHnZBAPQw1q7?g_st=ic",
    "the boulevard": "https://maps.app.goo.gl/mPLomGHnZBAPQw1q7?g_st=ic",
    
    "المالية": "https://maps.app.goo.gl/Cs45ckXh7AwqPqUJ8?g_st=ic",
    "financial district": "https://maps.app.goo.gl/Cs45ckXh7AwqPqUJ8?g_st=ic",
    "kafd": "https://maps.app.goo.gl/Cs45ckXh7AwqPqUJ8?g_st=ic",
    
    "واجهة روشن": "https://maps.app.goo.gl/81dz34BHHRamtSr27?g_st=ic",
    "roshn waterfront": "https://maps.app.goo.gl/81dz34BHHRamtSr27?g_st=ic",
    "roshn front": "https://maps.app.goo.gl/81dz34BHHRamtSr27?g_st=ic",
    
    "البجيري": "https://maps.app.goo.gl/mgGKsuyqhEK8ydrT8?g_st=ic",
    "bujairi terrace": "https://maps.app.goo.gl/mgGKsuyqhEK8ydrT8?g_st=ic",
    "al-bujairi": "https://maps.app.goo.gl/mgGKsuyqhEK8ydrT8?g_st=ic",
    
    "وادي حنيفة": "https://maps.app.goo.gl/6KhYZAnVumSQCVJb9?g_st=ic",
    "wadi hanifa": "https://maps.app.goo.gl/6KhYZAnVumSQCVJb9?g_st=ic",
    
    "منتزه الملك عبدالله": "https://maps.app.goo.gl/A3GArkz2aX5jD1Da8?g_st=ic",
    "king abdullah park": "https://maps.app.goo.gl/A3GArkz2aX5jD1Da8?g_st=ic",
    
    "حافة العالم": "https://maps.app.goo.gl/saiAr2PGJuqZXN8z5?g_st=ic",
    "edge of the world": "https://maps.app.goo.gl/saiAr2PGJuqZXN8z5?g_st=ic"
}

# --- بوابة اختيار اللغة الأولى ---
if st.session_state.page == 'lang_selection':
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); }
        
        .lang-card { 
            background: rgba(255, 255, 255, 0.8); 
            backdrop-filter: blur(10px); 
            padding: 40px; 
            border-radius: 30px; 
            text-align: center; 
            margin-top: 50px; 
            margin-bottom: 45px !important; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.1); 
        }
        
        div[data-testid="stHorizontalBlock"] .stButton > button {
            background: white !important;
            color: #0284C7 !important;
            border: 2px solid rgba(2, 132, 199, 0.15) !important;
            border-radius: 15px !important;
            padding: 12px 24px !important;
            font-size: 16px !important;
            font-weight: bold !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        
        div[data-testid="stHorizontalBlock"] .stButton > button:hover {
            transform: translateY(-5px) scale(1.02) !important;
            background: linear-gradient(90deg, #0284C7, #38BDF8) !important;
            color: white !important;
            box-shadow: 0 10px 22px rgba(2, 132, 199, 0.3) !important;
            border-color: transparent !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="lang-card"><h1>Path7 📍</h1><h3>Select Your Language / اختر اللغة</h3></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("English 🇬🇧", use_container_width=True):
            st.session_state.lang = "English"
            st.session_state.page = 'welcome'
            st.rerun()
    with col2:
        if st.button("العربية 🇸🇦", use_container_width=True):
            st.session_state.lang = "العربية"
            st.session_state.page = 'welcome'
            st.rerun()
    st.stop()

# جلب بيانات اللغة المحددة ديناميكياً من الـ JSON
lang_data = DATA_ALL.get(st.session_state.lang, DATA_ALL.get("العربية", {}))
IS_AR = st.session_state.lang == "العربية"

strings = {
    "title": lang_data.get("p_name", "Path7 📍"),
    "sub": lang_data.get("subtitle", ""),
    "name_q": lang_data.get("visitor_name", "Welcome, what is your name?"),
    "budget_q": lang_data.get("budget_q", "Choose your trip style:"),
    "budgets": [lang_data.get("eco", "Economy"), lang_data.get("lux", "Luxury")],
    "start_btn": lang_data.get("start_btn", "Explore Riyadh 🚀"),
    "day_lbl": f"📅 {lang_data.get('day', 'Day')} {st.session_state.day} {lang_data.get('of', 'of')} 3",
    "weather": (lang_data.get("sunny", "Sunny ☀️") if 5 <= hour <= 17 else lang_data.get("night", "Clear 🌙")),
    "interests_q": lang_data.get("interests_q", "What are your interests today?"),
    "interests_list": lang_data.get("interests_list", []),
    "analyze_btn": lang_data.get("analyze_btn", "Smart Path Analysis 🔍"),
    "trans_q": lang_data.get("transport_q", "Preferred Transport"),
    "metro": lang_data.get("m_btn", "🚇 Metro"),
    "car": lang_data.get("c_btn", "🚗 Car"),
    "taxi": lang_data.get("t_btn", "🚕 Taxi"),
    "est_time": lang_data.get("est_time", "Est. Time"),
    "mins": lang_data.get("min", "mins"),
    "map_btn": lang_data.get("map_btn", "📍 Open Maps"),
    "metro_msg": lang_data.get("metro_msg", "Metro station is nearby."),
    "metro_fail": lang_data.get("metro_fail", "No direct metro line to this destination."),
    "select_trans": lang_data.get("wait_choice", "⏳ Select transport to see path"),
    "rating_t": lang_data.get("rating_q", "Rate your experience ⭐"),
    "next_day": lang_data.get("next_day", "Next Day ⏭️"),
    "reset": "إعادة ضبط 🔄" if IS_AR else "Reset 🔄",
    "final_msg": lang_data.get("finish", "Thank you for trusting Path7.. Have a great trip! ✨")
}

# 4. التنسيق البصري العام للواجهة والأزرار والبطاقات
text_align = "right" if IS_AR else "left"
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&family=Inter:wght@400;700&display=swap');
    * {{ font-family: {"'IBM Plex Sans Arabic'" if IS_AR else "'Inter'"}, sans-serif !important; direction: {"rtl" if IS_AR else "ltr"}; }}
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); background-attachment: fixed; }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 25px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 15px 35px rgba(0,0,0,0.1); margin-bottom: 20px; text-align: {text_align}; }}
    .center-rating {{ text-align: center !important; }}
    .dest-card {{ background: white; padding: 20px; border-radius: 20px; border-{"right" if IS_AR else "left"}: 10px solid #0EA5E9; margin-bottom: 15px; text-align: {text_align}; }}
    .map-btn {{ background-color: #0284C7; color: white !important; padding: 8px 16px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 10px; }}
    
    /* تصميم الأزرار العامة */
    .stButton>button {{ background: linear-gradient(90deg, #0284C7, #38BDF8) !important; color: white !important; border-radius: 10px !important; width: 100%; }}
    
    /* أزرار الأرقام للتقييم */
    .center-rating .stButton>button {{
        width: 45px !important;
        height: 45px !important;
        padding: 0px !important;
        line-height: 45px !important;
        border-radius: 10px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 auto !important;
    }}
    </style>
''', unsafe_allow_html=True)

# زر الشريط الجانبي لتغيير اللغة
if st.sidebar.button("Switch Language / تغيير اللغة"):
    st.session_state.lang = "English" if IS_AR else "العربية"
    st.rerun()

# --- الصفحات ---
# أ. صفحة الترحيب وتأكيد تذكرة الطيران والثبات الرقمي
if st.session_state.page == 'welcome':
    st.markdown(f'<div class="glass-card" style="text-align: center;"><h1>{strings["title"]}</h1><p>{strings["sub"]}</p></div>', unsafe_allow_html=True)
    col_w1, col_w2, col_w3 = st.columns([1, 2, 1])
    
    with col_w2:
        ticket_html = """
        <div style="background: rgba(255, 255, 255, 0.85); padding: 18px; border-radius: 15px; border-left: 6px solid #1E3A8A; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 22px; text-align: center;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <span style="font-weight: bold; color: #1E3A8A; font-size: 0.95em;">✈️ الخطوط السعودية / SAUDIA</span>
                <span style="background: #E0F2FE; color: #0369A1; padding: 2px 10px; border-radius: 20px; font-size: 0.8em; font-weight: bold;">Tourist / سياحة</span>
            </div>
            <div style="margin: 12px 0;">
                <span style="color: #64748B; font-size: 0.85em; display: block; margin-bottom: 2px;">رقم الحجز المربوط / Linked PNR</span>
                <strong style="font-size: 1.3em; color: #0284C7; letter-spacing: 2px; font-family: 'Inter', sans-serif;">SV-RUH2026X</strong>
            </div>
            <div style="border-top: 1px dashed #CBD5E1; margin-top: 10px; padding-top: 8px; font-size: 0.8em; color: #64748B;">
                📍 Destination: Riyadh (RUH) | الوجهة: الرياض
            </div>
        </div>
        """
        st.markdown(ticket_html, unsafe_allow_html=True)
        
        # حقول إدخال البيانات المعتمدة للانطلاق
        st.session_state.user_name = st.text_input(strings["name_q"])
        u_budget = st.radio(strings["budget_q"], strings["budgets"], horizontal=True)
        
        if st.button(strings["start_btn"]):
            if st.session_state.user_name:
                st.session_state.budget_key = "Luxury" if (u_budget in ["فاخرة", "Luxury"]) else "Economy"
                st.session_state.page = 'system'
                st.rerun()
            else:
                st.warning("Please enter your name / فضلاً أدخل اسمك")

# ب. صفحة النظام والمسار السياحي الذكي
else:
    col_m, col_s = st.columns([2.2, 1])
    with col_m:
        st.markdown(f'<div class="glass-card"><h3>{strings["day_lbl"]}</h3><p>👤 {st.session_state.user_name} | 🕒 {now_riyadh.strftime("%I:%M %p")} | 🌤️ {strings["weather"]}</p></div>', unsafe_allow_html=True)
        
        st.subheader(strings["interests_q"])
        selected = st.multiselect("", strings["interests_list"], label_visibility="collapsed")
        
        if st.button(strings["analyze_btn"]):
            db = lang_data.get("db", {}).get(st.session_state.budget_key, [])
            st.session_state.suggestions = [p for p in db if p.get('الفئة') in selected] or db[:2]
            st.session_state.transport_choice = None
            st.rerun()

        if st.session_state.suggestions:
            st.markdown(f"### {strings['trans_q']}")
            t_cols = st.columns(3)
            if t_cols[0].button(strings["metro"]): st.session_state.transport_choice = "metro"
            if t_cols[1].button(strings["car"]): st.session_state.transport_choice = "car"
            if t_cols[2].button(strings["taxi"]): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                action_html = f"<p style='color:#94A3B8;'>{strings['select_trans']}</p>"
                if st.session_state.transport_choice:
                    base = p.get('b_time', 20)
                    t_val = base + 10 if st.session_state.transport_choice == "metro" else int(base * 1.4)
                    time_str = f"<b>{strings['est_time']}: {t_val} {strings['mins']}</b>"
                    
                    if st.session_state.transport_choice == "metro":
                        if p.get('metro') == True:
                            action_html = f"{time_str}<p style='color:#0284C7;'>{strings['metro_msg']}</p>"
                        else:
                            action_html = f"{time_str}<p style='color:#EF4444;'>{strings['metro_fail']}</p>"
                    else:
                        # جلب رابط الخريطة الصحيح للغتين بالاعتماد على الاسم الفعلي للوجهة
                        d_name_raw = p.get('الوجهة', '').strip()
                        d_name_lower = d_name_raw.lower()
                        
                        # الفحص والربط المباشر من القاموس
                        google_maps_link = p.get('map_url') or MAPS_REGISTRY.get(d_name_raw) or MAPS_REGISTRY.get(d_name_lower)
                        
                        # حماية إضافية في حال كتابة الاسم بأسلوب مختلف في الـ JSON
                        if not google_maps_link:
                            google_maps_link = f"https://www.google.com/maps/search/?api=1&query={d_name_raw}"
                        
                        action_html = f"{time_str}<br><a href='{google_maps_link}' target='_blank' class='map-btn'>{strings['map_btn']}</a>"

                d_name = p.get('الوجهة')
                d_desc = p.get('وصف')
                
                st.markdown(f'''
                    <div class="dest-card">
                        <h4 style="color:#0284C7;margin:0;">{d_name}</h4>
                        <p>{d_desc}</p>
                        {action_html}
                    </div>
                ''', unsafe_allow_html=True)
                
                if p.get('image') and os.path.exists(p['image']):
                    st.image(p['image'], use_container_width=True)

    with col_s:
        st.markdown(f'<div class="glass-card center-rating"><h4>{strings["rating_t"]}</h4>', unsafe_allow_html=True)
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}", key=f"s{i}"): 
                st.session_state.rated = True
        
        if st.session_state.rated:
            if st.session_state.day < 3:
                if st.button(strings["next_day"]):
                    st.session_state.day += 1
                    st.session_state.suggestions = []
                    st.session_state.transport_choice = None
                    st.session_state.rated = False
                    st.rerun()
            else:
                st.info(strings["final_msg"])
        
        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button(strings["reset"]):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.8em;'>Path7 | Engineering Excellence @ IAU</p>", unsafe_allow_html=True)
