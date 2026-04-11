import streamlit as st
import time

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
    h1 {{ background: linear-gradient(90deg, {t['accent']}, {t['text']}, {t['accent']}); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 950 !important; text-align: center; filter: drop-shadow(0 0 10px {t['accent']}); font-size: 3rem !important; }}
    
    .market-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        transition: 0.3s;
    }}
    .market-card:hover {{ border-color: #00FF88; transform: translateY(-5px); }}
    
    .vendor-badge {{
        background: {t['accent']};
        color: #000 !important;
        padding: 2px 10px;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: bold;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 12px !important;
        width: 100%;
    }}
    
    /* إصلاح القوائم المنسدلة */
    div[data-baseweb="select"] > div {{ background-color: {t['select_bg']} !important; color: {t['select_text']} !important; }}
    div[data-baseweb="popover"] li {{ color: {t['select_text']} !important; background-color: {t['select_bg']} !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة الجلسة للمتجر المتعدد ---
if 'my_products' not in st.session_state:
    st.session_state.my_products = []
if 'store_name' not in st.session_state:
    st.session_state.store_name = "متجري الخاص"

# --- 3. القائمة الجانبية ---
with st.sidebar:
    st.markdown(f"### 🎨 تخصيص المظهر")
    theme_choice = st.selectbox("النمط الحالي:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    st.markdown("### 🏪 إعدادات متجرك")
    st.session_state.store_name = st.text_input("اسم متجرك التجاري:", st.session_state.store_name)
    st.caption("سيظهر هذا الاسم للعملاء في السوق العالمي")

# --- 4. واجهة المركز التجاري ---
tab1, tab2, tab3 = st.tabs(["🌎 السوق العالمي", "🏗️ لوحة تحكم التاجر", "🔗 متجري الشخصي"])

# --- Tab 1: السوق العالمي ---
with tab1:
    st.markdown(f"<h1>السوق العالمي MR7</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>تصفح منتجات قادة MR7 حول العالم</p>", unsafe_allow_html=True)
    
    search = st.text_input("🔍 ابحث عن منتج، دورة، أو تاجر محدد...")
    
    # مبيعات وهمية للتوضيح
    global_items = [
        {"name": "خطة التسويق المليونية", "vendor": "أحمد القائد", "price": 299},
        {"name": "كتاب أسرار التريليون", "vendor": "سارة الاستراتيجية", "price": 49},
        {"name": "كوتشينج قيادي ساعة", "vendor": "إمبراطور MR7", "price": 500}
    ]
    
    # إضافة منتجات المستخدم الحقيقية للسوق
    for p in st.session_state.my_products:
        global_items.append({"name": p['name'], "vendor": st.session_state.store_name, "price": p['price']})

    cols = st.columns(3)
    for i, item in enumerate(global_items):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="market-card">
                <span class="vendor-badge">👤 {item['vendor']}</span>
                <h3 style="margin-top:10px;">{item['name']}</h3>
                <p style="color: #00FF88; font-size: 1.5rem;">${item['price']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"شراء الآن 🛒", key=f"buy_global_{i}"):
                st.success(f"تمت عملية الشراء من {item['vendor']} بنجاح!")

# --- Tab 2: لوحة تحكم التاجر (إضافة منتجات) ---
with tab2:
    st.header("🏗️ إدارة منتجاتك الخاصة")
    st.info("هنا يمكنك إضافة منتجاتك ليراها آلاف المتدربين في السوق العالمي.")
    
    with st.form("add_product"):
        p_name = st.text_input("اسم المنتج/الخدمة:")
        p_price = st.number_input("السعر المستهدف ($):", min_value=1)
        p_desc = st.text_area("وصف المنتج:")
        submitted = st.form_submit_button("إضافة المنتج للسوق 🚀")
        
        if submitted:
            if p_name:
                st.session_state.my_products.append({"name": p_name, "price": p_price, "desc": p_desc})
                st.success("تم إدراج منتجك بنجاح في السوق العالمي!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("يرجى إدخال اسم المنتج")

    if st.session_state.my_products:
        st.subheader("📦 مخزنك الحالي")
        for p in st.session_state.my_products:
            st.write(f"- **{p['name']}**: ${p['price']}")

# --- Tab 3: متجري الشخصي (Brand Experience) ---
with tab3:
    st.markdown(f"<h1 style='font-size: 4rem;'>{st.session_state.store_name}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color: #aaa;'>Domain: {st.session_state.store_name.lower().replace(' ', '-')}.mr7-app.com</p>", unsafe_allow_html=True)
    
    st.divider()
    
    if not st.session_state.my_products:
        st.warning("لم تقم بإضافة منتجات لمتجرك الخاص بعد. اذهب للوحة تحكم التاجر.")
    else:
        st.markdown(f"### 💎 معروضات {st.session_state.store_name}")
        for p in st.session_state.my_products:
            st.markdown(f"""
            <div class="market-card" style="border-color: #FFD700; background: rgba(255, 215, 0, 0.05);">
                <h2>{p['name']}</h2>
                <p>{p['desc']}</p>
                <div style="font-size: 2rem; color: #FFD700;">${p['price']}</div>
            </div>
            """, unsafe_allow_html=True)

st.divider()
if st.button("📊 الانتقال لنظام العمولات الاستراتيجي"):
    st.switch_page("pages/5_Commissions.py")
