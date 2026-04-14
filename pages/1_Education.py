import streamlit as st
import time

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="MR7 Education Academy", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. محرك الأنماط الشامل (Theme Engine) ---
if 'app_theme' not in st.session_state:
    st.session_state.app_theme = "غامق إمبراطوري 🖤"

themes = {
    "غامق إمبراطوري 🖤": {
        "bg": "#000000", "sidebar": "#050505", "text": "#FFFFFF", 
        "accent": "#FFD700", "card": "rgba(20, 20, 20, 0.9)", "border": "#FFD700"
    },
    "فاتح ملكي ✨": {
        "bg": "#F5F5F5", "sidebar": "#FFFFFF", "text": "#1A1A1A", 
        "accent": "#B8860B", "card": "rgba(255, 255, 255, 0.95)", "border": "#B8860B"
    },
    "أزرق القيادة 💙": {
        "bg": "#001F3F", "sidebar": "#001529", "text": "#FFFFFF", 
        "accent": "#0074D9", "card": "rgba(0, 31, 63, 0.8)", "border": "#0074D9"
    },
    "أخضر الاستدامة 💚": {
        "bg": "#002B1B", "sidebar": "#001A10", "text": "#FFFFFF", 
        "accent": "#00FF88", "card": "rgba(0, 43, 27, 0.8)", "border": "#00FF88"
    }
}
t = themes[st.session_state.app_theme]

