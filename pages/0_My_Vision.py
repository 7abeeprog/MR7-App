import streamlit as st
import time

# 1. إعدادات الصفحة والجرافيك (CSS المطور)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 60px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(80, 200, 120, 0.4);
    }
    .main-card {
        background-color: #1A1A1A;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #333;
        margin-bottom: 20px;
    }
    .stRadio > div {
        background-color: #1A1A1A;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #444;
    }
    </style>
    """, unsafe_allow_html=True)

# دالة لتشغيل صوت النجاح (Sound Effect)
def play_sound():
    sound_html = """
    <audio autoplay>
        <source src="https://www.soundjay.com/buttons/sounds/button-37a.mp3" type="audio/mpeg">
    </audio>
    """
    st.components.v1.html(sound_html, height=0)

# 2. جدار الحماية
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("الرجاء تسجيل الدخول من الصفحة الرئيسية أولاً.")
    st.stop()

st.title("🎯 بوصلة القائد 2.0: صناعة المستقبل")
st.write("---")

# إعداد حالة الجلسة
if 'vision_step' not in st.session_state:
    st.session_state.vision_step = 1
    st.session_state.selected_category = None
    st.session_state.temp_choice = None

# --- شريط التقدم الذكي ---
progress_mapping = {1: 10, 2: 50, 3: 90}
progress_val = progress_mapping.get(st.session_state.vision_step, 100)
st.progress(progress_val)
st.caption(f"مستوى صياغة الرؤية: {progress_val}%")

# --- المرحلة الأولى: اختيار التصنيف (4 خيارات) ---
if st.session_state.vision_step == 1:
    st.subheader("اختر ركيزة الانطلاق الأساسية:")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💰 مالي"):
            st.session_state.selected_category = "مالي"
            st.session_state.vision_step = 2
            st.rerun()
    with col2:
        if st.button("🎓 تعليمي"):
            st.session_state.selected_category = "تعليمي"
            st.session_state.vision_step = 2
            st.rerun()
    with col3:
        if st.button("✈️ سفر"):
            st.session_state.selected_category = "سفر"
            st.session_state.vision_step = 2
            st.rerun()
    with col4:
        if st.button("❤️ عاطفي"):
            st.session_state.selected_category = "عاطفي"
            st.session_state.vision_step = 2
            st.rerun()

# --- المرحلة الثانية: تحديد مستوى الطموح (4 مستويات) ---
elif st.session_state.vision_step == 2:
    cat = st.session_state.selected_category
    st.subheader(f"رائع! أنت الآن في مسار الـ {cat}. اختر سقف طموحك:")

    # تعريف الـ 4 مستويات لكل فئة
    levels = {
        "مالي": ["مليون دولار 🌱", "10 ملايين دولار 📈", "100 مليون دولار 🔥", "مليار دولار (نادي التريليون) 🌍"],
        "تعليمي": ["إتقان مهارة قيادية 🧠", "دبلوم احترافي دولي 📜", "درجة خبير متخصص (PhD) 🎓", "تأليف منهج عالمي باسمك ✍️"],
        "سفر": ["استكشاف محلي 🧭", "غزو قارة جديدة 🗺️", "جولة حول العالم ✈️", "رحلة مهمة عالمية لإرساء الفكر 🕊️"],
        "عاطفي": ["استقرار وتوازن داخلي ❤️", "بناء شبكة علاقات النخبة 🤝", "صناعة أثر مجتمعي مستدام 🏛️", "ترك إرث إنساني خالد للعالم 🕊️"]
    }

    selected_level = st.radio("حدد هدفك بدقة:", levels[cat])
    
    st.write("---")
    if st.button("✅ تثبيت الهدف المختار"):
        play_sound() # تشغيل الصوت عند الضغط
        st.session_state.temp_choice = selected_level
        with st.spinner("يتم الآن توثيق هدفك في سجلات العظماء..."):
            time.sleep(1.5)
            st.session_state.vision_step = 3
            st.rerun()

# --- المرحلة الثالثة: الاحتفال والرسالة ---
elif st.session_state.vision_step == 3:
    st.balloons()
    st.success(f"تم تثبيت هدفك بنجاح: {st.session_state.temp_choice}")
    
    st.markdown(f"""
    <div class="main-card">
        <h3>🤖 رسالة الوكيل الذكي للقائد:</h3>
        <p style='font-style: italic; font-size: 20px;'>
        "اختيارك لـ '{st.session_state.temp_choice}' ليس مجرد رقم أو كلمة، إنه العقد الذي وقعته اليوم مع المستقبل. 
        بصفتك جزءاً من MR7، نحن لا نعترف بالمستحيل. ابدأ الآن بتصرفات قائد يمتلك هذا الهدف بالفعل."
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("تعديل الرؤية أو البدء من جديد"):
        st.session_state.vision_step = 1
        st.rerun()

بهذا الكود، أصبح التطبيق يتمتع بـ:
1. **جرافيكس محسن** عبر CSS مخصص للبطاقات والأزرار.
2. **4 مستويات** لكل فئة أهداف لتوفير تدرج احترافي.
3. **مؤثر صوتي** يعمل لحظة "تثبيت الهدف".
4. **زر "تثبيت الهدف"** كخطوة تأكيدية تزيد من تفاعل المستخدم.

قم بتحديث ملف `0_My_Vision.py` بهذا الكود الجديد وجربه، ستشعر بفرق كبير في "فخامة" التجربة! 🦾✨
