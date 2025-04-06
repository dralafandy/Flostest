import streamlit as st
import pandas as pd
import plotly.express as px
from finance_manager import FinanceManager
from datetime import datetime
from mobile_styles import apply_mobile_styles

# Set page configuration
st.set_page_config(page_title="FloosAfandy - لوحة التحكم", layout="wide", initial_sidebar_state="collapsed")

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

apply_mobile_styles()

# Horizontal navigation bar
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

# Check if user is logged in
if not st.session_state.logged_in:
    st.error("يرجى تسجيل الدخول أولاً من الصفحة الرئيسية!")
    st.session_state.current_page = "home"
    st.experimental_rerun()
else:
    fm = FinanceManager(st.session_state.user_id)

    st.markdown(
        f'<div style="display: flex; justify-content: center; margin: 20px 0;">'
        f'<img src="https://i.ibb.co/KpzDy27r/IMG-2998.png" width="300">'
        f'</div>',
        unsafe_allow_html=True
    )  # Centered Welcome Banner
    st.markdown(f"""
        <div style="background-color: #0066cc; color: white; padding: 15px; border-radius: 10px; text-align: center;">
            <h1>مرحبًا بك في لوحة التحكم، {st.session_state.user_id}!</h1>
            <p>اليوم هو {datetime.now().strftime('%A, %d %B %Y')}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Key Metrics Section
    st.subheader("📊 نظرة عامة")
    accounts = fm.get_all_accounts()
    transactions = fm.get_all_transactions()

    if accounts:
        total_balance = sum(acc[3] for acc in accounts)
        income = sum(trans[4] for trans in transactions if trans[3] == "IN")
        expenses = sum(trans[4] for trans in transactions if trans[3] == "OUT")
        net_balance = income - expenses

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 إجمالي الرصيد", f"{total_balance:,.2f} جنيه")
        with col2:
            st.metric("📥 إجمالي الوارد", f"{income:,.2f} جنيه")
        with col3:
            st.metric("📤 إجمالي المصروفات", f"{expenses:,.2f} جنيه")
        with col4:
            st.metric("📊 صافي الرصيد", f"{net_balance:,.2f} جنيه")
    else:
        st.info("ℹ️ لا توجد حسابات مسجلة.")

    st.markdown("---")

    # Alerts Section
    st.subheader("🚨 التنبيهات")
    alerts = fm.check_alerts()
    if alerts:
        st.warning(alerts)
    else:
        st.success("✅ لا توجد تنبيهات حالياً.")

    st.markdown("---")

    # Visualizations Section
    st.subheader("📈 التحليل المالي")
    if transactions:
        df = pd.DataFrame(transactions, columns=["id", "user_id", "date", "type", "amount", "account_id", "description", "payment_method", "category"])
        df["date"] = pd.to_datetime(df["date"])
        df["type"] = df["type"].replace({"IN": "وارد", "OUT": "منصرف"})

        # Line Chart for Income and Expenses
        fig = px.line(df, x="date", y="amount", color="type", title="الوارد مقابل المصروفات بمرور الوقت", labels={"amount": "المبلغ", "date": "التاريخ"})
        st.plotly_chart(fig, use_container_width=True)

        # Pie Chart for Categories
        category_summary = df.groupby("category")["amount"].sum().reset_index()
        fig_pie = px.pie(category_summary, values="amount", names="category", title="توزيع المصروفات حسب الفئات", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("ℹ️ لا توجد بيانات كافية لعرض التحليل المالي.")

    st.markdown("---")

    # Recent Transactions Section
    st.subheader("🕒 الأنشطة الأخيرة")
    if transactions:
        recent_transactions = pd.DataFrame(transactions, columns=["id", "user_id", "date", "type", "amount", "account_id", "description", "payment_method", "category"]).tail(5)
        recent_transactions["date"] = pd.to_datetime(recent_transactions["date"])
        recent_transactions["type"] = recent_transactions["type"].replace({"IN": "وارد", "OUT": "منصرف"})
        st.table(recent_transactions[["date", "type", "amount", "description", "category"]])
    else:
        st.info("ℹ️ لا توجد معاملات مسجلة.")

    st.markdown("---")

    # Top Categories Section
    st.subheader("📂 أعلى الفئات")
    if transactions:
        with st.expander("عرض أعلى الفئات"):
            top_categories = df.groupby("category")["amount"].sum().nlargest(5).reset_index()
            st.table(top_categories.rename(columns={"category": "الفئة", "amount": "المبلغ"}))
    else:
        st.info("ℹ️ لا توجد بيانات كافية لعرض الفئات.")
