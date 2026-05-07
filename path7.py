import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)

st.set_page_config(page_title="Path7 | Smart Journey", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS) - الهوية البصرية لـ Path7
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right; color: #2D3748 !important;
    }
    .stApp { background-color: #F8F9FB !important; }
    
    /* البوكس الكحلي الترحيبي */
    [data-testid="stForm"] {
        background: white !important; padding: 40px !important; border-radius: 25px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08) !important; border-top: 12px solid #1A365D !important;
        max-width: 750px; margin: auto;
    }
    
    /* كروت النتائج */
    .result-card {
        background: white; padding: 25px; border-radius: 15px;
        border-right: 8px solid #1A365D; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    .transport-box {
        background: #F1F5F9; padding: 15px; border-radius: 12px;
        border: 1px dashed #1A365D; margin-top: 10px;
    }

    .update-box {
        background: #FFF9C4; padding: 20px; border-radius: 15px;
        border: 2px dashed #FBC02D; margin-bottom: 20px; text-align: center;
    }

    /* إخفاء القوائم الجانبية تماماً */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    
    .stButton>button { border-radius: 10px; font-weight: bold; }
    </style>
''', unsafe_allow_html=True)

# 3. إدارة الحالة (Session State)
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'user_hotel' not in st.session_state: st.session_state.user_hotel = None
if 'dest_result' not in st.session_state: st.session_state.dest_result = None
if 'traffic_val' not in st.session_state: st.session_state.traffic_val = 0
if 'status_msg' not in st.session_state: st.session_state.status_msg = ""
if 'star_rating' not in st.session_state: st.session_state.star_rating = 0
if 'is_day_two' not in st.session_state: st.session_state.is_day_two = False

# --- المشهد الأول: البوكس الكحلي الترحيبي مع تثبيت الفندق ---
if st.session_state.page == 'welcome':
    col_l, col_m, col_r = st.columns([1, 6, 1])
    with col_m:
        with st.form("gate_form"):
            st.markdown('<h1 style="color: #1A365D; text-align: center; margin-bottom:0;">📍 Path7</h1>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; color: #718096;">نظام التوافق اللحظي للسياحة الذكية</p>', unsafe_allow_html=True)
            st.markdown('---')
            
            u_name = st.text_input("الاسم الكريم", "جُمانة")
            u_budget = st.radio("نوع الميزانية", ["اقتصادية (Low)", "فاخرة (High)"], horizontal=True)
            
            # فنادق حي المروج المقترحة
            hotels_db = {
                "اقتصادية (Low)": ["أجنحة المروج الفندقية", "بودل المروج"],
                "فاخرة (High)": ["فندق موفنبيك الرياض", "فندق دبل تري - كافد"]
            }
            
            u_hotel = st.selectbox("حددي مكان إقامتك (حي المروج):", hotels_db[u_budget])
            u_interest = st.selectbox("بماذا تهتمين اليوم؟", ["تاريخ", "ترفيه", "طبيعة"])
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("تثبيت البيانات وبدء الرحلة 🚀", use_container_width=True)
            
            if submit:
                st.session_state.user_name = u_name
                st.session_state.user_budget = u_budget
                st.session_state.user_hotel = u_hotel
                st.session_state.user_interest = u_interest
                st.session_state.page = 'system'
                st.rerun()

# --- المشهد الثاني: صفحة التوافق والنتائج اللحظية ---
else:
    col_main, col_stats = st.columns([2, 1])
    
    with col_main:
        # عرض الوقت الحالي والفندق المثبت
        st.markdown(f'''
            <div class="result-card">
                <h3 style="margin:0; color:#1A365D;">🕒 {now_riyadh.strftime("%I:%M %p")}</h3>
                <p style="margin-top:10px;">أهلاً <b>{st.session_state.user_name}</b>، مكان إقامتك المثبت هو: <b>🏨 {st.session_state.user_hotel}</b></p>
                <small>حي المروج | مربوط بمحطة مترو كافد</small>
            </div>
        ''', unsafe_allow_html=True)

        # منطق تحديث اليوم الثاني (ARE YOU STILL IN RIYADH?)
        if st.session_state.is_day_two:
            st.markdown(f'''
                <div class="update-box">
                    <h3 style="margin:0; color:#856404;">🔔 تحديث اليوم الجديد</h3>
                    <p>هاه يا جمانة، لسا جالتنا بالرياض ولا خلصت فترة إجازتك؟</p>
                </div>
            ''', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            if c1.button("لسا موجودة (تحديث المسار) ✨", use_container_width=True):
                st.session_state.is_day_two = False
                st.rerun()
            if c2.button("خلصت الإجازة (وداعاً) 👋", use_container_width=True):
                st.success("رحلة سعيدة، ننتظركِ مرة أخرى في الرياض! ✈️")
                st.stop()

        # زر توليد الوجهة (خوارزمية التوافق اللحظي)
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
                st.session_state.status_msg = f"⚠️ طريق ({first_choice}) مزدحم جداً ({first_traffic}%)؛ تم تحويلك للخيار الأنسب سالكاً."
            else:
                st.session_state.dest_result = first_choice
                st.session_state.traffic_val = first_traffic
                st.session_state.status_msg = "✅ المسار المختار من حي المروج سالك حالياً."

        if st.session_state.dest_result:
            if "⚠️" in st.session_state.status_msg: st.warning(st.session_state.status_msg)
            else: st.success(st.session_state.status_msg)
            
            st.info(f"📍 الوجهة المقترحة: {st.session_state.dest_result}")
            
            st.markdown("---")
            st.subheader(f"🚗 خيارات النقل من {st.session_state.user_hotel}")
            transport = st.selectbox("كيف تودين الذهاب؟", ["-- اختر وسيلة النقل --", "مترو الرياض (اقتصادي/سريع)", "تاكسي / أوبر", "سيارة خاصة"])
            
            if transport != "-- اختر وسيلة النقل --":
                base_m = 18 
                if "مترو" in transport:
                    t_time = base_m
                    msg = "🚇 خيار ذكي! المترو يربط حي المروج بكافة الوجهات دون التأثر بزحمة السير."
                elif "تاكسي" in transport:
                    t_time = base_m + (st.session_state.traffic_val // 5)
                    msg = "🚕 مريح، ولكن المدة تعتمد على حركة المرور في طريق الملك فهد."
                else:
                    t_time = base_m + (st.session_state.traffic_val // 4)
                    msg = "🚘 تأكد من حجز موقف في الوجهة قبل الانطلاق."
                
                st.markdown(f'''
                    <div class="transport-box">
                        <h3 style="margin:0; color:#1A365D;">الوصول خلال: {t_time} دقيقة</h3>
                        <p>{msg}</p>
                    </div>
                ''', unsafe_allow_html=True)

        st.markdown("---")
        # نظام التقييم بالنجوم
        st.subheader("⭐ تقييمك للنظام")
        star_cols = st.columns(5)
        for i in range(1, 6):
            with star_cols[i-1]:
                if st.button(f"{i} ⭐", key=f"s_{i}", use_container_width=True):
                    st.session_state.star_rating = i
        if st.session_state.star_rating > 0:
            st.markdown(f"<h1 style='text-align: center; color: #FFD700;'>{'⭐' * st.session_state.star_rating}</h1>", unsafe_allow_html=True)

    with col_stats:
        st.subheader("📊 مؤشرات")
        st.metric("الازدحام اللحظي", f"{st.session_state.traffic_val}%")
        st.metric("حالة الطقس", "28°C", "صافي")
        
        st.markdown("---")
        if st.button("⏩ محاكاة اليوم التالي (24h)"):
            st.session_state.is_day_two = True
            st.rerun()
            
        if st.button("🔄 تغيير الإعدادات"):
            st.session_state.page = 'welcome'
            st.rerun()

st.markdown("<br><p style='text-align: center; color: #A0AEC0; font-size: 0.8em;'>Path7 | IA University | Engineering Team</p>", unsafe_allow_html=True)
Final update for Path7
