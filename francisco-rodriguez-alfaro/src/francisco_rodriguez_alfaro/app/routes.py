from flask import Blueprint, request, jsonify

from francisco_rodriguez_alfaro.clases.utils import Utils
from francisco_rodriguez_alfaro.clases.powerPlant import ResumePowerPlant

api_bp = Blueprint('api', __name__)

@api_bp.route('/productionplan', methods=['POST'])
def production_plan():
    if not request.is_json:
        return jsonify({"error": "Invalid content type, expecting application/json"}), 400

    data = request.get_json()
    response = Utils.checkJsonValid(data)
    
    if response.get("error") == True:
        return response, 400 
    
    obj_powerplant = ResumePowerPlant(response)
    
    
    return obj_powerplant, 200

    
