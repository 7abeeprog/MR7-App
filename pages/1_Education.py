import streamlit as st
import time

# --- 1. إعدادات التصميم الإبداعي (Ultra-High Contrast Education UI) ---
st.markdown("""
    <style>
    /* تحسين الخلفية العامة وجعلها سوداء عميقة */
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    /* جعل كل النصوص الافتراضية بيضاء ناصعة */
    div[data-testid="stMarkdownContainer"] p, h2, h3, span {
        color: #FFFFFF !important;
        font-weight: 500;
    }

    /* تصميم العنوان الرئيسي (st.title) - ذهبي ملكي متوهج */
    h1 {
        background: linear-gradient(90deg, #FFD700, #FFFFFF, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 950 !important;
        text-align: center;
        filter: drop-shadow(0 0 15px rgba(255, 215, 0, 0.7));
        padding-top: 20px;
        padding-bottom: 20px;
        font-size: 3.2rem !important;
    }
    
    /* تصميم عناوين الأقسام */
    h3 {
        color: #FFFFFF !important;
        border-right: 5px solid #00FF88;
        padding-right: 15px;
        margin-top: 30px;
        font-weight: 800 !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
    }

    /* تحسين تسميات الحقول (Labels) لتكون واضحة باللون الأخضر النيون */
    label {
        color: #00FF88 !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        text-shadow: 0 0 8px rgba(0, 255, 136, 0.4);
        margin-bottom: 10px !important;
    }
    
    /* بطاقة المسار التعليمي - Glassmorphism فخم */
    .course-card {
        background: rgba(30, 30, 30, 0.95);
        backdrop-filter: blur(25px);
        padding: 40px;
        border-radius: 35px;
        border: 2px solid #00FF88;
        box-shadow: 0 20px 50px rgba(0, 255, 136, 0.1);
        margin-bottom: 30px;
        transition: all 0.4s ease;
    }
    .course-card:hover {
        transform: translateY(-12px);
        border-color: #FFD700;
        box-shadow: 0 25px 60px rgba(255, 215, 0, 0.25);
    }

    /* نصوص عالية الوضوح داخل البطاقات الذكية */
    .elite-title {
        color: #FFD700 !important;
        font-weight: 950;
        font-size: 34px;
        text-shadow: 0 0 12px rgba(255, 215, 0, 0.6);
        margin-bottom: 15px;
    }
    .elite-desc {
        color: #FFFFFF !important;
        font-size: 20px;
        line-height: 1.8;
        font-weight: 500;
    }

    /* تخصيص صناديق الاختيار (Selectbox) */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #151515 !important;
        border-radius: 18px !important;
        border: 2px solid #444 !important;
        height: 60px;
    }
    .stSelectbox div[data-baseweb="select"]:hover {
        border-color: #00FF88 !important;
    }
    
    /* أزرار الإطلاق القيادية */
    .stButton>button {
        background: linear-gradient(135deg, #00FF88 0%, #008080 100%) !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
        height: 70px !important;
        font-size: 22px !important;
        border: none !important;
        transition: all 0.3s !important;
        box-shadow: 0 10px 25px rgba(0, 255, 136, 0.3);
    }
    .stButton>button:hover {
        transform: scale(1.03);
        box-shadow: 0 15px 35px rgba(0, 255, 136, 0.5);
    }
    
    /* تحسين شريط التقدم ليكون زمردياً مشعاً */
    .stProgress > div > div > div > div {
        background-color: #00FF88 !important;
        box-shadow: 0 0 20px #00FF88;
    }
    </style>

    <script>
    function playSfx(url) {
        const audio = new Audio(url);
        audio.volume = 0.5;
        audio.play().catch(e => console.log('Audio Blocked'));
    }
    </script>
    """, unsafe_allow_html=True)

def play_edu_sound(sound_key="recommend"):
    sounds = {
        "recommend": "https://www.soundjay.com/buttons/sounds/button-16.mp3",
        "start": "https://www.soundjay.com/buttons/sounds/button-10.mp3"
    }
    st.components.v1.html(f"""
        <audio autoplay><source src="{sounds[sound_key]}" type="audio/mpeg"></audio>
    """, height=0)

