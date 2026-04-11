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
    div[data-testid="stMarkdownContainer"] p, h2, h3, span, label, li {{ color: {t['text']} !important; font-weight: 700 !important; }}
    h1 {{ background: linear-gradient(90deg, {t['accent']}, {t['text']}, {t['accent']}); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 950 !important; text-align: center; filter: drop-shadow(0 0 10px {t['accent']}); font-size: 3rem !important; }}
    
    .product-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 25px;
        padding: 30px;
        margin-bottom: 25px;
        text-align: center;
        transition: transform 0.3s;
    }}
    .product-card:hover {{ transform: scale(1.02); box-shadow: 0 0 20px {t['accent']}; }}
    .price-tag {{ color: {t['accent']} !important; font-size: 28px; font-weight: 900; margin: 15px 0; }}
    
    div[data-baseweb="select"] > div {{ background-color: {t['select_bg']} !important; color: {t['select_text']} !important; }}
    div[data-baseweb="popover"] li {{ color: {t['select_text']} !important; background-color: {t['select_bg']} !important; }}

    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 20px !important;
        height: 60px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. التحكم في النمط ---
with st.sidebar:
    st.markdown(f"### 🎨 تخصيص المظهر")
    theme_choice = st.selectbox("اختر النمط:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()

# --- 3. واجهة المتجر ---
st.title("🛒 متجر النخبة MR7")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.3rem; font-weight:bold;'>بوابتك للاستثمار في أدوات التريليون</p>", unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns(2)

products = [
    {"name": "💎 باقة القائد البلاتيني", "price": 999, "desc": "وصول كامل لكافة الأنظمة + جلسات كوتشينج خاصة."},
    {"name": "🧠 ماستر كلاس عقلية المليار", "price": 499, "desc": "منهج إعادة البرمجة المالية للتحول الاقتصادي."},
    {"name": "🌍 باقة التوسع العالمي", "price": 2500, "desc": "أدوات متطورة لغزو الأسواق الدولية وإدارة الفرق."},
    {"name": "🤖 اشتراك الوكيل الذكي السنوي", "price": 150, "desc": "تفعيل كافة ميزات التحليل المالي والتعليم الآلي."}
]

for i, p in enumerate(products):
    with (col1 if i % 2 == 0 else col2):
        st.markdown(f"""
        <div class="product-card">
            <h3 style="color: {t['text']};">{p['name']}</h3>
            <p style="color: #aaa; font-size: 0.9rem;">{p['desc']}</p>
            <div class="price-tag">${p['price']:,}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"تفعيل الاستثمار الآن 💳", key=f"buy_now_{i}"):
            st.balloons()
            st.success(f"تم تفعيل {p['name']}! راجع محفظتك لمتابعة الأثر المالي.")

st.divider()
if st.button("📊 الانتقال لحساب العمولات"):
    st.switch_page("pages/5_Commissions.py")
