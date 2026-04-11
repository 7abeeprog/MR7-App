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

    .comm-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        transition: 0.3s ease;
    }}
    .comm-card:hover {{ transform: translateY(-5px); border-color: #00FF88; }}

    .level-badge {{
        background: {t['accent']};
        color: black !important;
        padding: 2px 10px;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: 900;
    }}

    /* --- تصميم خريطة الشجرة القيادية المتطور --- */
    .tree-wrapper {{
        width: 100%;
        overflow-x: auto;
        padding: 40px 0;
        text-align: center;
        background: rgba(255,255,255,0.01);
        border-radius: 30px;
    }}
    
    .tree {{
        display: inline-block;
        white-space: nowrap;
    }}
    
    .tree ul {{
        padding-top: 20px; 
        position: relative;
        transition: all 0.5s;
        display: flex;
        justify-content: center;
        padding-left: 0;
    }}
    
    .tree li {{
        float: left; text-align: center;
        list-style-type: none;
        position: relative;
        padding: 20px 10px 0 10px;
        transition: all 0.5s;
    }}
    
    /* رسم الخطوط العمودية */
    .tree li::before, .tree li::after {{
        content: '';
        position: absolute; top: 0; right: 50%;
        border-top: 2px solid {t['accent']};
        width: 50%; height: 20px;
    }}
    .tree li::after {{
        right: auto; left: 50%;
        border-left: 2px solid {t['accent']};
    }}
    
    /* إزالة الخطوط من الأطراف */
    .tree li:only-child::after, .tree li:only-child::before {{ display: none; }}
    .tree li:only-child {{ padding-top: 0; }}
    .tree li:first-child::before, .tree li:last-child::after {{ border: 0 none; }}
    .tree li:last-child::before {{ border-right: 2px solid {t['accent']}; border-radius: 0 5px 0 0; }}
    .tree li:first-child::after {{ border-radius: 5px 0 0 0; }}
    
    /* الخط النازل من الأب */
    .tree ul ul::before {{
        content: '';
        position: absolute; top: 0; left: 50%;
        border-left: 2px solid {t['accent']};
        width: 0; height: 20px;
    }}
    
    .tree-node-item {{
        border: 2px solid {t['accent']};
        padding: 10px 15px;
        text-decoration: none;
        color: {t['text']};
        display: inline-block;
        border-radius: 15px;
        background: {t['card']};
        transition: 0.4s;
        min-width: 120px;
    }}
    
    .tree-node-item:hover {{
        background: {t['accent']};
        color: black !important;
        transform: scale(1.1) translateY(-5px);
        box-shadow: 0 0 20px {t['accent']};
    }}

    .tree-node-item i {{ display: block; font-size: 1.5rem; margin-bottom: 5px; }}
    
    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 15px !important;
        height: 55px;
    }}

    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 12px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. محاكاة بيانات العمولات (7 Levels Standard) ---
commission_levels = [
    {"lvl": 1, "rate": 10, "members": 12, "sales": 5000},
    {"lvl": 2, "rate": 5, "members": 45, "sales": 12000},
    {"lvl": 3, "rate": 1, "members": 120, "sales": 25000},
    {"lvl": 4, "rate": 1, "members": 300, "sales": 40000},
    {"lvl": 5, "rate": 1, "members": 850, "sales": 95000},
    {"lvl": 6, "rate": 1, "members": 1400, "sales": 150000},
    {"lvl": 7, "rate": 1, "members": 3200, "sales": 420000},
]

# --- 3. واجهة نظام العمولات ---
st.title("🔗 نظام العمولات الذكي")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.3rem; margin-top:-20px;'>إدارة أرباح الأجيال وروابط الانتشار العالمي لمجتمع MR7</p>", unsafe_allow_html=True)

st.divider()

# التبويبات الرئيسية
tabs = st.tabs(["📊 أرباح المستويات", "🌳 الخريطة الشجرية", "🔗 روابط الإحالة", "📈 حاسبة التضاعف"])

