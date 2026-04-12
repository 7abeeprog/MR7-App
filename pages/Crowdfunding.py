import streamlit as st
import time
from datetime import datetime
import json
import requests
import uuid
import pandas as pd

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
    /* الفلسفة التصميمية: مجمع السيولة الكوني */
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
        transition: 0.3s ease-in-out;
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

    /* حل مشكلة الكتابة باللون الأسود في الحقول البيضاء */
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

# --- 2. محرك السحابة السيادي (Live Firestore Integration) ---
fb_config = json.loads(st.secrets.get("__firebase_config", "{}"))
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
project_id = fb_config.get("projectId", "mr7-app")
BASE_URL = "https://firestore.googleapis.com/v1/"
PROJECTS_PATH = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/public/data/crowd_projects"

def fetch_live_projects():
    """جلب كافة المشاريع الاستثمارية من السحابة"""
    try:
        res = requests.get(f"{BASE_URL}{PROJECTS_PATH}")
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
    """إرسال رؤية مشروع جديدة للسحابة للمراجعة من قبل الأدمن"""
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
    res = requests.post(f"{BASE_URL}{PROJECTS_PATH}?documentId={doc_id}", json=payload)
    return res.status_code == 200

def invest_in_project(p_id, current_raised, amount):
    """تحديث مبلغ السيولة المجمعة في السحابة فور الضخ"""
    new_total = current_raised + amount
    url = f"{BASE_URL}{PROJECTS_PATH}/{p_id}?updateMask.fieldPaths=raised"
    payload = {"fields": {"raised": {"integerValue": str(new_total)}}}
    res = requests.patch(url, json=payload)
    return res.status_code == 200

# --- 3. واجهة مجمع التمويل الملياري ---
st.title("🤝 مجمع التمويل الملياري")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.4rem; margin-top:-25px;'>حوّل رؤيتك الجغرافية إلى أصول حقيقية مدعومة سحابياً</p>", unsafe_allow_html=True)

st.divider()

tabs = st.tabs(["🌎 ساحة المشاريع الحية", "🚀 طرح رؤية سيادية", "💰 محفظة أصولي", "📊 تحليلات السوق"])

# --- Tab 1: ساحة المشاريع الحية (Active Funding) ---
with tabs[0]:
    st.subheader("🌎 استكشف فرص الضخ المالي")
    live_list = fetch_live_projects()
    
    # فلترة المشاريع المعتمدة (Approved) فقط للظهور للعامة
    approved_list = [p for p in live_list if p['status'] == 'approved']
    
    if not approved_list:
        st.info("لا توجد مشاريع معتمدة حالياً للتمويل. بادر بطرح رؤيتك أو انتظر موافقة الإدارة.")
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
                
                # حساب التقدم
                progress_val = min(proj['raised']/proj['goal'], 1.0)
                st.progress(progress_val)
                
                # واجهة الضخ المالي
                with st.expander(f"💰 ضخ سيولة في {proj['title']}"):
                    fund_amount = st.number_input("مبلغ الاستثمار ($):", min_value=10, max_value=100000, value=100, key=f"amt_{proj['id']}")
                    if st.button("تأكيد الضخ المالي 🚀", key=f"btn_fund_{proj['id']}"):
                        with st.spinner("جاري مزامنة العملية مع السحابة العالمية..."):
                            if invest_in_project(proj['id'], proj['raised'], fund_amount):
                                st.success(f"تم ضخ ${fund_amount:,} بنجاح في مشروع {proj['title']}! ✅")
                                time.sleep(1)
                                st.rerun()

# --- Tab 2: طرح رؤية (Submit Vision to Cloud) ---
with tabs[1]:
    st.subheader("🚀 سجل رؤيتك في السحابة الإمبراطورية")
    st.markdown("سيتم إرسال هذا الطلب مباشرة إلى **لوحة التحكم العليا** لتدقيقه واعتماده.")
    
    with st.form("pitch_to_cloud"):
        p_title = st.text_input("اسم المشروع الاستراتيجي:")
        p_loc = st.selectbox("النطاق الجغرافي للهيمنة:", ["مصر", "ليبيا", "السودان", "عالمي"])
        p_goal = st.number_input("الميزانية التأسيسية المطلوبة ($):", min_value=1000, value=10000)
        p_desc = st.text_area("وصف الرؤية والجدوى الاقتصادية:", height=150, placeholder="اشرح للقائد الأعلى كيف سيعيد هذا المشروع تشكيل المنطقة...")
        
        if st.form_submit_button("إطلاق الرؤية للمراجعة السيادية 📤"):
            if p_title and p_desc:
                with st.spinner("جاري توثيق الرؤية في السحابة..."):
                    if submit_new_vision(p_title, p_loc, p_goal, p_desc):
                        st.success("تم إرسال الرؤية بنجاح! ستظهر لدى الإدارة فوراً.")
                        time.sleep(1.2)
                        st.rerun()
            else: st.error("يرجى إكمال البيانات الأساسية للرؤية.")

# --- Tab 3: محفظة أصولي ---
with tabs[2]:
    st.subheader("💰 أصولك الموثقة سحابياً")
    my_uid_short = st.session_state.user_id[:5]
    my_projects = [p for p in live_list if my_uid_short in p['owner']]
    
    if not my_projects:
        st.info("لم تقم بطرح مشاريع استثمارية بعد. كن مبادراً واطرح رؤيتك الآن.")
    else:
        # عرض المشاريع في جدول منظم
        report_df = pd.DataFrame(my_projects)
        report_df = report_df[['title', 'country', 'goal', 'raised', 'status']]
        report_df.columns = ['المشروع', 'الإقليم', 'المستهدف ($)', 'المجمع ($)', 'الحالة']
        st.table(report_df)

# --- Tab 4: تحليلات السوق ---
with tabs[3]:
    st.subheader("📊 ذكاء الأعمال الاستراتيجي")
    st.write("توزيع المشاريع النشطة حسب الأقاليم الجغرافية.")
    if live_list:
        geo_counts = pd.DataFrame(live_list)['country'].value_counts()
        st.bar_chart(geo_counts)
    else:
        st.write("في انتظار تدفق البيانات الحية من الأقاليم...")

st.divider()
if st.button("🏰 العودة لمركز القيادة الرئيسي"):
    st.switch_page("app.py")
