import streamlit as st
import time
from datetime import datetime
import json
import requests

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
    /* الفلسفة التصميمية: الشفافية والسيادة المالية المطلقة */
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
        filter: drop-shadow(0 0 15px {t['accent']}); 
        font-size: 3.5rem !important; 
    }}

    .balance-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 35px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        margin-bottom: 25px;
    }}

    .income-source {{
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        border-right: 4px solid #00FF88;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    /* حل مشكلة الكتابة باللون الأسود */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
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

# --- 2. إدارة البيانات المالية (Global Cash Flow) ---
if 'cash_balance' not in st.session_state:
    st.session_state.cash_balance = 1250000.00
if 'pending_commissions' not in st.session_state:
    st.session_state.pending_commissions = 2450.75

# --- 3. واجهة الخزنة الإمبراطورية ---
st.title("💰 الخزنة الإمبراطورية MR7")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.4rem; margin-top:-25px;'>إدارة السيولة الكونية والتدفقات النقدية العابرة للأقاليم</p>", unsafe_allow_html=True)

st.divider()

# عرض الرصيد الرئيسي
st.markdown(f"""
<div class="balance-card">
    <p style="color: {t['accent']} !important; font-size: 1.2rem; letter-spacing: 2px;">إجمالي الرصيد القابل للسحب</p>
    <h1 style="font-size: 4.5rem !important; margin: 10px 0;">${st.session_state.cash_balance:,.2f}</h1>
    <div style="display: flex; justify-content: center; gap: 20px; margin-top: 15px;">
        <span style="color: #00FF88;">عمولات معلقة: ${st.session_state.pending_commissions:,.2f}</span>
        <span style="color: {t['accent']};">|</span>
        <span style="color: #FFFFFF;">قوة الشراء: فائقة</span>
    </div>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs(["📊 تدفقات الأقاليم", "💸 سحب وإيداع", "📜 سجل التدقيق المالي", "🔮 توقعات التضاعف"])

# --- Tab 1: تدفقات الأقاليم (Regional Sync) ---
with tabs[0]:
    st.subheader("📍 مصادر الدخل السيادي الحية")
    st.markdown("توزيع الأرباح بناءً على المشاريع النشطة في مصر وليبيا والسودان.")
    
    regional_incomes = [
        {"المنطقة": "🇪🇬 مصر (مجمع السيارات)", "الربح المحقق": "$5,240.00", "الحالة": "جاهز للسحب"},
        {"المنطقة": "🇱🇾 ليبيا (مشاريع صغرى)", "الربح المحقق": "$1,120.50", "الحالة": "قيد المزامنة"},
        {"المنطقة": "🇸🇩 السودان (سلة الغذاء)", "الربح المحقق": "$850.00", "الحالة": "جاهز للسحب"},
        {"الالمنطقة": "🌎 التجارة العالمية (المتجر)", "الربح المحقق": "$12,400.00", "الحالة": "تم الإيداع ✅"}
    ]
    
    for item in regional_incomes:
        st.markdown(f"""
        <div class="income-source">
            <span>{item['المنطقة']}</span>
            <span style="color: #00FF88; font-weight: 900;">{item['الربح المحقق']}</span>
            <small style="opacity: 0.6;">{item['الحالة']}</small>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🔄 مزامنة كافة أرباح الأقاليم الآن"):
        with st.spinner("جاري التواصل مع المحركات المالية الإقليمية..."):
            time.sleep(2)
            st.success("تمت مزامنة الأرباح! الرصيد المتاح زاد بقيمة $6,090")
            st.session_state.cash_balance += 6090
            st.rerun()

# --- Tab 2: سحب وإيداع ---
with tabs[1]:
    st.subheader("💸 إدارة السيولة النقدية")
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        st.markdown("#### إيداع استراتيجي")
        st.number_input("المبلغ المطلوب ضخه ($):", min_value=10, step=100)
        st.button("💳 شحن عبر البوابة العالمية")
    with col_w2:
        st.markdown("#### سحب الأرباح")
        st.number_input("المبلغ المطلوب سحبه ($):", min_value=10, max_value=int(st.session_state.cash_balance), step=100)
        st.button("🏦 تحويل للحساب البنكي الموثق")

# --- Tab 3: سجل التدقيق المالي ---
with tabs[2]:
    st.subheader("📜 كشف حساب الإمبراطورية")
    ledger = [
        {"التاريخ": "2026-04-12", "العملية": "أرباح مجمع سيارات مصر", "القيمة": "+$5,240", "الرصيد": "$1.25M"},
        {"التاريخ": "2026-04-11", "العملية": "عمولة شبكة (الجيل الأول)", "القيمة": "+$450", "الرصيد": "$1.24M"},
    ]
    st.table(ledger)

# --- Tab 4: توقعات التضاعف (Financial Advanced Bridge) ---
with tabs[3]:
    st.subheader("🔮 رؤية النمو المالي")
    st.markdown("تحليل ذكاء اصطناعي لمستقبل محفظتك بناءً على الأداء الحالي.")
    st.info("بناءً على نشاطك في إقليم 'مصر'، يتوقع النظام نمواً في رصيدك بنسبة 24% خلال الـ 6 أشهر القادمة.")
    if st.button("📉 فتح المحاكي المالي المتقدم"):
        st.switch_page("pages/14_Financial_Advanced.py")

st.divider()

# خريطة الانتقال
st.markdown("### 🗺️ خريطة السيادة السريعة")
c_b1, c_b2, c_b3 = st.columns(3)
with c_b1:
    if st.button("👥 جيش القادة"): st.switch_page("pages/6_Teams.py")
with c_b2:
    if st.button("🤝 التمويل الجماعي"): st.switch_page("pages/9_Crowdfunding.py")
with c_b3:
    if st.button("🏠 العودة للرئيسية"): st.switch_page("app.py")
