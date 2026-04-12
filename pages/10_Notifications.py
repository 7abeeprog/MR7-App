import streamlit as st
import time
import json
import requests
import uuid
from datetime import datetime

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
        font-size: 3.5rem !important; 
    }}

    .noti-card {{
        background: {t['card']};
        border-right: 6px solid {t['accent']};
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        transition: 0.3s ease;
    }}
    .noti-card:hover {{ transform: scale(1.02); border-right-color: #00FF88; }}
    
    .noti-badge-type {{
        background: {t['accent']};
        color: #000 !important;
        padding: 2px 10px;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 950;
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

# --- 2. محرك قاعدة البيانات (Live Firestore REST) ---
fb_config = json.loads(st.secrets.get("__firebase_config", "{}"))
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
project_id = fb_config.get("projectId", "mr7-app")
BASE_URL = "https://firestore.googleapis.com/v1/"

if 'user_id' not in st.session_state: st.session_state.user_id = str(uuid.uuid4())

def fetch_live_notifications():
    """جلب التنبيهات من مسار المستخدم الخاص"""
    path = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/users/{st.session_state.user_id}/notifications"
    try:
        res = requests.get(f"{BASE_URL}{path}")
        if res.status_code == 200:
            docs = res.json().get("documents", [])
            notis = []
            for doc in docs:
                f = doc.get("fields", {})
                notis.append({
                    "id": doc["name"].split("/")[-1],
                    "msg": f.get("msg", {}).get("stringValue", ""),
                    "type": f.get("type", {}).get("stringValue", "عام"),
                    "icon": f.get("icon", {}).get("stringValue", "🔔"),
                    "time": f.get("time", {}).get("stringValue", "غير معروف")
                })
            return sorted(notis, key=lambda x: x['time'], reverse=True)
        return []
    except: return []

# --- 3. واجهة مركز التنبيهات ---
st.title("🔔 مركز التنبيهات الإمبراطوري")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.4rem; margin-top:-25px;'>نظام المتابعة السيادية اللحظية</p>", unsafe_allow_html=True)

st.divider()

# جلب البيانات الحية
live_notis = fetch_live_notifications()

# في حال عدم وجود بيانات حية، نعرض بيانات افتراضية للتوضيح
if not live_notis:
    live_notis = [
        {"id": "1", "msg": "تم إيداع عمولة بقيمة $500 من مبيعات الجيل الثاني.", "type": "مالي", "icon": "💰", "time": "10:30 AM"},
        {"id": "2", "msg": "طلب تمويل جديد لمشروعك 'مدينة النبت' ينتظر المراجعة.", "type": "تمويل", "icon": "🤝", "time": "09:15 AM"},
        {"id": "3", "msg": "تهانينا! لقد حققت رتبة 'قائد استراتيجي' بنجاح.", "type": "نظام", "icon": "🏆", "time": "أمس"}
    ]

col_f, col_a = st.columns([2, 1])
with col_f:
    filter_type = st.selectbox("تصفية التنبيهات:", ["الكل", "مالي", "تمويل", "نظام"])
with col_a:
    st.write("") # مباعدة
    if st.button("🔄 تحديث"): st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

display_list = live_notis if filter_type == "الكل" else [n for n in live_notis if n['type'] == filter_type]

for n in display_list:
    st.markdown(f"""
    <div class="noti-card">
        <div style="font-size: 3rem;">{n['icon']}</div>
        <div style="flex-grow: 1;">
            <span class="noti-badge-type">{n['type']}</span>
            <div style="font-size: 1.2rem; font-weight: 800;">{n['msg']}</div>
            <div style="color: #888; font-size: 0.85rem; margin-top: 5px;">📅 {n['time']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
if st.button("🏠 العودة لمركز القيادة"):
    st.switch_page("app.py")
