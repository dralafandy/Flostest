import streamlit as st

def show_navigation():
    """Display the horizontal navigation bar."""
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        if st.button("🏠 الرئيسية", key="nav_home"):
            st.session_state.current_page = "home"
            st.experimental_rerun()
    with col2:
        if st.button("📊 لوحة التحكم", key="nav_dashboard"):
            st.session_state.current_page = "dashboard"
            st.experimental_rerun()
    with col3:
        if st.button("💳 المعاملات", key="nav_transactions"):
            st.session_state.current_page = "transactions"
            st.experimental_rerun()
    with col4:
        if st.button("🏦 الحسابات", key="nav_accounts"):
            st.session_state.current_page = "accounts"
            st.experimental_rerun()
    with col5:
        if st.button("💰 الميزانيات", key="nav_budgets"):
            st.session_state.current_page = "budgets"
            st.experimental_rerun()
    with col6:
        if st.button("📈 التقارير", key="nav_reports"):
            st.session_state.current_page = "reports"
            st.experimental_rerun()
    with col7:
        if st.button("📚 التعليمات", key="nav_instructions"):
            st.session_state.current_page = "instructions"
            st.experimental_rerun()

def show_menu_button():
    """Display a button to switch back to the main menu."""
    if st.button("🔙 العودة إلى القائمة الرئيسية"):
        st.session_state.current_page = "home"
        st.experimental_rerun()
