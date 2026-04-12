import streamlit as st
import time
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
    div[data-testid="stMarkdownContainer"] p, h2, h3, span, label, li {{ color: {t['text']} !important; font-weight: 700 !important; }}
    h1 {{ background: linear-gradient(90deg, {t['accent']}, {t['text']}, {t['accent']}); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 950 !important; text-align: center; filter: drop-shadow(0 0 10px {t['accent']}); font-size: 3.5rem !important; }}
    
    .market-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .market-card:hover {{ border-color: #00FF88; transform: scale(1.03); box-shadow: 0 10px 30px rgba(0,255,136,0.2); }}
    
    .vendor-badge {{
        background: {t['accent']};
        color: #000 !important;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 900;
    }}

    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: bold !important;
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

# --- 2. محرك قاعدة البيانات الحية (Live Firestore Logic) ---
fb_config = json.loads(st.secrets.get("__firebase_config", "{}"))
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
project_id = fb_config.get("projectId", "mr7-app")

BASE_URL = "https://firestore.googleapis.com/v1/"
COLLECTION_PATH = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/public/data/marketplace_products"

def fetch_live_products():
    """جلب كافة المنتجات الموثقة من السحابة"""
    try:
        res = requests.get(f"{BASE_URL}{COLLECTION_PATH}")
        if res.status_code == 200:
            docs = res.json().get("documents", [])
            items = []
            for doc in docs:
                fields = doc.get("fields", {})
                items.append({
                    "id": doc["name"].split("/")[-1],
                    "name": fields.get("name", {}).get("stringValue", "منتج غير مسمى"),
                    "price": fields.get("price", {}).get("integerValue", "0"),
                    "vendor": fields.get("vendor", {}).get("stringValue", "تاجر MR7"),
                    "tag": fields.get("tag", {}).get("stringValue", "نخبة"),
                    "img": fields.get("img", {}).get("stringValue", "https://images.unsplash.com/photo-1554224155-169641357599?w=500&q=80")
                })
            return items
        return []
    except: return []

def submit_live_product(name, price, desc, cat, vendor):
    """إرسال منتج جديد للسحابة العالمية"""
    doc_id = str(uuid.uuid4())
    payload = {
        "fields": {
            "name": {"stringValue": name},
            "price": {"integerValue": str(price)},
            "desc": {"stringValue": desc},
            "cat": {"stringValue": cat},
            "vendor": {"stringValue": vendor},
            "tag": {"stringValue": "تاجر جديد"},
            "time": {"stringValue": datetime.now().isoformat()}
        }
    }
    res = requests.post(f"{BASE_URL}{COLLECTION_PATH}?documentId={doc_id}", json=payload)
    return res.status_code == 200

# --- 3. إدارة الجلسة والهوية ---
if 'store_name' not in st.session_state:
    st.session_state.store_name = "إمبراطورية التجارة"

# --- 4. واجهة المركز التجاري العالمي ---
st.title("MR7 Global Marketplace")

tab1, tab2, tab3, tab4 = st.tabs(["🌎 السوق العالمي", "🏗️ لوحة التاجر", "🔗 متجري الشخصي", "🧠 أكاديمية التجار"])

# --- Tab 1: السوق العالمي (Live Feed) ---
with tab1:
    st.markdown(f"<p style='text-align:center; font-size: 1.2rem;'>منتجات حية من قادة الاقتصاد الجديد</p>", unsafe_allow_html=True)
    
    live_items = fetch_live_products()
    
    if not live_items:
        st.info("جاري مزامنة المنتجات مع السحابة العالمية...")
        # منتجات افتراضية في حالة فشل الاتصال
        live_items = [
            {"name": "هندسة النظم المالية", "vendor": "أكاديمية MR7", "price": 499, "tag": "إمبراطوري", "img": "https://images.unsplash.com/photo-1554224155-169641357599?w=500&q=80"},
            {"name": "كوتشينج المليار", "vendor": "القائد المؤسس", "price": 1200, "tag": "نخبة", "img": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=500&q=80"}
        ]

    rows = [live_items[i:i + 3] for i in range(0, len(live_items), 3)]
    for row in rows:
        cols = st.columns(3)
        for i, item in enumerate(row):
            with cols[i]:
                st.markdown(f"""
                <div class="market-card">
                    <img src="{item.get('img', '')}" style="width:100%; border-radius:15px; margin-bottom:10px;">
                    <span class="vendor-badge">{item['tag']}</span>
                    <h3 style="margin-top:10px;">{item['name']}</h3>
                    <p style="color: #aaa; font-size: 0.8rem;">بواسطة: {item['vendor']}</p>
                    <div style="color: #00FF88; font-size: 1.8rem; font-weight: 900;">${int(item['price']):,}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"اقتناء 🛒", key=f"buy_{item['id'] if 'id' in item else i}"):
                    st.success("تمت العملية بنجاح!")

# --- Tab 2: لوحة التاجر (Live Insertion) ---
with tab2:
    st.header("🏗️ مركز إدارة المحتوى التجاري")
    with st.form("live_product_form"):
        p_name = st.text_input("اسم المنتج الاستراتيجي:")
        p_price = st.number_input("السعر المقترح ($):", min_value=1)
        p_cat = st.selectbox("التصنيف:", ["دورة تدريبية", "كتاب إلكتروني", "جلسة استشارية"])
        p_desc = st.text_area("وصف القيمة المضافة:")
        if st.form_submit_button("إطلاق المنتج في السحابة 🚀"):
            if p_name:
                with st.spinner("جاري المزامنة العالمية..."):
                    if submit_live_product(p_name, p_price, p_desc, p_cat, st.session_state.store_name):
                        st.success("لقد تم إدراج منتجك في السحابة بنجاح!")
                        time.sleep(1)
                        st.rerun()
            else: st.error("يرجى كتابة اسم المنتج.")

# --- Tab 3: المتجر الشخصي ---
with tab3:
    st.markdown(f"<h1>{st.session_state.store_name}</h1>", unsafe_allow_html=True)
    st.info("هنا تظهر هويتك التجارية المستقلة أمام العالم.")

# --- Tab 4: أكاديمية التجار ---
with tab4:
    st.header("🧠 كيف تصبح تاجر تريليون؟")
    st.write("السر يكمن في ربط منتجك بـ 'رحلة الـ 100 يوم'.")

st.divider()
if st.button("📊 مراقبة العمولات"):
    st.switch_page("pages/11_Affiliate_System.py")
