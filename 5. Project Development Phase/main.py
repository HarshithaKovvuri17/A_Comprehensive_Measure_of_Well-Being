import os
import sys
from flask import Flask, render_template, session
from bson.objectid import ObjectId
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

from app.database import db, init_db
from app.api.auth import auth_bp
from app.api.study import study_bp

app = Flask(__name__)
app.secret_key = 'hdi_super_secret_key_for_sessions'

with app.app_context():
    init_db()

app.register_blueprint(auth_bp)
app.register_blueprint(study_bp)

@app.context_processor
def inject_user():
    user_id = session.get('user_id')
    if user_id:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        return dict(current_user=user)
    return dict(current_user=None)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Home')
def my_home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True, port=5000)
