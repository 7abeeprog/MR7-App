import streamlit as st
import time

# 1. جدار الحماية (التأكد من تسجيل الدخول)
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("الرجاء تسجيل الدخول من الصفحة الرئيسية أولاً.")
    st.stop()

st.title("🎯 بوصلة القائد: حدد رؤيتك للتريليون")
st.write("أهلاً بك يا قائد. العظمة تبدأ بقرار، والقرار يبدأ بهدف واضح.")

# إعداد حالة الجلسة للأهداف
if 'vision_step' not in st.session_state:
    st.session_state.vision_step = 1
    st.session_state.selected_category = None

# --- شريط التقدم الذكي ---
progress_value = 25 if st.session_state.vision_step == 1 else 75
st.progress(progress_value)
st.caption(f"مستوى إكمال الرؤية: {progress_value}%")

st.divider()

# --- المرحلة الأولى: اختيار التصنيف ---
if st.session_state.vision_step == 1:
    st.subheader("ما هو الجانب الذي تود التركيز عليه الآن؟")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💰 مالي", use_container_width=True):
            st.session_state.selected_category = "مالي"
            st.session_state.vision_step = 2
            st.rerun()
            
    with col2:
        if st.button("❤️ عاطفي", use_container_width=True):
            st.session_state.selected_category = "عاطفي"
            st.session_state.vision_step = 2
            st.rerun()

    with col3:
        if st.button("✈️ سفر", use_container_width=True):
            st.session_state.selected_category = "سفر"
            st.session_state.vision_step = 2
            st.rerun()

    with col4:
        if st.button("🎓 تعليمي", use_container_width=True):
            st.session_state.selected_category = "تعليمي"
            st.session_state.vision_step = 2
            st.rerun()

# --- المرحلة الثانية: تحديد مستوى الطموح (البطاقات الذكية) ---
elif st.session_state.vision_step == 2:
    category = st.session_state.selected_category
    st.subheader(f"رائع! لقد اخترت المسار الـ{category}. حدد الآن سقف طموحك:")

    options = []
    if category == "مالي":
        options = ["مليون دولار (بداية القائد) 🌱", "100 مليون دولار (تأثير إقليمي) 📈", "مليار دولار (نادي التريليون) 🌍"]
    elif category == "تعليمي":
        options = ["إتقان مهارة قيادية 🧠", "الحصول على دبلوم احترافي 📜", "تأليف منهج قيادي عالمي ✍️"]
    elif category == "سفر":
        options = ["رحلة استكشافية محلية 🧭", "زيارة قارة جديدة 🗺️", "جولة حول العالم لنشر الفكر ✈️"]
    elif category == "عاطفي":
        options = ["استقرار وتوازن عائلي ❤️", "بناء شبكة علاقات مؤثرة 🤝", "ترك إرث إنساني عالمي 🕊️"]

    choice = st.radio("اختر مستواك المستهدف:", options)

    if st.button("تثبيت الهدف وإطلاق الرؤية 🚀"):
        with st.spinner("جاري تحليل طموحك وربطه بمسار التريليون..."):
            time.sleep(2)
            st.session_state.vision_step = 3
            st.session_state.final_choice = choice
            st.rerun()

# --- المرحلة الثالثة: رسالة الذكاء الاصطناعي والاحتفال ---
elif st.session_state.vision_step == 3:
    st.balloons()
    st.success(f"تم اعتماد هدفك: {st.session_state.final_choice}")
    
    # رسالة تحفيزية ذكية بناءً على الاختيار
    st.info("🤖 **رسالة من وكيلك الذكي:**")
    if "مليار" in st.session_state.final_choice or "عالمي" in st.session_state.final_choice:
        st.write("> 'أنت لا تستهدف رقماً، أنت تستهدف تغيير وجه التاريخ. القادة العظام لا يطلبون الإذن، بل يصنعون الطريق. ابدأ اليوم كأنك تملك المليار بالفعل.'")
    else:
        st.write("> 'خطوة ممتازة في طريق الألف ميل. التوازن والتعلم هما وقود القائد الناجح. نحن معك في كل خطوة.'")
    
    if st.button("العودة لتعديل الأهداف"):
        st.session_state.vision_step = 1
        st.rerun()
