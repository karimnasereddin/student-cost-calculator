import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#ALL STREAMLIT CODE FOR VISUALIZATIONS 
st.set_page_config(page_title="Student Cost of Living Calculator", page_icon="💸", layout="centered")

st.title("💸 Student Cost of Living Calculator")
st.caption("A simple budgeting tool that turns student expenses into clear insights.")

st.sidebar.header("Enter your yearly costs ($)")

#Sidebar visualizations for user input
tuition = st.sidebar.number_input("Tuition", min_value=0, value=8000, step=100)
housing = st.sidebar.number_input("Residence / Rent", min_value=0, value=12000, step=100)
food = st.sidebar.number_input("Food", min_value=0, value=3600, step=50)
transport = st.sidebar.number_input("Transportation", min_value=0, value=1200, step=50)
entertainment = st.sidebar.number_input("Entertainment", min_value=0, value=1000, step=50)
misc = st.sidebar.number_input("Miscellaneous", min_value=0, value=800, step=50)

st.sidebar.header("Income assumptions")
hourly_wage = st.sidebar.number_input("Hourly wage ($/hr)", min_value=0.0, value=17.0, step=0.5)
hours_per_week = st.sidebar.number_input("Hours/week you can work", min_value=0.0, value=12.0, step=1.0)
#Dataframe for visualizations and calculations using Pandas
data = {
    "Category": ["Tuition", "Housing", "Food", "Transport", "Entertainment", "Misc"],
    "Yearly Cost": [tuition, housing, food, transport, entertainment, misc]
}
df = pd.DataFrame(data)

#Allocating values to session state for use in the coach page
total_yearly = df["Yearly Cost"].sum()
monthly = total_yearly / 12
weekly = total_yearly / 52

monthly_income = hourly_wage * hours_per_week * 4.33  # avg weeks/month
yearly_income = monthly_income * 12

st.subheader("📌 Your totals")
col1, col2, col3 = st.columns(3)
col1.metric("Yearly", f"${total_yearly:,.0f}")
col2.metric("Monthly", f"${monthly:,.0f}")
col3.metric("Weekly", f"${weekly:,.0f}")

st.divider()

# Work hours needed
hours_needed_week = weekly / hourly_wage if hourly_wage > 0 else 0
st.subheader("⏱️ Work needed to cover costs")
st.write(f"At **${hourly_wage:.2f}/hr**, you’d need about **{hours_needed_week:.1f} hours/week** to break even.")

gap = yearly_income - total_yearly
if gap >= 0:
    st.success(f"✅ With {hours_per_week:.1f} hrs/week, you’re projected to be **+${gap:,.0f}/year** ahead.")
else:
    st.error(f"⚠️ With {hours_per_week:.1f} hrs/week, you’re projected to be **-${abs(gap):,.0f}/year** short.")

st.divider()

# --- Share results with other pages (Budget Coach) ---
st.session_state["df"] = df
st.session_state["total_yearly"] = total_yearly
st.session_state["monthly"] = monthly
st.session_state["weekly"] = weekly
st.session_state["hourly_wage"] = hourly_wage
st.session_state["hours_per_week"] = hours_per_week
st.session_state["monthly_income"] = monthly_income
st.session_state["yearly_income"] = yearly_income

# Visuals
st.subheader("📊 Where your money goes")
fig1, ax1 = plt.subplots()
ax1.pie(df["Yearly Cost"], labels=df["Category"], autopct="%1.0f%%")
ax1.set_title("Annual Cost Distribution")
st.pyplot(fig1)

st.subheader("📅 Monthly breakdown")
df_month = df.copy()
df_month["Monthly Cost"] = df_month["Yearly Cost"] / 12
df_month = df_month[["Category", "Monthly Cost"]].sort_values("Monthly Cost", ascending=False)

fig2, ax2 = plt.subplots()
ax2.bar(df_month["Category"], df_month["Monthly Cost"])
ax2.set_ylabel("$/month")
ax2.set_title("Monthly Costs by Category")
st.pyplot(fig2)

st.divider()

# The “scroll-stopping” insight
st.subheader("🔥 Reality Check Insight")
top_cat = df.loc[df["Yearly Cost"].idxmax(), "Category"]
top_pct = (df["Yearly Cost"].max() / total_yearly) * 100 if total_yearly > 0 else 0
# Uses df.loc to find the max value and what index value is associated with it, then uses that index to find the category. Also calculates the percentage of total yearly cost that this category represents.


st.info(f"**{top_cat}** is your biggest cost at **{top_pct:.0f}%** of your total yearly spending.")

# One smart what-if
st.subheader("🧪 What-if: Cut entertainment by $40/month")
save_year = 40 * 12
st.write(f"That saves **${save_year:,.0f}/year**, which is about **{save_year/hourly_wage:.1f} work hours** at ${hourly_wage:.2f}/hr." if hourly_wage > 0 else f"That saves **${save_year:,.0f}/year**.")