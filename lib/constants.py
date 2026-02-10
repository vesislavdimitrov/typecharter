from typing import Tuple
import matplotlib.dates as mdates


class PlotConstants:
    # Plot dimensions
    DEFAULT_FIGSIZE: Tuple[int, int] = (14, 8)

    # Scatter plot styling
    SCATTER_ALPHA = 0.3
    SCATTER_SIZE = 10
    SCATTER_COLOR = "lightgray"

    # Line styling
    DAILY_LINE_WIDTH = 1.5
    DAILY_LINE_ALPHA = 0.7
    DAILY_LINE_COLOR = "blue"
    ROLLING_7_LINE_WIDTH = 2
    ROLLING_7_COLOR = "orange"
    ROLLING_30_LINE_WIDTH = 3
    ROLLING_30_COLOR = "red"

    # Text and layout
    TITLE_FONTSIZE = 16
    AXIS_LABEL_FONTSIZE = 12
    GRID_ALPHA = 0.3
    LEGEND_ALPHA = 0.8
    TICK_ROTATION = 45

    # Statistics box
    STATS_BOX_X = 0.02
    STATS_BOX_Y = 0.02
    STATS_BOX_STYLE = "round"
    STATS_BOX_COLOR = "wheat"
    STATS_BOX_ALPHA = 0.8

    # Time formatting thresholds
    YEARLY_THRESHOLD_DAYS = 365
    MONTHLY_THRESHOLD_DAYS = 30
    MONTH_INTERVAL = 2
    DAILY_DIVISOR = 30
    HOURLY_DIVISOR = 20

    # Date format strings
    YEARLY_FORMAT = "%Y-%m"
    MONTHLY_FORMAT = "%m/%d"
    DAILY_FORMAT = "%m/%d %H:%M"

    # Labels and titles
    PLOT_TITLE = "Words Per Minute (WPM) Over Time"
    X_AXIS_LABEL = "Date/Time"
    Y_AXIS_LABEL = "Words Per Minute (WPM)"
    SCATTER_LABEL = "Individual Sessions"
    DAILY_LABEL = "Daily Average (Interpolated)"
    ROLLING_7_LABEL = "7-Day Rolling Average"
    ROLLING_30_LABEL = "30-Day Rolling Average"
    LEGEND_LOCATION = "upper left"

    # Statistics text formatting
    STATS_TEXT_TEMPLATE = (
        "Statistics:\n"
        "Average WPM: {avg_wpm:.1f}\n"
        "Max WPM: {max_wpm:.1f}\n"
        "Min WPM: {min_wpm:.1f}\n"
        "Total Sessions: {total_sessions}"
    )


class FileDialogConstants:
    DEFAULT_TITLE = "Select Typing Data CSV Files"
    FILE_TYPES = [("CSV files", "*.csv"), ("All files", "*.*")]
    
    # Error and success messages
    NO_FILES_ERROR = "No CSV files could be loaded successfully!"
    TKINTER_UNAVAILABLE_MSG = "ERROR: tkinter is not available. Cannot open GUI dialog."
    TKINTER_WARNING = "WARNING: tkinter not available. GUI file selection will not work."
    
    # Console output templates
    SELECTED_FILES_TEMPLATE = "Selected {count} files:"
    FILE_LIST_ITEM_TEMPLATE = "  - {filename}"
    LOADED_SINGLE_FILE_TEMPLATE = "Loaded {count} records from {filename}"
    TOTAL_RECORDS_TEMPLATE = "Total records loaded: {count}"
    SUCCESS_MESSAGE_TEMPLATE = "Successfully loaded {count} records from {file_count} files!"
    WARNING_TEMPLATE = "WARNING: Could not load {filename}: {error}"


class DataProcessorConstants:
    # Column names
    DATETIME_COLUMN = "Date/Time (UTC)"
    WPM_COLUMN = "WPM"
    DATE_COLUMN = "Date"
    
    # Rolling window sizes
    ROLLING_7_DAYS = 7
    ROLLING_30_DAYS = 30
    
    # Column suffixes for rolling averages
    ROLLING_7_SUFFIX = "_7day"
    ROLLING_30_SUFFIX = "_30day"
    
    # Resampling and interpolation methods
    DAILY_FREQ = "D"
    LINEAR_METHOD = "linear"


class TimeFormatConfig:
    @staticmethod
    def get_time_configs():
        return [
            (
                PlotConstants.YEARLY_THRESHOLD_DAYS,
                PlotConstants.YEARLY_FORMAT,
                lambda: mdates.MonthLocator(interval=PlotConstants.MONTH_INTERVAL),
            ),
            (
                PlotConstants.MONTHLY_THRESHOLD_DAYS,
                PlotConstants.MONTHLY_FORMAT,
                lambda time_span: mdates.DayLocator(
                    interval=max(1, time_span // PlotConstants.DAILY_DIVISOR)
                ),
            ),
            (
                0,
                PlotConstants.DAILY_FORMAT,
                lambda time_span: mdates.HourLocator(
                    interval=max(1, time_span * 24 // PlotConstants.HOURLY_DIVISOR)
                ),
            ),
        ]
