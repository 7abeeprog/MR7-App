import streamlit as st
import time
import pandas as pd
import numpy as np

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

    .finance-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 30px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 15px 45px rgba(0,0,0,0.5);
    }}

    .stNumberInput input {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
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

# --- 2. محرك الحسابات المالية المتقدمة ---
st.title("📈 نظام الحسابات المتقدم")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.4rem; margin-top:-25px;'>محاكي التضاعف المالي والعوائد السيادية المركبة</p>", unsafe_allow_html=True)

st.divider()

tabs = st.tabs(["🚀 محاكي العوائد المركبة", "🏢 توزيع أرباح المشاريع", "📊 تحليل التدفقات النقدية"])

# --- Tab 1: محاكي العوائد المركبة (Compound Growth) ---
with tabs[0]:
    st.subheader("🧬 هندسة النمو المالي المستقبلي")
    st.info("قم بضبط معايير استثمارك لترى كيف ستتضاعف ثروتك عبر سنوات النهضة.")
    
    col1, col2 = st.columns(2)
    with col1:
        initial_inv = st.number_input("المبلغ التأسيسي ($):", min_value=100, value=10000, step=1000)
        annual_rate = st.slider("معدل العائد السنوي المتوقع (%):", 5, 100, 24)
    with col2:
        years = st.slider("فترة الاستثمار (بالسنوات):", 1, 30, 5)
        monthly_cont = st.number_input("الضخ الشهري الإضافي ($):", min_value=0, value=500)

    # حساب العائد المركب
    total_months = years * 12
    monthly_rate = (annual_rate / 100) / 12
    
    balance = initial_inv
    history = []
    
    for month in range(1, total_months + 1):
        balance = (balance + monthly_cont) * (1 + monthly_rate)
        if month % 12 == 0:
            history.append({"السنة": month // 12, "إجمالي الرصيد ($)": balance})
            
    df = pd.DataFrame(history)
    
    st.markdown(f"""
    <div class="finance-card">
        <h3 style="color: #00FF88; text-align: center;">الرصيد النهائي المتوقع: ${balance:,.2f}</h3>
        <p style="text-align: center; opacity: 0.7;">بناءً على تكرار الأرباح وإعادة استثمارها آلياً.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.line_chart(df.set_index("السنة"))

# --- Tab 2: توزيع أرباح المشاريع (Regional Projects) ---
with tabs[1]:
    st.subheader("🏢 عوائد المشاريع الإقليمية (مصر، ليبيا، السودان)")
    st.markdown("تحليل العوائد المباشرة من المشاريع السيادية النشطة في الأقاليم.")
    
    project_data = [
        {"المشروع": "مجمع السيارات الكهربائية (مصر)", "العائد الحالي": "24%", "حصة القائد": "$5,000", "الربح الموزع": "$1,200"},
        {"المشروع": "مبادرة الـ 20 ألف مشروع (ليبيا)", "العائد الحالي": "12%", "حصة القائد": "$2,000", "الربح الموزع": "$240"},
        {"المشروع": "سلة غذاء العرب (السودان)", "العائد الحالي": "19%", "حصة القائد": "$3,000", "الربح الموزع": "$570"}
    ]
    st.table(project_data)
    
    if st.button("💰 تحويل الأرباح للمحفظة المركزية"):
        with st.spinner("جاري تدقيق الحصص الضريبية والتحويل..."):
            time.sleep(2)
            st.success("تم تحويل $2,010 إلى خزنتك الإمبراطورية بنجاح! ✅")

# --- Tab 3: تحليل التدفقات النقدية ---
with tabs[2]:
    st.subheader("📊 مراقبة تدفق السيولة العالمية")
    st.markdown("توزيع السيولة النقدية في محفظة القائد حسب القطاعات الجغرافية.")
    
    source_data = pd.DataFrame({
        "الدولة": ["مصر", "ليبيا", "السودان", "عالمي"],
        "السيولة ($)": [450000, 250000, 150000, 400000]
    })
    st.bar_chart(source_data.set_index("الدولة"))
    
    st.info("💡 ملاحظة: إقليم مصر يمثل 45% من تدفقاتك النقدية الحالية نظراً لنمو قطاع التصنيع الثقيل.")

st.divider()

if st.button("🏠 العودة لمركز القيادة الرئيسي"):
    st.switch_page("app.py")
