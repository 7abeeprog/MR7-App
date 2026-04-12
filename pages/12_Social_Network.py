import streamlit as st
import time
from datetime import datetime
import uuid
import json
import requests
import pandas as pd

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
    /* الفلسفة التصميمية: ساحة رقمية للسيادة والتواصل الإمبراطوري */
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

    .post-card {{
        background: {t['card']};
        border: 1px solid rgba(255,215,0,0.2);
        border-radius: 25px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .post-card:hover {{ transform: scale(1.01); border-color: {t['accent']}; }}
    
    .rank-tag {{
        background: {t['accent']};
        color: black !important;
        padding: 3px 12px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 900;
        margin-right: 10px;
    }}

    .success-cable-badge {{
        background: #00FF88;
        color: black !important;
        padding: 2px 10px;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 900;
        margin-right: 5px;
    }}

    /* حل مشكلة الكتابة باللون الأسود في الحقول البيضاء */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid {t['border']} !important;
        border-radius: 15px !important;
        font-weight: bold !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 20px !important;
        height: 60px;
    }}
    
    .interaction-bar {{
        display: flex;
        gap: 25px;
        margin-top: 15px;
        border-top: 1px solid rgba(255,255,255,0.05);
        padding-top: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك السحابة السيادي (Live Firestore Integration) ---
fb_config = json.loads(st.secrets.get("__firebase_config", "{}"))
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
project_id = fb_config.get("projectId", "mr7-app")
BASE_URL = "https://firestore.googleapis.com/v1/"
COLLECTION_PATH = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/public/data/social_posts"

if 'user_id' not in st.session_state: st.session_state.user_id = str(uuid.uuid4())
if 'user_rank' not in st.session_state: st.session_state.user_rank = "قائد استراتيجي 💎"

def fetch_live_feed():
    """جلب برقيات النجاح الحية من السحابة"""
    try:
        res = requests.get(f"{BASE_URL}{COLLECTION_PATH}")
        if res.status_code == 200:
            docs = res.json().get("documents", [])
            feed = []
            for doc in docs:
                f = doc.get("fields", {})
                feed.append({
                    "id": doc["name"].split("/")[-1],
                    "user": f.get("user", {}).get("stringValue", "قائد مجهول"),
                    "rank": f.get("rank", {}).get("stringValue", "عضو"),
                    "content": f.get("content", {}).get("stringValue", ""),
                    "time": f.get("time", {}).get("stringValue", ""),
                    "likes": int(f.get("likes", {}).get("integerValue", 0)),
                    "type": f.get("type", {}).get("stringValue", "نصيحة")
                })
            return sorted(feed, key=lambda x: x['time'], reverse=True)
        return []
    except: return []

def publish_imperial_cable(content, cable_type):
    """بث برقية نجاح جديدة للسحابة العالمية"""
    doc_id = str(uuid.uuid4())
    display_name = f"القائد ({st.session_state.user_id[:5].upper()})"
    payload = {
        "fields": {
            "user_id": {"stringValue": st.session_state.user_id},
            "user": {"stringValue": display_name},
            "rank": {"stringValue": st.session_state.user_rank},
            "content": {"stringValue": content},
            "type": {"stringValue": cable_type},
            "time": {"stringValue": datetime.now().isoformat()},
            "likes": {"integerValue": "0"}
        }
    }
    res = requests.post(f"{BASE_URL}{COLLECTION_PATH}?documentId={doc_id}", json=payload)
    return res.status_code == 200

# --- 3. واجهة ساحة القادة العالمية ---
st.title("🌐 ساحة القادة العالمية")
st.markdown(f"<p style='text-align:center; color:{t['accent']}; font-size:1.4rem; margin-top:-20px;'>مزامنة فورية للرؤى والنجاحات بين قادة الأقاليم</p>", unsafe_allow_html=True)

st.divider()

# منطقة البث السيادي
with st.container():
    st.markdown(f"#### 🎙️ بث برقية نجاح جديدة")
    c_col1, c_col2 = st.columns([3, 1])
    with c_col2:
        cable_type = st.selectbox("نوع البرقية:", ["نصيحة استراتيجية", "إنجاز مالي", "توسع جغرافي", "فكر قيادي"])
    with c_col1:
        new_content = st.text_area("بماذا تفكر يا قائد؟", placeholder="شارك إنجاز اليوم أو نصيحة لجيوش القادة...", height=100)
    
    if st.button("🚀 بث البرقية في المنظومة"):
        if new_content:
            with st.spinner("جاري المزامنة مع السجلات السحابية..."):
                if publish_imperial_cable(new_content, cable_type):
                    st.success("تم البث بنجاح! رؤيتك الآن تلهم القادة عالمياً.")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
        else: st.warning("الرجاء كتابة محتوى البرقية أولاً.")

st.divider()

# الأقسام التفاعلية
tabs = st.tabs(["🔥 البرقيات الحية", "🏆 متصدرو التفاعل", "👤 أرشيفي السيادي"])

# --- Tab 1: البرقيات الحية (The Live Feed) ---
with tabs[0]:
    live_feed = fetch_live_feed()
    
    if not live_feed:
        # بيانات تجريبية فخمة في حالة عدم توفر اتصال
        live_feed = [
            {"id":"1", "user": "أحمد (مصر)", "rank": "إمبراطور تريليوني 👑", "content": "تم اليوم إتمام أول صفقة عقارية عبر نظام التمويل الجماعي في مدينة النبت. السيادة بدأت!", "time": "2026-04-12T10:00:00", "likes": 124, "type": "إنجاز مالي"},
            {"id":"2", "user": "صالح (ليبيا)", "rank": "قائد استراتيجي 💎", "content": "قانون الـ 10 يعمل بكفاءة مذهلة في إقليم ليبيا. فريقنا وصل لـ 500 عضو في أسبوعين.", "time": "2026-04-12T09:15:00", "likes": 85, "type": "توسع جغرافي"}
        ]

    for cable in live_feed:
        is_mine = st.session_state.user_id[:5].upper() in cable['user']
        border_color = "#00FF88" if is_mine else t['border']
        
        st.markdown(f"""
        <div class="post-card" style="border-color: {border_color};">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
                <div style="display: flex; align-items: center;">
                    <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={cable['user']}" width="50" style="border-radius: 50%; margin-left: 15px; border: 2px solid {t['accent']};">
                    <div>
                        <span style="font-size: 1.2rem; font-weight: 950;">{cable['user']}</span>
                        <br><span class="rank-tag">{cable['rank']}</span>
                    </div>
                </div>
                <span class="success-cable-badge">🛡️ {cable['type']}</span>
            </div>
            <p style="font-size: 1.3rem; line-height: 1.7; color: #ddd; margin-bottom: 20px;">{cable['content']}</p>
            <div style="color: #666; font-size: 0.85rem; display: flex; justify-content: space-between;">
                <span>🕒 {cable['time'][:16].replace('T', ' ')}</span>
                <span style="color: #00FF88; font-weight: 900;">👍 {cable['likes']} تأييد سيادي</span>
            </div>
            <div class="interaction-bar">
                <button style="background: transparent; border: 1px solid rgba(255,255,255,0.1); color: white; padding: 5px 15px; border-radius: 10px; cursor: pointer;">👍 تأييد</button>
                <button style="background: transparent; border: 1px solid rgba(255,255,255,0.1); color: white; padding: 5px 15px; border-radius: 10px; cursor: pointer;">💬 مناقشة</button>
                <button style="background: transparent; border: 1px solid rgba(255,255,255,0.1); color: white; padding: 5px 15px; border-radius: 10px; cursor: pointer;">📤 مشاركة</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- Tab 2: متصدرو التفاعل ---
with tabs[1]:
    st.subheader("🏆 عمالقة التأثير الاجتماعي")
    leaderboard = [
        {"المركز": "1", "القائد": "أحمد المؤسس", "التفاعل الكلي": "12,450", "الأوسمة": "👑🥇"},
        {"المركز": "2", "القائد": "صالح الليبي", "التفاعل الكلي": "8,120", "الأوسمة": "💎🥈"},
        {"المركز": "3", "القائد": "إدريس السوداني", "التفاعل الكلي": "5,400", "الأوسمة": "🌍🥉"}
    ]
    st.table(pd.DataFrame(leaderboard))

# --- Tab 3: أرشيفي السيادي ---
with tabs[2]:
    st.subheader("👤 برقياتي الموثقة سحابياً")
    my_cables = [c for c in live_feed if st.session_state.user_id[:5].upper() in c['user']]
    if not my_cables:
        st.info("لم تقم ببث أي برقية بعد. كن ملهماً وابدأ الآن!")
    else:
        for mc in my_cables:
            st.markdown(f"- **[{mc['type']}]**: {mc['content'][:50]}... ({mc['likes']} تأييد)")

st.divider()

# خريطة الانتقال
st.markdown("### 🗺️ خريطة السيادة السريعة")
cb1, cb2, cb3 = st.columns(3)
with cb1:
    if st.button("🔔 التنبيهات"): st.switch_page("pages/10_Notifications.py")
with cb2:
    if st.button("👥 إدارة الفرق"): st.switch_page("pages/6_Teams.py")
with cb3:
    if st.button("🏠 الرئيسية"): st.switch_page("app.py")
