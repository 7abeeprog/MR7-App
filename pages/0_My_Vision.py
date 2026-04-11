import streamlit as st
import time

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
# --- 1. إعدادات التصميم الإبداعي الفائق (Ultra-Elite UI Customization) ---
st.markdown("""
    <style>
    /* تحسين الخلفية العامة للتطبيق */
    .stApp {
        background-color: #000000 !important;
    }
    
    /* هندسة القائمة الجانبية (Sidebar) لتكون ذهبية ملكية */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 2px solid #FFD700 !important;
        box-shadow: 5px 0 15px rgba(255, 215, 0, 0.1);
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    [data-testid="stSidebarNav"] li {
        border-radius: 10px;
        margin: 5px;
        transition: all 0.3s ease;
    }
    [data-testid="stSidebarNav"] li:hover {
        background-color: rgba(255, 215, 0, 0.15) !important;
        transform: translateX(5px);
    }

    /* توحيد ألوان النصوص العامة لتكون بيضاء ناصعة */
    div[data-testid="stMarkdownContainer"] p, h2, h3, span, label {
        color: #FFFFFF !important;
        font-weight: 600;
    }

    /* العنوان الرئيسي (st.title) - توهج ذهبي ثلاثي الأبعاد */
    h1 {
        background: linear-gradient(90deg, #FFD700, #FFFFFF, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 950 !important;
        text-align: center;
        filter: drop-shadow(0 0 12px rgba(255, 215, 0, 0.9));
        padding-top: 20px;
        padding-bottom: 10px;
        font-size: 3.5rem !important;
    }

    /* الوصف الفرعي الذهبي */
    .subtitle-text {
        text-align: center;
        font-size: 1.7rem !important;
        color: #FFD700 !important;
        font-weight: 800;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.6);
        margin-top: -20px;
        margin-bottom: 40px;
    }

    /* بطاقة الرؤية الزجاجية */
    .vision-card {
        background: rgba(20, 20, 20, 0.95);
        backdrop-filter: blur(30px);
        padding: 55px;
        border-radius: 45px;
        border: 2px solid #FFD700;
        box-shadow: 0 0 60px rgba(255, 215, 0, 0.3);
        margin-bottom: 30px;
        text-align: center;
    }
    
    /* نصوص براقة للنتيجة النهائية */
    .glitter-text {
        background: linear-gradient(90deg, #FFFFFF, #FFD700, #FFFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 42px;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.7);
    }

    /* تصميم أزرار الاختيار (Radio Buttons) بتباين عالٍ جداً */
    .stRadio > div {
        gap: 22px;
        padding: 10px;
    }
    .stRadio label {
        background: #0a0a0a !important;
        border: 2px solid #333 !important;
        padding: 28px 40px !important;
        border-radius: 22px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: 100%;
        color: #FFFFFF !important; 
        font-weight: 900 !important;
        font-size: 22px !important;
        display: flex !important;
        align-items: center !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.9) !important;
    }
    
    .stRadio label:hover {
        border-color: #00FF88 !important;
        background: #111111 !important;
        transform: scale(1.025) translateX(8px);
        color: #00FF88 !important;
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.3) !important;
    }
    
    .stRadio div[role="radiogroup"] input:checked + label {
        border-color: #FFD700 !important;
        background: #1a1a1a !important;
        color: #FFD700 !important;
        box-shadow: 0 0 40px rgba(255, 215, 0, 0.4) !important;
    }

    /* زر التثبيت الإمبراطوري */
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%) !important;
        color: #000000 !important;
        border: none !important;
        height: 85px !important;
        font-size: 28px !important;
        font-weight: 900 !important;
        border-radius: 25px !important;
        box-shadow: 0 15px 45px rgba(184, 134, 11, 0.6) !important;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 65px rgba(255, 215, 0, 0.8) !important;
    }

    /* شريط التقدم الذهبي */
    .stProgress > div > div > div > div {
        background-color: #FFD700;
        box-shadow: 0 0 25px #FFD700;
    }
    </style>

    <script>
    // نظام المؤثرات الصوتية المتطور
    function playSfx(url) {
        const audio = new Audio(url);
        audio.volume = 0.4;
        audio.play().catch(e => console.log('Audio Autoplay Blocked'));
    }

    document.addEventListener('mouseover', function(e) {
        const target = e.target.closest('label') || e.target.closest('button');
        if (target) {
            playSfx('https://www.soundjay.com/buttons/sounds/button-37a.mp3');
        }
    });
    </script>
    """, unsafe_allow_html=True)

def play_epic_sound(sound_key="select"):
    sounds = {
        "select": "https://www.soundjay.com/buttons/sounds/button-16.mp3",
        "confirm": "https://assets.mixkit.co/active_storage/sfx/2020/2020-preview.mp3",
        "next": "https://www.soundjay.com/buttons/sounds/button-10.mp3"
    }
    st.components.v1.html(f"""
        <audio autoplay><source src="{sounds[sound_key]}" type="audio/mpeg"></audio>
    """, height=0)

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
st.title("🏛️ مجمع الرؤية الاستراتيجية")
st.markdown('<p class="subtitle-text">صناعة الاستحقاق القيادي لمنظومة MR7</p>', unsafe_allow_html=True)

