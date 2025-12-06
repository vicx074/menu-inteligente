import type { Product } from '../types';

export function ProductCard({ product }: { product: Product }) {
  return (
    <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-bold text-gray-800">{product.name}</h3>
        <span className="text-blue-600 font-bold bg-blue-50 px-2 py-1 rounded text-sm">
          R$ {product.price}
        </span>
      </div>
      <p className="text-sm text-gray-500">{product.description}</p>
    </div>
  );
}