// Define o formato do Produto (espelho do Supabase)
export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  category: string;
  pairing_suggestion?: string;
}

// Define o formato da Mensagem
export interface Message {
  sender: 'user' | 'bot';
  text: string;
}

// Define a resposta da API do Chat
export interface ApiChatResponse {
  response: string;
}