import streamlit as st
import time
from datetime import datetime
import uuid

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

    .post-card {{
        background: {t['card']};
        border: 1px solid {t['border']};
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }}
    
    .rank-tag {{
        background: {t['accent']};
        color: black !important;
        padding: 2px 10px;
        border-radius: 10px;
        font-size: 0.75rem;
        font-weight: 900;
        margin-left: 10px;
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
    }}
    
    .interaction-bar {{
        display: flex;
        gap: 20px;
        margin-top: 15px;
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. إدارة قاعدة البيانات (Database Integration) ---
# ملاحظة: في بيئة الاختبار، نستخدم محاكاة ذكية للبيانات المستمرة
# عند الربط الفعلي بـ Firestore، سيتم استخدام مكتبة firebase-admin

app_id = "mr7-empire-v1"

if 'social_posts' not in st.session_state:
    # بيانات أولية محاكاة لما هو موجود في قاعدة البيانات
    st.session_state.social_posts = [
        {"id": "p1", "user": "عمر الفاروق", "rank": "قائد ماسي 💎", "content": "الحمد لله، تم إغلاق جولة تمويل جماعي بنجاح! شكراً لجيش القادة.", "time": "منذ ساعتين", "likes": 24, "liked_by": []},
        {"id": "p2", "user": "ليلى الاستراتيجية", "rank": "خبير محتوى 📚", "content": "أطلقت درساً جديداً في استوديو المبدعين حول 'هندسة الثراء'. بانتظار تقييمكم.", "time": "منذ 4 ساعات", "likes": 15, "liked_by": []}
    ]

if 'user_rank' not in st.session_state:
    st.session_state.user_rank = "قائد ناشئ 🌱"

if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# --- 3. القائمة الجانبية ---
with st.sidebar:
    st.markdown(f"### 🎨 تخصيص المظهر")
    theme_choice = st.selectbox("النمط الحالي:", options=list(themes.keys()), index=list(themes.keys()).index(st.session_state.app_theme))
    if theme_choice != st.session_state.app_theme:
        st.session_state.app_theme = theme_choice
        st.rerun()
    st.divider()
    st.markdown("### 👤 ملفك القيادي")
    st.image(f"https://api.dicebear.com/7.x/avataaars/svg?seed={st.session_state.user_id}", width=100)
    st.markdown(f"**معرف القائد:** <br> `{st.session_state.user_id[:8]}`", unsafe_allow_html=True)
    st.markdown(f"**الرتبة:** <span style='color:{t['accent']}'>{st.session_state.user_rank}</span>", unsafe_allow_html=True)
    st.progress(0.4)
    st.caption("متبقي 600 XP للرتبة التالية")

# --- 4. واجهة شبكة التواصل ---
st.title("🌐 ساحة القادة العالمية")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.3rem; margin-top:-20px;'>نظام التواصل التفاعلي وقواعد البيانات المشتركة</p>", unsafe_allow_html=True)

st.divider()

tabs = st.tabs(["🔥 الساحة العامة", "🏆 مجلس النخبة", "👤 أرشيفي الخاص"])

# --- Tab 1: الساحة العامة (Feed) ---
with tabs[0]:
    # إنشاء منشور جديد وحفظه في "قاعدة البيانات"
    with st.container():
        st.markdown(f"<h4 style='color:{t['accent']}'>📝 انشر فكراً استراتيجياً</h4>", unsafe_allow_html=True)
        new_post_content = st.text_area("بماذا تفكر يا قائد؟", placeholder="اكتب إنجازاً أو نصيحة لزملائك القادة...", height=100, key="post_input")
        col_btn, col_empty = st.columns([1, 3])
        if col_btn.button("بث في المنظومة 🚀"):
            if new_post_content:
                # هنا يتم تنفيذ الـ setDoc في قاعدة البيانات الفعلية
                post_entry = {
                    "id": str(uuid.uuid4()),
                    "user": "أنت (قائد)",
                    "rank": st.session_state.user_rank,
                    "content": new_post_content,
                    "time": datetime.now().strftime("%H:%M"),
                    "likes": 0,
                    "liked_by": []
                }
                st.session_state.social_posts.insert(0, post_entry)
                st.success("تم الحفظ في قاعدة البيانات وبث المنشور عالمياً!")
                time.sleep(1)
                st.rerun()

    st.divider()

    # عرض المنشورات بجلبها من الحالة (التي تمثل قاعدة البيانات)
    for idx, post in enumerate(st.session_state.social_posts):
        st.markdown(f"""
        <div class="post-card">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={post['user']}" width="40" style="border-radius: 50%; margin-left: 10px;">
                <div>
                    <span style="font-size: 1.1rem; font-weight: 900;">{post['user']}</span>
                    <span class="rank-tag">{post['rank']}</span>
                </div>
            </div>
            <p style="font-size: 1.1rem; line-height: 1.6; color: #ddd;">{post['content']}</p>
            <div style="color: #666; font-size: 0.8rem;">🕒 {post['time']}</div>
            <div class="interaction-bar">
                <span>👍 {post['likes']} تأييد</span>
                <span>💬 مناقشة</span>
                <span>🔗 مشاركة الرابط</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # منطق الـ Like المرتبط بقاعدة البيانات
        if st.session_state.user_id not in post['liked_by']:
            if st.button(f"تأييد الرؤية 👍", key=f"like_{post['id']}"):
                post['likes'] += 1
                post['liked_by'].append(st.session_state.user_id)
                st.rerun()
        else:
            st.caption("لقد قمت بتأييد هذا القائد مسبقاً ✅")

# --- Tab 2: مجلس النخبة (Leaderboard) ---
with tabs[1]:
    st.subheader("🏆 ترتيب العمالقة (Live Leaderboard)")
    st.markdown("يتم تحديث هذه القائمة لحظياً بناءً على بيانات قاعدة البيانات المركزية.")
    
    # محاكاة لبيانات لوحة الصدارة المستخرجة من Firestore
    leaderboard_data = [
        {"المركز": "1", "القائد": "أحمد المؤسس", "الرتبة": "إمبراطور تريليوني 👑", "التفاعل": "15.4K"},
        {"المركز": "2", "القائد": "عمر الفاروق", "الرتبة": "قائد ماسي 💎", "التفاعل": "12.1K"},
        {"المركز": "3", "القائد": "سارة محمد", "الرتبة": "قائد بلاتيني 🥈", "التفاعل": "9.8K"},
        {"المركز": "4", "القائد": "ليلى الاستراتيجية", "الرتبة": "خبير محتوى 📚", "التفاعل": "7.2K"},
    ]
    st.table(leaderboard_data)
    
    st.info("💡 يتم احتساب الترتيب بناءً على: مبيعات الفريق، الأوسمة التعليمية، وتفاعل المجتمع مع منشوراتك.")

# --- Tab 3: أرشيفي الخاص ---
with tabs[2]:
    st.subheader("👤 أرشيف بياناتك")
    col1, col2 = st.columns(2)
    user_posts_count = len([p for p in st.session_state.social_posts if p['user'] == "أنت (قائد)"])
    
    with col1:
        st.markdown(f"""
        <div class="post-card" style="text-align: center;">
            <h4 style="color:{t['accent']}">منشوراتك الموثقة</h4>
            <div style="font-size: 2.5rem; font-weight: 900;">{user_posts_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="post-card" style="text-align: center;">
            <h4 style="color:{t['accent']}">إجمالي التأييدات</h4>
            <div style="font-size: 2.5rem; font-weight: 900;">124</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# العودة
if st.button("🔔 مركز التنبيهات المركزية"):
    st.switch_page("pages/10_Notifications.py")
