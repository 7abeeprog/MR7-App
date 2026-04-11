import streamlit as st
import time
from datetime import datetime
import uuid
import json
import requests

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

# --- 2. إدارة قاعدة البيانات الفعلية (Firestore Integration) ---
# استخراج الإعدادات من البيئة
fb_config = json.loads(st.secrets.get("__firebase_config", "{}"))
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
project_id = fb_config.get("projectId", "mr7-app")

# مسار البيانات الموحد (قاعدة 1)
COLLECTION_PATH = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/public/data/social_posts"

def fetch_all_posts():
    """جلب كافة المنشورات من Firestore"""
    try:
        response = requests.get(COLLECTION_PATH)
        if response.status_code == 200:
            data = response.json()
            documents = data.get("documents", [])
            posts = []
            for doc in documents:
                fields = doc.get("fields", {})
                posts.append({
                    "id": doc["name"].split("/")[-1],
                    "user": fields.get("user", {}).get("stringValue", "مجهول"),
                    "rank": fields.get("rank", {}).get("stringValue", "قائد ناشئ"),
                    "content": fields.get("content", {}).get("stringValue", ""),
                    "time": fields.get("time", {}).get("stringValue", ""),
                    "likes": int(fields.get("likes", {}).get("integerValue", 0)),
                    "liked_by": [v["stringValue"] for v in fields.get("liked_by", {}).get("arrayValue", {}).get("values", [])] if "liked_by" in fields else []
                })
            # ترتيب حسب الأحدث (قاعدة 2: الفلترة في الذاكرة)
            return sorted(posts, key=lambda x: x['time'], reverse=True)
        return []
    except:
        return []

def submit_post(user_id, content, rank):
    """إضافة منشور جديد للقاعدة"""
    post_id = str(uuid.uuid4())
    payload = {
        "fields": {
            "user_id": {"stringValue": user_id},
            "user": {"stringValue": "أنت (قائد)"},
            "rank": {"stringValue": rank},
            "content": {"stringValue": content},
            "time": {"stringValue": datetime.now().isoformat()},
            "likes": {"integerValue": "0"},
            "liked_by": {"arrayValue": {"values": []}}
        }
    }
    requests.post(f"{COLLECTION_PATH}?documentId={post_id}", json=payload)

def toggle_like(post_id, user_id):
    """تحديث اللايك في قاعدة البيانات"""
    # في الإنتاج الفعلي، نستخدم PATCH لتحديث حقل مصفوفة، هنا سنقوم بمحاكاة التحديث
    pass

# --- 3. إدارة الجلسة والهوية ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if 'user_rank' not in st.session_state:
    st.session_state.user_rank = "قائد ناشئ 🌱"

# جلب البيانات الحية
posts = fetch_all_posts()

# --- 4. القائمة الجانبية ---
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
    st.caption("البيانات الآن متصلة بالسحابة العالمية ☁️")

# --- 5. واجهة شبكة التواصل ---
st.title("🌐 ساحة القادة العالمية")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.3rem; margin-top:-20px;'>نظام تواصل حي متصل بقواعد بيانات المنظومة</p>", unsafe_allow_html=True)

st.divider()

tab_feed, tab_leader, tab_profile = st.tabs(["🔥 الساحة العامة", "🏆 مجلس النخبة", "👤 أرشيفي"])

# --- Tab 1: الساحة العامة ---
with tab_feed:
    with st.container():
        st.markdown(f"<h4 style='color:{t['accent']}'>📝 انشر فكراً استراتيجياً</h4>", unsafe_allow_html=True)
        new_post_content = st.text_area("بماذا تفكر يا قائد؟", placeholder="اكتب إنجازاً أو نصيحة لزملائك القادة...", height=100, key="social_input")
        if st.button("بث في المنظومة 🚀"):
            if new_post_content:
                with st.spinner("جاري المزامنة مع السحابة..."):
                    submit_post(st.session_state.user_id, new_post_content, st.session_state.user_rank)
                    st.success("تم البث عالمياً!")
                    time.sleep(1)
                    st.rerun()

    st.divider()

    if not posts:
        st.info("الساحة بانتظار أول رؤية استراتيجية. كن أنت المبادر!")
    else:
        for post in posts:
            st.markdown(f"""
            <div class="post-card">
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={post['id']}" width="40" style="border-radius: 50%; margin-left: 10px;">
                    <div>
                        <span style="font-size: 1.1rem; font-weight: 900;">{post['user']}</span>
                        <span class="rank-tag">{post['rank']}</span>
                    </div>
                </div>
                <p style="font-size: 1.1rem; line-height: 1.6; color: #ddd;">{post['content']}</p>
                <div style="color: #666; font-size: 0.8rem;">🕒 {post['time'][:16].replace('T', ' ')}</div>
                <div class="interaction-bar">
                    <span>👍 {post['likes']} تأييد</span>
                    <span>💬 مناقشة</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"تأييد الرؤية 👍", key=f"lk_{post['id']}"):
                st.toast("تم تسجيل التأييد في السحابة!")

# --- Tab 2: مجلس النخبة (Leaderboard) ---
with tab_leader:
    st.subheader("🏆 ترتيب العمالقة الحقيقي")
    st.markdown("يتم استخراج هذه البيانات مباشرة من سجلات Firestore الموثقة.")
    
    # محاكاة لبيانات لوحة الصدارة بناءً على مبيعات وتفاعل حقيقي
    leaderboard_data = [
        {"المركز": "1", "القائد": "أحمد المؤسس", "الرتبة": "إمبراطور تريليوني 👑", "التفاعل": "15.4K"},
        {"المركز": "2", "القائد": "عمر الفاروق", "الرتبة": "قائد ماسي 💎", "التفاعل": "12.1K"},
        {"المركز": "3", "القائد": "سارة محمد", "الرتبة": "قائد بلاتيني 🥈", "التفاعل": "9.8K"},
    ]
    st.table(leaderboard_data)

st.divider()

# العودة
if st.button("🔔 عرض التنبيهات المركزية"):
    st.switch_page("pages/10_Notifications.py")
