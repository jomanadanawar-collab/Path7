import streamlit as st
import json
import os

# إعدادات الصفحة الأساسية للتطبيق ونظام الاتجاه العربي/الإنجليزي
st.set_page_config(page_title="Path7 - Riyadh Smart Guide", page_icon="📍", layout="centered")

# دالة مساعدة لقراءة ملف البيانات مع دعم ترميز UTF-8 لمنع تشوه النصوص العربية
def load_data():
    with open("path7_data.json", "r", encoding="utf-8") as file:
        return json.load(file)

data = load_data()

# شريط جانبي لاختيار اللغة
lang = st.sidebar.selectbox("🌐 Language / اللغة", ["العربية", "English"])
texts = data[lang]

# تصميم الهوية الفخرية في الأعلى (نادي الهندسة بجامعة الإمام عبدالرحمن بن فيصل 2026)
st.markdown(
    """
    <div style="text-align: center; background-color: #f0f7ff; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #0066cc;">
        <h4 style="color: #003366; margin: 0;">نادي الهندسة | Engineering Club 2026</h4>
        <p style="color: #666; margin: 5px 0 0 0; font-size: 0.9rem;">جامعة الإمام عبدالرحمن بن فيصل - IAU</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# عنوان التطبيق الرئيسي
st.title(texts["p_name"])
st.subheader(texts["subtitle"])

# استقبال مدخلات المستخدم الأساسية
visitor_name = st.text_input(texts["visitor_name"], placeholder="Jumana")

st.write("---")

# اختيار نمط الرحلة (اقتصادية أو فاخرة)
budget_choice = st.radio(
    texts["budget_q"],
    [texts["eco"], texts["lux"]]
)

# تحويل الاختيار النصي إلى المفتاح البرمجي المناسب داخل الـ JSON
budget_key = "Economy" if budget_choice == texts["eco"] else "Luxury"

# اختيار الاهتمامات الحالية
selected_interest = st.selectbox(texts["interests_q"], texts["interests_list"])

# زر بدء التحليل الذكي للمسار
analyze_clicked = st.button(texts["analyze_btn"], type="primary")

# إدارة الحالة (State Management) لحفظ النتائج المعروضة أثناء تغيير وسائل النقل
if analyze_clicked:
    st.session_state["analyzed"] = True

# عرض التوصيات والمسارات الذكية في حال تم تفعيل البحث
if st.session_state.get("analyzed", False):
    st.write("### 🧭 Recommended Path / المسار المقترح")
    
    # جلب قائمة الأماكن المطابقة من قاعدة البيانات
    all_places = texts["db"][budget_key]
    
    # فلترة الأماكن بناءً على الفئة المختارة (تدعم الفلترة باللغتين)
    filtered_places = [
        p for p in all_places 
        if p.get("الفئة") == selected_interest or p.get("Category") == selected_interest
    ]
    
    if filtered_places:
        for idx, place in enumerate(filtered_places):
            # إنشاء حاوية أنيقة لكل معلم
            with st.container():
                place_title = place.get("الوجهة", place.get("Destination"))
                place_desc = place.get("وصف", place.get("Description"))
                
                st.markdown(f"#### 📍 {place_title}")
                st.write(place_desc)
                
                # عرض الصورة ديناميكياً إذا تم العثور عليها في المجلد
                img_name = place.get("image", "")
                if img_name and os.path.exists(img_name):
                    st.image(img_name, use_container_width=True)
                
                # حساب وإدارة وقت الوصول والاتصال الذكي بالمترو
                base_time = place.get("b_time", 20)
                has_metro = place.get("metro", false)
                
                st.write(f"**{texts['transport_q']}:**")
                
                # عرض أزرار وسائل النقل بشكل أفقي متناسق
                col1, col2, col3 = st.columns(3)
                with col1:
                    metro_btn = st.button(texts["m_btn"], key=f"m_{idx}")
                with col2:
                    car_btn = st.button(texts["c_btn"], key=f"c_{idx}")
                with col3:
                    taxi_btn = st.button(texts["t_btn"], key=f"t_{idx}")
                
                # حساب الوقت وعرض حالة خطوط النقل الذكية بناءً على الضغط
                if metro_btn:
                    if has_metro:
                        st.success(f"✅ {texts['metro_msg']} | {texts['est_time']}: {base_time} {texts['min']}")
                    else:
                        st.error(f"❌ {texts['metro_fail']} | {texts['est_time']}: -- {texts['min']}")
                elif car_btn:
                    st.info(f"🚗 {texts['est_time']}: {base_time + 10} {texts['min']} (Traffic integrated)")
                elif taxi_btn:
                    st.info(f"🚕 {texts['est_time']}: {base_time + 5} {texts['min']}")
                else:
                    st.caption(texts["wait_choice"])
                
                # رابط فتح خرائط جوجل الخارجي للمعلم
                maps_url = f"https://www.google.com/maps/search/?api=1&query={place_title}"
                st.markdown(f"[{texts['map_btn']}]({maps_url})")
                
                st.write("---")
                
        # قسم تقييم واجهة المستخدم الختامي والتفاعلي
        st.write(texts["rating_q"])
        st.slider("", 1, 5, 5, key="user_rating")
        
        if st.button(texts["next_day"]):
            st.success(texts["finish"])
    else:
        st.warning("No destinations found for this active query yet. Try another combination! / لم يتم العثور على معالم لهذه الفئة حالياً، جربي مزيجاً آخر!")
