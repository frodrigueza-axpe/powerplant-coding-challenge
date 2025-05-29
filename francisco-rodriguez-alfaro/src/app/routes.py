from flask import Blueprint, request, jsonify
import logging

from clases.utils import Utils
from clases.powerPlant import ResumePowerPlant
from clases.exceptions import ExceptionCalculatingOptimizedData, ExceptionCostResume, ExceptionSortedPlants, ExceptionErroCheckJSON

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

@api_bp.route('/productionplan', methods=['POST'])
def production_plan():
    if not request.is_json:  
        json_respuesta = {
            "error": True 
            , "message": "Invalid content type, expecting application/json"
        }
        return jsonify(json_respuesta), 400

    try:
        data = request.get_json(force=True)
        response = Utils.checkJsonValid(data)
        
        if response.get("error") == True:
            return jsonify(response), 400 
        
    except ExceptionErroCheckJSON as e:
        logger.error(f"ExceptionErroCheckJSON: {e}")
        return jsonify({"error": True, "message": "Invalid JSON format"}), 400
    except Exception as e:
        logger.error(f"Exception: {e}")
        return jsonify({"error": True, "message": "Invalid JSON format"}), 400
        
        
    try:
        obj_powerplant = ResumePowerPlant(response)
        production_plan = obj_powerplant.compute_production_plan()
        
        return jsonify(production_plan), 200
    
    except ExceptionCostResume as e:
        logger.error(f"ExceptionCostResume: {e}")
    except ExceptionSortedPlants as e:
        logger.error(f"ExceptionSortedPlants: {e}")
    except ExceptionCalculatingOptimizedData as e:
        logger.error(f"ExceptionCalculatingOptimizedData: {e}")
    except Exception as e:
        logger.error(f"Exception: {e}")
        return jsonify({"error": True, "message": "Invalid JSON format"}), 400

    
