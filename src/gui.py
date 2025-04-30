import streamlit as st
import pandas as pd
from combine_data import merged_data

# Configure Streamlit
st.set_page_config(
    page_title="CSV Data Resolutions Preview",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def add_time_delta(df: pd.DataFrame, time_col: str) -> pd.DataFrame:
    """
    Convert the specified time column to datetime and add a 'time_since_start' column.
    """
    if time_col in df.columns and not df.empty:
        df[time_col] = pd.to_datetime(df[time_col])
        start = df[time_col].iloc[0]
        df['time_since_start'] = df[time_col] - start
    return df

def run_app():
    st.title("Task 1 - Data Manipulation and Combination")
    st.write("Preview the head of each merged DataFrame at minute, hourly, and daily resolutions, with time since start.")

    views = [
        ('minutes_df', 'ActivityMinute', "Minute-Level Data Preview"),
        ('hourly_df', 'ActivityHour', "Hourly-Level Data Preview"),
        ('dailyActivity_merged', 'ActivityDate', "Daily-Level Data Preview")
    ]

    for attr, time_col, title in views:
        st.subheader(title)
        if hasattr(merged_data, attr):
            df = getattr(merged_data, attr).copy()
            if not df.empty:
                df = add_time_delta(df, time_col)
                st.dataframe(df.head())
            else:
                st.warning(f"{title} is empty.")
        else:
            st.warning(f"{title} attribute '{attr}' does not exist in merged_data.")

if __name__ == "__main__":
    run_app()
