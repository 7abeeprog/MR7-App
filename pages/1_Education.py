import streamlit as st
import time
from datetime import datetime, date
import json
import requests
import uuid
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

    .rank-badge {{
        background: linear-gradient(135deg, {t['accent']}, #FFFFFF);
        color: #000 !important;
        padding: 10px 25px;
        border-radius: 50px;
        font-weight: 900;
        display: inline-block;
        margin: 10px 0;
        box-shadow: 0 0 20px {t['accent']};
        font-size: 1.2rem;
    }}

    .journey-counter {{
        background: {t['card']};
        border: 2px solid {t['border']};
        border-radius: 25px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
    }}
    .days-number {{
        font-size: 4rem !important;
        font-weight: 900 !important;
        color: {t['accent']} !important;
    }}

    .course-card {{
        background: rgba(25, 25, 25, 0.95);
        padding: 35px;
        border-radius: 30px;
        border: 2px solid #00FF88;
        margin-bottom: 25px;
        transition: 0.3s;
    }}
    .course-card:hover {{ transform: translateY(-5px); border-color: {t['accent']}; }}

    .stButton>button {{
        background: linear-gradient(135deg, {t['accent']} 0%, {t['border']} 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 20px !important;
        height: 65px;
        font-size: 1.1rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك الرتب والذكاء التعليمي (Rank Logic) ---
def get_rank_info(xp):
    """تحديد الرتبة والتقدم بناءً على نقاط الخبرة"""
    if xp < 1000:
        return "قائد متدرب 🌱", "المستكشف", 1000, 0.2
    elif xp < 5000:
        return "استراتيجي صاعد 📈", "القائد الميداني", 5000, 0.5
    elif xp < 15000:
        return "مهندس إمبراطورية 🏗️", "جنرال السيادة", 15000, 0.7
    elif xp < 50000:
        return "أسطورة المعرفة 👑", "الحكيم الملياري", 50000, 0.9
    else:
        return "باني حضارات 🌌", "مؤسس التريليون", 1000000, 1.0

# --- 3. محرك السحابة (Education Cloud Integration) ---
fb_config = json.loads(st.secrets.get("__firebase_config", "{}"))
app_id = st.secrets.get("__app_id", "mr7-empire-v1")
project_id = fb_config.get("projectId", "mr7-app")
BASE_URL = "https://firestore.googleapis.com/v1/"

if 'user_id' not in st.session_state: st.session_state.user_id = str(uuid.uuid4())

def get_user_edu_data():
    """جلب بيانات التقدم التعليمي من السحابة"""
    path = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/users/{st.session_state.user_id}/education_data/main"
    try:
        res = requests.get(f"{BASE_URL}{path}")
        if res.status_code == 200:
            f = res.json().get("fields", {})
            return {
                "xp": int(f.get("xp", {}).get("integerValue", 0)),
                "progress": int(f.get("progress", {}).get("integerValue", 0)),
                "start_date": f.get("start_date", {}).get("stringValue", datetime.now().strftime("%Y-%m-%d"))
            }
        return {"xp": 0, "progress": 0, "start_date": "2026-03-27"}
    except: return {"xp": 0, "progress": 0, "start_date": "2026-03-27"}

def update_edu_progress(new_xp, new_prog):
    """تحديث التقدم التعليمي في السحابة"""
    path = f"projects/{project_id}/databases/(default)/documents/artifacts/{app_id}/users/{st.session_state.user_id}/education_data/main"
    payload = {
        "fields": {
            "xp": {"integerValue": str(new_xp)},
            "progress": {"integerValue": str(new_prog)},
            "last_active": {"stringValue": datetime.now().isoformat()},
            "start_date": {"stringValue": "2026-03-27"}
        }
    }
    requests.patch(f"{BASE_URL}{path}?updateMask.fieldPaths=xp&updateMask.fieldPaths=progress&updateMask.fieldPaths=last_active&updateMask.fieldPaths=start_date", json=payload)

# --- 4. واجهة الأكاديمية التعليمية ---
st.title("🎓 مركز التميز القيادي")

# جلب البيانات الحية وحساب الرتبة
edu_data = get_user_edu_data()
rank_title, rank_desc, next_target, rank_prog = get_rank_info(edu_data['xp'])

# عرض الرتبة والتقدم بشكل فخم
col_r1, col_r2 = st.columns([2, 1])
with col_r1:
    st.markdown(f"### الحالة الحالية: <div class='rank-badge'>{rank_title}</div>", unsafe_allow_html=True)
    st.write(f"لقب الاستحقاق: **{rank_desc}**")
with col_r2:
    st.markdown(f"<div style='text-align:right;'><small>التقدم للرتبة التالية</small></div>", unsafe_allow_html=True)
    st.progress(min(1.0, edu_data['xp'] / next_target))
    st.markdown(f"<div style='text-align:right;'><small>{edu_data['xp']:,} / {next_target:,} XP</small></div>", unsafe_allow_html=True)

st.divider()

# حساب رحلة الـ 100 يوم
s_date = datetime.strptime(edu_data['start_date'], "%Y-%m-%d").date()
days_passed = (date.today() - s_date).days
days_left = max(0, 100 - days_passed)

col_info1, col_info2 = st.columns(2)
with col_info1:
    st.markdown(f"""
    <div class="journey-counter">
        <small>يوم متبقي للسيادة</small>
        <div class="days-number">{days_left}</div>
    </div>
    """, unsafe_allow_html=True)
with col_info2:
    st.markdown(f"""
    <div class="journey-counter">
        <small>إجمالي نقاط الخبرة (XP)</small>
        <div class="days-number" style="color:#00FF88 !important;">{edu_data['xp']:,}</div>
    </div>
    """, unsafe_allow_html=True)

# شريط التقدم التعليمي العام
st.subheader("📈 تقدم المنهج الموثق")
st.progress(edu_data['progress'] / 100)
st.caption(f"تم إنجاز {edu_data['progress']}% من المسار التأسيسي.")

st.markdown("<br>", unsafe_allow_html=True)

# الأقسام الدراسية
col_c1, col_c2 = st.columns(2)

with col_c1:
    st.markdown(f"""
    <div class="course-card">
        <h3 style='color:#FFD700;'>عقلية المليار 🧠</h3>
        <p>دروس هندسة القيمة الذاتية وتجاوز حدود الممكن.</p>
        <p style='color:#00FF88; font-weight:900;'>+150 XP لكل درس</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("متابعة الدرس الحالي 📖", key="btn_course_1"):
        with st.spinner("جاري توثيق الحضور وتحديث الرتبة..."):
            update_edu_progress(edu_data['xp'] + 150, min(100, edu_data['progress'] + 5))
            st.success("أحسنت! +150 XP. تقدمك في السحابة محفوظ.")
            time.sleep(1)
            st.rerun()

with col_c2:
    st.markdown(f"""
    <div class="course-card" style="border-color: #FFD700;">
        <h3 style='color:#FFD700;'>القيادة الخضراء 🌍</h3>
        <p>التوسع الجغرافي المستدام وأثر مشاريع السودان ومصر.</p>
        <p style='color:#FF4B4B; font-weight:900;'>فتح عند 5000 XP</p>
    </div>
    """, unsafe_allow_html=True)
    disabled = edu_data['xp'] < 5000
    if st.button("بدء المسار الاستراتيجي 🚀", disabled=disabled, key="btn_course_2"):
        st.success("انطلق يا قائد!")

st.divider()

# وحدة استخراج البيانات السيادية
with st.expander("📊 وحدة استخراج تقارير الأداء"):
    report_data = {
        "المعرف": st.session_state.user_id[:8],
        "الرتبة": rank_title,
        "اللقب": rank_desc,
        "XP المجموع": edu_data['xp'],
        "نسبة الإنجاز": f"{edu_data['progress']}%",
        "تاريخ البدء": edu_data['start_date']
    }
    report_df = pd.DataFrame([report_data])
    st.table(report_df)
    
    csv = report_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 تحميل شهادة الأداء المؤقتة (CSV)",
        data=csv,
        file_name=f"MR7_Leader_Report_{st.session_state.user_id[:8]}.csv",
        mime='text/csv',
    )

st.divider()

if st.button("🏠 العودة لمركز القيادة الرئيسي"):
    st.switch_page("app.py")
