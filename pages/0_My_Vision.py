import streamlit as st
import time

# --- 1. إعدادات التصميم الإبداعي (Glassmorphism & Elite UI) ---
st.markdown("""
    <style>
    /* تحسين الخلفية العامة والتنسيق */
    .main {
        background-color: #050505;
    }
    
    /* تصميم بطاقة الرؤية - Glassmorphism */
    .vision-card {
        background: rgba(25, 25, 25, 0.7);
        backdrop-filter: blur(10px);
        padding: 40px;
        border-radius: 30px;
        border: 1px solid rgba(80, 200, 120, 0.3);
        box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        margin-bottom: 30px;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    /* تأثيرات للنصوص */
    .glitter-text {
        background: linear-gradient(90deg, #50C878, #FFD700, #50C878);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 28px;
    }

    /* تحسين شكل الراديو (الاختيارات) ليصبح كأنه أزرار فخمة */
    .stRadio > div {
        gap: 15px;
        padding: 10px;
    }
    .stRadio label {
        background: #151515;
        border: 1px solid #333;
        padding: 15px 25px !important;
        border-radius: 15px !important;
        transition: all 0.3s !important;
        width: 100%;
        color: #ddd !important;
    }
    .stRadio label:hover {
        border-color: #FFD700;
        background: #1a1a1a;
        transform: translateX(10px);
    }
    
    /* زر التثبيت "الإمبراطوري" */
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%);
        color: #000 !important;
        border: none;
        height: 70px;
        font-size: 22px !important;
        font-weight: 900;
        border-radius: 20px;
        letter-spacing: 1px;
        box-shadow: 0 10px 20px rgba(184, 134, 11, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 30px rgba(255, 215, 0, 0.5);
        color: #000 !important;
    }

    /* شريط التقدم الذهبي */
    .stProgress > div > div > div > div {
        background-color: #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

# دالة التأثير الصوتي المحدثة لضمان التشغيل (استخدام رابط موثوق)
def trigger_audio_v2():
    # نستخدم مكون HTML مخفي لتشغيل الصوت عند الاستدعاء
    audio_placeholder = st.empty()
    sound_url = "https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3" # صوت نجاح فاخر
    audio_placeholder.markdown(f"""
        <audio autoplay style="display:none;">
            <source src="{sound_url}" type="audio/mpeg">
        </audio>
    """, unsafe_allow_html=True)

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
st.markdown("<p style='font-size:20px; color:#aaa;'>صمم استحقاقك القيادي في منظومة MR7</p>", unsafe_allow_html=True)

# شريط التقدم الذهبي
p_val = {1: 15, 2: 60, 3: 100}.get(st.session_state.v_step, 100)
st.progress(p_val)

st.markdown("<br>", unsafe_allow_html=True)

# المرحلة الأولى: اختيار التصنيف (أزرار أيقونية)
if st.session_state.v_step == 1:
    st.markdown("<h3 style='text-align:center;'>1️⃣ اختر قطاع السيادة</h3>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        if st.button("💰\nالمالي", key="btn_money"):
            st.session_state.v_cat = "مالي"
            st.session_state.v_step = 2
            st.rerun()
    with c2:
        if st.button("🎓\nالتعليمي", key="btn_edu"):
            st.session_state.v_cat = "تعليمي"
            st.session_state.v_step = 2
            st.rerun()
    with c3:
        if st.button("✈️\nالسفر", key="btn_travel"):
            st.session_state.v_cat = "سفر"
            st.session_state.v_step = 2
            st.rerun()
    with c4:
        if st.button("❤️\nالعاطفي", key="btn_emo"):
            st.session_state.v_cat = "عاطفي"
            st.session_state.v_step = 2
            st.rerun()

# المرحلة الثانية: اختيار مستوى الطموح (4 مستويات إبداعية)
elif st.session_state.v_step == 2:
    cat = st.session_state.v_cat
    st.markdown(f"<h3 style='text-align:center;'>2️⃣ مسار القوة الـ {cat}: حدد درجتك في الهرم</h3>", unsafe_allow_html=True)
    
    levels = {
        "مالي": [
            "🌱 مستوى الـ 1M: تأمين القاعدة المالية", 
            "📈 مستوى الـ 10M: النفوذ الإقليمي", 
            "🔥 مستوى الـ 100M: الهيمنة الاقتصادية", 
            "👑 مستوى المليار: نادي التريليون العالمي"
        ],
        "تعليمي": [
            "🧠 إتقان المهارات النادرة", 
            "📜 الاعتماد القيادي الدولي", 
            "🎓 درجة المرجعية العلمية (PhD)", 
            "✍️ مؤلف المناهج القيادية العالمية"
        ],
        "سفر": [
            "🧭 الاستكشاف المحلى العميق", 
            "🗺️ فتح آفاق القارات الجديدة", 
            "✈️ الطواف حول العالم لنشر الرسالة", 
            "🕊️ المهمة الكونية: ترك أثر في كل عاصمة"
        ],
        "عاطفي": [
            "❤️ التوازن العائلي والداخلي", 
            "🤝 بناء شبكة النخبة (High-Net-Worth)", 
            "🏛️ قيادة الأثر المجتمعي الوطني", 
            "🕊️ الإرث الإنساني العابر للأجيال"
        ]
    }

    st.markdown("<div style='max-width: 600px; margin: auto;'>", unsafe_allow_html=True)
    selected = st.radio("اختر مستوى استحقاقك:", levels[cat], label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🏆 تثبيت الهدف الإمبراطوري"):
        trigger_audio_v2() # تشغيل الصوت المطور
        st.session_state.v_goal = selected
        with st.spinner("يتم الآن نقش رؤيتك في الذاكرة الأبدية..."):
            time.sleep(2)
            st.session_state.v_step = 3
            st.rerun()

# المرحلة الثالثة: النتيجة بتصميم مذهل
elif st.session_state.v_step == 3:
    st.balloons()
    st.markdown(f"""
    <div class="vision-card">
        <div style='font-size: 50px; margin-bottom: 20px;'>✨</div>
        <h2 class="glitter-text">لقد ولدت رؤية جديدة</h2>
        <p style='font-size: 26px; color: #FFD700;'><b>{st.session_state.v_goal}</b></p>
        <div style='height: 2px; background: linear-gradient(90deg, transparent, #50C878, transparent); margin: 20px 0;'></div>
        <p style='font-style: italic; color: #DAFFDE; font-size: 18px; line-height: 1.6;'>
        "من هذه اللحظة، لم تعد مجرد عضو.. أنت قائد يمتلك خارطة طريق. 
        الذكاء الاصطناعي في MR7 بدأ الآن في مواءمة الفرص والاجتماعات لتناسب هذا الاستحقاق العظيم."
        </p>
        <p style='margin-top:20px; color: #888;'>سجل الدخول يومياً لتحديث تقدمك نحو هذا الهدف.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 إعادة صياغة المسار"):
        st.session_state.v_step = 1
        st.session_state.v_cat = None
        st.session_state.v_goal = None
        st.rerun()
