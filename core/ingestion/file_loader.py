import os
import pandas as pd


class UnsupportedFileTypeError(Exception):
    """Raised when the uploaded file is not CSV or Excel."""


class FileLoadError(Exception):
    """Raised when a supported file cannot be read or validated."""


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


def _get_extension(file) -> str:
    """Get the file extension in lowercase."""
    filename = getattr(file, "name", file)

    if not filename:
        raise UnsupportedFileTypeError("Could not determine the file type.")

    return os.path.splitext(str(filename))[1].lower()


def _rewind(file) -> None:
    """Reset seekable uploaded files before passing them to Pandas."""
    seek = getattr(file, "seek", None)

    if callable(seek):
        try:
            seek(0)
        except (OSError, ValueError) as error:
            raise FileLoadError("The uploaded file could not be read.") from None


def _unsupported_file_type(extension: str) -> UnsupportedFileTypeError:
    return UnsupportedFileTypeError(
        f"Unsupported file type: '{extension or 'unknown'}'. "
        "Please upload a .csv, .xlsx, or .xls file."
    )


def _read_csv(file) -> pd.DataFrame:
    _rewind(file)

    try:
        return pd.read_csv(file)
    except Exception as error:
        raise FileLoadError(f"Could not read the CSV file: {error}") from None


def _read_excel(file, sheet_name=0) -> pd.DataFrame:
    _rewind(file)

    try:
        return pd.read_excel(file, sheet_name=sheet_name)
    except ValueError as error:
        raise FileLoadError(f"Could not load Excel sheet '{sheet_name}': {error}") from None
    except Exception as error:
        raise FileLoadError(f"Could not read the Excel file: {error}") from None


def load_file(file) -> pd.DataFrame:
    """
    Load a CSV or Excel file into a pandas DataFrame.

    Supports:
        .csv
        .xlsx
        .xls
    """
    extension = _get_extension(file)

    if extension == ".csv":
        return _read_csv(file)

    if extension in SUPPORTED_EXTENSIONS - {".csv"}:
        return _read_excel(file)

    raise _unsupported_file_type(extension)


def list_sheets(file) -> list[str]:
    """
    Return the sheet names of an Excel file.

    For CSV files, returns ['Sheet1'].
    """
    extension = _get_extension(file)

    if extension == ".csv":
        return ["Sheet1"]

    if extension in SUPPORTED_EXTENSIONS - {".csv"}:
        _rewind(file)

        try:
            with pd.ExcelFile(file) as excel_file:
                return excel_file.sheet_names
        except Exception as error:
            raise FileLoadError(f"Could not list Excel sheets: {error}") from None

    raise _unsupported_file_type(extension)


def load_sheet(file, sheet_name: str) -> pd.DataFrame:
    """Load a specific Excel sheet into a pandas DataFrame."""
    extension = _get_extension(file)

    if extension == ".csv":
        if sheet_name != "Sheet1":
            raise FileLoadError("CSV files only contain the 'Sheet1' sheet.")

        return _read_csv(file)

    if extension in SUPPORTED_EXTENSIONS - {".csv"}:
        return _read_excel(file, sheet_name=sheet_name)

    raise _unsupported_file_type(extension)