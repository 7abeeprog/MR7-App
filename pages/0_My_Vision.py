import streamlit as st
import time

# --- 1. إعدادات التصميم الإبداعي (Elite High-Contrast UI) ---
st.markdown("""
    <style>
    /* تحسين الخلفية العامة */
    .main {
        background-color: #000000 !important;
    }
    
    /* بطاقة الرؤية - تصميم زجاجي بحدود ذهبية مضيئة */
    .vision-card {
        background: rgba(25, 25, 25, 0.95);
        backdrop-filter: blur(20px);
        padding: 50px;
        border-radius: 40px;
        border: 2px solid #FFD700;
        box-shadow: 0 0 40px rgba(255, 215, 0, 0.3);
        margin-bottom: 30px;
        text-align: center;
    }
    
    /* نصوص براقة عالية التباين */
    .glitter-text {
        background: linear-gradient(90deg, #FFD700, #FFFFFF, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 40px;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
    }

    /* إصلاح ألوان الاختيارات (Radio Buttons) لتكون مرئية جداً */
    .stRadio > div {
        gap: 20px;
        padding: 10px;
    }
    .stRadio label {
        background: #1A1A1A !important;
        border: 2px solid #444 !important;
        padding: 25px 40px !important;
        border-radius: 20px !important;
        transition: all 0.3s ease !important;
        width: 100%;
        /* جعل النص أبيض ناصع ليظهر فوق الأسود */
        color: #FFFFFF !important; 
        font-weight: 800 !important;
        font-size: 22px !important;
        display: block !important;
        box-shadow: 0 4px 15px rgba(0,0,0,1) !important;
    }
    /* عند المرور فوق الخيار */
    .stRadio label:hover {
        border-color: #00FF88 !important;
        background: #222 !important;
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.4) !important;
    }
    /* عند اختيار العنصر */
    .stRadio div[role="radiogroup"] input:checked + label {
        border-color: #FFD700 !important;
        background: #2A2A2A !important;
        color: #FFD700 !important;
    }
    
    /* زر التثبيت الذهبي العملاق */
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%) !important;
        color: #000000 !important;
        border: none !important;
        height: 85px !important;
        font-size: 28px !important;
        font-weight: 900 !important;
        border-radius: 25px !important;
        box-shadow: 0 15px 40px rgba(184, 134, 11, 0.6) !important;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 60px rgba(255, 215, 0, 0.8) !important;
    }

    /* شريط التقدم الذهبي */
    .stProgress > div > div > div > div {
        background-color: #FFD700;
        box-shadow: 0 0 25px #FFD700;
    }
    </style>

    <script>
    // نظام الأصوات المطور للعمل داخل المتصفح
    function playSfx(url) {
        const audio = new Audio(url);
        audio.play().catch(e => console.log('Audio Blocked:', e));
    }

    // صوت Hover عند المرور على الأهداف
    document.addEventListener('mouseover', function(e) {
        if (e.target.tagName === 'LABEL' || e.target.tagName === 'BUTTON') {
            playSfx('https://www.soundjay.com/buttons/sounds/button-37a.mp3');
        }
    });
    </script>
    """, unsafe_allow_html=True)

# دالة لتشغيل أصوات ملهمة
def play_inspire_sound(sound_key="select"):
    sounds = {
        "select": "https://www.soundjay.com/buttons/sounds/button-16.mp3", # صوت اختيار نقي
        "confirm": "https://assets.mixkit.co/active_storage/sfx/2020/2020-preview.mp3", # صوت ملهم (Epic Success)
        "next": "https://www.soundjay.com/buttons/sounds/button-10.mp3"
    }
    st.components.v1.html(f"""
        <audio autoplay><source src="{sounds[sound_key]}" type="audio/mpeg"></audio>
    """, height=0)

# --- 2. جدار الحماية ---
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
st.markdown("<p style='font-size:24px; color:#FFD700; font-weight:bold;'>هندسة الاستحقاق القيادي لمنظومة MR7</p>", unsafe_allow_html=True)

# شريط التقدم
p_val = {1: 15, 2: 60, 3: 100}.get(st.session_state.v_step, 100)
st.progress(p_val)

st.markdown("<br>", unsafe_allow_html=True)

