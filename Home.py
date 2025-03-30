import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page setup
st.set_page_config(page_title="Solar Power Plant Dashboard", layout="wide")

# === Title and Intro ===
st.title("☀️ Solar Power Plant: Financial Dashboard")
st.markdown("Get a quick overview of project revenue, costs, debt, and return metrics for your solar investment.")

# === Sidebar Inputs ===
st.sidebar.header("📊 Input Parameters")

# --- Revenue Inputs ---
st.sidebar.subheader("💰 Revenues")
average_production_per_mw_day = st.sidebar.slider(
    'Average Production per MW per Day (kWh)',
    min_value=0.0, max_value=7000.0, value=5500.0, step=10.0
)
rate_per_unit = st.sidebar.slider(
    'Rate per Unit (₹)', min_value=2.0, max_value=5.0, value=3.11, step=0.01
)
total_mw = st.sidebar.slider(
    'Number of MW Production', min_value=1, max_value=25, value=8, step=1, key="total_mw"
)

# --- Cost Inputs ---
st.sidebar.subheader("🧾 Working Costs")
labor_cost = st.sidebar.slider(
    'Labor Cost per month (₹)', min_value=100000, max_value=1000000, value=250000, step=1000
)
electricity_cost = st.sidebar.slider(
    'Electricity Cost per month (₹)', min_value=5000, max_value=50000, value=20000, step=500
)

# --- Debt Inputs ---
st.sidebar.subheader("🏦 Debt")
cost_per_mw = st.sidebar.slider(
    'Cost per MW (₹)', min_value=35000000, max_value=50000000, value=35000000, step=1000000
)
debt_percent = st.sidebar.slider(
    "Debt Percentage of Total Cost (%)", min_value=0, max_value=100, value=80
)
interest_rate = st.sidebar.slider(
    "Annual Interest Rate (%)", min_value=1.0, max_value=20.0, value=10.0, step=0.1
)
loan_term_years = st.sidebar.slider(
    "Loan Payoff Period (Years)", min_value=1, max_value=30, value=25
)

# === Revenue Calculations ===
revenue_per_day = average_production_per_mw_day * rate_per_unit * total_mw
revenue_per_year = revenue_per_day * 365
revenue_per_month = revenue_per_year / 12

# === Cost Calculations ===
working_cost_monthly = labor_cost + electricity_cost
working_cost_annual = working_cost_monthly * 12

# === Capital & Loan Calculations ===
total_cost = total_mw * cost_per_mw
loan_amount = total_cost * (debt_percent / 100)
annual_interest_rate = interest_rate / 100
n_years = loan_term_years

# Loan payment calculation
if annual_interest_rate > 0:
    annual_payment = (loan_amount * annual_interest_rate) / (1 - (1 + annual_interest_rate) ** -n_years)
else:
    annual_payment = loan_amount / n_years

monthly_payment = annual_payment / 12

# === Income ===
monthly_income = revenue_per_month - (working_cost_monthly + monthly_payment)
annual_income = revenue_per_year - (working_cost_annual + annual_payment)

# === ROI and IRR ===
roi = (annual_income / total_cost) * 100 if total_cost else 0
cash_flows = [-total_cost] + [annual_income] * n_years


# === Cumulative Cash Flow for Graphs ===
cumulative_cash_flow = pd.Series(cash_flows).cumsum()
years = list(range(n_years + 1))

# === Section 1: Revenue ===
st.divider()
st.subheader("💰 Revenue Summary")
revenue_cols = st.columns(2)
revenue_cols[0].metric(label="Monthly Revenue", value=f"₹{revenue_per_month:,.0f}")
revenue_cols[1].metric(label="Annual Revenue", value=f"₹{revenue_per_year:,.0f}")

# === Section 2: Working Costs ===
st.divider()
st.subheader("🧾 Working Cost Summary")
cost_cols = st.columns(2)
cost_cols[0].metric(label="Monthly Working Cost", value=f"₹{working_cost_monthly:,.0f}")
cost_cols[1].metric(label="Annual Working Cost", value=f"₹{working_cost_annual:,.0f}")

