# Product Requirements Document (PRD)
## Explainable AI Platform for Heavy Metal Detection Using Carbon Dot Fluorescence

| | |
|---|---|
| **Document owner** | Bhavya (Team Leader) |
| **Team size** | 4 |
| **Status** | Draft v1.0 |
| **Last updated** | 2026-09-04 |
| **Target platform** | Python / Streamlit web application |

---

## 1. Executive Summary

An AI-powered analytical platform that combines automated **carbon dot (CD) characterization** with **explainable machine-learning-based heavy metal detection, identification, and concentration estimation** from carbon-dot fluorescence sensing data.

The platform is organized into two independently usable, loosely-coupled modules:

- **Module 1 — Carbon Dot Characterization**: ingests spectroscopy data (UV-Vis, PL, FTIR, XRD) and automatically produces cleaned spectra, λmax, band-gap (direct/indirect via Tauc analysis), and a characterization report.
- **Module 2 — Heavy Metal Detection & Analysis**: ingests fluorescence/sensing response data and uses trained ML models to detect whether a heavy metal is present, identify which metal, estimate its concentration, and explain the prediction using Explainable AI (XAI).

Module 1 provides scientific context about the sensing material; Module 2 delivers the core analytical result. They share a common upload/report/export layer but run as distinct pipelines.

---

## 2. Problem Statement

Researchers currently do this work manually and across disconnected tools:

| # | Problem | Current pain | Platform solution |
|---|---|---|---|
| 1 | Manual characterization | Time-consuming manual cleaning, plotting of spectra | Automated column detection, cleaning, smoothing, plotting |
| 2 | Difficult property interpretation | λmax and band gap require manual multi-step calculation | Automatic λmax detection + direct/indirect band-gap via Tauc analysis |
| 3 | Heavy-metal detection | Fluorescence changes are hard to interpret manually, especially across multiple candidate metals | ML classifier trained on fluorescence response patterns |
| 4 | Metal identification | Detecting *a* change doesn't reveal *which* metal caused it | Multi-class classification model |
| 5 | Concentration estimation | Presence alone is insufficient; concentration is needed | Regression/calibration model |
| 6 | Black-box AI | ML predictions with no scientific justification are not trustworthy for research use | SHAP-based Explainable AI layer on every prediction |

---

## 3. Goals & Success Metrics

### 3.1 Product goals
- G1: Reduce manual spectral-processing time from hours to minutes per sample.
- G2: Provide scientifically defensible, explainable heavy-metal predictions (not just a label).
- G3: Deliver a single, visual, exportable environment covering synthesis characterization → sensing → prediction → explanation → report.
- G4: Keep the architecture simple and modular enough for a 4-person team to build, maintain, and extend within an academic timeline.

### 3.2 Success metrics (initial version)
| Metric | Target |
|---|---|
| Time to process one characterization dataset (upload → report) | < 2 minutes |
| Time to process one heavy-metal sample (upload → prediction + XAI) | < 1 minute |
| Classification accuracy (metal identification), validation set | Report honestly; target ≥ 85% as a stretch goal, not a hard requirement for v1 |
| Concentration regression R² on validation set | Report honestly; target ≥ 0.80 as a stretch goal |
| % of predictions accompanied by an XAI explanation | 100% |
| Successful report export rate | ≥ 99% of completed analyses |
| Concurrent users supported at launch | 10–50 |

> Note: ML performance targets are aspirational and depend entirely on dataset quality/size — the PRD treats model accuracy as something to be *measured and reported*, not guaranteed.

---

## 4. Target Users & Personas

| Persona | Description | Primary module used |
|---|---|---|
| **Nanomaterials researcher** | Synthesizes carbon dots, needs to characterize optical/structural properties | Module 1 |
| **Analytical/environmental chemist** | Investigates heavy-metal contamination in water via CD fluorescence sensing | Module 2 |
| **Graduate student / lab member** | Needs a fast, guided way to process raw instrument exports without scripting | Both |
| **Environmental testing lab technician** | Screens water samples, needs quick detection + concentration with justification | Module 2 |
| **Faculty / PI (reviewer)** | Reviews reports and model explanations for scientific validity | Both (report consumer) |

---

## 5. Scope

### 5.1 In scope (v1)
- Excel/CSV upload with automatic column/technique detection
- Full Module 1 pipeline: validation → cleaning/smoothing → λmax → Tauc/band gap → plots → report
- Full Module 2 pipeline: preprocessing → feature extraction → detection → identification → concentration → SHAP-based XAI → report
- Interactive Plotly visualizations + downloadable Matplotlib-quality figures
- PDF/exportable reports (characterization report, heavy-metal analysis report)
- SQLite persistence of samples, experiments, results, model runs
- Model training/evaluation workflow (offline, by the team) with versioned model artifacts loaded by the app
- Single-user / no-auth mode for v1

### 5.2 Out of scope (v1, candidate for later phases)
- Authentication, roles, permissions (email/password, admin, researcher roles)
- Multi-tenant / organization-level access control
- PostgreSQL migration
- Real-time instrument integration (direct spectrometer feed)
- Mobile app
- SOC2 / HIPAA / GDPR compliance program
- Public-facing hosted SaaS billing/subscription features

---

## 6. System Architecture Overview

Streamlit is both the frontend and the app server; Python modules underneath implement all analytical/ML logic. No separate REST API is required for v1, but the backend logic must be written as **independent, importable Python packages** (not inline in Streamlit page files) so that:
- it is unit-testable without the UI,
- it can later be wrapped behind a FastAPI service if the platform needs to scale beyond Streamlit's single-process model.