# المرحلة الأولى: اختيار التصنيف
if st.session_state.v_step == 1:
    st.markdown("<h3 style='text-align:center; color: white;'>1️⃣ اختر قطاع السيادة</h3>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        if st.button("💰\nالمالي", key="btn_money_v3"):
            play_inspire_sound("select")
            st.session_state.v_cat = "مالي"
            st.session_state.v_step = 2
            st.rerun()
    with c2:
        if st.button("🎓\nالتعليمي", key="btn_edu_v3"):
            play_inspire_sound("select")
            st.session_state.v_cat = "تعليمي"
            st.session_state.v_step = 2
            st.rerun()
    with c3:
        if st.button("✈️\nالسفر", key="btn_travel_v3"):
            play_inspire_sound("select")
            st.session_state.v_cat = "سفر"
            st.session_state.v_step = 2
            st.rerun()
    with c4:
        if st.button("❤️\nالعاطفي", key="btn_emo_v3"):
            play_inspire_sound("select")
            st.session_state.v_cat = "عاطفي"
            st.session_state.v_step = 2
            st.rerun()

# المرحلة الثانية: اختيار مستوى الطموح
elif st.session_state.v_step == 2:
    cat = st.session_state.v_cat
    st.markdown(f"<h3 style='text-align:center; color: white;'>2️⃣ مسار الـ {cat}: حدد درجتك في الهرم</h3>", unsafe_allow_html=True)
    
    levels = {
        "مالي": ["🌱 مستوى الـ 1M: تأمين القاعدة", "📈 مستوى الـ 10M: النفوذ الإقليمي", "🔥 مستوى الـ 100M: الهيمنة الاقتصادية", "👑 مستوى المليار: نادي التريليون"],
        "تعليمي": ["🧠 إتقان المهارات النادرة", "📜 الاعتماد القيادي الدولي", "🎓 خبير متخصص (PhD)", "✍️ مؤلف المناهج العالمية"],
        "سفر": ["🧭 الاستكشاف المحلى العميق", "🗺️ فتح آفاق القارات الجديدة", "✈️ الطواف حول العالم", "🕊️ المهمة الكونية الإنسانية"],
        "عاطفي": ["❤️ التوازن العائلي والداخلي", "🤝 شبكة علاقات النخبة", "🏛️ قيادة الأثر المجتمعي الوطني", "🕊️ الإرث الإنساني العالمي"]
    }

    st.markdown("<div style='max-width: 800px; margin: auto;'>", unsafe_allow_html=True)
    selected = st.radio("اختر مستوى استحقاقك:", levels[cat], label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🏆 تثبيت الهدف الإمبراطوري"):
        play_inspire_sound("confirm") # صوت ملهم جداً (Epic)
        st.session_state.v_goal = selected
        with st.spinner("يتم الآن نقش رؤيتك في الذاكرة الأبدية..."):
            time.sleep(3)
            st.session_state.v_step = 3
            st.rerun()

# المرحلة الثالثة: النتيجة النهائية
elif st.session_state.v_step == 3:
    st.balloons()
    st.markdown(f"""
    <div class="vision-card">
        <div style='font-size: 80px; margin-bottom: 20px;'>⚡</div>
        <h2 class="glitter-text">ولدت رؤية التريليون</h2>
        <p style='font-size: 38px; color: #FFD700; font-weight: 900;'>{st.session_state.v_goal}</p>
        <div style='height: 5px; background: linear-gradient(90deg, transparent, #00FF88, transparent); margin: 35px 0;'></div>
        <p style='font-style: italic; color: #FFFFFF; font-size: 24px; line-height: 1.8; font-weight: 500;'>
        "يا قائد.. هذا الهدف ليس حلماً، بل هو خطة عمل تبدأ من هذه اللحظة. 
        لقد أعدنا ضبط بوصلة التطبيق لتوجهك نحو هذا الاستحقاق العظيم."
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    c_back, c_next = st.columns(2)
    with c_back:
        if st.button("🔄 إعادة الصياغة"):
            play_inspire_sound("select")
            st.session_state.v_step = 1
            st.rerun()
    with c_next:
        if st.button("🚀 انطلق لمركز التدريب الآن"):
            play_inspire_sound("next")
            st.switch_page("pages/1_Education.py")
