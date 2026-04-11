import streamlit as st
import time

# --- 1. إعدادات التصميم الإبداعي الفائق (Neon Elite UI & High Contrast) ---
st.markdown("""
    <style>
    /* تحسين الخلفية العامة والخطوط */
    .main {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* بطاقة الرؤية الزجاجية - توهج زمردي وذهبي */
    .vision-card {
        background: rgba(20, 20, 20, 0.9);
        backdrop-filter: blur(20px);
        padding: 50px;
        border-radius: 40px;
        border: 2px solid #FFD700;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.2), inset 0 0 15px rgba(80, 200, 120, 0.1);
        margin-bottom: 30px;
        text-align: center;
    }
    
    /* نصوص براقة عالية التباين جداً */
    .glitter-text {
        background: linear-gradient(90deg, #FFD700, #00FF88, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 36px;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }

    /* تحسين تباين الاختيارات (Radio Buttons) لتكون واضحة تماماً */
    .stRadio > div {
        gap: 25px;
        padding: 20px;
    }
    .stRadio label {
        background: #111111 !important;
        border: 2px solid #333 !important;
        padding: 25px 35px !important;
        border-radius: 20px !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: 100%;
        color: #00FF88 !important; /* لون أخضر نيون للوضوح العالي */
        font-weight: 800 !important;
        font-size: 20px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    .stRadio label:hover {
        border-color: #FFD700 !important;
        background: #1a1a1a !important;
        transform: scale(1.03) translateY(-5px);
        box-shadow: 0 10px 25px rgba(255, 215, 0, 0.3);
        color: #FFFFFF !important;
    }
    
    /* زر التثبيت الإمبراطوري المتوهج */
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%) !important;
        color: #000000 !important;
        border: none !important;
        height: 80px !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        border-radius: 25px !important;
        box-shadow: 0 15px 35px rgba(184, 134, 11, 0.5) !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .stButton>button:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 50px rgba(255, 215, 0, 0.7) !important;
        filter: brightness(1.2);
    }

    /* شريط التقدم الذهبي اللامع */
    .stProgress > div > div > div > div {
        background-color: #FFD700;
        box-shadow: 0 0 20px #FFD700;
    }

    /* تحسين الأزرار الجانبية */
    .stButton.primary-btn > button {
        background: #00FF88 !important;
        color: #000 !important;
    }
    </style>

    <script>
    // نظام الأصوات المطور
    function playSfx(url) {
        const audio = new Audio(url);
        audio.volume = 0.5;
        audio.play().catch(e => console.log('Audio error:', e));
    }

    // صوت الـ Hover عند المرور على الأهداف أو الأزرار
    document.addEventListener('mouseover', function(e) {
        const target = e.target.closest('label') || e.target.closest('button');
        if (target) {
            playSfx('https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3'); // صوت Hover قصير واحترافي
        }
    });
    </script>
    """, unsafe_allow_html=True)

# دالة لتشغيل أصوات محددة برمجياً
def play_audio_feedback(sound_key="select"):
    sounds = {
        "select": "https://www.soundjay.com/buttons/sounds/button-16.mp3", # صوت اختيار نقي
        "confirm": "https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3", # صوت ملهم (Success Fanfare)
        "next": "https://www.soundjay.com/buttons/sounds/button-3.mp3"
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

# --- 4. واجهة المستخدم الإبداعية ---
st.title("🏛️ مجمع الرؤية الاستراتيجية")
st.markdown("<p style='font-size:24px; color:#FFD700; font-weight:bold; text-shadow: 0 0 10px rgba(255,215,0,0.3);'>صمم استحقاقك القيادي في منظومة MR7</p>", unsafe_allow_html=True)

# شريط التقدم الذهبي
p_val = {1: 15, 2: 60, 3: 100}.get(st.session_state.v_step, 100)
st.progress(p_val)

st.markdown("<br>", unsafe_allow_html=True)

# المرحلة الأولى: اختيار التصنيف
if st.session_state.v_step == 1:
    st.markdown("<h3 style='text-align:center; color: white; margin-bottom: 30px;'>1️⃣ اختر قطاع السيادة</h3>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        if st.button("💰\nالمالي", key="btn_money_v2"):
            play_audio_feedback("select")
            st.session_state.v_cat = "مالي"
            st.session_state.v_step = 2
            st.rerun()
    with c2:
        if st.button("🎓\nالتعليمي", key="btn_edu_v2"):
            play_audio_feedback("select")
            st.session_state.v_cat = "تعليمي"
            st.session_state.v_step = 2
            st.rerun()
    with c3:
        if st.button("✈️\nالسفر", key="btn_travel_v2"):
            play_audio_feedback("select")
            st.session_state.v_cat = "سفر"
            st.session_state.v_step = 2
            st.rerun()
    with c4:
        if st.button("❤️\nالعاطفي", key="btn_emo_v2"):
            play_audio_feedback("select")
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

    st.markdown("<div style='max-width: 750px; margin: auto;'>", unsafe_allow_html=True)
    selected = st.radio("اختر مستوى استحقاقك:", levels[cat], label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🏆 تثبيت الهدف الإمبراطوري"):
        play_audio_feedback("confirm") # صوت إلهامي جداً عند التثبيت
        st.session_state.v_goal = selected
        with st.spinner("يتم الآن نقش رؤيتك في الذاكرة الأبدية..."):
            time.sleep(3)
            st.session_state.v_step = 3
            st.rerun()

# المرحلة الثالثة: النتيجة النهائية وزر الانتقال
elif st.session_state.v_step == 3:
    st.balloons()
    st.markdown(f"""
    <div class="vision-card">
        <div style='font-size: 70px; margin-bottom: 20px;'>✨</div>
        <h2 class="glitter-text">لقد ولدت رؤية جديدة</h2>
        <p style='font-size: 34px; color: #00FF88; font-weight: 900; text-shadow: 0 0 15px rgba(0,255,136,0.4);'>{st.session_state.v_goal}</p>
        <div style='height: 4px; background: linear-gradient(90deg, transparent, #FFD700, transparent); margin: 35px 0;'></div>
        <p style='font-style: italic; color: #FFFFFF; font-size: 22px; line-height: 1.8; font-weight: 500;'>
        "من هذه اللحظة، أنت قائد يمتلك بوصلة كونية. 
        كل ثانية من الآن يجب أن تخدم هذا الهدف العظيم. الذكاء الاصطناعي بدأ فعلياً في إعادة هندسة واقعك."
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_x, col_y = st.columns(2)
    with col_x:
        if st.button("🔄 إعادة صياغة المسار"):
            play_audio_feedback("select")
            st.session_state.v_step = 1
            st.rerun()
    with col_y:
        # زر الانتقال للصفحة التالية (النظام التعليمي) بتصميم بارز
        if st.button("🚀 انطلق لمركز التدريب الآن"):
            play_audio_feedback("next")
            st.switch_page("pages/1_Education.py")
