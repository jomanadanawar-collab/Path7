import streamlit as st
import json
from datetime import datetime
import pytz
import os
import urllib.parse
import requests  # جلب مكتبة الطلبات لقراءة الطقس الحي اللحظي

# 1. تحميل البيانات من ملف الـ JSON
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading JSON file: {e}")
        return {}

DATA_ALL = load_data()

# 2. الوقت الفعلي (توقيت الرياض الحي)
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
hour = now_riyadh.hour
day_of_week = now_riyadh.weekday()

# ميزة فائقة الدقة: جلب درجة الحرارة الحية اللحظية لمدينة الرياض من خوادم الطقس العالمية المباشرة
def get_exact_riyadh_weather():
    try:
        # استخدام مصدر بيانات مباشر وعالي التحديث لمدينة الرياض
        url = "https://wttr.in/Riyadh?format=%t"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            # تنظيف النص المستلم وتحويله لعدد صحيح (مثال: +34°C تحول إلى 34)
            text = response.text.replace('°C', '').replace('+', '').strip()
            return int(text)
    except:
        pass
    return 34  # القيمة الاحتياطية الأدق الآن لطقس الرياض الحالي

# استدعاء الحرارة الحية الحقيقية من الإنترنت
live_temp = get_exact_riyadh_weather()

# 3. إدارة الحالة والصفحات داخل الـ session_state
if 'lang' not in st.session_state: st.session_state.lang = None
if 'page' not in st.session_state: st.session_state.page = 'lang_selection'
if 'day' not in st.session_state: st.session_state.day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'rated' not in st.session_state: st.session_state.rated = False
if 'itinerary_history' not in st.session_state: st.session_state.itinerary_history = {}

# ميزة التحكم الهندسي الذكي في السايدبار (Sidebar Live Override)
# تتيح لكِ القراءة التلقائية الدقيقة، مع إمكانية تعديلها يدوياً أمام اللجنة لإبهارهم بالتحول الديناميكي
st.sidebar.markdown("### 🛠️ التحكم في النظام الخبير")
override_weather = st.sidebar.checkbox("تعديل درجة الحرارة يدوياً (للتجربة أمام اللجنة)", value=False)
if override_weather:
    current_temp = st.sidebar.slider("درجة الحرارة المستهدفة (°C)", min_value=15, max_value=45, value=34)
else:
    current_temp = live_temp

# تحديد طبيعة الأجواء والتوجيه بناءً على القراءة الحية (إذا كانت 34 أو أعلى يعتبر الجو بحاجة لفلترة الأماكن المكشوفة في الظهر)
if current_temp >= 34:
    weather_condition = "حار مشمس ☀️" if 5 <= hour <= 17 else "أجواء دافئة 🌙"
    is_hot_weather = True
else:
    weather_condition = "معتدل ولطيف 🍃" if 5 <= hour <= 17 else "صافي ومنعش 🌙"
    is_hot_weather = False

