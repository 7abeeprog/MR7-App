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
    /* التنسيق العام بمستوى Enterprise */
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

    /* غلاف البروفايل (Cover Photo) الفاخر */
    .profile-cover {{
        height: 280px;
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1579546929518-9e396f3cc809?auto=format&fit=crop&q=80&w=2070') center/cover;
        border-radius: 40px 40px 0 0;
        border: 2px solid {t['accent']};
        border-bottom: none;
        position: relative;
    }}

    /* حاوية رأس البروفايل */
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

    /* بطاقات الميزات (Merchant Style) */
    .feature-card {{
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        transition: 0.3s;
    }}
    .feature-card:hover {{ border-color: {t['accent']}; transform: translateY(-5px); background: rgba(255,215,0,0.05); }}

    /* إحصائيات بنظام علي بابا */
    .dashboard-stat {{
        text-align: center;
        padding: 20px;
        background: rgba(255,255,255,0.03);
        border-radius: 15px;
        border-bottom: 4px solid {t['accent']};
    }}

    /* حل مشكلة الكتابة باللون الأسود صراحةً */
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
    
    /* تنسيق التبويبات */
    .stTabs [data-baseweb="tab-list"] {{ gap: 15px; }}
    .stTabs [data-baseweb="tab"] {{ font-weight: 900; font-size: 1.1rem; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات والهوية ---
if 'user_id' not in st.session_state: st.session_state.user_id = str(uuid.uuid4())
if 'leader_name' not in st.session_state: st.session_state.leader_name = "إمبراطور السيادة"
if 'discount_points' not in st.session_state: st.session_state.discount_points = 12500
if 'profile_pic_b64' not in st.session_state: st.session_state.profile_pic_b64 = None

# --- 3. القائمة الجانبية (إعدادات متقدمة) ---
with st.sidebar:
    st.markdown(f"### 🎨 تخصيص الواجهة")
    theme_choice = st.selectbox("نمط المنظومة:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    
    with st.expander("👤 تحديث الهوية البصرية"):
        st.session_state.leader_name = st.text_input("اسم الشهرة:", st.session_state.leader_name)
        up_file = st.file_uploader("رفع ختم الصورة:", type=["png", "jpg", "jpeg"])
        if up_file:
            st.session_state.profile_pic_b64 = f"data:image/png;base64,{base64.b64encode(up_file.getvalue()).decode()}"
        if st.button("حفظ الهوية"): st.success("تم التحديث!")

# --- 4. واجهة ملف القائد الاحترافية ---
# غلاف احترافي
st.markdown('<div class="profile-cover"></div>', unsafe_allow_html=True)

# رأس البروفايل (The Elite Hub)
avatar = st.session_state.profile_pic_b64 or f"https://api.dicebear.com/7.x/avataaars/svg?seed={st.session_state.user_id}"
st.markdown(f"""
<div class="elite-header">
    <img src="{avatar}" class="avatar-glow">
    <h2 style="color: {t['accent']}; font-size: 3rem; margin-bottom: 5px;">{st.session_state.leader_name}</h2>
    <p style="font-size: 1.1rem; opacity: 0.8; font-family: monospace;">Global Leader ID: {st.session_state.user_id[:13]}</p>
    <div style="display: flex; justify-content: center; gap: 15px; margin-top: 20px;">
        <span style="background: {t['accent']}; color: black; padding: 6px 20px; border-radius: 50px; font-weight: 950; font-size: 0.9rem;">VIP LEVEL 7 👑</span>
        <span style="background: #00FF88; color: black; padding: 6px 20px; border-radius: 50px; font-weight: 950; font-size: 0.9rem;">TRUST SCORE: 98% ✅</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# لوحة المؤشرات (Merchant Dashboard Style)
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.markdown(f'<div class="dashboard-stat"><small>إجمالي الأرباح</small><br><span style="font-size:1.8rem; color:#00FF88;">$1.2M</span></div>', unsafe_allow_html=True)
with col_m2:
    st.markdown(f'<div class="dashboard-stat"><small>نقاط المكافآت</small><br><span style="font-size:1.8rem; color:{t["accent"]};">{st.session_state.discount_points:,}</span></div>', unsafe_allow_html=True)
with col_m3:
    st.markdown(f'<div class="dashboard-stat"><small>حجم الفريق</small><br><span style="font-size:1.8rem; color:#FFFFFF;">8.5K</span></div>', unsafe_allow_html=True)
with col_m4:
    st.markdown(f'<div class="dashboard-stat"><small>قوة التأثير</small><br><span style="font-size:1.8rem; color:#FF4B4B;">A+++</span></div>', unsafe_allow_html=True)

st.divider()

# تبويبات الأنظمة الاحترافية
tabs = st.tabs(["🚀 النمو والانتشار", "💎 الخزنة والولاء", "✉️ مركز المراسلات", "⚙️ مهندس الظهور (SEO)"])

# --- Tab 1: النمو والانتشار (Affiliate Center) ---
with tabs[0]:
    st.subheader("🔗 محرك التوسع العالمي (Affiliate Engine)")
    st.info("رابط الإحالة الموثق الخاص بك لبناء أجيال السيادة السبعة.")
    
    aff_code = st.session_state.user_id[:8].upper()
    aff_link = f"https://mr7-empire.com/invite?ref={aff_code}"
    
    st.code(aff_link, language="text")
    if st.button("نسخ الرابط الملكي 📋"): st.toast("تم النسخ! انطلق لبناء إمبراطوريتك.")
    
    col_gr1, col_gr2 = st.columns(2)
    with col_gr1:
        st.markdown(f"""
        <div class="feature-card">
            <h4>تحليل الجيل الأول</h4>
            <p>عدد المسجلين: <b>852 قائد</b></p>
            <p>معدل النشاط: <span style="color:#00FF88;">92%</span></p>
        </div>
        """, unsafe_allow_html=True)
    with col_gr2:
        st.markdown(f"""
        <div class="feature-card">
            <h4>عمولات الأجيال السبعة</h4>
            <p>أرباح الشهر الحالي: <b>$24,500</b></p>
            <p>توقعات النمو: <span style="color:{t['accent']};">+15%</span></p>
        </div>
        """, unsafe_allow_html=True)

# --- Tab 2: الخزنة ونظام الولاء (Loyalty Hub) ---
with tabs[1]:
    st.subheader("💎 نظام المكافآت الذكي (Points & Vouchers)")
    
    c_p1, c_p2 = st.columns([2, 1])
    with c_p1:
        st.markdown("#### 🎫 قسائم الخصم المتاحة (Vouchers)")
        st.table([
            {"القسيمة": "WELCOME_TR7", "الخصم": "15%", "الانتهاء": "30 يوم"},
            {"القسيمة": "ELITE_LEADER", "الخصم": "50$", "الانتهاء": "دائم"}
        ])
    with c_p2:
        st.markdown(f"""
        <div class="feature-card" style="text-align:center; background:rgba(0,255,136,0.05);">
            <p>رصيد الكاش باك</p>
            <h2 style="color:#00FF88;">$1,250.00</h2>
            <button style="width:100%; height:35px; background:#00FF88; border:none; border-radius:10px; font-weight:bold;">سحب الآن 💸</button>
        </div>
        """, unsafe_allow_html=True)

# --- Tab 3: مركز المراسلات (Imperial Mail) ---
with tabs[2]:
    st.subheader("📩 مركز قيادة التواصل الجماعي")
    st.write("أرسل تحديثاتك الاستراتيجية مباشرة لبريد فريقك أو للإدارة.")
    
    with st.container():
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        target_group = st.selectbox("المستهدفين:", ["الجيل الأول (Directs)", "الفريق بالكامل (8.5K)", "قادة النخبة فقط", "أدمن MR7"])
        subject = st.text_input("عنوان البرقية الاستراتيجية:", placeholder="مثلاً: خطة الربع الثاني للنمو...")
        mail_body = st.text_area("نص الرسالة:", height=150)
        
        if st.button("بث الرسالة عبر السيرفرات ⚡"):
            if mail_body:
                with st.spinner("جاري التشفير والبث عالمياً..."):
                    time.sleep(2)
                    st.success("تم إرسال الرسالة بنجاح لجميع الأطراف.")
            else: st.warning("الرسالة فارغة!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- Tab 4: SEO & GEO (Global Visibility) ---
with tabs[3]:
    st.subheader("⚙️ هندسة الظهور الرقمي")
    
    col_seo1, col_seo2 = st.columns(2)
    with col_seo1:
        st.markdown("#### 🌍 التواجد الجغرافي (GEO)")
        ops_base = st.text_input("قاعدة العمليات الأساسية:", "Dubai, UAE")
        region = st.multiselect("نطاق الظهور العالمي:", ["الشرق الأوسط", "أوروبا", "أمريكا الشمالية", "آسيا"], default=["الشرق الأوسط"])
        st.caption("تحديد النطاق يساعد في جلب قادة من نفس المناطق الجغرافية.")

    with col_seo2:
        st.markdown("#### 🔍 تحسين محركات البحث (SEO)")
        keywords = st.text_area("كلمات المفتاح الموثقة:", "Financial Mastery, Empire Builder, MR7 Mentorship")
        st.progress(0.85)
        st.caption("كفاءة أرشفة بروفايلك: 85% (ممتاز)")
        st.checkbox("تفعيل الظهور في نتائج البحث العامة (Google/Bing)", value=True)

st.divider()

# معرض أصول الإمبراطورية (Business Portfolio)
st.subheader("🖼️ معرض أصول القائد (Business Portfolio)")
assets = [
    ("https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500&q=80", "مشروع الاستثمار العقاري الذكي"),
    ("https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=500&q=80", "أكاديمية تدريب الجيل الثالث"),
    ("https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=500&q=80", "مركز تطوير حلول الـ AI")
]
asset_cols = st.columns(3)
for i, (img, title) in enumerate(assets):
    with asset_cols[i]:
        st.image(img, caption=title, use_container_width=True)

st.divider()

# روابط التنقل السريع
st.markdown("### 🗺️ خريطة السيادة السريعة")
c_nav1, c_nav2, c_nav3, c_nav4 = st.columns(4)
with c_nav1:
    if st.button("🛒 المتجر العالمي"): st.switch_page("pages/4_Marketplace.py")
with c_nav2:
    if st.button("👥 إدارة الفريق"): st.switch_page("pages/6_Teams.py")
with c_nav3:
    if st.button("💰 الخزنة"): st.switch_page("pages/3_Wallet.py")
with c_nav4:
    if st.button("🏠 الرئيسية"): st.switch_page("app.py")