```
                          STREAMLIT MULTI-PAGE APP
                                    │
                 ┌──────────────────┴───────────────────┐
                 │                                       │
                 ▼                                       ▼
     MODULE 1: CD CHARACTERIZATION           MODULE 2: HEAVY METAL ANALYSIS
                 │                                       │
     ┌───────────┼────────────┐              ┌───────────┼────────────┐
     ▼           ▼            ▼              ▼           ▼            ▼
  UV-Vis        PL        FTIR / XRD      Preprocess   ML Models   Explainable AI
     │                                        │             │            │
     ▼                                        ▼             ▼            ▼
Tauc & Band-Gap                          Feature      Detect /     SHAP explanations
   Analysis                              Extraction   Identify /
     │                                        │        Quantify
     └────────────────┬───────────────────────┘
                       ▼
              VISUALIZATION LAYER (Plotly / Matplotlib)
                       ▼
              REPORT & EXPORT LAYER (ReportLab / PDF, CSV, PNG)
                       ▼
                    SQLite (samples, experiments, results, model runs)
```

### 6.1 Recommended repository/package structure

```
carbondot-platform/
├── app/
│   ├── Home.py                        # Streamlit entry point
│   └── pages/
│       ├── 1_Characterization.py
│       ├── 2_Heavy_Metal_Detection.py
│       ├── 3_Explainable_AI.py
│       ├── 4_Reports_Export.py
│       └── 5_History.py
├── core/
│   ├── ingestion/
│   │   ├── file_loader.py             # Excel/CSV load, sheet handling
│   │   └── column_detector.py         # auto-detect technique & columns
│   ├── characterization/
│   │   ├── validation.py
│   │   ├── cleaning.py                # smoothing, artifact/outlier removal
│   │   ├── uvvis.py                   # λmax, absorption features, energy
│   │   ├── tauc.py                    # direct/indirect band gap
│   │   ├── pl.py
│   │   ├── ftir.py
│   │   └── xrd.py
│   ├── heavy_metal/
│   │   ├── preprocessing.py
│   │   ├── feature_extraction.py
│   │   ├── detection_model.py         # binary: metal present / absent
│   │   ├── identification_model.py    # multiclass: which metal
│   │   ├── concentration_model.py     # regression
│   │   └── model_registry.py          # load/version trained models
│   ├── xai/
│   │   └── shap_explainer.py
│   ├── viz/
│   │   ├── characterization_plots.py
│   │   └── heavy_metal_plots.py
│   ├── reporting/
│   │   ├── characterization_report.py
│   │   └── heavy_metal_report.py
│   └── db/
│       ├── models.py                  # SQLite schema (SQLAlchemy)
│       ├── session.py
│       └── crud.py
├── ml_training/
│   ├── datasets/
│   ├── train_detection.py
│   ├── train_identification.py
│   ├── train_concentration.py
│   └── evaluate.py
├── models/                            # serialized trained model artifacts
├── tests/
│   ├── test_characterization.py
│   ├── test_heavy_metal.py
│   └── test_ingestion.py
├── data/
│   └── sample_datasets/
├── requirements.txt
└── README.md
```

---

## 7. Functional Requirements — Module 1: Carbon Dot Characterization

### 7.1 Upload & Ingestion
- FR1.1: Accept `.xlsx`, `.xls`, `.csv` uploads.
- FR1.2: Auto-detect which technique(s) are present (UV-Vis, PL, FTIR, XRD) based on column headers/patterns, without requiring a fixed template.
- FR1.3: Show a data preview (first N rows, detected columns, detected technique) before processing.
- FR1.4: Validate file structure; reject/flag malformed files with a clear, specific error message (not a stack trace).

### 7.2 Data Processing
- FR2.1: Detect missing values and invalid values (non-numeric, out-of-range) per column.
- FR2.2: Detect spectral artifacts/noise (e.g., spikes, cosmic rays, baseline drift).
- FR2.3: Clean data (interpolate/remove invalid points) and apply configurable smoothing (e.g., Savitzky-Golay).
- FR2.4: Preserve an audit trail: raw data vs. cleaned data must both be retrievable.

### 7.3 UV-Vis Analysis
- FR3.1: Plot wavelength vs. absorption.
- FR3.2: Automatically detect λmax.
- FR3.3: Identify/annotate absorption features (shoulders, secondary peaks).
- FR3.4: Calculate photon energy: `E = hν = 1240 / λ` (λ in nm, E in eV).

### 7.4 Tauc / Band-Gap Analysis
- FR4.1: Auto-generate Tauc plot from absorption + energy data.
- FR4.2: Calculate direct band gap: `Eg_direct = (2.303 × A × E)^2`.
- FR4.3: Calculate indirect band gap: `Eg_indirect = (2.303 × A × E)^0.5`.
- FR4.4: Display both values with the fitted region highlighted on the Tauc plot.

### 7.5 PL / FTIR / XRD Analysis
- FR5.1 (PL): Plot PL spectrum; detect emission peak(s); summarize fluorescence response shape.
- FR5.2 (FTIR): Plot FTIR spectrum; detect peaks; assign/label known functional-group absorption bands where identifiable.
- FR5.3 (XRD): Plot intensity vs. 2θ; detect peaks; report structural/crystallinity indicators (e.g., approximate d-spacing from peak position where feasible).

