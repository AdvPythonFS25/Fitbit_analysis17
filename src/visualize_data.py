# Copyright (c) 2025 Micael Moreira Lemos, Gilles Reichenbach, Tobias Aubert, Nicolas Stettler
# This software is licensed under the MIT License

import streamlit as st
import pandas as pd
from combine_data import merged_data

# Configure the Streamlit page layout and title
st.set_page_config(
    page_title="CSV Data Resolutions Preview",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def run_app():
    """Main Streamlit app: displays column previews for each merged DataFrame."""
    st.title("Task 1 - Data Manipulation and Combination")
    st.write("Preview columns of each merged DataFrame at different resolutions.")

    # Define the DataFrames to show: attribute name in merged_data and a display title
    views = [
        ('minutes_df', "Minute-Level Data Columns"),
        ('hourly_df', "Hourly-Level Data Columns"),
        ('dailyActivity_merged', "Daily-Level Data Columns")
    ]

    # Loop through each view and display its columns + first few rows
    for attr, title in views:
        st.subheader(title)
        if hasattr(merged_data, attr):
            df = getattr(merged_data, attr)
            if not df.empty:
                st.write("Columns:", list(df.columns))
                # Show a small preview for context
                st.dataframe(df.head())
            else:
                st.warning(f"{title} DataFrame is empty.")
        else:
            st.warning(f"{title} DataFrame does not exist in merged_data.")

# Launch the app when this script is run directly
if __name__ == "__main__":
    run_app()
