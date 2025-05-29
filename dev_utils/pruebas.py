## Añadir "env": {"PYTHONPATH": "${workspaceFolder}"} al fichero launch.json

import json
from clases.utils import Utils
from clases.powerPlant import ResumePowerPlant


path_json_pruebas = "./example_payloads/payload2.json"
with open(path_json_pruebas, 'r', encoding='utf-8') as f:
    datos = json.load(f)


response = Utils.checkJsonValid(datos)


if response.get("error") == True:
    print( response, 400 )

obj_powerplant = ResumePowerPlant(response)
production_plan = obj_powerplant.compute_production_plan()



pass 