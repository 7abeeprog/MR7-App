import streamlit as st
import time
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

    .project-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 25px;
        padding: 25px;
        margin-bottom: 25px;
        transition: 0.4s ease;
        position: relative;
        overflow: hidden;
    }}
    .project-card:hover {{ border-color: #00FF88; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,255,136,0.2); }}

    .country-tag {{
        position: absolute;
        top: 15px;
        left: 15px;
        background: rgba(0,0,0,0.6);
        color: white;
        padding: 5px 12px;
        border-radius: 10px;
        font-size: 0.8rem;
        border: 1px solid {t['accent']};
    }}

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
        border-radius: 15px !important;
        height: 55px;
    }}

    .stProgress > div > div > div > div {{
        background-color: #00FF88 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة البيانات الاستراتيجية ---
if 'crowd_projects' not in st.session_state:
    st.session_state.crowd_projects = [
        {
            "title": "مدينة النبت الذكية (Nabt Smart City)", 
            "category": "مدن مستدامة", 
            "country": "مصر / عالمي",
            "owner": "منظومة MR7", 
            "goal": 2000000000, 
            "raised": 150000000, 
            "desc": "نموذج بملياري دولار للحياة المستدامة، مع خطط لتكراره 100 مرة عالمياً. يشمل مزارع متخصصة، مراكز أبحاث، ومناطق سكنية ذكية.", 
            "status": "approved"
        },
        {
            "title": "مدينة السيارات الكهربائية (EV City)", 
            "category": "تصنيع ثقيل", 
            "country": "مصر",
            "owner": "التحالف الصناعي MR7", 
            "goal": 3600000000, 
            "raised": 500000000, 
            "desc": "استثمار بقيمة 3.6 مليار دولار لبناء 600 مصنع، لإعادة صياغة القيادة الصناعية في المنطقة وتوطين تكنولوجيا النقل الذكي.", 
            "status": "approved"
        },
        {
            "title": "مبادرة الـ 20,000 مشروع صغرى", 
            "category": "ريادة أعمال مجتمعية", 
            "country": "ليبيا / السودان",
            "owner": "مؤسسة قادة الغد", 
            "goal": 700000000, 
            "raised": 85000000, 
            "desc": "محفز بقيمة 700 مليون دولار لدعم رواد الأعمال في القاعدة الشعبية عبر ليبيا والسودان، وخلق فرص عمل لآلاف الشباب.", 
            "status": "approved"
        }
    ]

if 'notifications' not in st.session_state:
    st.session_state.notifications = []

def add_notification(msg, icon="💰"):
    st.session_state.notifications.insert(0, {"msg": msg, "time": datetime.now().strftime("%Y-%m-%d %H:%M"), "icon": icon})

# --- 3. الشريط الجانبي (فلترة الدول) ---
with st.sidebar:
    st.markdown(f"### 🎨 تخصيص المظهر")
    theme_choice = st.selectbox("النمط الحالي:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    
    st.markdown("### 🌍 نطاق العمليات")
    country_filter = st.multiselect(
        "فلترة حسب الدولة:", 
        ["مصر", "ليبيا", "السودان", "عالمي"],
        default=["مصر", "ليبيا", "السودان", "عالمي"]
    )
    
    st.divider()
    st.markdown("### 🏛️ رصيد الاستثمار")
    st.success("المحفظة الاستثمارية: 50,000 $")

# --- 4. واجهة مجمع التمويل الجماعي ---
st.title("🤝 مجمع التمويل الملياري")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.3rem; margin-top:-20px;'>نظام تمويل المشاريع السيادية والاقتصاد التشاركي العالمي</p>", unsafe_allow_html=True)

st.divider()

tabs = st.tabs(["🌎 استكشاف المشاريع الإمبراطورية", "🚀 طرح مشروع سيادي", "💰 محفظتي الاستثمارية", "📊 إحصائيات النمو"])

# --- Tab 1: استكشاف المشاريع ---
with tabs[0]:
    st.subheader("🌎 منصة المشاريع الكبرى")
    
    # فلترة المشاريع بناءً على الدول المختارة
    display_projects = [
        p for p in st.session_state.crowd_projects 
        if any(country in p['country'] for country in country_filter) and p.get('status') == "approved"
    ]
    
    if not display_projects:
        st.info("لا توجد مشاريع تطابق نطاق البحث الجغرافي حالياً.")
    else:
        for idx, proj in enumerate(display_projects):
            with st.container():
                st.markdown(f"""
                <div class="project-card">
                    <div class="country-tag">📍 {proj['country']}</div>
                    <div style="margin-top: 25px;">
                        <span style="color: {t['accent']}; font-size: 0.9rem; font-weight: 900;">{proj['category']}</span>
                        <h2 style="color: {t['accent']}; margin: 5px 0;">{proj['title']}</h2>
                        <p style="color: #888; font-size: 0.9rem;">بواسطة: {proj['owner']}</p>
                    </div>
                    <p style="color: #ddd; line-height: 1.6; margin: 15px 0;">{proj['desc']}</p>
                    
                    <div style="background: rgba(255,255,255,0.03); padding: 15px; border-radius: 15px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <span>الهدف المالي: <b>${proj['goal']:,.0f}</b></span>
                            <span style="color: #00FF88;">تم جمع: <b>${proj['raised']:,.0f}</b></span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                progress = min(proj['raised'] / proj['goal'], 1.0)
                st.progress(progress)
                
                col_amt, col_btn = st.columns([2, 1])
                with col_amt:
                    fund_val = st.number_input("مبلغ الضخ المالي ($):", min_value=10, key=f"fund_{idx}", step=100)
                with col_btn:
                    st.write("") # تباعد
                    if st.button("🤝 ضخ استثماري", key=f"btn_fund_{idx}"):
                        for original in st.session_state.crowd_projects:
                            if original['title'] == proj['title']:
                                original['raised'] += fund_val
                                add_notification(f"تم ضخ {fund_val:,} $ في مشروع '{proj['title']}'", "⚡")
                        st.success(f"تمت المساهمة بنجاح! أنت الآن شريك في بناء '{proj['title']}'")
                        time.sleep(1)
                        st.rerun()

# --- Tab 2: طرح مشروعك ---
with tabs[1]:
    st.subheader("🚀 طرح رؤية اقتصادية للمراجعة")
    st.warning("تحذير: المشاريع المليارية تتطلب دراسة جدوى موثقة من مكتب MR7 الاستشاري.")
    
    with st.form("strategic_pitch_form"):
        p_name = st.text_input("اسم المشروع الاستراتيجي:")
        p_loc = st.selectbox("الدولة الرئيسية للعمليات:", ["مصر", "ليبيا", "السودان", "الجزائر", "عالمي"])
        p_goal = st.number_input("الميزانية المطلوبة للتأسيس ($):", min_value=1000)
        p_desc = st.text_area("وصف الرؤية والناتج القومي المتوقع:", height=150)
        
        if st.form_submit_button("إرسال للتدقيق الإمبراطوري 📤"):
            if p_name and p_desc:
                st.session_state.crowd_projects.append({
                    "title": p_name, "category": "مشروع ناشئ", "country": p_loc,
                    "owner": "أنت (قائد)", "goal": p_goal, "raised": 0,
                    "desc": p_desc, "status": "pending"
                })
                st.success("تم إرسال مشروعك بنجاح. ستصلك النتيجة عبر مركز التنبيهات قريباً.")
                add_notification(f"مشروعك الجديد '{p_name}' قيد التدقيق الآن.", "⏳")
            else:
                st.error("يرجى إكمال البيانات الأساسية.")

# --- Tab 3: محفظتي ---
with tabs[2]:
    st.subheader("💰 سجل الأصول والمساهمات")
    # محاكاة لأصول القائد
    my_assets = [
        {"المشروع": "مدينة السيارات الكهربائية", "المساهمة": "$5,000", "الحصة المتوقعة": "0.00014%", "الحالة": "نشط ✅"},
        {"المشروع": "مشاريع صغرى ليبيا", "المساهمة": "$1,000", "الحصة المتوقعة": "0.00014%", "الحالة": "نشط ✅"}
    ]
    st.table(my_assets)

# --- Tab 4: إحصائيات السوق ---
with tabs[3]:
    st.subheader("📊 أداء المحرك المالي العام")
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي الضخ العالمي", "$6.1B", "+12% سنوي")
    c2.metric("معدل نجاح المشاريع", "94%", "فائق")
    c3.metric("المستثمرون القادة", "1.2M", "🚀")
    
    st.markdown("### 🗺️ التوزيع الجغرافي للسيولة")
    st.write("مصر: 45% | ليبيا: 20% | السودان: 15% | أخرى: 20%")
    st.progress(0.45) # تمثيل لمصر

st.divider()

if st.button("👑 الانتقال للوحة التحكم العليا (Admin)"):
    st.switch_page("pages/8_Admin_Panel.py")
