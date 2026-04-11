import streamlit as st
import time

# --- 1. إعدادات التصميم الإبداعي المتطور (Elite UI & High Contrast) ---
st.markdown("""
    <style>
    /* تحسين الخلفية العامة */
    .main {
        background-color: #050505;
        color: #FFFFFF;
    }
    
    /* بطاقة الرؤية الزجاجية مع حدود ذهبية */
    .vision-card {
        background: rgba(30, 30, 30, 0.8);
        backdrop-filter: blur(15px);
        padding: 45px;
        border-radius: 35px;
        border: 2px solid rgba(255, 215, 0, 0.4);
        box-shadow: 0 25px 60px rgba(0,0,0,0.9), inset 0 0 20px rgba(255, 215, 0, 0.05);
        margin-bottom: 30px;
        text-align: center;
    }
    
    /* نصوص عالية التباين */
    .glitter-text {
        background: linear-gradient(90deg, #FFD700, #FFFFFF, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 32px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* تحسين تباين الاختيارات (Radio Buttons) */
    .stRadio > div {
        gap: 20px;
        padding: 15px;
    }
    .stRadio label {
        background: linear-gradient(145deg, #1a1a1a, #0d0d0d) !important;
        border: 1px solid #444 !important;
        padding: 20px 30px !important;
        border-radius: 18px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: 100%;
        color: #FFFFFF !important; /* لون نص أبيض واضح */
        font-weight: 600 !important;
        font-size: 18px !important;
    }
    .stRadio label:hover {
        border-color: #FFD700 !important;
        transform: scale(1.02) translateX(10px);
        box-shadow: 0 10px 20px rgba(255, 215, 0, 0.2);
    }
    
    /* زر التثبيت الإمبراطوري المتوهج */
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        color: #000 !important;
        border: none;
        height: 75px;
        font-size: 24px !important;
        font-weight: 900;
        border-radius: 22px;
        box-shadow: 0 12px 25px rgba(184, 134, 11, 0.4);
        transition: all 0.4s !important;
    }
    .stButton>button:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(255, 215, 0, 0.6);
        filter: brightness(1.2);
    }

    /* أزرار الانتقال (Next Page) */
    .next-btn>button {
        background: transparent !important;
        color: #50C878 !important;
        border: 2px solid #50C878 !important;
        margin-top: 20px;
    }

    /* شريط التقدم الذهبي */
    .stProgress > div > div > div > div {
        background-color: #FFD700;
        box-shadow: 0 0 10px #FFD700;
    }
    </style>

    <script>
    // نظام الأصوات التفاعلية بالحقن المباشر
    function playSound(url) {
        const audio = new Audio(url);
        audio.play();
    }

    // نراقب العناصر لإضافة صوت الـ Hover
    document.addEventListener('mouseover', function(e) {
        if (e.target.tagName === 'LABEL' || e.target.tagName === 'BUTTON') {
            playSound('https://www.soundjay.com/buttons/sounds/button-37a.mp3');
        }
    });
    </script>
    """, unsafe_allow_html=True)

