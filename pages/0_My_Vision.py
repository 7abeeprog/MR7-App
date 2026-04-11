import streamlit as st
import time

# --- 1. إعدادات التصميم الإبداعي (Ultra-High Contrast Elite UI) ---
st.markdown("""
    <style>
    /* تحسين الخلفية العامة وجعل الخطوط بيضاء تماماً */
    .main {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    /* جعل كل النصوص الافتراضية بيضاء باستثناء العنوان الرئيسي */
    div[data-testid="stMarkdownContainer"] p, h2, h3, span {
        color: #FFFFFF !important;
    }

    /* تصميم خاص للعنوان الرئيسي (st.title) ليصبح ذهبياً متوهجاً */
    h1 {
        background: linear-gradient(90deg, #FFD700, #FFFFFF, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 950 !important;
        text-align: center;
        filter: drop-shadow(0 0 15px rgba(255, 215, 0, 0.6));
        padding-bottom: 20px;
    }

    /* بطاقة الرؤية - تصميم زجاجي بحدود ذهبية مضيئة */
    .vision-card {
        background: rgba(30, 30, 30, 0.9);
        backdrop-filter: blur(25px);
        padding: 60px;
        border-radius: 40px;
        border: 2px solid #FFD700;
        box-shadow: 0 0 50px rgba(255, 215, 0, 0.25);
        margin-bottom: 30px;
        text-align: center;
    }
    
    /* نصوص براقة عالية التباين (أبيض مع توهج ذهبي) */
    .glitter-text {
        background: linear-gradient(90deg, #FFFFFF, #FFD700, #FFFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 45px;
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
    }

    /* إصلاح ألوان الاختيارات (Radio Buttons) لتكون بيضاء وواضحة جداً */
    .stRadio > div {
        gap: 25px;
        padding: 15px;
    }
    .stRadio label {
        background: #111111 !important;
        border: 2px solid #444 !important;
        padding: 30px 45px !important;
        border-radius: 20px !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: 100%;
        color: #FFFFFF !important; 
        font-weight: 900 !important;
        font-size: 24px !important;
        display: flex !important;
        align-items: center !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.8) !important;
    }
    
    .stRadio label:hover {
        border-color: #00FF88 !important;
        background: #1A1A1A !important;
        transform: scale(1.03) translateX(5px);
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.3) !important;
        color: #00FF88 !important;
    }
    
    .stRadio div[role="radiogroup"] input:checked + label {
        border-color: #FFD700 !important;
        background: #222222 !important;
        color: #FFD700 !important;
        box-shadow: 0 0 40px rgba(255, 215, 0, 0.4) !important;
    }

    div[data-testid="stMarkdownContainer"] [data-testid="stWidgetLabel"] {
        color: #FFFFFF !important;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%) !important;
        color: #000000 !important;
        border: none !important;
        height: 90px !important;
        font-size: 30px !important;
        font-weight: 900 !important;
        border-radius: 25px !important;
        box-shadow: 0 20px 50px rgba(184, 134, 11, 0.5) !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .stButton>button:hover {
        transform: translateY(-12px);
        box-shadow: 0 30px 70px rgba(255, 215, 0, 0.7) !important;
        filter: brightness(1.1);
    }

    .stProgress > div > div > div > div {
        background-color: #FFD700;
        box-shadow: 0 0 30px #FFD700;
    }
    </style>

    <script>
    function playSfx(url) {
        const audio = new Audio(url);
        audio.volume = 0.6;
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

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("الرجاء تسجيل الدخول من الصفحة الرئيسية أولاً.")
    st.stop()

if 'v_step' not in st.session_state:
    st.session_state.v_step = 1
    st.session_state.v_cat = None
    st.session_state.v_goal = None

st.title("🏛️ مجمع الرؤية الاستراتيجية")
st.markdown("<p style='text-align:center; font-size:26px; color:#FFD700; font-weight:bold; text-shadow: 0 0 10px rgba(255,215,0,0.4);'>صناعة الاستحقاق القيادي لمنظومة MR7</p>", unsafe_allow_html=True)

p_val = {1: 15, 2: 60, 3: 100}.get(st.session_state.v_step, 100)
st.progress(p_val)

st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.v_step == 1:
    st.markdown("<h3 style='text-align:center; color: #FFFFFF;'>1️⃣ اختر قطاع السيادة الكوني</h3>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        if st.button("💰\nالمالي", key="btn_money_v4"):
            play_epic_sound("select")
            st.session_state.v_cat = "مالي"
            st.session_state.v_step = 2
            st.rerun()
    with c2:
        if st.button("🎓\nالتعليمي", key="btn_edu_v4"):
            play_epic_sound("select")
            st.session_state.v_cat = "تعليمي"
            st.session_state.v_step = 2
            st.rerun()
    with c3:
        if st.button("✈️\nالسفر", key="btn_travel_v4"):
            play_epic_sound("select")
            st.session_state.v_cat = "سفر"
            st.session_state.v_step = 2
            st.rerun()
    with c4:
        if st.button("❤️\nالعاطفي", key="btn_emo_v4"):
            play_epic_sound("select")
            st.session_state.v_cat = "عاطفي"
            st.session_state.v_step = 2
            st.rerun()

elif st.session_state.v_step == 2:
    cat = st.session_state.v_cat
    st.markdown(f"<h3 style='text-align:center; color: #FFFFFF;'>2️⃣ مسار الـ {cat}: حدد درجتك في الهرم</h3>", unsafe_allow_html=True)
    
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

elif st.session_state.v_step == 3:
    st.balloons()
    st.markdown(f"""
    <div class="vision-card">
        <div style='font-size: 100px; margin-bottom: 20px;'>✨</div>
        <h2 class="glitter-text">لقد وُلدت رؤية التريليون</h2>
        <p style='font-size: 42px; color: #FFFFFF; font-weight: 900; text-shadow: 0 0 20px #FFD700;'>{st.session_state.v_goal}</p>
        <div style='height: 6px; background: linear-gradient(90deg, transparent, #00FF88, transparent); margin: 40px 0;'></div>
        <p style='color: #FFFFFF; font-size: 26px; line-height: 1.8; font-weight: 600; background: rgba(0,0,0,0.3); padding: 20px; border-radius: 15px;'>
        "من هذه اللحظة، أنت قائد يمتلك خارطة طريق كونية. 
        لقد أعدنا ضبط بوصلة التطبيق لتوجهك نحو هذا الاستحقاق العظيم بكل قوة."
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_back, col_next = st.columns(2)
    with col_back:
        if st.button("🔄 إعادة الصياغة"):
            play_epic_sound("select")
            st.session_state.v_step = 1
            st.rerun()
    with col_next:
        if st.button("🚀 انطلق لمركز التدريب الآن"):
            play_epic_sound("next")
            st.switch_page("pages/1_Education.py")
