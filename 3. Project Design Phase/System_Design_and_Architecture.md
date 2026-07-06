# Phase 3: Detailed System Design and Architecture

## 1. System Architecture Blueprint
The HDI Prediction System follows a classic Model-View-Controller (MVC) architecture, utilizing Flask as the controller and Jinja2/Bootstrap as the view layer, with a scikit-learn ML model acting as the core data processing engine.

```text
       ┌────────────────────────────────────────────────────────┐
       │             Web Browser UI (Bootstrap 5)               │
       │           (HTML5 / CSS3 / JavaScript Gauge)            │
       └───────────────────────────┬────────────────────────────┘
                                   │
                           HTTP GET / POST
                                   │
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │             Flask Application Core Router              │
       │                      (app.py)                          │
       └─────┬────────────────────────────────────────────┬─────┘
             │                                            │
             ▼                                            ▼
┌───────────────────────────┐              ┌───────────────────────────┐
│     View Templates        │              │  Machine Learning Model   │
├───────────────────────────┤              ├───────────────────────────┤
│ • base.html               │              │ • Artifact: HDI.pkl       │
│ • home.html               │              │ • Alg: Linear Regression  │
│ • indexnew.html           │              │ • Engine: scikit-learn    │
│ • resultnew.html          │              │ • Input: 1D Array (4 var) │
└───────────────────────────┘              └───────────────────────────┘
```

## 2. Module Decomposition & Technical Specification

### A. Machine Learning Pipeline
*   **Training Script:** Handles EDA, missing-value imputation, label encoding, and data splitting (90/10). Trains a Multiple Linear Regression model achieving an R² score of ~0.955.
*   **Model Artifact (`HDI.pkl`):** The serialized weights and intercept of the trained model, ready for rapid inference.

### B. Web Application Layer
*   **`app.py`**: The core Flask router. Handles rendering templates, receiving form data, formatting inputs into NumPy arrays, and invoking the `.predict()` method on the loaded model.
*   **Templates (`templates/`)**: Jinja2 HTML files providing the structure. `indexnew.html` contains the input forms, while `resultnew.html` displays the output metric and dynamic gauge.
*   **Static Assets (`static/`)**: CSS stylesheets and JavaScript files responsible for the "statistical atlas" aesthetic and visual animations.

## 3. Data Flow Matrix

| User Action | HTTP Method | Route | Backend Processing | Output |
| :--- | :--- | :--- | :--- | :--- |
| Load Home | `GET` | `/` or `/Home` | Renders the landing page. | `home.html` |
| Navigate to Predict | `GET` | `/Prediction` | Renders the data input form. | `indexnew.html` |
| Submit Form | `POST` | `/predict` | Extracts form data, scales/formats it, passes to `HDI.pkl`, maps the result to a category. | `resultnew.html` with HDI score |

## 4. UI/UX Design System
*   **Theme:** Dark navy palette with brass-gold index accents to evoke a premium "statistical atlas" feel.
*   **Typography:** Serif display type for headers to maintain an academic and authoritative tone, with sans-serif for data inputs.
*   **Data Visualization:** An animated HDI gauge visually representing the predicted score across the four development bands. 
 
 
