import streamlit as st
import time

# --- 1. إعدادات التصميم والجرافيك (UI/UX) ---
st.markdown("""
    <style>
    /* تصميم البطاقة الرئيسية */
    .vision-card {
        background: linear-gradient(145deg, #1e1e1e, #121212);
        padding: 30px;
        border-radius: 25px;
        border: 1px solid #333;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 25px;
    }
    /* تحسين شكل الراديو (الاختيارات) */
    .stRadio > div {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 20px;
        border: 1px solid #444;
        transition: all 0.3s ease;
    }
    .stRadio > div:hover {
        border-color: #50C878;
    }
    /* تصميم زر التثبيت */
    .stButton>button {
        background: linear-gradient(90deg, #50C878, #2E8B57);
        color: white;
        border: none;
        height: 65px;
        font-size: 20px !important;
        font-weight: bold;
        border-radius: 15px;
        transition: all 0.4s;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(80, 200, 120, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# دالة التأثير الصوتي
def play_confirm_sound():
    sound_html = """
    <audio autoplay>
        <source src="https://www.soundjay.com/buttons/sounds/button-09.mp3" type="audio/mpeg">
    </audio>
    """
    st.components.v1.html(sound_html, height=0)

# --- 2. التحقق من الدخول ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("الرجاء تسجيل الدخول من الصفحة الرئيسية أولاً.")
    st.stop()

# --- 3. إدارة حالة الصفحة ---
if 'v_step' not in st.session_state:
    st.session_state.v_step = 1
    st.session_state.v_cat = None
    st.session_state.v_goal = None

# --- 4. واجهة المستخدم ---
st.title("🏆 صياغة الرؤية القيادية")
st.write("مستقبلك يبدأ من هذه اللحظة. حدد مسارك بعناية.")

# شريط التقدم
p_val = {1: 15, 2: 60, 3: 100}.get(st.session_state.v_step, 100)
st.progress(p_val)

st.write("---")

# المرحلة الأولى: اختيار التصنيف
if st.session_state.v_step == 1:
    st.markdown("### 1️⃣ اختر ركيزة قوتك القادمة:")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        if st.button("💰 مالي"):
            st.session_state.v_cat = "مالي"
            st.session_state.v_step = 2
            st.rerun()
    with c2:
        if st.button("🎓 تعليمي"):
            st.session_state.v_cat = "تعليمي"
            st.session_state.v_step = 2
            st.rerun()
    with c3:
        if st.button("✈️ سفر"):
            st.session_state.v_cat = "سفر"
            st.session_state.v_step = 2
            st.rerun()
    with c4:
        if st.button("❤️ عاطفي"):
            st.session_state.v_cat = "عاطفي"
            st.session_state.v_step = 2
            st.rerun()

# المرحلة الثانية: اختيار مستوى الطموح (4 مستويات)
elif st.session_state.v_step == 2:
    cat = st.session_state.v_cat
    st.markdown(f"### 2️⃣ مسار الـ {cat}: حدد سقف طموحك")
    
    levels = {
        "مالي": ["1 مليون دولار (بداية التمكين) 🌱", "10 ملايين دولار (مرحلة التوسع) 📈", "100 مليون دولار (سيادة السوق) 🔥", "1 مليار دولار (نادي التريليون) 🌍"],
        "تعليمي": ["إتقان مهارة تقنية/قيادية 🧠", "دبلوم احترافي دولي 📜", "درجة خبير متخصص (PhD) 🎓", "تأليف منهج عالمي ✍️"],
        "سفر": ["استكشاف محلي معمق 🧭", "فتح آفاق في قارة جديدة 🗺️", "جولة عالمية لنشر الفكر ✈️", "مهمة عالمية إنسانية قيادية 🕊️"],
        "عاطفي": ["توازن داخلي وعائلي ❤️", "بناء شبكة علاقات النخبة 🤝", "أثر مجتمعي رائد ومستدام 🏛️", "ترك إرث إنساني خالد 🕊️"]
    }

    selected = st.radio("اختر المستوى الذي تجرؤ على الوصول إليه:", levels[cat])
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🎯 تثبيت الهدف وإعلان الرؤية"):
        play_confirm_sound()
        st.session_state.v_goal = selected
        with st.spinner("جاري تشفير هدفك في قاعدة بيانات العظماء..."):
            time.sleep(1.8)
            st.session_state.v_step = 3
            st.rerun()

# المرحلة الثالثة: النتيجة والاحتفال
elif st.session_state.v_step == 3:
    st.balloons()
    st.markdown(f"""
    <div class="vision-card">
        <h2 style='color: #50C878; text-align: center;'>✅ تم تثبيت الرؤية</h2>
        <p style='text-align: center; font-size: 24px;'>هدفك الحالي: <b>{st.session_state.v_goal}</b></p>
        <hr style='border-color: #333;'>
        <p style='font-style: italic; color: #DAFFDE;'>
        "الوكيل الذكي: لقد قمت للتو بتغيير احتمالات مستقبلك. هذا الهدف يتطلب شخصية جديدة، عادات جديدة، وعقلاً لا يعرف الكلل. 
        نحن هنا لنقودك نحو هذا الاستحقاق."
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("تعديل المسار"):
        st.session_state.v_step = 1
        st.rerun()
