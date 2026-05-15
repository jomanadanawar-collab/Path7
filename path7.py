import streamlit as st
import json
from datetime import datetime
import pytz

# ==========================================
# 1. INITIALIZE SESSION STATE (ترتيب التهيئة يمنع خطأ NameError)
# ==========================================
if 'lang' not in st.session_state: st.session_state.lang = None
if 'page' not in st.session_state: st.session_state.page = 'lang_select'
if 'day' not in st.session_state: st.session_state.day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None
if 'rated' not in st.session_state: st.session_state.rated = False
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'budget_key' not in st.session_state: st.session_state.budget_key = "Economy"

# ==========================================
# 2. LOAD DATA DATABASE (قاعدة البيانات التفاعلية لمدينة الرياض)
# ==========================================
def load_data():
    try:
        with open('path7_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        # قاعدة بيانات احتياطية متكاملة لضمان عمل النظام بكفاءة في كل الظروف
        return {
            "العربية": {
                "db": {
                    "اقتصادية": [
                        {"الفئة": "طبيعة", "الوجهة": "وادي حنيفة", "وصف": "مسار بيئي ممتد وسط أشجار النخيل والبحيرات الجذابة ومناسب للمشي الاسترخائي.", "b_time": 20},
                        {"الفئة": "تاريخ وآثار", "الوجهة": "حي الطريف التاريخي", "وصف": "موقع تراثي عالمي مسجل في اليونسكو يروي تاريخ الدولة السعودية الأولى وبداياتها العريقة.", "b_time": 30},
                        {"الفئة": "تسوق", "الوجهة": "أسواق طيبة", "وصف": "تجربة تسوق شعبية أصيلة مفعمة بالحيوية والمنتجات المتنوعة بأسعار ممتازة تناسب الجميع.", "b_time": 25},
                        {"الفئة": "ترفيه", "الوجهة": "بوليفارد سيتي", "وصف": "الوجهة الترفيهية الأكبر والأكثر حيوية في الرياض مع فعاليات وألعاب خيالية وعروض حية.", "b_time": 15},
                        {"الفئة": "مطاعم ومقاهي", "الوجهة": "بيت الكبسة الشعبي", "وصف": "أطباق سعودية تقليدية لذيذة تعكس كرم الضيافة المحلية بأجواء تراثية دافئة.", "b_time": 20}
                    ],
                    "فاخرة": [
                        {"الفئة": "طبيعة", "الوجهة": "مطل حافة العالم", "وصف": "مغامرة فاخرة مع إطلالات شاهقة ساحرة على منحدرات طويق العريقة مع تنظيم راقٍ ومميز.", "b_time": 60},
                        {"الفئة": "تاريخ وآثار", "الوجهة": "قصر المربع الملكي", "وصف": "جولة ملكية تاريخية توثق نمط الحياة والقرارات السياسية العظيمة في عهد الملك عبدالعزيز.", "b_time": 35},
                        {"الفئة": "تسوق", "الوجهة": "مركز سنتريا مول", "وصف": "أرقى دور الأزياء العالمية والماركات الفاخرة الحصرية لتجربة تسوق استثنائية ونخبوية.", "b_time": 20},
                        {"الفئة": "ترفيه", "الوجهة": "فيا رياض (Via Riyadh)", "وصف": "منطقة فاخرة مصممة على الطراز السلماني وتضم أرقى صالات السينما والمطاعم العالمية.", "b_time": 15},
                        {"الفئة": "مطاعم ومقاهي", "الوجهة": "مطعم صم بلس ديزاين", "وصف": "تجربة عشاء فاخرة تجمع بين الأطباق العالمية المبتكرة والتصاميم الهندسية الراقية والمبهرة.", "b_time": 25}
                    ]
                }
            },
            "English": {
                "db": {
                    "Economy": [
                        {"الفئة": "Nature", "الوجهة": "Wadi Hanifa", "وصف": "An open natural valley featuring palm trees and scenic water streams, perfect for relaxation.", "b_time": 20},
                        {"الفئة": "History", "الوجهة": "At-Turaif District", "وصف": "A breathtaking UNESCO World Heritage site showcasing the beautiful mud-brick architecture of the first Saudi state.", "b_time": 30},
                        {"الفئة": "Shopping", "الوجهة": "Taiba Market", "وصف": "A traditional and vibrant local market filled with diverse cultural products at great prices.", "b_time": 25},
                        {"الفئة": "Entertainment", "الوجهة": "Boulevard City", "وصف": "The largest premium entertainment hub in Riyadh, offering incredible live shows and games.", "b_time": 15},
                        {"الفئة": "Dining", "الوجهة": "Al-Kabsa Traditional House", "وصف": "Authentic local flavors reflecting original Saudi hospitality in an elegant cultural setting.", "b_time": 20}
                    ],
                    "Luxury": [
                        {"الفئة": "Nature", "الوجهة": "Edge of the World", "وصف": "A luxurious guided desert excursion offering majestic views from the historic Tuwaiq cliffs.", "b_time": 60},
                        {"الفئة": "History", "الوجهة": "Al-Murabba Palace", "وصف": "A royal historic journey documenting the structural design and artifacts from King Abdulaziz's era.", "b_time": 35},
                        {"الفئة": "Shopping", "الوجهة": "Centria Mall", "وصف": "The ultimate high-end fashion destination hosting world-class luxury brands and boutiques.", "b_time": 20},
                        {"الفئة": "Entertainment", "الوجهة": "Via Riyadh", "وصف": "An exclusive elite zone featuring premium luxury cinemas and Michelin-starred restaurants.", "b_time": 15},
                        {"الفئة": "Dining", "الوجهة": "Someplace Else Design", "وصف": "A luxury fine-dining concept blending exceptional contemporary culinary art with architectural mastery.", "b_time": 25}
                    ]
                }
            }
        }

DATA_ALL = load_data()

# ==========================================
# 3. TIME & GLOBAL LOCALIZATION
# ==========================================
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)
hour = now_riyadh.hour

