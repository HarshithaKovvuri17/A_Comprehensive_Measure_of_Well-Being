from flask import Blueprint, render_template, request, session, redirect, url_for
import numpy as np
import pandas as pd
import pickle
import os
from datetime import datetime
from bson.objectid import ObjectId
from app.database import db

study_bp = Blueprint('study', __name__)

model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'HDI.pkl')
try:
    ml_model = pickle.load(open(model_path, 'rb'))
except Exception as e:
    ml_model = None

country_names = {
    0: "Afghanistan", 1: "Albania", 2: "Andorra", 3: "Argentina", 4: "Armenia", 5: "Australia", 6: "Austria", 7: "Azerbaijan", 8: "Bahamas", 9: "Bahrain", 10: "Bangladesh", 11: "Barbados", 12: "Belgium", 13: "Belize", 14: "Benin", 15: "Bhutan", 16: "Bosnia and Herzegovina", 17: "Botswana", 18: "Brazil", 19: "Brunei Darussalam", 20: "Bulgaria", 21: "Burkina Faso", 22: "Burundi", 23: "Cambodia", 24: "Cameroon", 25: "Canada", 26: "Cape Verde", 27: "Central African Republic", 28: "Chad", 29: "Chile", 30: "China", 31: "Colombia", 32: "Congo (DRC)", 33: "Costa Rica"
}

@study_bp.route('/Prediction', methods=['GET'])
def prediction():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
        
    user = db.users.find_one({"_id": ObjectId(user_id)})
    is_admin = False
    if user and user.get('role') == 'Admin':
        is_admin = True
        
    return render_template('indexnew.html', is_admin=is_admin)

@study_bp.route('/admin', methods=['GET'])
def admin():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
        
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user or user.get('role') != 'Admin':
        return redirect(url_for('study.prediction'))
        
    total_users = db.users.count_documents({})
    total_predictions = db.hdi_predictions.count_documents({})
    total_models = db.ml_models.count_documents({})
    
    pipeline = [
        {"$sort": {"prediction_time": -1}},
        {"$limit": 10},
        {"$lookup": {
            "from": "hdi_inputs",
            "localField": "input_id",
            "foreignField": "_id",
            "as": "input_data"
        }},
        {"$unwind": "$input_data"},
        {"$lookup": {
            "from": "users",
            "localField": "input_data.user_id",
            "foreignField": "_id",
            "as": "user_data"
        }},
        {"$unwind": "$user_data"}
    ]
    
    recent_predictions = list(db.hdi_predictions.aggregate(pipeline))
    
    recent_logs = []
    for p in recent_predictions:
        date_str = p["prediction_time"].strftime("%Y-%m-%d %H:%M:%S") if "prediction_time" in p else "Unknown"
        recent_logs.append({
            "date": date_str,
            "name": p["user_data"].get("name", "Unknown"),
            "email": p["user_data"].get("email", "Unknown"),
            "score": p.get("predicted_hdi_score", 0),
            "category": p.get("hdi_category", "Unknown")
        })
        
    return render_template('admin_dashboard.html', 
                           total_users=total_users, 
                           total_predictions=total_predictions,
                           total_models=total_models,
                           recent_logs=recent_logs)

@study_bp.route('/predict', methods=['POST'])
def predict():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
        
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return redirect(url_for('auth.login'))
        
    country_idx = request.form.get('country')
    life_expectancy = request.form.get('life_expectancy')
    schooling = request.form.get('schooling')
    gni = request.form.get('gni')
    internet_users = request.form.get('internet_users')
    internet_users_surrogate = internet_users
    
    session_id = db.sessions.insert_one({
        "user_id": user["_id"],
        "login_time": datetime.utcnow(),
        "status": "Active"
    }).inserted_id
    
    country_name_str = country_names.get(int(country_idx), f"Country_{country_idx}")
    country = db.countries.find_one({"country_name": country_name_str})
    if not country:
        country_id = db.countries.insert_one({
            "country_name": country_name_str,
            "region": "Global",
            "population": 0,
            "created_at": datetime.utcnow()
        }).inserted_id
    else:
        country_id = country["_id"]
    
    hdi_input_id = db.hdi_inputs.insert_one({
        "user_id": user["_id"],
        "country_id": country_id,
        "life_expectancy": float(life_expectancy),
        "mean_years_schooling": float(schooling),
        "internet_users": float(internet_users),
        "gnl_per_capita": float(gni),
        "created_at": datetime.utcnow()
    }).inserted_id
    
    input_features = [float(country_idx), float(life_expectancy), float(schooling), float(gni), float(internet_users_surrogate)]
    features_value = [np.array(input_features)]
    features_name = ['Country','Life expectancy','Mean years of schooling','Gross national income (GNI) per capita','Internet users']
    df = pd.DataFrame(features_value, columns=features_name)
    output = ml_model.predict(df)
    
    y_pred = round(output[0][0], 2)
    category = "Unknown"
    
    if(y_pred >= 0.3 and y_pred <= 0.4) :
        category = "Low HDI"
    elif(y_pred >= 0.4 and y_pred <= 0.7) :
        category = "Medium HDI"
    elif(y_pred >= 0.7 and y_pred <= 0.8) :
        category = "High HDI"
    elif(y_pred >= 0.8 and y_pred <= 10) :
        category = "Very High HDI"
    else :
        category = "The given values do not match the expected HDI range"
        
    active_model = db.ml_models.find_one()
    
    prediction_id = db.hdi_predictions.insert_one({
        "input_id": hdi_input_id,
        "model_id": active_model["_id"],
        "predicted_hdi_score": y_pred,
        "hdi_category": category,
        "prediction_time": datetime.utcnow()
    }).inserted_id
    
    db.visualization_reports.insert_one({
        "prediction_id": prediction_id,
        "graph_path": f"static/images/report_{prediction_id}.png",
        "report_type": "Summary",
        "generated_at": datetime.utcnow()
    })
    
    db.sessions.update_one(
        {"_id": session_id},
        {"$set": {
            "logout_time": datetime.utcnow(),
            "status": "Completed"
        }}
    )
    
    return render_template('resultnew.html', prediction_text=category + ' ' + str(y_pred), hdi_score=y_pred, hdi_category=category)
