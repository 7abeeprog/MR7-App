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

    /* تصميم شجرة التضاعف العشري */
    .decade-tree {{
        background: rgba(255, 215, 0, 0.05);
        border: 2px dashed {t['accent']};
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
    }}
    .node-active {{ color: #00FF88 !important; font-size: 1.2rem; }}
    .node-empty {{ color: #555 !important; font-size: 1.2rem; }}

    /* فقاعات الدردشة */
    .chat-bubble {{
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        max-width: 80%;
    }}
    .chat-received {{ background: #222; border-right: 4px solid {t['accent']}; text-align: right; }}
    .chat-sent {{ background: {t['accent']}; color: #000 !important; margin-left: auto; text-align: left; }}

    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 15px !important;
        height: 55px;
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
    st.markdown("### 🏆 حالتك القيادية")
    st.success("الرتبة: قائد ماسي 💎")
    st.info("قوة الفريق: 85% كفاءة")
    st.progress(8.5/10)
    st.caption("متبقي 2 من القادة للوصول لمستوى 'الإمبراطور'")

# --- 3. واجهة إدارة الفرق ---
st.title("👥 إدارة فرق النخبة MR7")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.3rem; margin-top:-20px;'>نظام التضاعف العشري والسيادة الجماعية</p>", unsafe_allow_html=True)

st.divider()

# ملخص الإحصائيات الحية
col1, col2, col3, col4 = st.columns(4)
stats = [
    ("إجمالي الفريق", "1,248", "👥"),
    ("مبيعات الفريق", "$842K", "📈"),
    ("عمولاتك", "$126K", "💰"),
    ("هدف الـ 10", "8/10", "🎯")
]
for i, (label, val, icon) in enumerate(stats):
    with [col1, col2, col3, col4][i]:
        st.markdown(f"""
        <div class="team-card" style="padding: 15px;">
            <p style="font-size: 0.9rem;">{icon} {label}</p>
            <div style="font-size: 1.8rem; font-weight: 900; color: {t['accent']};">{val}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# التبويبات المتطورة
tabs = st.tabs(["🌳 شجرة التضاعف العشري", "💬 مركز التواصل", "🏆 الإنجازات", "❓ الدعم والأسئلة"])

# --- Tab 1: شجرة التضاعف العشري ---
with tabs[0]:
    st.subheader("🌲 استراتيجية الـ 10: المعيار الذهبي للسيادة")
    st.markdown("""
    تعتمد فلسفة MR7 على **قانون الـ 10**. عندما تكتمل صفوفك العشرة الأولى، تبدأ الماكينة المالية في التضاعف تلقائياً.
    - **المستوى 1 (مباشر):** 10 قادة (عمولة 20%)
    - **المستوى 2:** 100 عضو (عمولة 10%)
    - **المستوى 3:** 1,000 مسوق (عمولة 5%)
    """)
    
    st.markdown("### 📊 مسار تضاعفك الحالي")
    
    # محاكاة بصرية للشجرة
    cols = st.columns(10)
    for i in range(10):
        with cols[i]:
            if i < 8:
                st.markdown(f"<div style='text-align:center;' class='node-active'>👤<br><span style='font-size:10px;'>قائد {i+1}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align:center;' class='node-empty'>⚪<br><span style='font-size:10px;'>شاغر</span></div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="decade-tree">
        <h4 style="color: {t['accent']}; text-align: center;">لقد حققت 80% من هدف "العشرة الذهبية"</h4>
        <p style="text-align: center; font-size: 0.9rem;">بإضافة قائدين إضافيين، ستحصل على بونص "السيادة العشرية" بقيمة $5,000</p>
    </div>
    """, unsafe_allow_html=True)

# --- Tab 2: مركز التواصل (Chat & Media) ---
with tabs[1]:
    st.subheader("💬 غرفة عمليات التواصل")
    
    col_chat_list, col_chat_view = st.columns([1, 2])
    
    with col_chat_list:
        st.markdown("#### القنوات")
        st.button("📢 الفريق العام (1.2K)")
        st.button("💎 مجلس القادة (15)")
        st.divider()
        st.markdown("#### خاص")
        st.button("👤 عمر الفاروق (نشط)")
        st.button("👤 ليلى (غير نشط)")

    with col_chat_view:
        st.markdown(f"""
        <div style="height: 300px; overflow-y: auto; padding: 10px; background: rgba(255,255,255,0.02); border-radius: 15px;">
            <div class="chat-bubble chat-received">عمر الفاروق: قائد، لقد أكملت أول 5 أعضاء في فريقي اليوم! 🚀</div>
            <div class="chat-bubble chat-sent">أنت: ممتاز يا بطل! استمر حتى تصل للـ 10 لفتح عمولات الجيل الثاني.</div>
            <div class="chat-bubble chat-received">ليلى: هل هناك اجتماع صوتي اليوم لمناقشة استراتيجية المليار؟</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        c_v1, c_v2, c_v3 = st.columns([3, 1, 1])
        with c_v1:
            st.text_input("اكتب رسالتك...", label_visibility="collapsed")
        with c_v2:
            st.button("🎙️") # صوت
        with c_v3:
            st.button("🎥") # فيديو

# --- Tab 3: الإنجازات (Gamification) ---
with tabs[2]:
    st.subheader("🏆 لوحة أوسمة الاستحقاق")
    col_a, col_b, col_c = st.columns(3)
    
    badges = [
        ("🥇 باني الفريق", "إكمال أول 10 قادة مباشرين", "قيد الإنجاز"),
        ("💎 المحرك المالي", "تحقيق مبيعات فريق بقيمة $500K", "تم الإنجاز ✅"),
        ("🌍 عابر القارات", "توسع الفريق في أكثر من 5 دول", "تم الإنجاز ✅")
    ]
    
    for i, (name, desc, status) in enumerate(badges):
        with [col_a, col_b, col_c][i]:
            st.markdown(f"""
            <div class="team-card">
                <div style="font-size: 40px;">{'🎖️' if 'تم' in status else '🔒'}</div>
                <h4 style="margin: 10px 0;">{name}</h4>
                <p style="font-size: 0.8rem; color: #aaa;">{desc}</p>
                <p style="color: #00FF88;">{status}</p>
            </div>
            """, unsafe_allow_html=True)

# --- Tab 4: الدعم والأسئلة ---
with tabs[3]:
    st.subheader("❓ مساعدة فريق القيادة")
    with st.expander("كيف يتم احتساب عمولات الجيل الثالث؟"):
        st.write("يتم احتسابها بنسبة 5% من إجمالي مبيعات الأعضاء الذين انضموا عن طريق أعضاء جيلك الثاني، بشرط أن تكون قد أكملت 'العشرة الذهبية' الخاصة بك.")
    
    with st.expander("هل يمكنني نقل قائد من فريق لآخر؟"):
        st.write("نظام MR7 يدعم الهيكلة الثابتة لضمان حقوق الجميع، ولكن يمكنك طلب استشارة من الأدمن للحالات الاستثنائية.")
    
    st.divider()
    st.button("📝 فتح تذكرة دعم خاصة للفريق")

st.divider()

# العودة
c_back, c_next = st.columns(2)
with c_back:
    if st.button("📊 مراجعة العمولات"):
        st.switch_page("pages/5_Commissions.py")
with c_next:
    if st.button("🎨 استوديو بناء المحتوى"):
        st.switch_page("pages/7_Creator_Studio.py")
