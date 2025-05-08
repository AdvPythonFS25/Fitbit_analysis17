# Copyright (c) 2025 Micael Moreira Lemos, Gilles Reichenbach, Tobias Aubert, Nicolas Stettler
# This software is licensed under the MIT License


"""summary_statistics.py

Aggregates commonly requested Fitbit metrics such as total steps, average
sleep duration, etc., from any time-resolution DataFrame.
"""

import pandas as pd

class SummaryStatistics:
    """Compute headline metrics on an arbitrary Fitbit DataFrame.

    The class inspects the presence of expected columns and automatically
    adapts its calculations to minute-, hour- or day-level data.

    Parameters
    ----------
    df : pandas.DataFrame
        Source data whose columns follow Fitbit export conventions.
    """
    def __init__(self, df):
        self.df = df if isinstance(df, pd.DataFrame) else pd.DataFrame()

    def total_steps(self):
        """Return the sum of all available step columns.

        Returns
        -------
        int | None
            Total number of steps, or ``None`` if no step column exists.
        """
        if not self.df.empty and "TotalSteps" in self.df.columns:
            return self.df["TotalSteps"].sum()
        # Fallback for minute/hourly data which might have "Steps" or "StepTotal"
        elif not self.df.empty and "Steps" in self.df.columns: # from minutes_df
            return self.df["Steps"].sum()
        elif not self.df.empty and "StepTotal" in self.df.columns: # from hourly_df
            return self.df["StepTotal"].sum()
        return None

    def average_daily_steps(self):
        """Mean of *TotalSteps* (daily resolution only).

        Returns
        -------
        float | None
        """
        if not self.df.empty and "TotalSteps" in self.df.columns and "ActivityDate" in self.df.columns:
            return self.df["TotalSteps"].mean()
        return None

    def average_sleep_duration(self):
        """Average of *TotalMinutesAsleep* in minutes; ``None`` if absent."""
        if not self.df.empty and "TotalMinutesAsleep" in self.df.columns:
            return self.df["TotalMinutesAsleep"].mean()
        return None

    def total_sleep_duration(self):
        """Sum of *TotalMinutesAsleep* in minutes; ``None`` if absent."""
        if not self.df.empty and "TotalMinutesAsleep" in self.df.columns:
            return self.df["TotalMinutesAsleep"].sum()
        return None

    def average_calories_per_hour(self):
        """Mean of *Calories* — context-sensitive.

        * Hourly data → arithmetic mean over rows  
        * Minute or daily data → arithmetic mean over the available column

        Returns
        -------
        float | None
        """
        if not self.df.empty and "Calories" in self.df.columns and "ActivityHour" in self.df.columns: # Hourly data
            return self.df["Calories"].mean()
        # If it's minute data, one could resample, but for now, direct mean if column exists.
        elif not self.df.empty and "Calories" in self.df.columns: # Could be minute or daily data
            return self.df["Calories"].mean() 
        return None