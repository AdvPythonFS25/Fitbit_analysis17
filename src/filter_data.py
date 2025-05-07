import pandas as pd

class DataFilter:
    def __init__(self, merged_data):
        self.minutes_df = merged_data.minutes_df
        self.hourly_df = merged_data.hourly_df
        self.daily_df = merged_data.dailyActivity_merged

    def filter_by_user(self, user_id):
        return {
            "minutes": self.minutes_df[self.minutes_df["Id"] == user_id],
            "hourly": self.hourly_df[self.hourly_df["Id"] == user_id],
            "daily": self.daily_df[self.daily_df["Id"] == user_id]
        }

    def filter_by_time_range(self, start_time, end_time, freq="minutes"):
        if freq == "minutes":
            df = self.minutes_df
            time_col = "ActivityMinute"
        elif freq == "hourly":
            df = self.hourly_df
            time_col = "ActivityHour"
        elif freq == "daily":
            df = self.daily_df
            time_col = "ActivityDate"
        else:
            raise ValueError("Invalid frequency. Choose from 'minutes', 'hourly', or 'daily'.")

        mask = (df[time_col] >= pd.to_datetime(start_time)) & (df[time_col] <= pd.to_datetime(end_time))
        return df[mask]

    def filter_by_user_and_time(self, user_id, start_time, end_time, freq="minutes"):
        df = self.filter_by_time_range(start_time, end_time, freq)
        return df[df["Id"] == user_id]