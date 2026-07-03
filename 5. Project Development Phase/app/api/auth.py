from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.database import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = db.users.find_one({"email": email})
        
        if not user:
            return render_template('login.html', error="Account not found. Please register first.")
            
        if not check_password_hash(user.get("password_hash", ""), password):
            return render_template('login.html', error="Incorrect password.")
            
        session['user_id'] = str(user["_id"])
        
        return redirect(url_for('home'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
        
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match.")
        
        user = db.users.find_one({"email": email})
        
        if user:
            return render_template('register.html', error="Email already registered. Please log in.")
            
        hashed_password = generate_password_hash(password)
            
        db.users.insert_one({
            "name": name,
            "email": email,
            "password_hash": hashed_password,
            "role": role,
            "created_at": datetime.utcnow()
        })
            
        return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
 
 
