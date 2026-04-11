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
    ("دورات قيد المراجعة", "14", "📝"),
    ("معدل النمو", "+24%", "🚀")
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

tabs = st.tabs(["👥 إدارة المستخدمين", "🛒 مراقبة السوق", "💹 العمولات والمالية", "🏆 الأوسمة والترقيات"])

# --- Tab 1: إدارة المستخدمين ---
with tabs[0]:
    st.subheader("👥 إدارة قاعدة بيانات القادة")
    
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        st.text_input("بحث عن مستخدم (ID, Email, Name):", placeholder="أدخل بيانات البحث...")
    with col_filter:
        st.selectbox("الفلترة حسب الرتبة:", ["الكل", "أدمن", "مدرب", "متدرب", "قائد فريق"])

    user_data = [
        {"ID": "MR7-001", "الاسم": "أحمد علي", "الرتبة": "مدرب بلاتيني", "XP": "4500", "الحالة": "نشط ✅"},
        {"ID": "MR7-042", "الاسم": "سارة محمد", "الرتبة": "قائد ماسي", "XP": "2800", "الحالة": "نشط ✅"},
        {"ID": "MR7-105", "الاسم": "ياسين كريم", "الرتبة": "متدرب ناشئ", "XP": "120", "الحالة": "محظور 🚫"},
    ]
    st.table(user_data)
    
    with st.expander("🛠️ إجراءات إدارية سريعة"):
        u_id = st.text_input("أدخل ID المستخدم:")
        action = st.selectbox("الإجراء:", ["ترقية الرتبة", "تعديل XP", "حظر الحساب", "إرسال تنبيه خاص"])
        if st.button("تنفيذ الإجراء ⚡"):
            st.success(f"تم تنفيذ {action} للمستخدم {u_id}")

# --- Tab 2: مراقبة السوق (Marketplace Oversight) ---
with tabs[1]:
    st.subheader("🛒 مراجعة المنتجات والدورات")
    st.info("هناك 14 دورة جديدة تنتظر الموافقة للنشر في السوق العالمي.")
    
    pending_courses = [
        {"المدرب": "أحمد علي", "اسم الدورة": "هندسة التريليون", "السعر": "5000 EGP"},
        {"المدرب": "ليلى محمود", "اسم الدورة": "أسرار الفانل البيعي", "السعر": "1200 EGP"},
    ]
    for course in pending_courses:
        with st.expander(f"📋 مراجعة: {course['اسم الدورة']} - {course['المدرب']}"):
            st.write(f"السعر المطلوب: {course['السعر']}")
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # مثال لمعاينة الفيديو
            c1, c2 = st.columns(2)
            c1.button(f"✅ موافقة ونشر ({course['اسم الدورة']})")
            c2.button(f"❌ رفض مع ملاحظات ({course['اسم الدورة']})")

# --- Tab 3: العمولات والمالية ---
with tabs[2]:
    st.subheader("💹 الرقابة المالية والتدفقات النقدية")
    
    col_fin1, col_fin2 = st.columns(2)
    with col_fin1:
        st.markdown(f"""
        <div class="admin-card" style="border-color: #00FF88;">
            <h4 style="color: #00FF88;">طلبات سحب الأرباح قيد الانتظار</h4>
            <p style="font-size: 2rem; font-weight: 900;">120,500 EGP</p>
            <button style="width:100%; height:40px; border-radius:10px; background:#00FF88; border:none; color:black; font-weight:bold;">تحويل جماعي الآن 💸</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col_fin2:
        st.markdown(f"""
        <div class="admin-card" style="border-color: {t['accent']};">
            <h4 style="color: {t['accent']};">إجمالي عمولات النظام اليوم</h4>
            <p style="font-size: 2rem; font-weight: 900;">42,300 EGP</p>
            <p>صافي الربح بعد الضرائب والرسوم</p>
        </div>
        """, unsafe_allow_html=True)

# --- Tab 4: الأوسمة والترقيات (Master Gamification) ---
with tabs[3]:
    st.subheader("🏆 إدارة نظام الاستحقاق والجيميفيكيشن")
    
    with st.form("create_badge"):
        st.markdown("### إنشاء وسام أو رتبة جديدة")
        b_name = st.text_input("اسم الوسام:")
        b_icon = st.selectbox("الأيقونة:", ["🥇", "🥈", "🥉", "💎", "👑", "🚀", "🧠"])
        b_req = st.text_area("شروط الاستحقاق (XP, مبيعات، دورات):")
        b_points = st.number_input("نقاط XP إضافية عند الحصول عليه:", min_value=0)
        
        if st.form_submit_button("إضافة الوسام للنظام العالمي 🎖️"):
            st.success(f"تم إدراج وسام '{b_name}' بنجاح في المنظومة.")

st.divider()

# العودة للرئيسية
if st.button("🏠 العودة للوحة التحكم الرئيسية"):
    st.switch_page("app.py")
