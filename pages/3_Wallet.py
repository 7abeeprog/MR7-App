import streamlit as st

# 1. التأكد من تسجيل الدخول
if 'logged_in' not in st.session_state or st.session_state['logged_in'] == False:
    st.warning("الرجاء تسجيل الدخول أولاً.")
    st.stop()

st.title("💰 محفظة MR7 الرقمية")
st.write("إدارة أموالك، عمولاتك، ونقاط الولاء في مكان واحد.")

st.divider()

# 2. عرض الأرصدة بنظام الأعمدة الاحترافي
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="الرصيد النقدي (USD)", value="$1,250.00", delta="+ $150")

with col2:
    st.metric(label="نقاط الجيميفيكيشن (PTS)", value="5,400", delta="تحدي يومي")

with col3:
    st.metric(label="العمولات المعلقة", value="$45.00")

st.divider()

# 3. قسم العمليات السريعة
st.subheader("🚀 عمليات سريعة")
action = st.radio("ماذا تريد أن تفعل؟", ["عرض السجل", "تحويل رصيد", "سحب الأرباح"])

if action == "عرض السجل":
    st.table({
        "التاريخ": ["2024-03-01", "2024-03-05", "2024-03-10"],
        "العملية": ["عمولة بيع", "مكافأة تعليمية", "سحب كاش"],
        "المبلغ": ["+$20", "+100 PTS", "-$50"]
    })
elif action == "تحويل رصيد":
    target = st.text_input("أدخل معرف المستخدم (User ID) للمستلم:")
    amount = st.number_input("المبلغ المراد تحويله:", min_value=1.0)
    if st.button("تأكيد التحويل الآمن 🔒"):
        st.success(f"تم إرسال {amount} إلى {target} بنجاح!")
