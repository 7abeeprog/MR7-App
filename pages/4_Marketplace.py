import streamlit as st
import time

# --- 1. محرك الأنماط الشامل (Theme Engine) ---
# التأكد من وجود متغير النمط في ذاكرة الجلسة لضمان الاستمرارية
if 'app_theme' not in st.session_state:
    st.session_state.app_theme = "غامق إمبراطوري 🖤"

# تعريف مصفوفة الألوان لكل نمط لضمان أعلى مستويات التباين والوضوح
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

# حقن تنسيقات CSS المتقدمة لبناء الواجهة العالمية
st.markdown(f"""
    <style>
    /* تنسيق الخلفية العامة والقائمة الجانبية */
    .stApp {{ background-color: {t['bg']} !important; color: {t['text']} !important; }}
    [data-testid="stSidebar"] {{ background-color: {t['sidebar']} !important; border-right: 2px solid {t['accent']} !important; }}
    
    /* تنسيق النصوص والعناوين لضمان الوضوح التام */
    div[data-testid="stMarkdownContainer"] p, h2, h3, span, label, li {{ 
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
    
    /* بطاقات المنتجات في السوق العالمي */
    .market-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }}
    .market-card:hover {{ 
        border-color: #00FF88; 
        transform: scale(1.03) translateY(-10px); 
        box-shadow: 0 15px 40px rgba(0,255,136,0.2);
    }}
    
    /* شارات التجار (Vendor Badges) */
    .vendor-badge {{
        background: {t['accent']};
        color: #000 !important;
        padding: 4px 12px;
        border-radius: 10px;
        font-size: 0.85rem;
        font-weight: 900;
        text-transform: uppercase;
    }}

    /* تنسيق الأزرار الاحترافي */
    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 15px !important;
        height: 55px;
        transition: 0.3s;
    }}
    .stButton>button:hover {{ transform: translateY(-3px); filter: brightness(1.1); }}

    /* إصلاح القوائم المنسدلة لضمان وضوح النص في كل الأنماط */
    div[data-baseweb="select"] > div {{ background-color: {t['select_bg']} !important; color: {t['select_text']} !important; }}
    div[data-baseweb="popover"] ul {{ background-color: {t['select_bg']} !important; }}
    div[data-baseweb="popover"] li {{ color: {t['select_text']} !important; background-color: {t['select_bg']} !important; }}
    div[data-baseweb="popover"] li:hover {{ background-color: {t['accent']} !important; color: #000000 !important; }}

    /* تحسين شكل التبويبات (Tabs) */
    .stTabs [data-baseweb="tab-list"] {{ gap: 25px; }}
    .stTabs [data-baseweb="tab"] {{ color: {t['text']} !important; font-weight: 900 !important; font-size: 1.2rem !important; }}
    .stTabs [aria-selected="true"] {{ color: {t['accent']} !important; border-bottom: 3px solid {t['accent']} !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة الحالة والبيانات (Multi-Vendor Session State) ---
if 'my_products' not in st.session_state:
    st.session_state.my_products = []
if 'store_name' not in st.session_state:
    st.session_state.store_name = "إمبراطورية التجارة"
if 'store_slogan' not in st.session_state:
    st.session_state.store_slogan = "حلول ذكية لعصر المليار"

# --- 3. القائمة الجانبية (إعدادات النمط والهوية) ---
with st.sidebar:
    st.markdown(f"### 🎨 تخصيص المظهر")
    theme_choice = st.selectbox("اختر نمط الألوان:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    st.markdown("### 🏪 إعدادات علامتك التجارية")
    st.session_state.store_name = st.text_input("اسم متجرك العالمي:", st.session_state.store_name)
    st.session_state.store_slogan = st.text_input("شعار المتجر (Slogan):", st.session_state.store_slogan)
    st.caption("سيتم تخصيص متجرك الشخصي بهذه البيانات فوراً.")

# --- 4. واجهة المركز التجاري العالمي ---
st.title("MR7 Global Marketplace")

tab1, tab2, tab3, tab4 = st.tabs(["🌎 السوق العالمي", "🏗️ لوحة التاجر", "🔗 متجري الشخصي", "🧠 أكاديمية التجار"])

# --- Tab 1: السوق العالمي (تعدد التجار) ---
with tab1:
    st.markdown(f"<p style='text-align:center; font-size: 1.3rem; margin-top: -20px;'>تصفح المنتجات والخدمات من قادة منظومة MR7</p>", unsafe_allow_html=True)
    
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search = st.text_input("🔍 ابحث عن دورة، أداة، أو منتج محدد...")
    with col_filter:
        category = st.selectbox("الفئة:", ["الكل", "خدمات مالية", "دورات قيادية", "أدوات تقنية"])

    # محاكاة لمنتجات التجار الآخرين
    global_items = [
        {"name": "أسرار هندسة النظم المالية", "vendor": "أكاديمية MR7", "price": 499, "tag": "إمبراطوري"},
        {"name": "دليل غزو الأسواق الناشئة", "vendor": "د. عاصم القائد", "price": 120, "tag": "خبير"},
        {"name": "جلسة كوتشينج المليار", "vendor": "إدارة MR7", "price": 1000, "tag": "نخبة"}
    ]
    
    # دمج منتجات المستخدم الحقيقية التي قام بإضافتها
    for p in st.session_state.my_products:
        global_items.append({"name": p['name'], "vendor": st.session_state.store_name, "price": p['price'], "tag": "تاجر صاعد"})

    # عرض المنتجات بنظام الشبكة المتطورة
    rows = [global_items[i:i + 3] for i in range(0, len(global_items), 3)]
    for row in rows:
        cols = st.columns(3)
        for i, item in enumerate(row):
            with cols[i]:
                st.markdown(f"""
                <div class="market-card">
                    <span class="vendor-badge">{item['tag']}</span>
                    <h3 style="margin-top:15px; font-size: 1.4rem;">{item['name']}</h3>
                    <p style="color: #888; font-size: 0.9rem;">بواسطة: {item['vendor']}</p>
                    <div style="color: #00FF88; font-size: 2rem; font-weight: 900; margin: 15px 0;">${item['price']:,}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"اقتناء الآن 🛒", key=f"buy_grid_{item['name']}_{i}"):
                    st.success(f"تمت العملية بنجاح! أنت الآن تمتلك {item['name']}")