### 7.6 Visualization
- FR6.1: All plots interactive (zoom/pan/hover) via Plotly.
- FR6.2: "All columns" comparison view — every detected data series plotted together and individually.
- FR6.3: Annotated λmax, band-gap fit region, and detected peaks shown directly on plots.

### 7.7 Reporting
- FR7.1: Generate a Characterization Report containing: detected λmax, band gap (direct & indirect), detected peaks/features, data-quality summary, all plots, and technique-wise summary.
- FR7.2: Export report as PDF; export processed data as CSV/Excel; export plots as PNG.
- FR7.3: Persist each characterization run (inputs, parameters, results) to the database for later retrieval (History page).

---

## 8. Functional Requirements — Module 2: Heavy Metal Detection & Analysis

### 8.1 Upload & Preprocessing
- FR8.1: Accept fluorescence/sensing response datasets (Excel/CSV).
- FR8.2: Validate and preprocess (missing value handling, normalization/scaling consistent with the trained models).
- FR8.3: Extract relevant features (e.g., intensity change, emission wavelength shift, intensity ratio, spectral shape descriptors) via a documented, reusable feature-extraction pipeline shared between training and inference.

### 8.2 Detection
- FR9.1: Run the trained binary classifier to determine heavy-metal presence.
- FR9.2: Display result clearly: **Heavy Metal Detected: YES/NO** with model confidence.

### 8.3 Identification
- FR10.1: If detected, run the multiclass classifier over the supported metal set (configurable; e.g., Pb, Hg, Cd, Cr, Cu — dependent on training data availability).
- FR10.2: Display identified metal + prediction confidence/probability distribution across all candidate metals.
- FR10.3: If confidence is below a configurable threshold, flag the result as "low confidence — inconclusive" rather than presenting a false-certain answer.

### 8.4 Concentration Estimation
- FR11.1: Run the regression/calibration model for the identified metal to estimate concentration (units: ppm, or as appropriate to the training data).
- FR11.2: Display estimated concentration with an uncertainty range where the model supports it (e.g., prediction interval, or cross-validated RMSE shown alongside the point estimate).
- FR11.3: If reference/actual concentration is available (e.g., known standard used for validation), show actual vs. predicted.

### 8.5 Explainable AI
- FR12.1: Generate a SHAP explanation for every detection, identification, and concentration prediction.
- FR12.2: Show global feature importance (which features matter most overall) and local/per-sample explanation (why *this* sample got *this* prediction).
- FR12.3: Present contributions as both a table (feature → contribution level/sign) and a visual (e.g., SHAP bar/waterfall plot).
- FR12.4: Show model performance context: confusion matrix (identification), accuracy/precision/recall, actual-vs-predicted plot and error metrics (concentration).

### 8.6 Reporting
- FR13.1: Generate a Heavy Metal Analysis Report: detection result, identified metal + confidence, concentration + uncertainty, XAI visuals, model performance context.
- FR13.2: Export as PDF; export raw predictions and SHAP values as CSV/JSON.
- FR13.3: Persist each run to the database.

---

## 9. Non-Functional Requirements

| Category | Requirement |
|---|---|
| **Performance** | Characterization pipeline completes in < 2 min for a typical dataset (<10k rows); heavy-metal prediction + XAI completes in < 1 min per sample. |
| **Usability** | No coding required by end users; every upload gets a clear preview + validation feedback before processing runs. |
| **Reliability** | Invalid/malformed uploads must fail gracefully with actionable error messages, never a raw Python traceback shown to the user. |
| **Interpretability** | Every ML output must be accompanied by an explanation — this is a hard product requirement, not optional polish. |
| **Data integrity** | Raw uploaded data is never overwritten; processed/cleaned data is stored separately and traceably. |
| **Maintainability** | Analytical logic lives in `core/`, fully decoupled from Streamlit UI code, and is unit-tested independently. |
| **Extensibility** | Adding a new target metal or a new characterization technique should not require restructuring the pipeline — new modules plug into the existing `core/` package layout. |
| **Security (basic)** | Validate file types/size before processing; sanitize file names; no execution of uploaded file content; no PII collected. |
| **Deployment** | Must run via `streamlit run app/Home.py` locally and be deployable to Streamlit Community Cloud or a single VM/container without additional infrastructure. |
| **Scale** | Designed for 10–50 concurrent academic users; no requirement for horizontal scaling, load balancing, or multi-region deployment in v1. |

---

## 10. Data Model (SQLite, v1)

Core entities (exact schema to be implemented with SQLAlchemy in `core/db/models.py`):

- **Sample** — id, name/label, description, created_at, source_module (characterization/heavy_metal), notes
- **Experiment** — id, sample_id (FK), technique (UV-Vis/PL/FTIR/XRD/Fluorescence), raw_file_ref, uploaded_at, status
- **CharacterizationResult** — id, experiment_id (FK), lambda_max, eg_direct, eg_indirect, detected_features (JSON), data_quality_summary (JSON), plot_refs (JSON), created_at
- **HeavyMetalPrediction** — id, experiment_id (FK), detected (bool), detection_confidence, identified_metal, identification_confidence, concentration_value, concentration_uncertainty, model_version, created_at
- **XAIExplanation** — id, prediction_id (FK), explanation_type (detection/identification/concentration), shap_values (JSON), feature_importance (JSON), plot_ref
- **ModelRun** (training metadata) — id, model_type, model_version, trained_at, dataset_ref, metrics (JSON), artifact_path
- **Report** — id, experiment_id (FK), report_type, file_path, generated_at

