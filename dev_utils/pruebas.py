## Añadir "env": {"PYTHONPATH": "${workspaceFolder}"} al fichero launch.json

import json
from francisco_rodriguez_alfaro.clases.utils import Utils
from francisco_rodriguez_alfaro.clases.powerPlant import ResumePowerPlant


path_json_pruebas = "./example_payloads/payload1.json"
with open(path_json_pruebas, 'r', encoding='utf-8') as f:
    datos = json.load(f)


response = Utils.checkJsonValid(datos)


if response.get("error") == True:
    print( response, 400 )

obj_powerplant = ResumePowerPlant(response)


print( obj_powerplant, 200 )

pass 