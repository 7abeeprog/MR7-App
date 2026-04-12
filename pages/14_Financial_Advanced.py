import streamlit as st
import time
import pandas as pd
import numpy as np
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

# --- 2. محرك الاتصال بالسحابة (Live Cloud Integration) ---
fb_config = json.loads(st.secrets.get("__firebase_config", "{}"))
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
project_id = fb_config.get("projectId", "mr7-app")
BASE_URL = "https://firestore.googleapis.com/v1/"
PROJECTS_PATH = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/public/data/crowd_projects"

def fetch_approved_projects():
    """جلب المشاريع المعتمدة فقط لحساب الأرباح الحية"""
    try:
        res = requests.get(f"{BASE_URL}{PROJECTS_PATH}")
        if res.status_code == 200:
            docs = res.json().get("documents", [])
            approved = []
            for doc in docs:
                f = doc.get("fields", {})
                if f.get("status", {}).get("stringValue") == "approved":
                    approved.append({
                        "id": doc["name"].split("/")[-1],
                        "title": f.get("title", {}).get("stringValue", "غير مسمى"),
                        "country": f.get("country", {}).get("stringValue", "مجهول"),
                        "roi": f.get("roi", {}).get("stringValue", "0%"),
                        "raised": int(f.get("raised", {}).get("integerValue", "0"))
                    })
            return approved
        return []
    except: return []

# --- 3. إدارة الحالة المالية (State Integration) ---
if 'cash_balance' not in st.session_state:
    st.session_state.cash_balance = 1250000.00

# --- 4. واجهة الحسابات المتقدمة ---
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
        <h3 style="color: #00FF88; text-align: center;">الرصيد النهائي المتوقع بعد {years} سنوات:</h3>
        <h1 style="text-align: center; color: #FFFFFF !important;">${balance:,.2f}</h1>
        <p style="text-align: center; opacity: 0.7;">بناءً على تكرار الأرباح وإعادة استثمارها آلياً.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.line_chart(df.set_index("السنة"))

# --- Tab 2: توزيع أرباح المشاريع (Regional Projects - Live) ---
with tabs[1]:
    st.subheader("🏢 عوائد المشاريع الإقليمية الحية")
    st.markdown("يتم استرداد هذه البيانات مباشرة من قاعدة البيانات السحابية.")
    
    live_projects = fetch_approved_projects()
    
    if not live_projects:
        st.warning("لا توجد مشاريع استثمارية معتمدة حالياً لجلب أرباحها.")
    else:
        # حساب الربح التقريبي بناءً على النسبة المئوية المسجلة (مثلاً 24%)
        total_p = 0
        p_list = []
        for p in live_projects:
            # استخراج الرقم من نص مثل "24%"
            rate_val = int(p['roi'].replace('%', '')) / 100
            # افتراض حصة القائد هي 1% من المبلغ المجموع للتوضيح
            my_share = p['raised'] * 0.01 
            profit_val = my_share * rate_val
            total_p += profit_val
            p_list.append({
                "المشروع": p['title'],
                "الدولة": p['country'],
                "العائد": p['roi'],
                "حصتك في الأصول": f"${my_share:,.0f}",
                "الربح المستحق": f"${profit_val:,.2f}",
                "val": profit_val
            })
            
        st.table(pd.DataFrame(p_list).drop(columns=['val']))
        
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: rgba(0, 255, 136, 0.05); border-radius: 20px; border: 1px dashed #00FF88; margin-bottom: 20px;">
            <span style="font-size: 1.1rem;">إجمالي الأرباح المستحقة للترحيل الفوري: </span>
            <b style="font-size: 1.8rem; color: #00FF88;">${total_p:,.2f}</b>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💰 ترحيل الأرباح السحابية إلى الخزنة"):
            with st.spinner("جاري مزامنة السجلات المالية العالمية..."):
                time.sleep(2)
                st.session_state.cash_balance += total_p
                st.success(f"تم ترحيل ${total_p:,.2f} بنجاح! رصيدك الكلي الآن: ${st.session_state.cash_balance:,.2f}")
                st.balloons()
                time.sleep(1)
                st.rerun()

# --- Tab 3: تحليل التدفقات النقدية ---
with tabs[2]:
    st.subheader("📊 مراقبة تدفق السيولة الجغرافية")
    st.markdown("توزيع السيولة النقدية بناءً على الأقاليم النشطة.")
    
    source_data = pd.DataFrame({
        "الدولة": ["مصر", "ليبيا", "السودان", "عالمي"],
        "السيولة ($)": [450000, 250000, 150000, 400000]
    })
    st.bar_chart(source_data.set_index("الدولة"))
    
    st.info("💡 تحليل MR7: إقليم مصر يقود التدفقات بنسبة 45% نتيجة لنمو المشاريع الصناعية.")

st.divider()

col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    if st.button("💰 الانتقال للمحفظة الرئيسية"):
        st.switch_page("pages/3_Wallet.py")
with col_nav2:
    if st.button("🏠 العودة لمركز القيادة"):
        st.switch_page("app.py")
