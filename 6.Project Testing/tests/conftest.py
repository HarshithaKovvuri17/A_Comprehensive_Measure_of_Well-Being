import sys
import os
from pathlib import Path
import pytest

# Ensure the app folder is on the python path
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../5. Project Development Phase'))
sys.path.insert(0, app_dir)

# We must set this before importing app so we don't send real emails during testing
os.environ['MAIL_SERVER'] = ''
os.environ['MAIL_PORT'] = ''
os.environ['MAIL_USERNAME'] = ''
os.environ['MAIL_PASSWORD'] = ''

# pyrefly: ignore [missing-import]
from main import app as flask_app
# pyrefly: ignore [missing-import]
from app.database import client as mongo_client

# Fixtures from original root tests/conftest.py
@pytest.fixture()
def app():
    flask_app.config.update(TESTING=True)
    yield flask_app

@pytest.fixture()
def client(app):
    return app.test_client()

# Fixtures from original Flask/tests/conftest.py
@pytest.fixture
def test_db():
    # Use a separate test database
    db = mongo_client['hdi_test_database']
    # Clear out any old test data
    db.users.delete_many({})
    db.email_verifications.delete_many({})
    db.hdi_inputs.delete_many({})
    db.hdi_predictions.delete_many({})
    
    # Insert a dummy model so predictions work
    db.ml_models.insert_one({
        "filename": "HDI.pkl",
        "description": "Human Development Index Prediction Model",
        "is_active": True,
        "created_at": "2026-07-01T00:00:00Z"
    })
    
    # Override the database objects in auth and study blueprints
    # pyrefly: ignore [missing-import]
    import app.api.auth as auth_module
    # pyrefly: ignore [missing-import]
    import app.api.study as study_module
    # pyrefly: ignore [missing-import]
    import main as main_module
    
    auth_module.db = db
    study_module.db = db
    main_module.db = db
    
    yield db
    
    # Teardown: drop collections after tests
    db.users.drop()
    db.email_verifications.drop()
    db.hdi_inputs.drop()
    db.hdi_predictions.drop()
    db.ml_models.drop()

@pytest.fixture
def test_client(test_db):
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    
    with flask_app.test_client() as c:
        yield c