---

## 11. Tech Stack (confirmed)

| Layer | Technology |
|---|---|
| UI / App server | Streamlit (multi-page app) |
| Language | Python 3.11+ |
| Data processing | Pandas, NumPy |
| Scientific/signal processing | SciPy (smoothing, peak detection) |
| Machine learning | Scikit-learn, XGBoost |
| Explainable AI | SHAP |
| Visualization | Plotly (interactive), Matplotlib (publication-style export) |
| Excel handling | OpenPyXL, Pandas |
| Database | SQLite (SQLAlchemy ORM) |
| Reporting | ReportLab (PDF generation) |
| Testing | Pytest |

---

## 12. User Journeys

### 12.1 Characterization journey
`Upload Excel/CSV → Select "Characterization" → Auto-detect technique/columns → Preview → Validate → Clean/Smooth → Analyze (λmax, Tauc, band gap, peaks) → Visualize → Generate report → Export`

### 12.2 Heavy metal journey
`Upload fluorescence dataset → Select "Heavy Metal Analysis" → Preprocess → Extract features → Detect (Y/N) → If Y: Identify metal → Estimate concentration → Generate SHAP explanation → Visualize → Generate report → Export`

### 12.3 Cross-cutting
`History page → browse past samples/experiments → re-open results/report without re-running analysis`

---

## 13. Team & Roles

| Person | Role | Primary responsibility | Git branch |
|---|---|---|---|
| **Bhavya** | Leader | Main project ownership, code review, integration of all branches into `main`, architecture decisions, release management | `main` |
| **Archit** | Member 1 | Data processing — ingestion, column auto-detection, validation, cleaning/smoothing, feature extraction pipelines (shared by both modules) | `data-processing` |
| **Bhumi** | Member 2 | Visualization/graphs — all Plotly/Matplotlib plots (UV-Vis, Tauc, PL, FTIR, XRD, fluorescence, SHAP, confusion matrix, actual-vs-predicted) | `visualization` |
| **Abhishek** | Member 3 | UI + additional features — Streamlit pages/UX, Reports & Export page, History page, report generation (PDF/CSV), any stretch features | `app-development` |

**Workflow convention:** each member works on their own feature branch, opens a PR into `main`, Bhavya reviews and merges. `core/` modules should be built so that Data Processing (Archit) and Visualization (Bhumi) can work in parallel without blocking each other — Archit owns everything under `core/ingestion/`, `core/characterization/` (processing side), `core/heavy_metal/preprocessing.py` and `feature_extraction.py`; Bhumi owns `core/viz/*` and consumes the outputs Archit's functions produce, agreed on via a shared interface (e.g., a documented DataFrame/dict schema) early in Phase 0 so both can build against a stable contract.

ML model work (detection/identification/concentration models + XAI) and Reporting/UI don't map to a single named member above — the team should decide who leads `core/heavy_metal/{detection,identification,concentration}_model.py`, `core/xai/shap_explainer.py`, and `ml_training/*`. Given the current split, the natural fit is:
- **Bhavya (Leader)**, alongside integration duties, owns the ML models + XAI layer (`core/heavy_metal/*_model.py`, `core/xai/shap_explainer.py`, `ml_training/*`), since this is the core scientific/analytical engine and benefits from the leader's cross-module visibility.
- **Abhishek** owns Reports & Export and History pages (`core/reporting/*`, `4_Reports_Export.py`, `5_History.py`) in addition to general UI/app-development, since these sit naturally alongside the Streamlit page work.

Adjust this pairing if someone on the team has stronger ML background — that person should take the model/XAI ownership regardless of title.

## 14. Development Phases

| Phase | Scope | Owner(s) |
|---|---|---|
| **Phase 0 — Foundations** | Repo scaffold, Streamlit skeleton, DB schema, file ingestion + column auto-detection, sample datasets, shared data-contract agreed across the team | Bhavya (scaffold/DB) + Archit (ingestion) |
| **Phase 1 — Module 1 (Characterization)** | Cleaning/smoothing, UV-Vis + λmax, Tauc/band gap, PL/FTIR/XRD processing | Archit (processing logic) + Bhumi (plots) |
| **Phase 2 — Module 2 core (ML)** | Feature extraction, detection model, identification model, concentration model, offline training scripts + evaluation | Archit (feature extraction) + Bhavya (models) |
| **Phase 3 — Explainable AI** | SHAP integration for all three predictions, global + local explanation views + XAI plots | Bhavya (SHAP logic) + Bhumi (XAI plots) |
| **Phase 4 — Reporting & Export** | PDF report generation for both modules, CSV/PNG export, History page | Abhishek |
| **Phase 5 — UI Assembly** | All Streamlit pages (`app/pages/*`), wiring `core/` functions into the UI, UX polish | Abhishek, consuming outputs from Archit/Bhumi/Bhavya |
| **Phase 6 — Polish & Integration** | End-to-end testing, error handling, branch merges into `main`, deployment | Whole team, led by Bhavya |

This split is intentionally parallelizable: once Phase 0's shared data contract is agreed, Archit (data-processing), Bhumi (visualization), and Bhavya (ML/XAI) can build largely independently, with Abhishek assembling their outputs into the final UI and reports in Phases 4–5.

---

