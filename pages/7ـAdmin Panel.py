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
    /* الفلسفة التصميمية: مركز القيادة والتحكم (The Command Center) */
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

    .admin-stat-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 25px;
        padding: 25px;
        text-align: center;
        transition: 0.3s;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .admin-stat-card:hover {{ border-color: #00FF88; transform: translateY(-5px); }}

    .approval-box {{
        background: rgba(255,255,255,0.03);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        border-right: 5px solid {t['accent']};
    }}

    /* تصميم بطاقات الذكاء الاصطناعي */
    .ai-insight-card {{
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(0,0,0,0.8) 100%);
        border: 1px solid #00FF88;
        border-radius: 20px;
        padding: 20px;
        margin-top: 15px;
    }}

    /* حل مشكلة الكتابة بالأسود */
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

# --- 2. إدارة البيانات (Master Admin State) ---
if 'crowd_projects' not in st.session_state:
    st.session_state.crowd_projects = []

# --- 3. الشريط الجانبي ---
with st.sidebar:
    st.markdown(f"### 🎨 تخصيص المنظومة")
    theme_choice = st.selectbox("نمط الإدارة:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    st.markdown("### 👑 رتبة الوصول")
    st.warning("Root Admin: MR7-GOD-MODE")
    st.success("حالة السيرفر: 99.9% Up-time")

# --- 4. واجهة لوحة التحكم العليا ---
st.title("👑 لوحة التحكم العليا")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.4rem; margin-top:-25px;'>إدارة أركان الإمبراطورية وهندسة السيادة العالمية</p>", unsafe_allow_html=True)

st.divider()

# مؤشرات السيادة (Global KPIs)
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.markdown(f'<div class="admin-stat-card"><small>إجمالي السيولة</small><br><span style="font-size:1.8rem; color:#00FF88;">$6.1B</span></div>', unsafe_allow_html=True)
with col_m2:
    st.markdown(f'<div class="admin-stat-card"><small>جيش القادة</small><br><span style="font-size:1.8rem; color:{t["accent"]};">1.2M</span></div>', unsafe_allow_html=True)
with col_m3:
    st.markdown(f'<div class="admin-stat-card"><small>طلبات معلقة</small><br><span style="font-size:1.8rem;">42</span></div>', unsafe_allow_html=True)
with col_m4:
    st.markdown(f'<div class="admin-stat-card"><small>معدل النمو</small><br><span style="font-size:1.8rem; color:#FF4B4B;">+22%</span></div>', unsafe_allow_html=True)

st.divider()

# التبويبات الإدارية (The 5 Pillars of Admin)
tabs = st.tabs(["🏗️ المشاريع الجغرافية", "🎬 جودة المحتوى", "💹 نظام العمولات", "👥 الهويات السيادية", "🧠 الذكاء الاستراتيجي"])

# --- Tab 1: تدقيق المشاريع ---
with tabs[0]:
    st.subheader("📍 مراجعة طلبات الضخ المالي الإقليمي")
    pending_projects = [
        {"title": "توسعة مزارع السودان", "country": "السودان", "goal": "$500,000", "user": "القائد إدريس"},
        {"title": "مركز لوجستي في بنغازي", "country": "ليبيا", "goal": "$250,000", "user": "القائد صالح"},
        {"title": "مصنع تجميع EV", "country": "مصر", "goal": "$1,200,000", "user": "القائد أحمد"}
    ]
    
    for proj in pending_projects:
        with st.container():
            st.markdown(f"""
            <div class="approval-box">
                <div style="display: flex; justify-content: space-between;">
                    <h4>{proj['title']} - {proj['country']}</h4>
                    <span style="color:#00FF88;">المستهدف: {proj['goal']}</span>
                </div>
                <p style="font-size:0.8rem; opacity:0.7;">بواسطة: {proj['user']}</p>
            </div>
            """, unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1, 1, 2])
            c1.button("✅ موافقة", key=f"app_{proj['title']}")
            c2.button("❌ رفض", key=f"rej_{proj['title']}")
            c3.text_input("ملاحظات التدقيق:", key=f"note_{proj['title']}")

# --- Tab 2: مراقبة المحتوى ---
with tabs[1]:
    st.subheader("🎬 اعتماد الملكية الفكرية")
    st.table([
        {"الدورة": "أسرار التداول العشري", "المبدع": "ياسين القائد", "الحالة": "قيد المراجعة ⏳"},
        {"الدورة": "قيادة الفرق العابرة للحدود", "المبدع": "سارة القائد", "الحالة": "قيد المراجعة ⏳"}
    ])
    st.button("دخول غرفة الفحص المرئي 📺")

# --- Tab 3: نظام العمولات ---
with tabs[2]:
    st.subheader("💹 المعايير المالية للأجيال")
    st.markdown(f"""
    <div style="background:rgba(255,215,0,0.05); padding:20px; border-radius:20px; border: 1px solid {t['accent']};">
        <p>يتم الآن تطبيق <b>السياسة المالية الموحدة</b>:</p>
        <ul>
            <li>الجيل الأول: <b>10%</b></li>
            <li>الجيل الثاني: <b>5%</b></li>
            <li>الأجيال من 3 إلى 7: <b>1%</b></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.slider("تعديل نسبة الجيل الأول (طوارئ):", 1, 20, 10)
    st.button("💾 تثبيت القوانين المالية")

# --- Tab 4: إدارة الهويات ---
with tabs[3]:
    st.subheader("👥 السجل الإمبراطوري للقادة")
    st.text_input("🔍 ابحث عن قائد بالـ UUID أو الاسم:")
    st.table([
        {"UUID": "7c9e-...", "الاسم": "أحمد المصري", "الرتبة": "جنرال ماسي", "الحالة": "موثق ✅"},
        {"UUID": "2b1a-...", "الاسم": "صالح الليبي", "الرتبة": "قائد استراتيجي", "الحالة": "موثق ✅"}
    ])

# --- Tab 5: الذكاء الاستراتيجي (New Opinion Upgrade) ---
with tabs[4]:
    st.subheader("🧠 وكيل التحليل الاستراتيجي (MR7-AI)")
    st.markdown("""
    <div class="ai-insight-card">
        <h4 style="color: #00FF88;">🚀 توصية النمو اللحظي:</h4>
        <p>بناءً على نشاط الأجيال الأخير، إقليم <b>"ليبيا"</b> يظهر زيادة في معدل التضاعف بنسبة 15%. 
        نقترح توجيه 5% من ميزانية التسويق العالمية لدعم القادة في بنغازي هذا الأسبوع.</p>
    </div>
    <div class="ai-insight-card" style="border-color: #FFD700;">
        <h4 style="color: #FFD700;">💹 تحليل مخاطر السيولة:</h4>
        <p>المشاريع الجارية في <b>"مصر"</b> تقترب من مرحلة التشغيل الكامل. معدل العائد المتوقع (ROI) قد يرتفع إلى 28% في الربع القادم.</p>
    </div>
    """, unsafe_allow_html=True)
    st.button("توليد تقرير الذكاء الاصطناعي الشامل 📊")

st.divider()

if st.button("🏠 العودة لمركز العمليات الرئيسي"):
    st.switch_page("app.py")
