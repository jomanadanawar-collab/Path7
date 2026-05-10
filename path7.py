import streamlit as st
import random
from datetime import datetime
import pytz

# 1. إعدادات الوقت والصفحة (العرض الواسع عاد)
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)

st.set_page_config(page_title="Path7 | Smart Journey", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (لتجنب الأخطاء البرمجية)
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'current_day' not in st.session_state: st.session_state.current_day = 1
if 'suggestions' not in st.session_state: st.session_state.suggestions = []
if 'transport_choice' not in st.session_state: st.session_state.transport_choice = None

# 3. التنسيق الجمالي (النسخة السماوية الأصلية اللي حبيتيها)
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }

    .stApp { background-color: #F0F9FF !important; }

    /* صناديق العناوين والأسئلة البارزة */
    .highlight-box {
        background-color: #E0F2FE; 
        padding: 20px; border-radius: 18px;
        border-right: 10px solid #0EA5E9; 
        margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .main-card { 
        background: white; padding: 25px; border-radius: 25px; 
        border-top: 12px solid #0284C7; box-shadow: 0 10px 30px rgba(0,0,0,0.08); 
    }

    .info-box { 
        background: white; padding: 20px; border-radius: 20px; 
        border: 1px solid #BAE6FD; border-right: 8px solid #38BDF8; 
        margin-bottom: 15px; 
    }

    /* الأزرار السماوية */
    .stButton>button {
        background: linear-gradient(90deg, #0284C7 0%, #38BDF8 100%) !important;
        color: white !important; border: none !important;
        border-radius: 15px !important; height: 3.8em !important; 
        font-weight: bold !important; font-size: 1.1em !important;
        width: 100% !important;
    }
    
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
    </style>
''', unsafe_allow_html=True)

# 4. قاعدة البيانات (مباشرة من ملفك المحدث)
PLACES_DB = {
    "اقتصادية / متوسطة": [
        {"الوجهة": "أسواق المعيقلية", "الفئة": "تسوق", "وصف": "مركز تسوق تقليدي للبخور والعود والبشوت.", "base_time": 25, "metro": True},
        {"الوجهة": "حصن المصمك", "الفئة": "تاريخ وآثار", "وصف": "رمز توحيد المملكة وتأسيسها.", "base_time": 28, "metro": True},
        {"الوجهة": "سوق الزل", "الفئة": "تسوق", "وصف": "أقدم سوق مليء بالتاريخ والتحف النادرة.", "base_time": 27, "metro": True},
        {"الوجهة": "مركز الملك عبدالله المالي (KAFD)", "الفئة": "طبيعة", "وصف": "أعجوبة معمارية وأيقونة اقتصادية حديثة.", "base_time": 10, "metro": True},
        {"الوجهة": "واجهة روشن", "الفئة": "تسوق", "وصف": "ممشى مفتوح للتسوق والمطاعم العصرية.", "base_time": 22, "metro": False},
        {"الوجهة": "وادي حنيفة / نمار", "الفئة": "طبيعة", "وصف": "مساحات خضراء خلابة وبحيرات مثالية للنزهات.", "base_time": 35, "metro": False},
        {"الوجهة": "منتزه الملك عبد الله", "الفئة": "طبيعة", "وصف": "نافورات راقصة ومساحات خضراء شاسعة للعائلات.", "base_time": 30, "metro": False},
        {"الوجهة": "حافة العالم", "الفئة": "طبيعة", "وصف": "إطلالات منحدرة تخطف الأنفاس لعشاق الطبيعة.", "base_time": 90, "metro": False}
    ],
    "فاخرة": [
        {"الوجهة": "حي الطريف", "الفئة": "تاريخ وآثار", "وصف": "موقع اليونسكو وقلب التاريخ السعودي.", "base_time": 18, "metro": True},
        {"الوجهة": "فيا رياض", "الفئة": "ترفيه", "وصف": "عمارة سلمية مع مطاعم وسينما عالمية.", "base_time": 15, "metro": False},
        {"الوجهة": "بوليفارد سيتي", "الفئة": "ترفيه", "وصف": "أكبر منطقة في العاصمة للثقافات العالمية.", "base_time": 12, "metro": False},
        {"الوجهة": "مطل البجيري", "الفئة": "تاريخ وآثار", "وصف": "مطاعم راقية بإطلالات تاريخية ساحرة.", "base_time": 18, "metro": True}
    ]
}

# --- الصفحة الأولى: الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.form("main_welcome_form"):
        st.markdown('<h1 style="text-align: center; color: #0369A1; margin-bottom:0; font-size: 3.5em;">📍 Path7</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #64748B; margin-top:5px; font-size: 1.3em;">نظام التوافق اللحظي للسياحة الذكية</p>', unsafe_allow_html=True)
        st.markdown('<hr style="margin: 30px 0; opacity: 0.1;">', unsafe_allow_html=True)
        
        u_name = st.text_input("اسم السائح الموقر", value="") # الاسم فارغ تماماً
        u_budget = st.radio("حدد نوع الميزانية للرحلة", ["اقتصادية / متوسطة", "فاخرة"], horizontal=True)
        
        if st.form_submit_button("استكشف مسارك الآن 🚀"):
            st.session_state.user_name = u_name
            st.session_state.user_budget = u_budget
            st.session_state.page = 'system'
            st.rerun()

# --- الصفحة الثانية: لوحة التحكم ---
else:
    col_main, col_stats = st.columns([2, 1])
    with col_main:
        st.markdown(f'''
            <div class="main-card">
                <h3 style="margin:0; color: #0369A1;">📅 اليوم {st.session_state.current_day} من 3</h3>
                <p style="color: #475569;">مرحباً يا <b>{st.session_state.user_name}</b></p>
            </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f'''
            <div class="highlight-box">
                <h4 style="margin:0; color: #0369A1;">🌟 ما هي اهتماماتك المفضلة لليوم؟</h4>
            </div>
        ''', unsafe_allow_html=True)
        
        u_interests = st.multiselect("", ["تاريخ وآثار", "ترفيه", "تسوق", "مطاعم ومقاهي", "طبيعة"], label_visibility="collapsed")

        if st.button("تحليل الوجهات الأنسب لهذا اليوم 🔍"):
            if not u_interests:
                st.error("لطفاً، اختر اهتماماً واحداً على الأقل.")
            else:
                available = PLACES_DB[st.session_state.user_budget]
                final = [p for p in available if p['الفئة'] in u_interests] # منطق الفلترة المصلح
                st.session_state.suggestions = final
                st.session_state.transport_choice = None

        if st.session_state.suggestions:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f'''
                <div class="highlight-box">
                    <h4 style="margin:0; color: #0369A1;">🚕 كيف تفضل الوصول لوجهاتك اليوم؟</h4>
                </div>
            ''', unsafe_allow_html=True)
            
            # أزرار وسيلة النقل
            t_col1, t_col2, t_col3 = st.columns(3)
            # إخفاء المترو إذا كانت إحدى الوجهات لا تدعمه (الواقعية!)
            has_no_metro = any(not p['metro'] for p in st.session_state.suggestions)
            
            if not has_no_metro:
                if t_col1.button("🚇 مترو الرياض"): st.session_state.transport_choice = "metro"
            else:
                t_col1.markdown('<p style="text-align:center; color:#94A3B8; font-size:0.8em; margin-top:15px;">المترو غير متاح ❌</p>', unsafe_allow_html=True)
                
            if t_col2.button("🚗 سيارتي"): st.session_state.transport_choice = "car"
            if t_col3.button("🚕 تاكسي"): st.session_state.transport_choice = "taxi"

            for p in st.session_state.suggestions:
                st.markdown(f'''
                    <div class="info-box">
                        <h4 style="margin:0; color:#0284C7;">📍 {p['الوجهة']}</h4>
                        <p style="margin:2px 0; font-size:0.9em; color:#475569;">{p['وصف']}</p>
                        <p style="margin:10px 0 0 0; font-weight:bold; color:#0369A1;">⏱️ الوقت المقدر: {p['base_time']} دقيقة</p>
                    </div>
                ''', unsafe_allow_html=True)

    with col_stats:
        st.subheader("⚙️ النظام")
        if st.button("🔄 إعادة ضبط"):
            st.session_state.clear()
            st.rerun()

st.markdown("<br><p style='text-align: center; color: #94A3B8; font-size: 0.8em;'>Path7 | Engineering @ IAU</p>", unsafe_allow_html=True)