# --- Tab 2: لوحة تحكم التاجر (إدارة المحتوى) ---
with tab2:
    st.header("🏗️ مركز إدارة المحتوى التجاري")
    st.markdown("قم بتحويل خبرتك وقيمتك إلى منتج رقمي متاح لآلاف القادة في المنظومة.")
    
    col_form, col_stats = st.columns([2, 1])
    
    with col_form:
        st.markdown("### إطلاق منتج جديد")
        with st.form("advanced_vendor_form"):
            p_name = st.text_input("اسم المنتج الاستراتيجي:")
            p_price = st.number_input("السعر المقترح ($):", min_value=1)
            p_cat = st.selectbox("تصنيف المنتج:", ["دورة تدريبية", "كتاب إلكتروني", "خدمة استشارية", "أداة ذكاء اصطناعي"])
            p_desc = st.text_area("وصف القيمة المضافة لعميلك:")
            submitted = st.form_submit_button("إرسال المنتج للسوق العالمي 🚀")
            
            if submitted and p_name:
                st.session_state.my_products.append({"name": p_name, "price": p_price, "desc": p_desc, "cat": p_cat})
                st.success(f"لقد تم إدراج '{p_name}' بنجاح! سيتم إخطار شبكة المسوقين فوراً.")
                time.sleep(1)
                st.rerun()

    with col_stats:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 25px; border-radius: 20px; border: 1px solid #444; text-align: center;">
            <h4 style="color: {t['accent']};">ملخص أداء التاجر</h4>
            <div style="font-size: 2.5rem; font-weight: 900; color: #00FF88;">{len(st.session_state.my_products)}</div>
            <p>منتج نشط في السوق</p>
            <hr style="border-color: #333;">
            <p style="font-size: 1.2rem;">إجمالي المبيعات: <b>$0.00</b></p>
            <p>رتبة المتجر: <span style="color: #FFD700;">تاجر طموح</span></p>
        </div>
        """, unsafe_allow_html=True)

# --- Tab 3: المتجر الشخصي (White Label Experience) ---
with tab3:
    st.markdown(f"<h1 style='font-size: 4.5rem; margin-bottom: 0;'>{st.session_state.store_name}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size: 1.6rem; color: {t['accent']}; font-weight: 800; letter-spacing: 4px;'>{st.session_state.store_slogan}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color: #555; font-style: italic;'>Subdomain: https://{st.session_state.store_name.lower().replace(' ', '-')}.mr7-market.com</p>", unsafe_allow_html=True)
    
    st.divider()
    
    if not st.session_state.my_products:
        st.warning("متجرك الخاص فارغ الآن. ابدأ بإضافة منتجاتك من 'لوحة التاجر' لتظهر هنا بهويتك الخاصة.")
    else:
        st.markdown(f"### 💎 منتجات {st.session_state.store_name} المختارة")
        for p in st.session_state.my_products:
            st.markdown(f"""
            <div class="market-card" style="border-color: {t['accent']}; background: rgba(255, 215, 0, 0.03);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h2 style="color: {t['text']}; margin: 0;">{p['name']}</h2>
                        <p style="color: {t['accent']}; font-weight: bold;">{p['cat']}</p>
                    </div>
                    <div style="font-size: 2.5rem; color: #00FF88; font-weight: 950;">${p['price']:,}</div>
                </div>
                <hr style="border-color: #444;">
                <p style="font-size: 1.2rem; color: #ccc; line-height: 1.6;">{p['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

# --- Tab 4: أكاديمية التجار (Inspiration & Education) ---
with tab4:
    st.header("🧠 كيف تهيمن على السوق العالمي؟")
    st.markdown("""
    في MR7، نحن لا نبيع مجرد منتجات، نحن نبيع **نتائج استراتيجية**. لكي ينجح متجرك، يجب أن تركز على حل مشكلات القادة الآخرين.
    """)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div style="background: {t['card']}; padding: 20px; border-radius: 15px; border: 1px solid #00FF88;">
            <h3 style="color: #00FF88;">🎬 أسرار المحتوى البيعي</h3>
            <p>تعلم كيف تكتب وصفاً للمنتج يجعل القائد يشعر بأن هذا المنتج هو القطعة الناقصة في رحلته.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div style="background: {t['card']}; padding: 20px; border-radius: 15px; border: 1px solid #FFD700;">
            <h3 style="color: #FFD700;">📈 استراتيجية التسعير</h3>
            <p>كيف توازن بين السعر العادل والقيمة الإمبراطورية لضمان ولاء العملاء وتكرار الشراء.</p>
        </div>
        """, unsafe_allow_html=True)

# زر الانتقال لنظام العمولات
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("📊 مراقبة العمولات وحجم مبيعات الفريق"):
    st.switch_page("pages/5_Commissions.py")
