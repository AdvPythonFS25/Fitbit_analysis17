# Copyright (c) 2025 Micael Moreira Lemos, Gilles Reichenbach, Tobias Aubert, Nicolas Stettler
# This software is licensed under the MIT License

import streamlit as st
import pandas as pd
from combine_data import merged_data
from summary_statistics import SummaryStatistics
from filter_data import DataFilter

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

    # Optional: Show filter panel
    with st.expander("🔍 Filter Data"):
        filter_enabled = st.checkbox("Enable filtering")

    if filter_enabled:
        data_filter = DataFilter(merged_data)

        freq = st.selectbox("Select Data Resolution", ["minutes", "hourly", "daily"])
        
        # Get available IDs across all merged DataFrames
        id_options = pd.concat([
            merged_data.minutes_df["Id"],
            merged_data.hourly_df["Id"],
            merged_data.dailyActivity_merged["Id"]
        ]).dropna().unique()

        selected_id = st.selectbox("Select User ID", ["All"] + sorted(id_options.astype(str).tolist()))

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
        with col2:
            end_date = st.date_input("End Date", value=pd.to_datetime("2020-12-31"))

        # Filter data
        start_time = pd.to_datetime(start_date)
        end_time = pd.to_datetime(end_date)

        if selected_id != "All":
            filtered_df = data_filter.filter_by_user_and_time(
                user_id=selected_id, start_time=start_time, end_time=end_time, freq=freq
            )
        else:
            filtered_df = data_filter.filter_by_time_range(
                start_time=start_time, end_time=end_time, freq=freq
            )

        st.subheader(f"Filtered {freq.capitalize()} Data")
        if not filtered_df.empty:
            st.dataframe(filtered_df.head(100))
        else:
            st.warning("No data matched your filter criteria.")

    # Optional: Show summary statistics
    with st.expander("📊 Summary Statistics"):
        if filter_enabled:
            summary = SummaryStatistics(filtered_df)

            stats = {
                "Total Steps": summary.total_steps(),
                "Average Daily Steps": summary.average_daily_steps(),
                "Total Sleep Duration (minutes)": summary.total_sleep_duration(),
                "Average Sleep Duration (minutes)": summary.average_sleep_duration(),
                "Average Calories per Hour": summary.average_calories_per_hour()
            }

            for label, value in stats.items():
                if value is not None:
                    st.write(f"{label}: {value:,.2f}")
        else:
            st.warning("Filtering is disabled. Summary statistics are not available.")

# Launch the app when this script is run directly
if __name__ == "__main__":
    run_app()
