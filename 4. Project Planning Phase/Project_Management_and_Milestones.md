# Phase 4: Project Planning and Milestones

## 1. Project Execution Methodology
The "A Comprehensive Measure of Well-Being" project was executed using an iterative development methodology. The process was divided into data engineering, machine learning modeling, backend development, and frontend integration phases.

## 2. Work Breakdown Structure (WBS) Matrix

| Milestone ID | Task Segment | Operational Scope & Metrics | Status |
| :--- | :--- | :--- | :--- |
| **M1: Data Acquisition & EDA** | Data Science | • Source global demographic and economic datasets. <br>• Perform Exploratory Data Analysis (correlation heatmaps, strip plots). <br>• Clean missing values and apply label encoding. | **Completed** |
| **M2: Model Training** | Machine Learning | • Split data 90/10 for train/test. <br>• Train Linear Regression model using scikit-learn. <br>• Evaluate metrics (R², MAE, RMSE) and serialize to `HDI.pkl`. | **Completed** |
| **M3: Backend Development** | Web Engineering (Flask) | • Initialize Flask app (`app.py`). <br>• Create route controllers (`/Home`, `/Prediction`, `/predict`). <br>• Integrate model loading and exception handling. | **Completed** |
| **M4: Frontend UI/UX** | Web Design (Bootstrap) | • Design the "statistical atlas" aesthetic. <br>• Build HTML templates (`home.html`, `indexnew.html`, `resultnew.html`). <br>• Implement responsive CSS and HDI gauge animations. | **Completed** |
| **M5: Testing & Validation** | Quality Assurance | • Write unit tests for routes and model predictions. <br>• Verify edge-case inputs and test UI responsiveness. | **Completed** |

## 3. Critical Path Timeline

### Phase 1: Modeling (Weeks 1-2)
*   **Focus:** Data cleaning, feature selection (Life expectancy, schooling, GNI, internet users), model training, and exporting the `.pkl` file.

### Phase 2: Web Integration (Weeks 3-4)
*   **Focus:** Setting up the Flask environment, routing, and successfully connecting the HTML form inputs to the Python prediction function.

### Phase 3: Polish and Testing (Weeks 5-6)
*   **Focus:** Refining the Bootstrap 5 UI, implementing the dark theme, writing the pytest suite (205 tests), and finalizing documentation. 
