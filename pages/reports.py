import streamlit as st
import pandas as pd
import plotly.express as px
from finance_manager import FinanceManager
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
from mobile_styles import apply_mobile_styles

# Set page configuration
st.set_page_config(page_title="FloosAfandy - التقارير", layout="wide", initial_sidebar_state="collapsed")

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

    st.title("📊 التقارير المالية")
    st.markdown("<p style='color: #6b7280;'>احصل على رؤية شاملة لأدائك المالي من خلال التقارير التفصيلية.</p>", unsafe_allow_html=True)
    st.markdown("---")

    accounts = fm.get_all_accounts()
    account_options = {acc[0]: acc[2] for acc in accounts}

    st.markdown("""
        <style>
        .filter-box {background-color: #e5e7eb; padding: 15px; border-radius: 10px; margin-bottom: 15px;}
        .metric-box {padding: 20px; border-radius: 10px; color: #1A2525;}
        </style>
    """, unsafe_allow_html=True)

    st.subheader("⚙️ فلاتر التقرير")
    with st.container():
        st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            account_id = st.selectbox("🏦 الحساب", ["جميع الحسابات"] + list(account_options.keys()), 
                                      format_func=lambda x: "جميع الحسابات" if x == "جميع الحسابات" else account_options[x])
        with col_f2:
            trans_type = st.selectbox("📋 النوع", ["الكل", "وارد", "منصرف"])
        with col_f3:
            category = st.selectbox("📂 الفئة", ["الكل"] + [cat[0] for cat in fm.get_custom_categories(account_id, "IN" if trans_type == "وارد" else "OUT")] if trans_type != "الكل" and account_id != "جميع الحسابات" else ["الكل"])
        col_f4, col_f5, col_f6 = st.columns(3)
        with col_f4:
            start_date = st.date_input("📅 من", value=None)
        with col_f5:
            end_date = st.date_input("📅 إلى", value=None)
        with col_f6:
            compare_period = st.selectbox("📅 مقارنة بـ", ["لا مقارنة", "الشهر الماضي"])
        st.markdown("</div>", unsafe_allow_html=True)

    start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S") if start_date else None
    end_date_str = end_date.strftime("%Y-%m-%d %H:%M:%S") if end_date else None
    transactions = fm.filter_transactions(
        account_id=account_id if account_id != "جميع الحسابات" else None,
        start_date=start_date_str,
        end_date=end_date_str,
        trans_type="IN" if trans_type == "وارد" else "OUT" if trans_type == "منصرف" else None,
        category=category if category != "الكل" else None
    )
    df = pd.DataFrame(transactions, columns=["id", "user_id", "date", "type", "amount", "account_id", "description", "payment_method", "category"]) if transactions else pd.DataFrame()

    if compare_period == "الشهر الماضي":
        last_month_start = (date.today() - relativedelta(months=1)).replace(day=1)
        last_month_end = (date.today() - relativedelta(months=1) + relativedelta(days=31)).replace(day=1) - timedelta(days=1)
        last_month_start_str = last_month_start.strftime("%Y-%m-%d %H:%M:%S")
        last_month_end_str = last_month_end.strftime("%Y-%m-%d %H:%M:%S")
        transactions_last = fm.filter_transactions(
            account_id=account_id if account_id != "جميع الحسابات" else None,
            start_date=last_month_start_str,
            end_date=last_month_end_str,
            trans_type="IN" if trans_type == "وارد" else "OUT" if trans_type == "منصرف" else None,
            category=category if category != "الكل" else None
        )
        df_last = pd.DataFrame(transactions_last, columns=["id", "user_id", "date", "type", "amount", "account_id", "description", "payment_method", "category"]) if transactions_last else pd.DataFrame()
    else:
        df_last = pd.DataFrame()

    if not df.empty:
        income = df[df["type"] == "IN"]["amount"].sum()
        expenses = df[df["type"] == "OUT"]["amount"].sum()
        net = income - expenses
        trans_count = len(df)
    else:
        income, expenses, net, trans_count = 0, 0, 0, 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='metric-box' style='background: linear-gradient(#86efac, #22c55e);'>", unsafe_allow_html=True)
        st.metric("📥 الوارد", f"{income:,.2f} جنيه")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-box' style='background: linear-gradient(#f87171, #ef4444); color: #ffffff;'>", unsafe_allow_html=True)
        st.metric("📤 الصادر", f"{expenses:,.2f} جنيه")
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-box' style='background: linear-gradient(#60a5fa, #3b82f6); color: #ffffff;'>", unsafe_allow_html=True)
        st.metric("📊 الصافي", f"{net:,.2f} جنيه")
        st.markdown("</div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='metric-box' style='background: linear-gradient(#d1d5db, #9ca3af);'>", unsafe_allow_html=True)
        st.metric("📋 عدد المعاملات", f"{trans_count}")
        st.markdown("</div>", unsafe_allow_html=True)

    if compare_period == "الشهر الماضي" and not df.empty and not df_last.empty:
        income_last = df_last[df_last["type"] == "IN"]["amount"].sum()
        expenses_last = df_last[df_last["type"] == "OUT"]["amount"].sum()
        net_last = income_last - expenses_last
        income_change = ((income - income_last) / income_last * 100) if income_last > 0 else 0
        expenses_change = ((expenses - expenses_last) / expenses_last * 100) if expenses_last > 0 else 0
        st.markdown("<h3 style='color: #1A2525;'>📝 ملخص التقرير</h3>", unsafe_allow_html=True)
        st.write(f"- الوارد: {'ارتفع' if income_change > 0 else 'انخفض'} بنسبة {abs(income_change):.1f}% مقارنة بالشهر الماضي.")
        st.write(f"- الصادر: {'ارتفع' if expenses_change > 0 else 'انخفض'} بنسبة {abs(expenses_change):.1f}% مقارنة بالشهر الماضي.")
        st.write(f"- الصافي السابق: {net_last:,.2f}")

    st.subheader("📋 جدول المعاملات")
    if not df.empty:
        df["type"] = df["type"].replace({"IN": "وارد", "OUT": "منصرف"})
        df["account"] = df["account_id"].map(account_options)
        visible_columns = st.multiselect("📊 الأعمدة المرئية", df.columns.tolist(), default=["id", "date", "type", "amount", "account", "category"])
        st.dataframe(df[visible_columns], use_container_width=True, height=300)
        col1, col2 = st.columns(2)
        with col1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("💾 تحميل CSV", csv, "report.csv", "text/csv", use_container_width=True)
        with col2:
            st.button("📑 تصدير PDF", disabled=True, help="قيد التطوير", use_container_width=True)
    else:
        st.info("ℹ️ لا توجد معاملات تطابق الفلاتر.")

    st.subheader("📂 أعلى 5 فئات")
    if not df.empty:
        df_expanded = df.assign(category=df["category"].str.split(", ")).explode("category")
        category_summary = df_expanded.groupby("category")["amount"].sum().nlargest(5).reset_index()
        st.table(category_summary.rename(columns={"category": "الفئة", "amount": "المبلغ"}))
    else:
        st.write("لا توجد فئات لعرضها.")

    st.subheader("📈 تحليل بياني")
    if not df.empty:
        col1, col2 = st.columns([1, 1])
        with col1:
            fig = px.bar(df, x="date", y="amount", color="type", title="المعاملات بمرور الوقت", 
                         color_discrete_map={"وارد": "#22c55e", "منصرف": "#ef4444"}, height=300)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig_pie = px.pie(category_summary, values="amount", names="category", title="توزيع حسب الفئات", 
                             color_discrete_sequence=px.colors.qualitative.Pastel, height=300)
            st.plotly_chart(fig_pie, use_container_width=True)
