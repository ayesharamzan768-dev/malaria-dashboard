# WHO Malaria Intelligence Dashboard

A complete professional Streamlit dashboard for country-level malaria cases using the WHO Global Health Observatory indicator **MALARIA002**.

## Project Structure

```text
/dashboard_project/
├── data/
│   └── MALARIA002.csv
├── notebooks/
│   └── analysis.ipynb
├── app.py
├── charts.py
├── filters.py
├── requirements.txt
├── README.md
└── .streamlit/config.toml
```

## Features

- Professional dark executive dashboard UI
- KPI summary cards
- Sidebar filters connected to all charts
- Year range filter
- Region and country multi-select filters
- Numerical range slider
- Search filter
- Required chart types:
  - Pie Chart
  - Histogram
  - Line Chart
  - Bar Chart
  - Scatter Plot
  - Box Plot
  - Heatmap
  - Area Chart
  - Count Plot
  - Violin Plot
- Bonus bubble chart
- Data table
- WHO source refresh button

## Dataset

The expected dataset filename is kept exactly as required:

```text
MALARIA002.csv
```

Original source provided:

```text
https://apps.who.int/gho/athena/data/GHO/MALARIA002.csv
```

WHO has retired the old Athena API, so the app tries the old link first, then the current GHO OData endpoint, and finally uses the included local CSV so the project always runs.

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Upload this folder to GitHub.
2. Go to Streamlit Community Cloud.
3. Click **New app**.
4. Select your GitHub repo.
5. Main file path: `app.py`.
6. Click **Deploy**.

## Main Insights to Present

- Malaria burden is concentrated in a small group of high-burden countries.
- African countries dominate the latest case totals in the sample data.
- Country-level trends show that some countries improved over time while others remained high burden.
- Uncertainty ranges can be compared using the low/high estimate scatter plot.
- Regional distributions are highly skewed, visible in box and violin charts.

## Submission Notes

This project includes the required folder structure, dashboard application, chart functions, filter functions, notebook, requirements file, and documentation.
