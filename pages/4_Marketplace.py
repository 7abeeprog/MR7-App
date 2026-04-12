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
        filter: drop-shadow(0 0 15px {t['accent']}); 
        font-size: 3.5rem !important; 
    }}

    /* تصميم بطاقات المنتجات الاحترافي */
    .market-card {{
        background: {t['card']};
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 25px;
        padding: 0;
        margin-bottom: 30px;
        overflow: hidden;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
    }}
    .market-card:hover {{ transform: translateY(-10px); border-color: {t['accent']}; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }}
    
    .product-img {{
        width: 100%;
        height: 200px;
        object-fit: cover;
    }}

    .product-info {{ padding: 20px; }}

    .badge-premium {{
        position: absolute;
        top: 15px;
        right: 15px;
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: black !important;
        padding: 5px 12px;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 900;
        z-index: 10;
    }}

    .price-tag {{
        color: #00FF88;
        font-size: 1.8rem;
        font-weight: 950;
    }}

    /* حل مشكلة الكتابة باللون الأسود في الحقول */
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
        width: 100%;
        font-size: 1.1rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات والربط المالي (Financial Integration) ---
fb_config = json.loads(st.secrets.get("__firebase_config", "{}"))
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
project_id = fb_config.get("projectId", "mr7-app")
BASE_URL = "https://firestore.googleapis.com/v1/"
COLLECTION_PATH = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/public/data/marketplace_products"

if 'cash_balance' not in st.session_state: st.session_state.cash_balance = 1250000.00
if 'store_name' not in st.session_state: st.session_state.store_name = "إمبراطورية التجارة"

def fetch_live_products():
    """جلب كافة المنتجات الموثقة من السحابة"""
    try:
        res = requests.get(f"{BASE_URL}{COLLECTION_PATH}")
        if res.status_code == 200:
            docs = res.json().get("documents", [])
            items = []
            for doc in docs:
                f = doc.get("fields", {})
                items.append({
                    "id": doc["name"].split("/")[-1],
                    "name": f.get("name", {}).get("stringValue", "منتج إمبراطوري"),
                    "price": int(f.get("price", {}).get("integerValue", "0")),
                    "vendor": f.get("vendor", {}).get("stringValue", "تاجر MR7"),
                    "img": f.get("img", {}).get("stringValue", "https://images.unsplash.com/photo-1554224155-169641357599?w=500&q=80"),
                    "cat": f.get("cat", {}).get("stringValue", "عام"),
                    "rating": f.get("rating", {}).get("doubleValue", 5.0),
                    "sales": int(f.get("sales", {}).get("integerValue", "0")),
                    "region": f.get("region", {}).get("stringValue", "عالمي")
                })
            return items
        return []
    except: return []

def buy_product(price, name):
    """منطق الشراء المباشر والخصم من الخزنة"""
    if st.session_state.cash_balance >= price:
        st.session_state.cash_balance -= price
        st.success(f"تم شراء '{name}' بنجاح! الرصيد المتبقي: ${st.session_state.cash_balance:,.2f}")
        st.balloons()
        return True
    else:
        st.error("عذراً قائد، السيولة في خزنتك لا تغطي تكلفة هذا الأصل.")
        return False

# --- 3. واجهة المركز التجاري العالمي ---
st.title("MR7 Global Marketplace")

# شريط السيادة المالي (Top Header Wallet)
c_h1, c_h2 = st.columns([2, 1])
with c_h1:
    st.markdown(f"**إقليمك المفضل:** `{st.session_state.get('leader_region', 'مصر')}`")
with c_h2:
    st.markdown(f"<div style='text-align:left; background:rgba(0,255,136,0.1); padding:10px; border-radius:15px; border:1px solid #00FF88;'>💰 الخزنة: **${st.session_state.cash_balance:,.2f}**</div>", unsafe_allow_html=True)

st.divider()

# الفلاتر الاستراتيجية (Professional Filters)
with st.expander("🔍 فلاتر البحث المتقدمة"):
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        region_filter = st.multiselect("الإقليم الاستراتيجي:", ["مصر", "ليبيا", "السودان", "عالمي"], default=["مصر", "ليبيا", "السودان", "عالمي"])
    with f_col2:
        price_range = st.slider("نطاق السعر ($):", 0, 10000, (0, 10000))
    with f_col3:
        sort_by = st.selectbox("ترتيب حسب:", ["الأعلى مبيعاً", "السعر: من الأقل", "السعر: من الأعلى", "الأعلى تقييماً"])

tabs = st.tabs(["🌎 السوق العالمي", "👑 العروض الذهبية", "🏗️ لوحة التاجر", "📦 مشترياتي الموثقة"])

