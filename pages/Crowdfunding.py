import streamlit as st
import time
import json
import requests
import uuid
from datetime import datetime

# --- 1. إعدادات التصميم الإبداعي الفائق ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 2px solid #FFD700 !important;
    }
    div[data-testid="stMarkdownContainer"] p, h2, h3, span, label {
        color: #FFFFFF !important;
        font-weight: 600;
    }
    h1 {
        background: linear-gradient(90deg, #FFD700, #FFFFFF, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 950 !important;
        text-align: center;
        filter: drop-shadow(0 0 12px rgba(255, 215, 0, 0.9));
        font-size: 3.5rem !important;
    }
    .subtitle-text {
        text-align: center;
        font-size: 1.7rem !important;
        color: #FFD700 !important;
        font-weight: 800;
        margin-bottom: 40px;
    }
    .vision-card {
        background: rgba(20, 20, 20, 0.95);
        padding: 55px;
        border-radius: 45px;
        border: 2px solid #FFD700;
        box-shadow: 0 0 60px rgba(255, 215, 0, 0.3);
        margin-bottom: 30px;
        text-align: center;
    }
    .glitter-text {
        background: linear-gradient(90deg, #FFFFFF, #FFD700, #FFFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 42px;
    }
    .stRadio label {
        background: #0a0a0a !important;
        border: 2px solid #333 !important;
        padding: 25px !important;
        border-radius: 20px !important;
        color: #FFFFFF !important; 
        font-weight: 900 !important;
        font-size: 20px !important;
        margin-bottom: 10px;
        display: flex !important;
    }
    .stRadio div[role="radiogroup"] input:checked + label {
        border-color: #FFD700 !important;
        background: #1a1a1a !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%) !important;
        color: #000000 !important;
        height: 80px !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        border-radius: 25px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك السحابة السيادي (Cloud Vision Sync) ---
fb_config = json.loads(st.secrets.get("__firebase_config", "{}"))
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
project_id = fb_config.get("projectId", "mr7-app")
BASE_URL = "https://firestore.googleapis.com/v1/"

if 'user_id' not in st.session_state: st.session_state.user_id = str(uuid.uuid4())

def save_vision_to_cloud(category, goal):
    """تخزين الرؤية الاستراتيجية في السحابة"""
    path = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/users/{st.session_state.user_id}/strategic_vision/vision_doc"
    payload = {
        "fields": {
            "category": {"stringValue": category},
            "goal": {"stringValue": goal},
            "timestamp": {"stringValue": datetime.now().isoformat()},
            "status": {"stringValue": "active"}
        }
    }
    # استخدام patch لإنشاء أو تحديث الوثيقة
    requests.patch(f"{BASE_URL}{path}", json=payload)

def fetch_vision_from_cloud():
    """جلب الرؤية المحفوظة"""
    path = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/users/{st.session_state.user_id}/strategic_vision/vision_doc"
    try:
        res = requests.get(f"{BASE_URL}{path}")
        if res.status_code == 200:
            f = res.json().get("fields", {})
            return f.get("category", {}).get("stringValue"), f.get("goal", {}).get("stringValue")
        return None, None
    except: return None, None

# --- 3. إدارة الحالة الواجهة ---
if 'v_step' not in st.session_state:
    saved_cat, saved_goal = fetch_vision_from_cloud()
    if saved_goal:
        st.session_state.v_step = 3
        st.session_state.v_cat = saved_cat
        st.session_state.v_goal = saved_goal
    else:
        st.session_state.v_step = 1

# --- 4. واجهة مجمع الرؤية ---
st.title("🏛️ مجمع الرؤية الاستراتيجية")
st.markdown('<p class="subtitle-text">نقش أهداف السيادة في السحابة الإمبراطورية</p>', unsafe_allow_html=True)

# شريط التقدم
p_val = {1: 30, 2: 70, 3: 100}.get(st.session_state.v_step, 100)
st.progress(p_val / 100)

if st.session_state.v_step == 1:
    st.markdown("<h3 style='text-align:center;'>1️⃣ اختر قطاع الهيمنة</h3>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    sectors = [("💰\nالمالي", "مالي"), ("🎓\nالتعليمي", "تعليمي"), ("✈️\nالسفر", "سفر"), ("❤️\nالعاطفي", "عاطفي")]
    
    for i, (label, val) in enumerate(sectors):
        with [c1, c2, c3, c4][i]:
            if st.button(label, key=f"sec_{val}"):
                st.session_state.v_cat = val
                st.session_state.v_step = 2
                st.rerun()

elif st.session_state.v_step == 2:
    cat = st.session_state.v_cat
    st.markdown(f"<h3 style='text-align:center;'>2️⃣ حدد درجة الاستحقاق في مسار {cat}</h3>", unsafe_allow_html=True)
    
    options = {
        "مالي": ["🌱 مستوى الـ 1M: القاعدة", "📈 مستوى الـ 10M: التوسع", "🔥 مستوى الـ 100M: السيادة", "👑 مستوى المليار: نادي التريليون"],
        "تعليمي": ["🧠 إتقان المهارات", "📜 الاعتماد العالمي", "🎓 المرجعية العلمية", "✍️ مؤلف المناهج العالمية"],
        "سفر": ["🧭 الاستكشاف المحلي", "🗺️ فتح القارات", "✈️ الطواف العالمي", "🕊️ المهمة الكونية"],
        "عاطفي": ["❤️ التوازن الداخلي", "🤝 شبكة النخبة", "🏛️ الأثر المجتمعي", "🕊️ الإرث الإنساني"]
    }
    
    selected = st.radio("اختر هدفك:", options[cat], label_visibility="collapsed")
    
    if st.button("🏆 تثبيت الهدف ونقشه سحابياً"):
        with st.spinner("جاري التواصل مع الخزنة السحابية..."):
            save_vision_to_cloud(cat, selected)
            st.session_state.v_goal = selected
            time.sleep(2)
            st.session_state.v_step = 3
            st.rerun()

elif st.session_state.v_step == 3:
    st.balloons()
    st.markdown(f"""
    <div class="vision-card">
        <div style='font-size: 70px;'>⚡</div>
        <h2 class="glitter-text">رؤيتك موثقة سحابياً</h2>
        <p style='font-size: 32px; color: #FFD700; font-weight: 900;'>{st.session_state.v_goal}</p>
        <hr style='opacity: 0.2; margin: 30px 0;'>
        <p style='font-size: 1.2rem; line-height: 1.6;'>
        "تم تسجيل رؤيتك في السجلات الإمبراطورية. سيقوم نظام الذكاء الاصطناعي الآن بتوجيه كافة موارد MR7 لدعمك في تحقيق هذا الهدف."
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    c_rev, c_edu = st.columns(2)
    with c_rev:
        if st.button("🔄 صياغة الرؤية من جديد"):
            st.session_state.v_step = 1
            st.rerun()
    with c_edu:
        if st.button("🚀 انطلق للأكاديمية التعليمية"):
            st.switch_page("pages/1_Education.py")

st.divider()
if st.button("🏠 العودة لمركز القيادة"):
    st.switch_page("app.py")