IS_AR = st.session_state.lang == "العربية"

# قواميس النصوص الديناميكية الموحدة بناءً على اختيار لغة المستخدم
strings = {
    "title": "Path7 📍",
    "sub": "نظام التوافق اللحظي للسياحة الذكية" if IS_AR else "Real-time Smart Tourism System",
    "name_q": "مرحباً بك، ما هو اسمك؟" if IS_AR else "Welcome, what is your name?",
    "budget_q": "حدد طابع رحلتك اليوم:" if IS_AR else "Choose your trip style:",
    "budgets": ["اقتصادية", "فاخرة"] if IS_AR else ["Economy", "Luxury"],
    "start_btn": "انطلق لاستكشاف الرياض 🚀" if IS_AR else "Explore Riyadh 🚀",
    "day_lbl": f"📅 يوم {st.session_state.day} من 3" if IS_AR else f"📅 Day {st.session_state.day} of 3",
    "weather": ("مشمس ☀️" if 5 <= hour <= 17 else "صافي 🌙") if IS_AR else ("Sunny ☀️" if 5 <= hour <= 17 else "Clear 🌙"),
    "interests_q": "ما هي اهتماماتك المفضلة اليوم؟" if IS_AR else "What are your interests today?",
    "interests_list": ["تاريخ وآثار", "ترفيه", "طبيعة", "تسوق", "مطاعم ومقاهي"] if IS_AR else ["History", "Entertainment", "Nature", "Shopping", "Dining"],
    "analyze_btn": "تحليل المسار الذكي 🔍" if IS_AR else "Smart Path Analysis 🔍",
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
    "reset": "إعادة ضبط 🔄" if IS_AR else "Reset 🔄",
    "final_msg": "شكرًا لثقتك بـ Path7.. نتمنى لك رحلة سعيدة في الرياض! ✨" if IS_AR else "Thank you for trusting Path7.. Have a great trip in Riyadh! ✨"
}

