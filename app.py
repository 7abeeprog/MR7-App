import streamlit as st
import hashlib

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# 1. إعداد "ذاكرة الجلسة" (التأكد من وجود مفتاح حالة الدخول)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 2. إذا لم يكن المستخدم يملك بطاقة الدخول (False)، نعرض شاشة تسجيل الدخول
if st.session_state['logged_in'] == False:
    st.title("مرحباً بك في MR7 🚀")
    email = st.text_input("أدخل بريدك الإلكتروني:")
    password = st.text_input("أدخل كلمة المرور:", type="password")
    
    if st.button("تسجيل الدخول"):
        if password:
            hashed_pw = hash_password(password)
            
            # منح المستخدم بطاقة الدخول!
            st.session_state['logged_in'] = True
            
            # تحديث الشاشة فوراً لتطبيق التغيير
            st.rerun() 
        else:
            st.warning("الرجاء إدخال كلمة المرور أولاً.")

# 3. إذا كان المستخدم يملك البطاقة (True)، نعرض الشاشة الرئيسية (لوحة التحكم)
else:
    st.title("لوحة تحكم MR7 📊")
    st.write("مرحباً! ماذا ترغب في تعلمه اليوم؟")
    st.write("استكشف التوصيات المخصصة لك.")
    
    # محاكاة لإحصائيات من توثيق تطبيقك
    st.info("إحصائيات الأداء: عدد المستخدمين المسجلين في فريقك: 10")
    
    # زر لسحب البطاقة والعودة للبداية
    if st.button("تسجيل الخروج"):
        st.session_state['logged_in'] = False
        st.rerun()
