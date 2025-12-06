import { Bot, User } from 'lucide-react';
import type { Message } from '../types';

export function MessageBubble({ message }: { message: Message }) {
  const isBot = message.sender === 'bot';
  return (
    <div className={`flex gap-3 ${isBot ? 'flex-row' : 'flex-row-reverse'} animate-fade-in`}>
      <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 
        ${isBot ? 'bg-blue-100 text-blue-600' : 'bg-gray-200 text-gray-600'}`}>
        {isBot ? <Bot size={18} /> : <User size={18} />}
      </div>
      <div className={`max-w-[85%] p-3 rounded-2xl text-sm leading-relaxed shadow-sm
        ${isBot ? 'bg-white text-gray-800 rounded-tl-none border border-gray-200' : 'bg-blue-600 text-white rounded-tr-none'}`}>
        <p className="whitespace-pre-wrap">{message.text}</p>
      </div>
    </div>
  );
}