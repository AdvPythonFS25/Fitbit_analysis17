import streamlit as st
import pandas as pd
from combine_data import merged_data

st.set_page_config(
    page_title="CSV Data Resolutions Preview",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def run_app():
    st.title("Task 1 - Data Manipulation and Combination")
    st.write("Preview columns of each merged DataFrame at different resolutions.")

    views = [
        ('minutes_df', "Minute-Level Data Columns"),
        ('hourly_df', "Hourly-Level Data Columns"),
        ('dailyActivity_merged', "Daily-Level Data Columns")
    ]

    for attr, title in views:
        st.subheader(title)
        if hasattr(merged_data, attr):
            df = getattr(merged_data, attr)
            if not df.empty:
                # Display the columns clearly
                st.write("Columns:", list(df.columns))
                # Also show a preview for context
                st.dataframe(df.head())
            else:
                st.warning(f"{title} DataFrame is empty.")
        else:
            st.warning(f"{title} DataFrame does not exist in merged_data.")

if __name__ == "__main__":
    run_app()
