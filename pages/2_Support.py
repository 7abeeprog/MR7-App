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

    .ticket-card {{
        background: rgba(255, 255, 255, 0.03);
        border-right: 5px solid {t['accent']};
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }}

    .status-badge {{
        padding: 4px 12px;
        border-radius: 10px;
        font-size: 0.85rem;
        font-weight: 900;
        text-transform: uppercase;
    }}

    /* تخصيص مظهر الدردشة */
    .chat-bubble-user {{
        background: {t['accent']};
        color: black !important;
        padding: 15px;
        border-radius: 20px 20px 0 20px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
    }}

    .chat-bubble-ai {{
        background: rgba(255,255,255,0.08);
        color: white !important;
        padding: 15px;
        border-radius: 20px 20px 20px 0;
        margin: 10px 0;
        max-width: 80%;
        border-left: 3px solid #00FF88;
    }}

    /* حل مشكلة الكتابة باللون الأسود في الحقول البيضاء */
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] {{
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

# --- 2. محرك السحابة والذكاء الاصطناعي (Cloud & AI Core) ---
fb_config = json.loads(st.secrets.get("__firebase_config", "{}"))
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
project_id = fb_config.get("projectId", "mr7-app")
apiKey = "" # يتم توفيره تلقائياً في البيئة
BASE_URL = "https://firestore.googleapis.com/v1/"
TICKETS_PATH = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/public/data/support_tickets"

if 'user_id' not in st.session_state: st.session_state.user_id = str(uuid.uuid4())

def get_ai_support_advice(query):
    """استخدام Gemini لتقديم دعم فني فوري أولي"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={apiKey}"
    payload = {
        "contents": [{
            "parts": [{ "text": f"You are the MR7 Imperial Support Agent. The user says: '{query}'. Provide a brief, supportive, and professional response in Arabic as a first-line support bot. Help them feel empowered." }]
        }]
    }
    
    # Exponential Backoff Logic
    for delay in [1, 2, 4, 8, 16]:
        try:
            res = requests.post(url, json=payload, timeout=10)
            if res.status_code == 200:
                result = res.json()
                return result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "أنا هنا لدعمك يا قائد، جاري رفع استفسارك للإدارة.")
        except:
            time.sleep(delay)
    return "نظام الذكاء الاصطناعي قيد التحديث، سأقوم برفع تذكرتك للإدارة مباشرة."

def submit_ticket_to_cloud(message, category, priority):
    """إرسال تذكرة دعم فني احترافية للسحابة"""
    doc_id = str(uuid.uuid4())
    ai_advice = get_ai_support_advice(message)
    payload = {
        "fields": {
            "user_id": {"stringValue": st.session_state.user_id},
            "message": {"stringValue": message},
            "category": {"stringValue": category},
            "priority": {"stringValue": priority},
            "status": {"stringValue": "قيد المراجعة"},
            "timestamp": {"stringValue": datetime.now().isoformat()},
            "ai_first_response": {"stringValue": ai_advice},
            "admin_reply": {"stringValue": "لم يتم الرد من قبل الإدارة بعد."}
        }
    }
    res = requests.post(f"{BASE_URL}{TICKETS_PATH}?documentId={doc_id}", json=payload)
    return res.status_code == 200, ai_advice

def fetch_user_tickets():
    """جلب تاريخ التذاكر الخاص بالمستخدم"""
    try:
        res = requests.get(f"{BASE_URL}{TICKETS_PATH}")
        if res.status_code == 200:
            docs = res.json().get("documents", [])
            user_notis = []
            for doc in docs:
                f = doc.get("fields", {})
                if f.get("user_id", {}).get("stringValue") == st.session_state.user_id:
                    user_notis.append({
                        "msg": f.get("message", {}).get("stringValue", ""),
                        "cat": f.get("category", {}).get("stringValue", "عام"),
                        "pri": f.get("priority", {}).get("stringValue", "عادية"),
                        "status": f.get("status", {}).get("stringValue", "مفتوحة"),
                        "time": f.get("timestamp", {}).get("stringValue", ""),
                        "ai": f.get("ai_first_response", {}).get("stringValue", ""),
                        "reply": f.get("admin_reply", {}).get("stringValue", "")
                    })
            return sorted(user_notis, key=lambda x: x['time'], reverse=True)
        return []
    except: return []

# --- 3. واجهة غرفة العمليات الذكية 2.0 ---
st.title("💬 غرفة العمليات الذكية")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.5rem; margin-top:-20px;'>مركز الاستجابة السيادي المدعوم بالذكاء الاصطناعي</p>", unsafe_allow_html=True)

st.divider()

# عرض وكيل الدعم الفخم
st.markdown(f"""
<div class="agent-card">
    <div style="font-size: 70px;">🤖</div>
    <div style="color: {t['accent']}; font-size: 2.2rem; font-weight: 950; margin-top:10px;">MR7 AI Sentinel</div>
    <p style="font-size: 1.1rem; opacity: 0.8; margin-top:15px;">أنا رادارك الخاص لمواجهة التحديات. صف مشكلتك وسأقوم بحلها أو رفعها لمجلس القيادة فوراً.</p>
</div>
""", unsafe_allow_html=True)

# نظام إرسال التذاكر المتقدم
with st.container():
    st.markdown("### 📝 فتح برقية دعم جديدة")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        category = st.selectbox("تصنيف التحدي:", ["مشكلة تقنية", "استفسار مالي", "توثيق رتبة", "اقتراح تطوير"])
    with col_t2:
        priority = st.select_slider("درجة الأولوية:", options=["عادية", "متوسطة", "عاجلة 🔥"], value="عادية")
    
    problem_text = st.text_area("تفاصيل التذكرة السيادية:", height=120, placeholder="اشرح لنا بوضوح ما يواجهك لنتمكن من خدمتك بأفضل شكل...")

    if st.button("🚀 إرسال وبدء المعالجة الذكية"):
        if problem_text:
            with st.spinner("جاري تحليل المشكلة بالذكاء الاصطناعي وتوثيقها سحابياً..."):
                success, ai_resp = submit_ticket_to_cloud(problem_text, category, priority)
                if success:
                    st.success("تم التوثيق! إليك الرد الأولي من الوكيل الذكي:")
                    st.markdown(f'<div class="chat-bubble-ai"><b>🤖 الوكيل الذكي:</b><br>{ai_resp}</div>', unsafe_allow_html=True)
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("فشل الاتصال بمركز العمليات السحابي.")
        else:
            st.warning("يرجى كتابة تفاصيل التحدي للمتابعة.")

st.divider()

# نظام متابعة التذاكر (Professional Threading)
st.markdown("### 📜 سجل المتابعة والحلول الحية")
my_tickets = fetch_user_tickets()

if not my_tickets:
    st.info("لا توجد تذاكر نشطة حالياً. الإمبراطورية تعمل بانتظام.")
else:
    for ticket in my_tickets:
        # تحديد الألوان بناءً على الحالة
        status_map = {"قيد المراجعة": "#FFD700", "مرفوضة": "#FF4B4B", "مغلقة": "#00FF88", "قيد المعالجة": "#0074D9"}
        s_color = status_map.get(ticket['status'], "#888")
        
        with st.expander(f"📍 {ticket['cat']} | {ticket['msg'][:40]}..."):
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                <span style="opacity:0.6;">📅 {ticket['time'][:16].replace('T', ' ')}</span>
                <span class="status-badge" style="background:{s_color}; color:black;">{ticket['status']}</span>
            </div>
            <div class="chat-bubble-user">
                <b>👤 طلبك:</b><br>{ticket['msg']}
            </div>
            <div class="chat-bubble-ai">
                <b>🤖 الرد الأولي (AI):</b><br>{ticket['ai']}
            </div>
            <div style="background: rgba(0,255,136,0.05); padding: 15px; border-radius: 15px; border: 1px dashed #00FF88; margin-top: 10px;">
                <b>🏛️ قرار الإدارة السيادي:</b><br>{ticket['reply']}
            </div>
            """, unsafe_allow_html=True)

st.divider()

# اختصارات سريعة للعودة
if st.button("🏠 العودة لمركز القيادة الرئيسي"):
    st.switch_page("app.py")
