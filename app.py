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
    /* الفلسفة التصميمية: مركز العمليات العالمي (Global Operations Center) */
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
        font-size: 3.8rem !important; 
    }}

    /* تصميم بطاقات المعلومات الحية (Live Scorecards) */
    .metric-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 25px;
        padding: 20px;
        text-align: center;
        transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }}
    .metric-card:hover {{ border-color: #00FF88; transform: translateY(-8px); }}

    .quick-link-box {{
        background: rgba(255,255,255,0.03);
        border-radius: 20px;
        padding: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
        cursor: pointer;
        transition: 0.3s;
    }}
    .quick-link-box:hover {{ background: rgba(255,215,0,0.05); border-color: {t['accent']}; }}

    /* حل مشكلة الكتابة باللون الأسود */
    .stTextInput input {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: bold !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 15px !important;
        height: 60px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة الجلسة والبيانات الحية (Global State) ---
if 'user_id' not in st.session_state: st.session_state.user_id = str(uuid.uuid4())
if 'logged_in' not in st.session_state: st.session_state.logged_in = True # محاكاة للدخول

# --- 3. واجهة لوحة القيادة المركزية ---
st.title("🏛️ الإمبراطورية")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.5rem; margin-top:-25px;'>مركز العمليات السيادية للقائد الأعلى</p>", unsafe_allow_html=True)

st.divider()

# صف المؤشرات الحية (Live KPIs)
col_k1, col_k2, col_k3, col_k4 = st.columns(4)
with col_k1:
    st.markdown(f'<div class="metric-card"><small>💰 الرصيد المتاح</small><br><span style="font-size:1.6rem; color:#00FF88;">$1.25M</span></div>', unsafe_allow_html=True)
with col_k2:
    st.markdown(f'<div class="metric-card"><small>👥 حجم الجيش</small><br><span style="font-size:1.6rem; color:{t["accent"]};">12,450</span></div>', unsafe_allow_html=True)
with col_k3:
    st.markdown(f'<div class="metric-card"><small>🔔 تنبيهات حية</small><br><span style="font-size:1.6rem; color:#FF4B4B;">+4</span></div>', unsafe_allow_html=True)
with col_k4:
    st.markdown(f'<div class="metric-card"><small>📈 قوة التضاعف</small><br><span style="font-size:1.6rem;">X10</span></div>', unsafe_allow_html=True)

st.divider()

# الأقسام الاستراتيجية (The Big Picture Layout)
col_main, col_side = st.columns([2, 1])

with col_main:
    st.subheader("🚀 حالة التقدم في رحلة الـ 100 يوم")
    st.progress(35)
    st.markdown("<p style='font-size:0.9rem; opacity:0.7;'>تم اجتياز 35 يوماً بنجاح. رتبتك الحالية: <b>قائد استراتيجي 💎</b></p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🌍 رادارات الأقاليم (مصر، ليبيا، السودان)")
    
    # خريطة مصغرة للنشاط الجغرافي
    c_geo1, c_geo2, c_geo3 = st.columns(3)
    with c_geo1:
        st.markdown('<div class="quick-link-box">🇪🇬 مصر<br><span style="color:#00FF88;">نشط جداً</span></div>', unsafe_allow_html=True)
    with c_geo2:
        st.markdown('<div class="quick-link-box">🇱🇾 ليبيا<br><span style="color:#FFD700;">توسع</span></div>', unsafe_allow_html=True)
    with c_geo3:
        st.markdown('<div class="quick-link-box">🇸🇩 السودان<br><span style="color:#0074D9;">ناشئ</span></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("💡 توصية الذكاء الاستراتيجي")
    st.info("نظام MR7-AI يقترح عليك ضخ 10% من أرباح اليوم في 'مشروع مدينة النبت' لزيادة العائد السنوي المتوقع.")

with col_side:
    st.subheader("🔗 وصول سريع")
    if st.button("💰 الخزنة المالية"): st.switch_page("pages/3_Wallet.py")
    if st.button("👥 جيش القادة"): st.switch_page("pages/6_Teams.py")
    if st.button("🤝 التمويل الجماعي"): st.switch_page("pages/9_Crowdfunding.py")
    if st.button("🛒 المتجر العالمي"): st.switch_page("pages/4_Marketplace.py")
    if st.button("🔔 مركز التنبيهات"): st.switch_page("pages/10_Notifications.py")
    if st.button("👤 ملفي الشخصي"): st.switch_page("pages/13_Leader_Profile.py")
    
    st.divider()
    st.markdown("### 🏆 مجلس القادة (توب 3)")
    st.markdown("""
    1. أحمد المؤسس (مصر) 🥇
    2. صالح الليبي (ليبيا) 🥈
    3. إدريس السوداني (السودان) 🥉
    """)

st.divider()

# شريط الحالة السفلي
st.markdown(f"<p style='text-align:center; opacity:0.5; font-size:0.8rem;'>منظومة MR7 - نسخة السيادة v2.0 | معرف القائد: {st.session_state.user_id[:8]}</p>", unsafe_allow_html=True)
