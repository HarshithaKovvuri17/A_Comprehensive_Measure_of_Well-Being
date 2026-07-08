# Phase 6: Testing Report and System Validation

## 1. System Testing Strategy
The testing framework for the HDI Prediction System ensures the mathematical accuracy of the ML model and the reliability of the Flask web application. Testing covers unit tests for individual functions, route tests for the web server, and integration tests for the full prediction pipeline.

## 2. Test Suite Matrix

| Test ID | Functional Area | Input / Action | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **TC-MOD-001** | Model Loading | Initialize Flask app. | `HDI.pkl` loads successfully into memory without errors. | **PASS** |
| **TC-ROU-002** | Home Route (`/`) | `GET` request to `/`. | Returns HTTP 200 and renders `home.html`. | **PASS** |
| **TC-PRE-003** | Prediction Endpoint | `POST` to `/predict` with valid inputs (e.g., Life Exp: 70, Schooling: 10, GNI: 15000, Internet: 50). | Returns HTTP 200, renders `resultnew.html`, and displays a valid HDI score (0.0 to 1.0). | **PASS** |
| **TC-VAL-004** | Input Validation | `POST` to `/predict` with missing or non-numeric data. | Backend catches exception, prevents crash, and displays a friendly error message or form validation warning. | **PASS** |
| **TC-CAT-005** | Band Categorization | Internal function mapping score `0.85`. | System correctly classifies the score as "Very High HDI". | **PASS** |

## 3. Performance and Evaluation Metrics
The underlying Linear Regression model was evaluated on a 10% holdout test set with the following results:
*   **R² Score:** ~0.955 (Indicating the model explains 95.5% of the variance in HDI).
*   **Mean Absolute Error (MAE):** ~0.022.
*   **Root Mean Squared Error (RMSE):** ~0.028.

These metrics confirm the model provides highly accurate estimations of the Human Development Index based on the provided socio-economic parameters. 
