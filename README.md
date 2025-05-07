
# Fitbit Health Data Analyzer

## Overview

This project provides an interactive data analysis and visualization tool for Fitbit health data, originally collected from 30 users. It processes and combines multiple datasets to generate insights into users’ physical activity, sleep patterns, and calorie expenditure. The application allows for exploration of this data across different temporal resolutions (minute, hour, and day) through a Streamlit-based graphical user interface (GUI).

## Key Features

- **Data Combination:** Merges various Fitbit CSV files (activity, sleep, calories, etc.) into unified DataFrames for minute, hourly, and daily resolutions.
- **Interactive Filtering:** Allows users to dynamically filter the data by specific User ID and a selected time period.
- **Multi-Resolution Analysis:** Supports detailed analysis at minute-level, aggregated hourly trends, and daily summaries.
- **Rich Visualizations:** Generates interactive charts for key metrics, including:
  - Steps taken
  - Calories burned
  - Sleep duration
  - Activity intensity levels
  - METs (Metabolic Equivalents)
  - Daily activity distribution (sedentary, light, fair, very active minutes)
- **Summary Statistics:** Calculates and displays relevant statistics for the filtered data.

## How to Use the GUI

1. Ensure all dependencies are installed (see `requirements.txt`).
2. Place your Fitbit CSV data files into the `data/folder_1` and `data/folder_2` directories as per the project structure.
3. Run the Streamlit application from the root directory of the project:

   ```bash
   streamlit run ./src/main.py
   ```
4. Use the sidebar in the opened web application to select the data resolution, user ID, and date range for analysis. The visualizations and statistics will update automatically.

## Project Structure

**Fitbit_analysis/**
├── data/
│ ├── Folder_1/ # Directory for one set of CSV files (raw Fitbit data)
│ │ └── *.csv
│ └── Folder_2/ # Directory for another set of CSV files (if applicable)
│ └── *.csv
├── src/ # Python scripts for the application
│ ├── combine_data.py # Handles data loading, merging, and initial cleaning
│ ├── filter_data.py # Implements data filtering logic
│ ├── summary_statistics.py # Calculates summary metrics
│ ├── visualize_data.py # Streamlit GUI, plotting, and display logic
│ └── main.py # Entry point to launch the Streamlit application
├── requirements.txt # Python dependencies for the project
└── README.md # This project overview


## Data Requirements

For the application to function as intended (especially with error handling removed from the visualization script):

- The CSV files must be present in the specified `data/Folder_1` (and `data/Folder_2` if used) directories.
- The files should generally conform to the expected Fitbit data schema, containing necessary columns like 'Id', time-related columns ('ActivityMinute', 'ActivityHour', 'ActivityDate', etc.), and metric columns ('Steps', 'Calories', 'Intensity', 'TotalMinutesAsleep', etc.).
- The `combine_data.py` script is responsible for handling the initial merging; ensure it successfully creates `merged_data.minutes_df`, `merged_data.hourly_df`, and `merged_data.daily_df`.
