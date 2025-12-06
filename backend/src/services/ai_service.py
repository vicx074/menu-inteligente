import google.generativeai as genai
from src.config import Config
from src.repositories.product_repository import ProductRepository

class AISalesService:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_KEY)
        # Modelo atualizado conforme sua preferência
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.repository = ProductRepository()

    def _build_context(self):
        """Formata o cardápio com base no banco de dados."""
        products = self.repository.get_products()
        context = "CARDÁPIO ATUAL (Estoque Real):\n"
        for p in products:
            context += f"- {p['name']} (R$ {p['price']}). Upsell ideal: {p['pairing_suggestion']}\n"
        return context

    def get_sales_response(self, user_message, chat_history=[]):
        menu_context = self._build_context()

        # 1. GATILHO DE INÍCIO (Apresentação única)
        if user_message == "START_CHAT_SIGNAL":
            prompt_intro = f"""
            Você é o 'Garçom Virtual' do Restaurante do Vitinho.
            
            CARDÁPIO DE HOJE:
            {menu_context}
            
            SUA MISSÃO AGORA:
            1. Dê as boas-vindas curtas e animadas.
            2. Apresente o cardápio de forma resumida e atraente (use emojis).
            3. Pergunte o que o cliente deseja pedir.
            """
            try:
                return self.model.generate_content(prompt_intro).text, False
            except:
                return "Olá! Sou a IA do Restaurante do Vitinho. O que deseja?", False

        # 2. FORMATAR HISTÓRICO (MEMÓRIA)
        history_text = ""
        for msg in chat_history:
            role = "Garçom" if msg['sender'] == 'bot' else "Cliente"
            history_text += f"{role}: {msg['text']}\n"

        # 3. PROMPT BLINDADO E ESTRITO
        system_prompt = f"""
        --- IDENTIDADE ---
        Você é o Garçom Virtual do 'Restaurante do Vitinho'.
        Seu tom é profissional, amigável e focado em vendas.
        
        --- CARDÁPIO (A ÚNICA VERDADE) ---
        {menu_context}

        --- MEMÓRIA DA CONVERSA ---
        {history_text}
        
        --- REGRAS DE OURO (CRÍTICO) ---
        1. RECUSA IMEDIATA DE TEMA: Se o cliente pedir histórias, piadas, código ou qualquer coisa fora do restaurante, responda APENAS: 
           "Desculpe, mas eu só entendo de comida! 🍔 Vamos voltar pro cardápio?"
        
        2. FORMATAÇÃO LIMPA: JAMAIS comece sua frase com "Garçom:", "IA:" ou "Bot:". Responda diretamente.
        
        3. UPSELL INTELIGENTE (SEM INSISTÊNCIA): 
           - Ofereça o 'Upsell ideal' quando o cliente escolher um lanche.
           - IMPORTANTE: Se o cliente disser "não", "não obrigado" ou recusar a oferta: NÃO INSISTA. Aceite a recusa imediatamente e vá para a confirmação do pedido.
        
        --- PROTOCOLO DE FECHAMENTO (OBRIGATÓRIO) ---
        Você deve seguir EXATAMENTE esta ordem de duas etapas:
        
        PASSO 1 (RESUMO E CONFIRMAÇÃO): Se o cliente escolheu os itens, PRIMEIRO faça um resumo do pedido com o valor total e PERGUNTE: "Posso confirmar o pedido?".
           -> IMPORTANTE: NESTA MENSAGEM NÃO USE A TAG DE FECHAMENTO AINDA.
           
        PASSO 2 (FINALIZAÇÃO): APENAS se o cliente responder de forma AFIRMATIVA (ex: Sim, Pode, Podemos, Claro, Ok, Manda ver, Isso aí, Fechado) APÓS o resumo:
           -> Diga que enviou para a cozinha.
           -> E SÓ AGORA adicione a tag: <PEDIDO_FECHADO>.
        """

        try:
            response = self.model.generate_content(f"{system_prompt}\nCliente agora disse: {user_message}")
            text = response.text
            
            # Limpeza de segurança (remove prefixos indesejados)
            if text.startswith("Garçom:"):
                text = text.replace("Garçom:", "").strip()
            
            # Lógica de detecção do fim
            is_completed = False
            if "<PEDIDO_FECHADO>" in text:
                is_completed = True
                text = text.replace("<PEDIDO_FECHADO>", "").strip()
            
            return text, is_completed
        except Exception as e:
            print(f"Erro na IA: {e}")
            return "Desculpe, pode repetir?", False