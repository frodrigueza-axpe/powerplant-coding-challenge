import pytest
from src.app import routes
from src.clases.powerPlant import ResumePowerPlant

# 🔹 Test básico de integración
def test_calculo_coste_plantas_basic():
    input_data = {
        "data": {
            "load": 100,
            "fuels": {
                "gas(euro/MWh)": 13.4,
                "kerosine(euro/MWh)": 50.8,
                "co2(euro/ton)": 20,
                "wind(%)": 60
            },
            "powerplants": [
                {"name": "windpark1", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 100}
            ]
        }
    }

    dispatcher = ResumePowerPlant(input_data)
    result = dispatcher.calculo_coste_plantas()

    assert result == [{"name": "windpark1", "p": 60.0}]

