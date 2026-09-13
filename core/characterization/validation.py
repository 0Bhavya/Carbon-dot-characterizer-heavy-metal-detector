import math
from collections.abc import Mapping
from dataclasses import dataclass

import pandas as pd


@dataclass
class ValidationReport:
	"""Checklist-friendly result of spectrum validation."""

	is_valid: bool
	warnings: list[str]
	errors: list[str]
	missing_count: int
	invalid_count: int


def _report(
	errors: list[str],
	warnings: list[str],
	missing_count: int = 0,
	invalid_count: int = 0,
) -> ValidationReport:
	return ValidationReport(
		is_valid=not errors,
		warnings=warnings,
		errors=errors,
		missing_count=missing_count,
		invalid_count=invalid_count,
	)


def validate_spectrum(
	df: pd.DataFrame,
	col_map: dict,
) -> ValidationReport:
	"""Validate the required numeric columns of a spectrum.

	The input DataFrame is read-only from this function's perspective. The
	validator reports data-quality problems but does not clean, interpolate,
	smooth, or otherwise alter the input data.
	"""
	errors: list[str] = []
	warnings: list[str] = []

	if not isinstance(df, pd.DataFrame):
		return _report(
			["The spectrum must be provided as a pandas DataFrame."],
			warnings,
		)

	if df.empty:
		return _report(
			["The spectrum is empty. Provide at least two data rows."],
			warnings,
		)

	if df.columns.duplicated().any():
		return _report(
			["The dataset contains duplicate column names."],
			warnings,
		)

	if not isinstance(col_map, Mapping):
		return _report(
			["Column mapping is missing or has an invalid format."],
			warnings,
		)

	roles = {"x": "x", "y": "y"}
	required_columns: dict[str, object] = {}

	for role, label in roles.items():
		if role not in col_map or col_map[role] is None:
			errors.append(f"Required {label} column mapping is missing.")
			continue

		required_columns[role] = col_map[role]

	try:
		missing_columns = [
			str(column)
			for column in required_columns.values()
			if column not in df.columns
		]
	except Exception:
		return _report(
			["Column mapping contains an invalid column reference."],
			warnings,
		)
	for column in missing_columns:
		errors.append(f"Required column '{column}' was not found in the dataset.")

	if errors:
		return _report(errors, warnings)

	x_column = required_columns["x"]
	y_column = required_columns["y"]

	if x_column == y_column:
		errors.append("The x and y roles must reference different columns.")
		return _report(errors, warnings)

	x_values = df[x_column]
	y_values = df[y_column]

	missing_count = int(x_values.isna().sum() + y_values.isna().sum())
	if missing_count:
		warnings.append(
			f"Found {missing_count} missing value(s) in the required x/y columns."
		)

	invalid_count = 0
	numeric_values: dict[str, pd.Series] = {}

	for role, values in (("x", x_values), ("y", y_values)):
		if values.isna().all():
			errors.append(f"The required {role} column '{required_columns[role]}' is empty.")
			numeric_values[role] = pd.Series(index=values.index, dtype="float64")
			continue

		try:
			numeric = pd.to_numeric(values, errors="coerce")
		except Exception:
			errors.append(
				f"The required {role} column '{required_columns[role]}' could not be interpreted."
			)
			numeric_values[role] = pd.Series(index=values.index, dtype="float64")
			continue

		non_numeric = numeric.isna() & values.notna()
		invalid_count += int(non_numeric.sum())
		numeric_values[role] = numeric

	try:
		infinite_count = sum(
			int(numeric.map(lambda value: pd.notna(value) and not math.isfinite(value)).sum())
			for numeric in numeric_values.values()
		)
	except Exception:
		infinite_count = 0

	invalid_count += infinite_count
	if invalid_count:
		warnings.append(
			f"Found {invalid_count} invalid non-numeric or non-finite value(s) in the required x/y columns."
		)

	try:
		usable_rows = numeric_values["x"].notna() & numeric_values["y"].notna()
		usable_rows &= numeric_values["x"].map(math.isfinite)
		usable_rows &= numeric_values["y"].map(math.isfinite)
		usable_count = int(usable_rows.sum())
	except Exception:
		usable_count = 0

	if usable_count < 2:
		errors.append(
			"The spectrum must contain at least two usable numeric x/y rows."
		)

	return _report(errors, warnings, missing_count, invalid_count)
