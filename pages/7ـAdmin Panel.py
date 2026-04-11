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
        font-size: 3.2rem !important; 
    }}

    .admin-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        text-align: center;
    }}

    /* حل مشكلة الكتابة (نص أسود على خلفية بيضاء) لضمان الوضوح التام */
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
        border-radius: 15px !important;
        height: 50px;
    }}

    /* تحسين شكل القوائم المنسدلة */
    div[data-baseweb="select"] > div {{ background-color: {t['select_bg']} !important; color: {t['select_text']} !important; }}
    div[data-baseweb="popover"] li {{ color: {t['select_text']} !important; background-color: {t['select_bg']} !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. القائمة الجانبية ---
with st.sidebar:
    st.markdown(f"### 🎨 تخصيص المظهر")
    theme_choice = st.selectbox("النمط الحالي:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    st.markdown("### 👑 حالة الإدارة")
    st.warning("وصول: أدمن رئيسي (Root)")
    st.success("سيرفرات المنظومة: مستقرة ✅")

# --- 3. واجهة لوحة التحكم العليا ---
st.title("👑 لوحة التحكم العليا")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.3rem; margin-top:-20px;'>الإدارة الإمبراطورية لمنظومة MR7 العالمية</p>", unsafe_allow_html=True)

st.divider()

# إحصائيات حية وشاملة
col1, col2, col3, col4 = st.columns(4)
metrics = [
    ("إجمالي القادة", "15,420", "👥"),
    ("أرباح المنظومة (EGP)", "2.4M", "💰"),
    ("روابط الإحالة النشطة", "8,210", "🔗"),
    ("معدل التحويل", "12.5%", "⚡")
]

for i, (label, val, icon) in enumerate(metrics):
    with [col1, col2, col3, col4][i]:
        st.markdown(f"""
        <div class="admin-card">
            <p style="font-size: 0.9rem;">{icon} {label}</p>
            <div style="font-size: 1.8rem; font-weight: 900; color: {t['accent']};">{val}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

tabs = st.tabs(["👥 إدارة القادة", "🛒 مراجعة المتجر", "💹 هندسة العمولات", "🔗 روابط الإحالة", "🏆 الترقيات"])

# --- Tab 1: إدارة المستخدمين ---
with tabs[0]:
    st.subheader("👥 إدارة قاعدة بيانات القادة")
    
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        st.text_input("بحث عن مستخدم (ID, Email, Name):", placeholder="أدخل بيانات البحث...", key="user_search")
    with col_filter:
        st.selectbox("الفلترة حسب الرتبة:", ["الكل", "أدمن", "مدرب", "متدرب", "قائد فريق"], key="rank_filter")

    user_data = [
        {"ID": "MR7-001", "الاسم": "أحمد علي", "الرتبة": "مدرب بلاتيني", "XP": "4500", "الحالة": "نشط ✅"},
        {"ID": "MR7-042", "الاسم": "سارة محمد", "الرتبة": "قائد ماسي", "XP": "2800", "الحالة": "نشط ✅"},
    ]
    st.table(user_data)

# --- Tab 2: مراجعة المتجر ---
with tabs[1]:
    st.subheader("🛒 مراجعة معروضات السوق")
    st.info("إدارة جودة المنتجات والخدمات المقدمة من التجار.")
    
    with st.expander("📝 طلبات نشر جديدة (14)"):
        st.write("- دورة 'هندسة التريليون' (المدرب: أحمد علي) - **[معاينة]**")
        st.write("- باقة 'أدوات الانتشار' (التاجر: سارة) - **[معاينة]**")
        st.button("الموافقة على جميع الطلبات المستوفية للشروط")

# --- Tab 3: هندسة العمولات (Commission Engineering) ---
with tabs[2]:
    st.subheader("💹 إدارة نظام العمولات الذكي")
    st.markdown("تحكم في نسب الأرباح والمكافآت لتجار وقادة المنظومة.")
    
    with st.container():
        st.markdown("<div class='admin-card'>", unsafe_allow_html=True)
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("#### إعدادات العمولة العامة")
            gen_rate = st.number_input("نسبة العمولة الأساسية للمسوقين (%):", value=10)
            vip_rate = st.number_input("نسبة العمولة للقادة الموثقين (%):", value=20)
        with col_c2:
            st.markdown("#### تخصيص حسب المنتج")
            target_prod = st.selectbox("اختر المنتج لتخصيص عمولته:", ["باقة القائد البلاتيني", "دورة عقلية المليار", "اشتراك الوكيل الذكي"])
            spec_rate = st.number_input(f"عمولة {target_prod} (%):", value=15)
        
        if st.button("💾 حفظ إعدادات العمولات الاستراتيجية"):
            st.success("تم تحديث هيكلية العمولات في كامل المنظومة.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- Tab 4: روابط الإحالة (Referral Management) ---
with tabs[3]:
    st.subheader("🔗 مركز إدارة روابط الإحالة")
    st.info("توليد وربط روابط التتبع بالمنتجات والمتاجر لتحفيز الانتشار.")
    
    col_ref1, col_ref2 = st.columns([2, 1])
    
    with col_ref1:
        st.markdown("#### إنشاء رابط إحالة مخصص (Deep Linking)")
        ref_user = st.text_input("معرف المستخدم (User ID):", placeholder="مثلاً: MR7-550")
        
        link_type = st.radio("نوع الربط:", ["رابط للمتجر العام", "رابط لمنتج محدد", "رابط لمتجر تاجر معين"])
        
        if link_type == "رابط لمنتج محدد":
            st.selectbox("اختر المنتج المستهدف:", ["دورة القيادة", "باقة التوسع", "أدوات الذكاء الاصطناعي"])
        elif link_type == "رابط لمتجر تاجر معين":
            st.text_input("معرف التاجر (Vendor ID):")
            
        if st.button("🚀 توليد رابط الإحالة"):
            generated_url = f"https://mr7.com/ref={ref_user or 'XXXX'}&target={link_type.replace(' ', '_')}"
            st.code(generated_url, language="text")
            st.success("الرابط جاهز للنشر وتتبع المبيعات!")

    with col_ref2:
        st.markdown("#### إحصائيات الروابط")
        st.markdown(f"""
        <div class="admin-card">
            <p>أكثر الروابط تحويلاً</p>
            <h4 style="color:{t['accent']};">MR7-VIP-001</h4>
            <p>1,240 مبيعة</p>
        </div>
        """, unsafe_allow_html=True)

# --- Tab 5: الأوسمة والترقيات ---
with tabs[4]:
    st.subheader("🏆 نظام الاستحقاق والجيميفيكيشن")
    with st.form("admin_badge_form"):
        st.text_input("اسم الوسام الجديد:")
        st.selectbox("أيقونة الوسام:", ["👑", "💎", "🚀", "⚡", "🔥"])
        st.number_input("نقاط XP المطلوبة:", min_value=0)
        if st.form_submit_button("إدراج الوسام في النظام"):
            st.success("تم التحديث!")

st.divider()

# العودة للرئيسية
if st.button("🏠 العودة للوحة التحكم الرئيسية"):
    st.switch_page("app.py")
