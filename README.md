# Insight Flow

**Business Analytics Platform with AI-Assisted Insights**

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen.svg)](https://insightflow-v1.streamlit.app/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/Lakshya1003/InsightFlow-v1)

## Overview

Insight Flow is a lightweight, zero-configuration business analytics platform designed to transform raw tabular data into actionable insights instantly. It empowers business analysts, product managers, and decision-makers to upload CSV datasets, visualize key performance indicators (KPIs), analyze trends, and engage in natural language querying powered by AI—all without writing a single line of SQL or configuring a database.

By prioritizing a privacy-first, stateless architecture, the platform guarantees that sensitive business data is processed entirely in-memory and is never stored on a server.

## 📥 Test Data / Sample CSV

To quickly test the capabilities of Insight Flow, you can use our sample dataset. Download it here to upload directly into the live demo or your local environment.

**Download Test CSV:** [TEST CSV DOWNLOAD LINK HERE](https://drive.google.com/file/d/1rlOJqRb8kV6wf9foubGprvR4VPgddQ3-/view?usp=sharing)


## 📄 Sample Output Report

Insight Flow automatically generates a professional executive business analytics report summarizing KPIs, trends, AI-assisted insights, and visual analytics.

If you'd like to review the final output without running the application, you can download a sample report below.

📥 **Download Sample Analytics Report**

➡️ **[View Sample Report (PDF)](https://drive.google.com/file/d/1NpsNHkWJ6f_OBzthuKtYHC5BuXEa7GVc/view?usp=sharing)**



> The report was generated using the sample dataset provided in this repository and demonstrates the structure, analytics, charts, and AI-generated executive summary produced by Insight Flow.
## 📸 Screenshots

|                                    Landing Page                                    |                            CSV Upload & Processing                            |
| :--------------------------------------------------------------------------------: | :----------------------------------------------------------------------------: |
| <img src="./Project Screenshots/landing_page.png" alt="Landing Page" width="400"/> | <img src="./Project Screenshots/csv_upload.png" alt="CSV Upload" width="400"/> |

|                             Dashboard & Dynamic Charts                             |                            AI Chat Assistant                            |
| :---------------------------------------------------------------------------------: | :----------------------------------------------------------------------: |
| <img src="./Project Screenshots/dashboard_charts.png" alt="Dashboard" width="400"/> | <img src="./Project Screenshots/ai_chat.png" alt="AI Chat" width="400"/> |

|                                   PDF Report Export                                   |
| :-----------------------------------------------------------------------------------: |
| <img src="./Project Screenshots/pdf_export.png" alt="PDF Report Output" width="400"/> |

## 🚀 Key Features

- **Instant CSV Upload:** Seamless ingestion of raw datasets without schema configuration.
- **Auto KPI Generation:** Deterministic calculation of totals, averages, and aggregations.
- **Trend Analysis:** Month-over-month and week-over-week performance tracking.
- **Interactive Charts:** Rich, dynamic visualizations built with Plotly.
- **AI-Assisted Chat:** Context-aware data querying using the Google Gemini API.
- **Executive PDF Export:** One-click generation of professional, offline reports.
- **Dynamic Theme Support:** Clean, customizable aesthetics that sync with chart layouts.
- **Stateless Processing:** 100% in-memory computation ensuring absolute data privacy.

## 🛠 Engineering Highlights

<p align="center">
  <img src="./Project Screenshots/architecture.png" alt="Project Architecture" width="600"/>
  <br>
  <em>High-level component architecture of Insight Flow</em>
</p>

- **Stateless Architecture:** No persistent database is used. The application relies entirely on temporary memory, maximizing user privacy and eliminating database schema migrations.
- **Privacy-First In-Memory Processing:** Leverages Streamlit Session State and `io.BytesIO` buffers to parse data, generate charts, and compile PDFs dynamically without ever writing files to a hard drive.
- **Modular Analytics Pipeline:** Clean separation of concerns between data ingestion, mathematical aggregation, and UI rendering (1200–1400 LOC).
- **Metadata-Driven AI Context:** Implements strict Context Bounding. The AI is fed deterministic, pre-calculated summaries rather than raw CSV data, heavily mitigating the risk of mathematical hallucinations.
- **Dynamic Plotly Engine:** A centralized layout engine synchronizes JavaScript-based interactive charts with the active CSS theme system.

## 🏗 Architecture & Workflow

<p align="center">
  <img src="./Project Screenshots/workflow.png" alt="User Workflow" width="700"/>
  <br>
  <em>End-to-end user workflow and software interactions</em>
</p>

The data flows sequentially through highly decoupled modules:

1. **CSV Upload:** User drops a file; `app.py` captures the memory buffer.
2. **Data Processing:** `data_processor.py` coerces types, handles missing values, and infers schemas (Dates, Metrics, Categories).
3. **Analytics Generation:** `analytics_engine.py` executes deterministic Pandas math (grouping, resampling) to extract KPIs.
4. **Chart Building:** `chart_builder.py` wraps `plotly.express` to generate interactive DOM elements.
5. **Gemini Chat Assistant:** `gemini_handler.py` merges analytics context with a strict System Prompt to answer user questions securely.
6. **PDF Export:** `pdf_generator.py` compiles charts, KPIs, and chat history into a downloadable ReportLab PDF.

## 📂 Folder Structure

<p align="center">
  <img src="./Project Screenshots/dependencies.png" alt="File Dependencies" width="450"/>
  <br>
  <em>Internal file dependency bubble diagram</em>
</p>

```text
InsightFlow-v1/
├── app.py                   # Main Streamlit application and state controller
├── data_processor.py        # CSV parsing, schema inference, and validation
├── analytics_engine.py      # Deterministic math, KPIs, and aggregations
├── chart_builder.py         # Plotly visualization wrappers
├── gemini_handler.py        # Google Gemini API integration and prompt bounds
├── pdf_generator.py         # ReportLab in-memory PDF compiler
├── theme_engine.py          # Design system configuration
├── styles.py                # Dynamic CSS generator
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## 🌟 Why This Project Is Different

Unlike traditional web applications, Insight Flow requires **zero configuration**.

- **No Database:** Eliminates the bottleneck of maintaining SQL schemas or NoSQL collections.
- **No Authentication:** Frictionless onboarding—users can start analyzing data immediately.
- **Privacy-First Design:** Data is destroyed the moment the browser tab is closed.
- **AI Analytics Without Storage:** Users get the power of an LLM data interpreter without risking their sensitive CSVs in a persistent cloud storage bucket.

Insight Flow works best with standard structured business or time-series data (e.g., sales logs, website analytics, user data, etc.).

To ensure the system works as intended, your CSV **must** contain:

1. 🗓️ **At least one Date column:** (e.g., `Date`, `Timestamp`, `Created_At`). The system is quite flexible and parses most standard date formats (like `YYYY-MM-DD`, `MM/DD/YYYY`).
2. 🔢 **At least one Numeric column:** (e.g., `Revenue`, `Sales`, `Quantity`, `Visits`, `Temperature`). Used for KPI generation and primary chart axes.

**Optional but recommended:**

- 🏷️ **Categorical columns:** (e.g., `Region`, `Product Category`, `Status`, `User Segment`). Used to generate breakdowns, pie charts, and segment analysis.

### Example CSV Structure:

```csv
Date,Region,Product,Revenue,Quantity
2023-01-15,North,Software,1500.50,10
2023-01-16,South,Hardware,850.00,5
2023-01-17,North,Hardware,1200.00,8
```

---

## 🏢 Our Services  **[InsightFlow services](https://insightflowv1.netlify.app/)**

---

## 📊 Direct use  **[InsightFlow v1](https://insightflow-v1.streamlit.app/)**

```
```

💻 How to Run

### Prerequisites

- Python 3.9+
- A valid Google Gemini API Key (Optional, for AI Chat)

### Installation & Environment Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/Lakshya1003/InsightFlow-v1.git
   cd InsightFlow-v1
   ```
2. **Create a virtual environment (Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables (Optional)**
   Create a `.env` file in the root directory and add your Gemini API Key if you want to use the AI chat feature.

   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

### Run the Application

```bash
streamlit run app.py
```

## 🔮 Future Improvements

- **Large Dataset Optimization:** Migrate from Pandas to Polars or Dask for out-of-core, lazy-evaluation processing to handle multi-gigabyte CSVs.
- **Advanced Data Cleaning:** Provide a UI layer for users to manually resolve coerced `NaN` values or rename columns.
- **Multi-File Analytics:** Allow relational mapping between multiple uploaded CSVs.
- **Optional Authentication Mode:** Implement a lightweight OAuth layer for users who *want* to persist session history securely.
- **Scheduled Reports:** Add background Celery workers to email PDF reports automatically.

## 📬 Author / Contact

- **GitHub:** [Lakshya1003](https://github.com/Lakshya1003)
- ***LinkedIn***: [www.linkedin.com/in/lakshya-raj-malviya](https://www.linkedin.com/in/lakshya-raj-malviya/)*
