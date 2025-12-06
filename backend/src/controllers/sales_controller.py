from flask import Blueprint, request, jsonify
from src.services.ai_service import AISalesService

sales_bp = Blueprint('sales', __name__)

# Tenta iniciar o serviço. Se der erro, printa no terminal para a gente ver.
try:
    ai_service = AISalesService()
except Exception as e:
    print(f"ERRO AO INICIAR IA: {e}")
    ai_service = None

@sales_bp.route('/chat', methods=['POST'])
def chat():
    if not ai_service:
        return jsonify({"error": "Backend iniciando..."}), 503

    data = request.json
    user_message = data.get('message', '')
    history = data.get('history', []) 
    
    # Chama a IA (que já está funcionando)
    response_text, is_completed = ai_service.get_sales_response(user_message, history)
    
    return jsonify({
        "response": response_text,
        "is_completed": is_completed
    }), 200

@sales_bp.route('/products', methods=['GET'])
def list_products():
    """
    Rota que preenche a sidebar do Frontend.
    """
    if not ai_service:
        return jsonify([]), 500
        
    try:
        products = ai_service.repository.get_products()
        return jsonify(products), 200
    except Exception as e:
        print(f"Erro na rota /products: {e}")
        return jsonify({"error": str(e)}), 500