"use client";

import { useMemo, useState } from "react";
import type { Card } from "@/types/card";

export default function CardBrowser({ cards }: { cards: Card[] }) {
  const [query, setQuery] = useState("");

  const sorted = useMemo(
    () => [...cards].sort((a, b) => a.common_name.localeCompare(b.common_name)),
    [cards],
  );

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return sorted;
    return sorted.filter((card) => card.common_name.toLowerCase().includes(q));
  }, [sorted, query]);

  return (
    <div className="w-full">
      <input
        type="search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search by common name…"
        aria-label="Search species by common name"
        className="w-full rounded-lg border border-black/10 dark:border-white/20 bg-transparent px-4 py-2 text-base outline-none focus:ring-2 focus:ring-foreground/30"
      />

      <p
        data-testid="result-count"
        className="mt-3 text-sm text-zinc-500 dark:text-zinc-400"
      >
        {filtered.length} of {cards.length} species
      </p>

      {filtered.length === 0 ? (
        <p data-testid="no-results" className="mt-6 text-sm text-zinc-500 dark:text-zinc-400">
          No species match &quot;{query}&quot;.
        </p>
      ) : (
        <ul
          data-testid="card-list"
          className="mt-4 divide-y divide-black/10 dark:divide-white/10"
        >
          {filtered.map((card) => {
            const taxonomyLine = [card.family, card.order]
              .filter(Boolean)
              .join(" · ");
            return (
              <li key={card.id} className="py-3">
                <div className="font-medium">{card.common_name}</div>
                {card.scientific_name && (
                  <div className="text-sm italic text-zinc-600 dark:text-zinc-400">
                    {card.scientific_name}
                  </div>
                )}
                <div className="text-xs text-zinc-500 dark:text-zinc-500">
                  {taxonomyLine || `Taxonomy confirmed to ${card.taxon_rank} level only`}
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
