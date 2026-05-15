# --- الصفحات ---
if st.session_state.page == 'welcome':
    st.markdown(f'<div class="glass-card" style="text-align: center;"><h1>{strings["title"]}</h1><p>{strings["sub"]}</p></div>', unsafe_allow_html=True)
    col_w1, col_w2, col_w3 = st.columns([1, 2, 1])
    
    with col_w2:
        # إضافة خانة رقم الحجز الثابت للمحكمين
        demo_code = st.text_input("Enter Booking Number / أدخل رقم الحجز (اختياري)", placeholder="e.g. PATH7-2026")
        
        st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)
        
        # إذا أدخل الكود الصحيح، يتم تعبئة البيانات تلقائياً وتخطي التعقيد
        if demo_code.strip().upper() == "PATH7-2026":
            st.success("✨ Demo Mode Activated / تم تفعيل طور العرض الثابت")
            st.session_state.user_name = "VIP Judge" if not IS_AR else "المُحكّم المتميز"
            u_budget = "Luxury" if not IS_AR else "فاخرة"
            
            # زر الانطلاق السريع للمحكم
            if st.button("Fast Track Entry ⚡ / دخول سريع"):
                st.session_state.budget_key = "Luxury"
                st.session_state.page = 'system'
                st.rerun()
        else:
            # الدخول العادي في حال لم يتم إدخال الكود الثابت
            st.session_state.user_name = st.text_input(strings["name_q"])
            u_budget = st.radio(strings["budget_q"], strings["budgets"], horizontal=True)
            
            if st.button(strings["start_btn"]):
                if st.session_state.user_name:
                    st.session_state.budget_key = "Luxury" if (u_budget in ["فاخرة", "Luxury"]) else "Economy"
                    st.session_state.page = 'system'
                    st.rerun()
                else:
                    st.warning("Please enter your name / فضلاً أدخل اسمك")