# ==========================================
# 4. ADVANCED VISUAL DESIGN (CSS واجهة هندسية فائقة الأناقة والنعومة)
# ==========================================
text_align = "right" if IS_AR else "left"
st.markdown(f'''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&family=Inter:wght@400;700&display=swap');
    
    * {{ 
        font-family: {"'IBM Plex Sans Arabic'" if IS_AR else "'Inter'"}, sans-serif !important; 
        direction: {"rtl" if IS_AR else "ltr"}; 
    }}
    
    .stApp {{ 
        background: linear-gradient(135deg, #0284C7 0%, #E0F2FE 100%); 
        background-attachment: fixed; 
    }}
    
    /* تصميم الكروت الزجاجية العامة للموقع */
    .glass-card {{ 
        background: rgba(255, 255, 255, 0.75); 
        backdrop-filter: blur(12px); 
        padding: 25px; 
        border-radius: 25px; 
        border: 1px solid rgba(255, 255, 255, 0.3); 
        box-shadow: 0 15px 35px rgba(0,0,0,0.1); 
        margin-bottom: 25px !important; 
        text-align: {text_align}; 
    }}
    
    /* كرت صفحة اللغة المطور بتباعد مدروس لمنع الالتصاق نهائياً */
    .lang-card {{ 
        background: rgba(255, 255, 255, 0.75); 
        backdrop-filter: blur(12px); 
        padding: 40px 25px; 
        border-radius: 25px; 
        border: 1px solid rgba(255, 255, 255, 0.3); 
        box-shadow: 0 15px 35px rgba(0,0,0,0.1); 
        margin-bottom: 50px !important; /* مسافة هندسية كافية تفصل اللوحة عن الأزرار بالأسفل */
        text-align: center; 
    }}
    
    .center-rating {{ text-align: center !important; }}
    
    .dest-card {{ 
        background: white; 
        padding: 20px; 
        border-radius: 20px; 
        border-{"right" if IS_AR else "left"}: 10px solid #0EA5E9; 
        margin-bottom: 15px; 
        text-align: {text_align}; 
    }}
    
    .map-btn {{ 
        background-color: #0284C7; 
        color: white !important; 
        padding: 8px 16px; 
        border-radius: 10px; 
        text-decoration: none; 
        font-weight: bold; 
        display: inline-block; 
        margin-top: 10px; 
    }}
    
    /* تصميم الأزرار العامة للموقع */
    .stButton>button {{ 
        background: linear-gradient(90deg, #0284C7, #38BDF8) !important; 
        color: white !important; 
        border-radius: 10px !important; 
        width: 100%; 
        font-weight: bold;
    }}
    
    /* 🔥 تصميم وأنيميشن أزرار اختيار اللغة الفخم والسلس للغاية 🔥 */
    .lang-marker + div[data-testid="stHorizontalBlock"] .stButton > button {{
        background: white !important;
        color: #0284C7 !important;
        border: 2px solid rgba(2, 132, 199, 0.2) !important;
        border-radius: 14px !important;
        padding: 14px 28px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06) !important;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important; /* حركة انتقالية انسيابية */
    }}
    
    .lang-marker + div[data-testid="stHorizontalBlock"] .stButton > button:hover {{
        transform: translateY(-5px) scale(1.02) !important; /* تأثير ارتفاع ناعم وتكبير مايكرو عند التحويم */
        background: linear-gradient(90deg, #0284C7, #38BDF8) !important;
        color: white !important;
        box-shadow: 0 12px 25px rgba(2, 132, 199, 0.35) !important;
        border-color: transparent !important;
    }}

    /* 🔥 الحل الهندسي الذكي لظهور أزرار النجوم الخمسة كمربعات متناسقة تماماً 🔥 */
    .star-marker + div[data-testid="stHorizontalBlock"] .stButton > button {{
        width: 45px !important;
        height: 45px !important;
        min-width: 45px !important;
        max-width: 45px !important;
        padding: 0px !important;
        font-size: 15px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 12px !important;
        background: white !important;
        color: #0284C7 !important;
        border: 2px solid rgba(2, 132, 199, 0.15) !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    
    .star-marker + div[data-testid="stHorizontalBlock"] .stButton > button:hover {{
        transform: translateY(-4px) scale(1.08) !important;
        background: linear-gradient(90deg, #0284C7, #38BDF8) !important;
        color: white !important;
        box-shadow: 0 6px 18px rgba(2, 132, 199, 0.3) !important;
    }}
    </style>
''', unsafe_allow_html=True)

# ==========================================
# 5. PAGES NAVIGATION LOGIC (منطق الملاحة والتنقل بين الصفحات)
# ==========================================

