import pandas as pd

from .constants import DataProcessorConstants


class TypingDataProcessor:
    @staticmethod
    def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df[DataProcessorConstants.DATETIME_COLUMN] = pd.to_datetime(
            df[DataProcessorConstants.DATETIME_COLUMN]
        )
        df = df.sort_values(DataProcessorConstants.DATETIME_COLUMN)
        return df

    @staticmethod
    def create_daily_averages(df: pd.DataFrame) -> pd.DataFrame:
        daily_avg = TypingDataProcessor._calculate_daily_averages(df)
        date_range = TypingDataProcessor._create_full_date_range(daily_avg)
        daily_smooth = TypingDataProcessor._interpolate_missing_dates(
            daily_avg, date_range
        )
        return daily_smooth

    @staticmethod
    def add_rolling_averages(daily_smooth: pd.DataFrame) -> pd.DataFrame:
        daily_smooth = daily_smooth.copy()
        daily_smooth[
            f"{DataProcessorConstants.WPM_COLUMN}{DataProcessorConstants.ROLLING_7_SUFFIX}"
        ] = (
            daily_smooth[DataProcessorConstants.WPM_COLUMN]
            .rolling(window=DataProcessorConstants.ROLLING_7_DAYS, center=True)
            .mean()
        )
        daily_smooth[
            f"{DataProcessorConstants.WPM_COLUMN}{DataProcessorConstants.ROLLING_30_SUFFIX}"
        ] = (
            daily_smooth[DataProcessorConstants.WPM_COLUMN]
            .rolling(window=DataProcessorConstants.ROLLING_30_DAYS, center=True)
            .mean()
        )
        return daily_smooth

    @staticmethod
    def _calculate_daily_averages(df: pd.DataFrame) -> pd.DataFrame:
        df[DataProcessorConstants.DATE_COLUMN] = df[
            DataProcessorConstants.DATETIME_COLUMN
        ].dt.date
        daily_avg = (
            df.groupby(DataProcessorConstants.DATE_COLUMN)[
                DataProcessorConstants.WPM_COLUMN
            ]
            .mean()
            .reset_index()
        )
        daily_avg[DataProcessorConstants.DATE_COLUMN] = pd.to_datetime(
            daily_avg[DataProcessorConstants.DATE_COLUMN]
        )
        return daily_avg

    @staticmethod
    def _create_full_date_range(daily_avg: pd.DataFrame) -> pd.DatetimeIndex:
        return pd.date_range(
            start=daily_avg[DataProcessorConstants.DATE_COLUMN].min(),
            end=daily_avg[DataProcessorConstants.DATE_COLUMN].max(),
            freq=DataProcessorConstants.DAILY_FREQ,
        )

    @staticmethod
    def _interpolate_missing_dates(
        daily_avg: pd.DataFrame, date_range: pd.DatetimeIndex
    ) -> pd.DataFrame:
        daily_smooth = (
            daily_avg.set_index(DataProcessorConstants.DATE_COLUMN)
            .reindex(date_range)
            .interpolate(method=DataProcessorConstants.LINEAR_METHOD)
        )
        daily_smooth = daily_smooth.reset_index()
        daily_smooth.columns = [
            DataProcessorConstants.DATE_COLUMN,
            DataProcessorConstants.WPM_COLUMN,
        ]
        return daily_smooth
