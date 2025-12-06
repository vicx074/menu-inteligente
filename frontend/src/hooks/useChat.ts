import { useState, useEffect, useRef } from 'react';
import { MenuService } from '../services/api';
import type { Product, Message } from '../types';

export function useChat() {
  const [products, setProducts] = useState<Product[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const init = async () => {
      setIsLoading(true);
      try {
        const [menu, greeting] = await Promise.all([
          MenuService.getProducts(),
          MenuService.sendMessage("START_CHAT_SIGNAL")
        ]);
        setProducts(menu);
        setMessages([{ sender: 'bot', text: greeting }]);
      } catch (e) {
        setMessages([{ sender: 'bot', text: "Erro ao conectar ao servidor." }]);
      } finally {
        setIsLoading(false);
      }
    };
    init();
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;
    
    setMessages(prev => [...prev, { sender: 'user', text }]);
    setIsLoading(true);

    try {
      const response = await MenuService.sendMessage(text);
      setMessages(prev => [...prev, { sender: 'bot', text: response }]);
    } catch (e) {
      setMessages(prev => [...prev, { sender: 'bot', text: "Erro técnico." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return { products, messages, isLoading, sendMessage, scrollRef };
}