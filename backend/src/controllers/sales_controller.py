from flask import Blueprint, request, jsonify
from src.services.ai_service import AISalesService

sales_bp = Blueprint('sales', __name__)

try:
    ai_service = AISalesService()
except Exception as e:
    print(f"Erro ao iniciar AISalesService: {e}")
    ai_service = None

@sales_bp.route('/chat', methods=['POST'])
def chat():
    if not ai_service:
        return jsonify({"error": "Serviço de IA indisponível"}), 500

    data = request.json
    user_message = data.get('message', '')
    
    try:
        response_text = ai_service.get_sales_response(user_message)
        return jsonify({"response": response_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sales_bp.route('/products', methods=['GET'])
def list_products():
    if not ai_service:
        return jsonify({"error": "Serviço indisponível"}), 500
        
    try:
        repo = ai_service.repository
        products = repo.get_available_products()
        return jsonify(products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500