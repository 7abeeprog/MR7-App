import streamlit as st
import time
from datetime import datetime, date
# --- كود محرك الأنماط الشامل (Theme Engine) ---
# انسخ هذا الجزء وضعه في بداية أي صفحة بعد سطر الاستدعاء (import)

# 1. التأكد من وجود متغير النمط في ذاكرة الجلسة
if 'app_theme' not in st.session_state:
    st.session_state.app_theme = "غامق إمبراطوري 🖤"

# 2. تعريف الألوان والخصائص لكل نمط (Themes Dictionary)
themes = {
    "غامق إمبراطوري 🖤": {
        "bg": "#000000", "sidebar": "#050505", "text": "#FFFFFF", 
        "accent": "#FFD700", "card": "rgba(30, 30, 30, 0.9)", "border": "#FFD700",
        "select_text": "#FFFFFF", "select_bg": "#1A1A1A"
    },
    "فاتح ملكي ✨": {
        "bg": "#F5F5F5", "sidebar": "#FFFFFF", "text": "#1A1A1A", 
        "accent": "#B8860B", "card": "rgba(255, 255, 255, 0.95)", "border": "#B8860B",
        "select_text": "#1A1A1A", "select_bg": "#FFFFFF"
    },
    "أزرق القيادة 💙": {
        "bg": "#001F3F", "sidebar": "#001529", "text": "#FFFFFF", 
        "accent": "#0074D9", "card": "rgba(0, 31, 63, 0.8)", "border": "#0074D9",
        "select_text": "#FFFFFF", "select_bg": "#001529"
    },
    "أخضر الاستدامة 💚": {
        "bg": "#002B1B", "sidebar": "#001A10", "text": "#FFFFFF", 
        "accent": "#00FF88", "card": "rgba(0, 43, 27, 0.8)", "border": "#00FF88",
        "select_text": "#FFFFFF", "select_bg": "#001A10"
    }
}

t = themes[st.session_state.app_theme]

# 3. حقن تنسيقات CSS بناءً على النمط المختار
st.markdown(f"""
    <style>
    /* الخلفية العامة */
    .stApp {{ background-color: {t['bg']} !important; color: {t['text']} !important; }}
    
    /* القائمة الجانبية */
    [data-testid="stSidebar"] {{ background-color: {t['sidebar']} !important; border-right: 2px solid {t['accent']} !important; }}

    /* النصوص والعناوين */
    div[data-testid="stMarkdownContainer"] p, h2, h3, span, label, li {{ color: {t['text']} !important; font-weight: 700 !important; }}
    h1 {{ background: linear-gradient(90deg, {t['accent']}, {t['text']}, {t['accent']}); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 950 !important; text-align: center; filter: drop-shadow(0 0 10px {t['accent']}); font-size: 3rem !important; }}

    /* حل مشكلة القوائم المنسدلة (Selectbox) لضمان وضوح النص */
    div[data-baseweb="select"] > div {{ background-color: {t['select_bg']} !important; color: {t['select_text']} !important; }}
    div[data-baseweb="popover"] ul {{ background-color: {t['select_bg']} !important; }}
    div[data-baseweb="popover"] li {{ color: {t['select_text']} !important; background-color: {t['select_bg']} !important; }}
    div[data-baseweb="popover"] li:hover {{ background-color: {t['accent']} !important; color: #000000 !important; }}

    /* تنسيق الأزرار */
    .stButton>button {{ background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important; color: #000000 !important; font-weight: 950 !important; border-radius: 20px !important; }}
    </style>
    """, unsafe_allow_html=True)

