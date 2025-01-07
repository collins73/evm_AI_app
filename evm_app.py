import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("Earned Value Management (EVM) Interactive App")

# Input: Project details
st.header("Enter the Project Details")

# User Inputs
project_name = st.text_input("Project Name", "Project A")
total_budget = st.number_input("Enter Total Budget (BAC) in USD", value=100000.0, step=1000.0)  # float value and step
planned_values = []
earned_values = []
actual_costs = []
months = ['Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5']

# Collect monthly data from the user
for i in range(5):
    planned_values.append(st.number_input(f"Planned Value for {months[i]} in USD", value=total_budget/5.0, step=1000.0))  # float value and step
    earned_values.append(st.number_input(f"Earned Value for {months[i]} in USD", value=total_budget/5.0, step=1000.0))  # float value and step
    actual_costs.append(st.number_input(f"Actual Cost for {months[i]} in USD", value=total_budget/5.0, step=1000.0))  # float value and step

# Create a DataFrame to hold the project data
df = pd.DataFrame({
    'Month': months,
    'Planned Value (PV)': planned_values,
    'Earned Value (EV)': earned_values,
    'Actual Cost (AC)': actual_costs
})

# Display the entered data
st.subheader("Project Data Overview")
st.write(df)

# Calculate EVM metrics
df['Cost Performance Index (CPI)'] = df['Earned Value (EV)'] / df['Actual Cost (AC)']
df['Schedule Performance Index (SPI)'] = df['Earned Value (EV)'] / df['Planned Value (PV)']
df['Cost Variance (CV)'] = df['Earned Value (EV)'] - df['Actual Cost (AC)']
df['Schedule Variance (SV)'] = df['Earned Value (EV)'] - df['Planned Value (PV)']

# Display the metrics
st.subheader("EVM Metrics Overview")
st.write(df)

# Plot the results for visualization
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['Month'], df['Planned Value (PV)'], label='Planned Value (PV)', marker='o')
ax.plot(df['Month'], df['Earned Value (EV)'], label='Earned Value (EV)', marker='o')
ax.plot(df['Month'], df['Actual Cost (AC)'], label='Actual Cost (AC)', marker='o')

ax.set_title(f"{project_name} - EVM Analysis")
ax.set_xlabel('Months')
ax.set_ylabel('Value in USD')
ax.legend()

# Show the plot in the Streamlit app
st.pyplot(fig)

# EAC and VAC calculations
EAC = total_budget / df['Cost Performance Index (CPI)'].mean()  # Estimate at Completion
VAC = total_budget - EAC  # Variance at Completion

st.subheader("Forecasting")
st.write(f"Estimate at Completion (EAC): ${EAC:,.2f}")
st.write(f"Variance at Completion (VAC): ${VAC:,.2f}")

# Notifications based on thresholds
if df['Cost Performance Index (CPI)'].mean() < 1:
    st.warning("The project is over budget (CPI < 1).")
else:
    st.success("The project is under budget (CPI >= 1).")

if df['Schedule Performance Index (SPI)'].mean() < 1:
    st.warning("The project is behind schedule (SPI < 1).")
else:
    st.success("The project is ahead of schedule (SPI >= 1).")
