'''
This file combines all the data to a single dataframe
'''

import pandas as pd
import os

class CSVData:
    def __init__(self, folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                var_name = os.path.splitext(filename)[0].replace(" ", "_").replace("-", "_")
                df = pd.read_csv(os.path.join(folder_path, filename))
                setattr(self, var_name, df)

# Usage
folder_path = "data/Folder_1"
data_1 = CSVData(folder_path)

folder_path = "data/Folder_2"
data_2 = CSVData(folder_path)


class MergedData:
    def __init__(self, data_1, data_2):
        for attr in dir(data_1):
            if not attr.startswith("_") and isinstance(getattr(data_1, attr), pd.DataFrame):
                print(f"Data from {attr}:")
                print(getattr(data_1, attr).head())
                df1 = getattr(data_1, attr)
                df2 = getattr(data_2, attr, None)
                if isinstance(df2, pd.DataFrame):
                    merged_df = pd.concat([df1, df2], ignore_index=True)
                else:
                    merged_df = df1
                setattr(self, attr, merged_df)

merged_data = MergedData(data_1, data_2)


'''

Here we merge all data that is stored by every minute.

'''

merged_data.minuteCaloriesNarrow_merged = merged_data.minuteCaloriesNarrow_merged.drop_duplicates(subset=["Id", "ActivityMinute"])
merged_data.minuteIntensitiesNarrow_merged = merged_data.minuteIntensitiesNarrow_merged.drop_duplicates(subset=["Id", "ActivityMinute"])
merged_data.minuteMETsNarrow_merged = merged_data.minuteMETsNarrow_merged.drop_duplicates(subset=["Id", "ActivityMinute"])
merged_data.minuteStepsNarrow_merged = merged_data.minuteStepsNarrow_merged.drop_duplicates(subset=["Id", "ActivityMinute"])
merged_data.minuteSleep_merged = merged_data.minuteSleep_merged.drop_duplicates(subset=["Id", "date"])


merged_data.minutes_df = pd.merge(merged_data.minuteCaloriesNarrow_merged, merged_data.minuteIntensitiesNarrow_merged, on=["Id", "ActivityMinute"], how="outer")
merged_data.minutes_df = pd.merge(merged_data.minutes_df, merged_data.minuteMETsNarrow_merged, on=["Id", "ActivityMinute"], how="outer")
merged_data.minutes_df = pd.merge(merged_data.minutes_df, merged_data.minuteStepsNarrow_merged, on=["Id", "ActivityMinute"], how="outer")
merged_data.minutes_df = pd.merge(merged_data.minutes_df, merged_data.minuteSleep_merged, left_on=["Id", "ActivityMinute"], right_on=["Id", "date"], how="outer")

# Update ActivityMinute with values from date where ActivityMinute is missing
merged_data.minutes_df["ActivityMinute"] = merged_data.minutes_df["ActivityMinute"].combine_first(merged_data.minutes_df["date"])

# Drop the date column
merged_data.minutes_df = merged_data.minutes_df.drop(columns=["date"])


merged_data.minutes_df["ActivityMinute"] = pd.to_datetime(merged_data.minutes_df["ActivityMinute"], format="%m/%d/%Y %I:%M:%S %p")

print(merged_data.minutes_df)


'''

Here we merge all data that is stored hourly.

'''

merged_data.hourlyCalories_merged = merged_data.hourlyCalories_merged.drop_duplicates(subset=["Id", "ActivityHour"])
merged_data.hourlyIntensities_merged = merged_data.hourlyIntensities_merged.drop_duplicates(subset=["Id", "ActivityHour"])
merged_data.hourlySteps_merged = merged_data.hourlySteps_merged.drop_duplicates(subset=["Id", "ActivityHour"])


merged_data.hourly_df = pd.merge(merged_data.hourlyCalories_merged, merged_data.hourlyIntensities_merged, on=["Id", "ActivityHour"], how="inner")
merged_data.hourly_df = pd.merge(merged_data.hourly_df, merged_data.hourlySteps_merged, on=["Id", "ActivityHour"], how="inner")

merged_data.hourly_df["ActivityHour"] = pd.to_datetime(merged_data.hourly_df["ActivityHour"], format="%m/%d/%Y %I:%M:%S %p")
print(merged_data.hourly_df)


'''

Here we merge all data that is stored daily.

'''


merged_data.dailyActivity_merged["ActivityDate"] = pd.to_datetime(merged_data.dailyActivity_merged["ActivityDate"])
print(merged_data.dailyActivity_merged)