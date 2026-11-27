export default function ItemCard({ item }) {
  return (
    <article className="flex flex-col rounded-2xl bg-white p-5 shadow-sm ring-1 ring-stone-200 transition hover:-translate-y-0.5 hover:shadow-md">
      <p className="text-xs uppercase tracking-wide text-brand-700">{item.kind}</p>
      <h3 className="mt-2 font-display text-lg text-stone-900">{item.title}</h3>
      {item.short_description && (
        <p className="mt-2 line-clamp-3 text-sm text-stone-600">{item.short_description}</p>
      )}
    </article>
  );
}
