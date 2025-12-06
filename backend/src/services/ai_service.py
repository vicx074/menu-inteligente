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
        Gera a resposta de vendas com personalidade blindada.
        """
        menu_context = self._build_context()

        # --- LÓGICA DE BOAS-VINDAS (NOVO) ---
        # Se o frontend mandar essa palavra-chave, a IA faz a apresentação
        if user_message == "START_CHAT_SIGNAL":
            prompt_boas_vindas = f"""
            Você é a IA do 'Restaurante do Vitinho'.
            
            CONTEXTO (CARDÁPIO):
            {menu_context}
            
            SUA TAREFA AGORA:
            1. Apresente-se com carisma e diga que é a IA do Restaurante do Vitinho.
            2. Liste o cardápio completo que está no contexto acima para o cliente ver as opções e preços. Use emojis para ilustrar cada prato.
            3. Pergunte o que ele gostaria de pedir hoje.
            """
            try:
                response = self.model.generate_content(prompt_boas_vindas)
                return response.text
            except Exception:
                return "Olá! Sou a IA do Restaurante do Vitinho. O que deseja?"

        # --- LÓGICA NORMAL DE CONVERSA (Seu código anterior continua aqui) ---
        system_prompt = f"""
        --- IDENTIDADE ---
        Você é a IA oficial do 'Restaurante do Vitinho'.
        Seu tom de voz é: Amigável, prestativo e vendedor.
        
        --- CONTEXTO (CARDÁPIO REAL) ---
        {menu_context}

        --- REGRAS ---
        1. Se apresente como IA do Restaurante do Vitinho apenas se perguntarem quem é você e na primeira mensagem que enviarem.
        2. Foco total em vender e fazer Upsell (Combinação Perfeita).
        3. Proteções ativas: Não fale de assuntos fora do restaurante.
        """

        try:
            response = self.model.generate_content(f"{system_prompt}\n\nCliente disse: {user_message}")
            return response.text
        except Exception as e:
            print(f"Erro na IA: {e}")
            return "Desculpe, pode repetir?"