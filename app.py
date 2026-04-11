import streamlit as st
import hashlib

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

# إعداد شكل الصفحة (يجب أن يكون أول سطر بعد الاستدعاء)
st.set_page_config(page_title="MR7 Super App", page_icon="🚀", layout="wide")

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# إعداد ذاكرة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# شاشة تسجيل الدخول
if st.session_state['logged_in'] == False:
    st.title("مرحباً بك في منصة MR7 🚀")
    st.write("الرجاء تسجيل الدخول للوصول إلى الأنظمة.")
    
    email = st.text_input("أدخل بريدك الإلكتروني:")
    password = st.text_input("أدخل كلمة المرور:", type="password")
    
    if st.button("تسجيل الدخول"):
        if password:
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.warning("الرجاء إدخال كلمة المرور أولاً.")

# الشاشة الرئيسية بعد الدخول
else:
    st.title("لوحة تحكم MR7 📊")
    st.success("مرحباً بك مجدداً!")
    
    # توجيه المستخدم للقائمة الجانبية
    st.write("### 👈 **استخدم القائمة الجانبية للتنقل بين أنظمة التطبيق.**")
    st.info("إحصائيات سريعة: لديك 10 أعضاء في فريقك، و 50 نقطة في نظام الجيميفيكيشن.")
    
    st.divider()
    if st.button("تسجيل الخروج"):
        st.session_state['logged_in'] = False
        st.rerun()
