import streamlit as st
import hashlib

# 1. دالة التشفير
def hash_password(password):
    # نستخدم خوارزمية SHA-256 القوية للتشفير
    return hashlib.sha256(str.encode(password)).hexdigest()

st.title("مرحباً بك في MR7 🚀")

email = st.text_input("أدخل بريدك الإلكتروني:")
password = st.text_input("أدخل كلمة المرور:", type="password")

if st.button("تسجيل الدخول"):
    if password:
        # 2. تشفير كلمة المرور قبل أي شيء
        hashed_pw = hash_password(password)
        
        st.success("تم التقاط البيانات بنجاح!")
        st.info(f"شكل كلمة المرور المشفرة التي سنحفظها لاحقاً في قاعدة البيانات:\n {hashed_pw}")
    else:
        st.warning("الرجاء إدخال كلمة المرور أولاً.")
