# Copyright (c) 2025 Micael Moreira Lemos, Gilles Reichenbach, Tobias Aubert, Nicolas Stettler
# This software is licensed under the MIT License

"""visualize_data.py

Streamlit front-end for interactively filtering Fitbit data and showing both
summary numbers and time-series charts.

The module exposes a single public function ``run_app()`` so it can be imported
from ``main.py`` without causing Streamlit to execute on import elsewhere.
"""

import streamlit as st
import pandas as pd
from combine_data import merged_data 
from summary_statistics import SummaryStatistics
from filter_data import DataFilter

# Configure the Streamlit page layout and title
st.set_page_config(
    page_title="Fitbit Data Visualizer",
    layout="wide",
    initial_sidebar_state="expanded" 
)

def run_app():
    """Launch the Streamlit dashboard.

    The GUI consists of three vertical panes:

    1. **Sidebar** – resolution, user and date-range selectors  
    2. **Data preview** – up to 100 filtered rows (``st.dataframe``)  
    3. **Statistics & plots** – key metrics plus interactive charts
    """

    st.title("Fitbit Data Visualizer & Analyzer")
    st.write("Select data resolution, user, and time range from the sidebar to explore visualizations and statistics.")

    data_filter = DataFilter(merged_data)

    st.sidebar.header("Data Filters")
    
    freq_options = ["daily", "hourly", "minutes"] 
        
    freq = st.sidebar.selectbox("Select Data Resolution", freq_options, key="freq_select")
    
    id_options_list = []
    if "Id" in merged_data.minutes_df.columns:
        id_options_list.append(merged_data.minutes_df["Id"])
    if "Id" in merged_data.hourly_df.columns:
        id_options_list.append(merged_data.hourly_df["Id"])
    if "Id" in merged_data.daily_df.columns:
        id_options_list.append(merged_data.daily_df["Id"])
    
    all_ids_series = pd.concat(id_options_list).dropna().unique()

    try:
        if all(str(x).replace('.0','').isdigit() for x in all_ids_series):
                sorted_ids_str = sorted([str(int(float(x))) for x in all_ids_series])
        else:
            sorted_ids_str = sorted(map(str, all_ids_series))
    except ValueError: # Minimal fallback
        sorted_ids_str = sorted(map(str, all_ids_series))
    id_options_display = ["All"] + sorted_ids_str

    selected_id_str = st.sidebar.selectbox("Select User ID", id_options_display, key="user_id_select")
    
    min_date_val = pd.to_datetime("2010-01-01").date() 
    max_date_val = pd.to_datetime("2030-12-31").date() 

    current_df_for_dates = None
    time_col_for_dates = None

    if freq == "minutes":
        current_df_for_dates = data_filter.minutes_df
        time_col_for_dates = "ActivityMinute"
    elif freq == "hourly":
        current_df_for_dates = data_filter.hourly_df
        time_col_for_dates = "ActivityHour"
    elif freq == "daily":
        current_df_for_dates = data_filter.daily_df
        time_col_for_dates = "ActivityDate"
    

    date_times = pd.to_datetime(current_df_for_dates[time_col_for_dates], errors='coerce').dropna()
    if not date_times.empty: 
        min_date_val = date_times.min().date()
        max_date_val = date_times.max().date()

    start_date = st.sidebar.date_input("Start Date", value=min_date_val, min_value=min_date_val, max_value=max_date_val, key="start_date")
    end_date = st.sidebar.date_input("End Date", value=max_date_val, min_value=min_date_val, max_value=max_date_val, key="end_date")



    start_time = pd.to_datetime(start_date)
    end_time = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(nanoseconds=1)

    selected_id_typed = selected_id_str
    if selected_id_str != "All":
        example_df_for_id_type = None
        if freq == "daily": example_df_for_id_type = data_filter.daily_df
        elif freq == "hourly": example_df_for_id_type = data_filter.hourly_df
        elif freq == "minutes": example_df_for_id_type = data_filter.minutes_df
        
        id_dtype = example_df_for_id_type["Id"].dtype
        selected_id_typed = pd.Series(selected_id_str).astype(id_dtype).iloc[0]

    if selected_id_str != "All":
        filtered_df = data_filter.filter_by_user_and_time(
            user_id=selected_id_typed, start_time=start_time, end_time=end_time, freq=freq
        )
    else:
        filtered_df = data_filter.filter_by_time_range(
            start_time=start_time, end_time=end_time, freq=freq
        )


    st.subheader(f"Preview of Filtered {freq.capitalize()} Data (Max 100 Rows)")
    st.dataframe(filtered_df.head(100))
    
    st.markdown("---")
    st.subheader("Summary Statistics for Filtered Data")
    summary = SummaryStatistics(filtered_df)
    stats_values = {
        "Total Steps": summary.total_steps(),
        "Average Daily Steps (if daily data)": summary.average_daily_steps(),
        "Total Sleep Duration (minutes, if available)": summary.total_sleep_duration(),
        "Average Sleep Duration (minutes, if available)": summary.average_sleep_duration(),
        "Average Calories (per unit of freq, if available)": summary.average_calories_per_hour()
    }

    for label, value in stats_values.items():
        if value is not None: 
            if isinstance(value, float):
                st.write(f"{label}: {value:,.2f}")
            else:
                st.write(f"{label}: {value:,}")

    st.markdown("---") 
    st.subheader("Visualizations for Filtered Data")

    time_col_plot = None
    if freq == "daily": time_col_plot = "ActivityDate"
    elif freq == "hourly": time_col_plot = "ActivityHour"
    elif freq == "minutes": time_col_plot = "ActivityMinute"
    
    plot_df_copy = filtered_df.copy()
    plot_df_copy[time_col_plot] = pd.to_datetime(plot_df_copy[time_col_plot], errors='coerce')
    plot_df_copy = plot_df_copy.dropna(subset=[time_col_plot])


    
    def generate_line_chart(df, data_col_name, chart_title_suffix, y_axis_label_for_display):
        """Wrapper around :pyfunc:`st.line_chart` with common styling.

        Parameters
        ----------
        df : pandas.DataFrame
            Already filtered and properly time-indexed DataFrame.
        data_col_name : str
            Column to plot on the Y-axis.
        chart_title_suffix : str
            Text appended to the automatic title prefix.
        y_axis_label_for_display : str
            Human-readable label inserted into captions.
        """
        st.markdown(f"##### {freq.capitalize()} {chart_title_suffix}")
        
        series_for_plotting = df.set_index(time_col_plot)[data_col_name].sort_index()
        series_for_plotting = series_for_plotting[series_for_plotting.notna()] 

        if selected_id_str == "All" and "Id" in df.columns and df['Id'].nunique() > 1:
            aggregated_series = df.groupby(time_col_plot)[data_col_name].mean().sort_index()
            series_for_plotting = aggregated_series[aggregated_series.notna()] 
            st.caption(f"Showing average {y_axis_label_for_display.lower()} across all selected users per time point.")
        

        st.line_chart(series_for_plotting, use_container_width=True)
        st.caption(f"Y-axis represents: {y_axis_label_for_display}")

    if freq == "daily":
        generate_line_chart(plot_df_copy, "TotalSteps", "Total Steps", "Steps")
        generate_line_chart(plot_df_copy, "Calories", "Calories Burned", "Calories")
        generate_line_chart(plot_df_copy, "TotalMinutesAsleep", "Total Minutes Asleep", "Minutes Asleep")
        
        activity_cols_daily = ['VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes', 'SedentaryMinutes']

        st.markdown("##### Average Daily Activity Distribution (Minutes)")
        avg_activity_data = plot_df_copy[activity_cols_daily].mean().dropna() 
        st.bar_chart(avg_activity_data, use_container_width=True)

    elif freq == "hourly":
        generate_line_chart(plot_df_copy, "Calories", "Calories", "Calories")
        generate_line_chart(plot_df_copy, "StepTotal", "Steps", "Steps")
        generate_line_chart(plot_df_copy, "TotalIntensity", "Total Intensity", "Intensity")
    
    elif freq == "minutes":
        # Removed "too large" data warning
        generate_line_chart(plot_df_copy, "Steps", "Steps", "Steps")
        generate_line_chart(plot_df_copy, "Calories", "Calories", "Calories")
        generate_line_chart(plot_df_copy, "Intensity", "Intensity", "Intensity")
        if 'METs' in plot_df_copy.columns: # Keep this check for optional plot
            generate_line_chart(plot_df_copy, "METs", "METs", "METs")

if __name__ == "__main__":
    run_app()