import streamlit as st

# 1. عنوان الشاشة
st.title("مرحباً بك في MR7 🚀")

# 2. حقول إدخال البيانات
email = st.text_input("أدخل بريدك الإلكتروني:")
password = st.text_input("أدخل كلمة المرور:", type="password")

# 3. زر الدخول والرسالة
if st.button("تسجيل الدخول"):
    st.success("تم تسجيل الدخول بنجاح!")
