import streamlit as st
import time
from datetime import datetime
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
        filter: drop-shadow(0 0 12px {t['accent']}); 
        font-size: 3.5rem !important; 
    }}

    .project-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 30px;
        padding: 35px;
        margin-bottom: 30px;
        box-shadow: 0 15px 45px rgba(0,0,0,0.5);
    }}
    .project-card:hover {{ border-color: #00FF88; transform: translateY(-5px); }}

    .country-tag {{
        background: rgba(0, 255, 136, 0.1);
        color: #00FF88 !important;
        border: 1px solid #00FF88;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 900;
    }}

    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid {t['border']} !important;
        border-radius: 12px !important;
        font-weight: bold !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 20px !important;
        height: 60px;
        font-size: 1.1rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك السحابة السيادي (Cloud Sync Engine) ---
fb_config = json.loads(st.secrets.get("__firebase_config", "{}"))
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
project_id = fb_config.get("projectId", "mr7-app")
BASE_URL = "https://firestore.googleapis.com/v1/"
PATH = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/public/data/crowd_projects"

def fetch_live_projects():
    """جلب كافة المشاريع من السحابة"""
    try:
        res = requests.get(f"{BASE_URL}{PATH}")
        if res.status_code == 200:
            docs = res.json().get("documents", [])
            items = []
            for doc in docs:
                f = doc.get("fields", {})
                items.append({
                    "id": doc["name"].split("/")[-1],
                    "title": f.get("title", {}).get("stringValue", "غير مسمى"),
                    "country": f.get("country", {}).get("stringValue", "عالمي"),
                    "desc": f.get("desc", {}).get("stringValue", ""),
                    "goal": int(f.get("goal", {}).get("integerValue", 0)),
                    "raised": int(f.get("raised", {}).get("integerValue", 0)),
                    "roi": f.get("roi", {}).get("stringValue", "15%"),
                    "status": f.get("status", {}).get("stringValue", "pending"),
                    "owner": f.get("owner", {}).get("stringValue", "مجهول")
                })
            return items
        return []
    except: return []

def submit_new_vision(title, country, goal, desc):
    """إرسال رؤية مشروع جديدة للسحابة للمراجعة"""
    doc_id = str(uuid.uuid4())
    payload = {
        "fields": {
            "title": {"stringValue": title},
            "country": {"stringValue": country},
            "goal": {"integerValue": str(goal)},
            "raised": {"integerValue": "0"},
            "desc": {"stringValue": desc},
            "roi": {"stringValue": "20%"},
            "status": {"stringValue": "pending"},
            "owner": {"stringValue": f"القائد ({st.session_state.user_id[:5]})"},
            "timestamp": {"stringValue": datetime.now().isoformat()}
        }
    }
    res = requests.post(f"{BASE_URL}{PATH}?documentId={doc_id}", json=payload)
    return res.status_code == 200

# --- 3. واجهة مجمع التمويل الملياري ---
st.title("🤝 مجمع التمويل الملياري")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.4rem; margin-top:-25px;'>حوّل رؤيتك الجغرافية إلى أصول حقيقية مدعومة سحابياً</p>", unsafe_allow_html=True)

st.divider()

tabs = st.tabs(["🌎 ساحة المشاريع الحية", "🚀 طرح رؤية سيادية", "💰 محفظة أصولي", "📊 تحليلات السوق"])

# --- Tab 1: ساحة المشاريع الحية ---
with tabs[0]:
    st.subheader("🌎 استكشف فرص الضخ المالي")
    live_list = fetch_live_projects()
    
    # فلترة المشاريع المعتمدة فقط للظهور في الساحة العامة
    approved_list = [p for p in live_list if p['status'] == 'approved']
    
    if not approved_list:
        st.info("لا توجد مشاريع معتمدة حالياً. قم بطرح رؤيتك في التبويب التالي!")
    else:
        for proj in approved_list:
            with st.container():
                st.markdown(f"""
                <div class="project-card">
                    <div style="display: flex; justify-content: space-between;">
                        <span class="country-tag">📍 {proj['country']}</span>
                        <span style="color: #00FF88;">العائد المتوقع: {proj['roi']}</span>
                    </div>
                    <h2 style="color: {t['accent']}; margin: 15px 0;">{proj['title']}</h2>
                    <p style="color: #ddd; line-height: 1.8;">{proj['desc']}</p>
                    
                    <div style="display: flex; justify-content: space-between; margin: 15px 0; background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px;">
                        <div>
                            <p style="color: #888; font-size: 0.8rem; margin: 0;">المستهدف</p>
                            <span style="font-size: 1.3rem;">${proj['goal']:,}</span>
                        </div>
                        <div style="text-align: right;">
                            <p style="color: #888; font-size: 0.8rem; margin: 0;">تم جمع</p>
                            <span style="font-size: 1.3rem; color: #00FF88;">${proj['raised']:,}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(min(proj['raised']/proj['goal'], 1.0))
                if st.button(f"🤝 ضخ سيادي في {proj['title']}", key=f"fund_{proj['id']}"):
                    st.success("سيتم توجيهك لبوابة الدفع الموثقة...")

# --- Tab 2: طرح رؤية (Submit to Cloud) ---
with tabs[1]:
    st.subheader("🚀 سجل رؤيتك في السحابة الإمبراطورية")
    st.markdown("سيتم إرسال هذا الطلب مباشرة إلى 'لوحة التحكم العليا' لتدقيقه من قبل الأدمن.")
    
    with st.form("pitch_to_cloud"):
        p_title = st.text_input("اسم المشروع الاستراتيجي:")
        p_loc = st.selectbox("النطاق الجغرافي:", ["مصر", "ليبيا", "السودان", "عالمي"])
        p_goal = st.number_input("الميزانية التأسيسية المطلوبة ($):", min_value=1000, value=10000)
        p_desc = st.text_area("وصف الرؤية والجدوى الاقتصادية:", height=150)
        
        if st.form_submit_button("إطلاق الرؤية للمراجعة 📤"):
            if p_title and p_desc:
                with st.spinner("جاري المزامنة مع مركز القيادة..."):
                    if submit_new_vision(p_title, p_loc, p_goal, p_desc):
                        st.success("تم إرسال الرؤية بنجاح! ستظهر لدى الأدمن فوراً للموافقة عليها.")
                        time.sleep(1)
                        st.rerun()
            else: st.error("يرجى إكمال البيانات.")

# --- Tab 3: أصولي ---
with tabs[2]:
    st.subheader("💰 أصولك الموثقة سحابياً")
    my_projects = [p for p in live_list if st.session_state.user_id[:5] in p['owner']]
    if not my_projects:
        st.info("لم تقم بطرح مشاريع بعد.")
    else:
        st.table(pd.DataFrame(my_projects).drop(columns=['id', 'desc']))

st.divider()
if st.button("🏰 العودة لمركز القيادة الرئيسي"):
    st.switch_page("app.py")
