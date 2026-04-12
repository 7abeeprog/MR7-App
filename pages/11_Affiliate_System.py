import streamlit as st
import time
import json
import requests
import uuid
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
    /* الفلسفة التصميمية: هندسة النمو والتضاعف */
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
        font-size: 3.5rem !important; 
    }}

    .comm-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 25px;
        padding: 25px;
        margin-bottom: 20px;
        transition: 0.4s;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .comm-card:hover {{ border-color: #00FF88; transform: translateY(-5px); }}

    .level-badge {{
        background: {t['accent']};
        color: black !important;
        padding: 5px 15px;
        border-radius: 12px;
        font-size: 0.9rem;
        font-weight: 900;
    }}

    /* تصميم شجرة الأجيال السحابية */
    .tree-node {{
        border: 2px solid {t['accent']};
        padding: 15px;
        border-radius: 20px;
        background: rgba(255,255,255,0.03);
        text-align: center;
        margin: 10px;
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

# --- 2. محرك قاعدة البيانات والعمولات (Live Logic) ---
fb_config = json.loads(st.secrets.get("__firebase_config", "{}"))
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
project_id = fb_config.get("projectId", "mr7-app")

BASE_URL = "https://firestore.googleapis.com/v1/"
COLLECTION_PATH = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/public/data/affiliate_stats"

def fetch_affiliate_data():
    """جلب بيانات النمو والأرباح من السحابة"""
    # محاكاة البيانات بناءً على القانون المالي الموحد (10-5-1)
    return [
        {"lvl": 1, "rate": 10, "members": 12, "sales": 5200, "desc": "الجيل الأول المباشر (قادة التأثير)"},
        {"lvl": 2, "rate": 5, "members": 85, "sales": 12400, "desc": "الجيل الثاني (التوسع المحلي)"},
        {"lvl": 3, "rate": 1, "members": 340, "sales": 45000, "desc": "الجيل الثالث (الانتشار الإقليمي)"},
        {"lvl": 4, "rate": 1, "members": 1200, "sales": 98000, "desc": "الجيل الرابع (التمدد الجغرافي)"},
        {"lvl": 5, "rate": 1, "members": 4500, "sales": 250000, "desc": "الجيل الخامس (السيادة الدولية)"},
        {"lvl": 6, "rate": 1, "members": 12000, "sales": 650000, "desc": "الجيل السادس (إمبراطورية المليار)"},
        {"lvl": 7, "rate": 1, "members": 45000, "sales": 1200000, "desc": "الجيل السابع (القمة الأسطورية)"},
    ]

# --- 3. واجهة نظام العمولات الذكي ---
st.title("🔗 نظام الأجيال والسيادة")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.4rem; margin-top:-25px;'>هندسة الأرباح التضاعفية لجيش قادة MR7</p>", unsafe_allow_html=True)

st.divider()

# ملخص الأداء المالي الموحد
col_sum1, col_sum2, col_sum3 = st.columns(3)
data = fetch_affiliate_data()
total_earned = sum((level['sales'] * level['rate']) / 100 for level in data)
total_network = sum(level['members'] for level in data)

with col_sum1:
    st.metric("إجمالي العمولات الموثقة", f"${total_earned:,.2f}", "+12% اليوم")
with col_sum2:
    st.metric("حجم جيش القادة", f"{total_network:,}", "قانون الـ 10")
with col_sum3:
    st.metric("رتبة الانتشار", "إمبراطور ماسي", "VIP")

st.divider()

tabs = st.tabs(["📈 تحليل الأرباح", "🌳 شجرة الأجيال", "🔗 روابط الانتشار", "🧮 حاسبة التضاعف"])

# --- Tab 1: تحليل الأرباح (10-5-1% Logic) ---
with tabs[0]:
    st.subheader("🌲 هيكلية العمولات الموحدة")
    st.info("القانون المالي: الجيل الأول 10% | الجيل الثاني 5% | الأجيال (3-7) 1% لكل جيل.")
    
    for level in data:
        profit = (level['sales'] * level['rate']) / 100
        st.markdown(f"""
        <div class="comm-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span class="level-badge">المستوى {level['lvl']}</span>
                    <h3 style="margin: 5px 0;">العمولة: {level['rate']}%</h3>
                    <p style="color: #888; font-size: 0.85rem;">{level['desc']}</p>
                </div>
                <div style="text-align: right;">
                    <p style="color: #aaa; font-size: 0.8rem; margin: 0;">مبيعات الجيل</p>
                    <span style="font-size: 1.4rem; color: #00FF88;">${level['sales']:,}</span>
                    <p style="color: {t['accent']}; font-weight: 900; margin-top: 5px;">ربحك: ${profit:,.2f}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- Tab 2: شجرة الأجيال (Visual Tree) ---
with tabs[1]:
    st.subheader("🌳 خريطة الانتشار الهيكلية")
    st.markdown("رؤية بصرية لتوسع جيشك عبر الحدود (مصر، ليبيا، السودان).")
    
    # تمثيل مبسط للشجرة
    st.markdown(f"""
    <div style="text-align: center; padding: 40px; background: rgba(255,215,0,0.02); border-radius: 30px; border: 1px dashed {t['accent']};">
        <div class="tree-node" style="width: 150px; margin: auto; background: {t['accent']}; color: black; font-weight: 900;">👑 أنت (القائد)</div>
        <div style="height: 30px; width: 2px; background: {t['accent']}; margin: auto;"></div>
        <div style="display: flex; justify-content: center; gap: 20px;">
            <div class="tree-node">👤 ج1: أحمد (مصر)</div>
            <div class="tree-node">👤 ج1: صالح (ليبيا)</div>
            <div class="tree-node">👤 ج1: إدريس (السودان)</div>
        </div>
        <p style="margin-top: 20px; opacity: 0.6;">... تستمر الشجرة تلقائياً حتى الجيل السابع (+58,000 عضو إضافي)</p>
    </div>
    """, unsafe_allow_html=True)

# --- Tab 3: روابط الانتشار ---
with tabs[2]:
    st.subheader("🔗 مركز توليد روابط السيادة")
    my_ref = f"REF-{uuid.uuid4().hex[:8].upper()}"
    st.markdown("استخدم هذا الرابط لبناء جيلك الأول. كل مسجل عن طريقك يمنحك 10% من مشترياته مدى الحياة.")
    
    link = f"https://mr7-empire.com/join?ref={my_ref}"
    st.code(link, language="text")
    if st.button("نسخ الرابط الملكي 📋"):
        st.toast("تم النسخ! انطلق لغزو الأسواق.")
    
    st.divider()
    st.markdown("### 📊 أداء الروابط")
    c1, c2 = st.columns(2)
    c1.metric("عدد النقرات", "1,240", "تفاعل عالي")
    c2.metric("معدل التحويل", "14%", "ناجح")

# --- Tab 4: حاسبة التضاعف العشري ---
with tabs[3]:
    st.subheader("🧮 محاكي أرباح التريليون")
    avg_order = st.number_input("متوسط قيمة طلب العضو ($):", min_value=10, value=100)
    
    # حساب التضاعف
    sim_data = []
    current_m = 10
    for level in data:
        sim_profit = (current_m * avg_order * level['rate']) / 100
        sim_data.append({
            "الجيل": f"المستوى {level['lvl']}",
            "الأعضاء (تضاعف 10)": f"{current_m:,}",
            "الربح المتوقع": f"${sim_profit:,.2f}"
        })
        current_m *= 10
    
    st.table(sim_data)
    st.success(f"إجمالي الربح المتوقع في حال التزام الجميع بقانون الـ 10: ${sum(float(d['ال الربح المتوقع'].replace('$', '').replace(',', '')) for d in sim_data):,.2f}")

st.divider()
if st.button("🏠 العودة لمركز القيادة الرئيسي"):
    st.switch_page("app.py")
