from lib.visualizer import TypingDataVisualizer
from lib.data_processor import TypingDataProcessor
from lib.gui_data_loader import GuiTypingDataLoader


def main():
    loader = GuiTypingDataLoader()
    processor = TypingDataProcessor()
    visualizer = TypingDataVisualizer()

    data_frame = loader.load_data()
    if data_frame is None:
        return

    data_frame = processor.prepare_data(data_frame)
    daily_smooth = processor.create_daily_averages(data_frame)
    daily_smooth = processor.add_rolling_averages(daily_smooth)
    visualizer.create_plot(data_frame, daily_smooth)


if __name__ == "__main__":
    main()
