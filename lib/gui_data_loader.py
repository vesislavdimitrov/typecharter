import pandas as pd
from typing import List, Optional

from .constants import FileDialogConstants

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox

    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    print(FileDialogConstants.TKINTER_WARNING)


class GuiTypingDataLoader:

    def __init__(self):
        self.root = None
        if TKINTER_AVAILABLE:
            self._initialize_root()

    def select_files(self) -> List[str]:
        if not self._ensure_root_available():
            return []

        files = filedialog.askopenfilenames(
            title=FileDialogConstants.DEFAULT_TITLE,
            filetypes=FileDialogConstants.FILE_TYPES,
            multiple=True,
        )

        selected = list(files) if files else []
        return selected

    def load_data(self) -> Optional[pd.DataFrame]:
        csv_files = self.select_files()
        if not csv_files:
            return None

        self._print_selected_files(csv_files)
        all_data = self._load_csv_files(csv_files)

        if not all_data:
            self._show_error_message(FileDialogConstants.NO_FILES_ERROR)
            return None

        return self._concatenate_and_report(all_data)

    def _print_selected_files(self, csv_files: List[str]) -> None:
        print(FileDialogConstants.SELECTED_FILES_TEMPLATE.format(count=len(csv_files)))
        for file in csv_files:
            print(FileDialogConstants.FILE_LIST_ITEM_TEMPLATE.format(filename=file))

    def _load_csv_files(self, csv_files: List[str]) -> List[pd.DataFrame]:
        all_data = []
        for csv_file in csv_files:
            df = self._load_single_csv(csv_file)
            if df is not None:
                all_data.append(df)
        return all_data

    def _load_single_csv(self, csv_file: str) -> Optional[pd.DataFrame]:
        try:
            df = pd.read_csv(csv_file)
            return df
        except Exception:
            return None

    def _concatenate_and_report(self, all_data: List[pd.DataFrame]) -> pd.DataFrame:
        df = pd.concat(all_data, ignore_index=True)
        print(FileDialogConstants.TOTAL_RECORDS_TEMPLATE.format(count=len(df)))

        self._show_success_message(
            FileDialogConstants.SUCCESS_MESSAGE_TEMPLATE.format(
                count=len(df), file_count=len(all_data)
            )
        )
        return df

    def _show_error_message(self, message: str) -> None:
        if not self._ensure_root_available():
            print(f"Error: {message}")
            return
        messagebox.showerror("Error", message)

    def _show_success_message(self, message: str) -> None:
        if not self._ensure_root_available():
            print(f"Success: {message}")
            return
        messagebox.showinfo("Success", message)

    def _initialize_root(self) -> None:
        if self.root is None:
            self.root = tk.Tk()
            self.root.attributes("-alpha", 0.0)
            self.root.withdraw()

    def _ensure_root_available(self) -> bool:
        if not TKINTER_AVAILABLE:
            print(FileDialogConstants.TKINTER_UNAVAILABLE_MSG)
            return False

        if self.root is None:
            self._initialize_root()
        return True
