from werkzeug.security import generate_password_hash

def test_register_page_renders(test_client):
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b'Create Account' in response.data

def test_login_page_renders(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Welcome Back' in response.data

def test_successful_registration(test_client, test_db):
    response = test_client.post('/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'role': 'User'
    }, follow_redirects=True)
    
    # Should redirect straight to login
    assert response.status_code == 200
    assert b'Welcome Back' in response.data
    
    # Check DB for user
    user = test_db.users.find_one({'email': 'test@example.com'})
    assert user is not None
    assert user['name'] == 'Test User'
    assert user['role'] == 'User'
    assert 'password_hash' in user

def test_duplicate_registration(test_client, test_db):
    # Register first time
    test_client.post('/register', data={
        'name': 'Duplicate User',
        'email': 'duplicate@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'role': 'User'
    })
    
    # Register second time
    response = test_client.post('/register', data={
        'name': 'Duplicate User',
        'email': 'duplicate@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'role': 'User'
    })
    
    # Should show error on register page
    assert response.status_code == 200
    assert b'Email already registered. Please log in.' in response.data

def test_unregistered_login(test_client, test_db):
    response = test_client.post('/login', data={
        'email': 'notfound@example.com',
        'password': 'password123'
    })
    
    # Should show error on login page
    assert response.status_code == 200
    assert b'Account not found. Please register first.' in response.data

def test_successful_login_flow(test_client, test_db):
    # 1. Manually insert user
    test_db.users.insert_one({
        'name': 'Existing User',
        'email': 'exist@example.com',
        'password_hash': generate_password_hash('correctpassword'),
        'role': 'User'
    })
    
    # 2. Login
    response = test_client.post('/login', data={
        'email': 'exist@example.com',
        'password': 'correctpassword'
    }, follow_redirects=True)
    
    # Should go straight to home page for User role
    assert response.status_code == 200
    assert b'Human Development Index' in response.data

def test_incorrect_password_login(test_client, test_db):
    # 1. Manually insert user
    test_db.users.insert_one({
        'name': 'Existing User',
        'email': 'exist@example.com',
        'password_hash': generate_password_hash('correctpassword'),
        'role': 'User'
    })
    
    # 2. Login with wrong password
    response = test_client.post('/login', data={
        'email': 'exist@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    
    # Should show error on login page
    assert response.status_code == 200
    assert b'Incorrect password' in response.data
