import streamlit as st
import time
import uuid
import json
import requests
from datetime import datetime
import base64

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
    /* الفلسفة التصميمية: سيادة، عمق، ووضوح Enterprise */
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

    /* رأس البروفايل الملكي (Elite Dashboard Header) */
    .profile-cover {{
        height: 300px;
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1510511459019-5dee997ddfdf?auto=format&fit=crop&q=80&w=2070') center/cover;
        border-radius: 40px 40px 0 0;
        border: 2px solid {t['accent']};
        border-bottom: none;
        position: relative;
    }}

    .elite-header {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 0 0 50px 50px;
        padding: 0 50px 40px 50px;
        text-align: center;
        margin-top: -100px;
        position: relative;
        box-shadow: 0 25px 60px rgba(0,0,0,0.8);
        z-index: 10;
    }}

    .avatar-glow {{
        width: 190px;
        height: 190px;
        border-radius: 50%;
        border: 6px solid {t['accent']};
        box-shadow: 0 0 45px {t['accent']};
        margin-bottom: 20px;
        background: #111;
        object-fit: cover;
    }}

    /* بطاقات الميزات عالية الكثافة */
    .feature-card {{
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        transition: 0.3s;
    }}
    .feature-card:hover {{ border-color: {t['accent']}; transform: translateY(-5px); background: rgba(255,215,0,0.05); }}

    /* حل مشكلة الكتابة باللون الأسود في الحقول البيضاء */
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid {t['border']} !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        opacity: 1 !important;
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

# --- 2. إدارة البيانات والهوية المتقدمة ---
if 'user_id' not in st.session_state: st.session_state.user_id = str(uuid.uuid4())
if 'leader_name' not in st.session_state: st.session_state.leader_name = "إمبراطور السيادة"
if 'discount_points' not in st.session_state: st.session_state.discount_points = 12500
if 'reward_balance' not in st.session_state: st.session_state.reward_balance = 1250.00
if 'profile_pic_b64' not in st.session_state: st.session_state.profile_pic_b64 = None

