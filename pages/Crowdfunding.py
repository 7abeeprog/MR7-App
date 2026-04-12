import streamlit as st
import time
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
    /* الفلسفة التصميمية: احترافية Enterprise وكثافة بيانات */
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
        filter: drop-shadow(0 0 12px {t['accent']}); 
        font-size: 3.5rem !important; 
    }}

    .project-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 30px;
        padding: 35px;
        margin-bottom: 30px;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        box-shadow: 0 15px 45px rgba(0,0,0,0.5);
    }}
    .project-card:hover {{ border-color: #00FF88; transform: translateY(-10px); box-shadow: 0 20px 60px rgba(0,255,136,0.15); }}

    .country-badge {{
        background: rgba(0, 255, 136, 0.1);
        color: #00FF88 !important;
        border: 1px solid #00FF88;
        padding: 4px 15px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 900;
    }}

    .metric-box {{
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        border-bottom: 3px solid {t['accent']};
    }}

    /* حل مشكلة الكتابة باللون الأسود */
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
        font-size: 1.1rem;
    }}

    .stProgress > div > div > div > div {{
        background-color: #00FF88 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات الاستراتيجية المتوسعة ---
if 'crowd_projects' not in st.session_state:
    st.session_state.crowd_projects = [
        {
            "title": "مدينة النبت الذكية (Nabt Smart City)", 
            "category": "مدن مستدامة وكربون صفر", 
            "country": "مصر / عالمي",
            "type": "سيادي استراتيجي",
            "goal": 2000000000, 
            "raised": 185000000, 
            "roi": "18% سنوي",
            "risk": "منخفض",
            "desc": "أضخم مشروع للمدن المستدامة بملياري دولار. يعتمد على الزراعة الذكية وتوليد الطاقة النظيفة، مصمم ليكون نموذجاً قابلاً للتكرار 100 مرة في عواصم القارات.", 
            "status": "approved"
        },
        {
            "title": "مجمع السيارات الكهربائية (EV City Hub)", 
            "category": "تصنيع ثقيل وتكنولوجيا", 
            "country": "مصر",
            "type": "صناعي إنتاجي",
            "goal": 3600000000, 
            "raised": 520000000, 
            "roi": "24% سنوي",
            "risk": "متوسط",
            "desc": "تأسيس 600 مصنع متكامل لتوطين صناعة النقل الكهربائي في الشرق الأوسط وأفريقيا، بهدف السيطرة على سلاسل التوريد الإقليمية.", 
            "status": "approved"
        },
        {
            "title": "مبادرة الـ 20,000 مشروع صغرى", 
            "category": "تمكين مجتمعي وتجزئة", 
            "country": "ليبيا / السودان",
            "type": "تنمية قاعدية",
            "goal": 700000000, 
            "raised": 92000000, 
            "roi": "12% سنوي + أثر مجتمعي",
            "risk": "منخفض جداً",
            "desc": "محفز مالي يستهدف رواد الأعمال في ليبيا والسودان لإنشاء مشاريع إنتاجية صغيرة ومتوسطة، مع توفير الدعم اللوجستي والتقني من MR7.", 
            "status": "approved"
        },
        {
            "title": "مركز سيادة البيانات الأفريقي", 
            "category": "بنية تحتية رقمية", 
            "country": "عالمي",
            "type": "تقني سيادي",
            "goal": 500000000, 
            "raised": 45000000, 
            "roi": "21% سنوي",
            "risk": "متوسط",
            "desc": "بناء مراكز بيانات عملاقة لتخزين ومعالجة بيانات القارة الأفريقية محلياً، مما يضمن الاستقلال الرقمي والسيادة المعلوماتية.", 
            "status": "approved"
        }
    ]

# --- 3. الشريط الجانبي (الفلترة الذكية حسب الدولة) ---
with st.sidebar:
    st.markdown(f"### 🎨 النمط الإمبراطوري")
    theme_choice = st.selectbox("الجو العام:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    
    st.markdown("### 🌍 تصفية النطاق الجغرافي")
    country_filter = st.multiselect(
        "اختر الدول المستهدفة:", 
        ["مصر", "ليبيا", "السودان", "عالمي"],
        default=["مصر", "ليبيا", "السودان", "عالمي"]
    )
    
    st.divider()
    st.markdown("### 🏛️ محفظة السيادة")
    st.metric("رصيدك الاستثماري", "50,000 $", "+2.4% أرباح")

# --- 4. واجهة مجمع التمويل الملياري ---
st.title("🤝 مجمع التمويل الملياري")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.4rem; margin-top:-25px;'>محرك الاستثمار السيادي لنهضة اقتصاد القادة</p>", unsafe_allow_html=True)

st.divider()

# تبويبات الأنظمة الاحترافية
tabs = st.tabs(["🌎 استكشاف المشاريع الكبرى", "🚀 طرح رؤية استثمارية", "💰 أصولي وعوائدي", "📊 تحليلات السوق"])

# --- Tab 1: استكشاف المشاريع (Enterprise Style) ---
with tabs[0]:
    st.subheader("🌎 الساحة الاستثمارية العالمية")
    st.info("قم بفلترة المشاريع بناءً على المخاطر، العوائد، أو الموقع الجغرافي.")
    
    # منطق الفلترة المتقدم
    display_projects = [
        p for p in st.session_state.crowd_projects 
        if any(country in p['country'] for country in country_filter) and p.get('status') == "approved"
    ]
    
    if not display_projects:
        st.warning("لا توجد مشاريع استثمارية نشطة في هذا النطاق حالياً.")
    else:
        for idx, proj in enumerate(display_projects):
            with st.container():
                st.markdown(f"""
                <div class="project-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <span class="country-badge">📍 {proj['country']}</span>
                            <span style="color: {t['accent']}; margin-right: 10px; font-size: 0.8rem;">[{proj['type']}]</span>
                            <h2 style="color: {t['accent']}; margin: 10px 0;">{proj['title']}</h2>
                        </div>
                        <div style="text-align: right;">
                            <p style="color: #00FF88; font-size: 1.2rem; margin: 0;">العائد: {proj['roi']}</p>
                            <p style="color: #888; font-size: 0.8rem;">المخاطر: {proj['risk']}</p>
                        </div>
                    </div>
                    
                    <p style="color: #ddd; line-height: 1.8; margin: 20px 0; font-size: 1.1rem;">{proj['desc']}</p>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; background: rgba(0,0,0,0.3); padding: 20px; border-radius: 20px;">
                        <div>
                            <p style="color: #888; font-size: 0.8rem; margin: 0;">الهدف المالي</p>
                            <span style="font-size: 1.5rem;">${proj['goal']:,.0f}</span>
                        </div>
                        <div style="text-align: right;">
                            <p style="color: #888; font-size: 0.8rem; margin: 0;">التمويل المجموع</p>
                            <span style="font-size: 1.5rem; color: #00FF88;">${proj['raised']:,.0f}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # شريط التقدم والتمويل
                progress = min(proj['raised'] / proj['goal'], 1.0)
                st.progress(progress)
                
                col_amt, col_btn = st.columns([2, 1])
                with col_amt:
                    fund_val = st.number_input("مبلغ الضخ المالي ($):", min_value=10, key=f"invest_{idx}", step=500)
                with col_btn:
                    st.write("") # مباعدة
                    if st.button("🤝 تأكيد الاستثمار السيادي", key=f"btn_invest_{idx}"):
                        for original in st.session_state.crowd_projects:
                            if original['title'] == proj['title']:
                                original['raised'] += fund_val
                        st.success(f"تمت المساهمة! أنت الآن شريك رسمي في '{proj['title']}'")
                        time.sleep(1.5)
                        st.rerun()

# --- Tab 2: طرح رؤية (Submission) ---
with tabs[1]:
    st.subheader("🚀 طرح رؤية اقتصادية للمراجعة السيادية")
    st.markdown("حول فكرتك إلى مشروع ملياري مدعوم من جيش القادة.")
    
    with st.form("pitch_empire_form"):
        p_name = st.text_input("اسم المشروع الاستراتيجي:")
        p_loc = st.selectbox("الدولة الرئيسية للعمليات:", ["مصر", "ليبيا", "السودان", "الجزائر", "عالمي"])
        p_goal = st.number_input("الميزانية التقديرية للتأسيس ($):", min_value=5000)
        p_roi = st.text_input("العائد السنوي المتوقع (Expected ROI %):", placeholder="مثلاً: 15%")
        p_desc = st.text_area("وصف الرؤية والناتج القومي المستهدف:", height=150)
        
        if st.form_submit_button("إرسال للمراجعة والتدقيق الإمبراطوري 📤"):
            if p_name and p_desc:
                st.success("تم استلام مسودة المشروع بنجاح. سيتم تحليل البيانات من قبل 'العقل المركزي' وإبلاغك بالنتيجة.")
            else:
                st.error("يرجى ملء كافة تفاصيل الرؤية.")

# --- Tab 3: أصولي (Portfolio) ---
with tabs[2]:
    st.subheader("💰 محفظة أصولك السيادية")
    col_st1, col_st2 = st.columns(2)
    with col_st1:
        st.markdown(f'<div class="metric-box"><p>إجمالي استثماراتك</p><h2 style="color:{t["accent"]};">$6,000</h2></div>', unsafe_allow_html=True)
    with col_st2:
        st.markdown(f'<div class="metric-box"><p>العائد التراكمي المحقق</p><h2 style="color:#00FF88;">$450</h2></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.table([
        {"المشروع": "مجمع السيارات الكهربائية", "المبلغ": "$5,000", "الحصة": "0.00014%", "العائد": "قيد الإنتاج"},
        {"المشروع": "مبادرة صغرى ليبيا", "المبلغ": "$1,000", "الحصة": "0.00014%", "العائد": "+$450 (موزع)"}
    ])

# --- Tab 4: التحليلات (Analytics) ---
with tabs[3]:
    st.subheader("📊 أداء المحرك المالي العالمي (MR7 Stats)")
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي الضخ السنوي", "$6.1B", "+15% شهرية")
    c2.metric("عدد المشاريع النشطة", "142", "✅")
    c3.metric("المستثمرون الفاعلون", "1.2M", "🚀")
    
    st.divider()
    st.markdown("### 🗺️ توزيع تدفقات السيولة الجغرافية")
    # محاكاة توزيع جغرافي
    st.write("مصر (45%)")
    st.progress(0.45)
    st.write("ليبيا (25%)")
    st.progress(0.25)
    st.write("السودان (20%)")
    st.progress(0.20)
    st.write("عالمي (10%)")
    st.progress(0.10)

st.divider()

if st.button("🏰 العودة لمركز القيادة الرئيسي"):
    st.switch_page("app.py")
