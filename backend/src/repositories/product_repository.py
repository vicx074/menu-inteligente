from supabase import create_client
from src.config import Config

class ProductRepository:
    def __init__(self):
        # Garante que as credenciais existem
        if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
            raise ValueError("Faltam as credenciais do Supabase no .env")
            
        self.supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

    def get_products(self):
        """
        Busca todos os produtos disponíveis no banco de dados.
        NOTA: O nome desta função deve ser 'get_products' para alinhar com o ai_service.
        """
        try:
            response = self.supabase.table('products')\
                .select("*")\
                .eq('is_available', True)\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"Erro ao buscar no Supabase: {e}")
            return []