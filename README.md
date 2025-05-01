# Fitbit analysis

## Overview

This project provides a data analysis and visualization tool for Fitbit health data collected from 30 users. The goal is to combine and process multiple datasets to generate insights into users’ physical activity, sleep patterns, and calorie expenditure over different temporal resolutions (minute, hour, and day).

## Recent Changes

- Streamlit GUI added for previewing combined DataFrames at different resolutions.
- Columns discrepancies across minute/hour/day resolutions clarified.

## Features

- Combines various Fitbit CSV files into a unified data frame
- Allows filtering by user and time period
- Offers interactive visualizations for steps, sleep, calories, and more
- Supports analysis at minute, hourly, and daily resolutions


## How to Use GUI

Run the Streamlit app with:

```bash
streamlit run main.py
```

## Structure

Fitbit analysis/

- ── data/folder_1 # CSV files (raw Fitbit data)
  - │──folder_2 # CSV files (raw Fitbit data)
- ── scripts/ # Python scripts
- │ ── combine_data.py # Data merging and cleaning
- │ ── filter_data.py # Filtering and statistics
- │ ── visualize_data.py # Visualization functions
- ── members.txt # Names of group members
- ── requirements.txt # Python dependencies
- ── README.md # Project overview
- ── main.py # Entry point to run the analysis
