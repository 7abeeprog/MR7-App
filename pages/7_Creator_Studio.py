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

    .studio-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 25px;
        padding: 30px;
        margin-bottom: 25px;
        transition: 0.4s ease;
    }}
    .studio-card:hover {{ border-color: #00FF88; transform: translateY(-5px); }}

    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 15px !important;
        height: 60px;
    }}

    /* تحسين شكل القوائم المنسدلة */
    div[data-baseweb="select"] > div {{ background-color: {t['select_bg']} !important; color: {t['select_text']} !important; }}
    div[data-baseweb="popover"] li {{ color: {t['select_text']} !important; background-color: {t['select_bg']} !important; }}
    
    /* تنسيق منطقة الإدخال */
    .stTextInput input, .stTextArea textarea {{
        background-color: rgba(255,255,255,0.05) !important;
        color: {t['text']} !important;
        border: 2px solid {t['border']} !important;
        border-radius: 15px !important;
    }}
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
    st.markdown("### 🛠️ حالة الاستوديو")
    st.info("سعة التخزين: 10GB / 50GB")
    st.success("حساب صانع محتوى موثق ✅")

# --- 3. واجهة استوديو بناء المحتوى ---
st.title("🎬 استوديو بناء المحتوى")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.3rem; margin-top:-20px;'>حول خبرتك القيادية إلى إرث تعليمي عالمي</p>", unsafe_allow_html=True)

st.divider()

# إدارة تبويبات الاستوديو
tabs = st.tabs(["🏗️ بناء دورة جديدة", "📊 أداء المحتوى", "📦 مكتبة الوسائط", "💡 نصائح الإبداع"])

# --- Tab 1: بناء دورة جديدة ---
with tabs[0]:
    st.subheader("🏗️ مصنع الدورات الاستراتيجية")
    
    with st.container():
        st.markdown(f"""
        <div class="studio-card">
            <h4 style="color: {t['accent']};">1. أساسيات الدورة</h4>
        </div>
        """, unsafe_allow_html=True)
        
        c_name = st.text_input("عنوان الدورة (مثال: أسرار القيادة العشرية):")
        c_desc = st.text_area("وصف الدورة والقيمة المضافة للمتدربين:")
        c_price = st.number_input("السعر المقترح في المركز التجاري ($):", min_value=1, value=100)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown(f"""
        <div class="studio-card">
            <h4 style="color: {t['accent']};">2. هيكلة المحتوى</h4>
        </div>
        """, unsafe_allow_html=True)
        
        lesson_count = st.number_input("عدد الدروس المخطط لها:", min_value=1, max_value=50, value=5)
        
        for i in range(lesson_count):
            with st.expander(f"📖 الدرس رقم {i+1}"):
                st.text_input(f"عنوان الدرس {i+1}:", key=f"l_title_{i}")
                st.file_uploader(f"ارفع فيديو أو ملف الدرس {i+1}:", key=f"l_file_{i}")
                st.text_area(f"ملخص سريع للدرس {i+1}:", key=f"l_desc_{i}")

    st.divider()
    if st.button("🚀 إطلاق الدورة للمراجعة والنشر"):
        with st.spinner("يتم الآن ضغط الوسائط وتجهيز النسخة الرقمية..."):
            time.sleep(3)
            st.success("تم إرسال دورتك بنجاح! سيتم فحصها ونشرها في المركز التجاري خلال 24 ساعة.")
            st.balloons()

# --- Tab 2: أداء المحتوى ---
with tabs[1]:
    st.subheader("📊 إحصائيات صناعة التأثير")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="studio-card">
            <p>إجمالي المتدربين</p>
            <div style="font-size: 2rem; color: #00FF88;">452</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="studio-card">
            <p>أرباح المحتوى</p>
            <div style="font-size: 2rem; color: {t['accent']};">$12,400</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="studio-card">
            <p>تقييم الجودة</p>
            <div style="font-size: 2rem; color: #00FF88;">4.9 / 5</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 📈 الرسم البياني للمبيعات")
    st.line_chart([10, 25, 45, 30, 60, 85, 120])
    st.caption("نمو مبيعات دوراتك خلال الـ 6 أشهر الماضية.")

# --- Tab 3: مكتبة الوسائط ---
with tabs[2]:
    st.subheader("📦 أرشيف ملفاتك")
    st.info("هنا يتم تخزين كافة الملفات واللقطات التي رفعتها لاستخدامها في دورات متعددة.")
    
    files = [
        {"الاسم": "مقدمة_القيادة.mp4", "الحجم": "450MB", "النوع": "Video"},
        {"الاسم": "خطة_العمل.pdf", "الحجم": "2MB", "النوع": "Document"},
        {"الاسم": "شعار_الدورة.png", "الحجم": "150KB", "النوع": "Image"},
    ]
    st.table(files)
    st.button("➕ رفع ملفات جديدة للمكتبة")

# --- Tab 4: نصائح الإبداع ---
with tabs[3]:
    st.subheader("💡 أسرار إنتاج المحتوى الملياري")
    
    st.markdown(f"""
    <div class="studio-card" style="border-color: {t['accent']};">
        <h4 style="color: {t['accent']};">قاعدة الـ 10 دقائق ⏱️</h4>
        <p>الأبحاث تشير إلى أن تركيز المتدرب يبدأ في الانخفاض بعد 10 دقائق. اجعل دروسك مركزة، سريعة، ومليئة بالمعلومات العملية.</p>
    </div>
    
    <div class="studio-card" style="border-color: #00FF88;">
        <h4 style="color: #00FF88;">التفاعل هو المفتاح 🤝</h4>
        <p>لا تكتفِ بالشرح؛ ضع تحدياً عملياً في نهاية كل درس. الدورات التي تحتوي على مهام عملية تحقق مبيعات أعلى بنسبة 40%.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# العودة أو الانتقال للأدمن
c_back, c_next = st.columns(2)
with c_back:
    if st.button("👥 العودة لإدارة الفرق"):
        st.switch_page("pages/6_Teams.py")
with c_next:
    if st.button("👑 لوحة التحكم العليا (Admin)"):
        st.switch_page("pages/8_Admin_Panel.py")
