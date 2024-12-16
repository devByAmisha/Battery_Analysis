import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# Ensure Plotly is in offline mode and renders in the browser
pio.renderers.default = "browser"

# Load the dataset
file_path = "metadata.csv"  # Update the file path if necessary
data = pd.read_csv("metadata.csv")

# Clean column names (remove any extra spaces)
data.columns = data.columns.str.strip()

# Check missing values in 'Re' and 'Rct' columns
print("Missing values in 'Re' and 'Rct' columns before conversion:")
print(data[['Re', 'Rct']].isnull().sum())

# Convert 'Re' and 'Rct' columns to numeric (handle non-numeric values by setting them to NaN)
data['Re'] = pd.to_numeric(data['Re'], errors='coerce')
data['Rct'] = pd.to_numeric(data['Rct'], errors='coerce')

# Check missing values after conversion
print("\nMissing values in 'Re' and 'Rct' columns after conversion:")
print(data[['Re', 'Rct']].isnull().sum())

# Drop rows with NaN values in 'Re' or 'Rct' columns
data = data.dropna(subset=['Re', 'Rct'])

# Create 'Cycle' column as a sequential index starting from 0
data['Cycle'] = range(len(data))

# Check the number of rows and data sample for 'Re' and 'Rct'
print("\nNumber of rows after cleaning:")
print(f"Rows after cleaning: {len(data)}")

print("\nData Sample after conversion (First 5 Rows):")
print(data[['Cycle', 'Re', 'Rct']].head(5))

# Verify the 'Rct' column specifically for valid values
print("\nSummary of 'Rct' column:")
print(data['Rct'].describe())  # This will show min, max, and other stats

# Plot Battery Impedance vs. Aging Cycles (First Plot)
if 'Re' in data.columns and data['Re'].notnull().any():
    fig1 = px.line(data, x='Cycle', y='Re', 
                   title='Battery Impedance vs. Aging Cycles', 
                   labels={'Cycle': 'Aging Cycles', 'Re': 'Battery Impedance (Ohms)'})
    fig1.show()
else:
    print("No valid 'Re' data found for plotting.")

# Plot Charge Transfer Resistance vs. Aging Cycles (Second Plot)
if 'Rct' in data.columns and data['Rct'].notnull().any():
    fig2 = px.line(data, x='Cycle', y='Rct', 
                   title='Charge Transfer Resistance vs. Aging Cycles', 
                   labels={'Cycle': 'Aging Cycles', 'Rct': 'Charge Transfer Resistance (Ohms)'})
    fig2.show()
else:
    print("No valid 'Rct' data found for plotting.")

# Combined Plot: Battery Impedance and Charge Transfer Resistance
if 'Re' in data.columns and 'Rct' in data.columns and data['Re'].notnull().any() and data['Rct'].notnull().any():
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=data['Cycle'], y=data['Re'], mode='lines', name='Battery Impedance'))
    fig3.add_trace(go.Scatter(x=data['Cycle'], y=data['Rct'], mode='lines', name='Charge Transfer Resistance'))

    fig3.update_layout(
        title='Battery Parameters vs. Aging Cycles',
        xaxis_title='Aging Cycles',
        yaxis_title='Resistance (Ohms)',
        legend_title='Parameters'
    )
    fig3.show()
else:
    print("No valid data found for either 'Re' or 'Rct'.")