## 15. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Insufficient/small training dataset for ML models | Poor identification/concentration accuracy | Report metrics honestly; use cross-validation; consider simpler baseline models (Random Forest, linear regression) before complex ones; treat model accuracy as a research finding, not a fixed spec |
| Heterogeneous instrument export formats (different column names/layouts across labs) | Column auto-detection fails | Build detection with fuzzy/heuristic matching + a manual column-mapping fallback UI |
| Streamlit's single-process model under concurrent use | Slowness with multiple simultaneous users | Acceptable at 10–50 user scale; document FastAPI-backend migration path if this becomes a bottleneck |
| SHAP computation cost on large feature sets | Slow XAI generation | Cache SHAP explainer per model version; use TreeExplainer for tree-based models (fast, exact) |
| No authentication in v1 | Any user can see all samples/history | Acceptable for single-lab v1 use; documented as a known limitation, roadmap item for Phase 6 |

---

## 16. Future Enhancements (post-v1)

- Authentication & role-based access (researcher/admin)
- PostgreSQL migration for multi-user/multi-lab deployment
- FastAPI backend to decouple UI from analysis logic
- Additional target metals as more training data becomes available
- Batch processing (multiple samples per upload)
- Direct instrument/API integration
- Model retraining workflow accessible from the UI (not just offline scripts)

---

## 17. Appendix A — Key Formulas

- Photon energy: `E = hν = 1240 / λ` (λ in nm → E in eV)
- Direct band gap (Tauc): `Eg_direct = (2.303 × A × E)^2`
- Indirect band gap (Tauc): `Eg_indirect = (2.303 × A × E)^0.5`

Where `A` = absorbance, `E` = photon energy (eV).

---

## 18. Appendix B — Detailed Module & Function Specification

This appendix specifies every file under `core/`, `ml_training/`, and `app/`, its functions, exact signatures, inputs/outputs, and behavior. This is the level of detail each branch owner should build against. Types are given as Python type hints; `DataFrame` = `pandas.DataFrame`.

### 18.1 `core/ingestion/` — owned by Archit (`data-processing`)

#### `file_loader.py`
| Function | Signature | Description |
|---|---|---|
| `load_file` | `load_file(file) -> DataFrame` | Accepts a Streamlit `UploadedFile` or file path. Detects extension (`.xlsx`, `.xls`, `.csv`) and dispatches to the correct reader (`pandas.read_excel` / `pandas.read_csv`). Raises `UnsupportedFileTypeError` (custom exception, not raw pandas error) on invalid extensions. |
| `list_sheets` | `list_sheets(file) -> list[str]` | For Excel files with multiple sheets, returns sheet names so the UI can let the user pick one. Returns `["Sheet1"]` equivalent for CSV. |
| `load_sheet` | `load_sheet(file, sheet_name: str) -> DataFrame` | Loads a specific sheet by name. |

#### `column_detector.py`
| Function | Signature | Description |
|---|---|---|
| `detect_technique` | `detect_technique(df: DataFrame) -> str` | Returns one of `"uvvis"`, `"pl"`, `"ftir"`, `"xrd"`, `"fluorescence"`, or `"unknown"`. Uses a heuristic keyword-matching scheme against column headers (case-insensitive, fuzzy — e.g. "wavelength(nm)" matches "wavelength"). |
| `detect_columns` | `detect_columns(df: DataFrame, technique: str) -> dict[str, str]` | Returns a mapping of logical role → actual column name, e.g. `{"x": "Wavelength (nm)", "y": "Absorbance"}`. This mapping is what every downstream analysis function consumes — **this is the shared contract** referenced in the build prompt's "contract-first rule." |
| `get_manual_mapping_options` | `get_manual_mapping_options(df: DataFrame) -> list[str]` | Returns the list of column names for the UI's manual-mapping fallback dropdown when auto-detection is ambiguous or fails. |

---

### 18.2 `core/characterization/` — owned by Archit (processing), consumed by Bhumi (plots)

#### `validation.py`
| Function | Signature | Description |
|---|---|---|
| `validate_spectrum` | `validate_spectrum(df: DataFrame, col_map: dict) -> ValidationReport` | Runs missing-value, non-numeric-value, out-of-range, and empty-column checks. `ValidationReport` is a small dataclass: `{is_valid: bool, warnings: list[str], errors: list[str], missing_count: int, invalid_count: int}`. Never raises — always returns a report the UI renders as a checklist. |

#### `cleaning.py`
| Function | Signature | Description |
|---|---|---|
| `handle_missing_values` | `handle_missing_values(df: DataFrame, col_map: dict, method: str = "interpolate") -> DataFrame` | Interpolates or drops missing values per `method` (`"interpolate"` \| `"drop"` \| `"ffill"`). |
| `detect_artifacts` | `detect_artifacts(y: np.ndarray, z_thresh: float = 3.0) -> np.ndarray` | Returns a boolean mask flagging spike/outlier points via rolling z-score or rolling-median deviation. |
| `smooth_spectrum` | `smooth_spectrum(y: np.ndarray, window: int = 11, polyorder: int = 3) -> np.ndarray` | Applies `scipy.signal.savgol_filter`. Window/polyorder configurable from the UI (with sane defaults + validation that window > polyorder and is odd). |
| `clean_pipeline` | `clean_pipeline(df: DataFrame, col_map: dict, config: CleaningConfig) -> CleanedResult` | Orchestrates the above three; returns `CleanedResult{raw: DataFrame, cleaned: DataFrame, artifact_mask: np.ndarray, params_used: dict}`. Raw data is always preserved. |

