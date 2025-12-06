'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';

export default function Home() {
  const [items, setItems] = useState<Array<{ id: number; name: string }>>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchItems = async () => {
      try {
        setLoading(true);
        const response = await api.get('/api/items');
        setItems(response.data.items);
        setError(null);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : 'Failed to fetch items'
        );
      } finally {
        setLoading(false);
      }
    };

    fetchItems();
  }, []);

  return (
    <main className="container mx-auto py-12">
      <div className="max-w-2xl mx-auto text-center">
        <h1 className="text-5xl font-bold mb-4 text-gradient">
          FastAPI + Next.js
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          A modern monorepo combining Python backend and React frontend
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 my-12">
          <div className="p-6 bg-white rounded-lg shadow-lg hover:shadow-xl transition">
            <h2 className="text-2xl font-bold mb-2">🚀 Backend (FastAPI)</h2>
            <p className="text-gray-600 mb-4">
              High-performance async API with automatic documentation
            </p>
            <a
              href={`${process.env.NEXT_PUBLIC_API_URL}/docs`}
              className="inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
              target="_blank"
              rel="noopener noreferrer"
            >
              View API Docs →
            </a>
          </div>

          <div className="p-6 bg-white rounded-lg shadow-lg hover:shadow-xl transition">
            <h2 className="text-2xl font-bold mb-2">⚡ Frontend (Next.js)</h2>
            <p className="text-gray-600 mb-4">
              Modern React with TypeScript and Tailwind CSS
            </p>
            <button
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition disabled:opacity-50"
              disabled
            >
              You are here ✓
            </button>
          </div>
        </div>

        <div className="my-12">
          <h3 className="text-2xl font-bold mb-6">Items from Backend</h3>

          {loading && (
            <p className="text-gray-500 py-4">Loading items...</p>
          )}

          {error && (
            <div className="p-4 bg-red-50 text-red-700 rounded mb-4">
              Error: {error}
            </div>
          )}

          {!loading && !error && (
            <div className="bg-white rounded-lg shadow p-6">
              {items.length > 0 ? (
                <ul className="space-y-2">
                  {items.map((item) => (
                    <li key={item.id} className="p-2 border-l-4 border-blue-600">
                      {item.name}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500">No items available</p>
              )}
            </div>
          )}
        </div>

        <div className="mt-12 p-8 bg-gray-50 rounded-lg">
          <h3 className="text-xl font-bold mb-4">📚 Getting Started</h3>
          <pre className="bg-gray-900 text-green-400 p-4 rounded overflow-x-auto text-sm">
            {`# Install dependencies
make install

# Run in development
make docker-up

# Or run separately
make backend-dev
make frontend-dev`}
          </pre>
        </div>
      </div>
    </main>
  );
}
