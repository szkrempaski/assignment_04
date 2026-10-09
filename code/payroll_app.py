import streamlit as st

from payroll import build_payroll, load_employees, load_timesheet, payroll_export

st.title("Salt City Coffee — Weekly Payroll")
st.write(
    "Upload this week's timesheet to see payroll "
    "and download the provider's file."
)
roster = load_employees()
upload = st.file_uploader("Timesheet CSV", type="csv", key="timesheet")

if upload is not None:
    timesheet = load_timesheet(upload)
    payroll = build_payroll(timesheet, roster)
    payroll_date = payroll["payroll_date"].iloc[0]

    unmatched = payroll[payroll["pay_type"] == "unmatched"]
    paid = payroll[payroll["pay_type"] != "unmatched"]
    overtime = payroll[payroll["pay_type"] == "overtime"]

    st.subheader(f"Pay period: {payroll_date}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Employees paid", len(paid))
    col2.metric("Total hours", f"{payroll['hours_worked'].sum():,.2f}")
    col3.metric("Total gross pay", f"${payroll['gross_pay'].sum():,.2f}")
    col4.metric("Overtime weeks", len(overtime))

    if len(unmatched) > 0:
        ids = ", ".join(unmatched["employee_id"])
        st.warning(f"Unmatched employee IDs (not in the roster, not paid): {ids}")
    else:
        st.success("Every employee on the timesheet matched the roster.")

    st.dataframe(payroll)

    st.download_button(
        "Download payroll CSV for the provider",
        data=payroll_export(payroll).to_csv(index=False),
        file_name=f"payroll_{payroll_date}.csv",
        mime="text/csv",
        key="download",
    )