# دالة لتشغيل أصوات محددة برمجياً
def play_audio(sound_type="select"):
    urls = {
        "select": "https://www.soundjay.com/buttons/sounds/button-09.mp3",
        "confirm": "https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3", # صوت إلهامي
        "hover": "https://www.soundjay.com/buttons/sounds/button-37a.mp3"
    }
    st.components.v1.html(f"""
        <audio autoplay><source src="{urls[sound_type]}" type="audio/mpeg"></audio>
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

# --- 4. واجهة المستخدم الإبداعية ---
st.title("🏛️ مجمع الرؤية الاستراتيجية")
st.markdown("<p style='font-size:22px; color:#FFD700; font-weight:bold;'>صمم استحقاقك القيادي في منظومة MR7</p>", unsafe_allow_html=True)

# شريط التقدم الذهبي المتوهج
p_val = {1: 15, 2: 60, 3: 100}.get(st.session_state.v_step, 100)
st.progress(p_val)

st.markdown("<br>", unsafe_allow_html=True)

# المرحلة الأولى: اختيار التصنيف
if st.session_state.v_step == 1:
    st.markdown("<h3 style='text-align:center; color: white;'>1️⃣ اختر قطاع السيادة</h3>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        if st.button("💰\nالمالي", key="btn_money"):
            play_audio("select")
            st.session_state.v_cat = "مالي"
            st.session_state.v_step = 2
            st.rerun()
    with c2:
        if st.button("🎓\nالتعليمي", key="btn_edu"):
            play_audio("select")
            st.session_state.v_cat = "تعليمي"
            st.session_state.v_step = 2
            st.rerun()
    with c3:
        if st.button("✈️\nالسفر", key="btn_travel"):
            play_audio("select")
            st.session_state.v_cat = "سفر"
            st.session_state.v_step = 2
            st.rerun()
    with c4:
        if st.button("❤️\nالعاطفي", key="btn_emo"):
            play_audio("select")
            st.session_state.v_cat = "عاطفي"
            st.session_state.v_step = 2
            st.rerun()

# المرحلة الثانية: اختيار مستوى الطموح (4 مستويات)
elif st.session_state.v_step == 2:
    cat = st.session_state.v_cat
    st.markdown(f"<h3 style='text-align:center; color: white;'>2️⃣ مسار الـ {cat}: حدد درجتك في الهرم</h3>", unsafe_allow_html=True)
    
    levels = {
        "مالي": ["🌱 مستوى الـ 1M: تأمين القاعدة المالية", "📈 مستوى الـ 10M: النفوذ الإقليمي", "🔥 مستوى الـ 100M: الهيمنة الاقتصادية", "👑 مستوى المليار: نادي التريليون العالمي"],
        "تعليمي": ["🧠 إتقان المهارات النادرة", "📜 الاعتماد القيادي الدولي", "🎓 درجة المرجعية العلمية (PhD)", "✍️ مؤلف المناهج القيادية العالمية"],
        "سفر": ["🧭 الاستكشاف المحلى العميق", "🗺️ فتح آفاق القارات الجديدة", "✈️ الطواف حول العالم لنشر الرسالة", "🕊️ المهمة الكونية: ترك أثر في كل عاصمة"],
        "عاطفي": ["❤️ التوازن العائلي والداخلي", "🤝 بناء شبكة النخبة (High-Net-Worth)", "🏛️ قيادة الأثر المجتمعي الوطني", "🕊️ الإرث الإنساني العابر للأجيال"]
    }

    st.markdown("<div style='max-width: 700px; margin: auto;'>", unsafe_allow_html=True)
    selected = st.radio("اختر مستوى استحقاقك:", levels[cat], label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🏆 تثبيت الهدف الإمبراطوري"):
        play_audio("confirm") # صوت إلهامي عند التثبيت
        st.session_state.v_goal = selected
        with st.spinner("يتم الآن نقش رؤيتك في الذاكرة الأبدية..."):
            time.sleep(2.5)
            st.session_state.v_step = 3
            st.rerun()

# المرحلة الثالثة: النتيجة بتصميم مذهل وزر الانتقال
elif st.session_state.v_step == 3:
    st.balloons()
    st.markdown(f"""
    <div class="vision-card">
        <div style='font-size: 60px; margin-bottom: 20px;'>✨</div>
        <h2 class="glitter-text">لقد ولدت رؤية جديدة</h2>
        <p style='font-size: 30px; color: #FFD700; font-weight: bold;'>{st.session_state.v_goal}</p>
        <div style='height: 3px; background: linear-gradient(90deg, transparent, #FFD700, transparent); margin: 30px 0;'></div>
        <p style='font-style: italic; color: #FFFFFF; font-size: 20px; line-height: 1.8;'>
        "من هذه اللحظة، أنت قائد يمتلك بوصلة. 
        كل ثانية من الآن يجب أن تخدم هذا الهدف العظيم. الذكاء الاصطناعي بدأ فعلياً في إعادة جدولة أولوياتك."
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 إعادة صياغة المسار"):
            st.session_state.v_step = 1
            st.rerun()
    with col_b:
        # زر الانتقال للصفحة التالية (النظام التعليمي)
        if st.button("🚀 انطلق لمركز التدريب", type="primary"):
            play_audio("select")
            st.switch_page("pages/1_Education.py")
