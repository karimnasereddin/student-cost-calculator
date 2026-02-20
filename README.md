# Student Cost of Living Calculator (Laurier)

## Why I built this
With recent OSAP changes and continued conversation around tuition increases in Ontario, I wanted a simple way to understand what student life actually costs in a clear, measurable way.

Instead of guessing, I built a lightweight tool that turns my real expenses into totals, visuals, and quick insights I can use to plan month-to-month. It also doubles as a personal learning project to get more comfortable coding with structured datasets that are directly applicable to me (and other students).

## What it does
This is a small Streamlit app that:
- Collects yearly student expense inputs (tuition, housing, food, transportation, entertainment, misc.)
- Calculates total yearly, monthly, and weekly costs
- Visualizes spending distribution (pie chart + monthly breakdown bar chart)
- Estimates work hours/week needed to break even based on hourly wage
- Includes a “Budget Coach” page that provides simple recommendations based on your results

## Tech stack
- Python
- Streamlit
- pandas
- matplotlib

## How to run locally
1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies
4. Run the Streamlit app

### Windows (PowerShell)
```bash
py -m venv venv
venv\Scripts\activate
py -m pip install -r requirements.txt
py -m streamlit run app.py