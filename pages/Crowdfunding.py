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
    /* التنسيق الإمبراطوري عالي الكثافة */
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
    }}
    .project-card:hover {{ border-color: #00FF88; transform: translateY(-10px); }}

    .country-tag {{
        background: rgba(0, 255, 136, 0.1);
        color: #00FF88 !important;
        border: 1px solid #00FF88;
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 900;
    }}

    /* حل مشكلة الكتابة باللون الأسود في الحقول البيضاء */
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
    </style>
    """, unsafe_allow_html=True)

# --- 2. قاعدة بيانات المشاريع الجغرافية (Geographic Strategy) ---
if 'crowd_projects' not in st.session_state:
    st.session_state.crowd_projects = [
        {
            "title": "مجمع السيارات الكهربائية (EV City)", 
            "category": "صناعة ثقيلة", 
            "country": "مصر",
            "desc": "إنشاء 600 مصنع متكامل لتوطين تكنولوجيا النقل الكهربائي. استثمار سيادي يعيد صياغة ريادة مصر الصناعية.", 
            "goal": 3600000000, "raised": 520000000, "roi": "24% سنوي"
        },
        {
            "title": "مبادرة الـ 20,000 مشروع صغرى", 
            "category": "تمكين ريادي", 
            "country": "ليبيا",
            "desc": "تمويل ودعم مشاريع الشباب الصغرى والمتوسطة في ليبيا لخلق اقتصاد تشاركي قوي وتوفير آلاف فرص العمل.", 
            "goal": 700000000, "raised": 95000000, "roi": "12% + أثر اجتماعي"
        },
        {
            "title": "سلة غذاء العرب (مشاريع زراعية)", 
            "category": "أمن غذائي", 
            "country": "السودان",
            "desc": "استصلاح أراضي زراعية شاسعة في السودان باستخدام تقنيات الري الذكي لضمان السيادة الغذائية للمنطقة العربية.", 
            "goal": 900000000, "raised": 45000000, "roi": "19% سنوي"
        },
        {
            "title": "مدينة النبت الذكية (Nabt City)", 
            "category": "مدن مستدامة", 
            "country": "عالمي",
            "desc": "أول نموذج عالمي للحياة المستدامة (كربون صفر) يعتمد على الطاقة النظيفة والذكاء الاصطناعي.", 
            "goal": 2000000000, "raised": 185000000, "roi": "18% سنوي"
        }
    ]

# --- 3. القائمة الجانبية (فلترة حسب طبيعة الدولة) ---
with st.sidebar:
    st.markdown(f"### 🎨 تخصيص المنظومة")
    theme_choice = st.selectbox("اختر الجو العام:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    
    st.markdown("### 🌍 نطاق العمليات")
    target_country = st.multiselect("عرض مشاريع دول مختارة:", ["مصر", "ليبيا", "السودان", "عالمي"], default=["مصر", "ليبيا", "السودان", "عالمي"])

# --- 4. واجهة مجمع التمويل الملياري ---
st.title("🤝 مجمع التمويل الملياري")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.4rem; margin-top:-25px;'>السيادة المالية من خلال المشاريع القومية العابرة للحدود</p>", unsafe_allow_html=True)

st.divider()

tabs = st.tabs(["🌎 ساحة المشاريع", "🚀 طرح رؤية سيادية", "💰 محفظتي الاستثمارية", "📊 تحليل السوق"])

# --- Tab 1: ساحة المشاريع (توزيع جغرافي) ---
with tabs[0]:
    st.subheader("🌎 استكشف فرص بناء الإمبراطورية")
    
    # الفلترة بناءً على الدول
    display_projects = [p for p in st.session_state.crowd_projects if p['country'] in target_country]
    
    if not display_projects:
        st.info("لا توجد مشاريع استثمارية نشطة في هذا النطاق الجغرافي حالياً.")
    else:
        for idx, proj in enumerate(display_projects):
            with st.container():
                st.markdown(f"""
                <div class="project-card">
                    <span class="country-tag">📍 {proj['country']}</span>
                    <h2 style="color: {t['accent']}; margin: 15px 0;">{proj['title']}</h2>
                    <p style="color: #ddd; line-height: 1.8; font-size: 1.1rem;">{proj['desc']}</p>
                    
                    <div style="display: flex; justify-content: space-between; margin: 20px 0; background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px;">
                        <div>
                            <p style="color: #888; font-size: 0.8rem; margin: 0;">العائد المتوقع</p>
                            <span style="color: #00FF88; font-size: 1.3rem;">{proj['roi']}</span>
                        </div>
                        <div style="text-align: right;">
                            <p style="color: #888; font-size: 0.8rem; margin: 0;">الميزانية المطلوبة</p>
                            <span style="font-size: 1.3rem;">${proj['goal']:,.0f}</span>
                        </div>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 5px;">
                        <span>تم جمع: ${proj['raised']:,.0f}</span>
                        <span>النسبة: {min(proj['raised']/proj['goal']*100, 100):.1f}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(min(proj['raised'] / proj['goal'], 1.0))
                
                col_amt, col_btn = st.columns([2, 1])
                with col_amt:
                    fund_val = st.number_input("مبلغ الضخ الاستثماري ($):", min_value=10, key=f"invest_{idx}", step=100)
                with col_btn:
                    st.write("") # مباعدة
                    if st.button("🤝 تأكيد المساهمة", key=f"btn_invest_{idx}"):
                        for original in st.session_state.crowd_projects:
                            if original['title'] == proj['title']:
                                original['raised'] += fund_val
                        st.success(f"تمت المساهمة! أنت الآن شريك في بناء '{proj['title']}'")
                        time.sleep(1.5)
                        st.rerun()

# --- Tab 2: طرح رؤية (Submission) ---
with tabs[1]:
    st.subheader("🚀 طرح رؤية اقتصادية للمراجعة السيادية")
    st.markdown("لديك رؤية لمشروع ملياري؟ قدمها لمكتب الدراسات الاستراتيجية في MR7.")
    
    with st.form("new_pitch"):
        p_name = st.text_input("اسم المشروع الاستراتيجي:")
        p_loc = st.selectbox("الدولة المستهدفة:", ["مصر", "ليبيا", "السودان", "عالمي"])
        p_goal = st.number_input("الميزانية التقديرية للتأسيس ($):", min_value=10000)
        p_desc = st.text_area("وصف الرؤية والناتج القومي المستهدف:", height=150)
        
        if st.form_submit_button("إرسال للمراجعة والتدقيق 📤"):
            if p_name and p_desc:
                st.success("تم استلام مسودة المشروع بنجاح. سيتم تحليل البيانات وإبلاغك بالنتيجة عبر التنبيهات.")
            else:
                st.error("يرجى إكمال تفاصيل الرؤية.")

# --- Tab 3: أصولي (Portfolio) ---
with tabs[2]:
    st.subheader("💰 محفظة أصول السيادة")
    st.table([
        {"المشروع": "مجمع السيارات الكهربائية", "المساهمة": "$5,000", "الحصة": "0.00014%", "العائد": "قيد التأسيس"},
        {"المشروع": "مشاريع ليبيا الصغرى", "المساهمة": "$1,000", "الحصة": "0.00014%", "العائد": "+$450 (موزع)"}
    ])

# --- Tab 4: تحليل السوق ---
with tabs[3]:
    st.subheader("📊 أداء المحرك المالي العام")
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي الضخ العالمي", "$6.1B", "+15% شهرية")
    c2.metric("عدد المشاريع النشطة", "142", "✅")
    c3.metric("معدل نجاح المشاريع", "94%", "فائق")

st.divider()

if st.button("🏰 العودة لمركز القيادة"):
    st.switch_page("app.py")
