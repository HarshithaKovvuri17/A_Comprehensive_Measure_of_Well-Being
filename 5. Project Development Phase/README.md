# Phase 5: Project Development Phase

This phase contains the core source code for "A Comprehensive Measure of Well-Being" (HDI Prediction System).

## Directory Structure
*   **`app/` / `Flask/`**: Contains the Flask web application (`app.py`).
*   **`Dataset/`**: Contains the raw CSV and processed data used for EDA and model training.
*   **`Training/`**: Jupyter notebooks and Python scripts utilized for cleaning data, feature engineering, and fitting the Linear Regression model.
*   **`static/`**: CSS and JS assets for the frontend UI.
*   **`templates/`**: Jinja2 HTML files (`indexnew.html`, `resultnew.html`, etc.).

## Development Workflow
1.  **Model Training:** Run the training scripts to generate the `HDI.pkl` model artifact.
2.  **Integration:** Place `HDI.pkl` in the application root.
3.  **App Execution:** Run `app.py` via Flask to serve the model predictions over HTTP.
