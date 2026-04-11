import streamlit as st
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
    .stApp {{ background-color: {t['bg']} !important; color: {t['text']} !important; }}
    [data-testid="stSidebar"] {{ background-color: {t['sidebar']} !important; border-right: 2px solid {t['accent']} !important; }}
    
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
        font-size: 3.2rem !important; 
    }}

    .notification-card {{
        background: {t['card']};
        border-left: 5px solid {t['accent']};
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    
    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 15px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات ---
if 'notifications' not in st.session_state:
    st.session_state.notifications = []

# --- 3. واجهة مركز التنبيهات ---
st.title("🔔 مركز التنبيهات الإمبراطوري")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.3rem; margin-top:-20px;'>سجل الأحداث والعمليات لسيادتكم</p>", unsafe_allow_html=True)

st.divider()

col_actions, col_empty = st.columns([1, 2])
with col_actions:
    if st.button("🗑️ مسح جميع التنبيهات"):
        st.session_state.notifications = []
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

if not st.session_state.notifications:
    st.info("صندوق التنبيهات خالٍ حالياً. سيتم إخطارك هنا بأي أحداث هامة.")
else:
    for n in st.session_state.notifications:
        st.markdown(f"""
        <div class="notification-card">
            <div style="font-size: 2.5rem;">{n['icon']}</div>
            <div style="flex-grow: 1;">
                <div style="font-size: 1.2rem; font-weight: bold;">{n['msg']}</div>
                <div style="color: #888; font-size: 0.9rem;">{n['time']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()
if st.button("🏠 العودة للوحة التحكم"):
    st.switch_page("app.py")
