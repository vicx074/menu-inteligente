import { useState } from 'react';
import { Send, Menu as MenuIcon } from 'lucide-react';
import { useChat } from './hooks/useChat';
import { ProductCard } from './components/ProductCard';
import { MessageBubble } from './components/MessageBubble';

function App() {
  const { products, messages, isLoading, sendMessage, scrollRef } = useChat();
  const [input, setInput] = useState('');

  const handleSend = () => {
    sendMessage(input);
    setInput('');
  };

  return (
    <div className="flex h-screen bg-slate-50 font-sans">
      {/* Sidebar - Cardápio */}
      <aside className="w-1/3 max-w-md bg-white border-r border-gray-200 hidden md:flex flex-col">
        <div className="p-6 border-b border-gray-100">
          <h1 className="text-xl font-bold text-gray-800 flex items-center gap-2">
            <MenuIcon className="text-blue-600" /> Cardápio
          </h1>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-slate-50">
          {products.map(p => <ProductCard key={p.id} product={p} />)}
        </div>
      </aside>

      {/* Chat */}
      <main className="flex-1 flex flex-col relative">
        <header className="bg-white p-4 border-b border-gray-200 shadow-sm z-10">
          <h2 className="font-semibold text-gray-800">🤖 Garçom Virtual</h2>
        </header>

        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((m, i) => <MessageBubble key={i} message={m} />)}
          {isLoading && <div className="text-xs text-gray-400 italic ml-12">Digitando...</div>}
          <div ref={scrollRef} />
        </div>

        <div className="p-4 bg-white border-t border-gray-200">
          <div className="flex gap-2 max-w-4xl mx-auto">
            <input
              className="flex-1 px-4 py-3 bg-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50"
              placeholder="Digite seu pedido..."
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyPress={e => e.key === 'Enter' && handleSend()}
              disabled={isLoading}
            />
            <button onClick={handleSend} disabled={isLoading || !input.trim()} 
              className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-xl disabled:bg-gray-300">
              <Send size={20} />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;