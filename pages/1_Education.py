import streamlit as st
import time

# --- 1. إعدادات التصميم الإبداعي (Neon Education UI) ---
st.markdown("""
    <style>
    /* تحسين الخلفية العامة */
    .stApp {
        background-color: #000000 !important;
    }

    /* تحسين العناوين الرئيسية لتبرز فوق الأسود */
    h1 {
        color: #FFD700 !important;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
        text-align: center;
        font-weight: 900 !important;
    }
    
    h3 {
        color: #FFFFFF !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
        font-weight: 800 !important;
    }

    /* تحسين تسميات الحقول (Labels) لتكون واضحة جداً */
    label {
        color: #00FF88 !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        text-shadow: 0 0 5px rgba(0, 255, 136, 0.2);
    }
    
    /* بطاقة المسار التعليمي - Glassmorphism */
    .course-card {
        background: rgba(20, 20, 20, 0.9);
        backdrop-filter: blur(20px);
        padding: 35px;
        border-radius: 30px;
        border: 1px solid #00FF88;
        box-shadow: 0 15px 35px rgba(0, 255, 136, 0.15);
        margin-bottom: 25px;
        transition: all 0.3s ease;
    }
    .course-card:hover {
        transform: translateY(-10px);
        border-color: #FFD700;
        box-shadow: 0 20px 40px rgba(255, 215, 0, 0.2);
    }

    /* نصوص عالية الوضوح داخل البطاقات */
    .elite-title {
        color: #FFD700 !important;
        font-weight: 900;
        font-size: 30px;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }
    .elite-desc {
        color: #FFFFFF !important;
        font-size: 18px;
        line-height: 1.6;
    }

    /* تخصيص صناديق الاختيار (Selectbox) */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #111 !important;
        border-radius: 15px !important;
        border: 2px solid #333 !important;
        color: white !important;
    }
    .stSelectbox div[data-baseweb="select"]:hover {
        border-color: #00FF88 !important;
    }
    
    /* أزرار الإطلاق */
    .stButton>button {
        background: linear-gradient(135deg, #00FF88 0%, #008080 100%) !important;
        color: #000 !important;
        font-weight: 900 !important;
        border-radius: 15px !important;
        height: 60px !important;
        font-size: 20px !important;
        border: none !important;
    }
    
    /* تحسين شريط التقدم */
    .stProgress > div > div > div > div {
        background-color: #00FF88 !important;
        box-shadow: 0 0 15px #00FF88;
    }
    </style>

    <script>
    function playSfx(url) {
        const audio = new Audio(url);
        audio.volume = 0.4;
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
st.markdown("<p style='color:#00FF88; font-size:22px; text-align:center; font-weight:bold;'>نحول طموحك إلى كفاءة عالمية</p>", unsafe_allow_html=True)

st.divider()

# شريط التقدم التعليمي العام
st.write("### 📈 مستوى تطورك القيادي")
st.progress(35)
st.markdown("<p style='color:#FFFFFF; font-size:16px;'>لقد أكملت <b>35%</b> من مسار 'تأسيس القيادة'.</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# وكيل التوصيات الذكي
with st.container():
    st.markdown("""
    <div class="course-card">
        <h2 class="elite-title">🤖 وكيل التوصيات الذكي</h2>
        <p class="elite-desc">بناءً على هدفك (<b>المليار دولار</b>) الذي حددته في صفحة الرؤية، قمت بتحليل المسارات المتاحة لاقتراح الأنسب لك.</p>
    </div>
    """, unsafe_allow_html=True)

    interest = st.selectbox(
        "ما هو التحدي الذي تواجهه الآن؟",
        ["اختر تحدياً...", "إدارة فرق عمل ضخمة", "رفع كفاءة التدفقات النقدية", "غزو أسواق دولية جديدة"]
    )

    if interest != "اختر تحدياً...":
        play_edu_sound("recommend")
        if interest == "إدارة فرق عمل ضخمة":
            st.success("🎯 وكيل MR7 يقترح: 'ماستر كلاس القيادة الهرمية'. ستتعلم كيف تدير 100+ موظف بكفاءة المليار.")
        elif interest == "رفع كفاءة التدفقات النقدية":
            st.success("🎯 وكيل MR7 يقترح: 'دبلوم الهندسة المالية المتقدمة'.")
        elif interest == "غزو أسواق دولية جديدة":
            st.success("🎯 وكيل MR7 يقترح: 'استراتيجيات التوسع العالمي العابر للقارات'.")

st.divider()

# عرض المسارات التعليمية كبطاقات
st.subheader("🚀 مسارات التعلم النشطة")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="course-card">
        <h3 style='color:#FFD700;'>عقلية المليار 🧠</h3>
        <p style='color:#ccc;'>12 درس مرئي - 5 تمارين عملية</p>
        <p style='color:#00FF88; font-weight:bold;'>تم إنجاز 60%</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("متابعة التعلم 📖", key="c1"):
        play_edu_sound("start")

with col2:
    st.markdown("""
    <div class="course-card">
        <h3 style='color:#FFD700;'>إدارة الانبعاثات الكربونية 🌍</h3>
        <p style='color:#ccc;'>8 دروس - مشروع تطبيقي</p>
        <p style='color:#00FF88; font-weight:bold;'>لم يتم البدء</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("بدء المسار الآن 🚀", key="c2"):
        play_edu_sound("start")

# زر العودة أو الانتقال للمحفظة
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("💰 الانتقال لمحفظة الأرباح"):
    st.switch_page("pages/3_Wallet.py")
