import { useState, useEffect, useRef } from 'react';
import { MenuService } from '../services/api';
import type { Product, Message } from '../types';

export function useChat() {
  const [products, setProducts] = useState<Product[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOrderCompleted, setIsOrderCompleted] = useState(false); // Novo Estado
  const scrollRef = useRef<HTMLDivElement>(null);

  // Função para Reiniciar o Chat
  const resetChat = async () => {
    setIsOrderCompleted(false);
    setMessages([]); // Limpa a tela
    setIsLoading(true);
    try {
      // Chama o Hello de novo
      const { response } = await MenuService.sendMessage("START_CHAT_SIGNAL", []);
      setMessages([{ sender: 'bot', text: response }]);
    } catch (e) {
        // erro silencioso ou msg padrão
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const init = async () => {
      setIsLoading(true);
      try {
        const [menu, initialRes] = await Promise.all([
          MenuService.getProducts(),
          MenuService.sendMessage("START_CHAT_SIGNAL")
        ]);
        setProducts(menu);
        setMessages([{ sender: 'bot', text: initialRes.response }]);
      } catch (e) { /* ... */ } 
      finally { setIsLoading(false); }
    };
    init();
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;

    const newUserMsg: Message = { sender: 'user', text };
    setMessages(prev => [...prev, newUserMsg]);
    setIsLoading(true);

    try {
      // Pega a resposta e a flag de completado
      const { response, is_completed } = await MenuService.sendMessage(text, messages);
      
      setMessages(prev => [...prev, { sender: 'bot', text: response }]);
      
      if (is_completed) {
        setIsOrderCompleted(true); // Trava o chat!
      }

    } catch (e) {
      setMessages(prev => [...prev, { sender: 'bot', text: "Erro técnico." }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Retorna tudo isso pro App
  return { products, messages, isLoading, isOrderCompleted, sendMessage, resetChat, scrollRef };
}