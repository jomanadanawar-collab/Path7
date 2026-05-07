import streamlit as st
import random
from datetime import datetime, timedelta
import pytz 

# 1. إعدادات الوقت
riyadh_tz = pytz.timezone('Asia/Riyadh')
now_riyadh = datetime.now(riyadh_tz)

st.set_page_config(page_title="Path7 | Smart Bot", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق (CSS)
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, span, label, input, button, select {
        font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        direction: rtl; text-align: right;
    }
    .stApp { background-color: #F8F9FB !important; }
    [data-testid="stForm"] {
        background: white !important; padding: 40px !important; border-radius: 25px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08) !important; border-top: 12px solid #1A365D !important;
    }
    .bot-msg {
        background: #E8EAF6; padding: 15px; border-radius: 15px 15px 0 15px;
        border-right: 5px solid #1A365D; margin-bottom: 10px;
    }
    </style>
''', unsafe_allow_html=True)

# 3. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'user_phone' not in st.session_state: st.session_state.user_phone = ""
if 'is_day_two' not in st.session_state: st.session_state.is_day_two = False

# --- الصفحة الأولى: التسجيل وربط الجوال ---
if st.session_state.page == 'welcome':
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        with st.form("registration"):
            st.markdown('<h2 style="text-align: center; color: #1A365D;">ربط نظام Path7 بجوالك</h2>', unsafe_allow_html=True)
            u_name = st.text_input("الاسم", "جُمانة")
            # طلب الرقم لضمان فتح الشات المباشر
            u_phone = st.text_input("رقم الجوال (مع مفتاح الدولة مثلاً 9665...)", placeholder="9665XXXXXXXX")
            u_budget = st.radio("الميزانية", ["اقتصادية", "فاخرة"], horizontal=True)
            
            if st.form_submit_button("تفعيل المزامنة اللحظية ✅"):
                if u_phone:
                    st.session_state.user_name = u_name
                    st.session_state.user_phone = u_phone
                    st.session_state.user_budget = u_budget
                    st.session_state.page = 'system'
                    st.rerun()
                else:
                    st.error("لطفاً أدخلي رقم الجوال لتفعيل ميزة الإشعارات")

# --- الصفحة الثانية: النظام الذكي ---
else:
    col_main, col_stats = st.columns([2, 1])
    
    with col_main:
        if not st.session_state.is_day_two:
            st.markdown(f'<div class="bot-msg"><b>Path7 Bot:</b><br>أهلاً {st.session_state.user_name}! تم ربط النظام بنجاح. سأرسل لكِ تحديثات الزحمة فوراً.</div>', unsafe_allow_html=True)
            
            if st.button("تحليل الوجهة الآن 🔍"):
                st.session_state.dest_result = random.choice(["بوليفارد وورلد", "المصمك", "وادي حنيفة"])
                st.session_state.traffic_val = random.randint(20, 90)
                
                # إرسال واتساب للرقم المدخل فعلياً
                wa_msg = f"تنبيه لحظي من Path7: وجهتك المقترحة هي {st.session_state.dest_result}. نسبة الزحمة الآن {st.session_state.traffic_val}%."
                wa_url = f"https://wa.me/{st.session_state.user_phone}?text={wa_msg}"
                st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; padding:10px; background:#25D366; color:white; border:none; border-radius:10px;">إرسال التقرير لـ WhatsApp 📱</button></a>', unsafe_allow_html=True)
        
        else:
            # محاكاة اليوم الثاني
            st.warning("🔔 إشعار متابعة (اليوم الثاني)")
            st.markdown(f'''
                <div class="bot-msg" style="background: #FFF9C4; border-right-color: #FBC02D;">
                <b>Path7 Bot:</b><br>
                صباح الخير {st.session_state.user_name}! هاه لسا جالتنا بالرياض ولا خلصت فترة إجازتك؟<br>
                لو لسا موجودة، اضغطي "تحديث" لنبدأ مسار اليوم!
                </div>
            ''', unsafe_allow_html=True)
            if st.button("تحديث المسار ليوم جديد 🔄"):
                st.session_state.is_day_two = False
                st.rerun()
            if st.button("انتهت الرحلة (وداع السائح) 👋"):
                st.success("رحلة سعيدة، ننتظركِ مرة أخرى في الرياض! ✈️")

    with col_stats:
        st.subheader("إدارة الرحلة")
        if st.button("⏩ محاكاة مرور 24 ساعة"):
            st.session_state.is_day_two = True
            st.rerun()
        
        st.markdown("---")
        # النجوم
        st.subheader("تقييمك")
        stars = st.columns(5)
        for i in range(1, 6):
            if stars[i-1].button(f"{i}⭐"): st.session_state.rating = i
