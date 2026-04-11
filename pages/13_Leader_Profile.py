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
    /* الفلسفة التصميمية الاحترافية */
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

    /* غلاف البروفايل (Cover Photo) */
    .profile-cover {{
        height: 250px;
        background: url('https://images.unsplash.com/photo-1579546929518-9e396f3cc809?auto=format&fit=crop&q=80&w=2070') center/cover;
        border-radius: 40px 40px 0 0;
        border: 2px solid {t['accent']};
        border-bottom: none;
    }}

    .elite-header {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 0 0 50px 50px;
        padding: 0 50px 50px 50px;
        text-align: center;
        margin-top: -80px;
        position: relative;
        box-shadow: 0 25px 60px rgba(0,0,0,0.8);
    }}

    .avatar-glow {{
        width: 180px;
        height: 180px;
        border-radius: 50%;
        border: 5px solid {t['accent']};
        box-shadow: 0 0 40px {t['accent']};
        margin-bottom: 20px;
        background: {t['bg']};
        object-fit: cover;
    }}

    /* بطاقات الميزات الجديدة */
    .feature-card {{
        background: rgba(255,255,255,0.03);
        border: 1px solid {t['accent']};
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
    }}

    /* حل مشكلة الكتابة باللون الأسود */
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: bold !important;
        border-radius: 12px !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 20px !important;
        height: 55px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات والهوية ---
if 'user_id' not in st.session_state: st.session_state.user_id = str(uuid.uuid4())
if 'leader_name' not in st.session_state: st.session_state.leader_name = "إمبراطور النخبة"
if 'discount_points' not in st.session_state: st.session_state.discount_points = 2450
if 'reward_balance' not in st.session_state: st.session_state.reward_balance = 125.50

