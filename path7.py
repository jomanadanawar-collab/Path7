import streamlit as st
import random
from datetime import datetime
import pytz 

# 1. إعدادات الوقت والصفحة
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)

st.set_page_config(page_title="Path7 | Smart Riyadh Guide", layout="wide", initial_sidebar_state="collapsed")

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
        max-width: 700px; margin: auto;
    }
    
    /* كروت النتائج */
    .result-card {
        background: white; padding: 20px; border-radius: 15px;
        border-right: 8px solid #1A365D; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    .transport-box {
        background: #F1F5F9; padding: 20px; border-radius: 12px;
        border: 1px dashed #1A365D; margin-top: 15px;
    }

    /* إخفاء القوائم الجانبية تماماً */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    
    /* تحسين أزرار النجوم */
    .stButton>button { border-radius: 10px; font-weight: bold; }
    </style>
''', unsafe_allow_html=True)

# 3. إدارة الحالة (Session State)
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'dest_result' not in st.session_state: st.session_state.dest_result = None
if 'traffic_val' not in st.session_state: st.session_state.traffic_val = 0
if 'status_msg' not in st.session_state: st.session_state.status_msg = ""
if 'star_rating' not in st.session_state: st.session_state.star_rating = 0

# --- المشهد الأول: البوكس الكحلي الترحيبي ---
if st.session_state.page == 'welcome':
    col_left, col_mid, col_right = st.columns([1, 5, 1])
    with col_mid:
        with st.form("gate_form"):
            st.markdown('<h1 style="color: #1A365D; text-align: center; margin-bottom:0;">📍 Path7</h1>', unsafe_allow_html=True)
            st.markdown('<p style="text-align: center; color: #718096;">دليلك الهندسي الذكي لاستكشاف الرياض</p>', unsafe_allow_html=True)
            st.markdown('---')
            
            u_name = st.text_input("الاسم", "جُمانة")
            u_interest = st.selectbox("بماذا تهتمين اليوم؟", ["تاريخ", "ترفيه", "طبيعة"])
            u_budget = st.radio("نوع الميزانية", ["اقتصادية (Low)", "فاخرة (High)"], horizontal=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("بدء تحليل المسار اللحظي 🚀", use_container_width=True)
            
            if submit:
                st.session_state.user_name = u_name
                st.session_state.user_interest = u_interest
                st.session_state.user_budget = u_budget
                st.session_state.page = 'system'
                st.session_state.dest_result = None
                st.rerun()

# --- المشهد الثاني: صفحة التوافق والنتائج اللحظية ---
else:
    h_left, h_right = st.columns([5, 1])
    with h_left: st.markdown(f"<h2>📍 لوحة التحليل: {st.session_state.user_name}</h2>", unsafe_allow_html=True)
    with h_right:
        if st.button("🔄 تعديل"):
            st.session_state.page = 'welcome'
            st.rerun()

    col_main, col_stats = st.columns([2, 1])
    
    with col_main:
        # تحديد نقطة الانطلاق في حي المروج
        starting_point = "حي المروج (بجوار محطة مترو كافد)"
        hotel_info = "فندق موفنبيك / شذا الرياض" if "فاخرة" in st.session_state.user_budget else "أجنحة فندقية عصرية"
        
        st.markdown(f'''
            <div class="result-card">
                <h4 style="margin:0; color:#1A365D;">نقطة الانطلاق (حي المروج):</h4>
                <p style="font-size: 1.1em; margin-bottom:5px;">🏨 {hotel_info}</p>
                <small>موقع استراتيجي يربطك بالمترو ويهرب من زحمة وسط المدينة.</small><br>
                <small>التوقيت اللحظي: {now_riyadh.strftime("%I:%M %p")}</small>
            </div>
        ''', unsafe_allow_html=True)

        if st.button("توليد الوجهة الأنسب حالياً 🔍", use_container_width=True):
            data = {
                "تاريخ": {"Low": ["قصر المصمك", "مركز الملك عبدالعزيز"], "High": ["حي الطريف", "المتحف الوطني"]},
                "ترفيه": {"Low": ["حديقة السويدي", "ممشى الفريان"], "High": ["بوليفارد وورلد", "فيا رياض"]},
                "طبيعة": {"Low": ["وادي حنيفة", "منتزه السلام"], "High": ["منتجع نوفا", "الجهة الخفية"]}
            }
            b_key = "Low" if "اقتصادية" in st.session_state.user_budget else "High"
            
            # خوارزمية التوافق اللحظي
            first_choice = random.choice(data[st.session_state.user_interest][b_key])
            first_traffic = random.randint(10, 99)
            
            if first_traffic > 80:
                alternatives = [d for d in data[st.session_state.user_interest][b_key] if d != first_choice]
                st.session_state.dest_result = alternatives[0] if alternatives else first_choice
                st.session_state.traffic_val = random.randint(10, 45)
                st.session_state.status_msg = f"⚠️ الوجهة ({first_choice}) مزدحمة جداً ({first_traffic}%)؛ تم تفعيل التوافق اللحظي وتحويلك للخيار الأنسب."
            else:
                st.session_state.dest_result = first_choice
                st.session_state.traffic_val = first_traffic
                st.session_state.status_msg = "✅ المسار المختار سالك ومناسب للزيارة الآن."

        if st.session_state.dest_result:
            if "⚠️" in st.session_state.status_msg: st.warning(st.session_state.status_msg)
            else: st.success(st.session_state.status_msg)
            
            st.info(f"📍 الوجهة المقترحة: {st.session_state.dest_result}")
            
            st.markdown("---")
            st.subheader("🚗 تفاصيل النقل من حي المروج")
            transport = st.selectbox("اختر وسيلة النقل لمعرفة المدة:", ["-- اختر --", "مترو الرياض (محطة كافد)", "تاكسي / أوبر", "سيارة خاصة"])
            
            if transport != "-- اختر --":
                base_m = 18 
                if "مترو" in transport:
                    t_time = base_m
                    msg = "🚇 خيار ذكي! المترو يربط المروج بقلب الرياض دون التأثر بالزحمة."
                elif "تاكسي" in transport:
                    t_time = base_m + (st.session_state.traffic_val // 5)
                    msg = "🚕 مريح، المدة تعتمد على حركة السير في طريق العليا."
                else:
                    t_time = base_m + (st.session_state.traffic_val // 4)
                    msg = "🚘 طريق الملك فهد هو خيارك الأسرع حالياً."
                
                st.markdown(f'''
                    <div class="transport-box">
                        <h3 style="margin:0; color:#1A365D;">المدة المتوقعة: {t_time} دقيقة</h3>
                        <p>{msg}</p>
                    </div>
                ''', unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("⭐ التقييم")
        s_cols = st.columns(5)
        for i in range(1, 6):
            with s_cols[i-1]:
                if st.button(f"{i} ⭐", key=f"s_{i}", use_container_width=True):
                    st.session_state.star_rating = i
        if st.session_state.star_rating > 0:
            st.markdown(f"<h1 style='text-align: center; color: #FFD700;'>{'⭐' * st.session_state.star_rating}</h1>", unsafe_allow_html=True)

    with col_stats:
        st.subheader("📊 مؤشرات لحظية")
        st.metric("نسبة الازدحام", f"{st.session_state.traffic_val}%")
        st.metric("حالة الطقس", "27°C", "صافي")
        st.metric("التوافق", "نشط ✅")

st.markdown("<br><p style='text-align: center; color: #A0AEC0; font-size: 0.8em;'>Path7 | IA University | Engineering Team</p>", unsafe_allow_html=True)