# --- 2. جدار الحماية ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("الرجاء تسجيل الدخول أولاً للوصول إلى مركز المعرفة.")
    st.stop()

# --- 3. واجهة المستخدم ---
st.title("🎓 مركز التميز القيادي")
st.markdown("<p style='color:#00FF88; font-size:24px; text-align:center; font-weight:bold; text-shadow: 0 0 10px rgba(0,255,136,0.3);'>نحو هندسة عقلية المليار دولار</p>", unsafe_allow_html=True)

st.divider()

# شريط التقدم التعليمي العام بتصميم واضح
st.markdown("### 📈 مستوى تطورك القيادي الموثق")
st.progress(35)
st.markdown("<p style='color:#FFFFFF; font-size:18px; font-weight:bold;'>لقد أنجزت <span style='color:#00FF88; font-size:22px;'>35%</span> من مسار 'تأسيس القيادة الإمبراطورية'.</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# وكيل التوصيات الذكي (Smart AI Agent)
with st.container():
    st.markdown("""
    <div class="course-card">
        <h2 class="elite-title">🤖 وكيل التوصيات الذكي</h2>
        <p class="elite-desc">بناءً على هدفك العظيم (<b>المليار دولار</b>) الذي صغته في الرؤية، قمت بتحليل الفجوات المعرفية لديك واقتراح المسار الأمثل:</p>
    </div>
    """, unsafe_allow_html=True)

    # تحسين اختيار التحدي
    interest = st.selectbox(
        "ما هو التحدي الاستراتيجي الذي يواجهك الآن؟",
        ["اختر تحدياً من قائمة القادة...", "إدارة فرق عمل عابرة للقارات", "رفع كفاءة التدفقات النقدية والسيولة", "التوسع والاستحواذ في أسواق ناشئة"]
    )

    if interest != "اختر تحدياً من قائمة القادة...":
        play_edu_sound("recommend")
        if "إدارة فرق عمل" in interest:
            st.success("🎯 وكيل MR7 يقترح: 'ماستر كلاس القيادة الهرمية المرنة'. ستتعلم كيف تدير 500+ موظف بروح الفريق الواحد.")
        elif "التدفقات النقدية" in interest:
            st.success("🎯 وكيل MR7 يقترح: 'دبلوم الهندسة المالية المتقدمة لأصحاب المليارات'.")
        elif "التوسع" in interest:
            st.success("🎯 وكيل MR7 يقترح: 'استراتيجيات الاختراق العالمي: كيف تغزو سوقاً جديداً في 30 يوماً'.")

st.divider()

# عرض المسارات التعليمية كبطاقات متطورة
st.subheader("🚀 مسارات التعلم النشطة")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="course-card">
        <h3 style='color:#FFD700; margin-bottom:10px;'>عقلية المليار 🧠</h3>
        <p style='color:#FFFFFF; font-size:16px;'>12 درس مرئي عالي الجودة - 5 مشاريع تطبيقية</p>
        <p style='color:#00FF88; font-weight:900; font-size:20px;'>معدل الإنجاز: 60%</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("متابعة بناء العقلية 📖", key="course_1"):
        play_edu_sound("start")

with col2:
    st.markdown("""
    <div class="course-card">
        <h3 style='color:#FFD700; margin-bottom:10px;'>القيادة الخضراء 🌍</h3>
        <p style='color:#FFFFFF; font-size:16px;'>8 دروس استراتيجية - مشروع تقليل الانبعاثات</p>
        <p style='color:#FF4B4B; font-weight:900; font-size:20px;'>لم يتم البدء بعد</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("بدء المسار البيئي 🚀", key="course_2"):
        play_edu_sound("start")

# الانتقال للمحفظة
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("💰 عرض أرباح القائد واستلام العمولات"):
    play_edu_sound("recommend")
    st.switch_page("pages/3_Wallet.py")
