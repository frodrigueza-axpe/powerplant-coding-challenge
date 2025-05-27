from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__)

@api_bp.route('/productionplan', methods=['POST'])
def production_plan():
    if not request.is_json:
        return jsonify({"error": "Invalid content type, expecting application/json"}), 400

    data = request.get_json()

    required_keys = {"load", "fuels", "powerplants"}
    if not required_keys.issubset(data.keys()):
        return jsonify({"error": "Missing required fields"}), 400

    # Aquí puedes hacer tu lógica de cálculo con el payload
    # Por ahora solo devolvemos una respuesta vacía de ejemplo
    return jsonify([]), 200
