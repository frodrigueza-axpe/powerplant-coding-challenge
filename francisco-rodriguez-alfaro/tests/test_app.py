import json
import pytest
from flask import Flask
from src.francisco_rodriguez_alfaro.app.routes import api_bp  # Importa tu blueprint

# Fixture para crear la app de test
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(api_bp)

    with app.test_client() as client:
        yield client

# Test exitoso con JSON válido
def test_production_plan_success(client):
    payload = {
            "load": 100,
            "fuels": {
                "gas(euro/MWh)": 13.4,
                "kerosine(euro/MWh)": 50.8,
                "co2(euro/ton)": 20,
                "wind(%)": 60
            },
            "powerplants": [
                {
                    "name": "windpark1",
                    "type": "windturbine",
                    "efficiency": 1,
                    "pmin": 0,
                    "pmax": 100
                }
            ]
        }

    response = client.post(
        "/productionplan",
        data=json.dumps(payload),
        content_type="application/json"
    )

    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert response.json[0]["name"] == "windpark1"
    assert response.json[0]["p"] == 60.0  # 60% de 100

# Test de error por content-type incorrecto
def test_production_plan_wrong_content_type(client):
    response = client.post("/productionplan", data="nojson", content_type="text/plain")
    assert response.status_code == 400
    assert "Invalid content type" in response.json["error"]

# Test de JSON inválido (simula que checkJsonValid devuelve error)
def test_production_plan_invalid_json(client, monkeypatch):
    def mock_check_json_invalid(data):
        return {"error": True, "message": "Invalid format"}

    from francisco_rodriguez_alfaro.clases import utils
    monkeypatch.setattr(utils.Utils, "checkJsonValid", staticmethod(mock_check_json_invalid))

    response = client.post("/productionplan", json={"invalid": "data"})
    assert response.status_code == 400
