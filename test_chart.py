import pandas as pd
import streamlit as st

df = pd.DataFrame({
    "Fuel Type": ["Petrol", "Diesel"],
    "Avg Price (₹)": [300000, 400000],
    "Median Price (₹)": [280000, 390000]
})

st.bar_chart(
    df,
    x="Fuel Type", y=["Avg Price (₹)", "Median Price (₹)"],
    color=["#FF6B35", "#6C63FF"]
)
