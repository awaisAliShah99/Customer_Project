
"""Functions for loading raw source data."""

from pathlib import Path

import pandas as pd

from src.config import RAW_DATA_PATH


def load_raw_data(file_path: Path | str | None = None) -> pd.DataFrame:
    """Load the raw customer CSV and return it as a DataFrame."""

    # Step 1: Use the default path if no path is provided.
    if file_path is None:
        file_path = RAW_DATA_PATH

    # Step 2: Convert the path into a Path object.
    file_path = Path(file_path)

    # Step 3: Check whether the file exists.
    if not file_path.is_file():
        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    # Step 4: Read CSV and return the DataFrame.
    data = pd.read_csv(file_path)

    return data
