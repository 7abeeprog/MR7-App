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
    /* الفلسفة التصميمية: تجربة تسوق عالمية (World-Class Shopping Experience) */
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

    /* تصميم بطاقات المنتجات (Alibaba Inspired) */
    .market-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 25px;
        padding: 0;
        margin-bottom: 30px;
        overflow: hidden;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 15px 40px rgba(0,0,0,0.5);
    }}
    .market-card:hover {{ transform: scale(1.03) translateY(-10px); border-color: #00FF88; }}
    
    .product-img {{
        width: 100%;
        height: 220px;
        object-fit: cover;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }}

    .product-info {{ padding: 20px; }}

    .vendor-badge {{
        background: {t['accent']};
        color: #000 !important;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 950;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 8px;
    }}

    /* لوحة التاجر (Merchant Dashboard) */
    .stat-tile {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid {t['border']};
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }}

    /* حل مشكلة الكتابة باللون الأسود */
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
    
    /* تنسيق التبويبات Tabs */
    .stTabs [data-baseweb="tab-list"] {{ gap: 25px; }}
    .stTabs [data-baseweb="tab"] {{ font-weight: 900; font-size: 1.1rem; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك قاعدة البيانات الحية (Live Firestore Logic) ---
fb_config = json.loads(st.secrets.get("__firebase_config", "{}"))
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
project_id = fb_config.get("projectId", "mr7-app")

BASE_URL = "https://firestore.googleapis.com/v1/"
COLLECTION_PATH = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/public/data/marketplace_products"

def fetch_live_products():
    """جلب كافة المنتجات من السحابة"""
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
                    "img": fields.get("img", {}).get("stringValue", "https://images.unsplash.com/photo-1554224155-169641357599?w=500&q=80"),
                    "cat": fields.get("cat", {}).get("stringValue", "عام")
                })
            return items
        return []
    except: return []

def submit_live_product(name, price, desc, cat, vendor):
    """إرسال منتج جديد للسحابة"""
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
if 'store_name' not in st.session_state: st.session_state.store_name = "إمبراطورية التجارة"
if 'store_slogan' not in st.session_state: st.session_state.store_slogan = "حلول ذكية لعصر المليار"

# --- 4. واجهة المركز التجاري العالمي ---
st.title("MR7 Global Marketplace")

# شريط البحث والفلترة العلوي
col_s1, col_s2 = st.columns([3, 1])
with col_s1:
    search_query = st.text_input("🔍 ابحث في أكبر متجر للقادة في العالم...", placeholder="مثلاً: دورة الهندسة المالية، باقة التوسع...")
with col_s2:
    cat_filter = st.selectbox("تصفية بالفئة:", ["الكل", "دورة تدريبية", "كتاب إلكتروني", "جلسة استشارية"])

st.markdown("<br>", unsafe_allow_html=True)

tabs = st.tabs(["🌎 السوق العالمي", "🏗️ لوحة التاجر", "🔗 متجري الشخصي", "🧠 أكاديمية التجار"])

# --- Tab 1: السوق العالمي (Enhanced Alibaba Grid) ---
with tabs[0]:
    live_items = fetch_live_products()
    
    if not live_items:
        st.info("جاري المزامنة مع شبكة التجار العالمية...")
        live_items = [
            {"name": "هندسة النظم المالية", "vendor": "أكاديمية MR7", "price": 499, "tag": "إمبراطوري", "img": "https://images.unsplash.com/photo-1554224155-169641357599?w=500&q=80", "cat": "دورة تدريبية"},
            {"name": "كوتشينج المليار", "vendor": "القائد المؤسس", "price": 1200, "tag": "نخبة", "img": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=500&q=80", "cat": "جلسة استشارية"}
        ]

    # فلترة النتائج
    filtered_items = [i for i in live_items if (cat_filter == "الكل" or i['cat'] == cat_filter) and (search_query.lower() in i['name'].lower())]

    if not filtered_items:
        st.warning("لم يتم العثور على منتجات تطابق بحثك.")
    else:
        rows = [filtered_items[idx:idx + 3] for idx in range(0, len(filtered_items), 3)]
        for row in rows:
            cols = st.columns(3)
            for i, item in enumerate(row):
                with cols[i]:
                    st.markdown(f"""
                    <div class="market-card">
                        <img src="{item.get('img', '')}" class="product-img">
                        <div class="product-info">
                            <span class="vendor-badge">{item['tag']}</span>
                            <h3 style="margin: 5px 0; font-size: 1.2rem;">{item['name']}</h3>
                            <p style="color: #aaa; font-size: 0.8rem; margin-bottom: 10px;">بواسطة: {item['vendor']}</p>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="color: #00FF88; font-size: 1.8rem; font-weight: 950;">${int(item['price']):,}</div>
                                <div style="color: {t['accent']}; font-size: 0.9rem;">⭐ 4.9 (124)</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"اقتناء 🛒", key=f"buy_{item.get('id', i)}"):
                        st.success("تمت إضافة المنتج لخزنتك الموثقة!")

# --- Tab 2: لوحة التاجر (Merchant Dashboard & Form) ---
with tabs[1]:
    st.header("🏗️ مركز إدارة المحتوى التجاري")
    
    # إحصائيات التاجر
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    col_stat1.markdown('<div class="stat-tile"><small>إجمالي المبيعات</small><br><span style="font-size:1.8rem; color:#00FF88;">$0.00</span></div>', unsafe_allow_html=True)
    col_stat2.markdown('<div class="stat-tile"><small>عدد الطلبات</small><br><span style="font-size:1.8rem;">0</span></div>', unsafe_allow_html=True)
    col_stat3.markdown('<div class="stat-tile"><small>نقاط التقييم</small><br><span style="font-size:1.8rem; color:#FFD700;">5.0</span></div>', unsafe_allow_html=True)
    
    st.divider()
    
    st.subheader("إضافة منتج استراتيجي جديد")
    with st.form("merchant_product_form"):
        p_name = st.text_input("اسم المنتج:")
        p_price = st.number_input("السعر المستهدف ($):", min_value=1)
        p_cat = st.selectbox("تصنيف المنتج:", ["دورة تدريبية", "كتاب إلكتروني", "جلسة استشارية"])
        p_desc = st.text_area("وصف القيمة المضافة للعميل:")
        if st.form_submit_button("إطلاق المنتج في السحابة العالمية 🚀"):
            if p_name:
                with st.spinner("جاري المزامنة مع الأسطول التجاري..."):
                    if submit_live_product(p_name, p_price, p_desc, p_cat, st.session_state.store_name):
                        st.success("تم النشر بنجاح! منتجك الآن متاح لـ 110 مليون شاب عربي.")
                        time.sleep(1)
                        st.rerun()
            else: st.error("يرجى إكمال البيانات.")

# --- Tab 3: المتجر الشخصي (White Labeling) ---
with tabs[3]:
    st.markdown(f"<h1>{st.session_state.store_name}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.4rem;'>{st.session_state.store_slogan}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; opacity:0.6;'>Subdomain: <code>https://{st.session_state.store_name.replace(' ', '-').lower()}.mr7-market.com</code></p>", unsafe_allow_html=True)
    
    st.divider()
    st.info("متجرك الخاص فارغ الآن. ابدأ بإضافة منتجاتك من 'لوحة التاجر' لتظهر هنا بهويتك الخاصة.")

    # إعدادات العلامة التجارية
    with st.expander("🏪 إعدادات علامتك التجارية"):
        st.session_state.store_name = st.text_input("اسم متجرك العالمي:", st.session_state.store_name)
        st.session_state.store_slogan = st.text_input("شعار المتجر (Slogan):", st.session_state.store_slogan)
        st.caption("سيتم تخصيص متجرك الشخصي بهذه البيانات فوراً.")

# --- Tab 4: أكاديمية التجار ---
with tabs[4]:
    st.header("🧠 كيف تصبح تاجر تريليون؟")
    st.write("أسرار النجاح في التجارة الرقمية عبر منصة MR7.")
    st.markdown("""
    - **قاعدة الـ 10:** كيف تحول أول 10 مشترين إلى جيش من المسوقين.
    - **هندسة العروض:** كيفية تسعير خدماتك لتعظيم الربح والانتشار.
    - **التوسع الجغرافي:** استراتيجيات الوصول لأسواق مصر وليبيا والسودان.
    """)

st.divider()
if st.button("📊 مراقبة العمولات ونظام الأجيال"):
    st.switch_page("pages/11_Affiliate_System.py")