# 4. القائمة الجانبية للتحكم في النمط
with st.sidebar:
    st.markdown(f"### 🎨 تخصيص المظهر")
    theme_choice = st.selectbox(
        "اختر نمط الألوان المفضل لديك:",
        options=list(themes.keys()),
        index=list(themes.keys()).index(st.session_state.app_theme)
    )
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
# --- 1. إعدادات التصميم الفائق (Ultra-Visibility & Journey UI) ---
st.markdown("""
    <style>
    /* تحسين الخلفية العامة وجعلها سوداء عميقة جداً */
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    /* ضمان أن كل النصوص باللون الأبيض الناصع أو الذهبي للوضوح */
    div[data-testid="stMarkdownContainer"] p, li, span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 1.1rem;
    }

    /* العنوان الرئيسي - ذهبي متوهج */
    h1 {
        background: linear-gradient(90deg, #FFD700, #FFFFFF, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 950 !important;
        text-align: center;
        filter: drop-shadow(0 0 15px rgba(255, 215, 0, 0.8));
        font-size: 3.5rem !important;
        margin-bottom: 0px !important;
    }
    
    /* عداد رحلة الـ 100 يوم - تصميم Neon */
    .journey-counter {
        background: linear-gradient(145deg, #111, #050505);
        border: 2px solid #FFD700;
        border-radius: 25px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.2);
    }
    .days-number {
        font-size: 5rem !important;
        font-weight: 900 !important;
        color: #FFD700 !important;
        line-height: 1;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
    }
    .days-label {
        font-size: 1.5rem !important;
        color: #FFFFFF !important;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* بطاقات المسارات التعليمية */
    .course-card {
        background: rgba(25, 25, 25, 0.95);
        padding: 40px;
        border-radius: 35px;
        border: 2px solid #00FF88;
        box-shadow: 0 10px 40px rgba(0, 255, 136, 0.1);
        margin-bottom: 30px;
    }

    /* تحسين تسميات الحقول (Labels) لتكون واضحة باللون الأخضر النيون */
    label {
        color: #00FF88 !important;
        font-weight: 900 !important;
        font-size: 1.4rem !important;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.4);
    }
    
    /* أزرار الإطلاق */
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%) !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
        height: 75px !important;
        font-size: 24px !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02) translateY(-5px);
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.5);
    }

    /* شريط التقدم */
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

# --- 3. حسابات رحلة الـ 100 يوم ---
# نفترض أن الرحلة بدأت قبل 15 يوماً كمثال
start_date = date(2026, 3, 27) 
today = date.today()
days_passed = (today - start_date).days
days_left = 100 - days_passed

# --- 4. واجهة المستخدم ---
st.title("🎓 مركز التميز القيادي")
st.markdown("<p style='color:#FFD700; font-size:24px; text-align:center; font-weight:bold; margin-top:-20px;'>نحو هندسة عقلية المليار دولار</p>", unsafe_allow_html=True)

# عداد رحلة الـ 100 يوم
st.markdown(f"""
<div class="journey-counter">
    <div class="days-label">يوم متبقي في رحلة الـ 100 يوم للسيادة</div>
    <div class="days-number">{max(0, days_left)}</div>
    <div style="color: #00FF88; font-weight: 800; font-size: 1.2rem; margin-top: 10px;">
        تم اجتياز {days_passed}% من المسار التاريخي
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# شريط التقدم التعليمي
st.markdown("### 📈 مستوى تطورك القيادي الموثق")
st.progress(35)
st.markdown("<p style='color:#FFFFFF; font-size:1.2rem; font-weight:bold;'>لقد أنجزت <span style='color:#00FF88; font-size:1.6rem;'>35%</span> من مسار 'تأسيس القيادة الإمبراطورية'.</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# وكيل التوصيات الذكي
with st.container():
    st.markdown("""
    <div class="course-card" style="border-color: #FFD700;">
        <h2 style="color: #FFD700; font-weight: 950; font-size: 2.2rem; margin-bottom: 15px;">🤖 وكيل التوصيات الذكي</h2>
        <p style="color: #FFFFFF; font-size: 1.3rem; line-height: 1.6;">
        بناءً على هدفك العظيم (<b>المليار دولار</b>) ومرحلتك في <b>رحلة الـ 100 يوم</b>، قمت بتحليل الفجوات واقتراح المسار الأمثل:
        </p>
    </div>
    """, unsafe_allow_html=True)

    interest = st.selectbox(
        "ما هو التحدي الاستراتيجي الذي يواجهك اليوم؟",
        ["اختر تحدياً من قائمة القادة...", "إدارة فرق عمل عابرة للقارات", "رفع كفاءة التدفقات النقدية والسيولة", "التوسع والاستحواذ في أسواق ناشئة"]
    )

    if interest != "اختر تحدياً من قائمة القادة...":
        play_edu_sound("recommend")
        if "إدارة فرق عمل" in interest:
            st.success("🎯 وكيل MR7 يقترح: 'ماستر كلاس القيادة الهرمية المرنة'.")
        elif "التدفقات النقدية" in interest:
            st.success("🎯 وكيل MR7 يقترح: 'دبلوم الهندسة المالية لأصحاب المليارات'.")
        elif "التوسع" in interest:
            st.success("🎯 وكيل MR7 يقترح: 'استراتيجيات الاختراق العالمي السريع'.")

st.divider()

# عرض المسارات التعليمية
st.subheader("🚀 مسارات التعلم النشطة")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="course-card">
        <h3 style='color:#FFD700; margin-bottom:15px; font-size: 1.8rem;'>عقلية المليار 🧠</h3>
        <p style='color:#FFFFFF; font-size:1.1rem;'>12 درس مرئي عالي الجودة - 5 مشاريع تطبيقية</p>
        <p style='color:#00FF88; font-weight:900; font-size:1.5rem; margin-top:10px;'>معدل الإنجاز: 60%</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("متابعة بناء العقلية 📖", key="course_1"):
        play_edu_sound("start")

with col2:
    st.markdown("""
    <div class="course-card">
        <h3 style='color:#FFD700; margin-bottom:15px; font-size: 1.8rem;'>القيادة الخضراء 🌍</h3>
        <p style='color:#FFFFFF; font-size:1.1rem;'>8 دروس استراتيجية - مشروع تقليل الانبعاثات</p>
        <p style='color:#FF4B4B; font-weight:900; font-size:1.5rem; margin-top:10px;'>لم يتم البدء بعد</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("بدء المسار البيئي 🚀", key="course_2"):
        play_edu_sound("start")

# الانتقال للمحفظة
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("💰 عرض أرباح القائد واستلام العمولات"):
    play_edu_sound("recommend")
    st.switch_page("pages/3_Wallet.py")
