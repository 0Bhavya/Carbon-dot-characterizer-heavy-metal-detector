"""PDF reporting and processed-data export for carbon dot characterization."""

from datetime import datetime
from html import escape
from io import BytesIO
from os import PathLike
from typing import Any, Mapping

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
	Paragraph,
	SimpleDocTemplate,
	Spacer,
	Table,
	TableStyle,
	Image,
)


def _display_value(value: Any) -> str:
	"""Return a report-safe value for missing or unavailable results."""
	if value is None or (isinstance(value, float) and pd.isna(value)):
		return "N/A"
	if isinstance(value, Mapping):
		return "; ".join(
			f"{key}: {_display_value(item)}" for key, item in value.items()
		)
	if isinstance(value, (list, tuple, set)):
		return ", ".join(_display_value(item) for item in value)
	return str(value)


def _paragraph(text: Any, style: Any) -> Paragraph:
	"""Create a Paragraph with escaped user/result content."""
	return Paragraph(escape(_display_value(text)), style)


def _result_value(results: Mapping[str, Any], *keys: str) -> Any:
	"""Get the first available value for a set of compatible result keys."""
	for key in keys:
		if key in results:
			return results[key]
	return None


def _section_table(
	title: str,
	values: Any,
	styles: Any,
) -> list[Any]:
	"""Build a labeled report section from a mapping or a scalar value."""
	story: list[Any] = [_paragraph(title, styles["Heading2"]), Spacer(1, 4)]
	if isinstance(values, Mapping) and values:
		rows = [[_paragraph("Item", styles["Normal"]), _paragraph("Value", styles["Normal"])]]
		rows.extend(
			[
				[_paragraph(key, styles["Normal"]), _paragraph(value, styles["Normal"])]
				for key, value in values.items()
			]
		)
	else:
		rows = [[_paragraph(_display_value(values), styles["Normal"])]]

	table = Table(rows, repeatRows=1 if len(rows) > 1 else 0, hAlign="LEFT")
	table.setStyle(
		TableStyle(
			[
				("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
				("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
				("VALIGN", (0, 0), (-1, -1), "TOP"),
				("LEFTPADDING", (0, 0), (-1, -1), 6),
				("RIGHTPADDING", (0, 0), (-1, -1), 6),
			]
		)
	)
	story.extend([table, Spacer(1, 12)])
	return story


def _peak_section(peaks: Any, styles: Any) -> list[Any]:
	"""Build a table for peak results when peak data is available."""
	story: list[Any] = [_paragraph("Peak Information", styles["Heading2"]), Spacer(1, 4)]
	if isinstance(peaks, list) and peaks and all(isinstance(peak, Mapping) for peak in peaks):
		columns = list(dict.fromkeys(key for peak in peaks for key in peak))
		rows = [[_paragraph(column, styles["Normal"]) for column in columns]]
		rows.extend(
			[
				[_paragraph(peak.get(column), styles["Normal"]) for column in columns]
				for peak in peaks
			]
		)
	else:
		rows = [[_paragraph(peaks, styles["Normal"])]]

	table = Table(rows, repeatRows=1 if len(rows) > 1 else 0, hAlign="LEFT")
	table.setStyle(
		TableStyle(
			[
				("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
				("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
				("VALIGN", (0, 0), (-1, -1), "TOP"),
			]
		)
	)
	story.extend([table, Spacer(1, 12)])
	return story


def _graph_section(graph_images: Any, styles: Any) -> list[Any]:
	"""Build a PDF section containing valid, scaled characterization images."""
	if isinstance(graph_images, (str, bytes, PathLike, BytesIO)):
		graph_images = [graph_images]

	if not graph_images:
		return []

	story: list[Any] = [_paragraph("Characterization Graphs", styles["Heading2"]), Spacer(1, 4)]
	max_width = A4[0] - 72
	max_height = A4[1] - 144
	valid_image_count = 0

	for image_source in graph_images:
		try:
			if isinstance(image_source, BytesIO):
				image_source.seek(0)
			image = Image(image_source)
			if image.imageWidth <= 0 or image.imageHeight <= 0:
				continue

			scale = min(max_width / image.imageWidth, max_height / image.imageHeight, 1)
			image.drawWidth = image.imageWidth * scale
			image.drawHeight = image.imageHeight * scale
			story.extend([image, Spacer(1, 12)])
			valid_image_count += 1
		except (OSError, TypeError, ValueError):
			continue

	return story if valid_image_count else []


def generate_characterization_pdf(
	characterization_results: Mapping[str, Any] | None = None,
	graph_images: Any = None,
) -> BytesIO:
	"""Generate a characterization PDF and return it as an in-memory file.

	Expected result keys include ``sample_info``, ``lambda_max``, ``band_gap``,
	``data_quality``, ``peaks``, and ``summary``. Missing keys are reported as
	``N/A`` rather than causing report generation to fail.
	"""
	results = characterization_results or {}
	styles = getSampleStyleSheet()
	output = BytesIO()
	document = SimpleDocTemplate(output, pagesize=A4, title="Carbon Dot Characterization Report")
	story = [
		_paragraph("Carbon Dot Characterization Report", styles["Title"]),
		Spacer(1, 8),
		_paragraph(
			f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
			styles["Normal"],
		),
		Spacer(1, 16),
	]
	story.extend(_section_table("Sample / Experiment Information", results.get("sample_info"), styles))
	story.extend(
		_section_table(
			"Lambda Max Result",
			_result_value(results, "lambda_max", "lambda max", "lambda_max_result"),
			styles,
		)
	)
	story.extend(
		_section_table(
			"Band Gap Result",
			_result_value(results, "band_gap", "band gap", "band_gap_result"),
			styles,
		)
	)
	story.extend(_section_table("Data Quality Summary", results.get("data_quality"), styles))
	story.extend(_peak_section(results.get("peaks"), styles))
	story.extend(_section_table("Characterization Summary", results.get("summary"), styles))
	story.extend(_graph_section(graph_images, styles))

	document.build(story)
	output.seek(0)
	return output


def export_processed_data(data: pd.DataFrame, export_format: str) -> BytesIO:
	"""Export a processed DataFrame as an in-memory CSV or XLSX file."""
	output = BytesIO()
	normalized_format = export_format.strip().lower().lstrip(".")

	if normalized_format == "csv":
		output.write(data.to_csv(index=False).encode("utf-8"))
	elif normalized_format in {"xlsx", "excel"}:
		with pd.ExcelWriter(output, engine="openpyxl") as writer:
			data.to_excel(writer, index=False, sheet_name="Processed Data")
	else:
		raise ValueError("Unsupported export format. Use 'CSV' or 'XLSX'.")

	output.seek(0)
	return output
