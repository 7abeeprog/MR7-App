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

    /* حل مشكلة الكتابة (نص أسود على خلفية بيضاء) */
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid {t['border']} !important;
        border-radius: 12px !important;
        font-weight: bold !important;
    }}
    
    /* تنسيق الرتب والأوسمة */
    .rank-badge {{
        background: linear-gradient(135deg, {t['accent']}, #FFFFFF);
        color: #000 !important;
        padding: 10px 20px;
        border-radius: 50px;
        font-weight: 900;
        display: inline-block;
        margin: 10px 0;
        box-shadow: 0 0 15px {t['accent']};
    }}

    .badge-container {{
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        background: rgba(255,255,255,0.05);
        border: 1px solid {t['border']};
        transition: 0.3s;
    }}
    .badge-container:hover {{ transform: scale(1.05); border-color: #00FF88; }}

    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 15px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات (Gamification Stats) ---
if 'creator_xp' not in st.session_state:
    st.session_state.creator_xp = 1250
if 'sections' not in st.session_state:
    st.session_state.sections = [{"title": "القسم التمهيدي", "lessons": []}]

# دالة لتحديد رتبة المبدع
def get_rank(xp):
    if xp < 500: return "مبدع ناشئ 🌱", "🥉"
    if xp < 2000: return "خبير محتوى 📚", "🥈"
    if xp < 5000: return "ماستر استراتيجي 💎", "🥇"
    return "أسطورة التريليون 👑", "🌌"

rank_name, rank_icon = get_rank(st.session_state.creator_xp)

# --- 3. القائمة الجانبية ---
with st.sidebar:
    st.markdown(f"### 🎨 تخصيص المظهر")
    theme_choice = st.selectbox("النمط الحالي:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    st.markdown(f"### 🏆 مركز قوتك")
    st.markdown(f"<div class='rank-badge'>{rank_icon} {rank_name}</div>", unsafe_allow_html=True)
    st.progress(min(st.session_state.creator_xp / 5000, 1.0))
    st.caption(f"نقاط الخبرة الحالية: {st.session_state.creator_xp} XP")

# --- 4. واجهة الاستوديو ---
st.title("🎬 استوديو بناء المحتوى")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.3rem; margin-top:-20px;'>نظام هندسة المناهج المتكامل والأوسمة القيادية</p>", unsafe_allow_html=True)

st.divider()

tabs = st.tabs(["🏗️ هيكلة الدورة", "📝 الاختبارات", "📜 الشهادات والترقية", "📊 الأداء والجيميفيكيشن"])

# --- Tab 1: هيكلة الدورة ---
with tabs[0]:
    st.subheader("🏗️ مصنع المناهج الاحترافي")
    
    with st.expander("⚙️ إعدادات الهوية المالية", expanded=True):
        c_title = st.text_input("اسم الدورة العالمي (للمتجر):")
        col_curr, col_price = st.columns([1, 2])
        with col_curr:
            currency = st.selectbox("العملة المحلية:", ["EGP (جنيه مصري)", "USD (دولار)", "SAR (ريال سعودي)"])
            sym = currency.split(' ')[0]
        with col_price:
            st.number_input(f"سعر البيع المقترح ({sym}):", min_value=0)

    st.markdown("---")
    
    for s_idx, section in enumerate(st.session_state.sections):
        with st.container():
            st.markdown(f"<div class='studio-card' style='border-right: 5px solid {t['accent']};'>", unsafe_allow_html=True)
            section['title'] = st.text_input(f"عنوان القسم {s_idx + 1}:", value=section['title'], key=f"s_{s_idx}")
            
            for l_idx, lesson in enumerate(section['lessons']):
                with st.expander(f"📖 الدرس {l_idx + 1}: {lesson.get('title', 'غير معنون')}"):
                    lesson['title'] = st.text_input("عنوان الدرس:", key=f"lt_{s_idx}_{l_idx}")
                    lesson['yt'] = st.text_input("رابط يوتيوب (Video ID or Link):", key=f"ly_{s_idx}_{l_idx}")
                    if lesson['yt']:
                        st.video(lesson['yt'])
            
            if st.button(f"➕ إضافة درس جديد للقسم {s_idx + 1}", key=f"al_{s_idx}"):
                section['lessons'].append({"title": "درس جديد", "yt": ""})
                st.session_state.creator_xp += 15
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    if st.button("➕ إضافة قسم استراتيجي جديد"):
        st.session_state.sections.append({"title": "قسم جديد", "lessons": []})
        st.session_state.creator_xp += 50
        st.rerun()

# --- Tab 2: الاختبارات ---
with tabs[1]:
    st.subheader("📝 تصميم اختبارات التميز")
    st.info("قم بوضع أسئلة ذكية لقياس استيعاب المتدربين لعمق المنظومة.")
    
    with st.container():
        st.markdown("<div class='studio-card'>", unsafe_allow_html=True)
        q_text = st.text_input("نص السؤال القيادي:")
        c1, c2 = st.columns(2)
        ans1 = c1.text_input("الخيار الأول:")
        ans2 = c2.text_input("الخيار الثاني:")
        correct = st.selectbox("حدد الإجابة الصحيحة لتفعيل التصحيح التلقائي:", [ans1, ans2])
        
        if st.button("📥 حفظ السؤال +30 XP"):
            st.session_state.creator_xp += 30
            st.success("تم إضافة السؤال وتحديث رصيد خبرتك!")
        st.markdown("</div>", unsafe_allow_html=True)

# --- Tab 3: الشهادات والترقية (Promotion System) ---
with tabs[2]:
    st.subheader("📜 نظام الشهادات والترقية التلقائي")
    
    col_st, col_inst = st.columns(2)
    
    with col_st:
        st.markdown("#### 🎓 للمتدرب")
        st.write("حدد شروط الحصول على وسام الإتمام:")
        st.checkbox("اجتياز الاختبار بنسبة 80% فأكثر", value=True)
        st.checkbox("مشاهدة 100% من فيديوهات الدورة")
        if st.button("👁️ معاينة شهادة المتدرب"):
            st.markdown(f"""
            <div style="background: white; color: black; padding: 40px; border: 10px solid {t['accent']}; text-align: center; border-radius: 10px;">
                <h1 style="color: black !important; font-size: 30px !important;">شهادة استحقاق MR7</h1>
                <p>تمنح للمتدرب المثالي تقديراً لإتمامه:</p>
                <h2 style="color: {t['accent']} !important;">{c_title if c_title else 'دورة القيادة'}</h2>
                <p>توقيع الإدارة</p>
            </div>
            """, unsafe_allow_html=True)

    with col_inst:
        st.markdown("#### 👑 للمدرب (ترقية الرتبة)")
        st.write("متطلبات الرتبة التالية:")
        st.write("- **الهدف:** الوصول لـ 2000 XP")
        st.write("- **المتبقي:** 750 XP")
        st.write("- **الامتيازات:** ظهور دورتك في الصفحة الأولى للمتجر.")

# --- Tab 4: الأداء والجيميفيكيشن (Badges) ---
with tabs[3]:
    st.subheader("📊 لوحة الأوسمة والإنجازات")
    
    # أوسمة المدرب
    st.markdown("### 🎖️ أوسمة المبدع (Instructor Badges)")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown("<div class='badge-container'>🥇<br><b>مؤسس المناهج</b><br><small>إنشاء أول دورة</small></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='badge-container'>👥<br><b>المعلم الملهم</b><br><small>100+ طالب</small></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='badge-container' style='opacity: 0.3;'>💰<br><b>تاجر التريليون</b><br><small>أرباح $10k+</small></div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='badge-container'>⭐<br><b>الجودة الفائقة</b><br><small>تقييم 5 نجوم</small></div>", unsafe_allow_html=True)

    st.divider()
    
    # أوسمة المتدرب (كيف يراها المدرب)
    st.markdown("### 🎓 أوسمة المتدربين (Student Badges)")
    st.info("هذه الأوسمة تمنح تلقائياً لطلابك لتحفيزهم على الإكمال.")
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.markdown("<div class='badge-container'>🚀<br><b>المنطلق السريع</b><br><small>إكمال أول قسم في يوم</small></div>", unsafe_allow_html=True)
    with sc2:
        st.markdown("<div class='badge-container'>🧠<br><b>العقل الذهبي</b><br><small>100% في الاختبار</small></div>", unsafe_allow_html=True)
    with sc3:
        st.markdown("<div class='badge-container'>💬<br><b>القائد المتفاعل</b><br><small>أكثر من 10 تعليقات</small></div>", unsafe_allow_html=True)

st.divider()

if st.button("🚀 نشر الدورة وتوزيع الأوسمة"):
    with st.spinner("جاري برمجة نظام المكافآت ورفع المحتوى..."):
        time.sleep(2)
        st.balloons()
        st.success("تم النشر بنجاح! دورتك الآن تدعم نظام الجيميفيكيشن بالكامل.")

if st.button("👑 الانتقال للوحة التحكم العليا (Admin)"):
    st.switch_page("pages/8_Admin_Panel.py")
