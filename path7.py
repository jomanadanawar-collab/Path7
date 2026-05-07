import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)

st.set_page_config(page_title="Path7 | Smart Journey", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS)
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right; color: #2D3748 !important;
    }
    .stApp { background-color: #F8F9FB !important; }
    [data-testid="stForm"] {
        background: white !important; padding: 40px !important; border-radius: 25px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08) !important; border-top: 12px solid #1A365D !important;
        max-width: 750px; margin: auto;
    }
    .result-card {
        background: white; padding: 20px; border-radius: 15px;
        border-right: 8px solid #1A365D; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .hotel-feature {
        background: #EBF4FF; padding: 10px; border-radius: 8px; font-size: 0.9em; margin-top: 5px;
    }
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    </style>
''', unsafe_allow_html=True)

# 3. إدارة الحالة (Session State) لتخزين بيانات السكن
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'user_hotel' not in st.session_state: st.session_state.user_hotel = None
if 'dest_result' not in st.session_state: st.session_state.dest_result = None
if 'traffic_val' not in st.session_state: st.session_state.traffic_val = 0
if 'star_rating' not in st.session_state: st.session_state.star_rating = 0

# --- المشهد الأول: البوكس الترحيبي مع اختيار الفندق ---
if st.session_state.page == 'welcome':
    col_l, col_m, col_r = st.columns([1, 6, 1])
    with col_m:
        with st.form("travel_form"):
            st.markdown('<h1 style="color: #1A365D; text-align: center;">📍 Path7</h1>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; color: #718096;">حددي تفاصيل إقامتك لنقوم ببرمجة مسارك اللحظي</p>', unsafe_allow_html=True)
            st.markdown('---')
            
            u_name = st.text_input("الاسم", "جُمانة")
            
            # خيار الميزانية أولاً لتحديد قائمة الفنادق
            u_budget = st.radio("نوع الميزانية المتوقعة", ["اقتصادية (Low)", "فاخرة (High)"], horizontal=True)
            
            # قائمة الفنادق المقترحة بناءً على الميزانية في حي المروج
            if u_budget == "اقتصادية (Low)":
                hotels = {
                    "أجنحة المروج السكنية": "🌟 قريبة جداً من المترو، اقتصادية ونظيفة.",
                    "فندق بودل المروج": "🌟 موقع حيوي، سهولة الوصول لطريق الملك فهد."
                }
            else:
                hotels = {
                    "فندق موفنبيك الرياض": "💎 فخامة مطلقة، إطلالة على كافد، خدمات ملكية.",
                    "فندق دبل تري من هيلتون": "💎 عصري، مريح، ومثالي لرجال الأعمال والسياح."
                }
            
            selected_hotel = st.selectbox("اختار فندق إقامتك في حي المروج:", list(hotels.keys()))
            st.markdown(f'<div class="hotel-feature">{hotels[selected_hotel]}</div>', unsafe_allow_html=True)
            
            u_interest = st.selectbox("بماذا تهتمين اليوم؟", ["تاريخ", "ترفيه", "طبيعة"])
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("تثبيت البيانات وبدء الرحلة 🚀", use_container_width=True)
            
            if submit:
                st.session_state.user_name = u_name
                st.session_state.user_budget = u_budget
                st.session_state.user_hotel = selected_hotel
                st.session_state.user_interest = u_interest
                st.session_state.page = 'system'
                st.rerun()

# --- المشهد الثاني: لوحة التحكم (الفندق الآن مثبت) ---
else:
    h_l, h_r = st.columns([5, 1])
    with h_l: st.markdown(f"<h2>📍 مسارك الذكي: {st.session_state.user_name}</h2>", unsafe_allow_html=True)
    with h_r:
        if st.button("🔄 تغيير الفندق"):
            st.session_state.page = 'welcome'
            st.rerun()

    col_main, col_stats = st.columns([2, 1])
    
    with col_main:
        # عرض الفندق المثبت
        st.markdown(f'''
            <div class="result-card">
                <h4 style="margin:0; color:#1A365D;">مكان الإقامة المثبت:</h4>
                <p style="font-size: 1.2em; font-weight: bold; margin-bottom:2px;">🏨 {st.session_state.user_hotel}</p>
                <small>حي المروج | مربوط بمحطة مترو كافد</small>
            </div>
        ''', unsafe_allow_html=True)

        if st.button("تحليل الوجهة الأنسب بناءً على موقعي حالياً 🔍", use_container_width=True):
            data = {
                "تاريخ": {"Low": ["قصر المصمك", "مركز الملك عبدالعزيز"], "High": ["حي الطريف", "المتحف الوطني"]},
                "ترفيه": {"Low": ["حديقة السويدي", "ممشى الفريان"], "High": ["بوليفارد وورلد", "فيا رياض"]},
                "طبيعة": {"Low": ["وادي حنيفة", "منتزه السلام"], "High": ["منتجع نوفا", "الجهة الخفية"]}
            }
            b_key = "Low" if "اقتصادية" in st.session_state.user_budget else "High"
            
            first_choice = random.choice(data[st.session_state.user_interest][b_key])
            first_traffic = random.randint(10, 99)
            
            if first_traffic > 80:
                alternatives = [d for d in data[st.session_state.user_interest][b_key] if d != first_choice]
                st.session_state.dest_result = alternatives[0] if alternatives else first_choice
                st.session_state.traffic_val = random.randint(10, 45)
                st.session_state.status_msg = f"⚠️ طريق ({first_choice}) مزدحم؛ تم تعديل المسار تلقائياً."
            else:
                st.session_state.dest_result = first_choice
                st.session_state.traffic_val = first_traffic
                st.session_state.status_msg = "✅ المسار من فندقك إلى الوجهة سالك حالياً."

        if st.session_state.dest_result:
            st.info(f"📍 الوجهة المقترحة: {st.session_state.dest_result}")
            
            st.markdown("---")
            st.subheader(f"🚗 خيارات النقل من {st.session_state.user_hotel}")
            transport = st.selectbox("وسيلة النقل:", ["-- اختر --", "مترو الرياض", "تاكسي / أوبر", "سيارة خاصة"])
            
            if transport != "-- اختر --":
                base_m = 18 
                t_time = base_m if "مترو" in transport else base_m + (st.session_state.traffic_val // 5)
                msg = "🚇 المترو هو الأسرع من محطة كافد القريبة." if "مترو" in transport else "🚘 الطريق يتأثر بالزحمة اللحظية."
                
                st.markdown(f'''<div class="transport-box"><h4>الوصول خلال: {t_time} دقيقة</h4><p>{msg}</p></div>''', unsafe_allow_html=True)

    with col_stats:
        st.subheader("📊 مؤشرات")
        st.metric("الازدحام اللحظي", f"{st.session_state.traffic_val}%")
        st.metric("حالة الربط", "فندق مُثبت ✅")

st.markdown("<br><p style='text-align: center; color: #A0AEC0; font-size: 0.8em;'>Path7 | Engineering Project</p>", unsafe_allow_html=True)
