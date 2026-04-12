import streamlit as st
import time
import uuid
import json
import requests
from datetime import datetime
import base64

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
        filter: drop-shadow(0 0 15px {t['accent']}); 
        font-size: 3.5rem !important; 
    }}

    .profile-cover {{
        height: 280px;
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1510511459019-5dee997ddfdf?auto=format&fit=crop&q=80&w=2070') center/cover;
        border-radius: 40px 40px 0 0;
        border: 2px solid {t['accent']};
        border-bottom: none;
    }}

    .elite-header {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 0 0 50px 50px;
        padding: 0 50px 40px 50px;
        text-align: center;
        margin-top: -100px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.8);
    }}

    .avatar-glow {{
        width: 190px; height: 190px;
        border-radius: 50%;
        border: 6px solid {t['accent']};
        box-shadow: 0 0 45px {t['accent']};
        margin-bottom: 20px;
        background: #111;
        object-fit: cover;
    }}

    .stat-tile {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        transition: 0.3s;
    }}
    .stat-tile:hover {{ border-color: #00FF88; transform: translateY(-5px); }}

    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid {t['border']} !important;
        border-radius: 12px !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 20px !important;
        height: 60px;
    }}

    .noti-badge {{
        background: #FF4B4B;
        color: white;
        padding: 2px 8px;
        border-radius: 50%;
        font-size: 0.8rem;
        position: relative;
        top: -10px;
        right: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات الحية (Live Integration) ---
fb_config = json.loads(st.secrets.get("__firebase_config", "{}"))
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
project_id = fb_config.get("projectId", "mr7-app")
BASE_URL = "https://firestore.googleapis.com/v1/"

if 'user_id' not in st.session_state: st.session_state.user_id = str(uuid.uuid4())
if 'leader_name' not in st.session_state: st.session_state.leader_name = "القائد الإمبراطوري"
if 'user_rank' not in st.session_state: st.session_state.user_rank = "قائد استراتيجي 💎"

def get_notifications_count():
    """محاكاة لجلب عدد التنبيهات غير المقروءة من السحابة"""
    return 4 # مثال ثابت

# --- 3. الشريط الجانبي ---
with st.sidebar:
    st.markdown(f"### 🎨 تخصيص المنظومة")
    theme_choice = st.selectbox("نمط الواجهة:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    
    with st.expander("👤 إدارة الهوية الرقمية"):
        st.session_state.leader_name = st.text_input("اسم الشهرة العالمي:", st.session_state.leader_name)
        st.file_uploader("رفع ختم الصورة الشخصية:", type=["png", "jpg", "jpeg"])
        if st.button("تأكيد وتوثيق الهوية"):
            st.success("تم تحديث السجلات!")
            time.sleep(1)
            st.rerun()

# --- 4. واجهة ملف القائد (The Masterpiece) ---
st.markdown('<div class="profile-cover"></div>', unsafe_allow_html=True)

# رأس البروفايل
display_avatar = f"https://api.dicebear.com/7.x/avataaars/svg?seed={st.session_state.user_id}"
st.markdown(f"""
<div class="elite-header">
    <img src="{display_avatar}" class="avatar-glow">
    <h2 style="color: {t['accent']}; font-size: 3rem; margin-bottom: 5px;">{st.session_state.leader_name}</h2>
    <div style="display: flex; justify-content: center; gap: 15px; margin-top: 15px;">
        <span style="background: {t['accent']}; color: black; padding: 6px 20px; border-radius: 50px; font-weight: 950;">{st.session_state.user_rank}</span>
        <span style="background: #00FF88; color: black; padding: 6px 20px; border-radius: 50px; font-weight: 950;">موثق ✅</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# صف الأزرار التفاعلية
col_n1, col_n2, col_n3 = st.columns([1, 1, 1])
with col_n1:
    if st.button(f"🔔 التنبيهات ({get_notifications_count()})"):
        st.switch_page("pages/10_Notifications.py")

# الإحصائيات
st.subheader("📈 لوحة مؤشرات السيادة")
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
with col_stat1: st.markdown(f'<div class="stat-tile"><small>صافي الثروة</small><br><span style="font-size:1.8rem; color:#00FF88;">$1.25M</span></div>', unsafe_allow_html=True)
with col_stat2: st.markdown(f'<div class="stat-tile"><small>جيش القادة</small><br><span style="font-size:1.8rem; color:{t["accent"]};">12,450</span></div>', unsafe_allow_html=True)
with col_stat3: st.markdown(f'<div class="stat-tile"><small>قوة التأثير</small><br><span style="font-size:1.8rem;">98%</span></div>', unsafe_allow_html=True)
with col_stat4: st.markdown(f'<div class="stat-tile"><small>معدل التضاعف</small><br><span style="font-size:1.8rem; color:#FF4B4B;">X10</span></div>', unsafe_allow_html=True)

st.divider()

tabs = st.tabs(["🏛️ ميثاق الرؤية", "🏆 جدار الأوسمة", "💬 تنبيهات حية", "⚙️ هندسة الظهور"])

with tabs[0]:
    st.markdown(f"""
    <div style="background: {t['card']}; padding: 35px; border-radius: 30px; border: 2px solid {t['accent']};">
        <h3 style="color: {t['accent']};">بوصلة التريليون الموثقة</h3>
        <p style="font-size: 1.5rem; line-height: 1.8;">"أقسمت أن أقود فريقاً نحو الحرية المالية المطلقة، وبناء نظام تعليمي يغير وجه المنطقة العربية تجارياً."</p>
    </div>
    """, unsafe_allow_html=True)

with tabs[1]:
    st.subheader("🏅 خزنة الاستحقاقات")
    st.markdown("🥇 باني الإمبراطورية | 🧠 مهندس العقول | 🌍 عابر الحدود")

with tabs[2]:
    st.subheader("🔔 آخر التنبيهات المستلمة")
    # عرض مختصر للتنبيهات الحية
    st.markdown("""
    <div style="background: rgba(255,215,0,0.05); padding: 15px; border-radius: 15px; border-right: 5px solid #FFD700; margin-bottom: 10px;">
        <b>💰 عمولة جديدة:</b> تم إيداع $500 من الجيل الثاني. <br> <small>منذ 10 دقائق</small>
    </div>
    <div style="background: rgba(0,255,136,0.05); padding: 15px; border-radius: 15px; border-right: 5px solid #00FF88; margin-bottom: 10px;">
        <b>🏆 ترقية:</b> رتبتك القادمة "إمبراطور ماسي" تقترب! <br> <small>منذ ساعة</small>
    </div>
    """, unsafe_allow_html=True)
    if st.button("فتح مركز التنبيهات الكامل 🚀"):
        st.switch_page("pages/10_Notifications.py")

with tabs[3]:
    st.subheader("⚙️ هندسة الظهور العالمي")
    st.text_input("قاعدة العمليات الجغرافية (GEO):", "New Cairo, Egypt")

st.divider()
c_nav1, c_nav2, c_nav3, c_nav4 = st.columns(4)
with c_nav1:
    if st.button("💰 الخزنة المالية"): st.switch_page("pages/3_Wallet.py")
with c_nav2:
    if st.button("👥 جيش القادة"): st.switch_page("pages/6_Teams.py")
with c_nav3:
    if st.button("🛒 المتجر العالمي"): st.switch_page("pages/4_Marketplace.py")
with c_nav4:
    if st.button("🏠 الرئيسية"): st.switch_page("app.py")
