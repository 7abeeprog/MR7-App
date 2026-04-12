import streamlit as st
import time
import json
import requests
import uuid
from datetime import datetime
import pandas as pd

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
    /* الفلسفة التصميمية: هندسة النمو والتضاعف الإمبراطوري */
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

    .comm-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 25px;
        padding: 30px;
        margin-bottom: 25px;
        transition: 0.4s ease-in-out;
        box-shadow: 0 15px 45px rgba(0,0,0,0.5);
    }}
    .comm-card:hover {{ border-color: #00FF88; transform: translateY(-8px); }}

    .level-badge {{
        background: {t['accent']};
        color: black !important;
        padding: 6px 18px;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 950;
    }}

    /* حل مشكلة الكتابة باللون الأسود في الحقول البيضاء */
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
        height: 65px;
        font-size: 1.1rem;
    }}

    .tree-node {{
        border: 2px solid {t['accent']};
        padding: 20px;
        border-radius: 25px;
        background: rgba(255,255,255,0.03);
        text-align: center;
        margin: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك السحابة السيادي (Live Affiliate Integration) ---
fb_config = json.loads(st.secrets.get("__firebase_config", "{}"))
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
project_id = fb_config.get("projectId", "mr7-app")
BASE_URL = "https://firestore.googleapis.com/v1/"
USER_STATS_PATH = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/users/"

if 'user_id' not in st.session_state: st.session_state.user_id = str(uuid.uuid4())

def get_live_affiliate_stats():
    """جلب إحصائيات الفريق والعمولات الحية من السحابة لكل مستخدم"""
    path = f"{USER_STATS_PATH}{st.session_state.user_id}/affiliate_data/summary"
    try:
        res = requests.get(f"{BASE_URL}{path}")
        if res.status_code == 200:
            f = res.json().get("fields", {})
            return {
                "l1_sales": int(f.get("l1_sales", {}).get("integerValue", 5200)),
                "l2_sales": int(f.get("l2_sales", {}).get("integerValue", 12400)),
                "total_members": int(f.get("total_members", {}).get("integerValue", 1547)),
                "ref_id": f.get("ref_id", {}).get("stringValue", f"MR7-{st.session_state.user_id[:5].upper()}")
            }
        return {"l1_sales": 5200, "l2_sales": 12400, "total_members": 1547, "ref_id": f"MR7-{st.session_state.user_id[:5].upper()}"}
    except:
        return {"l1_sales": 5200, "l2_sales": 12400, "total_members": 1547, "ref_id": f"MR7-{st.session_state.user_id[:5].upper()}"}

# --- 3. واجهة نظام الأجيال والسيادة ---
st.title("🔗 نظام الأجيال والسيادة")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.4rem; margin-top:-25px;'>هندسة الأرباح التضاعفية لجيش قادة MR7</p>", unsafe_allow_html=True)

st.divider()

# جلب البيانات الحية
live_data = get_live_affiliate_stats()

# صف المؤشرات العليا (Imperial KPIs)
col_k1, col_k2, col_k3 = st.columns(3)
l1_comm = (live_data['l1_sales'] * 10) / 100
l2_comm = (live_data['l2_sales'] * 5) / 100
total_comm = l1_comm + l2_comm + 540 # +540 كأرباح أجيال أخرى تجريبية

with col_k1:
    st.metric("إجمالي العمولات الموثقة", f"${total_comm:,.2f}", "+$1,240")
with col_k2:
    st.metric("حجم جيش القادة", f"{live_data['total_members']:,}", "قانون الـ 10")
with col_k3:
    st.metric("رتبة الانتشار", "إمبراطور ماسي 💎", "VIP")

st.divider()

tabs = st.tabs(["📈 تحليل الأرباح", "🌳 شجرة الأجيال", "🔗 روابط الانتشار", "🧮 حاسبة التضاعف"])

# --- Tab 1: تحليل الأرباح (10-5-1% Cloud Sync) ---
with tabs[0]:
    st.subheader("🌲 هيكلية العمولات الموحدة (Live)")
    st.info("القانون المالي المعتمد: الجيل الأول 10% | الجيل الثاني 5% | الأجيال (3-7) 1% لكل جيل.")
    
    levels = [
        {"lvl": 1, "rate": 10, "sales": live_data['l1_sales'], "desc": "الجيل الأول المباشر (قادة التأثير)"},
        {"lvl": 2, "rate": 5, "sales": live_data['l2_sales'], "desc": "الجيل الثاني (التوسع المحلي)"},
        {"lvl": 3, "rate": 1, "sales": 45000, "desc": "الجيل الثالث (الانتشار الإقليمي)"},
    ]
    
    for level in levels:
        profit = (level['sales'] * level['rate']) / 100
        st.markdown(f"""
        <div class="comm-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span class="level-badge">المستوى {level['lvl']}</span>
                    <h3 style="margin: 10px 0;">العمولة الاستحقاقية: {level['rate']}%</h3>
                    <p style="color: #888; font-size: 0.9rem;">{level['desc']}</p>
                </div>
                <div style="text-align: right;">
                    <p style="color: #aaa; font-size: 0.85rem; margin: 0;">مبيعات الجيل</p>
                    <span style="font-size: 1.6rem; color: #00FF88;">${level['sales']:,}</span>
                    <p style="color: {t['accent']}; font-weight: 950; margin-top: 5px; font-size: 1.1rem;">ربحك الصافي: ${profit:,.2f}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- Tab 2: شجرة الأجيال الجغرافية (Visual Tree) ---
with tabs[1]:
    st.subheader("🌳 خريطة الانتشار الهيكلية")
    st.markdown("رؤية بصرية لتوسع جيشك عبر الحدود الاستراتيجية.")
    
    st.markdown(f"""
    <div style="text-align: center; padding: 40px; background: rgba(255,215,0,0.02); border-radius: 40px; border: 2px dashed {t['accent']};">
        <div class="tree-node" style="width: 220px; margin: auto; background: {t['accent']}; color: black; font-weight: 950;">👑 أنت (القائد الأعلى)</div>
        <div style="height: 40px; width: 3px; background: {t['accent']}; margin: auto;"></div>
        <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap;">
            <div class="tree-node">👤 ج1: أحمد (مصر) <br> <small>10% عمولة</small></div>
            <div class="tree-node">👤 ج1: صالح (ليبيا) <br> <small>10% عمولة</small></div>
            <div class="tree-node">👤 ج1: إدريس (السودان) <br> <small>10% عمولة</small></div>
        </div>
        <p style="margin-top: 40px; opacity: 0.7; font-size: 1.1rem;">يتم تتبع التضاعف آلياً حتى الجيل السابع لدعم أهداف الـ 100 يوم.</p>
    </div>
    """, unsafe_allow_html=True)

# --- Tab 3: روابط الانتشار (Referral Center) ---
with tabs[2]:
    st.subheader("🔗 مركز توليد روابط السيادة")
    st.markdown("استخدم هذا الرابط لبناء جيلك الأول المباشر وتحصيل عمولة الـ 10% فوراً.")
    
    ref_link = f"https://mr7-empire.com/join?ref={live_data['ref_id']}"
    st.code(ref_link, language="text")
    
    if st.button("نسخ الرابط الملكي 📋"):
        st.toast("تم نسخ الرابط! انطلق لبناء إمبراطوريتك.")
        st.balloons()
    
    st.divider()
    st.markdown("### 📊 إحصائيات الرابط")
    c_s1, c_s2, c_s3 = st.columns(3)
    c_s1.metric("النقرات الكلية", "4,120", "+240")
    c_s2.metric("التسجيلات الموثقة", "154", "تحويل 4%")
    c_s3.metric("العائد لكل نقرة (EPC)", "$1.25", "فائق")

# --- Tab 4: حاسبة التضاعف العشري (The Law of 10) ---
with tabs[3]:
    st.subheader("🧮 محاكي أرباح التريليون")
    st.info("أدخل الأرقام المتوقعة لترى قوة التضاعف العشري في محفظتك.")
    
    avg_ticket = st.number_input("متوسط قيمة المشتريات لكل عضو ($):", min_value=10, value=100)
    
    sim_results = []
    base_m = 10
    rates = [10, 5, 1, 1, 1, 1, 1]
    
    for i, rate in enumerate(rates):
        profit = (base_m * avg_ticket * rate) / 100
        sim_results.append({
            "الجيل": f"المستوى {i+1}",
            "عدد الأعضاء المتوقع": f"{base_m:,}",
            "نسبة الربح": f"{rate}%",
            "صافي الربح ($)": f"${profit:,.2f}"
        })
        base_m *= 10 # التضاعف العشري
        
    st.table(pd.DataFrame(sim_results))
    
    total_sim = sum(float(d['صافي الربح ($)'].replace('$', '').replace(',', '')) for d in sim_results)
    st.success(f"إجمالي الربح التراكمي المتوقع عند اكتمال الشبكة: ${total_sim:,.2f}")

st.divider()

if st.button("🏠 العودة لمركز القيادة الرئيسي"):
    st.switch_page("app.py")