# --- 3. القائمة الجانبية (تخصيص متقدم) ---
with st.sidebar:
    st.markdown(f"### 🎨 تخصيص المنظومة")
    theme_choice = st.selectbox("النمط:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    
    with st.expander("🌐 إعدادات SEO و GEO"):
        st.text_input("موقع قاعدة العمليات (City/Country):", "Cairo, Egypt")
        st.text_area("الكلمات المفتاحية للبحث (SEO Keywords):", "Leadership, Wealth Engineering, MR7 Mentor")
        st.caption("هذه الإعدادات تساعد في أرشفة بروفايلك عالمياً.")

# --- 4. واجهة ملف القائد الاحترافية ---
# غلاف احترافي
st.markdown('<div class="profile-cover"></div>', unsafe_allow_html=True)

# رأس البروفايل
avatar_url = f"https://api.dicebear.com/7.x/avataaars/svg?seed={st.session_state.user_id}"
st.markdown(f"""
<div class="elite-header">
    <img src="{avatar_url}" class="avatar-glow">
    <h2 style="color: {t['accent']}; font-size: 2.8rem; margin-bottom: 5px;">{st.session_state.leader_name}</h2>
    <p style="font-size: 1.1rem; opacity: 0.8; font-family: monospace;">قائد عمليات معتمد: {st.session_state.user_id[:13]}</p>
    <div style="display: flex; justify-content: center; gap: 15px; margin-top: 15px;">
        <span style="background: {t['accent']}; color: black; padding: 4px 15px; border-radius: 50px; font-weight: 900;">الرتبة: ماسي 💎</span>
        <span style="background: #00FF88; color: black; padding: 4px 15px; border-radius: 50px; font-weight: 900;">نقاط الخصم: {st.session_state.discount_points} 🎟️</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# تبويبات الوظائف المتقدمة
tabs = st.tabs(["🔗 الانتشار والنمو", "💰 المحفظة والمكافآت", "📩 بريد القادة", "🛠️ إدارة الظهور (SEO)"])

# --- Tab 1: رابط الإحالة والانتشار ---
with tabs[0]:
    st.subheader("🔗 مركز الانتشار العالمي (Affiliate Hub)")
    st.markdown("""
    استخدم الرابط أدناه لبناء جيشك الخاص. كل مسجل عن طريقك يضاف لجيلك الأول وتكسب نقاط استحقاق ومكافآت تضاعفية.
    """)
    aff_link = f"https://mr7-empire.com/join?ref={st.session_state.user_id[:8]}"
    st.code(aff_link, language="text")
    if st.button("نسخ الرابط ونشره في الساحة 🚀"):
        st.toast("تم نسخ الرابط! انطلق لغزو الأسواق.")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown(f"""
        <div class="feature-card">
            <h4>إجمالي المحالين</h4>
            <div style="font-size: 2rem; color: {t['accent']};">852 قائد</div>
        </div>
        """, unsafe_allow_html=True)
    with col_p2:
        st.markdown(f"""
        <div class="feature-card">
            <h4>عمولات الجيل المباشر</h4>
            <div style="font-size: 2rem; color: #00FF88;">$12,450</div>
        </div>
        """, unsafe_allow_html=True)

# --- Tab 2: المحفظة ونقاط الخصم ---
with tabs[1]:
    st.subheader("💰 نظام الولاء والمكافآت (AliBaba Style)")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.metric("نقاط الخصم (Store Credit)", f"{st.session_state.discount_points} PTS", "+150 اليوم")
    with c2:
        st.metric("رصيد المكافآت المباشرة", f"${st.session_balance if 'session_balance' in st.session_state else 125.50}", "متاح للسحب")
    with c3:
        st.metric("قسائم الشراء (Vouchers)", "3 قسائم", "خصم 20%")

    st.markdown("### 🏆 قائمة المكافآت المحققة")
    st.table([
        {"المكافأة": "بونص بناء الفريق (الجيل الثاني)", "المبلغ": "$50.00", "التاريخ": "اليوم"},
        {"المكافأة": "نقاط ولاء - إتمام كورس المليار", "المبلغ": "500 PTS", "التاريخ": "أمس"},
        {"المكافأة": "خصم ترويجي للمتجر", "المبلغ": "قسيمة $10", "التاريخ": "منذ يومين"}
    ])

# --- Tab 3: البريد الإمبراطوري ---
with tabs[2]:
    st.subheader("📩 مركز المراسلات الاستراتيجية")
    st.info("أرسل تعليماتك مباشرة لأعضاء فريقك أو تواصل مع الدعم الفني العالمي.")
    
    with st.container():
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        to_who = st.selectbox("إلى:", ["الفريق بالكامل (Bulk Email)", "قادة الجيل الأول فقط", "الإدارة العليا (MR7 Admin)"])
        subject = st.text_input("موضوع البرقية:")
        body = st.text_area("نص الرسالة القيادية:", height=150)
        if st.button("إرسال البريد الآن ⚡"):
            if body:
                with st.spinner("جاري بث الرسالة عبر السيرفرات العالمية..."):
                    time.sleep(2)
                    st.success("تم إرسال البرقية بنجاح لكافة المستهدفين!")
            else:
                st.warning("الرسالة فارغة!")
        st.markdown("</div>", unsafe_allow_html=True)

# --- Tab 4: SEO و GEO ---
with tabs[3]:
    st.subheader("🛠️ هندسة الظهور العالمي")
    col_seo1, col_seo2 = st.columns([1, 1])
    
    with col_seo1:
        st.markdown("#### 🌍 التواجد الجغرافي (GEO)")
        st.write("يظهر بروفايلك حالياً في نطاق:")
        st.info("الشرق الأوسط، شمال أفريقيا، والخليج العربي")
        if st.button("توسيع النطاق لأوروبا"):
            st.toast("تحتاج لـ 5000 XP لتوسيع نطاق ظهورك!")

    with col_seo2:
        st.markdown("#### 🔍 تحسين البحث (SEO)")
        st.write("ترتيب بروفايلك في نتائج البحث الداخلية:")
        st.progress(0.75)
        st.caption("قوة الظهور: 75% (ممتاز)")
        st.checkbox("السماح لمحركات البحث (Google/Bing) بأرشفة بروفايلي", value=True)

st.divider()

# معرض صور المشاريع (Visual Grid)
st.subheader("🖼️ معرض أصول الإمبراطورية")
img_cols = st.columns(3)
empire_assets = [
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500&q=80",
    "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=500&q=80",
    "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?w=500&q=80"
]
for i, img in enumerate(empire_assets):
    with img_cols[i]:
        st.image(img, caption=f"مشروع سيادة #{i+1}", use_container_width=True)

# روابط سريعة
st.divider()
c_b1, c_b2, c_b3 = st.columns(3)
with c_b1:
    if st.button("🛒 المتجر العالمي"): st.switch_page("pages/4_Marketplace.py")
with c_b2:
    if st.button("👥 إدارة الفريق"): st.switch_page("pages/6_Teams.py")
with c_b3:
    if st.button("🏛️ العودة للرؤية"): st.switch_page("pages/0_My_Vision.py")
