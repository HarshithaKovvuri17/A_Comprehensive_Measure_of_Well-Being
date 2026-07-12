# HDI Prediction System

An end-to-end machine learning web application that predicts a country's
**Human Development Index (HDI)** from four core development indicators:
life expectancy, mean years of schooling, GNI per capita, and internet users (%).

Built with **Python, scikit-learn, Flask, and Bootstrap 5**.

![R2 Score](https://img.shields.io/badge/R²-0.955-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/flask-3.x-black)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## ✨ Features

- **Machine Learning pipeline** — EDA, missing-value handling, label
  encoding, correlation heatmap, strip plots, 90/10 train/test split,
  Linear Regression training, and full evaluation (R², MAE, MSE, RMSE).
- **Flask web app** — clean routes (`/`, `/Home`, `/Prediction`, `/predict`),
  automatic model loading at startup, robust input validation, and
  friendly error handling.
- **Modern, responsive UI** — a distinctive "statistical atlas" visual
  design built on Bootstrap 5: dark navy palette, brass-gold index accent,
  serif display type, and an animated HDI gauge that shows exactly
  where a prediction falls across the four development bands.
- **Test suite** — unit tests, Flask route tests, model tests, prediction
  tests, and edge-case coverage (205 tests).
- **Production-quality code** — logging, exception handling, type hints,
  docstrings, and a modular folder structure.

---

## 📁 Project Structure

```
hdi_project/
├── ML - 0027 - Human Development Index/
│   └── Flask/
│       ├── app.py                     # Flask application (routes, prediction logic)
│       ├── HDI.pkl                    # Trained model artifact
│       ├── templates/                 # Jinja2 HTML templates
│       │   ├── base.html
│       │   ├── home.html
│       │   ├── login.html
│       │   ├── register.html
│       │   ├── indexnew.html
│       │   ├── resultnew.html
│       │   └── admin.html
│       ├── static/                    # CSS, JS, Images
│       │   ├── css/
│       │   └── js/
│       └── tests/                     # Unit and Integration Tests
│
├── tests/                             # Root level tests (if any)
├── requirements.txt                   # Python dependencies
├── pytest.ini                         # Pytest configuration
├── README.md                          # This file
└── .gitignore                         # Git ignore file
```

---

## 🚀 Quick Start

```bash
# 1. Clone / unzip the project, then create a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the web app
cd "ML - 0027 - Human Development Index\Flask"
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.
---

## ⚠️ A note on the ML Model

This project ships with a **pre-trained Machine Learning model** (`HDI.pkl`)
that predicts the Human Development Index based on the exact indicators used
by the real UNDP Human Development Report (life expectancy, schooling, GNI
per capita, internet users).

**To retrain or use real data:** You can write your own training script using 
scikit-learn to generate a new `HDI.pkl` file, and simply drop it into the 
`ML - 0027 - Human Development Index\Flask` directory to seamlessly integrate 
it with the web app!

---

## 🧠 Model Details

| Item | Value |
|---|---|
| Algorithm | Linear Regression (scikit-learn) |
| Features | Country (label-encoded), Life expectancy, Mean years of schooling, GNI per capita, Internet users |
| Target | HDI (0–1) |
| Split | 90% train / 10% test |
| R² (test) | ~0.955 |
| MAE | ~0.022 |
| RMSE | ~0.028 |

## 🏷️ HDI Classification Bands

| Range | Category |
|---|---|
| 0.30 – 0.40 | Low HDI |
| 0.40 – 0.70 | Medium HDI |
| 0.70 – 0.80 | High HDI |
| 0.80 – 0.94+ | Very High HDI |

---

---

## 📝 License

MIT — free to use, modify, and distribute for educational and research purposes.