# شريط التقدم الذهبي
p_val = {1: 15, 2: 60, 3: 100}.get(st.session_state.v_step, 100)
st.progress(p_val)

st.markdown("<br>", unsafe_allow_html=True)

# المرحلة الأولى: اختيار التصنيف
if st.session_state.v_step == 1:
    st.markdown("<h3 style='text-align:center;'>1️⃣ اختر قطاع السيادة الكوني</h3>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        if st.button("💰\nالمالي", key="btn_money_final"):
            play_epic_sound("select")
            st.session_state.v_cat = "مالي"
            st.session_state.v_step = 2
            st.rerun()
    with c2:
        if st.button("🎓\nالتعليمي", key="btn_edu_final"):
            play_epic_sound("select")
            st.session_state.v_cat = "تعليمي"
            st.session_state.v_step = 2
            st.rerun()
    with c3:
        if st.button("✈️\nالسفر", key="btn_travel_final"):
            play_epic_sound("select")
            st.session_state.v_cat = "سفر"
            st.session_state.v_step = 2
            st.rerun()
    with c4:
        if st.button("❤️\nالعاطفي", key="btn_emo_final"):
            play_epic_sound("select")
            st.session_state.v_cat = "عاطفي"
            st.session_state.v_step = 2
            st.rerun()

# المرحلة الثانية: اختيار مستوى الطموح
elif st.session_state.v_step == 2:
    cat = st.session_state.v_cat
    st.markdown(f"<h3 style='text-align:center;'>2️⃣ مسار الـ {cat}: حدد درجتك في الهرم</h3>", unsafe_allow_html=True)
    
    levels = {
        "مالي": [
            "🌱 مستوى الـ 1M: تأمين القاعدة المالية", 
            "📈 مستوى الـ 10M: التوسع والنفوذ", 
            "🔥 مستوى الـ 100M: السيادة المطلقة", 
            "👑 مستوى المليار: نادي التريليون"
        ],
        "تعليمي": [
            "🧠 إتقان المهارات النادرة", 
            "📜 الاعتماد القيادي العالمي", 
            "🎓 درجة المرجعية (Specialized PhD)", 
            "✍️ مؤلف المناهج القيادية العالمية"
        ],
        "سفر": [
            "🧭 الاستكشاف المحلى العميق", 
            "🗺️ فتح آفاق القارات الجديدة", 
            "✈️ الطواف حول العالم لنشر الرسالة", 
            "🕊️ المهمة الكونية: ترك أثر في كل عاصمة"
        ],
        "عاطفي": [
            "❤️ التوازن العائلي والداخلي العميق", 
            "🤝 بناء شبكة علاقات النخبة العالمية", 
            "🏛️ قيادة الأثر المجتمعي الوطني", 
            "🕊️ الإرث الإنساني العابر للأجيال"
        ]
    }

    st.markdown("<div style='max-width: 850px; margin: auto;'>", unsafe_allow_html=True)
    selected = st.radio("اختر مستوى استحقاقك:", levels[cat], label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🏆 تثبيت الهدف الإمبراطوري"):
        play_epic_sound("confirm")
        st.session_state.v_goal = selected
        with st.spinner("يتم الآن نقش رؤيتك في الذاكرة الأبدية..."):
            time.sleep(3.5)
            st.session_state.v_step = 3
            st.rerun()

# المرحلة الثالثة: النتيجة النهائية
elif st.session_state.v_step == 3:
    st.balloons()
    st.markdown(f"""
    <div class="vision-card">
        <div style='font-size: 80px; margin-bottom: 20px;'>⚡</div>
        <h2 class="glitter-text">لقد وُلدت رؤية التريليون</h2>
        <p style='font-size: 38px; color: #FFFFFF; font-weight: 900; text-shadow: 0 0 20px #FFD700;'>{st.session_state.v_goal}</p>
        <div style='height: 6px; background: linear-gradient(90deg, transparent, #00FF88, transparent); margin: 35px 0;'></div>
        <p style='color: #FFFFFF; font-size: 24px; line-height: 1.8; font-weight: 600;'>
        "من هذه اللحظة، أنت قائد يمتلك بوصلة كونية. لقد أعددنا ضبط أنظمة MR7 لخدمة هذا الهدف العظيم."
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    c_back, c_next = st.columns(2)
    with c_back:
        if st.button("🔄 إعادة الصياغة"):
            play_epic_sound("select")
            st.session_state.v_step = 1
            st.rerun()
    with c_next:
        if st.button("🚀 انطلق لمركز التدريب الآن"):
            play_epic_sound("next")
            st.switch_page("pages/1_Education.py")
