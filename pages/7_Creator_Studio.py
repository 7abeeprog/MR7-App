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
    /* الفلسفة التصميمية: إبداع ملكي بلمسة تكنولوجية */
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
        filter: drop-shadow(0 0 12px {t['accent']}); 
        font-size: 3.5rem !important; 
    }}

    .studio-card {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 25px;
        padding: 30px;
        margin-bottom: 25px;
        transition: 0.4s ease;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .studio-card:hover {{ border-color: #00FF88; transform: translateY(-5px); }}

    .rank-badge {{
        background: linear-gradient(135deg, {t['accent']}, #FFFFFF);
        color: #000 !important;
        padding: 10px 25px;
        border-radius: 50px;
        font-weight: 900;
        display: inline-block;
        margin: 10px 0;
        box-shadow: 0 0 20px {t['accent']};
    }}

    .badge-icon-box {{
        background: rgba(255,255,255,0.05);
        border: 1px solid {t['border']};
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        transition: 0.3s;
    }}
    .badge-icon-box:hover {{ border-color: #00FF88; background: rgba(0,255,136,0.05); }}

    /* حل مشكلة الكتابة بالأسود */
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

# --- 2. إدارة البيانات (State Management) ---
if 'creator_xp' not in st.session_state:
    st.session_state.creator_xp = 2450
if 'sections' not in st.session_state:
    st.session_state.sections = [{"title": "مدخل إلى السيادة الاقتصادية", "lessons": [{"title": "فهم قانون الـ 10", "yt": ""}]}]

# تحديد الرتبة بناءً على النقاط
def get_creator_level(xp):
    if xp < 1000: return "مبدع واعد 🌱", "🥉", 0.3
    if xp < 5000: return "مهندس محتوى 📚", "🥈", 0.6
    return "أسطورة المعرفة 👑", "🥇", 1.0

rank_name, rank_icon, rank_prog = get_creator_level(st.session_state.creator_xp)

# --- 3. الشريط الجانبي (أدوات المبدع) ---
with st.sidebar:
    st.markdown(f"### 🎨 استوديو التخصيص")
    theme_choice = st.selectbox("النمط البصري:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    
    st.markdown(f"### 🏆 رتبة المبدع العالمي")
    st.markdown(f"<div class='rank-badge'>{rank_icon} {rank_name}</div>", unsafe_allow_html=True)
    st.progress(rank_prog)
    st.caption(f"الخبرة الموثقة: {st.session_state.creator_xp} XP")
    
    st.divider()
    st.markdown("### 🌍 استهداف الأقاليم")
    st.multiselect("هذا المحتوى موجه لـ:", ["مصر", "ليبيا", "السودان", "عالمي"], default=["عالمي"])

# --- 4. واجهة استوديو بناء المحتوى ---
st.title("🎬 استوديو هندسة المعرفة")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.4rem; margin-top:-25px;'>حول خبرتك القيادية إلى أصول رقمية تدر أرباحاً عالمية</p>", unsafe_allow_html=True)

st.divider()

tabs = st.tabs(["🏗️ بناء المنهج", "📝 بنك الاختبارات", "📜 أوسمة الإتمام", "📊 لوحة تحكم الأرباح"])

# --- Tab 1: بناء المنهج (Course Builder) ---
with tabs[0]:
    st.subheader("🏗️ مصنع المناهج المليارية")
    
    with st.expander("⚙️ إعدادات الهوية التجارية للدورة", expanded=True):
        c_name = st.text_input("عنوان الدورة الاستراتيجي:", placeholder="مثلاً: أسرار المليار في سوق السيارات الكهربائية")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.selectbox("الفئة المستهدفة:", ["رواد الأعمال", "المستثمرين القادة", "المسوقين المحترفين"])
        with col_c2:
            st.number_input("سعر الدورة المقترح ($):", min_value=10, value=499)
        st.text_area("وصف القيمة المضافة (SEO Friendly):", placeholder="اشرح كيف ستغير هذه الدورة حياة القائد...")

    st.markdown("---")
    
    for s_idx, section in enumerate(st.session_state.sections):
        with st.container():
            st.markdown(f"<div class='studio-card' style='border-right: 6px solid {t['accent']};'>", unsafe_allow_html=True)
            section['title'] = st.text_input(f"عنوان الوحدة {s_idx + 1}:", value=section['title'], key=f"sec_{s_idx}")
            
            for l_idx, lesson in enumerate(section['lessons']):
                with st.expander(f"🎬 الدرس {l_idx + 1}: {lesson['title']}"):
                    lesson['title'] = st.text_input("اسم الدرس:", value=lesson['title'], key=f"les_t_{s_idx}_{l_idx}")
                    lesson['yt'] = st.text_input("رابط الفيديو (Vimeo/Youtube):", value=lesson['yt'], key=f"les_v_{s_idx}_{l_idx}")
                    st.file_uploader("ارفق ملفات تدريبية (PDF/Worksheets):", key=f"les_f_{s_idx}_{l_idx}")
            
            if st.button(f"➕ إضافة درس للوحدة {s_idx + 1}", key=f"add_l_{s_idx}"):
                section['lessons'].append({"title": "درس جديد", "yt": ""})
                st.session_state.creator_xp += 20
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    if st.button("➕ إضافة وحدة استراتيجية جديدة"):
        st.session_state.sections.append({"title": "وحدة جديدة", "lessons": []})
        st.session_state.creator_xp += 100
        st.rerun()

# --- Tab 2: الاختبارات (Quizzes) ---
with tabs[1]:
    st.subheader("📝 هندسة اختبارات الجدارة")
    st.info("الاختبارات هي بوابة الحصول على 'وسام القوة'. اجعلها ذكية وتطبيقية.")
    
    with st.container():
        st.markdown("<div class='studio-card'>", unsafe_allow_html=True)
        st.text_input("سؤال قياس الاستيعاب:")
        q1, q2 = st.columns(2)
        q1.text_input("الخيار أ (صحيح):")
        q2.text_input("الخيار ب (خاطئ):")
        st.selectbox("ربط السؤال بدرس معين:", ["مقدمة السيادة", "قانون الـ 10"])
        if st.button("📥 حفظ السؤال في بنك الأسئلة"):
            st.success("تم التوثيق +50 XP")
            st.session_state.creator_xp += 50
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- Tab 3: الأوسمة (Gamification & Badges) ---
with tabs[2]:
    st.subheader("📜 نظام الأوسمة والشهادات التلقائي")
    st.markdown("حدد الأوسمة التي سيحصل عليها طلابك لتحفيزهم على الإنجاز.")
    
    col_b1, col_b2, col_b3 = st.columns(3)
    badges = [
        ("🚀 المنطلق السريع", "يمنح عند إتمام أول وحدة في 24 ساعة"),
        ("🧠 العقل الذهبي", "يمنح عند تخطي الاختبار النهائي بنسبة 100%"),
        ("🏆 القائد المطبق", "يمنح عند رفع أول مشروع تطبيقي")
    ]
    
    for i, (name, desc) in enumerate(badges):
        with [col_b1, col_b2, col_b3][i]:
            st.markdown(f"""
            <div class="badge-icon-box">
                <div style="font-size: 3rem;">🏅</div>
                <h4 style="color: {t['accent']} !important; margin: 10px 0;">{name}</h4>
                <p style="font-size: 0.8rem; opacity: 0.7;">{desc}</p>
                <input type="checkbox" checked> تفعيل الوسام
            </div>
            """, unsafe_allow_html=True)

# --- Tab 4: الأرباح (Business Intelligence) ---
with tabs[3]:
    st.subheader("📊 أداء المحتوى في المتجر العالمي")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("عدد الطلاب المسجلين", "1,248", "+15% هذا الشهر")
    m2.metric("إجمالي العوائد المحققة", "$45,200", "صافي")
    m3.metric("تقييم الجودة العالمي", "4.9/5", "⭐")
    
    st.divider()
    st.markdown("### 🗺️ التوزيع الجغرافي لطلابك")
    st.write("مصر: 55% | ليبيا: 15% | السودان: 10% | أخرى: 20%")
    st.progress(0.55)

st.divider()

# زر النشر النهائي
if st.button("🚀 إطلاق الدورة في المتجر العالمي"):
    with st.spinner("جاري تدقيق المنهج وبرمجته في خوارزميات المتجر..."):
        time.sleep(2.5)
        st.balloons()
        st.success("تم النشر بنجاح! دورتك الآن متاحة لـ 1.2 مليون قائد حول العالم.")

# خريطة الانتقال
st.markdown("### 🗺️ خريطة السيادة السريعة")
cb1, cb2 = st.columns(2)
with cb1:
    if st.button("🛒 معاينة الدورة في المتجر"): st.switch_page("pages/4_Marketplace.py")
with cb2:
    if st.button("🏠 العودة للرئيسية"): st.switch_page("app.py")
