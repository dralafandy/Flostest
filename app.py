import streamlit as st
from finance_manager import FinanceManager
from mobile_styles import apply_mobile_styles  # Import mobile styles
from styles import apply_sidebar_styles, apply_topbar_styles  # Import other styles

# Apply styles
apply_mobile_styles()
apply_sidebar_styles()
apply_topbar_styles()

# Set page configuration
st.set_page_config(page_title="FloosAfandy - إحسبها يا عشوائي !!", layout="wide")

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Show navigation components
st.sidebar.title("التنقل")
if st.sidebar.button("🏠 الرئيسية"):
    st.session_state.current_page = "home"
if st.sidebar.button("💳 المعاملات"):
    st.session_state.current_page = "transactions"
if st.sidebar.button("🏦 الحسابات"):
    st.session_state.current_page = "accounts"
if st.sidebar.button("📈 التقارير"):
    st.session_state.current_page = "reports"
if st.sidebar.button("📚 التعليمات"):
    st.session_state.current_page = "instructions"

# Handle page navigation
if st.session_state.current_page == "home":
    if st.session_state.logged_in:
        st.success("مرحبًا بك في FloosAfandy!")
        st.write("يمكنك الآن إدارة حساباتك ومعاملاتك.")
    else:
        st.title("مرحبًا بك في FloosAfandy")
        st.markdown(
            f'<div style="display: flex; justify-content: center; margin: 20px 0;">'
            f'<img src="https://i.ibb.co/KpzDy27r/IMG-2998.png" width="300">'
            f'</div>',
            unsafe_allow_html=True
        )
        tab1, tab2 = st.tabs(["🔑 تسجيل الدخول", "🆕 إنشاء حساب جديد"])

        fm = FinanceManager()

        with tab1:  # Login
            st.subheader("تسجيل الدخول إلى حسابك")
            login_username = st.text_input("اسم المستخدم", key="login_username")
            login_password = st.text_input("كلمة المرور", type="password", key="login_password")
            if st.button("تسجيل الدخول"):
                if fm.verify_user(login_username, login_password):
                    st.session_state.user_id = login_username
                    st.session_state.logged_in = True
                    st.success(f"مرحبًا بك، {login_username}!")
                    st.session_state.current_page = "transactions"  # Redirect to transactions page
                    st.experimental_rerun()
                else:
                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")

        with tab2:  # Register
            st.subheader("إنشاء حساب جديد")
            new_username = st.text_input("اسم المستخدم", key="new_username")
            new_password = st.text_input("كلمة المرور", type="password", key="new_password")
            confirm_password = st.text_input("تأكيد كلمة المرور", type="password", key="confirm_password")
            if st.button("إنشاء الحساب"):
                if new_password == confirm_password:
                    if fm.add_user(new_username, new_password):
                        st.success(f"تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول باستخدام {new_username}.")
                    else:
                        st.error("اسم المستخدم موجود بالفعل!")
                else:
                    st.error("كلمات المرور غير متطابقة!")

elif st.session_state.current_page == "transactions":
    st.experimental_switch_page("pages/transactions.py")

elif st.session_state.current_page == "accounts":
    st.experimental_switch_page("pages/accounts.py")

elif st.session_state.current_page == "reports":
    st.experimental_switch_page("pages/reports.py")

elif st.session_state.current_page == "instructions":
    st.experimental_switch_page("pages/instructions.py")
