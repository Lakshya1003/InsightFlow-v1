# Insight Flow — Codebase Functionality Overview

This document provides a deep dive into the architecture of the **Insight Flow** project. It explains the purpose of each file and details how every function operates within the system to deliver an AI-assisted business analytics dashboard.

---

## 1. `app.py`
**Purpose:** This is the main entry point for the Streamlit application. It acts as the central controller, binding together the UI, data processing, analytics, and AI logic.

**Key Functions:**
- `rwin_open(title, icon)` / `rwin_close()`: Generates raw HTML wrappers to render retro-styled window components in the UI.
- `kpi_html(label, value, delta)`: Generates the HTML layout for the Key Performance Indicator (KPI) cards, incorporating value formatting and dynamic growth indicators.
- `period_html(title, icon, value, detail)`: Generates the HTML layout for the "Best/Lowest Performing" period highlight cards.
- `get_gemini()`: A helper function that safely retrieves the `GeminiHandler` instance stored in Streamlit's session state.
- `status_html()`: Returns HTML badges indicating the live connection status of the Gemini API (Connected, Invalid Key, or Offline).
- `btn_group(options, key, cols_per_row)`: Dynamically builds retro-styled button group selectors for the sidebar. It updates session state immediately when clicked.
- `get_filtered_df()`: Returns a subset of the loaded dataset based on the user's selected date range filter (All, Week, Month, 6 Mo, Custom) from the sidebar.

---

## 2. `data_processor.py`
**Purpose:** Handles all initial CSV parsing, data validation, metadata extraction, and type casting.

**Key Functions:**
- `validate_and_load(file_obj)`: Reads the uploaded CSV file. It ensures the file is valid, drops entirely empty columns, sanitizes column names (stripping whitespace), and automatically converts the best candidate date column into `datetime` format.
- `_detect_columns(df)`: A private helper method that scans the DataFrame and classifies columns into `numeric` (float/int), `categorical` (string/object), and identifies the primary `date` column.
- `get_metadata()`: Returns a dictionary containing vital information about the dataset (e.g., total rows, column types, date range, and date span) used throughout the dashboard.

---

## 3. `analytics_engine.py`
**Purpose:** The mathematical heart of the application. It computes aggregates, trends, correlations, and business KPIs cleanly using Pandas, keeping logic separated from the UI.

**Key Functions:**
- `compute_kpis(df)`: Calculates total, mean, minimum, and maximum values for every numeric column in the provided dataset.
- `compute_growth(df, metric_col)`: Calculates month-over-month percentage growth for a specific metric by resampling data into monthly buckets and comparing the two most recent months.
- `best_worst_periods(df, metric_col)`: Resamples data monthly to pinpoint exactly which month recorded the highest (best) and lowest (worst) aggregate values for a chosen metric.
- `monthly_aggregation(df, metric_col)`: Aggregates a chosen metric over monthly periods, returning a formatted DataFrame ready for line/bar charting.
- `category_breakdown(df, metric_col, category_col)`: Groups data by a chosen category column, sums the chosen metric, sorts the results descending, and returns the breakdown for pie/donut charts.
- `correlation_matrix(df)`: Computes the mathematical correlation (Pearson) between all numeric columns to be visualized in a Heatmap.
- `generate_summary_text(df)`: Takes the raw `compute_kpis` output and converts it into a structured, readable string. This string is what gets securely passed to the Gemini AI as context.

---

## 4. `gemini_handler.py`
**Purpose:** Manages the integration with the Google GenAI SDK. Operates on a strict Bring-Your-Own-Key (BYOK), non-persistent, session-only architecture.

**Key Functions:**
- `connect(api_key)`: Validates the user's API key by initializing a client and making a tiny "Respond with OK" test query to `gemini-2.5-flash`.
- `generate_summary(sanitized_analytics_context, metadata)`: Packages the deterministic KPI strings and metadata into a prompt, verifies it doesn't exceed `MAX_CONTEXT_CHARS`, and asks Gemini to generate a bulleted executive summary.
- `ask_question(question, sanitized_analytics_context, metadata)`: Submits a direct user query alongside the sanitized dataset context. The strict system prompt forces the AI to only answer questions relating directly to this data.
- `disconnect()`: Flushes the API key and client from memory to securely log out.

---

## 5. `chart_builder.py`
**Purpose:** A centralized factory for generating all Plotly visualizations used in the application.

**Key Functions:**
- `set_chart_theme(theme_name)`: Updates the global template colors for Plotly charts to perfectly match the user's selected application theme.
- `bar_chart`, `line_chart`, `area_chart`, `pie_chart`, `donut_chart`, `scatter_plot`, `stacked_bar`, `histogram`, `heatmap`: A suite of modular wrapper functions. Each receives a Pandas DataFrame and specific parameters (x, y, color) to return a cleanly formatted Plotly figure object (`go.Figure`) without UI-blocking logic.

---

## 6. `pdf_generator.py`
**Purpose:** Handles the generation of the downloadable executive PDF report using the `reportlab` library.

**Key Functions:**
- `_get_styles()`: Initializes and returns standard typographic styles (fonts, colors, sizes) for PDF headers and body text.
- `_safe_text(text)`: Escapes raw characters (like `<` or `>`) to prevent ReportLab XML parsing errors.
- `_build_chat_section(elements, styles, chat_history)`: Dynamically generates a bordered, formatted Q&A table containing the user's AI conversation history to append to the report.
- `plotly_figure_to_png(fig)`: A robust helper function that converts a Plotly figure to a PNG image buffer using `kaleido`. It safely catches exceptions if `kaleido` fails (e.g., missing dependencies on Streamlit Cloud) without crashing the report.
- `generate_pdf_report(...)`: The master builder function. It takes all processed data, KPIs, AI summaries, selected chart figures, and chat history, compiling them into a professionally formatted, multi-page `BytesIO` PDF buffer.

---

## 7. `theme_engine.py` & `styles.py`
**Purpose:** Controls the aesthetic layer of the application.
- `theme_engine.py`: Contains a dictionary of predefined themes (e.g., macOS Classic, Windows 95, Cyberpunk, Obsidian). Each theme holds a color palette (`bg`, `surface`, `border`, `text_main`, etc.).
- `get_theme_names()` / `get_theme()`: Helpers to fetch theme definitions for the UI selector.
- `get_custom_css(theme_name)`: Located in `styles.py`, this function takes the active theme dictionary and maps its colors into a giant string of raw CSS. This CSS styles Streamlit's native components to achieve the distinct "Retro Window" dashboard look.

---

## 8. `info_page.py`
**Purpose:** A standalone static view.
- `render_info_page()`: When called, it halts the main dashboard rendering and instead displays a full-page onboarding guide. This teaches new users how to use the dashboard, format their CSV files, and obtain a Gemini API key.