# --- 3. الهندسة البصرية المتقدمة (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
    
    .stApp {{ background-color: {t['bg']} !important; color: {t['text']} !important; font-family: 'Tajawal', sans-serif; }}
    [data-testid="stSidebar"] {{ background-color: {t['sidebar']} !important; border-right: 2px solid {t['accent']} !important; }}
    
    .header-title {{
        background: linear-gradient(90deg, {t['accent']}, #FFF, {t['accent']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 3.5rem;
        text-align: center;
        filter: drop-shadow(0 0 10px {t['accent']});
        margin-bottom: 0;
    }}
    .header-sub {{ text-align: center; color: #888; font-weight: 700; font-size: 1.2rem; margin-top: -10px; margin-bottom: 40px; letter-spacing: 2px; uppercase; }}

    .glass-card {{
        background: {t['card']};
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 25px;
        padding: 20px;
        text-align: right;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: 0.3s;
        margin-bottom: 20px;
        direction: rtl;
    }}
    .glass-card:hover {{ border-color: {t['accent']}; transform: translateY(-8px); box-shadow: 0 15px 40px rgba(255,215,0,0.1); }}
    
    .img-container {{ width: 100%; height: 200px; border-radius: 15px; overflow: hidden; margin-bottom: 15px; position: relative; }}
    .img-container img {{ width: 100%; height: 100%; object-fit: cover; transition: 0.7s; }}
    .glass-card:hover .img-container img {{ transform: scale(1.1); }}
    
    .badge {{ background: rgba(255,215,0,0.1); color: {t['accent']}; padding: 5px 12px; border-radius: 8px; font-size: 11px; font-weight: 900; border: 1px solid rgba(255,215,0,0.3); }}
    .price-tag {{ color: #00FF88; font-size: 26px; font-weight: 900; }}
    
    .stButton > button {{
        width: 100%;
        border-radius: 15px !important;
        height: 55px;
        font-weight: 900 !important;
        font-size: 16px !important;
        background: linear-gradient(135deg, {t['accent']}, #FF8C00) !important;
        color: black !important;
        border: none !important;
        transition: 0.3s !important;
    }}
    .stButton > button:hover {{ transform: scale(1.03); box-shadow: 0 0 20px {t['accent']}; }}
    
    /* تصميم زر التشفير (مغلق) */
    .btn-locked > button {{ background: transparent !important; border: 2px solid {t['accent']} !important; color: {t['accent']} !important; }}
    .btn-locked > button:hover {{ background: {t['accent']} !important; color: black !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. إدارة الجلسة (الحالة) ---
if 'unlocked_courses' not in st.session_state:
    st.session_state.unlocked_courses = [1] # الدورة الأولى مفتوحة افتراضياً

if 'cash_balance' not in st.session_state:
    st.session_state.cash_balance = 1250000

# --- 5. قاعدة بيانات المناهج السيادية ---
courses_db = [
    { 
        "id": 1, "phase": "القيادة الاستراتيجية", "title": "القيادة التحويلية في العصر الرقمي", "hours": 20, "price": 299, 
        "img": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800", 
        "desc": "دورة مكثفة لتمكين القادة من قيادة التغيير بفعالية في بيئة رقمية سريعة التطور."
    },
    { 
        "id": 2, "phase": "الاستثمار والمالية", "title": "تحليل الأسهم وأسواق المال", "hours": 25, "price": 499, 
        "img": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800", 
        "desc": "تعلم قراءة وتحليل القوائم المالية للشركات واستخدام النسب للتنبؤ المالي."
    },
    { 
        "id": 3, "phase": "التكنولوجيا والتحول", "title": "الذكاء الاصطناعي في الأعمال", "hours": 15, "price": 350, 
        "img": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800", 
        "desc": "استخدام الذكاء الاصطناعي في التسويق والمالية وخدمة العملاء."
    },
    { 
        "id": 4, "phase": "ريادة الأعمال", "title": "من الفكرة إلى المشروع الشامل", "hours": 25, "price": 399, 
        "img": "https://images.unsplash.com/photo-1507413245164-6160d8298b31?w=800", 
        "desc": "نموذج العمل، دراسة الجدوى، والتمويل الأولي."
    }
]

# --- 6. بناء الواجهة الأمامية ---
st.markdown('<div class="header-title">MR7 ACADEMY</div>', unsafe_allow_html=True)
st.markdown('<div class="header-sub">100 DAYS OF SOVEREIGNTY</div>', unsafe_allow_html=True)

# أزرار تحكم علوية
col_nav1, col_nav2, col_nav3 = st.columns([1,1,3])
with col_nav1:
    st.info(f"💰 الخزنة: ${st.session_state.cash_balance:,}")
with col_nav2:
    if st.button("⚙️ استوديو المبدعين"):
        st.switch_page("pages/7_Creator_Studio.py")

tabs = st.tabs(["📚 المناهج السيادية", "🎓 قاعتي الدراسية (المفتوحة)", "📝 المدونة الاستراتيجية"])

# التبويب الأول: معرض الكورسات
with tabs[0]:
    st.markdown("<br>", unsafe_allow_html=True)
    # رسم الكورسات بنظام الشبكة (Grid)
    cols = st.columns(4)
    for i, course in enumerate(courses_db):
        with cols[i % 4]:
            is_unlocked = course['id'] in st.session_state.unlocked_courses
            
            # كود HTML للبطاقة
            st.markdown(f"""
            <div class="glass-card">
                <div class="img-container">
                    <img src="{course['img']}">
                    {f'<div style="position:absolute; inset:0; background:rgba(0,0,0,0.6); display:flex; align-items:center; justify-content:center; font-size:40px;">🔒</div>' if not is_unlocked else ''}
                </div>
                <span class="badge">{course['phase']}</span>
                <h3 style="margin: 15px 0 10px 0; font-size: 1.3rem; font-weight: 900;">{course['title']}</h3>
                <p style="color: #aaa; font-size: 0.95rem; min-height: 70px; line-height: 1.6;">{course['desc']}</p>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-top: 1px solid #333; padding-top: 15px;">
                    <span style="font-size: 0.9rem; color: #888; font-weight: bold;">⏱️ {course['hours']} ساعة</span>
                    <span class="price-tag">${course['price']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # أزرار التفاعل (Streamlit Native)
            if is_unlocked:
                if st.button("دخول القاعة 🎬", key=f"play_{course['id']}"):
                    st.session_state.selected_course_id = course['id']
                    # سننتقل هنا للصفحة الجديدة التي سنبنيها
                    try:
                        st.switch_page("pages/1_1_Course_Player.py")
                    except Exception as e:
                        st.error("سيتم بناء صفحة المشغل (1_1_Course_Player) في الخطوة القادمة!")
            else:
                # حاوية لزر الشراء بتصميم مختلف
                st.markdown('<div class="btn-locked">', unsafe_allow_html=True)
                if st.button(f"فك التشفير (${course['price']}) 🔒", key=f"buy_{course['id']}"):
                    if st.session_state.cash_balance >= course['price']:
                        st.session_state.cash_balance -= course['price']
                        st.session_state.unlocked_courses.append(course['id'])
                        st.toast("تم فك تشفير المنهج بنجاح! انتقل لقاعتي الدراسية.")
                        st.rerun()
                    else:
                        st.error("رصيد الخزنة غير كافٍ.")
                st.markdown('</div>', unsafe_allow_html=True)

# التبويب الثاني: الكورسات المشتراة
with tabs[1]:
    st.markdown("<br>", unsafe_allow_html=True)
    my_courses = [c for c in courses_db if c['id'] in st.session_state.unlocked_courses]
    
    if not my_courses:
        st.info("لا يوجد لديك مناهج مفتوحة حالياً. قم بفك تشفير المناهج من المعرض.")
    else:
        cols_my = st.columns(4)
        for i, course in enumerate(my_courses):
            with cols_my[i % 4]:
                st.markdown(f"""
                <div class="glass-card" style="border-color: #00FF88;">
                    <div class="img-container">
                        <img src="{course['img']}">
                        <div style="position:absolute; top:10px; right:10px; background:#00FF88; color:black; padding:5px 10px; border-radius:10px; font-weight:bold; font-size:12px;">مفتوح ✅</div>
                    </div>
                    <h3 style="margin: 15px 0 10px 0; font-size: 1.2rem; font-weight: 900;">{course['title']}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("استكمال المنهج ▶️", key=f"resume_{course['id']}"):
                    st.session_state.selected_course_id = course['id']
                    try:
                        st.switch_page("pages/1_1_Course_Player.py")
                    except Exception as e:
                        st.error("سيتم بناء صفحة المشغل (1_1_Course_Player) في الخطوة القادمة!")

# التبويب الثالث: المدونة
with tabs[2]:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 60px; background: rgba(255,255,255,0.02); border: 2px dashed #444; border-radius: 30px;">
        <h1 style="font-size: 60px; filter: none; background: none; color: #666 !important; -webkit-text-fill-color: #666;">📝</h1>
        <h3 style="color: #888 !important;">محرك المدونات (CMS) قيد التجهيز</h3>
    </div>
    """, unsafe_allow_html=True)

st.divider()
if st.button("🏠 العودة للرئيسية"):
    st.switch_page("app.py")
