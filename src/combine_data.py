# Copyright (c) 2025 Micael Moreira Lemos, Gilles Reichenbach, Tobias Aubert, Nicolas Stettler	
# This software is licensed under the MIT License
'''
Utilities for loading raw Fitbit CSV exports from two folders, merging them
minute-, hour- and day-wise, and exposing the results as convenient attributes.
'''

import pandas as pd
import os

class CSVData:
    """Load **all** CSV files in a folder into attributes of the instance.

    Each file becomes a ``pandas.DataFrame`` attribute whose name is the
    file-stem with spaces and dashes converted to underscores.

    Parameters
    ----------
    folder_path : str | os.PathLike
        Path to a directory that contains Fitbit CSV exports.

    Attributes
    ----------
    <file_stem> : pandas.DataFrame
        One attribute per CSV discovered. The attribute name equals the
        filename without extension, with illegal identifier characters
        replaced.

    Notes
    -----
    The constructor never raises; it prints a message if a CSV cannot be read.
    """
    def __init__(self, folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                var_name = os.path.splitext(filename)[0].replace(" ", "_").replace("-", "_")
                try:
                    df = pd.read_csv(os.path.join(folder_path, filename))
                    setattr(self, var_name, df)
                except Exception as e:
                    print(f"Error reading {filename}: {e}")


# Usage
folder_path = "data/Folder_1"
data_1 = CSVData(folder_path)

folder_path = "data/Folder_2"
data_2 = CSVData(folder_path)


class MergedData:
    """Container that holds union-merged DataFrames from two :class:`CSVData`
    loaders.

    The constructor:

    1. Collects the set-union of DataFrame-bearing attributes from *both*
       ``data_1`` and ``data_2``.
    2. For every common attribute, concatenates the two frames row-wise
       (``pd.concat``). If an attribute exists in only one source it is copied
       as-is.
    3. Builds three convenience attributes — ``minutes_df``, ``hourly_df``,
       ``daily_df`` — already deduplicated, dtype-fixed and timestamp-parsed.

    Parameters
    ----------
    data_1, data_2 : CSVData
        Two loaders representing separate export folders.

    Attributes
    ----------
    <attr> : pandas.DataFrame
        All merged per-file frames.
    minutes_df, hourly_df, daily_df : pandas.DataFrame
        Ready-to-use time-aligned master tables at the respective resolutions.
    """
    def __init__(self, data_1, data_2):
        # Collect all attribute names from both data_1 and data_2 that are DataFrames
        attrs_data1 = {attr for attr in dir(data_1) if not attr.startswith("_") and isinstance(getattr(data_1, attr), pd.DataFrame)}
        attrs_data2 = {attr for attr in dir(data_2) if not attr.startswith("_") and isinstance(getattr(data_2, attr), pd.DataFrame)}
        all_attrs = attrs_data1.union(attrs_data2)

        for attr in all_attrs:
            df1 = getattr(data_1, attr, None)
            df2 = getattr(data_2, attr, None)

            # Print header for df1 if it exists
            if isinstance(df1, pd.DataFrame):
                print(f"Data from {attr} (Folder_1):")
                print(df1.head())
            
            # Concatenate if both exist, otherwise use the one that exists
            if isinstance(df1, pd.DataFrame) and isinstance(df2, pd.DataFrame):
                merged_df = pd.concat([df1, df2], ignore_index=True)
                # print(f"Merged {attr} from Folder_1 and Folder_2.")
            elif isinstance(df1, pd.DataFrame):
                merged_df = df1
                # print(f"Using {attr} from Folder_1 (not found in Folder_2).")
            elif isinstance(df2, pd.DataFrame):
                merged_df = df2
                # print(f"Using {attr} from Folder_2 (not found in Folder_1).")
            else:
                # This case should ideally not happen if attr was found in all_attrs
                continue 
            
            setattr(self, attr, merged_df)

merged_data = MergedData(data_1, data_2)


'''

Here we merge all data that is stored by every minute.

'''
if hasattr(merged_data, 'minuteCaloriesNarrow_merged') and \
   hasattr(merged_data, 'minuteIntensitiesNarrow_merged') and \
   hasattr(merged_data, 'minuteMETsNarrow_merged') and \
   hasattr(merged_data, 'minuteStepsNarrow_merged'):

    merged_data.minuteCaloriesNarrow_merged = merged_data.minuteCaloriesNarrow_merged.drop_duplicates(subset=["Id", "ActivityMinute"])
    merged_data.minuteIntensitiesNarrow_merged = merged_data.minuteIntensitiesNarrow_merged.drop_duplicates(subset=["Id", "ActivityMinute"])
    merged_data.minuteMETsNarrow_merged = merged_data.minuteMETsNarrow_merged.drop_duplicates(subset=["Id", "ActivityMinute"])
    merged_data.minuteStepsNarrow_merged = merged_data.minuteStepsNarrow_merged.drop_duplicates(subset=["Id", "ActivityMinute"])
    
    minutes_df_list = [
        merged_data.minuteCaloriesNarrow_merged,
        merged_data.minuteIntensitiesNarrow_merged,
        merged_data.minuteMETsNarrow_merged,
        merged_data.minuteStepsNarrow_merged
    ]
    
    # Base merge for the primary minute data
    merged_data.minutes_df = minutes_df_list[0]
    for df_to_merge in minutes_df_list[1:]:
        merged_data.minutes_df = pd.merge(merged_data.minutes_df, df_to_merge, on=["Id", "ActivityMinute"], how="outer")

    if hasattr(merged_data, 'minuteSleep_merged'):
        merged_data.minuteSleep_merged = merged_data.minuteSleep_merged.drop_duplicates(subset=["Id", "date"])
        merged_data.minutes_df = pd.merge(merged_data.minutes_df, merged_data.minuteSleep_merged, left_on=["Id", "ActivityMinute"], right_on=["Id", "date"], how="outer")
        # Update ActivityMinute with values from date where ActivityMinute is missing
        merged_data.minutes_df["ActivityMinute"] = merged_data.minutes_df["ActivityMinute"].combine_first(merged_data.minutes_df["date"])
        # Drop the date column
        merged_data.minutes_df = merged_data.minutes_df.drop(columns=["date"])
    else:
        print("Info: minuteSleep_merged not found. Proceeding without minute-level sleep data.")

    merged_data.minutes_df["ActivityMinute"] = pd.to_datetime(merged_data.minutes_df["ActivityMinute"], format="%m/%d/%Y %I:%M:%S %p", errors='coerce')
    merged_data.minutes_df.dropna(subset=['ActivityMinute'], inplace=True) # Clean up if parse failed

    print("\n--- merged_data.minutes_df ---")
    print(merged_data.minutes_df.head())
else:
    print("Warning: One or more core minute-level narrow dataframes are missing. Cannot create minutes_df.")
    merged_data.minutes_df = pd.DataFrame() # Create an empty DataFrame

'''

Here we merge all data that is stored hourly.

'''
if hasattr(merged_data, 'hourlyCalories_merged') and \
   hasattr(merged_data, 'hourlyIntensities_merged') and \
   hasattr(merged_data, 'hourlySteps_merged'):

    merged_data.hourlyCalories_merged = merged_data.hourlyCalories_merged.drop_duplicates(subset=["Id", "ActivityHour"])
    merged_data.hourlyIntensities_merged = merged_data.hourlyIntensities_merged.drop_duplicates(subset=["Id", "ActivityHour"])
    merged_data.hourlySteps_merged = merged_data.hourlySteps_merged.drop_duplicates(subset=["Id", "ActivityHour"])

    merged_data.hourly_df = pd.merge(merged_data.hourlyCalories_merged, merged_data.hourlyIntensities_merged, on=["Id", "ActivityHour"], how="inner")
    merged_data.hourly_df = pd.merge(merged_data.hourly_df, merged_data.hourlySteps_merged, on=["Id", "ActivityHour"], how="inner")

    merged_data.hourly_df["ActivityHour"] = pd.to_datetime(merged_data.hourly_df["ActivityHour"], format="%m/%d/%Y %I:%M:%S %p", errors='coerce')
    merged_data.hourly_df.dropna(subset=['ActivityHour'], inplace=True)

    print("\n--- merged_data.hourly_df ---")
    print(merged_data.hourly_df.head())
else:
    print("Warning: One or more core hourly-level dataframes are missing. Cannot create hourly_df.")
    merged_data.hourly_df = pd.DataFrame() # Create an empty DataFrame


'''

Here we merge all data that is stored daily.

'''

# Process dailyActivity_merged first, as it's a primary daily file.
if hasattr(merged_data, 'dailyActivity_merged'):
    merged_data.dailyActivity_merged["ActivityDate"] = pd.to_datetime(merged_data.dailyActivity_merged["ActivityDate"], errors='coerce')
    merged_data.dailyActivity_merged.dropna(subset=['ActivityDate'], inplace=True)
    merged_data.dailyActivity_merged = merged_data.dailyActivity_merged.drop_duplicates(subset=["Id", "ActivityDate"])
    
    print("\n--- merged_data.dailyActivity_merged (after date conversion and deduplication) ---")
    print(merged_data.dailyActivity_merged.head())
    
    # Initialize the comprehensive daily_df with a copy of dailyActivity_merged
    daily_df_combined = merged_data.dailyActivity_merged.copy()
else:
    print("Warning: dailyActivity_merged not found. Comprehensive daily_df will be limited or empty.")
    daily_df_combined = pd.DataFrame(columns=['Id', 'ActivityDate'])


# Prepare and merge sleepDay_merged
if hasattr(merged_data, 'sleepDay_merged'):
    df_sleep = merged_data.sleepDay_merged.copy()
    if 'Id' in df_sleep.columns and 'SleepDay' in df_sleep.columns:
        df_sleep["SleepDay"] = pd.to_datetime(df_sleep["SleepDay"], errors='coerce')
        df_sleep.dropna(subset=['SleepDay'], inplace=True)
        df_sleep = df_sleep.rename(columns={"SleepDay": "ActivityDate"})
        df_sleep = df_sleep.drop_duplicates(subset=["Id", "ActivityDate"])
        
        if not daily_df_combined.empty and 'Id' in daily_df_combined and 'ActivityDate' in daily_df_combined :
            daily_df_combined = pd.merge(daily_df_combined, df_sleep, on=["Id", "ActivityDate"], how="left")
        elif daily_df_combined.empty: # If dailyActivity_merged was missing, start with sleep data
             daily_df_combined = df_sleep
        else: # daily_df_combined was initialized minimal, try to merge
            daily_df_combined = pd.merge(daily_df_combined, df_sleep, on=["Id", "ActivityDate"], how="left")

    else:
        print("Warning: sleepDay_merged is missing 'Id' or 'SleepDay' column. Skipping merge with sleepDay_merged.")
else:
    print("Info: sleepDay_merged not found. Proceeding without daily sleep data.")


# Prepare and merge weightLogInfo_merged
if hasattr(merged_data, 'weightLogInfo_merged'):
    df_weight = merged_data.weightLogInfo_merged.copy()
    if 'Id' in df_weight.columns and 'Date' in df_weight.columns:
        df_weight["Date"] = pd.to_datetime(df_weight["Date"], errors='coerce')
        df_weight.dropna(subset=['Date'], inplace=True)
        df_weight = df_weight.rename(columns={"Date": "ActivityDate"})
        df_weight["ActivityDate"] = df_weight["ActivityDate"].dt.normalize() # Normalize to date part only
        df_weight = df_weight.drop_duplicates(subset=["Id", "ActivityDate"], keep='last')

        if not daily_df_combined.empty and 'Id' in daily_df_combined and 'ActivityDate' in daily_df_combined:
             daily_df_combined = pd.merge(daily_df_combined, df_weight, on=["Id", "ActivityDate"], how="left")
        elif daily_df_combined.empty: # If others were missing, start with weight data
             daily_df_combined = df_weight
        else: # daily_df_combined was initialized minimal, try to merge
            daily_df_combined = pd.merge(daily_df_combined, df_weight, on=["Id", "ActivityDate"], how="left")
    else:
        print("Warning: weightLogInfo_merged is missing 'Id' or 'Date' column. Skipping merge with weightLogInfo_merged.")
else:
    print("Info: weightLogInfo_merged not found. Proceeding without weight data.")

# Assign the fully combined daily data to merged_data.daily_df
merged_data.daily_df = daily_df_combined

print("\n--- merged_data.daily_df (Combined Daily Data) ---")
if hasattr(merged_data, 'daily_df') and not merged_data.daily_df.empty:
    print(merged_data.daily_df.head())
else:
    print("merged_data.daily_df is empty or was not created.")