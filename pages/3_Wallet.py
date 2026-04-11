import streamlit as st
from datetime import datetime
import time

# --- 1. إعدادات التصميم الإمبراطوري (High-Contrast Financial UI) ---
st.markdown("""
    <style>
    /* تحسين الخلفية العامة للسواد المطلق لضمان التباين */
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

    /* ضمان وضوح النصوص المالية باللون الأبيض الناصع */
    div[data-testid="stMarkdownContainer"] p, h2, h3, span, label, th, td {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.1rem;
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

    /* بطاقات الأرصدة - تصميم Glassmorphism فخم بتباين عالٍ */
    .balance-card {
        background: rgba(30, 30, 30, 0.95);
        border: 2px solid #FFD700;
        border-radius: 35px;
        padding: 45px;
        text-align: center;
        box-shadow: 0 20px 50px rgba(255, 215, 0, 0.2);
        margin-bottom: 30px;
    }
    
    .balance-value {
        font-size: 4rem !important;
        font-weight: 950 !important;
        color: #00FF88 !important; /* أخضر نيون للوضوح التام */
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.6);
    }
    
    .balance-label {
        color: #FFD700 !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 15px;
    }

    /* جداول العمليات (Audit Trail) بتباين فائق */
    .stTable {
        background-color: #111111 !important;
        border-radius: 25px !important;
        border: 2px solid #444 !important;
        overflow: hidden;
    }
    .stTable th {
        background-color: #222 !important;
        color: #FFD700 !important;
        font-size: 1.2rem !important;
    }

    /* أزرار التحويل والعمليات */
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #B8860B 100%) !important;
        color: #000000 !important;
        font-weight: 950 !important;
        border-radius: 22px !important;
        height: 80px !important;
        font-size: 26px !important;
        border: none !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 15px 40px rgba(184, 134, 11, 0.4);
    }
    .stButton>button:hover {
        transform: scale(1.05) translateY(-8px);
        box-shadow: 0 25px 60px rgba(255, 215, 0, 0.7);
    }

    /* حقول الإدخال لتكون واضحة باللون الأبيض */
    .stTextInput input, .stNumberInput input {
        background-color: #1a1a1a !important;
        color: #FFFFFF !important;
        border: 2px solid #555 !important;
        border-radius: 18px !important;
        height: 60px;
        font-size: 1.2rem !important;
    }
    .stTextInput input:focus {
        border-color: #FFD700 !important;
    }
    </style>

    <script>
    // نظام المؤثرات الصوتية المالية
    function playSfx(url) {
        const audio = new Audio(url);
        audio.volume = 0.6;
        audio.play().catch(e => console.log('Audio Blocked'));
    }
    </script>
    """, unsafe_allow_html=True)

def play_wallet_sound(sound_key="success"):
    sounds = {
        "success": "https://assets.mixkit.co/active_storage/sfx/2020/2020-preview.mp3", # صوت ملحمي للنجاح المالي
        "click": "https://www.soundjay.com/buttons/sounds/button-16.mp3"
    }
    st.components.v1.html(f"""
        <audio autoplay><source src="{sounds[sound_key]}" type="audio/mpeg"></audio>
    """, height=0)

# --- 2. جدار الحماية (التأكد من تسجيل الدخول) ---
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("الرجاء تسجيل الدخول أولاً للوصول إلى الخزنة الإمبراطورية.")
    st.stop()

# --- 3. بيانات المحفظة المحاكية لرحلة التريليون ---
if 'cash_balance' not in st.session_state:
    st.session_state.cash_balance = 1250000.00 
    st.session_state.points_balance = 54200

# --- 4. واجهة المستخدم ---
st.title("💰 الخزنة الإمبراطورية MR7")
st.markdown("<p style='text-align:center; color:#FFD700; font-size:24px; font-weight:bold; margin-top:-20px;'>إدارة الثروة والسيادة المالية للقادة</p>", unsafe_allow_html=True)

st.divider()

# عرض الأرصدة بتصميم البطاقات الفخم وعالي التباين
col_cash, col_points = st.columns(2)

with col_cash:
    st.markdown(f"""
    <div class="balance-card">
        <div class="balance-label">رصيد الكاش القابل للسحب</div>
        <div class="balance-value">${st.session_state.cash_balance:,.2f}</div>
        <div style="color: #FFFFFF; font-size: 1.1rem; margin-top: 15px; font-weight: bold;">الحالة: مؤمن تماماً 🔐</div>
    </div>
    """, unsafe_allow_html=True)

with col_points:
    st.markdown(f"""
    <div class="balance-card" style="border-color: #00FF88;">
        <div class="balance-label" style="color: #00FF88 !important;">نقاط الاستحقاق (هجين)</div>
        <div class="balance-value" style="color: #FFFFFF !important;">{st.session_state.points_balance:,.0f} PTS</div>
        <div style="color: #00FF88; font-size: 1.1rem; margin-top: 15px; font-weight: bold;">المستوى: قائد إمبراطوري 💎</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# سجل العمليات المالية (Audit Trail)
st.subheader("📜 سجل التدقيق المالي الموثق")
ledger_data = [
    {"التاريخ": "2026-04-11", "العملية": "عمولة مبيعات شبكة النخبة", "المبلغ": "+$5,200.00", "الحالة": "موثق ✅"},
    {"التاريخ": "2026-04-10", "العملية": "مكافأة إكمال ماراثون القيادة", "المبلغ": "+$1,000.00", "الحالة": "موثق ✅"},
    {"التاريخ": "2026-04-09", "العملية": "أرباح ذكاء اصطناعي مؤتمتة", "المبلغ": "+$450.00", "الحالة": "موثق ✅"},
]
st.table(ledger_data)

st.divider()

# وحدة التحويل الآمنة بين القادة
st.subheader("🔐 وحدة التحويل الاستراتيجي")
with st.expander("إجراء عملية تحويل فوري ومؤمن"):
    recipient = st.text_input("أدخل معرف القائد المستهدف (Elite ID):")
    amount = st.number_input("المبلغ المطلوب تحويله ($):", min_value=10.0, step=100.0)
    
    if st.button("🚀 إطلاق عملية التحويل"):
        if amount <= st.session_state.cash_balance:
            play_wallet_sound("success")
            st.session_state.cash_balance -= amount
            st.success(f"تم تنفيذ التحويل بنجاح إمبراطوري! رقم العملية: MR7-TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}")
            time.sleep(2.5)
            st.rerun()
        else:
            st.error("⚠️ فشل العملية: رصيد الخزنة لا يغطي هذا الطموح المالي.")

# زر الانتقال للدعم الفني
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("💬 طلب استشارة مالية من الخبير الذكي"):
    play_wallet_sound("click")
    st.switch_page("pages/2_Support.py")