# --- 3. القائمة الجانبية (أدوات القائد) ---
with st.sidebar:
    st.markdown(f"### 🎨 تخصيص المنظومة")
    theme_choice = st.selectbox("نمط الواجهة:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    
    with st.expander("👤 إدارة الهوية البصرية"):
        st.session_state.leader_name = st.text_input("اسم الشهرة العالمي:", st.session_state.leader_name)
        up_file = st.file_uploader("رفع ختم الصورة:", type=["png", "jpg", "jpeg"])
        if up_file:
            st.session_state.profile_pic_b64 = f"data:image/png;base64,{base64.b64encode(up_file.getvalue()).decode()}"
        if st.button("تأكيد الهوية"): st.success("تم التحديث!")

# --- 4. واجهة ملف القائد (The Enterprise Hub) ---
st.markdown('<div class="profile-cover"></div>', unsafe_allow_html=True)

avatar = st.session_state.profile_pic_b64 or f"https://api.dicebear.com/7.x/avataaars/svg?seed={st.session_state.user_id}"
st.markdown(f"""
<div class="elite-header">
    <img src="{avatar}" class="avatar-glow">
    <h2 style="color: {t['accent']}; font-size: 3rem; margin-bottom: 5px;">{st.session_state.leader_name}</h2>
    <p style="font-size: 1.1rem; opacity: 0.8;">Global Empire ID: <code>{st.session_state.user_id[:13]}</code></p>
    <div style="display: flex; justify-content: center; gap: 15px; margin-top: 15px;">
        <span style="background: {t['accent']}; color: black; padding: 6px 20px; border-radius: 50px; font-weight: 950;">VIP GOLD LEADER 👑</span>
        <span style="background: #00FF88; color: black; padding: 6px 20px; border-radius: 50px; font-weight: 950;">TRUST: 100% ✅</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# لوحة مؤشرات الأداء (Alibaba Analytics Style)
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
with col_stat1:
    st.markdown(f'<div class="feature-card" style="text-align:center;"><small>إجمالي الأرباح</small><br><span style="font-size:1.8rem; color:#00FF88;">${st.session_state.reward_balance:,.2f}</span></div>', unsafe_allow_html=True)
with col_stat2:
    st.markdown(f'<div class="feature-card" style="text-align:center;"><small>نقاط الخصم</small><br><span style="font-size:1.8rem; color:{t["accent"]};">{st.session_state.discount_points:,}</span></div>', unsafe_allow_html=True)
with col_stat3:
    st.markdown(f'<div class="feature-card" style="text-align:center;"><small>جيش القادة</small><br><span style="font-size:1.8rem; color:#FFFFFF;">8,500</span></div>', unsafe_allow_html=True)
with col_stat4:
    st.markdown(f'<div class="feature-card" style="text-align:center;"><small>الترتيب العالمي</small><br><span style="font-size:1.8rem; color:#FF4B4B;">#14</span></div>', unsafe_allow_html=True)

# تبويبات السيطرة (Enterprise Functions)
tabs = st.tabs(["🚀 محرك الانتشار", "💎 الخزنة والولاء", "📩 مركز المراسلات", "🛠️ مهندس SEO/GEO"])

with tabs[0]:
    st.subheader("🔗 مركز النمو العالمي (Affiliate Engine)")
    aff_link = f"https://mr7-empire.com/join?ref={st.session_state.user_id[:8].upper()}"
    st.code(aff_link, language="text")
    if st.button("نسخ الرابط ونشره عالمياً 🚀"): st.toast("تم النسخ! انطلق لبناء إمبراطوريتك.")

with tabs[1]:
    st.subheader("💎 إدارة المكافآت والسيولة")
    col_v1, col_v2 = st.columns([2, 1])
    with col_v1:
        st.markdown("#### 🎫 قسائم الخصم المفعلة")
        st.table([{"الكود": "EMPIRE_77", "الخصم": "25%", "الحالة": "نشط"}])
    with col_v2:
        st.markdown(f"""
        <div class="feature-card" style="background:rgba(0,255,136,0.05); text-align:center;">
            <p>متاح للسحب</p>
            <h2 style="color:#00FF88;">$500.00</h2>
            <button style="width:100%; height:40px; background:#00FF88; border:none; border-radius:12px; font-weight:900;">سحب فوري 💸</button>
        </div>
        """, unsafe_allow_html=True)

with tabs[2]:
    st.subheader("📩 مركز بريد القادة (Bulk Messenger)")
    with st.container():
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        target = st.selectbox("المستهدفين:", ["الجيل الأول", "جيش القادة بالكامل", "إدارة MR7"])
        subj = st.text_input("موضوع البرقية:")
        body = st.text_area("نص الرسالة القيادية:", height=150)
        if st.button("بث الرسالة عبر الأقمار الصناعية ⚡"):
            if body: 
                with st.spinner("جاري التشفير والبث..."):
                    time.sleep(2)
                    st.success("تم إرسال الرسالة لكافة القادة بنجاح!")
        st.markdown('</div>', unsafe_allow_html=True)

with tabs[3]:
    st.subheader("⚙️ هندسة الظهور العالمي")
    c_seo1, c_seo2 = st.columns(2)
    with c_seo1:
        st.markdown("#### 🌍 التواجد الجغرافي (GEO)")
        st.text_input("قاعدة العمليات:", "Dubai, UAE")
        st.multiselect("نطاق الظهور:", ["MENA", "Europe", "Global"], default=["MENA", "Global"])
    with c_seo2:
        st.markdown("#### 🔍 تحسين البحث (SEO)")
        st.text_area("كلمات المفتاح:", "Empire, Wealth, Leadership, MR7")
        st.progress(0.92)
        st.caption("قوة أرشفة بروفايلك: 92% (فائقة)")

st.divider()

# معرض الأصول التجارية
st.subheader("🖼️ معرض أصول الإمبراطورية (Business Portfolio)")
asset_cols = st.columns(3)
assets = [
    ("https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500&q=80", "الاستثمار العقاري الذكي"),
    ("https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=500&q=80", "أكاديمية تدريب النخبة"),
    ("https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=500&q=80", "مركز أبحاث الـ AI")
]
for i, (img, title) in enumerate(assets):
    with asset_cols[i]: st.image(img, caption=title, use_container_width=True)

# خريطة الانتقال (تم إصلاح الروابط لمنع الـ Crash)
st.divider()
st.markdown("### 🗺️ خريطة السيادة السريعة")
c_nav1, c_nav2, c_nav3, c_nav4 = st.columns(4)
with c_nav1:
    if st.button("🛒 المتجر العالمي"): st.switch_page("pages/4_Marketplace.py")
with c_nav2:
    if st.button("🔗 نظام الأجيال"): st.switch_page("pages/11_Affiliate_System.py")
with c_nav3:
    if st.button("💰 الخزنة المالية"): st.switch_page("pages/3_Wallet.py")
with c_nav4:
    if st.button("🏠 الرئيسية"): st.switch_page("app.py")
