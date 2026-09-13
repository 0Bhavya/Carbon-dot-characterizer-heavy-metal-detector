import re
import pandas as pd


# Keywords used to identify the spectroscopy/sensing technique.
TECHNIQUE_KEYWORDS = {
    "uvvis": [
        "uv-vis",
        "uv vis",
        "uvvis",
        "absorbance",
        "absorption",
    ],
    "pl": [
        "photoluminescence",
        "pl",
        "emission",
    ],
    "ftir": [
        "ftir",
        "ir",
        "infrared",
        "wavenumber",
    ],
    "xrd": [
        "xrd",
        "2theta",
        "2-theta",
        "2θ",
        "diffraction",
    ],
    "fluorescence": [
        "fluorescence",
        "fluorescent",
        "emission intensity",
    ],
}


def _normalize_column_name(column_name: str) -> str:
    """
    Normalize a column name so that different naming styles
    can be compared more easily.
    """
    column_name = str(column_name).lower().strip()

    # Replace special characters with spaces.
    column_name = re.sub(r"[^a-z0-9]+", " ", column_name)

    # Remove extra spaces.
    return " ".join(column_name.split())


def detect_technique(df: pd.DataFrame) -> str:
    """
    Detect the likely spectroscopy/sensing technique from
    the DataFrame column names.

    Returns:
        'uvvis', 'pl', 'ftir', 'xrd',
        'fluorescence', or 'unknown'
    """

    if df.empty or len(df.columns) == 0:
        return "unknown"

    normalized_columns = [
        _normalize_column_name(column)
        for column in df.columns
    ]

    scores = {
        technique: 0
        for technique in TECHNIQUE_KEYWORDS
    }

    for column in normalized_columns:
        for technique, keywords in TECHNIQUE_KEYWORDS.items():
            for keyword in keywords:
                normalized_keyword = _normalize_column_name(keyword)

                if normalized_keyword in column:
                    scores[technique] += 1

    best_technique = max(scores, key=scores.get)

    if scores[best_technique] == 0:
        return "unknown"

    return best_technique


def detect_columns(
    df: pd.DataFrame,
    technique: str
) -> dict[str, str]:
    """
    Detect the logical x/y columns for a given technique.

    Example:
        {
            "x": "Wavelength (nm)",
            "y": "Absorbance"
        }

    Raises:
        ValueError if the required columns cannot be detected.
    """

    if df.empty or len(df.columns) == 0:
        raise ValueError("The dataset does not contain any columns.")

    technique = technique.lower()

    if technique not in TECHNIQUE_KEYWORDS:
        raise ValueError(f"Unknown technique: {technique}")

    normalized = {
        column: _normalize_column_name(column)
        for column in df.columns
    }

    x_keywords = {
        "uvvis": ["wavelength", "lambda"],
        "pl": ["wavelength", "lambda"],
        "ftir": ["wavenumber"],
        "xrd": ["2theta", "2 theta", "theta", "angle"],
        "fluorescence": ["wavelength", "lambda"],
    }

    y_keywords = {
        "uvvis": ["absorbance", "absorption", "abs"],
        "pl": ["intensity", "emission"],
        "ftir": ["intensity", "transmittance", "absorbance"],
        "xrd": ["intensity", "counts"],
        "fluorescence": ["intensity", "fluorescence", "emission"],
    }

    x_column = None
    y_column = None

    # Find X column.
    for column, normalized_name in normalized.items():
        for keyword in x_keywords[technique]:
            if _normalize_column_name(keyword) in normalized_name:
                x_column = column
                break

        if x_column is not None:
            break

    # Find Y column.
    for column, normalized_name in normalized.items():
        if column == x_column:
            continue

        for keyword in y_keywords[technique]:
            if _normalize_column_name(keyword) in normalized_name:
                y_column = column
                break

        if y_column is not None:
            break

    if x_column is None or y_column is None:
        raise ValueError(
            f"Could not automatically detect the required "
            f"columns for technique '{technique}'."
        )

    return {
        "x": x_column,
        "y": y_column,
    }


def get_manual_mapping_options(
    df: pd.DataFrame
) -> list[str]:
    """
    Return all column names so the UI can provide
    manual column-mapping options.
    """

    return [str(column) for column in df.columns]