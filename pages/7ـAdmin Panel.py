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

    .project-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 25px;
        padding: 25px;
        margin-bottom: 25px;
        transition: 0.4s ease;
    }}
    .project-card:hover {{ border-color: #00FF88; transform: translateY(-5px); }}

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

    .stProgress > div > div > div > div {{
        background-color: #00FF88 !important;
    }}
    
    .status-badge {{
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"### 🎨 تخصيص المظهر")
    theme_choice = st.selectbox("النمط الحالي:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    st.markdown("### 🏛️ رصيد الاستثمار")
    st.success("المحفظة الاستثمارية: 50,000 EGP")

# --- 2. إدارة البيانات مع إضافة حالة المشروع (Status) ---
if 'crowd_projects' not in st.session_state:
    st.session_state.crowd_projects = [
        {"title": "مزرعة الهيدروبونيك الذكية", "category": "زراعة ذكية", "owner": "م. يوسف القائد", "goal": 100000, "raised": 45000, "desc": "إنشاء أول مزرعة مائية مؤتمتة بالكامل بالذكاء الاصطناعي لإنتاج محاصيل عضوية عالية الجودة.", "status": "approved"},
        {"title": "منصة تعليم البرمجة للأطفال", "category": "تعليم تقني", "owner": "ليلى المبدعة", "goal": 50000, "raised": 48000, "desc": "تطبيق لتبسيط منطق البرمجة باستخدام الألعاب لجيل التريليون القادم.", "status": "approved"}
    ]

st.title("🤝 مجمع التمويل الجماعي")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.3rem; margin-top:-20px;'>دعم المشاريع الناشئة وتبادل الاستثمارات الاستراتيجية</p>", unsafe_allow_html=True)

st.divider()

tabs = st.tabs(["🌎 استكشاف المشاريع", "🚀 اطرح مشروعك باحترافية", "💰 استثماراتي", "📊 إحصائيات السوق"])

# --- Tab 1: استكشاف المشاريع (المعتمدة فقط) ---
with tabs[0]:
    st.subheader("🌎 منصة عرض أفكار النخبة")
    
    # فلترة المشاريع المعتمدة فقط
    approved_projects = [p for p in st.session_state.crowd_projects if p.get('status') == "approved"]
    
    if not approved_projects:
        st.info("لا توجد مشاريع معتمدة حالياً. كن أول من يطرح فكرة مليار دولار!")
    else:
        for idx, proj in enumerate(approved_projects):
            with st.container():
                st.markdown(f"""
                <div class="project-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <span style="background: {t['accent']}; color: black; padding: 2px 8px; border-radius: 5px; font-size: 0.8rem;">{proj.get('category', 'عام')}</span>
                            <h2 style="color: {t['accent']}; margin-top: 5px;">{proj['title']}</h2>
                        </div>
                        <span style="color: #888; font-size: 0.9rem;">👤 صاحب المشروع: {proj['owner']}</span>
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
                
                progress = min(proj['raised'] / proj['goal'], 1.0)
                st.progress(progress)
                
                col_in, col_btn = st.columns([1, 1])
                with col_in:
                    fund_amt = st.number_input(f"مبلغ التمويل (EGP):", min_value=100, key=f"amt_{idx}", step=500)
                with col_btn:
                    st.write("") # تعويض المسافة
                    if st.button(f"🤝 تمويل الآن", key=f"btn_{idx}"):
                        # تحديث المشروع الأصلي في القائمة الكبيرة
                        for original_p in st.session_state.crowd_projects:
                            if original_p['title'] == proj['title']:
                                original_p['raised'] += fund_amt
                        st.success(f"تم تسجيل استثمارك في {proj['title']}!")
                        time.sleep(1)
                        st.rerun()

# --- Tab 2: اطرح مشروعك (مع حالة الانتظار) ---
with tabs[1]:
    st.subheader("🚀 نموذج طرح المشروع الاستراتيجي")
    st.info("املأ البيانات التالية بعناية. سيتم مراجعة مشروعك من قبل الإدارة قبل نشره في السوق العالمي.")
    
    with st.form("professional_pitch"):
        col_t, col_c = st.columns(2)
        with col_t:
            p_title = st.text_input("اسم المشروع (العنوان الجاذب):")
        with col_c:
            p_cat = st.selectbox("تصنيف المشروع:", ["تقني (AI/Software)", "زراعي", "عقاري", "تعليمي", "تجاري", "صناعي"])
        
        p_goal = st.number_input("المبلغ المطلوب للتمويل الإجمالي (EGP):", min_value=1000, step=1000)
        p_summary = st.text_input("ملخص فكرة المشروع (Hook):")
        p_desc = st.text_area("شرح تفصيلي للمشروع وجدواه الاقتصادية:", height=150)
        p_risks = st.text_area("المخاطر والتحديات وكيفية مواجهتها:")
        p_timeline = st.text_input("الجدول الزمني المتوقع:")
        p_video = st.text_input("رابط فيديو تعريفي (يوتيوب):")
        
        if st.form_submit_button("إرسال المشروع للمراجعة والنشر 📤"):
            if p_title and p_desc and p_goal > 0:
                # إضافة المشروع بحالة "pending"
                st.session_state.crowd_projects.append({
                    "title": p_title, 
                    "category": p_cat,
                    "owner": "أنت (القائد الحالي)", 
                    "goal": p_goal, 
                    "raised": 0, 
                    "desc": f"{p_summary}\n\n{p_desc}",
                    "status": "pending"
                })
                st.success("تم إرسال مشروعك بنجاح! هو الآن قيد المراجعة الإدارية وسنقوم بإشعارك فور اعتماده.")
                st.balloons()
            else:
                st.error("يرجى التأكد من ملء الحقول الأساسية.")

# --- Tab 3: استثماراتي ---
with tabs[2]:
    st.subheader("💰 محفظة استثماراتي الجماعية")
    my_investments = [
        {"المشروع": "منصة تعليم البرمجة", "المبلغ المستثمر": "5,000 EGP", "النسبة من الهدف": "10%", "الحالة": "نشط ✅"},
    ]
    st.table(my_investments)
    
    # عرض حالة المشاريع التي طرحها المستخدم
    st.markdown("---")
    st.subheader("📤 مشاريعي المطروحة")
    my_projects = [p for p in st.session_state.crowd_projects if p['owner'] == "أنت (القائد الحالي)"]
    if my_projects:
        for p in my_projects:
            status_text = "قيد المراجعة ⏳" if p['status'] == "pending" else "معتمد ومتاح للتمويل ✅"
            st.write(f"- **{p['title']}**: {status_text}")
    else:
        st.caption("لم تقم بطرح أي مشاريع بعد.")

# --- Tab 4: إحصائيات السوق ---
with tabs[3]:
    st.subheader("📊 أداء سوق التمويل")
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي الضخ المالي", "245,000 EGP", "+15%")
    c2.metric("مشاريع معتمدة", f"{len(approved_projects)}", "+2")
    c3.metric("المستثمرون", "142", "🚀")

st.divider()

if st.button("👑 الانتقال للوحة التحكم العليا"):
    st.switch_page("pages/8_Admin_Panel.py")
