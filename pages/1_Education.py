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

    /* تصميم بطاقة المرحلة (The Rank Card) */
    .rank-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        transition: 0.3s ease;
        text-align: center;
    }}
    .rank-card:hover {{ transform: scale(1.05); border-color: #00FF88; box-shadow: 0 0 20px rgba(0,255,136,0.3); }}

    /* شريط التقدم الزمني لرحلة الـ 100 يوم */
    .journey-bar {{
        background: #222;
        border-radius: 50px;
        height: 30px;
        width: 100%;
        margin: 20px 0;
        position: relative;
        overflow: hidden;
        border: 1px solid {t['accent']};
    }}
    .journey-fill {{
        background: linear-gradient(90deg, {t['accent']}, #00FF88);
        height: 100%;
        width: 15%; /* مثال للتقدم */
    }}

    /* حقول الإدخال */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: bold !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 20px !important;
        height: 50px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة الرتب (The 8 Ranks of MR7) ---
if 'user_rank' not in st.session_state:
    st.session_state.user_rank = "Dreamer"

ranks = {
    "Dreamer": {"icon": "🥚", "goal": "دفع $10 وبدء المسار", "reward": "$0", "next": "Adventurer"},
    "Adventurer": {"icon": "🧭", "goal": "بناء فريق من 10 أعضاء", "reward": "$10", "next": "Knight"},
    "Knight": {"icon": "🛡️", "goal": "الوصول لـ 100 عضو في الفريق", "reward": "$50", "next": "Warlord"},
    "Warlord": {"icon": "👑", "goal": "الوصول لـ 1,000 عضو في الفريق", "reward": "$100", "next": "Alchemist"},
    "Alchemist": {"icon": "🔮", "goal": "الوصول لـ 10,000 عضو", "reward": "$1,000", "next": "Visionary"},
    "Visionary": {"icon": "🔭", "goal": "الوصول لـ 100,000 عضو", "reward": "$10,000", "next": "Game Changer"},
    "Game Changer": {"icon": "⚡", "goal": "الوصول لـ 1,000,000 عضو", "reward": "$100,000", "next": "Legend"},
    "Legend": {"icon": "🌌", "goal": "الوصول لـ 10,000,000 عضو", "reward": "$1,000,000", "next": "Maxed"}
}

# --- 3. واجهة الأكاديمية (MR7 Education Engine) ---
st.title("🧠 مصنع قادة التريليون")
st.markdown(f"<p style='text-align:center; font-size:1.4rem; margin-top:-20px;'>رحلة الـ 100 يوم من $0 إلى $1,000,000</p>", unsafe_allow_html=True)

# شريط الرحلة (The 100-Day Bootcamp Progress)
st.markdown("### ⏳ مسار الـ 100 يوم للسيادة")
st.markdown("""
<div class="journey-bar">
    <div class="journey-fill"></div>
</div>
""", unsafe_allow_html=True)
col_j1, col_j2 = st.columns([1, 1])
col_j1.caption("بداية الرحلة: يوم 1")
col_j2.markdown("<p style='text-align:left;'>المستهدف: يوم 100 (أسطورة)</p>", unsafe_allow_html=True)

st.divider()

# عرض الرتبة الحالية والمسار
with st.sidebar:
    st.markdown("### 👤 ملف القائد")
    current = ranks[st.session_state.user_rank]
    st.markdown(f"""
    <div class="rank-card">
        <div style="font-size: 3rem;">{current['icon']}</div>
        <h2 style="margin: 0; color: {t['accent']} !important;">{st.session_state.user_rank}</h2>
        <p style="font-size: 0.9rem;">الهدف القادم: {current['next']}</p>
    </div>
    """, unsafe_allow_html=True)
    st.write(f"**المهمة:** {current['goal']}")
    st.write(f"**المكافأة المالية:** {current['reward']}")
    
    st.divider()
    st.markdown("### 🎨 تخصيص المظهر")
    theme_choice = st.selectbox("النمط:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()

# التبويبات التعليمية (Systems Analysis)
tabs = st.tabs(["🚀 بوت كامب الـ 100 يوم", "🧬 الأنظمة الثمانية", "🧪 استوديو المبدعين", "📜 أرشيف الاعتمادات"])

# --- Tab 1: رحلة التحول السريع ---
with tabs[0]:
    st.subheader("🔥 مسار التحول الرقمي الفائق")
    st.info("نحن لا نبني مجرد مجتمع، نحن ندير مصنعاً للقيادة يضاعف قدراتك كل 10 أيام.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="rank-card" style="border-color: #00FF88;">
            <h3>🧠 عقلية المليار</h3>
            <p>المستوى 1: التأسيس الذاتي</p>
            <button style="width:100%; height:40px; background:#00FF88; border:none; border-radius:10px; font-weight:bold;">دخول الدرس 📖</button>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="rank-card">
            <h3>📈 هندسة التضاعف</h3>
            <p>قانون الـ 10: كيف تضاعف فريقك؟</p>
            <button style="width:100%; height:40px; background:{t['accent']}; border:none; border-radius:10px; font-weight:bold; color:black;">دخول الدرس 📖</button>
        </div>
        """, unsafe_allow_html=True)

# --- Tab 2: الأنظمة الثمانية المتكاملة ---
with tabs[1]:
    st.subheader("🧬 الأنظمة الذكية لإدارة الإمبراطورية")
    st.write("تعلم كيفية التحكم في الأنظمة الثمانية التي تدير اقتصاد MR7:")
    
    systems = [
        ("🧠 العقل المركزي (AI Brain)", "تحليل البيانات والابتكار المستمر"),
        ("📂 محرك التعليم (Education)", "المحتوى التفاعلي والأكاديمية الرقمية"),
        ("👥 إدارة الفرق (Team Core)", "مراقبة الأداء والكفاءة"),
        ("🏆 التحفيز (Incentives Hub)", "المسابقات والجوائز القيادية"),
        ("🌐 شبكة الانتشار (Network)", "بناء المجتمع والنمو الجماعي"),
        ("💰 النظام المالي (Finance)", "المحافظ الرقمية والعمليات الذكية"),
        ("🛒 المتجر العالمي (E-Commerce)", "منصة البيع والشراء السلسة"),
        ("🤝 التمويل الجماعي (Crowdfunding)", "دعم المشاريع الناشئة والاقتصاد التشاركي")
    ]
    
    for name, desc in systems:
        with st.expander(f"⚙️ {name}"):
            st.write(desc)
            st.button(f"بدء تدريب {name}", key=f"sys_{name}")

# --- Tab 3: استوديو المبدعين ---
with tabs[2]:
    st.subheader("🧪 كن جزءاً من المحرك المعرفي")
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {t['accent']}, #00FF88); color: black; padding: 25px; border-radius: 20px; text-align: center;">
        <h2 style="color: black !important;">أنت لست مجرد متدرب، أنت مهندس!</h2>
        <p style="font-weight: 700;">ارفع محتواك التعليمي، حدد سعرك، وابدأ في تحقيق دخل سلبي من معرفتك.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎨 الانتقال لاستوديو بناء المحتوى"):
        st.switch_page("pages/7_Creator_Studio.py")

# --- Tab 4: الشهادات والتقدم الحقيقي ---
with tabs[3]:
    st.subheader("📜 سجل السيادة المعرفية")
    st.markdown("""
    <div style="text-align: center; padding: 40px; border: 2px dashed #444; border-radius: 20px;">
        <p style="font-size: 1.5rem; opacity: 0.5;">لا توجد شهادات صادرة بعد</p>
        <p>أكمل مسار 'Adventurer' بنجاح لتوليد أول شهادة موثقة.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# وحدة التضاعف العشري (The Formula)
st.markdown("### 🧮 معادلة التضاعف العشري")
with st.expander("كيف نصل لـ 100 مليون دولار في 100 يوم؟"):
    st.write("تبدأ الرحلة بـ 1,000 حالم (Dreamers) يتضاعفون تدريجياً عبر قانون الـ 10 ليصلوا لـ 10 مليون مشترك، محققين ناتجاً اقتصادياً يتجاوز المليار دولار.")
    st.image("http://googleusercontent.com/image_collection/image_retrieval/6449232857341181720") # صورة تعبيرية للنمو المالي

if st.button("🤝 استكشاف فرص التمويل الجماعي للمشاريع"):
    st.switch_page("pages/9_Crowdfunding.py")
