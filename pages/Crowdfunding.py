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

    /* تصميم بطاقة المشروع */
    .project-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 25px;
        padding: 25px;
        margin-bottom: 25px;
        transition: 0.4s ease;
    }}
    .project-card:hover {{ border-color: #00FF88; transform: translateY(-5px); }}

    /* حل مشكلة الكتابة (نص أسود على خلفية بيضاء) */
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
        height: 55px;
    }}

    /* تنسيق شريط التقدم المالي */
    .stProgress > div > div > div > div {{
        background-color: #00FF88 !important;
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
    st.markdown("### 🏛️ رصيد الاستثمار")
    st.success("المحفظة الاستثمارية: 50,000 EGP")
    st.info("عدد المشاريع الممولة: 3")

# --- 3. إدارة البيانات (Mock Database) ---
if 'crowd_projects' not in st.session_state:
    st.session_state.crowd_projects = [
        {"title": "مزرعة الهيدروبونيك الذكية", "owner": "م. يوسف القائد", "goal": 100000, "raised": 45000, "desc": "إنشاء أول مزرعة مائية مؤتمتة بالكامل بالذكاء الاصطناعي لإنتاج محاصيل عضوية."},
        {"title": "منصة تعليم البرمجة للأطفال", "owner": "ليلى المبدعة", "goal": 50000, "raised": 48000, "desc": "تطبيق لتبسيط منطق البرمجة باستخدام الألعاب لجيل التريليون القادم."}
    ]

# --- 4. واجهة التمويل الجماعي ---
st.title("🤝 مجمع التمويل الجماعي")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.3rem; margin-top:-20px;'>نظام دعم المشاريع الناشئة وتبادل الاستثمارات القيادية</p>", unsafe_allow_html=True)

st.divider()

tabs = st.tabs(["🌎 استكشاف المشاريع", "🚀 اطرح مشروعك", "💰 استثماراتي", "📊 إحصائيات السوق"])

# --- Tab 1: استكشاف المشاريع ---
with tabs[0]:
    st.subheader("🌎 منصة عرض أفكار النخبة")
    st.info("تصفح المشاريع المتاحة وكن شريكاً في قصة نجاح قادمة.")
    
    for idx, proj in enumerate(st.session_state.crowd_projects):
        with st.container():
            st.markdown(f"""
            <div class="project-card">
                <div style="display: flex; justify-content: space-between;">
                    <h2 style="color: {t['accent']};">{proj['title']}</h2>
                    <span style="background: {t['accent']}; color: black; padding: 2px 10px; border-radius: 10px; font-weight: bold; height: 25px;">👤 {proj['owner']}</span>
                </div>
                <p style="color: #ccc; margin-top: 10px;">{proj['desc']}</p>
                <div style="margin: 20px 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span>الهدف: {proj['goal']:,} EGP</span>
                        <span>تم جمع: {proj['raised']:,} EGP</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # حساب التقدم
            progress = min(proj['raised'] / proj['goal'], 1.0)
            st.progress(progress)
            
            c1, c2 = st.columns([1, 1])
            with c1:
                fund_amt = st.number_input(f"مبلغ الاستثمار (EGP):", min_value=100, key=f"amt_{idx}")
            with c2:
                if st.button(f"🤝 تمويل المشروع الآن", key=f"btn_{idx}"):
                    proj['raised'] += fund_amt
                    st.success(f"مبارك! لقد أصبحت شريكاً في {proj['title']}. سيتم التواصل معك من قبل صاحب المشروع.")
                    time.sleep(1)
                    st.rerun()

# --- Tab 2: اطرح مشروعك (Pitch Your Project) ---
with tabs[1]:
    st.subheader("🚀 بوابة طرح المشاريع الاستراتيجية")
    st.markdown("قدم مشروعك بشكل احترافي لجذب استثمارات القادة.")
    
    with st.form("pitch_form"):
        p_title = st.text_input("اسم المشروع:")
        p_goal = st.number_input("المبلغ المطلوب للتمويل (EGP):", min_value=1000)
        p_desc = st.text_area("وصف المشروع ودراسة الجدوى المختصرة:")
        p_video = st.text_input("رابط فيديو تعريفي (يوتيوب):", placeholder="اشرح فكرتك في دقيقتين...")
        
        if st.form_submit_button("إرسال المشروع للمراجعة والنشر 📤"):
            if p_title and p_desc:
                st.session_state.crowd_projects.append({
                    "title": p_title, "owner": "أنت (القائد الحالي)", 
                    "goal": p_goal, "raised": 0, "desc": p_desc
                })
                st.success("تم إدراج مشروعك بنجاح! سيتم إخطار جميع قادة المنظومة لبدء التمويل.")
                st.balloons()
            else:
                st.error("يرجى إكمال جميع بيانات المشروع.")

# --- Tab 3: استثماراتي ---
with tabs[2]:
    st.subheader("💰 محفظة استثماراتي الجماعية")
    st.info("هنا يمكنك متابعة المشاريع التي قمت بتمويلها وتطور نموها.")
    
    my_investments = [
        {"المشروع": "منصة تعليم البرمجة", "المبلغ المستثمر": "5,000 EGP", "العائد المتوقع": "15%", "الحالة": "قيد التنفيذ 🛠️"},
    ]
    st.table(my_investments)

# --- Tab 4: إحصائيات السوق ---
with tabs[3]:
    st.subheader("📊 أداء سوق التمويل الجماعي")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("إجمالي التمويلات", "245,000 EGP", "+15%")
    with col2:
        st.metric("مشاريع مكتملة", "8", "+2")
    with col3:
        st.metric("المستثمرون النشطون", "142", "🚀")

st.divider()

# العودة للأدمن أو الرئيسية
if st.button("👑 الانتقال للوحة التحكم العليا"):
    st.switch_page("pages/8_Admin_Panel.py")