#### `uvvis.py`
| Function | Signature | Description |
|---|---|---|
| `find_lambda_max` | `find_lambda_max(wavelength: np.ndarray, absorbance: np.ndarray) -> float` | Uses `scipy.signal.find_peaks` on the absorbance curve, falls back to `argmax` if no peak found by prominence threshold. Returns λmax in nm. |
| `find_absorption_features` | `find_absorption_features(wavelength: np.ndarray, absorbance: np.ndarray, prominence: float = 0.02) -> list[dict]` | Returns list of `{wavelength, absorbance, type: "shoulder"|"peak"}` for secondary features. |
| `compute_photon_energy` | `compute_photon_energy(wavelength_nm: np.ndarray) -> np.ndarray` | Vectorized `E = 1240 / λ`. |

#### `tauc.py`
| Function | Signature | Description |
|---|---|---|
| `build_tauc_arrays` | `build_tauc_arrays(absorbance: np.ndarray, energy_ev: np.ndarray, mode: str) -> tuple[np.ndarray, np.ndarray]` | `mode` is `"direct"` or `"indirect"`. Returns `(x, y)` arrays for the Tauc plot: `y = (2.303*A*E)**2` (direct) or `**0.5` (indirect), `x = energy_ev`. |
| `fit_band_gap` | `fit_band_gap(x: np.ndarray, y: np.ndarray, fit_window: tuple[float, float] | None = None) -> BandGapResult` | Fits a line to the steepest linear region of the Tauc curve (auto-detected via max-derivative window if `fit_window` not given) and extrapolates the x-intercept. Returns `BandGapResult{eg_value: float, fit_slope: float, fit_intercept: float, fit_x_range: tuple}`. |
| `compute_band_gaps` | `compute_band_gaps(absorbance, energy_ev) -> dict` | Convenience wrapper returning `{"direct": BandGapResult, "indirect": BandGapResult}`. |

#### `pl.py` / `ftir.py` / `xrd.py`
| Function | Signature | Description |
|---|---|---|
| `find_peaks_generic` | `find_peaks_generic(x: np.ndarray, y: np.ndarray, **kwargs) -> list[dict]` | Shared peak-detection wrapper (used by all three) returning `[{x, y, prominence}]`. |
| `pl.py: summarize_emission` | `summarize_emission(wavelength, intensity) -> dict` | Returns `{peak_wavelength, fwhm, peak_intensity}`. |
| `ftir.py: assign_functional_groups` | `assign_functional_groups(peaks: list[dict], reference_table: dict) -> list[dict]` | Matches detected wavenumber peaks (±tolerance) against a bundled reference table of common functional groups (e.g., O–H, C=O, N–H); returns best-effort labeled peaks. |
| `xrd.py: estimate_d_spacing` | `estimate_d_spacing(two_theta_deg: float, wavelength_angstrom: float = 1.5406) -> float` | Bragg's law: `d = λ / (2 sin θ)`, θ in radians = `two_theta_deg/2` converted. Default wavelength is Cu-Kα. |

---

### 18.3 `core/heavy_metal/` — feature extraction owned by Archit; models owned by Bhavya

#### `preprocessing.py` (Archit)
| Function | Signature | Description |
|---|---|---|
| `validate_fluorescence_data` | `validate_fluorescence_data(df: DataFrame, col_map: dict) -> ValidationReport` | Same pattern as characterization's validator, adapted to fluorescence data columns. |
| `apply_scaler` | `apply_scaler(X: np.ndarray, scaler_path: str, fit: bool = False) -> np.ndarray` | If `fit=True` (training time only), fits and saves a `StandardScaler`/`MinMaxScaler` to `scaler_path`. At inference, always `fit=False` — loads the persisted scaler and transforms. This prevents train/inference skew. |

#### `feature_extraction.py` (Archit) — **shared by training and inference, single source of truth**
| Function | Signature | Description |
|---|---|---|
| `extract_features` | `extract_features(df: DataFrame, col_map: dict) -> dict[str, float]` | Returns a flat dict of named features. Must include at minimum: `delta_f_over_f0` (fluorescence intensity change), `emission_shift_nm`, `intensity_ratio`, `peak_width`, `spectral_skewness`, `spectral_kurtosis`. Each feature has a one-line docstring inline explaining its physical meaning. |
| `features_to_vector` | `features_to_vector(features: dict, feature_order: list[str]) -> np.ndarray` | Converts the dict to an ordered numpy array matching the order the model was trained on (order persisted in `model_registry`). |

#### `detection_model.py` (Bhavya)
| Function | Signature | Description |
|---|---|---|
| `train_detection_model` | `train_detection_model(X: np.ndarray, y: np.ndarray, model_type: str = "random_forest") -> tuple[model, dict]` | Trains binary classifier (`random_forest` \| `xgboost`), returns fitted model + metrics dict (`accuracy`, `precision`, `recall`, `f1`, `roc_auc` via cross-validation). |
| `predict_detection` | `predict_detection(model, X: np.ndarray) -> tuple[bool, float]` | Returns `(is_detected, confidence)` where confidence is `predict_proba` of the positive class. |

