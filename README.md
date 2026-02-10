# TypeCharter
TypeCharter visualizes (WPM) over time with daily and rolling averages. Compatible with CSV files generated from the official [TypeRacer](https://typeracer.com) account history.

# Usage
## Option A:
- Use [pyinstaller](https://pyinstaller.org/en/stable/) to build into an executable via the build.sh script. (MacOS only)

## Option B:
- Run typecharter.py directly:
  ```shell
  cd typecharter
  python typecharter.py
  ```

- Then, use the file browser window to upload a single or multiple .csv files for visualization.

## Requirements
- Python 3.9+
- matplotlib
- pandas

## Author
Vesislav Dimitrov