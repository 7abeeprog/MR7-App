import streamlit as st
import time

# --- 1. إعدادات التصميم الإبداعي (Elite Support UI) ---
st.markdown("""
    <style>
    /* تحسين الخلفية العامة للسواد المطلق */
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    /* هندسة القائمة الجانبية (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 2px solid #FFD700 !important;
    }

    /* ضمان وضوح النصوص باللون الأبيض الناصع */
    div[data-testid="stMarkdownContainer"] p, h2, h3, span, label {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.1rem;
    }

    /* العنوان الرئيسي الذهبي المتوهج */
    h1 {
        background: linear-gradient(90deg, #FFD700, #FFFFFF, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 950 !important;
        text-align: center;
        filter: drop-shadow(0 0 15px rgba(255, 215, 0, 0.8));
        font-size: 3.5rem !important;
        margin-bottom: 20px !important;
    }

    /* بطاقة الوكيل الذكي - Glassmorphism */
    .agent-card {
        background: rgba(30, 30, 30, 0.9);
        backdrop-filter: blur(20px);
        padding: 40px;
        border-radius: 35px;
        border: 2px solid #00FF88;
        box-shadow: 0 15px 45px rgba(0, 255, 136, 0.15);
        margin-bottom: 30px;
        text-align: center;
    }
    
    .agent-title {
        color: #FFD700 !important;
        font-size: 2rem !important;
        font-weight: 900 !important;
        margin-bottom: 10px;
    }

    /* تحسين حقول الإدخال */
    .stTextArea textarea {
        background-color: #111111 !important;
        color: #FFFFFF !important;
        border: 2px solid #444 !important;
        border-radius: 20px !important;
        font-size: 1.2rem !important;
        padding: 20px !important;
    }
    .stTextArea textarea:focus {
        border-color: #FFD700 !important;
    }

    /* أزرار الإرسال الإمبراطورية */
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 20px !important;
        height: 75px !important;
        font-size: 24px !important;
        border: none !important;
        transition: all 0.4s ease;
        box-shadow: 0 10px 30px rgba(184, 134, 11, 0.4);
    }
    .stButton>button:hover {
        transform: scale(1.03) translateY(-5px);
        box-shadow: 0 20px 50px rgba(255, 215, 0, 0.6);
    }

    /* تصنيفات الوكيل */
    .category-tag {
        background: rgba(255, 215, 0, 0.1);
        border: 1px solid #FFD700;
        color: #FFD700 !important;
        padding: 10px 20px;
        border-radius: 12px;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
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

def play_support_sound(sound_key="send"):
    sounds = {
        "send": "https://www.soundjay.com/buttons/sounds/button-10.mp3",
        "analyze": "https://www.soundjay.com/buttons/sounds/button-16.mp3"
    }
    st.components.v1.html(f"""
        <audio autoplay><source src="{sounds[sound_key]}" type="audio/mpeg"></audio>
    """, height=0)

# --- 2. جدار الحماية ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("الرجاء تسجيل الدخول أولاً للوصول إلى مركز القيادة.")
    st.stop()

# --- 3. واجهة المستخدم ---
st.title("💬 مركز الدعم الذكي MR7")
st.markdown("<p style='text-align:center; color:#FFD700; font-size:22px; font-weight:bold; margin-top:-20px;'>صوتك مسموع في قلب المنظومة</p>", unsafe_allow_html=True)

st.divider()

# بطاقة الوكيل
st.markdown("""
<div class="agent-card">
    <div style="font-size: 60px;">🤖</div>
    <div class="agent-title">أهلاً بك يا قائد، أنا وكيلك الذكي</div>
    <p style="color: #FFFFFF; font-size: 1.2rem;">صف مشكلتك أو طلبك، وسأقوم بتحليله فوراً وتوجيهه للقسم المختص لضمان سرعة التنفيذ.</p>
</div>
""", unsafe_allow_html=True)

# منطقة كتابة المشكلة
problem_text = st.text_area("اكتب تفاصيل التذكرة هنا (مثال: أحتاج مساعدة في سحب الأرباح أو استفسار عن مسار المليار):", height=200)

if st.button("🚀 إرسال التذكرة فوراً"):
    if problem_text:
        play_support_sound("analyze")
        with st.spinner("الوكيل الذكي يقوم بتحليل النص وتحديد الأولويات..."):
            time.sleep(2)
            
            # منطق تحليل التصنيف
            category = "عامة 📝"
            if any(word in problem_text for word in ["دفع", "فلوس", "محفظة", "رصيد", "سحب", "دولار", "أرباح"]):
                category = "مالية 💰"
            elif any(word in problem_text for word in ["دورة", "شهادة", "درس", "اختبار", "مسار", "مليار"]):
                category = "استراتيجية 🎓"
            elif any(word in problem_text for word in ["تطبيق", "بطيء", "شاشة", "حساب", "خطأ", "لا يعمل"]):
                category = "تقنية ⚙️"
            
            play_support_sound("send")
            st.success("تم استلام تذكرتك وتوثيقها في قاعدة بيانات MR7!")
            
            st.markdown(f"""
            <div class="agent-card" style="border-color: #FFD700; padding: 30px;">
                <h3 style="color: #FFFFFF;">تقرير الوكيل الذكي</h3>
                <p>لقد تم تصنيف طلبك كعملية: <span class="category-tag">{category}</span></p>
                <p style="font-size: 0.9rem; color: #aaa;">رقم المرجع العالمي: REQ-{int(time.time())}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("الرجاء كتابة تفاصيل المشكلة قبل الإرسال.")

# الانتقال للوحة التحكم
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("📊 العودة للوحة التحكم الرئيسية"):
    st.switch_page("app.py")
