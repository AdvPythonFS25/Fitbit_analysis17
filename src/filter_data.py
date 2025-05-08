# Copyright (c) 2025 Micael Moreira Lemos, Gilles Reichenbach, Tobias Aubert, Nicolas Stettler
# This software is licensed under the MIT License

"""filter_data.py

Helpers for slicing the large merged Fitbit tables by user IDs and/or time
ranges, as well as combining the two filters.

All returned frames are *brand-new* copies; mutating them will not affect the
original ``MergedData`` object.
"""

import pandas as pd

class DataFilter:
    """Fast, chainable filters for :class:`combine_data.MergedData`.

    Parameters
    ----------
    merged_data : combine_data.MergedData
        Instance whose ``minutes_df``, ``hourly_df`` and ``daily_df`` attributes
        will be queried.

    Raises
    ------
    ValueError
        If an invalid ``freq`` argument is supplied to the time-range helpers.
    """
    def __init__(self, merged_data):
        self.minutes_df = merged_data.minutes_df if hasattr(merged_data, 'minutes_df') else pd.DataFrame()
        self.hourly_df = merged_data.hourly_df if hasattr(merged_data, 'hourly_df') else pd.DataFrame()
        # Use the new comprehensive daily_df
        self.daily_df = merged_data.daily_df if hasattr(merged_data, 'daily_df') else pd.DataFrame()

    def filter_by_user(self, user_id):
        """Return all three frames restricted to one user.

        Parameters
        ----------
        user_id : int | str
            Value of the *Id* column to match.

        Returns
        -------
        dict[str, pandas.DataFrame]
            Keys: ``"minutes"``, ``"hourly"``, ``"daily"``.
        """
        # Ensure DataFrames are not empty and contain 'Id' column
        filtered_minutes = pd.DataFrame()
        if not self.minutes_df.empty and "Id" in self.minutes_df.columns:
            filtered_minutes = self.minutes_df[self.minutes_df["Id"] == user_id]
        
        filtered_hourly = pd.DataFrame()
        if not self.hourly_df.empty and "Id" in self.hourly_df.columns:
            filtered_hourly = self.hourly_df[self.hourly_df["Id"] == user_id]

        filtered_daily = pd.DataFrame()
        if not self.daily_df.empty and "Id" in self.daily_df.columns:
            filtered_daily = self.daily_df[self.daily_df["Id"] == user_id]
            
        return {
            "minutes": filtered_minutes,
            "hourly": filtered_hourly,
            "daily": filtered_daily
        }

    def filter_by_time_range(self, start_time, end_time, freq="minutes"):
        """Extract a calendar slice from one of the three master tables.

        Parameters
        ----------
        start_time, end_time : str | pandas.Timestamp
            Inclusive bounds (coerced with ``pd.to_datetime``).
        freq : {"minutes", "hourly", "daily"}, default "minutes"
            Which underlying table to query.

        Returns
        -------
        pandas.DataFrame
            New frame containing only the requested interval; empty if the
            source has no matching data.
        """
        df_to_filter = pd.DataFrame()
        time_col = None

        if freq == "minutes":
            if not self.minutes_df.empty:
                df_to_filter = self.minutes_df
                time_col = "ActivityMinute"
        elif freq == "hourly":
            if not self.hourly_df.empty:
                df_to_filter = self.hourly_df
                time_col = "ActivityHour"
        elif freq == "daily":
            if not self.daily_df.empty:
                df_to_filter = self.daily_df
                time_col = "ActivityDate"
        else:
            raise ValueError("Invalid frequency. Choose from 'minutes', 'hourly', or 'daily'.")

        if df_to_filter.empty or time_col is None or time_col not in df_to_filter.columns:
            return pd.DataFrame() # Return empty if source df is empty or time_col missing

        # Ensure time column is datetime
        df_to_filter[time_col] = pd.to_datetime(df_to_filter[time_col], errors='coerce')
        
        mask = (df_to_filter[time_col] >= pd.to_datetime(start_time)) & \
               (df_to_filter[time_col] <= pd.to_datetime(end_time))
        return df_to_filter[mask]

    def filter_by_user_and_time(self, user_id, start_time, end_time, freq="minutes"):
        df_filtered_by_time = self.filter_by_time_range(start_time, end_time, freq)
        
        if df_filtered_by_time.empty or "Id" not in df_filtered_by_time.columns:
            return pd.DataFrame()
            
        return df_filtered_by_time[df_filtered_by_time["Id"] == user_id]