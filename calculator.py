import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Function to calculate mortgage schedule
def calculate_mortgage_schedule(current_year, mortgage_owing, fortnightly_payment, annual_lump_sum, interest_rate):
    schedule = []
    year = 0
    actual_year = current_year
    while mortgage_owing > 0:
        year += 1
        actual_year += 1
        interest_paid = 0
        principal_paid = 0
        
        # Fortnightly payments for the year
        for _ in range(26):  # 26 fortnights in a year
            interest = mortgage_owing * (interest_rate / 100 / 26)
            principal = min(fortnightly_payment - interest, mortgage_owing)
            mortgage_owing -= principal
            interest_paid += interest
            principal_paid += principal
            if mortgage_owing <= 0:
                break
        
        # Annual lump sum
        if mortgage_owing > 0:
            lump_sum = min(annual_lump_sum, mortgage_owing)
            mortgage_owing -= lump_sum
            principal_paid += lump_sum
        
        schedule.append({
            "Year": year,
            "Actual Year": str(actual_year),  # No comma formatting, using plain string
            "Interest Paid": round(interest_paid, 0),
            "Principal Paid": round(principal_paid, 0),
            "Mortgage Balance": round(max(0, mortgage_owing), 0)
        })
    
    return pd.DataFrame(schedule)

# Streamlit app
st.title("Mortgage Calculator")

# Sidebar for user inputs
st.sidebar.header("Input Parameters")
current_year = st.sidebar.number_input("Current Year", value=2024, step=1)
mortgage_owing = st.sidebar.number_input("Mortgage Owing ($)", value=500000.0, step=10000.0)
fortnightly_payment = st.sidebar.number_input("Fortnightly Payment ($)", value=2000.0, step=100.0)
annual_lump_sum = st.sidebar.number_input("Annual Lump Sum Payment ($)", value=10000.0, step=1000.0)
interest_rate = st.sidebar.number_input("Interest Rate (%)", value=5.0, step=0.1)

# Calculate the schedule
schedule = calculate_mortgage_schedule(
    current_year=current_year,
    mortgage_owing=mortgage_owing,
    fortnightly_payment=fortnightly_payment,
    annual_lump_sum=annual_lump_sum,
    interest_rate=interest_rate
)

# Display results
st.header("Mortgage Repayment Schedule")
st.dataframe(schedule)  # Display the table

# Plot graph with two y-axes
fig = go.Figure()

# Mortgage Balance on primary y-axis
fig.add_trace(go.Scatter(
    x=schedule["Year"], 
    y=schedule["Mortgage Balance"], 
    mode='lines+markers', 
    name="Mortgage Balance",
    yaxis="y1"
))

# Principal Paid and Interest Paid on secondary y-axis
fig.add_trace(go.Bar(
    x=schedule["Year"], 
    y=schedule["Principal Paid"], 
    name="Principal Paid", 
    opacity=0.6,
    yaxis="y2"
))
fig.add_trace(go.Bar(
    x=schedule["Year"], 
    y=schedule["Interest Paid"], 
    name="Interest Paid", 
    opacity=0.6,
    yaxis="y2"
))

# Update layout to include secondary y-axis
fig.update_layout(
    title="Mortgage Repayment Over Time",
    xaxis=dict(title="Year"),
    yaxis=dict(
        title="Mortgage Balance ($)",
        titlefont=dict(color="blue"),
        tickfont=dict(color="blue")
    ),
    yaxis2=dict(
        title="Principal/Interest Paid ($)",
        titlefont=dict(color="red"),
        tickfont=dict(color="red"),
        overlaying="y",
        side="right"
    ),
    legend=dict(x=0.5, y=1.2, orientation="h"),
    barmode="stack"
)

st.plotly_chart(fig)