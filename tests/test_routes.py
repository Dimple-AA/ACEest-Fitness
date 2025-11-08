from app import app, calculate_bmi, calculate_calories

def test_home_route():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_bmi_calculation():
    assert calculate_bmi(70, 175) == 22.86

def test_calorie_calculation():
    assert calculate_calories(30, "cardio") == 240
