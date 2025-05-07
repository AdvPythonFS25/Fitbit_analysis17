import pandas as pd

class SummaryStatistics:
    def __init__(self, df):
        self.df = df

    def total_steps(self):
        return self.df["TotalSteps"].sum() if "TotalSteps" in self.df.columns else None

    def average_daily_steps(self):
        return self.df["TotalSteps"].mean() if "TotalSteps" in self.df.columns else None

    def average_sleep_duration(self):
        return self.df["TotalMinutesAsleep"].mean() if "TotalMinutesAsleep" in self.df.columns else None

    def total_sleep_duration(self):
        return self.df["TotalMinutesAsleep"].sum() if "TotalMinutesAsleep" in self.df.columns else None

    def average_calories_per_hour(self):
        return self.df["Calories"].mean() if "Calories" in self.df.columns else None