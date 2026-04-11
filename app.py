import streamlit as st
import hashlib

# إعداد شكل الصفحة (يجب أن يكون أول سطر بعد الاستدعاء)
st.set_page_config(page_title="MR7 Super App", page_icon="🚀", layout="wide")

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# إعداد ذاكرة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# شاشة تسجيل الدخول
if st.session_state['logged_in'] == False:
    st.title("مرحباً بك في منصة MR7 🚀")
    st.write("الرجاء تسجيل الدخول للوصول إلى الأنظمة.")
    
    email = st.text_input("أدخل بريدك الإلكتروني:")
    password = st.text_input("أدخل كلمة المرور:", type="password")
    
    if st.button("تسجيل الدخول"):
        if password:
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.warning("الرجاء إدخال كلمة المرور أولاً.")

# الشاشة الرئيسية بعد الدخول
else:
    st.title("لوحة تحكم MR7 📊")
    st.success("مرحباً بك مجدداً!")
    
    # توجيه المستخدم للقائمة الجانبية
    st.write("### 👈 **استخدم القائمة الجانبية للتنقل بين أنظمة التطبيق.**")
    st.info("إحصائيات سريعة: لديك 10 أعضاء في فريقك، و 50 نقطة في نظام الجيميفيكيشن.")
    
    st.divider()
    if st.button("تسجيل الخروج"):
        st.session_state['logged_in'] = False
        st.rerun()
