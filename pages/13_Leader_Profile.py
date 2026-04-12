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
    /* الفلسفة التصميمية: الهوية القيادية الموثقة */
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

    /* غلاف البروفايل الفاخر (Imperial Cover) */
    .profile-cover {{
        height: 280px;
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1510511459019-5dee997ddfdf?auto=format&fit=crop&q=80&w=2070') center/cover;
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

    .stat-tile {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        transition: 0.3s;
    }}
    .stat-tile:hover {{ border-color: #00FF88; transform: translateY(-5px); }}

    /* حل مشكلة الكتابة باللون الأسود في الحقول البيضاء */
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
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

# --- 2. إدارة البيانات والهوية المتقدمة ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'leader_name' not in st.session_state:
    st.session_state.leader_name = "القائد الإمبراطوري"
if 'user_rank' not in st.session_state:
    st.session_state.user_rank = "قائد استراتيجي 💎"
if 'profile_pic_b64' not in st.session_state:
    st.session_state.profile_pic_b64 = None

# --- 3. الشريط الجانبي (إدارة الهوية) ---
with st.sidebar:
    st.markdown(f"### 🎨 تخصيص المنظومة")
    theme_choice = st.selectbox("نمط الواجهة:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    
    with st.expander("👤 إدارة الهوية الرقمية"):
        st.session_state.leader_name = st.text_input("اسم الشهرة العالمي:", st.session_state.leader_name)
        up_file = st.file_uploader("رفع ختم الصورة الشخصية:", type=["png", "jpg", "jpeg"])
        if up_file:
            st.session_state.profile_pic_b64 = f"data:image/png;base64,{base64.b64encode(up_file.getvalue()).decode()}"
        if st.button("تأكيد وتوثيق الهوية"):
            st.success("تم تحديث السجلات الإمبراطورية!")
            time.sleep(1)
            st.rerun()

# --- 4. واجهة ملف القائد (The Masterpiece) ---
# غلاف البروفايل
st.markdown('<div class="profile-cover"></div>', unsafe_allow_html=True)

# رأس البروفايل (Elite Header)
display_avatar = st.session_state.profile_pic_b64 or f"https://api.dicebear.com/7.x/avataaars/svg?seed={st.session_state.user_id}"
st.markdown(f"""
<div class="elite-header">
    <img src="{display_avatar}" class="avatar-glow">
    <h2 style="color: {t['accent']}; font-size: 3rem; margin-bottom: 5px;">{st.session_state.leader_name}</h2>
    <p style="font-size: 1.1rem; opacity: 0.8;">معرف القيادة الموحد: <code>{st.session_state.user_id[:13]}</code></p>
    <div style="display: flex; justify-content: center; gap: 15px; margin-top: 15px;">
        <span style="background: {t['accent']}; color: black; padding: 6px 20px; border-radius: 50px; font-weight: 950;">{st.session_state.user_rank}</span>
        <span style="background: #00FF88; color: black; padding: 6px 20px; border-radius: 50px; font-weight: 950;">موثق بالكامل ✅</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# القسم الثاني: إحصائيات السيادة اللحظية (KPIs)
st.subheader("📈 لوحة مؤشرات السيادة")
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    st.markdown(f'<div class="stat-tile"><small>صافي الثروة</small><br><span style="font-size:1.8rem; color:#00FF88;">$1.25M</span></div>', unsafe_allow_html=True)
with col_stat2:
    st.markdown(f'<div class="stat-tile"><small>جيش القادة</small><br><span style="font-size:1.8rem; color:{t["accent"]};">12,450</span></div>', unsafe_allow_html=True)
with col_stat3:
    st.markdown(f'<div class="stat-tile"><small>قوة التأثير</small><br><span style="font-size:1.8rem;">98%</span></div>', unsafe_allow_html=True)
with col_stat4:
    st.markdown(f'<div class="stat-tile"><small>معدل التضاعف</small><br><span style="font-size:1.8rem; color:#FF4B4B;">X10</span></div>', unsafe_allow_html=True)

st.divider()

# التبويبات التفصيلية
tabs = st.tabs(["🏛️ ميثاق الرؤية", "🏆 جدار الأوسمة", "💬 سجل النشاط الاستراتيجي", "⚙️ إعدادات SEO/GEO"])

with tabs[0]:
    st.markdown(f"""
    <div style="background: {t['card']}; padding: 35px; border-radius: 30px; border: 2px solid {t['accent']};">
        <h3 style="color: {t['accent']};">بوصلة التريليون الموثقة</h3>
        <p style="font-size: 1.5rem; line-height: 1.8;">"أقسمت أن أقود فريقاً نحو الحرية المالية المطلقة، وبناء نظام تعليمي يغير وجه المنطقة العربية تجارياً، والوصول لرأس مال قدره 100 مليون دولار بحلول 2027."</p>
        <hr style="opacity: 0.1;">
        <div style="display: flex; justify-content: space-between; font-size: 0.9rem; opacity: 0.7;">
            <span>حالة الميثاق: <b>نشط ✅</b></span>
            <span>تاريخ الانعقاد: <b>2026-04-12</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 تحديث ميثاق الرؤية"):
        st.switch_page("pages/0_My_Vision.py")

with tabs[1]:
    st.subheader("🏅 خزنة الأوسمة والاستحقاقات")
    col_b1, col_b2, col_b3 = st.columns(3)
    badges = [
        ("🥇 باني الإمبراطورية", "إتمام أول 1000 عضو في الفريق", "icon"),
        ("🧠 مهندس العقول", "اجتياز اختبارات عقلية المليار", "icon"),
        ("🌍 عابر الحدود", "بناء فريق في 3 دول (مصر، ليبيا، السودان)", "icon")
    ]
    for i, (name, desc, _) in enumerate(badges):
        with [col_b1, col_b2, col_b3][i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 25px; border: 1px solid {t['border']}; border-radius: 20px; background: rgba(255,215,0,0.02);">
                <div style="font-size: 3.5rem;">🏅</div>
                <h4 style="color: {t['accent']}; margin: 10px 0;">{name}</h4>
                <p style="font-size: 0.8rem; opacity: 0.7;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

with tabs[2]:
    st.subheader("💬 آخر ما بثت رؤيتك في الساحة")
    st.info("سجل المنشورات التي شاركتها مع المجتمع العالمي للقادة.")
    st.markdown("""
    <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 15px; border-right: 4px solid #00FF88; margin-bottom: 15px;">
        <p style="font-weight: 800; margin-bottom: 5px;">"السيادة لا تمنح، بل تنتزع بقوة التضاعف العشري واتساع رقعة الفريق."</p>
        <small style="color: #666;">منذ 3 ساعات • 154 تأييد 👍</small>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🌐 الانتقال للساحة العالمية"):
        st.switch_page("pages/12_Social_Network.py")

with tabs[3]:
    st.subheader("⚙️ هندسة الظهور العالمي (Visibility)")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.text_input("قاعدة العمليات الجغرافية (GEO):", "New Cairo, Egypt")
        st.multiselect("نطاق البحث المفضل:", ["مصر", "ليبيا", "السودان", "عالمي"], default=["مصر", "عالمي"])
    with col_v2:
        st.text_area("الكلمات المفتاحية للبروفايل (SEO):", "Wealth Engineering, Global Leadership, MR7 Expert")
        st.progress(0.92)
        st.caption("قوة أرشفة البروفايل عالمياً: 92%")

st.divider()

# خريطة الانتقال السريع (Imperial Navigation)
st.markdown("### 🗺️ خريطة السيادة السريعة")
c_nav1, c_nav2, c_nav3, c_nav4 = st.columns(4)
with c_nav1:
    if st.button("💰 الخزنة المالية"): st.switch_page("pages/3_Wallet.py")
with c_nav2:
    if st.button("👥 جيش القادة"): st.switch_page("pages/6_Teams.py")
with c_nav3:
    if st.button("🛒 المتجر العالمي"): st.switch_page("pages/4_Marketplace.py")
with c_nav4:
    if st.button("🏠 الرئيسية"): st.switch_page("app.py")
