import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Tuple

from .constants import PlotConstants, TimeFormatConfig, DataProcessorConstants


class TypingDataVisualizer:
    def __init__(self, figsize: Tuple[int, int] = PlotConstants.DEFAULT_FIGSIZE):
        self.figsize = figsize

    def create_plot(self, df: pd.DataFrame, daily_smooth: pd.DataFrame) -> None:
        plt.figure(figsize=self.figsize)

        self._plot_individual_sessions(df)
        self._plot_daily_averages(daily_smooth)
        self._plot_rolling_averages(daily_smooth)

        self._customize_plot(df)
        self._format_axes(df)
        self._add_statistics(df)

        plt.tight_layout()
        plt.show()

    def _plot_individual_sessions(self, df: pd.DataFrame) -> None:
        plt.scatter(
            df[DataProcessorConstants.DATETIME_COLUMN],
            df[DataProcessorConstants.WPM_COLUMN],
            alpha=PlotConstants.SCATTER_ALPHA,
            s=PlotConstants.SCATTER_SIZE,
            color=PlotConstants.SCATTER_COLOR,
            label=PlotConstants.SCATTER_LABEL,
        )

    def _plot_daily_averages(self, daily_smooth: pd.DataFrame) -> None:
        plt.plot(
            daily_smooth[DataProcessorConstants.DATE_COLUMN],
            daily_smooth[DataProcessorConstants.WPM_COLUMN],
            linewidth=PlotConstants.DAILY_LINE_WIDTH,
            alpha=PlotConstants.DAILY_LINE_ALPHA,
            color=PlotConstants.DAILY_LINE_COLOR,
            label=PlotConstants.DAILY_LABEL,
        )

    def _plot_rolling_averages(self, daily_smooth: pd.DataFrame) -> None:
        plt.plot(
            daily_smooth[DataProcessorConstants.DATE_COLUMN],
            daily_smooth[
                f"{DataProcessorConstants.WPM_COLUMN}{DataProcessorConstants.ROLLING_7_SUFFIX}"
            ],
            linewidth=PlotConstants.ROLLING_7_LINE_WIDTH,
            color=PlotConstants.ROLLING_7_COLOR,
            label=PlotConstants.ROLLING_7_LABEL,
        )
        plt.plot(
            daily_smooth[DataProcessorConstants.DATE_COLUMN],
            daily_smooth[
                f"{DataProcessorConstants.WPM_COLUMN}{DataProcessorConstants.ROLLING_30_SUFFIX}"
            ],
            linewidth=PlotConstants.ROLLING_30_LINE_WIDTH,
            color=PlotConstants.ROLLING_30_COLOR,
            label=PlotConstants.ROLLING_30_LABEL,
        )

    def _customize_plot(self, df: pd.DataFrame) -> None:
        plt.title(
            PlotConstants.PLOT_TITLE,
            fontsize=PlotConstants.TITLE_FONTSIZE,
            fontweight="bold",
        )
        plt.xlabel(
            PlotConstants.X_AXIS_LABEL, fontsize=PlotConstants.AXIS_LABEL_FONTSIZE
        )
        plt.ylabel(
            PlotConstants.Y_AXIS_LABEL, fontsize=PlotConstants.AXIS_LABEL_FONTSIZE
        )
        plt.grid(True, alpha=PlotConstants.GRID_ALPHA)
        plt.legend(
            loc=PlotConstants.LEGEND_LOCATION, framealpha=PlotConstants.LEGEND_ALPHA
        )

    def _format_axes(self, df: pd.DataFrame) -> None:
        time_span = (
            df[DataProcessorConstants.DATETIME_COLUMN].max()
            - df[DataProcessorConstants.DATETIME_COLUMN].min()
        ).days
        time_configs = TimeFormatConfig.get_time_configs()

        for threshold, format_str, locator_func in time_configs:
            if time_span > threshold:
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(format_str))
                self._set_axis_locator(threshold, locator_func, time_span)
                break
        plt.xticks(rotation=PlotConstants.TICK_ROTATION)

    def _set_axis_locator(self, threshold: int, locator_func, time_span: int) -> None:
        if threshold == 0 or threshold == PlotConstants.MONTHLY_THRESHOLD_DAYS:
            plt.gca().xaxis.set_major_locator(locator_func(time_span))
            return
        plt.gca().xaxis.set_major_locator(locator_func())

    def _add_statistics(self, df: pd.DataFrame) -> None:
        avg_wpm = df[DataProcessorConstants.WPM_COLUMN].mean()
        max_wpm = df[DataProcessorConstants.WPM_COLUMN].max()
        min_wpm = df[DataProcessorConstants.WPM_COLUMN].min()

        stats_text = PlotConstants.STATS_TEXT_TEMPLATE.format(
            avg_wpm=avg_wpm, max_wpm=max_wpm, min_wpm=min_wpm, total_sessions=len(df)
        )

        plt.text(
            PlotConstants.STATS_BOX_X,
            PlotConstants.STATS_BOX_Y,
            stats_text,
            transform=plt.gca().transAxes,
            verticalalignment="bottom",
            bbox=dict(
                boxstyle=PlotConstants.STATS_BOX_STYLE,
                facecolor=PlotConstants.STATS_BOX_COLOR,
                alpha=PlotConstants.STATS_BOX_ALPHA,
            ),
        )