#### `identification_model.py` (Bhavya)
| Function | Signature | Description |
|---|---|---|
| `train_identification_model` | `train_identification_model(X, y, metal_classes: list[str], model_type="random_forest") -> tuple[model, dict]` | Multiclass classifier over `metal_classes` (config constant, e.g. `["Pb","Hg","Cd","Cr","Cu"]`). Returns model + metrics (`accuracy`, per-class precision/recall, confusion matrix array). |
| `predict_identification` | `predict_identification(model, X: np.ndarray, threshold: float = 0.6) -> IdentificationResult` | `IdentificationResult{metal: str, confidence: float, probabilities: dict[str,float], is_confident: bool}`. `is_confident = confidence >= threshold`; UI must flag `False` cases as "inconclusive." |

#### `concentration_model.py` (Bhavya)
| Function | Signature | Description |
|---|---|---|
| `train_concentration_model` | `train_concentration_model(X, y, model_type="random_forest") -> tuple[model, dict]` | Regression model (`random_forest` \| `xgboost` \| `svr`). Returns model + metrics (`rmse`, `mae`, `r2`, all cross-validated). |
| `predict_concentration` | `predict_concentration(model, X: np.ndarray) -> ConcentrationResult` | `ConcentrationResult{value: float, uncertainty: float}` — uncertainty from cross-validated RMSE (constant) or a proper prediction interval if the model type supports it (e.g., quantile regression variant). |

#### `model_registry.py` (Bhavya)
| Function | Signature | Description |
|---|---|---|
| `load_model` | `load_model(model_type: str, version: str = "latest") -> LoadedModel` | `model_type` is `"detection"` \| `"identification"` \| `"concentration"`. `LoadedModel{model, scaler, feature_order, version, metrics}`. This is the **only** place `app/` code should touch model artifacts. |
| `list_versions` | `list_versions(model_type: str) -> list[str]` | Lists available versions in `models/` for the History/admin views. |

---

### 18.4 `core/xai/shap_explainer.py` — owned by Bhavya (logic), Bhumi (plots consume this)

| Function | Signature | Description |
|---|---|---|
| `get_explainer` | `get_explainer(loaded_model: LoadedModel) -> shap.TreeExplainer` | Builds (and caches, keyed by model version) a `TreeExplainer` for tree-based models. |
| `explain_prediction` | `explain_prediction(explainer, X_sample: np.ndarray, feature_names: list[str]) -> LocalExplanation` | `LocalExplanation{shap_values: np.ndarray, feature_names: list[str], base_value: float}` for one sample — feeds the waterfall/force plot. |
| `global_feature_importance` | `global_feature_importance(explainer, X_reference: np.ndarray, feature_names: list[str]) -> DataFrame` | Returns a ranked DataFrame `[feature, mean_abs_shap]` sorted descending — feeds the global importance bar chart. |
| `model_performance_summary` | `model_performance_summary(model_type: str, metrics: dict) -> dict` | Passes through stored training-time metrics (confusion matrix, R², RMSE, etc.) for display alongside the explanation, so XAI page always has performance context, not just per-sample attribution. |

---

### 18.5 `core/viz/` — owned by Bhumi (`visualization`)

