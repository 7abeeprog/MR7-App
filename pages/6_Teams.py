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
    
    div[data-testid="stMarkdownContainer"] p, h2, h3, span, label, li {{ 
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
        font-size: 3rem !important; 
    }}

    .team-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 25px;
        padding: 25px;
        margin-bottom: 20px;
        text-align: center;
        transition: 0.3s ease;
    }}
    .team-card:hover {{ border-color: #00FF88; transform: translateY(-5px); }}

    .stat-value {{
        font-size: 2.5rem !important;
        font-weight: 950 !important;
        color: {t['accent']} !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 15px !important;
        height: 60px;
    }}

    /* إصلاح القوائم المنسدلة */
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
    st.markdown("### 🏆 رتبة القيادة")
    st.success("الرتبة: قائد ماسي 💎")
    st.info("قوة الفريق: 85% كفاءة")

# --- 3. واجهة إدارة الفرق ---
st.title("👥 إدارة فرق النخبة MR7")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.3rem; margin-top:-20px;'>قيادة الجيوش الاقتصادية نحو سيادة التريليون</p>", unsafe_allow_html=True)

st.divider()

# ملخص الإحصائيات (Dashboard Stats)
col_stat1, col_stat2, col_stat3 = st.columns(3)

with col_stat1:
    st.markdown(f"""
    <div class="team-card">
        <p>إجمالي الأعضاء</p>
        <div class="stat-value">1,248</div>
        <p style="color:#00FF88;">+12% هذا الأسبوع</p>
    </div>
    """, unsafe_allow_html=True)

with col_stat2:
    st.markdown(f"""
    <div class="team-card">
        <p>مبيعات الفريق</p>
        <div class="stat-value">$842K</div>
        <p style="color:#00FF88;">معدل نمو مرتفع 📈</p>
    </div>
    """, unsafe_allow_html=True)

with col_stat3:
    st.markdown(f"""
    <div class="team-card">
        <p>عمولات القيادة</p>
        <div class="stat-value">$126K</div>
        <p style="color:#FFD700;">جاهزة للسحب 💰</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

tab1, tab2, tab3 = st.tabs(["📊 هيكلية الفريق", "🤝 قائمة القادة", "🛠️ أدوات القيادة"])

# --- Tab 1: هيكلية الفريق (Hierarchy) ---
with tab1:
    st.subheader("🌲 هيكل الانتشار الهرمي")
    st.info("هذا الرسم يوضح توزع القوة داخل فريقك بين الأجيال المختلفة.")
    
    # محاكاة لهيكل شجري
    st.markdown(f"""
    - **أنت (القائد المؤسس)**
        - 👤 الجيل الأول (15 قائد مباشر)
            - 👥 الجيل الثاني (142 عضو)
                - 🌐 الجيل الثالث (1091 مسوق)
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background: {t['card']}; padding: 20px; border-radius: 15px; border: 1px solid {t['accent']};">
        <h4 style="color: {t['accent']};">تحليل استراتيجي:</h4>
        <p>فريقك ينمو بشكل أكبر في الجيل الثالث. نوصي بتركيز التدريب لرفع كفاءة الجيل الأول لزيادة العمولات المباشرة.</p>
    </div>
    """, unsafe_allow_html=True)

# --- Tab 2: قائمة القادة ---
with tab2:
    st.subheader("🤝 نخبة القادة في فريقك")
    
    search_member = st.text_input("🔍 ابحث عن قائد محدد بالاسم أو المعرف (ID)...")
    
    leaders_data = [
        {"الاسم": "عمر الفاروق", "الرتبة": "ذهبي", "المبيعات": "$45,000", "الأعضاء": 120},
        {"الاسم": "ليلى القائدة", "الرتبة": "بلاتيني", "المبيعات": "$82,000", "الأعضاء": 310},
        {"الاسم": "ياسين الاستراتيجي", "الرتبة": "فضي", "المبيعات": "$12,000", "الأعضاء": 45},
    ]
    st.table(leaders_data)
    
    if st.button("تحميل تقرير الأداء الكامل (PDF) 📄"):
        st.toast("يتم الآن إنشاء التقرير...")

# --- Tab 3: أدوات القيادة ---
with tab3:
    st.subheader("🛠️ ترسانة أدوات الانتشار")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class="team-card" style="border-color: #00FF88;">
            <h3 style="color: #00FF88;">🔗 رابط الدعوة</h3>
            <p style="font-size: 0.9rem;">استخدم هذا الرابط لضم قادة جدد مباشرة تحت قيادتك.</p>
        </div>
        """, unsafe_allow_html=True)
        st.code("https://mr7-app.com/join?ref=LEADER_ID", language="text")
        st.button("نسخ الرابط وإرساله 📲", key="copy_link")

    with col_b:
        st.markdown(f"""
        <div class="team-card" style="border-color: #FFD700;">
            <h3 style="color: #FFD700;">📢 غرفة الاجتماعات</h3>
            <p style="font-size: 0.9rem;">أرسل رسالة فورية لجميع قادة الجيل الأول.</p>
        </div>
        """, unsafe_allow_html=True)
        msg = st.text_input("نص الرسالة القيادية:")
        if st.button("إرسال التوجيهات فوراً ⚡"):
            st.success("تم إرسال الرسالة لـ 15 قائداً بنجاح.")

st.divider()

# العودة للمتجر أو العمولات
c_back, c_next = st.columns(2)
with c_back:
    if st.button("📊 مراجعة العمولات"):
        st.switch_page("pages/5_Commissions.py")
with c_next:
    if st.button("🎨 استوديو بناء المحتوى"):
        st.info("سيتم تفعيل هذه الصفحة في الخطوة القادمة!")
