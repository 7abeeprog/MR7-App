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

    /* تصميم خريطة الشجرة */
    .tree-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 20px;
        padding: 20px;
    }}
    .tree-node {{
        background: {t['card']};
        border: 2px solid {t['accent']};
        padding: 10px 20px;
        border-radius: 50px;
        text-align: center;
        min-width: 150px;
        position: relative;
    }}
    .tree-line {{
        width: 2px;
        height: 20px;
        background: {t['accent']};
    }}
    .tree-branch {{
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 15px !important;
        height: 55px;
    }}

    .stTextInput input, .stNumberInput input {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: bold !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. محاكاة بيانات العمولات (MLM Stats) ---
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
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.3rem; margin-top:-20px;'>إدارة أرباح الأجيال وروابط الانتشار العالمي</p>", unsafe_allow_html=True)

st.divider()

tabs = st.tabs(["📊 أرباح المستويات", "🔗 روابط الإحالة", "📈 حاسبة التضاعف العشري", "🌳 الخريطة الشجرية"])

# --- Tab 1: أرباح المستويات (7 Levels) ---
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
                        <span class="level-badge">المستوى {level['lvl']}</span>
                        <h3 style="margin: 5px 0;">نسبة الربح: {level['rate']}%</h3>
                        <p style="color: #888;">عدد الأعضاء في هذا الجيل: {level['members']:,}</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="color: #888;">حجم مبيعات الجيل</p>
                        <h2 style="color: #00FF88; margin: 0;">${level['sales']:,}</h2>
                        <p style="color: {t['accent']}; font-weight: bold;">ربحك: ${profit:,}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background: {t['accent']}; color: black; padding: 25px; border-radius: 20px; text-align: center; margin-top: 20px;">
        <h2 style="color: black !important; margin: 0;">إجمالي عمولات الأجيال: ${total_earned:,.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

# --- Tab 2: روابط الإحالة الذكية ---
with tabs[1]:
    st.subheader("🔗 مركز توليد روابط الانتشار")
    st.info("استخرج روابط مخصصة لمنتجات معينة أو للمتجر العام لضمان تتبع العمولات في المستويات السبعة.")
    
    col_l, col_r = st.columns([2, 1])
    with col_l:
        target = st.selectbox("الوجهة المستهدفة للرابط:", ["المتجر العالمي", "دورة عقلية المليار", "باقة أدوات التوسع"])
        ref_code = st.text_input("كود الإحالة المخصص (اختياري):", placeholder="مثلاً: LEADER77")
        
        if st.button("🚀 توليد رابط التتبع"):
            final_link = f"https://mr7-app.com/shop?ref={ref_code if ref_code else 'USER_ID'}&target={target.replace(' ', '_')}"
            st.code(final_link, language="text")
            st.toast("تم توليد الرابط بنجاح!")
            
    with col_r:
        st.markdown(f"""
        <div class="comm-card" style="text-align: center;">
            <p>أداء الروابط</p>
            <h2 style="color: {t['accent']};">1,240</h2>
            <p>نقرة فريدة</p>
            <hr>
            <h2 style="color: #00FF88;">85</h2>
            <p>عملية شراء ناجحة</p>
        </div>
        """, unsafe_allow_html=True)

# --- Tab 3: حاسبة التضاعف العشري ---
with tabs[2]:
    st.subheader("📈 محاكي أرباح التضاعف (قانون الـ 10)")
    st.markdown("احسب أرباحك إذا قام كل شخص في فريقك بدعوة 10 أشخاص فقط.")
    
    avg_ticket = st.number_input("متوسط سعر المنتج المباع ($):", min_value=1, value=100)
    
    st.markdown("#### التوقع المالي للسبعة أجيال:")
    
    # حساب التضاعف العشري
    multiplier = 10
    results = []
    current_members = 10
    
    for level in commission_levels:
        level_profit = (current_members * avg_ticket * level['rate']) / 100
        results.append({"المستوى": f"الجيل {level['lvl']}", "الأعضاء": f"{current_members:,}", "الربح المتوقع": f"${level_profit:,.2f}"})
        current_members *= multiplier
        
    st.table(results)
    st.warning("⚠️ هذه الأرقام هي محاكاة رياضية لنسبة نجاح 100% في التضاعف العشري.")

# --- Tab 4: الخريطة الشجرية المرئية (Visual Tree Map) ---
with tabs[3]:
    st.subheader("🌳 خريطة الانتشار الهيكلية")
    st.markdown("رؤية بصرية لأهم القادة في شجرتك القيادية وتوزيع الأجيال.")
    
    # محاكاة الشجرة باستخدام HTML و CSS المخصص
    st.markdown(f"""
    <div class="tree-container">
        <!-- عقدة الجذر (أنت) -->
        <div class="tree-node" style="background: {t['accent']}; color: black; font-weight: 900;">
            👑 القائد (أنت)
        </div>
        <div class="tree-line"></div>
        
        <!-- الجيل الأول -->
        <div class="tree-branch">
            <div class="tree-node">👤 جيل 1: أحمد</div>
            <div class="tree-node">👤 جيل 1: سارة</div>
            <div class="tree-node">👤 جيل 1: ياسين</div>
            <div class="tree-node">👤 جيل 1: ليلى</div>
        </div>
        
        <div style="display: flex; gap: 100px;">
            <div class="tree-line"></div>
            <div class="tree-line"></div>
        </div>

        <!-- الجيل الثاني (مثال لفرع واحد) -->
        <div class="tree-branch">
            <div class="tree-node" style="border-color: #00FF88; font-size: 0.8rem;">👥 جيل 2: فريق أحمد (15)</div>
            <div class="tree-node" style="border-color: #00FF88; font-size: 0.8rem;">👥 جيل 2: فريق سارة (8)</div>
        </div>
        
        <div class="tree-line"></div>
        
        <!-- ملخص الأجيال البعيدة -->
        <div class="tree-node" style="border-style: dashed; opacity: 0.7;">
            🌐 بقية الأجيال (3-7)
            <br><small>+4,500 عضو نشط</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 نصيحة القيادة: ركز دعمك على الجيل الأول لضمان تماسك هيكل الشجرة وتضاعف الأرباح في الأجيال العميقة.")

st.divider()

# العودة
if st.button("🏠 العودة للوحة التحكم"):
    st.switch_page("app.py")