#### `characterization_plots.py`
| Function | Signature | Description |
|---|---|---|
| `plot_uvvis` | `plot_uvvis(wavelength, absorbance, lambda_max: float, features: list[dict]) -> plotly.Figure` | Absorption plot with λmax and feature annotations. |
| `plot_tauc` | `plot_tauc(x, y, fit_result: BandGapResult, mode: str) -> plotly.Figure` | Tauc plot with the fitted line and x-intercept (band gap) highlighted. |
| `plot_pl` / `plot_ftir` / `plot_xrd` | `plot_pl(wavelength, intensity, peaks) -> plotly.Figure` (same pattern for FTIR/XRD) | Spectrum plot with detected peaks annotated. |
| `plot_all_columns` | `plot_all_columns(df: DataFrame, col_map: dict) -> plotly.Figure` | Overlay/comparison view of every detected data series. |
| `figure_to_png_bytes` | `figure_to_png_bytes(fig) -> bytes` | Renders any of the above to PNG bytes for embedding in the PDF report (used by Abhishek's reporting code). |

#### `heavy_metal_plots.py`
| Function | Signature | Description |
|---|---|---|
| `plot_fluorescence_spectrum` | `plot_fluorescence_spectrum(x, y) -> plotly.Figure` | Raw sensing-response plot. |
| `plot_detection_badge` | `plot_detection_badge(detected: bool, confidence: float) -> plotly.Figure \| dict` | Visual YES/NO indicator with confidence. |
| `plot_identification_probabilities` | `plot_identification_probabilities(probabilities: dict[str,float], threshold: float) -> plotly.Figure` | Bar chart of per-metal probability, with the confidence threshold line drawn in. |
| `plot_concentration_estimate` | `plot_concentration_estimate(value: float, uncertainty: float, actual: float \| None = None) -> plotly.Figure` | Point estimate + uncertainty band; overlays actual value if provided. |
| `plot_shap_waterfall` | `plot_shap_waterfall(local_explanation: LocalExplanation) -> plotly.Figure` | Per-sample SHAP waterfall. |
| `plot_global_importance` | `plot_global_importance(importance_df: DataFrame) -> plotly.Figure` | Global feature-importance bar chart. |
| `plot_confusion_matrix` | `plot_confusion_matrix(cm: np.ndarray, class_labels: list[str]) -> plotly.Figure` | Heatmap. |
| `plot_actual_vs_predicted` | `plot_actual_vs_predicted(actual: np.ndarray, predicted: np.ndarray) -> plotly.Figure` | Scatter + ideal-fit line, with R²/RMSE annotated. |

---

### 18.6 `core/reporting/` — owned by Abhishek (`app-development`)

#### `characterization_report.py`
| Function | Signature | Description |
|---|---|---|
| `generate_characterization_pdf` | `generate_characterization_pdf(result: CharacterizationResult, figures: list[bytes], output_path: str) -> str` | Builds the PDF via ReportLab: header, λmax, band gaps, data-quality summary, embedded plot images. Returns the file path written. |
| `export_processed_data` | `export_processed_data(df: DataFrame, output_path: str, fmt: str = "csv") -> str` | `fmt` is `"csv"` \| `"xlsx"`. |

#### `heavy_metal_report.py`
| Function | Signature | Description |
|---|---|---|
| `generate_heavy_metal_pdf` | `generate_heavy_metal_pdf(prediction: HeavyMetalPrediction, explanation: LocalExplanation, figures: list[bytes], output_path: str) -> str` | Same pattern: detection/identification/concentration results + all XAI visuals + model performance context. |
| `export_predictions_json` | `export_predictions_json(prediction: HeavyMetalPrediction, explanation: LocalExplanation, output_path: str) -> str` | Raw predictions + SHAP values as JSON for programmatic reuse. |

---

### 18.7 `core/db/` — scaffolded by Bhavya, used by everyone

#### `models.py`
SQLAlchemy ORM classes for every entity in Section 10: `Sample`, `Experiment`, `CharacterizationResult`, `HeavyMetalPrediction`, `XAIExplanation`, `ModelRun`, `Report`. Each with `to_dict()` for easy Streamlit rendering.

#### `session.py`
| Function | Signature | Description |
|---|---|---|
| `get_engine` | `get_engine(db_path: str = "sqlite:///carbondot.db") -> Engine` | Single engine factory, swappable connection string for future Postgres migration. |
| `get_session` | `get_session() -> Session` | Context-managed session for use in `crud.py`. |

#### `crud.py`
| Function | Signature | Description |
|---|---|---|
| `create_sample` | `create_sample(name: str, description: str, source_module: str) -> Sample` | |
| `create_experiment` | `create_experiment(sample_id: int, technique: str, raw_file_ref: str) -> Experiment` | |
| `save_characterization_result` | `save_characterization_result(experiment_id: int, **fields) -> CharacterizationResult` | |
| `save_heavy_metal_prediction` | `save_heavy_metal_prediction(experiment_id: int, **fields) -> HeavyMetalPrediction` | |
| `save_xai_explanation` | `save_xai_explanation(prediction_id: int, **fields) -> XAIExplanation` | |
| `save_report` | `save_report(experiment_id: int, report_type: str, file_path: str) -> Report` | |
| `list_experiments` | `list_experiments(source_module: str \| None = None) -> list[Experiment]` | Powers the History page. |
| `get_experiment_detail` | `get_experiment_detail(experiment_id: int) -> dict` | Joins Experiment + its Result/Prediction/Explanation/Report rows into one dict for re-display without re-running analysis. |

---

### 18.8 `ml_training/` — owned by Bhavya

| Script | Responsibility |
|---|---|
| `train_detection.py` | Loads training dataset from `datasets/`, runs `feature_extraction.extract_features` on each row, calls `detection_model.train_detection_model`, persists model + scaler + metrics to `models/`, registers a `ModelRun` row. |
| `train_identification.py` | Same pattern for `identification_model.py`, over the configured `METAL_CLASSES` constant. |
| `train_concentration.py` | Same pattern for `concentration_model.py`, trained per identified metal (or globally with metal as a feature — decision documented in code comments). |
| `evaluate.py` | Re-runs all three trained models against a held-out test split and prints/saves a consolidated metrics report — used before promoting a new model version to "latest" in `model_registry`. |

---

### 18.9 `app/` — owned by Abhishek, consuming all `core/` functions above

Each page in `app/pages/` should contain **only**: Streamlit widgets (`st.file_uploader`, `st.button`, `st.tabs`, `st.plotly_chart`, `st.download_button`) and calls into the `core/` functions specified above — no analytical logic inline. Section 7 of this PRD (Streamlit pages) defines what each page must display; this section defines what it calls to get that data.

Example call chain for `1_Characterization.py`:
```
file_loader.load_file()
→ column_detector.detect_technique() / detect_columns()
→ validation.validate_spectrum()
→ cleaning.clean_pipeline()
→ uvvis.find_lambda_max() / find_absorption_features() / compute_photon_energy()
→ tauc.compute_band_gaps()
→ characterization_plots.plot_uvvis() / plot_tauc()
→ crud.save_characterization_result()
→ characterization_report.generate_characterization_pdf()   (on export)
```

Example call chain for `2_Heavy_Metal_Detection.py`:
```
file_loader.load_file()
→ preprocessing.validate_fluorescence_data()
→ feature_extraction.extract_features() → features_to_vector()
→ model_registry.load_model("detection") → detection_model.predict_detection()
→ (if detected) model_registry.load_model("identification") → identification_model.predict_identification()
→ model_registry.load_model("concentration") → concentration_model.predict_concentration()
→ shap_explainer.get_explainer() → explain_prediction()
→ heavy_metal_plots.* (all result + XAI plots)
→ crud.save_heavy_metal_prediction() / save_xai_explanation()
→ heavy_metal_report.generate_heavy_metal_pdf()   (on export)
```
