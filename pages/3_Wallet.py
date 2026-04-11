import streamlit as st
from datetime import datetime

# --- 1. إعدادات التصميم الإمبراطوري (High-Contrast Financial UI) ---
st.markdown("""
    <style>
    /* تحسين الخلفية العامة للسواد المطلق */
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    /* هندسة القائمة الجانبية (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 2px solid #FFD700 !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* ضمان وضوح النصوص المالية باللون الأبيض */
    div[data-testid="stMarkdownContainer"] p, h2, h3, span, label, th, td {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* العنوان الرئيسي الذهبي المتوهج */
    h1 {
        background: linear-gradient(90deg, #FFD700, #FFFFFF, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 950 !important;
        text-align: center;
        filter: drop-shadow(0 0 15px rgba(255, 215, 0, 0.8));
        font-size: 3.5rem !important;
        margin-bottom: 30px !important;
    }

    /* بطاقات الأرصدة - Glassmorphism فخم */
    .balance-card {
        background: rgba(25, 25, 25, 0.95);
        border: 2px solid #FFD700;
        border-radius: 30px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 15px 45px rgba(255, 215, 0, 0.15);
        margin-bottom: 25px;
    }
    
    .balance-value {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        color: #00FF88 !important; /* أخضر زمردي للنمو المالي */
        text-shadow: 0 0 15px rgba(0, 255, 136, 0.5);
    }
    
    .balance-label {
        color: #FFD700 !important;
        font-size: 1.4rem !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 10px;
    }

    /* جداول العمليات (Audit Trail) */
    .stTable {
        background-color: #0a0a0a !important;
        border-radius: 20px !important;
        border: 1px solid #444 !important;
        overflow: hidden;
    }

    /* أزرار التحويل والعمليات */
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%) !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
        height: 75px !important;
        font-size: 24px !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02) translateY(-5px);
        box-shadow: 0 20px 50px rgba(255, 215, 0, 0.6);
    }

    /* حقول الإدخال */
    .stTextInput input, .stNumberInput input {
        background-color: #111 !important;
        color: white !important;
        border: 2px solid #333 !important;
        border-radius: 15px !important;
        height: 55px;
    }
    </style>

    <script>
    function playSfx(url) {
        const audio = new Audio(url);
        audio.volume = 0.5;
        audio.play().catch(e => console.log('Audio Blocked'));
    }
    </script>
    """, unsafe_allow_html=True)

def play_wallet_sound(sound_key="success"):
    sounds = {
        "success": "https://assets.mixkit.co/active_storage/sfx/2020/2020-preview.mp3", # صوت نجاح ملحمي
        "click": "https://www.soundjay.com/buttons/sounds/button-16.mp3"
    }
    st.components.v1.html(f"""
        <audio autoplay><source src="{sounds[sound_key]}" type="audio/mpeg"></audio>
    """, height=0)

# --- 2. التحقق من الدخول ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("الرجاء تسجيل الدخول أولاً للوصول إلى الخزنة.")
    st.stop()

# --- 3. بيانات المحفظة المحاكية ---
if 'cash_balance' not in st.session_state:
    st.session_state.cash_balance = 1250000.00 # بدأت رحلة المليون!
    st.session_state.points_balance = 54200

# --- 4. واجهة المستخدم ---
st.title("💰 الخزنة الإمبراطورية MR7")
st.markdown("<p style='text-align:center; color:#FFD700; font-size:22px; font-weight:bold; margin-top:-20px;'>إدارة الثروة والتدفقات النقدية للقادة</p>", unsafe_allow_html=True)

st.divider()

# عرض الأرصدة بتصميم البطاقات الفخم
col_cash, col_points = st.columns(2)

with col_cash:
    st.markdown(f"""
    <div class="balance-card">
        <div class="balance-label">رصيد الكاش القابل للسحب</div>
        <div class="balance-value">${st.session_state.cash_balance:,.2f}</div>
        <div style="color: #FFFFFF; font-size: 1rem; margin-top: 10px;">الحالة: مؤمن وموثق ✅</div>
    </div>
    """, unsafe_allow_html=True)

with col_points:
    st.markdown(f"""
    <div class="balance-card" style="border-color: #00FF88;">
        <div class="balance-label" style="color: #00FF88 !important;">نقاط الاستحقاق (هجين)</div>
        <div class="balance-value" style="color: #FFFFFF !important;">{st.session_state.points_balance:,.0f} PTS</div>
        <div style="color: #00FF88; font-size: 1rem; margin-top: 10px;">المستوى: قائد بلاتيني 💎</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# سجل العمليات (Audit Trail) بوضوح عالٍ
st.subheader("📜 سجل العمليات المالية الموثق")
ledger_data = [
    {"التاريخ": "2026-04-11", "العملية": "عمولة مبيعات فريق النخبة", "المبلغ": "+$5,200", "الحالة": "مؤكد ✅"},
    {"التاريخ": "2026-04-10", "العملية": "مكافأة إكمال مسار المليار", "المبلغ": "+$1,000", "الحالة": "مؤكد ✅"},
    {"التاريخ": "2026-04-09", "العملية": "تحويل من الوكيل الذكي (AI)", "المبلغ": "+$450", "الحالة": "مؤكد ✅"},
]
st.table(ledger_data)

st.divider()

# نظام التحويل الآمن
st.subheader("🔐 وحدة التحويل الآمنة")
with st.expander("إجراء عملية تحويل خارق للحدود"):
    recipient = st.text_input("أدخل معرف القائد المستلم (Unique ID):")
    amount = st.number_input("المبلغ المطلوب تحويله ($):", min_value=10.0, step=100.0)
    
    if st.button("🚀 تنفيذ التحويل الفوري"):
        if amount <= st.session_state.cash_balance:
            play_wallet_sound("success")
            st.session_state.cash_balance -= amount
            st.success(f"تمت العملية بنجاح! رقم المرجع: MR7-TXN-{datetime.now().strftime('%Y%m%d%H%M')}")
            time.sleep(2)
            st.rerun()
        else:
            st.error("⚠️ فشل العملية: رصيد الخزنة غير كافٍ لهذا الطموح.")

# الانتقال لمركز الدعم
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("💬 طلب استشارة مالية من الدعم الفني"):
    play_wallet_sound("click")
    st.switch_page("pages/2_Support.py")