# --- الصفحة الأولى: اختيار لغة الواجهة الفورية ---
if st.session_state.page == 'lang_select':
    st.markdown('<div class="lang-card"><h1>Path7 📍</h1><h3>اختر اللغة / Select Your Language</h3></div>', unsafe_allow_html=True)
    
    # واسم CSS الموجه للتحكم الحصري بأزرار اللغة أدناه وتفعيل الأنميشن
    st.markdown('<div class="lang-marker"></div>', unsafe_allow_html=True)
    col_l1, col_l2 = st.columns(2)
    
    with col_l1:
        if st.button("SA العربية", key="btn_ar"):
            st.session_state.lang = "العربية"
            st.session_state.page = 'welcome'
            st.rerun()
    with col_l2:
        if st.button("English GB", key="btn_en"):
            st.session_state.lang = "English"
            st.session_state.page = 'welcome'
            st.rerun()

# --- الصفحة الثانية: الترحيب وجمع بيانات المستخدم بلسان اللغة المختارة ---
elif st.session_state.page == 'welcome':
    st.markdown(f'<div class="glass-card" style="text-align: center;"><h1>{strings["title"]}</h1><p>{strings["sub"]}</p></div>', unsafe_allow_html=True)
    col_w1, col_w2, col_w3 = st.columns([1, 2, 1])
    with col_w2:
        st.session_state.user_name = st.text_input(strings["name_q"], value=st.session_state.user_name)
        u_budget = st.radio(strings["budget_q"], strings["budgets"], horizontal=True)
        if st.button(strings["start_btn"]):
            if st.session_state.lang == "العربية":
                st.session_state.budget_key = "فاخرة" if u_budget == "فاخرة" else "اقتصادية"
            else:
                st.session_state.budget_key = "Luxury" if u_budget == "Luxury" else "Economy"
            st.session_state.page = 'system'
            st.rerun()

# --- الصفحة الثالثة: لوحة قيادة نظام السياحة الذكية المتوافق لحظياً ---
elif st.session_state.page == 'system':
    col_m, col_s = st.columns([2.2, 1])
    
    with col_m:
        st.markdown(f'<div class="glass-card"><h3>{strings["day_lbl"]}</h3><p>👤 {st.session_state.user_name} | 🕒 {now_riyadh.strftime("%I:%M %p")} | 🌤️ {strings["weather"]}</p></div>', unsafe_allow_html=True)
        
        st.subheader(strings["interests_q"])
        selected = st.multiselect("", strings["interests_list"], label_visibility="collapsed")
        
        if st.button(strings["analyze_btn"]):
            db = DATA_ALL.get(st.session_state.lang, {}).get("db", {}).get(st.session_state.budget_key, [])
            # تصفية ومطابقة الاهتمامات لحظياً بالاعتماد على اختيار المستخدم
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
                    time_str = f"<b>{strings['est_time']} {t_val} {strings['mins']}</b>"
                    if st.session_state.transport_choice == "metro":
                        action_html = f"{time_str}<p style='color:#0284C7;'>{strings['metro_msg']}</p>"
                    else:
                        action_html = f"{time_str}<br><a href='http://maps.google.com/?q={p['الوجهة']}' target='_blank' class='map-btn'>{strings['map_btn']}</a>"

                st.markdown(f'<div class="dest-card"><h4 style="color:#0284C7;margin:0;">{p["الوجهة"]}</h4><p>{p["وصف"]}</p>{action_html}</div>', unsafe_allow_html=True)

    with col_s:
        st.markdown(f'<div class="glass-card center-rating"><h4>{strings["rating_t"]}</h4>', unsafe_allow_html=True)
        
        # واسم CSS الموجه للتحكم الحصري بنماذج النجوم الخمسة وجعلها مربعة تفاعلية ومميزة
        st.markdown('<div class="star-marker"></div>', unsafe_allow_html=True)
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐", key=f"s{i}"): 
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
        
        st.markdown("<hr style='border: 0; border-top: 1px solid rgba(0,0,0,0.1); margin: 20px 0;'>", unsafe_allow_html=True)
        if st.button(strings["reset"]):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# الهوية الأكاديمية للمشروع الهندسي بجامعة الإمام عبدالرحمن بن فيصل
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.8em; margin-top: 35px;'>Path7 | Engineering Excellence @ IAU</p>", unsafe_allow_html=True)
