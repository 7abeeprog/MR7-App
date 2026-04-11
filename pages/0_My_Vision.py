import streamlit as st
import time

# --- 1. إعدادات التصميم الإبداعي (Ultra-High Contrast Elite UI) ---
st.markdown("""
    <style>
    /* تحسين الخلفية العامة وجعلها سوداء عميقة */
    .stApp {
        background-color: #000000 !important;
    }
    
    /* ضبط ألوان القائمة الجانبية (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a !important;
        border-right: 1px solid #333 !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    [data-testid="stSidebarNav"] {
        background-color: #0a0a0a !important;
    }

    /* تحسين الخطوط العامة لتكون بيضاء ناصعة */
    div[data-testid="stMarkdownContainer"] p, h2, h3, span, label {
        color: #FFFFFF !important;
    }

    /* تصميم العنوان الرئيسي (st.title) - ذهبي ملكي متوهج وواضح جداً */
    h1 {
        background: linear-gradient(90deg, #FFD700, #FFFFFF, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 950 !important;
        text-align: center;
        filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.8));
        padding-top: 10px;
        padding-bottom: 10px;
        font-size: 3rem !important;
    }

    /* تصميم الوصف الفرعي تحت العنوان */
    .subtitle-text {
        text-align: center;
        font-size: 1.5rem !important;
        color: #FFD700 !important;
        font-weight: bold;
        text-shadow: 0 0 8px rgba(255, 215, 0, 0.5);
        margin-top: -20px;
        margin-bottom: 30px;
    }

    /* بطاقة الرؤية - تصميم زجاجي */
    .vision-card {
        background: rgba(30, 30, 30, 0.9);
        backdrop-filter: blur(25px);
        padding: 50px;
        border-radius: 40px;
        border: 2px solid #FFD700;
        box-shadow: 0 0 50px rgba(255, 215, 0, 0.25);
        margin-bottom: 30px;
        text-align: center;
    }
    
    /* نصوص براقة عالية التباين */
    .glitter-text {
        background: linear-gradient(90deg, #FFFFFF, #FFD700, #FFFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 40px;
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
    }

    /* إصلاح ألوان الاختيارات (Radio Buttons) لتعمل فوق الخلفية السوداء */
    .stRadio > div {
        gap: 20px;
        padding: 10px;
    }
    .stRadio label {
        background: #111111 !important;
        border: 2px solid #444 !important;
        padding: 25px 35px !important;
        border-radius: 20px !important;
        transition: all 0.3s ease !important;
        width: 100%;
        color: #FFFFFF !important; 
        font-weight: 900 !important;
        font-size: 20px !important;
        display: flex !important;
        align-items: center !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.8) !important;
    }
    
    .stRadio label:hover {
        border-color: #00FF88 !important;
        background: #1A1A1A !important;
        transform: scale(1.02);
        color: #00FF88 !important;
    }
    
    .stRadio div[role="radiogroup"] input:checked + label {
        border-color: #FFD700 !important;
        background: #222222 !important;
        color: #FFD700 !important;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.3) !important;
    }

    /* زر التثبيت العملاق */
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%) !important;
        color: #000000 !important;
        border: none !important;
        height: 80px !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
        box-shadow: 0 15px 40px rgba(184, 134, 11, 0.5) !important;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 60px rgba(255, 215, 0, 0.7) !important;
    }

    /* شريط التقدم */
    .stProgress > div > div > div > div {
        background-color: #FFD700;
        box-shadow: 0 0 20px #FFD700;
    }
    </style>

    <script>
    function playSfx(url) {
        const audio = new Audio(url);
        audio.volume = 0.5;
        audio.play().catch(e => console.log('Audio Blocked:', e));
    }

    document.addEventListener('mouseover', function(e) {
        const isTarget = e.target.tagName === 'LABEL' || e.target.tagName === 'BUTTON' || e.target.closest('label');
        if (isTarget) {
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
