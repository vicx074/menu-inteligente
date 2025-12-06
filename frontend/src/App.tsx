import { useState } from 'react';
import { Send, Menu as MenuIcon, RefreshCcw } from 'lucide-react'; // Importe o ícone RefreshCcw
import { useChat } from './hooks/useChat';
import { ProductCard } from './components/ProductCard';
import { MessageBubble } from './components/MessageBubble';

function App() {
  // Pega os novos estados e funções
  const { products, messages, isLoading, isOrderCompleted, sendMessage, resetChat, scrollRef } = useChat();
  const [input, setInput] = useState('');

  const handleSend = () => {
    sendMessage(input);
    setInput('');
  };

  return (
    <div className="flex h-screen bg-slate-50 font-sans">
      {/* Sidebar igual ... */}
      <aside className="w-1/3 max-w-md bg-white border-r border-gray-200 hidden md:flex flex-col z-20 shadow-sm">
        <div className="p-6 border-b border-gray-100 bg-white">
          <h1 className="text-xl font-bold text-gray-800 flex items-center gap-2">
            <MenuIcon className="text-blue-600" />
            Cardápio Digital
          </h1>
          <p className="text-sm text-gray-500 mt-1 pl-8">Restaurante do Vitinho</p>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-slate-50">
          {products.map(p => <ProductCard key={p.id} product={p} />)}
        </div>
      </aside>

      {/* Main Chat */}
      <main className="flex-1 flex flex-col relative bg-slate-50">
        <header className="bg-white p-4 border-b border-gray-200 shadow-sm z-10 flex items-center justify-between">
          <h2 className="font-semibold text-gray-800 flex items-center gap-2">
             Garçom do Vitinho
            <span className={`flex h-2 w-2 relative ml-2`}>
               {/* Muda a cor da bolinha se tiver finalizado */}
              <span className={`relative inline-flex rounded-full h-2 w-2 ${isOrderCompleted ? 'bg-red-500' : 'bg-green-500'}`}></span>
            </span>
          </h2>
          {/* Botão de Resetar no Topo também (opcional) */}
          <button onClick={resetChat} className="text-sm text-gray-500 hover:text-blue-600 flex items-center gap-1">
            <RefreshCcw size={14}/> Reiniciar
          </button>
        </header>

        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          {messages.map((msg, idx) => (
            <MessageBubble key={idx} message={msg} />
          ))}
          {isLoading && <div className="text-xs text-gray-400 italic ml-12 animate-pulse">Digitando...</div>}
          <div ref={scrollRef} />
        </div>

        {/* --- ÁREA DE INPUT INTELIGENTE --- */}
        <div className="p-4 bg-white border-t border-gray-200">
          <div className="max-w-4xl mx-auto">
            
            {isOrderCompleted ? (
              // MODO FINALIZADO: Mostra botão de Novo Pedido
              <div className="flex flex-col items-center gap-3 py-2 animate-fade-in">
                <p className="text-green-600 font-medium">Pedido enviado para a cozinha! ✅</p>
                <button 
                  onClick={resetChat}
                  className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl font-bold flex items-center gap-2 shadow-lg hover:shadow-xl transition-all w-full md:w-auto justify-center"
                >
                  <RefreshCcw size={20} /> Iniciar Novo Atendimento
                </button>
              </div>
            ) : (
              // MODO NORMAL: Mostra Input
              <div className="flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                  placeholder="Digite seu pedido..."
                  className="flex-1 px-4 py-3 bg-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all text-gray-800"
                  disabled={isLoading}
                />
                <button
                  onClick={handleSend}
                  disabled={isLoading || !input.trim()}
                  className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white p-3 rounded-xl transition-colors shadow-lg shadow-blue-500/30"
                >
                  <Send size={20} />
                </button>
              </div>
            )}

          </div>
        </div>
      </main>
    </div>
  );
}

export default App;