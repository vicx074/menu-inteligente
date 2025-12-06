import axios from 'axios';
import type { Product, ApiChatResponse } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' }
});

export const MenuService = {
  getProducts: async (): Promise<Product[]> => {
    try {
      const { data } = await api.get<Product[]>('/products');
      return data;
    } catch (error) {
      console.error("Erro API:", error);
      return [];
    }
  },

  sendMessage: async (message: string): Promise<string> => {
    try {
      const { data } = await api.post<ApiChatResponse>('/chat', { message });
      return data.response;
    } catch (error) {
      throw new Error("Erro de comunicação");
    }
  }
};