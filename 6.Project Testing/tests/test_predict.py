
def test_unauthenticated_prediction_access(test_client):
    response = test_client.get('/Prediction')
    # Should redirect to login
    assert response.status_code == 302
    assert '/login' in response.location

def test_unauthenticated_admin_access(test_client):
    response = test_client.get('/admin')
    # Should redirect to login
    assert response.status_code == 302
    assert '/login' in response.location

def test_prediction_flow(test_client, test_db):
    # 1. Setup a verified user and log them in
    user_id = test_db.users.insert_one({
        'name': 'Predictor User',
        'email': 'predict@example.com',
        'role': 'User',
        'is_verified': True
    }).inserted_id
    
    with test_client.session_transaction() as sess:
        sess['user_id'] = str(user_id)
        
    # 2. Access prediction page
    response = test_client.get('/Prediction')
    assert response.status_code == 200
    assert b'Human Development Index' in response.data
    
    # 3. Submit a prediction
    response = test_client.post('/predict', data={
        'country': '0',
        'life_expectancy': '70.5',
        'internet_users': '12.0',
        'schooling': '8.5',
        'gni': '15000'
    })
    assert response.status_code == 200
    
    # Wait, the app currently returns a render_template for prediction result, so the text should contain the result
    assert b'The predicted HDI for' in response.data or b'result' in response.data.lower()
    
    # 4. Verify insertion in DB
    hdi_input = test_db.hdi_inputs.find_one({'user_id': user_id})
    assert hdi_input is not None
    assert hdi_input['life_expectancy'] == 70.5
    
    hdi_prediction = test_db.hdi_predictions.find_one({'input_id': hdi_input['_id']})
    assert hdi_prediction is not None
    assert 'predicted_hdi_score' in hdi_prediction
    assert 'hdi_category' in hdi_prediction

def test_admin_dashboard_access_allowed(test_client, test_db):
    # Setup Admin
    admin_id = test_db.users.insert_one({
        'name': 'Admin User',
        'email': 'admin@example.com',
        'role': 'Admin',
        'is_verified': True
    }).inserted_id
    
    with test_client.session_transaction() as sess:
        sess['user_id'] = str(admin_id)
        
    response = test_client.get('/admin')
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data

def test_admin_dashboard_access_denied(test_client, test_db):
    # Setup standard User
    user_id = test_db.users.insert_one({
        'name': 'Standard User',
        'email': 'user@example.com',
        'role': 'User',
        'is_verified': True
    }).inserted_id
    
    with test_client.session_transaction() as sess:
        sess['user_id'] = str(user_id)
        
    response = test_client.get('/admin')
    # Should block and redirect to /Prediction
    assert response.status_code == 302
    assert '/Prediction' in response.location
