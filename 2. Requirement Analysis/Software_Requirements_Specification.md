# Phase 2: Software Requirements Specification (SRS) Document

## 1. Introduction & Project Scope
This SRS document outlines the functional modules and architectural constraints governing "A Comprehensive Measure of Well-Being" (HDI Prediction System). The system delivers accurate ML-based predictions via a lightweight Flask web server.

## 2. System Users & Target Audience
* **Researchers & Economists:** Professionals needing quick HDI estimations based on custom or projected data.
* **Students & Educators:** Academic users exploring the relationship between life expectancy, schooling, GNI, internet usage, and overall human development.

## 3. Detailed Functional Requirements
* **FR-1 (Prediction Endpoint):** The system must expose a `POST` route (`/predict`) that accepts numeric inputs for life expectancy, schooling years, GNI per capita, and internet users (%), passing them to the ML model.
* **FR-2 (Model Integration):** The system must load the pre-trained `HDI.pkl` artifact (scikit-learn Linear Regression model) into memory at application startup.
* **FR-3 (Input Validation):** The web forms must validate user inputs to ensure they fall within realistic numerical bounds before processing the prediction.
* **FR-4 (Categorization):** The system must dynamically classify the predicted HDI score into predefined bands: Low (<0.40), Medium (0.40-0.70), High (0.70-0.80), and Very High (>0.80).

## 4. Non-Functional Requirements
* **Performance:** The web application must respond to prediction requests in under 500ms.
* **Usability:** The UI must be responsive (mobile-friendly), utilizing Bootstrap 5 for a clean, accessible layout.
* **Maintainability:** The project must maintain a modular structure, separating the ML training pipeline from the Flask application routes and Jinja2 templates. 
 
