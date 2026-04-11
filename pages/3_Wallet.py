import streamlit as st
from datetime import datetime

# 1. التحقق من الدخول
if 'logged_in' not in st.session_state or st.session_state['logged_in'] == False:
    st.warning("الرجاء تسجيل الدخول أولاً.")
    st.stop()

st.title("💰 محفظة MR7 الآمنة")

# محاكاة أرصدة من قاعدة البيانات
if 'cash_balance' not in st.session_state:
    st.session_state.cash_balance = 1250.0
    st.session_state.points_balance = 5400

# 2. عرض الأرصدة بشكل احترافي
col1, col2 = st.columns(2)
col1.metric("رصيد الكاش (قابل للسحب)", f"${st.session_state.cash_balance}", "USD")
col2.metric("نقاط الجيميفيكيشن (هجين)", f"{st.session_state.points_balance} PTS", "Active")

st.divider()

# 3. نظام التدقيق (Audit Trail)
st.subheader("📜 سجل العمليات الموثق")

# سجل بيانات محاكى (في الحقيقية نجلبه من قاعدة البيانات)
ledger_data = [
    {"التاريخ": "2026-04-10 10:30", "النوع": "كاش", "العملية": "عمولة مبيعات", "المبلغ": "+$50", "الحالة": "مؤكد ✅"},
    {"التاريخ": "2026-04-11 08:15", "النوع": "نقاط", "العملية": "إنهاء دورة القيادة", "المبلغ": "+100 PTS", "الحالة": "مؤكد ✅"},
]

st.table(ledger_data)

# 4. منطق التحويل الآمن
st.subheader("🔐 تحويل داخلي آمن")
with st.expander("إجراء تحويل جديد"):
    recipient = st.text_input("معرف المستلم (ID):")
    amount = st.number_input("المبلغ:", min_value=1.0)
    
    if st.button("تأفيذ التحويل"):
        if amount <= st.session_state.cash_balance:
            # هنا يحدث المنطق البرمجي الآمن
            st.session_state.cash_balance -= amount
            st.success(f"تم التحويل بنجاح! رقم العملية: TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}")
            st.rerun()
        else:
            st.error("⚠️ فشل العملية: الرصيد غير كافٍ.")
