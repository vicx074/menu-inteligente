import google.generativeai as genai
from src.config import Config
from src.repositories.product_repository import ProductRepository

class AISalesService:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.repository = ProductRepository()

    def _build_context(self):
        """Formata o cardápio."""
        products = self.repository.get_products()
        context = "CARDÁPIO ATUAL (Estoque Real):\n"
        for p in products:
            context += f"- {p['name']} (R$ {p['price']}). Upsell ideal: {p['pairing_suggestion']}\n"
        return context

    def get_sales_response(self, user_message, chat_history=[]):
        menu_context = self._build_context()

        #GATILHO DE INÍCIO (Apresentação única)
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
                # Retorna texto e False (pedido não finalizado)
                return self.model.generate_content(prompt_intro).text, False
            except:
                return "Olá! Sou a IA do Restaurante do Vitinho. O que deseja?", False

        #FORMATAR HISTÓRICO (MEMÓRIA)
        history_text = ""
        for msg in chat_history:
            role = "Garçom" if msg['sender'] == 'bot' else "Cliente"
            history_text += f"{role}: {msg['text']}\n"

        #PROMPT BLINDADO E ESTRITO (Correção do Fechamento)
        system_prompt = f"""
        --- IDENTIDADE ---
        Você é o Garçom Virtual do 'Restaurante do Vitinho'.
        Seu tom é profissional, amigável e focado em vendas.
        
        --- CARDÁPIO ---
        {menu_context}

        --- MEMÓRIA ---
        {history_text}
        
        --- REGRAS DE OURO ---
        1. FOCO: Venda e faça Upsell baseada no cardápio.
        2. ANTI-ALUCINAÇÃO: Não invente pratos.
        
        --- PROTOCOLO DE FECHAMENTO (CRÍTICO - NÃO ERRE AQUI) ---
        Você deve seguir EXATAMENTE esta ordem de duas etapas:
        
        PASSO 1 (CONFIRMAÇÃO): Se o cliente escolheu os itens, PRIMEIRO faça um resumo do pedido com o valor total e PERGUNTE: "Posso confirmar o pedido?".
           -> IMPORTANTE: NESTA MENSAGEM NÃO USE A TAG DE FECHAMENTO AINDA. O CHAT DEVE CONTINUAR ABERTO.
           
        PASSO 2 (FINALIZAÇÃO): APENAS se o cliente responder "Sim", "Pode", "Confirmo" ou "Fecha a conta" APÓS você ter feito o resumo:
           -> Diga que enviou para a cozinha.
           -> E SÓ AGORA adicione a tag: <PEDIDO_FECHADO>.
           
        ERRO PROIBIDO: Nunca coloque a tag <PEDIDO_FECHADO> se você estiver fazendo uma pergunta. Só coloque se estiver afirmando que acabou.
        """

        try:
            response = self.model.generate_content(f"{system_prompt}\nCliente: {user_message}")
            text = response.text
            
            # Lógica de detecção do fim
            is_completed = False
            if "<PEDIDO_FECHADO>" in text:
                is_completed = True
                text = text.replace("<PEDIDO_FECHADO>", "").strip()
            
            return text, is_completed
        except Exception as e:
            print(f"Erro: {e}")
            return "Desculpe, pode repetir?", False