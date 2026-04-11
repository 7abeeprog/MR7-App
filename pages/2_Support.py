import streamlit as st
import time

# --- 1. محرك الأنماط (Theme Engine) ---
# التأكد من وجود متغير النمط في ذاكرة الجلسة
if 'app_theme' not in st.session_state:
    st.session_state.app_theme = "غامق إمبراطوري 🖤"

# تعريف الألوان لكل نمط
themes = {
    "غامق إمبراطوري 🖤": {
        "bg": "#000000", "sidebar": "#050505", "text": "#FFFFFF", 
        "accent": "#FFD700", "card": "rgba(30, 30, 30, 0.9)", "border": "#FFD700"
    },
    "فاتح ملكي ✨": {
        "bg": "#F5F5F5", "sidebar": "#FFFFFF", "text": "#1A1A1A", 
        "accent": "#B8860B", "card": "rgba(255, 255, 255, 0.95)", "border": "#B8860B"
    },
    "أزرق القيادة 💙": {
        "bg": "#001F3F", "sidebar": "#001529", "text": "#FFFFFF", 
        "accent": "#0074D9", "card": "rgba(0, 31, 63, 0.8)", "border": "#0074D9"
    },
    "أخضر الاستدامة 💚": {
        "bg": "#002B1B", "sidebar": "#001A10", "text": "#FFFFFF", 
        "accent": "#00FF88", "card": "rgba(0, 43, 27, 0.8)", "border": "#00FF88"
    }
}

selected_theme = st.session_state.app_theme
t = themes[selected_theme]

# تطبيق التصميم بناءً على النمط المختار
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {t['bg']} !important;
        color: {t['text']} !important;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: {t['sidebar']} !important;
        border-right: 2px solid {t['accent']} !important;
    }}

    div[data-testid="stMarkdownContainer"] p, h2, h3, span, label, li {{
        color: {t['text']} !important;
        font-weight: 700 !important;
    }}

    h1 {{
        background: linear-gradient(90deg, {t['accent']}, {t['text']}, {t['accent']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 950 !important;
        text-align: center;
        filter: drop-shadow(0 0 10px {t['accent']});
        font-size: 3rem !important;
    }}

    .agent-card {{
        background: {t['card']};
        backdrop-filter: blur(20px);
        padding: 40px;
        border-radius: 35px;
        border: 2px solid {t['border']};
        box-shadow: 0 15px 45px rgba(0,0,0,0.5);
        margin-bottom: 30px;
        text-align: center;
    }}
    
    .stTextArea textarea {{
        background-color: rgba(255,255,255,0.05) !important;
        color: {t['text']} !important;
        border: 2px solid {t['border']} !important;
        border-radius: 20px !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 20px !important;
        height: 70px !important;
        font-size: 22px !important;
        border: none !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. القائمة الجانبية لإعدادات النمط ---
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

# --- 3. جدار الحماية ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("الرجاء تسجيل الدخول أولاً للوصول إلى مركز القيادة.")
    st.stop()

# --- 4. واجهة المستخدم ---
st.title("💬 مركز الدعم الذكي MR7")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:20px; font-weight:bold; margin-top:-20px;'>نحن هنا لخدمة رؤيتك وتذليل العقبات</p>", unsafe_allow_html=True)

st.divider()

# بطاقة الوكيل
st.markdown(f"""
<div class="agent-card">
    <div style="font-size: 60px;">🤖</div>
    <div style="color: {t['accent']}; font-size: 2rem; font-weight: 900;">أهلاً بك، أنا وكيلك الذكي</div>
    <p>صف مشكلتك وسنقوم بحلها فوراً لضمان استمرار رحلتك نحو التريليون.</p>
</div>
""", unsafe_allow_html=True)

# منطقة كتابة المشكلة
problem_text = st.text_area("اكتب تفاصيل التذكرة هنا:", height=150)

if st.button("🚀 إرسال الطلب فوراً"):
    if problem_text:
        with st.spinner("جاري التحليل..."):
            time.sleep(1.5)
            st.success("تم استلام تذكرتك بنجاح وتوثيقها في النظام!")
            st.balloons()
    else:
        st.warning("الرجاء كتابة تفاصيل الطلب.")

# العودة
st.markdown("<br>", unsafe_allow_html=True)
if st.button("📊 العودة للرئيسية"):
    st.switch_page("app.py")
