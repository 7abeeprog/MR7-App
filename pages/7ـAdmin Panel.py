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

    .level-box {{
        background: rgba(255, 215, 0, 0.1);
        border: 1px solid {t['accent']};
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
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

# --- Tab 3: هندسة العمولات متعددة المستويات (MLM System) ---
with tabs[2]:
    st.subheader("💹 هندسة العمولات متعددة المستويات")
    st.markdown("قم بتصميم هيكلية الأرباح التضاعفية للمنظومة.")
    
    # اختيار نوع النظام
    sys_type = st.radio("نوع إعدادات العمولات:", ["النظام الأساسي (الافتراضي)", "تخصيص حسب المنتج"], horizontal=True)
    
    if sys_type == "تخصيص حسب المنتج":
        selected_prod = st.selectbox("اختر المنتج لتعديل عمولاته:", ["باقة القائد البلاتيني", "دورة عقلية المليار", "اشتراك الوكيل الذكي"])
        st.info(f"أنت الآن تقوم بتخصيص عمولات: {selected_prod}")

    # تحديد عدد المستويات
    num_levels = st.number_input("حدد عدد مستويات العمولة:", min_value=1, max_value=15, value=7)
    
    # القيم الافتراضية للنظام الأساسي (7 مستويات)
    default_rates = [10.0, 5.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    
    st.markdown("#### ضبط نسب المستويات (%)")
    level_cols = st.columns(4)
    final_rates = []
    
    for i in range(num_levels):
        col_idx = i % 4
        with level_cols[col_idx]:
            # استخدام القيمة الافتراضية إذا كان المستوى ضمن الـ 7 الأوائل
            default_val = default_rates[i] if i < len(default_rates) else 0.5
            rate = st.number_input(f"المستوى {i+1}", min_value=0.0, max_value=100.0, value=default_val, step=0.5, key=f"lvl_rate_{i}")
            final_rates.append(rate)
            
    st.divider()
    
    # ملخص التوزيع المالي
    total_commission = sum(final_rates)
    st.markdown(f"""
    <div style="background: rgba(0, 255, 136, 0.1); border: 2px solid #00FF88; padding: 20px; border-radius: 15px; text-align: center;">
        <h3 style="color: #00FF88; margin: 0;">إجمالي نسبة التوزيع المالي: {total_commission}%</h3>
        <p style="margin: 5px 0 0 0;">سيتم خصم هذه النسبة من سعر البيع لتوزيعها على شجرة الإحالة.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("💾 حفظ وتطبيق هيكلية العمولات"):
        with st.spinner("جاري تحديث عقود العمولات الذكية..."):
            time.sleep(1.5)
            st.success(f"تم اعتماد نظام الـ {num_levels} مستويات بنجاح!")

# --- Tab 4: روابط الإحالة وتتبع المتاجر (Referral & Deep Linking) ---
with tabs[3]:
    st.subheader("🔗 مركز إدارة روابط الإحالة والانتشار")
    st.info("توليد روابط ذكية مرتبطة بنظام المستويات المذكور في التبويب السابق.")
    
    col_ref1, col_ref2 = st.columns([2, 1])
    
    with col_ref1:
        st.markdown("#### توليد رابط إحالة استراتيجي")
        ref_user_id = st.text_input("معرف القائد (Leader ID):", placeholder="MR7-XXXX")
        
        link_target = st.selectbox("ربط الإحالة بـ:", ["المتجر العالمي بالكامل", "منتج تعليمي محدد", "متجر متدرب (Vendor Store)"])
        
        if link_target == "منتج تعليمي محدد":
            st.selectbox("اختر المنتج:", ["دورة القيادة", "باقة التوسع", "أدوات الذكاء الاصطناعي"])
        elif link_target == "متجر متدرب (Vendor Store)":
            st.text_input("معرف التاجر المستهدف (Vendor ID):")
            
        if st.button("🚀 إنشاء رابط التتبع"):
            # محاكاة الرابط
            ref_code = ref_user_id or "MASTER"
            final_url = f"https://mr7-app.com/marketplace?ref={ref_code}&source=admin_gen"
            st.code(final_url, language="text")
            st.success("الرابط نشط ومرتبط بنظام الـ 7 مستويات تلقائياً.")

    with col_ref2:
        st.markdown("#### إحصائيات الروابط الذكية")
        st.markdown(f"""
        <div class="admin-card">
            <p>أكثر رابط تم تداوله</p>
            <h4 style="color:{t['accent']};">MR7-GOLD-01</h4>
            <p style="font-size: 1.5rem; font-weight: 900;">2,450 نقرة</p>
            <p style="color: #00FF88;">معدل تحويل: 18%</p>
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
