from pymongo import MongoClient

# MongoDB Configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['hdi_database']

def init_db():
    from datetime import datetime
    if db.datasets.count_documents({}) == 0:
        dataset_id = db.datasets.insert_one({
            "dataset_name": "Global_HDI_2024",
            "source": "UNDP",
            "total_rows": 195,
            "total_columns": 8,
            "uploaded_at": datetime.utcnow()
        }).inserted_id
    else:
        dataset_id = db.datasets.find_one()["_id"]

    if db.ml_models.count_documents({}) == 0:
        db.ml_models.insert_one({
            "model_name": "HDI_Linear_Reg_V1",
            "algorithm_used": "Linear Regression",
            "accuracy_score": 0.955,
            "r2_score": 0.951,
            "model_file_path": "HDI.pkl",
            "dataset_id": dataset_id,
            "trained_at": datetime.utcnow()
        })
