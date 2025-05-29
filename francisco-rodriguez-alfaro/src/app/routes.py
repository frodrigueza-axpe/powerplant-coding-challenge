from flask import Blueprint, request, jsonify
import logging

from clases.utils import Utils
from clases.power_plant import ResumePowerPlant
from clases.exceptions import ExceptionCalculatingOptimizedData, ExceptionCostResume, ExceptionSortedPlants, ExceptionErroCheckJSON

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

@api_bp.route('/productionplan', methods=['POST'])
def production_plan():
    logger.info("Received request to /productionplan")

    if not request.is_json:  
        logger.warning("Request content type is not JSON")
        json_respuesta = {
            "error": True,
            "message": "Invalid content type, expecting application/json"
        }
        return jsonify(json_respuesta), 400

    try:
        logger.debug("Parsing JSON payload")
        data = request.get_json(force=True)
        logger.debug(f"Payload content: {data}")

        logger.info("Validating JSON structure")
        response = Utils.checkJsonValid(data)
        logger.debug(f"Validation result: {response}")
        
        if response.get("error") == True:
            logger.warning("JSON validation failed")
            return jsonify(response), 400
        
    except ExceptionErroCheckJSON as e:
        logger.error(f"ExceptionErroCheckJSON: {e}")
        return jsonify({"error": True, "message": "Invalid JSON format"}), 400
    except Exception as e:
        logger.error(f"Unexpected exception during JSON parsing: {e}")
        return jsonify({"error": True, "message": "Invalid JSON format"}), 400
        
    try:
        logger.info("Creating ResumePowerPlant instance")
        obj_powerplant = ResumePowerPlant(response)

        logger.info("Computing production plan")
        production_plan = obj_powerplant.compute_production_plan()
        logger.debug(f"Computed production plan: {production_plan}")

        logger.info("Production plan generated successfully")
        return jsonify(production_plan), 200
    
    except ExceptionCostResume as e:
        logger.error(f"ExceptionCostResume: {e}")
        return jsonify({"error": True, "message": "ExceptionCostResume"}), 400
    except ExceptionSortedPlants as e:
        logger.error(f"ExceptionSortedPlants: {e}")
        return jsonify({"error": True, "message": "ExceptionSortedPlants"}), 400
    except ExceptionCalculatingOptimizedData as e:
        logger.error(f"ExceptionCalculatingOptimizedData: {e}")
        return jsonify({"error": True, "message": "ExceptionCalculatingOptimizedData"}), 400
    except Exception as e:
        logger.error(f"Exception: {e}")
        return jsonify({"error": True, "message": "Generic Error"}), 400

    