# === Section 3: Capital & Loan ===
st.divider()
st.subheader("🏗️ Capital & Loan Breakdown")
capital_cols = st.columns(3)
capital_cols[0].metric(label="Total Project Cost", value=f"₹{total_cost:,.0f}")
capital_cols[1].metric(label="Loan Amount", value=f"₹{loan_amount:,.0f}")
capital_cols[2].metric(label="Debt Percentage", value=f"{debt_percent}%")

repay_cols = st.columns(2)
repay_cols[0].metric(label="Annual Loan Payment", value=f"₹{annual_payment:,.0f}")
repay_cols[1].metric(label="Monthly Loan Payment", value=f"₹{monthly_payment:,.0f}")

# === Section 4: Net Income ===
st.divider()
st.subheader("💼 Net Income Summary")
income_cols = st.columns(2)
income_cols[0].metric(label="Monthly Net Income", value=f"₹{monthly_income:,.0f}")
income_cols[1].metric(label="Annual Net Income", value=f"₹{annual_income:,.0f}")

# === Section 5: ROI and IRR ===
st.divider()
st.subheader("📈 Project Returns")
roi_cols = st.columns(2)
roi_cols[0].metric(label="ROI (%)", value=f"{roi:.2f}%")

# === Section 6: Visual – Revenue vs Cost ===
st.divider()
st.subheader("📉 Annual Revenue vs Total Costs")

# Plotly Bar Chart
fig = go.Figure()
fig.add_trace(go.Bar(
    x=["Annual Revenue"],
    y=[revenue_per_year],
    name="Revenue",
    marker_color='green',
    text=[f'₹{revenue_per_year:,.0f}'],
    textposition='outside'
))
fig.add_trace(go.Bar(
    x=["Annual Costs"],
    y=[working_cost_annual + annual_payment],
    name="Costs",
    marker_color='red',
    text=[f'₹{working_cost_annual + annual_payment:,.0f}'],
    textposition='outside'
))
fig.update_layout(
    title="Annual Revenue vs Total Annual Costs",
    xaxis_title="",
    yaxis_title="Amount (₹)",
    showlegend=False,
    height=500,
    plot_bgcolor='white',
    yaxis=dict(gridcolor='lightgrey'),
    font=dict(size=14)
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

st.title("📈 Land Cost vs Size of Solar Project")


cost_per_acre = st.slider("Cost of Land per Acre (₹)", 1500000, 4000000, 1500000, step=50000)

# Range of project sizes
mw_range = list(range(1, 31))  # 1 MW to 30 MW
land_costs = [mw * 4 * cost_per_acre for mw in mw_range]

# Plotly Chart
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=mw_range,
    y=land_costs,
    mode='lines+markers',
    name='Land Cost',
    line=dict(color='darkblue', width=3),
    marker=dict(size=6),
    hovertemplate='Size: %{x} MW<br>Land Cost: ₹%{y:,.0f}'
))

fig.update_layout(
    title="🧮 Estimated Land Cost vs Project Size (MW)",
    xaxis_title="Project Size (MW)",
    yaxis_title="Total Land Cost (₹)",
    plot_bgcolor="white",
    height=500,
    yaxis=dict(gridcolor="lightgrey"),
    font=dict(size=14)
)

st.plotly_chart(fig, use_container_width=True)

land_factored_cost = total_cost + (4 * cost_per_acre * total_mw)
after_loan_cost = land_factored_cost - loan_amount
land_cols = st.columns(3)

land_cols[0].metric(label="Total Cost of Project with Land Factor", value=f"₹{land_factored_cost:,.0f}")
land_cols[1].metric(label="Total Cost of Project after Loan", value=f"₹{after_loan_cost:,.0f}")

# === Section 7: Efficiency Loss ===


