import google.generativeai as genai
from src.config import Config
from src.repositories.product_repository import ProductRepository

class AISalesService:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.repository = ProductRepository()

    def _build_context(self):
        """
        Método privado que formata o cardápio para a IA entender.
        """
        products = self.repository.get_available_products()
        
        context = "CARDÁPIO ATUAL:\n"
        for p in products:
            context += f"- {p['name']} (R$ {p['price']}). Combinação Perfeita: {p['pairing_suggestion']}\n"
        return context

    def get_sales_response(self, user_message):
        """
        Gera a resposta de vendas baseada na mensagem do usuário.
        """
        menu_context = self._build_context()

        system_prompt = f"""
        Você é um garçom vendedor.
        {menu_context}
        
        Regras:
        1. Responda a dúvida do cliente.
        2. SEMPRE tente vender o item da 'Combinação Perfeita'.
        3. Seja curto e persuasivo.
        """

        try:
            response = self.model.generate_content(f"{system_prompt}\nCliente: {user_message}")
            return response.text
        except Exception as e:
            return "Desculpe, estou com dificuldade para ler o cardápio agora."