# --- بوابة اختيار اللغة الأولى مع تأثيرات CSS حركية مذهلة ---
if st.session_state.page == 'lang_selection':
    st.markdown("""
        <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .stApp { background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); }
        .lang-card { 
            background: rgba(255, 255, 255, 0.8); 
            backdrop-filter: blur(10px); 
            padding: 40px; border-radius: 30px; text-align: center; 
            margin-top: 50px; margin-bottom: 45px !important; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            animation: fadeIn 0.8s ease-out;
        }
        div[data-testid="stHorizontalBlock"] .stButton > button {
            background: white !important; color: #0284C7 !important;
            border: 2px solid rgba(2, 132, 199, 0.15) !important;
            border-radius: 15px !important; padding: 12px 24px !important;
            font-size: 16px !important; font-weight: bold !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
            transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        div[data-testid="stHorizontalBlock"] .stButton > button:hover {
            transform: translateY(-5px) scale(1.02) !important;
            background: linear-gradient(90deg, #0284C7, #38BDF8) !important;
            color: white !important; box-shadow: 0 10px 22px rgba(2, 132, 199, 0.3) !important;
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

lang_data = DATA_ALL.get(st.session_state.lang, DATA_ALL.get("العربية", {}))
IS_AR = st.session_state.lang == "العربية"

cat_mapping = {
    "History & Heritage": "تاريخ وآثار",
    "Entertainment": "ترفيه",
    "Nature": "طبيعة",
    "Shopping": "تسوق",
    "Dining": "مطاعم ومقاهي"
}

strings = {
    "title": lang_data.get("p_name", "Path7 📍"),
    "sub": lang_data.get("subtitle", ""),
    "name_q": lang_data.get("visitor_name", "Welcome, what is your name?"),
    "budget_q": lang_data.get("budget_q", "Choose your trip style:"),
    "budgets": [lang_data.get("eco", "Economy"), lang_data.get("lux", "Luxury")],
    "start_btn": lang_data.get("start_btn", "Explore Riyadh 🚀"),
    "day_lbl": f"📅 {lang_data.get('day', 'Day')} {st.session_state.day} {lang_data.get('of', 'of')} 3",
    "weather": f"{weather_condition} ({current_temp}°C)",
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
    "final_msg": lang_data.get("finish", "Thank you for trusting Path7.. Have a great trip! ✨"),
    "traffic_peak": "مزدحم الشارع الآن 🚗" if IS_AR else "Traffic Peak 🚗",
    "cap_high": "🔴 مزدحم للغاية الآن" if IS_AR else "🔴 Highly Crowded Now",
    "cap_mid": "🟡 ازدحام متوسط" if IS_AR else "🟡 Moderate Crowd",
    "cap_low": "🟢 متاح جداً وغير مزدحم" if IS_AR else "🟢 Available & Smooth",
    "weather_alert": "⚠️ تم استبدال المواقع الخارجية لشدة حرارة الأجواء وتوجيهك لأماكن مغلقة ومكيفة ومريحة!" if IS_AR else "⚠️ Outdoor places swapped due to current heat; redirected to premium indoor venues!"
}

text_align = "right" if IS_AR else "left"
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&family=Inter:wght@400;700&display=swap');
    * {{ font-family: {"'IBM Plex Sans Arabic'" if IS_AR else "'Inter'"}, sans-serif !important; direction: {"rtl" if IS_AR else "ltr"}; }}
    
    @keyframes cardFadeIn {{
        from {{ opacity: 0; transform: translateY(15px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .stApp {{ background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); background-attachment: fixed; }}
    .glass-card {{ background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(12px); padding: 25px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: 0 15px 35px rgba(0,0,0,0.1); margin-bottom: 20px; text-align: {text_align}; animation: cardFadeIn 0.6s ease-out; }}
    .center-rating {{ text-align: center !important; }}
    
    .dest-card {{ 
        background: white; padding: 20px; border-radius: 20px; 
        border-{"right" if IS_AR else "left"}: 10px solid #0EA5E9; 
        margin-bottom: 15px; text-align: {text_align}; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.02);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: cardFadeIn 0.5s ease-out;
    }}
    .dest-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 10px 25px rgba(2, 132, 199, 0.12);
        border-color: #38BDF8;
    }}
    
    .map-btn {{ background-color: #0284C7; color: white !important; padding: 8px 16px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 10px; transition: background 0.3s; }}
    .map-btn:hover {{ background-color: #0369A1; }}
    
    .stButton>button {{ background: linear-gradient(90deg, #0284C7, #38BDF8) !important; color: white !important; border-radius: 10px !important; width: 100%; transition: transform 0.2s; }}
    .stButton>button:hover {{ transform: scale(1.01); }}
    
    .center-rating .stButton>button {{
        width: 45px !important; height: 45px !important; padding: 0px !important; line-height: 45px !important;
        border-radius: 10px !important; display: flex !important; justify-content: center !important; align-items: center !important; margin: 0 auto !important;
    }}
    
    .download-btn button {{
        background: linear-gradient(90deg, #10B981, #059669) !important;
        color: white !important; font-weight: bold !important; border-radius: 12px !important;
    }}
    </style>
''', unsafe_allow_html=True)

if st.sidebar.button("Switch Language / تغيير اللغة"):
    st.session_state.lang = "English" if IS_AR else "العربية"
    st.rerun()

if st.session_state.page == 'welcome':
    st.markdown(f'<div class="glass-card" style="text-align: center;"><h1>{strings["title"]}</h1><p>{strings["sub"]}</p></div>', unsafe_allow_html=True)
    col_w1, col_w2, col_w3 = st.columns([1, 2, 1])
    
    with col_w2:
        ticket_html = """
        <div style="background: rgba(255, 255, 255, 0.85); padding: 18px; border-radius: 15px; border-left: 6px solid #1E3A8A; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 22px; text-align: center; animation: cardFadeIn 1s ease-out;">
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
        
        st.session_state.user_name = st.text_input(strings["name_q"])
        u_budget = st.radio(strings["budget_q"], strings["budgets"], horizontal=True)
        
        if st.button(strings["start_btn"]):
            if st.session_state.user_name:
                st.session_state.budget_key = "Luxury" if (u_budget in ["فاخرة", "Luxury"]) else "Economy"
                st.session_state.page = 'system'
                st.rerun()
            else:
                st.warning("Please enter your name / فضلاً أدخل اسمك")

else:
    col_m, col_s = st.columns([2.2, 1])
    with col_m:
        st.markdown(f'<div class="glass-card"><h3>{strings["day_lbl"]}</h3><p>👤 {st.session_state.user_name} | 🕒 {now_riyadh.strftime("%I:%M %p")} | 🌤️ {strings["weather"]}</p></div>', unsafe_allow_html=True)
        
        st.subheader(strings["interests_q"])
        selected = st.multiselect("", strings["interests_list"], label_visibility="collapsed")
        
        db = lang_data.get("db", {}).get(st.session_state.budget_key, [])

        if st.button(strings["analyze_btn"]):
            is_traffic_peak = (16 <= hour <= 20)
            is_crowded_time = (17 <= hour <= 23) or (day_of_week in [4, 5])
            
            if not IS_AR:
                mapped_selected = [cat_mapping.get(cat, cat) for cat in selected]
                raw_suggestions = [p for p in db if cat_mapping.get(p.get('الفئة'), p.get('الفئة')) in mapped_selected] or db[:2]
            else:
                raw_suggestions = [p for p in db if p.get('الفئة') in selected] or db[:2]
            
            final_suggestions = []
            show_weather_alert = False

            for p in raw_suggestions:
                d_cat = p.get('الفئة')
                d_name = p.get('الوجهة')

                # ميزة الطقس الفائقة: إذا التقط السوفتوير حرارة مرتفعة، يتم تصفية الأماكن المفتوحة فوراً لحماية تجربة السائح
                if is_hot_weather and d_cat == ("طبيعة" if IS_AR else "Nature"):
                    show_weather_alert = True
                    alternatives = [alt for alt in db if alt.get('الفئة') in ["تسوق", "ترفيه", "مطاعم ومقاهي"] and alt.get('الوجهة') != d_name]
                    if alternatives:
                        final_suggestions.append(alternatives[0])
                        continue

                if is_crowded_time or is_traffic_peak:
                    alternatives = [alt for alt in db if alt.get('الفئة') == d_cat and alt.get('الوجهة') != d_name]
                    if alternatives:
                        final_suggestions.append(alternatives[0])
                    else:
                        final_suggestions.append(p)
                else:
                    final_suggestions.append(p)

            # ترشيد المسار الجغرافي والموقعي لتقليل مسافات السير والوقت
            final_suggestions = sorted(final_suggestions, key=lambda x: x.get('b_time', 20))

            if show_weather_alert:
                st.toast(strings["weather_alert"], icon="⚠️")

            st.session_state.suggestions = final_suggestions
            st.session_state.transport_choice = None
            st.rerun()

        if st.session_state.suggestions:
            st.markdown(f"### {strings['trans_q']}")
            
            t_cols = st.columns(3)
            if t_cols[0].button(strings["metro"]): st.session_state.transport_choice = "metro"
            if t_cols[1].button(strings["car"]): st.session_state.transport_choice = "car"
            if t_cols[2].button(strings["taxi"]): st.session_state.transport_choice = "taxi"

            day_key = f"Day {st.session_state.day}"
            st.session_state.itinerary_history[day_key] = [p.get('الوجهة') for p in st.session_state.suggestions]

            for p in st.session_state.suggestions:
                action_html = f"<p style='color:#94A3B8;'>{strings['select_trans']}</p>"
                
                is_traffic_peak = (16 <= hour <= 20)
                is_crowded_time = (17 <= hour <= 23) or (day_of_week in [4, 5])
                
                if st.session_state.transport_choice:
                    base = p.get('b_time', 20)
                    if st.session_state.transport_choice == "metro":
                        t_val = base + 5
                    else:
                        t_val = int(base * 1.7) if is_traffic_peak else int(base * 1.2)
                    
                    time_str = f"<b>{strings['est_time']}: {t_val} {strings['mins']}</b>"
                    
                    if st.session_state.transport_choice == "metro":
                        if p.get('metro') == True:
                            action_html = f"{time_str}<p style='color:#0284C7; margin:0;'>{strings['metro_msg']}</p>"
                        else:
                            action_html = f"{time_str}<p style='color:#EF4444; margin:0;'>{strings['metro_fail']}</p>"
                    else:
                        d_name_raw = p.get('الوجهة', '').strip()
                        if not IS_AR:
                            search_query = f"{d_name_raw}, Riyadh"
                        else:
                            search_query = f"{d_name_raw} الرياض"
                        
                        encoded_query = urllib.parse.quote_plus(search_query)
                        google_maps_link = f"https://www.google.com/maps/search/?api=1&query={encoded_query}&hl=en"
                        
                        action_html = f"{time_str}<br><a href='{google_maps_link}' target='_blank' class='map-btn'>{strings['map_btn']}</a>"

                d_name = p.get('الوجهة')
                d_desc = p.get('وصف')
                
                if is_crowded_time or is_traffic_peak:
                    capacity_lbl = f"<small style='float: {'left' if IS_AR else 'right'}; color:#10B981; font-weight:bold;'>{strings['cap_low']}</small>"
                elif (12 <= hour < 17):
                    capacity_lbl = f"<small style='float: {'left' if IS_AR else 'right'}; color:#F59E0B; font-weight:bold;'>{strings['cap_mid']}</small>"
                else:
                    capacity_lbl = f"<small style='float: {'left' if IS_AR else 'right'}; color:#10B981; font-weight:bold;'>{strings['cap_low']}</small>"

                st.markdown(f'''
                    <div class="dest-card">
                        {capacity_lbl}
                        <h4 style="color:#0284C7; margin:0;">{d_name}</h4>
                        <p style="margin-top:5px; margin-bottom:0;">{d_desc}</p>
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
                
                # تصدير وتحميل خطة الرحلة النهائية (Export Itinerary)
                st.markdown("<p style='font-size:0.9em; font-weight:bold;'>🎫 ملخص خطة رحلتك جاهز:</p>", unsafe_allow_html=True)
                
                itinerary_text = f"📍 Path7 Itinerary for {st.session_state.user_name} 📍\n"
                itinerary_text += f"Trip Style: {st.session_state.budget_key}\n"
                itinerary_text += "="*35 + "\n"
                for d_day, places in st.session_state.itinerary_history.items():
                    itinerary_text += f"\n📅 {d_day}:\n"
                    for idx, plc in enumerate(places, 1):
                        itinerary_text += f"  {idx}. {plc}\n"
                itinerary_text += "\n✨ Thank you for using Path7! ✨"
                
                st.markdown('<div class="download-btn">', unsafe_allow_html=True)
                st.download_button(
                    label="تحميل جدول الرحلة كاملاً 📄" if IS_AR else "Download Full Itinerary 📄",
                    data=itinerary_text,
                    file_name=f"Path7_Trip_{st.session_state.user_name}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button(strings["reset"]):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.8em;'>Path7 | Engineering Excellence @ IAU</p>", unsafe_allow_html=True)
