import { useEffect, useState } from "react";
import { listItems } from "./api.js";
import ItemCard from "./components/ItemCard.jsx";

export default function App() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    listItems()
      .then(setItems)
      .catch((err) => setError(err.message));
  }, []);

  return (
    <main className="mx-auto max-w-6xl px-6 py-12">
      <header className="mb-10">
        <h1 className="font-display text-4xl text-stone-900">NatyaSutra</h1>
        <p className="mt-3 max-w-2xl text-stone-600">
          Skeleton page. Replace with the real experiences from the design system.
        </p>
      </header>

      {error && (
        <p role="alert" className="rounded-lg bg-red-50 p-4 text-sm text-red-700">
          Could not load content: {error}
        </p>
      )}

      <section className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {items.map((item) => (
          <ItemCard key={item.id} item={item} />
        ))}
      </section>
    </main>
  );
}
