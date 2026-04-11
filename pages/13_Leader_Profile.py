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
    /* الفلسفة التصميمية الجديدة: عمق بصري وتفاعل فائق */
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

    /* بطاقة الهوية الملكية (Elite Header) */
    .elite-header {{
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.15) 0%, rgba(0,0,0,0.8) 100%);
        border: 2px solid {t['accent']};
        border-radius: 50px;
        padding: 50px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 25px 60px rgba(0,0,0,0.8);
    }}
    
    .elite-header::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,215,0,0.05) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }}

    @keyframes rotate {{ 100% {{ transform: rotate(360deg); }} }}

    .avatar-glow {{
        width: 200px;
        height: 200px;
        border-radius: 50%;
        border: 5px solid {t['accent']};
        box-shadow: 0 0 40px {t['accent']};
        margin-bottom: 25px;
        object-fit: cover;
        position: relative;
        z-index: 2;
    }}

    /* نظام الأوسمة المتقدم */
    .achievement-hub {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 20px;
        margin-top: 30px;
    }}

    .badge-card {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        transition: 0.4s;
    }}
    .badge-card:hover {{
        background: rgba(255, 215, 0, 0.1);
        border-color: {t['accent']};
        transform: translateY(-10px);
    }}

    /* إحصائيات الأداء (Global Standards) */
    .stat-metric {{
        background: {t['card']};
        border-left: 5px solid {t['accent']};
        border-radius: 15px;
        padding: 25px;
        text-align: right;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }}

    /* حل مشكلة الكتابة باللون الأسود */
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
        font-size: 1.2rem;
        transition: 0.3s;
    }}
    .stButton>button:hover {{ transform: scale(1.05); filter: brightness(1.2); }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة الهوية (Expanded Logic) ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'leader_name' not in st.session_state:
    st.session_state.leader_name = "إمبراطور المستقبل"
if 'user_rank' not in st.session_state:
    st.session_state.user_rank = "قائد استراتيجي 💎"
if 'profile_pic' not in st.session_state:
    st.session_state.profile_pic = None

# --- 3. القائمة الجانبية المتقدمة ---
with st.sidebar:
    st.markdown(f"### 🎨 النمط الإمبراطوري")
    theme_choice = st.selectbox("اختر الجو العام:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    
    with st.expander("🛠️ تخصيص الهوية الرسمية"):
        st.session_state.leader_name = st.text_input("اسم الشهرة في المنظومة:", st.session_state.leader_name)
        up_file = st.file_uploader("رفع ختم الصورة الشخصية:", type=["jpg", "png"])
        if up_file:
            b_data = up_file.getvalue()
            b64 = base64.b64encode(b_data).decode()
            st.session_state.profile_pic = f"data:image/png;base64,{b64}"
        
        if st.button("تثبيت التعديلات"):
            st.toast("تم تحديث السجلات العالمية!")

# --- 4. واجهة ملف القائد (The Masterpiece) ---
st.title("👤 مركز قيادة القائد")

# القسم العلوي: الهوية والبصمة (Elite Experience)
avatar = st.session_state.profile_pic or f"https://api.dicebear.com/7.x/avataaars/svg?seed={st.session_state.user_id}"

st.markdown(f"""
<div class="elite-header">
    <img src="{avatar}" class="avatar-glow">
    <h2 style="color: {t['accent']}; font-size: 3rem; margin-bottom: 10px;">{st.session_state.leader_name}</h2>
    <div style="display: flex; justify-content: center; gap: 15px; margin-bottom: 20px;">
        <span style="background: {t['accent']}; color: black; padding: 5px 20px; border-radius: 50px; font-weight: 900;">{st.session_state.user_rank}</span>
        <span style="background: #00FF88; color: black; padding: 5px 20px; border-radius: 50px; font-weight: 900;">مستوى السيادة: 12</span>
    </div>
    <p style="opacity: 0.7; font-family: monospace;">UUID: {st.session_state.user_id}</p>
</div>
""", unsafe_allow_html=True)

# القسم الثاني: لوحة بيانات القائد (Dashboard Metrics)
st.subheader("📈 مؤشرات السيادة اللحظية")
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""<div class="stat-metric"><small>صافي الثروة</small><br><span style="font-size:1.8rem; color:#00FF88;">$1.24M</span></div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""<div class="stat-metric"><small>عدد القادة</small><br><span style="font-size:1.8rem; color:{t['accent']};">852</span></div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""<div class="stat-metric"><small>تأثير المحتوى</small><br><span style="font-size:1.8rem;">94%</span></div>""", unsafe_allow_html=True)
with m4:
    st.markdown(f"""<div class="stat-metric"><small>رتبة العالم</small><br><span style="font-size:1.8rem; color:#FF4B4B;">#42</span></div>""", unsafe_allow_html=True)

st.divider()

# التبويبات الموسعة (Path 2: Expanding Functions)
tabs = st.tabs(["🏛️ ميثاق الرؤية", "🏆 خزنة الأوسمة", "📊 تحليل الفريق", "🤝 التحالفات والدعم"])

with tabs[0]:
    st.markdown(f"""
    <div style="background: {t['card']}; padding: 30px; border-radius: 30px; border: 2px solid {t['accent']};">
        <h3 style="color: {t['accent']};">بوصلة التريليون الموثقة</h3>
        <p style="font-size: 1.4rem; line-height: 1.8;">"أقسمت أن أقود فريقاً من 10,000 قائد نحو الحرية المالية المطلقة، وبناء نظام تعليمي يغير وجه المنطقة العربية تجارياً."</p>
        <hr style="opacity:0.2;">
        <div style="display: flex; justify-content: space-between;">
            <span>حالة الرؤية: <b>نشطة ✅</b></span>
            <span>تاريخ الانعقاد: <b>2026-04-11</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tabs[1]:
    st.subheader("🏅 جدار الاستحقاق العالمي")
    st.markdown('<div class="achievement-hub">', unsafe_allow_html=True)
    badges = [
        ("🥇 المؤسس الأول", "تم إطلاق أول مشروع تمويل جماعي", "icon"),
        ("🧠 مهندس العقول", "إتمام 50 ساعة تدريبية معتمدة", "icon"),
        ("🌍 عابر الحدود", "بناء فريق في 3 قارات مختلفة", "icon"),
        ("💎 نادي المليون", "تحقيق أول مليون دولار في المحفظة", "icon"),
        ("⚡ القائد الفذ", "الحصول على 1000 تأييد في الساحة", "icon"),
        ("👑 الرؤية الكونية", "توثيق ميثاق الرؤية الثلاثي", "icon")
    ]
    for name, desc, _ in badges:
        st.markdown(f"""
        <div class="badge-card">
            <div style="font-size: 3rem; margin-bottom: 10px;">🛡️</div>
            <h4 style="color: {t['accent']}; margin: 0;">{name}</h4>
            <p style="font-size: 0.8rem; opacity: 0.7;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]:
    st.subheader("📊 الهيكل التنظيمي وتحليل الأداء")
    st.info("هذا القسم يتم سحب بياناته مباشرة من 'شجرة التضاعف العشري' لتقديم تحليل ذكاء أعمال (BI) متقدم.")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("✅ نمو الجيل الأول: +15% هذا الشهر")
        st.progress(0.85)
    with col_b:
        st.write("✅ كفاءة التحويل: 22%")
        st.progress(0.65)
    
    st.markdown(f"""
    <div style="margin-top: 20px; padding: 20px; border-radius: 20px; background: rgba(0,255,136,0.05); border: 1px solid #00FF88;">
        <p style="color: #00FF88; margin: 0;">🚀 تنبيه ذكي: فريق القائد 'أحمد' يحتاج لدعم تدريبي لرفع مبيعات الجيل الثالث.</p>
    </div>
    """, unsafe_allow_html=True)

with tabs[3]:
    st.subheader("🤝 تواصل مع مستشارك الخاص")
    st.text_area("أرسل طلباً استراتيجياً مباشراً للإدارة أو لمستشارك الذكي:", placeholder="اكتب هنا...")
    st.button("إرسال البرقية القيادية ⚡")

st.divider()

# روابط سريعة (Global Navigation)
st.markdown("### 🗺️ خريطة السيادة السريعة")
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("💰 الخزنة المالية"): st.switch_page("pages/3_Wallet.py")
with c2:
    if st.button("👥 جيش القادة"): st.switch_page("pages/6_Teams.py")
with c3:
    if st.button("🛒 المتجر العالمي"): st.switch_page("pages/4_Marketplace.py")
with c4:
    if st.button("🌐 الساحة العامة"): st.switch_page("pages/12_Social_Network.py")
