import streamlit as st
from datetime import datetime
import time

# --- 1. محرك الأنماط الشامل (Theme Engine) ---
if 'app_theme' not in st.session_state:
    st.session_state.app_theme = "غامق إمبراطوري 🖤"

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

st.markdown(f"""
    <style>
    /* التنسيق العام */
    .stApp {{
        background-color: {t['bg']} !important;
        color: {t['text']} !important;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: {t['sidebar']} !important;
        border-right: 2px solid {t['accent']} !important;
    }}

    div[data-testid="stMarkdownContainer"] p, h2, h3, h4, span, label, li {{ 
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
        font-size: 3.5rem !important; 
    }}

    /* بطاقة التنبيه الاحترافية */
    .notification-card {{
        background: {t['card']};
        border-left: 6px solid {t['accent']};
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        transition: 0.3s ease;
    }}
    .notification-card:hover {{
        transform: scale(1.02);
        border-left-color: #00FF88;
    }}
    
    .noti-type {{
        background: {t['accent']};
        color: #000 !important;
        padding: 2px 10px;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 900;
        margin-bottom: 5px;
        display: inline-block;
    }}

    /* إصلاح مدخلات القوائم المنسدلة */
    div[data-baseweb="select"] > div {{
        background-color: {t['select_bg']} !important;
        color: {t['select_text']} !important;
    }}
    div[data-baseweb="popover"] li {{
        color: {t['select_text']} !important;
        background-color: {t['select_bg']} !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 15px !important;
        height: 55px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات (Notification Storage) ---
if 'notifications' not in st.session_state or len(st.session_state.notifications) == 0:
    st.session_state.notifications = [
        {"msg": "تم إيداع عمولة جديدة بقيمة $500 من الجيل الثاني.", "time": "10:30 AM", "icon": "💰", "type": "مالي"},
        {"msg": "مشروعك 'مزرعة الهيدروبونيك' حصل على تمويل جديد!", "time": "09:15 AM", "icon": "🤝", "type": "تمويل"},
        {"msg": "تمت ترقية رتبتك إلى 'قائد استراتيجي' بنجاح.", "time": "أمس", "icon": "🏆", "type": "نظام"},
        {"msg": "مرحباً بك في مركز التنبيهات الإمبراطوري MR7.", "time": "2026-04-10", "icon": "🔔", "type": "ترحيب"}
    ]

# --- 3. واجهة مركز التنبيهات ---
st.title("🔔 مركز التنبيهات الإمبراطوري")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.3rem; margin-top:-20px;'>نظام المتابعة اللحظية لإمبراطورية MR7</p>", unsafe_allow_html=True)

st.divider()

# أدوات التحكم في التنبيهات
col_filter, col_actions = st.columns([2, 1])

with col_filter:
    category = st.selectbox("تصفية التنبيهات حسب النوع:", ["الكل", "مالي", "تمويل", "نظام"])

with col_actions:
    st.write("") # مسافة تجميلية
    if st.button("🗑️ مسح السجل بالكامل"):
        st.session_state.notifications = []
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# عرض التنبيهات بناءً على الفلتر
display_list = st.session_state.notifications if category == "الكل" else [n for n in st.session_state.notifications if n['type'] == category]

if not display_list:
    st.info(f"لا توجد تنبيهات جديدة في قسم '{category}' حالياً.")
else:
    for n in display_list:
        st.markdown(f"""
        <div class="notification-card">
            <div style="font-size: 3rem;">{n['icon']}</div>
            <div style="flex-grow: 1;">
                <span class="noti-type">{n['type']}</span>
                <div style="font-size: 1.3rem; font-weight: 800; color: {t['text']};">{n['msg']}</div>
                <div style="color: #888; font-size: 0.95rem; margin-top: 5px;">📅 {n['time']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# العودة
col_back, col_home = st.columns(2)
with col_back:
    if st.button("🏠 العودة للرئيسية"):
        st.switch_page("app.py")
with col_home:
    if st.button("🤝 مجمع التمويل الجماعي"):
        st.switch_page("pages/9_Crowdfunding.py")
