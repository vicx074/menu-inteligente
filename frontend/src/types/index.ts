export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  category: string;
  pairing_suggestion?: string;
}

export interface Message {
  sender: 'user' | 'bot';
  text: string;
}

export interface ApiChatResponse {
  response: string;
}