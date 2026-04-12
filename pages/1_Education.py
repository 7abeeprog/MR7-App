import streamlit as st
import time
from datetime import datetime, date
import json
import requests
import uuid

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

    .journey-counter {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 25px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.1);
    }}
    .days-number {{
        font-size: 5rem !important;
        font-weight: 900 !important;
        color: {t['accent']} !important;
        line-height: 1;
    }}

    .course-card {{
        background: rgba(25, 25, 25, 0.95);
        padding: 40px;
        border-radius: 35px;
        border: 2px solid #00FF88;
        box-shadow: 0 10px 40px rgba(0, 255, 136, 0.1);
        margin-bottom: 30px;
        transition: 0.3s;
    }}
    .course-card:hover {{ transform: translateY(-5px); border-color: {t['accent']}; }}

    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 20px !important;
        height: 70px;
        font-size: 1.2rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك السحابة (Education Cloud Integration) ---
fb_config = json.loads(st.secrets.get("__firebase_config", "{}"))
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
project_id = fb_config.get("projectId", "mr7-app")
BASE_URL = "https://firestore.googleapis.com/v1/"

if 'user_id' not in st.session_state: st.session_state.user_id = str(uuid.uuid4())

def get_user_edu_data():
    """جلب بيانات التقدم التعليمي من السحابة"""
    path = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/users/{st.session_state.user_id}/education_data/main"
    try:
        res = requests.get(f"{BASE_URL}{path}")
        if res.status_code == 200:
            f = res.json().get("fields", {})
            return {
                "xp": int(f.get("xp", {}).get("integerValue", 0)),
                "progress": int(f.get("progress", {}).get("integerValue", 0)),
                "start_date": f.get("start_date", {}).get("stringValue", datetime.now().strftime("%Y-%m-%d"))
            }
        return {"xp": 0, "progress": 0, "start_date": "2026-03-27"}
    except: return {"xp": 0, "progress": 0, "start_date": "2026-03-27"}

def update_edu_progress(new_xp, new_prog):
    """تحديث التقدم التعليمي في السحابة"""
    path = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/users/{st.session_state.user_id}/education_data/main"
    payload = {
        "fields": {
            "xp": {"integerValue": str(new_xp)},
            "progress": {"integerValue": str(new_prog)},
            "last_active": {"stringValue": datetime.now().isoformat()}
        }
    }
    requests.patch(f"{BASE_URL}{path}?updateMask.fieldPaths=xp&updateMask.fieldPaths=progress", json=payload)

# --- 3. واجهة الأكاديمية التعليمية ---
st.title("🎓 مركز التميز القيادي")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.5rem; margin-top:-20px;'>نحو هندسة عقلية المليار دولار</p>", unsafe_allow_html=True)

# جلب البيانات الحية
edu_data = get_user_edu_data()

# حساب رحلة الـ 100 يوم
s_date = datetime.strptime(edu_data['start_date'], "%Y-%m-%d").date()
days_passed = (date.today() - s_date).days
days_left = max(0, 100 - days_passed)

st.markdown(f"""
<div class="journey-counter">
    <div style="text-transform: uppercase; letter-spacing: 2px;">يوم متبقي في رحلة الـ 100 يوم للسيادة</div>
    <div class="days-number">{days_left}</div>
    <div style="color: #00FF88; font-weight: 800; margin-top: 10px;">تم اجتياز {days_passed}% من المسار التاريخي</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# شريط التقدم التعليمي
st.subheader("📈 مستوى تطورك القيادي الموثق")
st.progress(edu_data['progress'] / 100)
st.markdown(f"<p style='font-size:1.2rem;'>لقد أنجزت <span style='color:#00FF88; font-size:1.6rem;'>{edu_data['progress']}%</span> من مسار 'تأسيس القيادة الإمبراطورية'.</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# الأقسام الدراسية
col_c1, col_c2 = st.columns(2)

with col_c1:
    st.markdown(f"""
    <div class="course-card">
        <h3 style='color:#FFD700; margin-bottom:15px; font-size: 1.8rem;'>عقلية المليار 🧠</h3>
        <p>12 درس مرئي - 5 مشاريع تطبيقية</p>
        <p style='color:#00FF88; font-weight:900; font-size:1.5rem;'>XP المتوفر: {edu_data['xp']}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("متابعة بناء العقلية 📖"):
        with st.spinner("جاري حفظ التقدم في السحابة..."):
            update_edu_progress(edu_data['xp'] + 150, min(100, edu_data['progress'] + 5))
            st.success("تم تسجيل حضورك! +150 XP")
            time.sleep(1)
            st.rerun()

with col_c2:
    st.markdown(f"""
    <div class="course-card" style="border-color: #FFD700;">
        <h3 style='color:#FFD700; margin-bottom:15px; font-size: 1.8rem;'>القيادة الخضراء 🌍</h3>
        <p>8 دروس استراتيجية - أثر مستدام</p>
        <p style='color:#FF4B4B; font-weight:900; font-size:1.5rem;'>لم يتم البدء بعد</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("بدء المسار البيئي 🚀"):
        st.info("سيتم فتح المسار قريباً...")

st.divider()

# العودة
if st.button("🏠 العودة لمركز القيادة الرئيسي"):
    st.switch_page("app.py")
