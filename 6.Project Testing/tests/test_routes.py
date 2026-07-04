def test_home_route(client):
    """Test that GET / returns the home page successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Human Development Index" in response.data

def test_home_alias_route(client):
    """Test that GET /Home returns the home page successfully."""
    response = client.get('/Home')
    assert response.status_code == 200
    assert b"Human Development Index" in response.data

def test_prediction_form_route(client):
    """Test that GET /Prediction returns the indexnew.html form successfully."""
    response = client.get('/Prediction')
    assert response.status_code == 302
    assert b"/login" in response.data

def test_prediction_post(client):
    """Test that POST /predict calculates the HDI successfully."""
    # Values corresponding to: Country=141 (Norway), Life expectancy=82, Schooling=13, GNI=68000, Internet=97
    response = client.post('/predict', data={
        "country": "141",
        "life_expectancy": "82",
        "schooling": "13",
        "gni": "68000",
        "internet_users": "97"
    })
    assert response.status_code == 302
    assert b"/login" in response.data
