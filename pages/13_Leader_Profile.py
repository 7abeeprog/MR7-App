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

    /* تصميم بطاقة البروفايل العلوية */
    .profile-header {{
        background: linear-gradient(180deg, rgba(255, 215, 0, 0.1) 0%, {t['card']} 100%);
        border: 2px solid {t['accent']};
        border-radius: 40px;
        padding: 40px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }}

    .avatar-glow {{
        width: 180px;
        height: 180px;
        border-radius: 50%;
        border: 4px solid {t['accent']};
        box-shadow: 0 0 30px {t['accent']};
        margin-bottom: 20px;
        object-fit: cover;
    }}

    .stat-box {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid {t['border']};
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        transition: 0.3s;
    }}
    .stat-box:hover {{ transform: translateY(-5px); border-color: #00FF88; }}

    .badge-wall {{
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
        margin-top: 20px;
    }}
    .mini-badge {{
        background: {t['accent']};
        color: black !important;
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 900;
    }}

    /* حل مشكلة الكتابة باللون الأسود */
    .stTextInput input {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: bold !important;
    }}
    
    /* تنسيق زر رفع الملفات */
    section[data-testid="stFileUploadDropzone"] {{
        background: rgba(255,255,255,0.05);
        border: 2px dashed {t['accent']};
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة بيانات القائد (Leader Identity) ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'leader_name' not in st.session_state:
    st.session_state.leader_name = "القائد المجهول"
if 'user_rank' not in st.session_state:
    st.session_state.user_rank = "قائد ناشئ 🌱"
if 'profile_pic_base64' not in st.session_state:
    st.session_state.profile_pic_base64 = None

# --- 3. القائمة الجانبية (الإعدادات) ---
with st.sidebar:
    st.markdown(f"### 🎨 تخصيص المظهر")
    theme_choice = st.selectbox("النمط الحالي:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    
    st.markdown("### ⚙️ إعدادات الهوية")
    st.session_state.leader_name = st.text_input("اسم الشهرة القيادي:", st.session_state.leader_name)
    
    # ميزة رفع الصورة الشخصية
    uploaded_file = st.file_uploader("رفع صورة البروفايل:", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # تحويل الصورة إلى Base64 لعرضها في الـ HTML
        bytes_data = uploaded_file.getvalue()
        base64_img = base64.b64encode(bytes_data).decode()
        st.session_state.profile_pic_base64 = f"data:image/png;base64,{base64_img}"
        st.success("تم تجهيز الصورة!")

    if st.button("💾 حفظ البيانات"):
        st.success("تم تحديث السجل الإمبراطوري بنجاح ✅")
        time.sleep(1)
        st.rerun()

# --- 4. واجهة ملف القائد ---
st.title("👤 الملف الشخصي للقائد")

# اختيار مصدر الصورة (المرفوعة أو الافتراضية)
display_avatar = st.session_state.profile_pic_base64 if st.session_state.profile_pic_base64 else f"https://api.dicebear.com/7.x/avataaars/svg?seed={st.session_state.user_id}"

# القسم العلوي: الهوية والبصمة
st.markdown(f"""
<div class="profile-header">
    <img src="{display_avatar}" class="avatar-glow">
    <h2 style="color: {t['accent']}; font-size: 2.5rem; margin-bottom: 5px;">{st.session_state.leader_name}</h2>
    <p style="font-size: 1.2rem; opacity: 0.8;">معرف القائد الفريد: <code>{st.session_state.user_id[:13]}</code></p>
    <div class="badge-wall">
        <span class="mini-badge">💎 {st.session_state.user_rank}</span>
        <span class="mini-badge" style="background: #00FF88;">✅ موثق</span>
        <span class="mini-badge" style="background: #FFFFFF;">🚀 عضو مؤسس</span>
    </div>
</div>
""", unsafe_allow_html=True)

# القسم الثاني: إحصائيات السيادة
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-box">
        <p style="color: #888; font-size: 0.8rem;">رصيد الثروة</p>
        <h3 style="color: #00FF88;">$1.2M</h3>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-box">
        <p style="color: #888; font-size: 0.8rem;">جيش القادة</p>
        <h3 style="color: {t['accent']};">1,248</h3>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-box">
        <p style="color: #888; font-size: 0.8rem;">نقاط الخبرة XP</p>
        <h3 style="color: #FFFFFF;">4,520</h3>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-box">
        <p style="color: #888; font-size: 0.8rem;">مستوى التأثير</p>
        <h3 style="color: #FF4B4B;">9.8/10</h3>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# الأقسام التفصيلية
tab_vision, tab_achievements, tab_social = st.tabs(["🏛️ الرؤية الاستراتيجية", "🏆 جدار الأوسمة", "💬 السجل التفاعلي"])

with tab_vision:
    st.subheader("🏛️ ميثاق الرؤية الشخصي")
    st.markdown(f"""
    <div style="background: rgba(255, 215, 0, 0.05); border-right: 4px solid {t['accent']}; padding: 25px; border-radius: 15px;">
        <h4 style="color: {t['accent']};">الهدف الكوني المختار:</h4>
        <p style="font-size: 1.5rem; font-weight: 800;">"تأمين سيادة مالية بقيمة 100 مليون دولار وقيادة جيل من القادة الأحرار"</p>
        <hr style="border-color: rgba(255,255,255,0.1);">
        <p style="color: #888;">تاريخ التوثيق: 11 أبريل 2026</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 تعديل ميثاق الرؤية"):
        st.switch_page("pages/0_My_Vision.py")

with tab_achievements:
    st.subheader("🏆 الإنجازات المحققة في المنظومة")
    cols = st.columns(3)
    badges = [
        ("🥇 باني الإمبراطورية", "إتمام أول 1000 عضو في الفريق"),
        ("🧠 العقل الذهبي", "اجتياز اختبارات عقلية المليار بنسبة 100%"),
        ("💰 المحرك المالي", "تحقيق أول مليون دولار تدفق نقدي")
    ]
    for i, (b_name, b_desc) in enumerate(badges):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; border: 1px solid {t['border']}; border-radius: 15px; background: {t['card']};">
                <div style="font-size: 40px;">🏅</div>
                <h5 style="color: {t['accent']};">{b_name}</h5>
                <p style="font-size: 0.8rem; color: #888;">{b_desc}</p>
            </div>
            """, unsafe_allow_html=True)

with tab_social:
    st.subheader("💬 آخر ما بثت رؤيتك في الساحة")
    st.info("هنا تظهر منشوراتك التي شاركتها مع المجتمع العالمي.")
    st.markdown("""
    <div style="background: rgba(255,255,255,0.03); padding: 15px; border-radius: 10px; margin-bottom: 10px;">
        <p style="font-weight: bold; margin-bottom: 5px;">"السيادة لا تمنح، بل تنتزع بقوة الرؤية واتساع الفريق."</p>
        <small style="color: #666;">منذ ساعتين • 24 تأييد 👍</small>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🌐 الانتقال للساحة العالمية"):
        st.switch_page("pages/12_Social_Network.py")

st.divider()

# أزرار الانتقال السريع
st.markdown("### 🚀 روابط السيادة السريعة")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("💰 الخزنة"): st.switch_page("pages/3_Wallet.py")
with c2:
    if st.button("👥 الفريق"): st.switch_page("pages/6_Teams.py")
with c3:
    if st.button("🔔 التنبيهات"): st.switch_page("pages/10_Notifications.py")