# --- Tab 1: السوق العالمي (Professional Grid) ---
with tabs[0]:
    live_items = fetch_live_projects() # دالة وهمية أو استدعاء fetch_live_products
    # تحسين عرض المنتجات
    if not live_items:
        # بيانات تجريبية احترافية في حالة عدم توفر السحابة
        live_items = [
            {"id":"1", "name": "أسرار سيارات الكهرباء", "price": 499, "vendor": "أكاديمية MR7", "cat": "دورة تدريبية", "rating": 4.9, "sales": 1240, "img": "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=500&q=80", "region": "مصر"},
            {"id":"2", "name": "حقيبة التوسع في ليبيا", "price": 250, "vendor": "القائد صالح", "cat": "أدوات تقنية", "rating": 4.7, "sales": 850, "img": "https://images.unsplash.com/photo-1526628953301-3e589a6a8b74?w=500&q=80", "region": "ليبيا"},
            {"id":"3", "name": "كوتشينج المليار", "price": 2500, "vendor": "القائد المؤسس", "cat": "جلسة استشارية", "rating": 5.0, "sales": 320, "img": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=500&q=80", "region": "عالمي"}
        ]

    rows = [live_items[i:i + 3] for i in range(0, len(live_items), 3)]
    for row in rows:
        cols = st.columns(3)
        for i, item in enumerate(row):
            with cols[i]:
                st.markdown(f"""
                <div class="market-card">
                    <div class="badge-premium">إصدار محدود</div>
                    <img src="{item['img']}" class="product-img">
                    <div class="product-info">
                        <small style="color:{t['accent']};">{item['region']} | {item['cat']}</small>
                        <h3 style="margin: 10px 0; font-size: 1.3rem;">{item['name']}</h3>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <span class="price-tag">${item['price']:,}</span>
                            <span style="font-size: 0.8rem; opacity: 0.6;">👤 {item['sales']} مبيعة</span>
                        </div>
                        <div style="color: #FFD700; margin-bottom: 15px;">{'⭐' * int(item['rating'])} <small>({item['rating']})</small></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"شراء بلمسة واحدة ⚡", key=f"buy_{item['id']}"):
                    buy_product(item['price'], item['name'])

# --- Tab 2: العروض الذهبية (Golden Deals) ---
with tabs[1]:
    st.subheader("🔥 صفقات السيادة اللحظية")
    st.markdown("عروض خاصة متاحة فقط لأعضاء رتبة 'قائد استراتيجي' فما فوق.")
    st.warning("تنتهي هذه العروض خلال 04:22:15")
    
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #111, #333); padding: 30px; border-radius: 20px; border: 1px solid {t['accent']}; display: flex; gap: 20px; align-items: center;">
        <div style="font-size: 4rem;">💎</div>
        <div style="flex-grow: 1;">
            <h3 style="margin:0;">باقة التريليون المتكاملة</h3>
            <p style="opacity:0.7;">تشمل كافة الدورات + استشارة مجانية مع مجلس الإدارة.</p>
        </div>
        <div style="text-align: center;">
            <span style="text-decoration: line-through; color: red;">$10,000</span><br>
            <span style="font-size: 2rem; color: #00FF88;">$4,999</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Tab 3: لوحة التاجر (Merchant Dashboard) ---
with tabs[2]:
    st.subheader("🏗️ مركز إدارة التجارة العالمي")
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("إجمالي المبيعات", "$45,200", "+12%")
    m_col2.metric("العمولات المستحقة", "$4,520", "+$500")
    m_col3.metric("المنتجات النشطة", "8", "نشط ✅")
    
    st.divider()
    with st.expander("➕ إضافة أصل تجاري جديد للسحابة"):
        with st.form("new_product_admin"):
            p_name = st.text_input("اسم المنتج الاستراتيجي:")
            p_price = st.number_input("السعر المقترح ($):", min_value=1)
            p_region = st.selectbox("إقليم الاستهداف الرئيسي:", ["مصر", "ليبيا", "السودان", "عالمي"])
            p_cat = st.selectbox("التصنيف:", ["دورة تدريبية", "كتاب إلكتروني", "جلسة استشارية"])
            if st.form_submit_button("إطلاق المنتج عالمياً 🚀"):
                st.success("تم إرسال المنتج لتدقيق الجودة. سيظهر في السوق خلال ساعات.")

# --- Tab 4: مشترياتي الموثقة ---
with tabs[3]:
    st.subheader("📦 أرشيف المشتريات والوصول")
    st.info("كافة منتجاتك الرقمية محفوظة في السحابة للأبد.")
    st.table([
        {"المنتج": "دليل غزو أسواق مصر", "التاريخ": "2026-03-27", "الوصول": "متاح ✅"},
        {"المنتج": "كوتشينج المليار", "التاريخ": "2026-04-05", "الوصول": "متاح ✅"}
    ])

st.divider()

# خريطة الانتقال
st.markdown("### 🗺️ خريطة السيادة السريعة")
cb1, cb2, cb3 = st.columns(3)
with cb1:
    if st.button("💰 الخزنة الإمبراطورية"): st.switch_page("pages/3_Wallet.py")
with cb2:
    if st.button("📊 نظام العمولات"): st.switch_page("pages/11_Affiliate_System.py")
with cb3:
    if st.button("🏠 العودة للرئيسية"): st.switch_page("app.py")
