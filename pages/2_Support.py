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
    /* الفلسفة التصميمية: استجابة سيادية فائقة السرعة */
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

    .agent-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 35px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        margin-bottom: 30px;
    }}

    /* حل مشكلة الكتابة باللون الأسود في الحقول البيضاء */
    .stTextArea textarea {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid {t['border']} !important;
        border-radius: 20px !important;
        font-weight: bold !important;
    }}

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

# --- 2. محرك السحابة (Cloud Support Sync) ---
fb_config = json.loads(st.secrets.get("__firebase_config", "{}"))
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
project_id = fb_config.get("projectId", "mr7-app")
BASE_URL = "https://firestore.googleapis.com/v1/"
TICKETS_PATH = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/public/data/support_tickets"

if 'user_id' not in st.session_state: st.session_state.user_id = str(uuid.uuid4())

def submit_ticket_to_cloud(message):
    """إرسال تذكرة دعم فني جديدة للسحابة لظهورها عند الإدارة"""
    doc_id = str(uuid.uuid4())
    payload = {
        "fields": {
            "user_id": {"stringValue": st.session_state.user_id},
            "message": {"stringValue": message},
            "status": {"stringValue": "open"},
            "timestamp": {"stringValue": datetime.now().isoformat()},
            "priority": {"stringValue": "عالية"}
        }
    }
    res = requests.post(f"{BASE_URL}{TICKETS_PATH}?documentId={doc_id}", json=payload)
    return res.status_code == 200

# --- 3. واجهة غرفة العمليات الذكية ---
st.title("💬 غرفة العمليات الذكية")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.5rem; margin-top:-20px;'>دعم سيادي لحظي لمعالجة تحديات الإمبراطورية</p>", unsafe_allow_html=True)

st.divider()

# عرض وكيل الدعم
st.markdown(f"""
<div class="agent-card">
    <div style="font-size: 60px;">🤖</div>
    <div style="color: {t['accent']}; font-size: 2rem; font-weight: 950;">أهلاً بك، أنا وكيل MR7 الذكي</div>
    <p style="font-size: 1.1rem; opacity: 0.8;">صف التحدي الذي يواجهك، وسأقوم برفع تذكرة فورية لغرفة القيادة العليا لضمان استمرارية رؤيتك.</p>
</div>
""", unsafe_allow_html=True)

# منطقة كتابة المشكلة
problem_text = st.text_area("اكتب تفاصيل التذكرة هنا:", height=150, placeholder="مثلاً: مشكلة في مزامنة الأرباح، طلب توثيق هوية، أو استفسار تقني...")

if st.button("🚀 إرسال التذكرة للسحابة فوراً"):
    if problem_text:
        with st.spinner("جاري تشفير البيانات وتوثيق التذكرة سحابياً..."):
            if submit_ticket_to_cloud(problem_text):
                st.success("تم إرسال التذكرة بنجاح! فريق العمليات سيقوم بمعالجتها خلال دقائق. ✅")
                st.balloons()
                time.sleep(2)
            else:
                st.error("حدث خطأ في الاتصال بالسحابة. يرجى المحاولة لاحقاً.")
    else:
        st.warning("الرجاء كتابة تفاصيل الطلب لضمان سرعة الاستجابة.")

st.divider()

# قسم متابعة التذاكر (Placeholder)
with st.expander("📜 تاريخ تذاكر الدعم الخاصة بك"):
    st.info("سيتم عرض حالة التذاكر المرسلة هنا فور معالجتها من قبل الأدمن في السحابة.")

if st.button("🏠 العودة لمركز القيادة الرئيسي"):
    st.switch_page("app.py")
