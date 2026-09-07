"""PDF reporting and prediction-data export for heavy metal detection."""

from datetime import datetime
from html import escape
from io import BytesIO
from os import PathLike
from typing import Any, Mapping
import json

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
	SimpleDocTemplate,
	Paragraph,
	Spacer,
	Table,
	TableStyle,
	Image,
)


def _display_value(value: Any) -> str:
	"""Return a readable value for missing or nested report data."""
	if value is None:
		return "N/A"
	if isinstance(value, Mapping):
		return "; ".join(
			f"{key}: {_display_value(item)}" for key, item in value.items()
		) or "N/A"
	if isinstance(value, (list, tuple, set)):
		return ", ".join(_display_value(item) for item in value) or "N/A"
	return str(value)


def _paragraph(value: Any, style: Any) -> Paragraph:
	"""Create a Paragraph with escaped result content."""
	return Paragraph(escape(_display_value(value)), style)


def _result_value(results: Mapping[str, Any], *keys: str) -> Any:
	"""Return the first present value from compatible result keys."""
	for key in keys:
		if key in results:
			return results[key]
	return None


def _section_table(title: str, value: Any, styles: Any) -> list[Any]:
	"""Build a labeled section table from a mapping or scalar value."""
	story: list[Any] = [_paragraph(title, styles["Heading2"]), Spacer(1, 4)]
	if isinstance(value, Mapping) and value:
		rows = [[_paragraph("Item", styles["Normal"]), _paragraph("Value", styles["Normal"])]]
		rows.extend(
			[_paragraph(key, styles["Normal"]), _paragraph(item, styles["Normal"])]
			for key, item in value.items()
		)
	else:
		rows = [[_paragraph(value, styles["Normal"])]]

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


def _image_section(images: Any, styles: Any) -> list[Any]:
	"""Build a section of scaled images from paths or in-memory streams."""
	if isinstance(images, (str, bytes, PathLike, BytesIO)):
		images = [images]
	if not images:
		return []

	story: list[Any] = [_paragraph("XAI Visualizations", styles["Heading2"]), Spacer(1, 4)]
	max_width = A4[0] - 72
	max_height = A4[1] - 144
	valid_image_count = 0

	for image_source in images:
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


def generate_heavy_metal_pdf(
	heavy_metal_results: Mapping[str, Any] | None = None,
	graph_images: Any = None,
	xai_images: Any = None,
) -> BytesIO:
	"""Generate a heavy metal detection PDF from completed result data.

	``graph_images`` and ``xai_images`` may contain file paths or ``BytesIO``
	objects created by visualization code. Images that cannot be read are
	skipped without preventing the report from being generated.
	"""
	results = heavy_metal_results or {}
	styles = getSampleStyleSheet()
	output = BytesIO()
	document = SimpleDocTemplate(
		output,
		pagesize=A4,
		title="Heavy Metal Detection Report",
	)
	story = [
		_paragraph("Heavy Metal Detection Report", styles["Title"]),
		Spacer(1, 8),
		_paragraph(
			f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
			styles["Normal"],
		),
		Spacer(1, 16),
	]
	story.extend(
		_section_table(
			"Detection Result",
			{
				"Detection status": _result_value(results, "detection_status", "status"),
				"Identified heavy metal": _result_value(
					results, "identified_heavy_metal", "heavy_metal", "metal"
				),
				"Prediction confidence": _result_value(
					results, "prediction_confidence", "confidence"
				),
				"Estimated concentration": _result_value(
					results, "estimated_concentration", "concentration"
				),
				"Concentration uncertainty": _result_value(
					results, "concentration_uncertainty", "uncertainty"
				),
			},
			styles,
		)
	)
	story.extend(_section_table("Detection Summary", results.get("detection_summary", results.get("summary")), styles))
	story.extend(
		_section_table(
			"XAI / Explainability Summary",
			_result_value(results, "xai_summary", "explainability_summary", "explanation"),
			styles,
		)
	)
	story.extend(_section_table("Model Performance Context", results.get("model_performance", results.get("model_context")), styles))
	image_sources: list[Any] = []
	for image_group in (graph_images, xai_images):
		if image_group is None:
			continue
		if isinstance(image_group, (list, tuple)):
			image_sources.extend(image_group)
		else:
			image_sources.append(image_group)
	story.extend(_image_section(image_sources, styles))

	document.build(story)
	output.seek(0)
	return output


def _json_safe(value: Any) -> Any:
	"""Convert common nested result values into JSON-compatible values."""
	if isinstance(value, Mapping):
		return {str(key): _json_safe(item) for key, item in value.items()}
	if isinstance(value, (list, tuple, set)):
		return [_json_safe(item) for item in value]
	if value is None or isinstance(value, (str, int, float, bool)):
		return value
	return str(value)


def export_predictions_json(
	prediction_results: Mapping[str, Any] | None = None,
	explainability_data: Mapping[str, Any] | None = None,
) -> BytesIO:
	"""Export completed prediction and SHAP/XAI data as readable JSON."""
	predictions = prediction_results or {}
	explainability = explainability_data or {}
	payload = {
		"prediction_result": _result_value(predictions, "prediction_result", "result")
		if any(key in predictions for key in ("prediction_result", "result"))
		else predictions,
		"identified_metal": _result_value(
			predictions, "identified_metal", "heavy_metal", "metal"
		),
		"confidence": _result_value(predictions, "confidence", "prediction_confidence"),
		"concentration": _result_value(predictions, "concentration", "estimated_concentration"),
		"uncertainty": _result_value(predictions, "uncertainty", "concentration_uncertainty"),
		"shap_values": _result_value(explainability, "shap_values", "shap"),
		"feature_importance": _result_value(explainability, "feature_importance"),
		"feature_contributions": _result_value(
			explainability, "feature_contributions", "contributions"
		),
		"model_information": _result_value(
			explainability, "model_information", "model_info"
		) or _result_value(predictions, "model_information", "model_info"),
	}
	output = BytesIO(json.dumps(_json_safe(payload), indent=4, default=str).encode("utf-8"))
	output.seek(0)
	return output