# --- Tab 1: أرباح المستويات ---
with tabs[0]:
    st.subheader("🌲 هيكلية أرباح السبعة مستويات")
    
    total_earned = 0
    for level in commission_levels:
        profit = (level['sales'] * level['rate']) / 100
        total_earned += profit
        
        with st.container():
            st.markdown(f"""
            <div class="comm-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span class="level-badge">الجيل {level['lvl']}</span>
                        <h3 style="margin: 5px 0;">العمولة: {level['rate']}%</h3>
                        <p style="color: #888;">الأعضاء: {level['members']:,}</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="color: #888;">مبيعات الجيل</p>
                        <h2 style="color: #00FF88; margin: 0;">${level['sales']:,}</h2>
                        <p style="color: {t['accent']}; font-weight: bold;">أرباحك: ${profit:,}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background: {t['accent']}; color: black; padding: 25px; border-radius: 20px; text-align: center; margin-top: 20px;">
        <h2 style="color: black !important; margin: 0;">إجمالي عمولات الشبكة الموثقة: ${total_earned:,.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

# --- Tab 2: الخريطة الشجرية المرئية المتطورة (Advanced Org Chart) ---
with tabs[1]:
    st.subheader("🌳 خريطة الانتشار الهيكلية")
    st.markdown("رؤية بصرية حقيقية لتوسع جيشك الاقتصادي عبر الأجيال.")
    
    st.markdown(f"""
    <div class="tree-wrapper">
        <div class="tree">
            <ul>
                <li>
                    <div class="tree-node-item" style="border-color: {t['accent']}; font-weight: 900;">
                        👑 أنت (القائد)
                    </div>
                    <ul>
                        <li>
                            <div class="tree-node-item">👤 أحمد (ج1)</div>
                            <ul>
                                <li><div class="tree-node-item" style="border-color: #00FF88; font-size: 0.7rem;">👥 فريق أحمد (15)</div></li>
                            </ul>
                        </li>
                        <li>
                            <div class="tree-node-item">👤 سارة (ج1)</div>
                            <ul>
                                <li><div class="tree-node-item" style="border-color: #00FF88; font-size: 0.7rem;">👥 فريق سارة (8)</div></li>
                            </ul>
                        </li>
                        <li>
                            <div class="tree-node-item">👤 ياسين (ج1)</div>
                        </li>
                        <li>
                            <div class="tree-node-item">👤 ليلى (ج1)</div>
                        </li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
    <br>
    <div style="text-align: center; opacity: 0.7;">
        <p style="font-size: 0.9rem;">🌳 تستمر الشجرة في التفرع حتى الجيل السابع (+4,500 عضو إضافي)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 نصيحة القيادة: الخطوط الذهبية تمثل روابط الثقة. كلما زاد دعمك المباشر للجيل الأول، زادت متانة قاعدتك الهرمية.")

# --- Tab 3: روابط الإحالة الذكية ---
with tabs[2]:
    st.subheader("🔗 مركز توليد روابط الانتشار")
    st.info("استخرج روابط مخصصة لمنتجات معينة أو للمتجر العام لضمان تتبع العمولات بدقة.")
    
    col_l, col_r = st.columns([2, 1])
    with col_l:
        target = st.selectbox("الوجهة المستهدفة للرابط:", ["المتجر العالمي", "دورة عقلية المليار", "باقة أدوات التوسع", "منصة التمويل الجماعي"])
        ref_code = st.text_input("كود الإحالة الخاص بك:", value="LEADER_MR7_001")
        
        if st.button("🚀 توليد رابط التتبع الملحمي"):
            final_link = f"https://mr7-app.com/marketplace?ref={ref_code}&target={target.replace(' ', '_')}"
            st.code(final_link, language="text")
            st.success("الرابط نشط وجاهز للانتشار!")
            
    with col_r:
        st.markdown(f"""
        <div class="comm-card" style="text-align: center; border-color: #00FF88;">
            <p>أداء الروابط</p>
            <h2 style="color: #00FF88;">2,450</h2>
            <p>زيارة فريدة</p>
            <hr style="border-color: #333;">
            <h2 style="color: {t['accent']};">182</h2>
            <p>قائد جديد انضم</p>
        </div>
        """, unsafe_allow_html=True)

# --- Tab 4: حاسبة التضاعف ---
with tabs[3]:
    st.subheader("📈 محاكي أرباح التضاعف العشري")
    st.markdown("احسب القوة الانفجارية لأرباحك في حال التزام كل قائد بدعوة 10 أشخاص فقط.")
    
    avg_ticket = st.number_input("متوسط قيمة مبيعات الفرد ($):", min_value=1, value=100)
    
    # حساب التضاعف
    results = []
    current_members = 10
    total_sim_profit = 0
    
    for level in commission_levels:
        level_profit = (current_members * avg_ticket * level['rate']) / 100
        total_sim_profit += level_profit
        results.append({
            "الجيل": f"المستوى {level['lvl']}",
            "عدد الأعضاء": f"{current_members:,}",
            "النسبة": f"{level['rate']}%",
            "الربح المتوقع": f"${level_profit:,.2f}"
        })
        current_members *= 10
        
    st.table(results)
    st.markdown(f"""
    <div style="background: rgba(0, 255, 136, 0.1); border: 2px solid #00FF88; padding: 15px; border-radius: 15px; text-align: center;">
        <h3 style="color: #00FF88; margin: 0;">إجمالي الربح المتوقع في الدورة الكاملة: ${total_sim_profit:,.2f}</h3>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# العودة للقائمة الجانبية أو الرئيسية
if st.button("🏠 العودة لمركز القيادة"):
    st.switch_page("app.py")
