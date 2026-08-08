"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import type { Card } from "@/types/card";
import NotYetResearched from "@/components/NotYetResearched";

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
        aria-label="Search dudus by common name"
        className="w-full rounded-lg border border-black/10 bg-transparent px-4 py-2 text-base outline-none focus:ring-2 focus:ring-foreground/30"
      />

      <p
        data-testid="result-count"
        className="mt-3 text-sm text-zinc-500"
      >
        {filtered.length} of {cards.length} dudus
      </p>

      {filtered.length === 0 ? (
        <NotYetResearched query={query} onClear={() => setQuery("")} />
      ) : (
        <ul
          data-testid="card-list"
          className="mt-4 divide-y divide-black/10"
        >
          {filtered.map((card) => {
            const taxonomyLine = [card.family, card.order]
              .filter(Boolean)
              .join(" · ");
            return (
              <li key={card.id} className="py-3">
                <Link
                  href={`/dudus/${card.id}`}
                  className="flex items-center gap-3 hover:opacity-70"
                >
                  {card.photo_ref && (
                    <div className="relative h-12 w-12 shrink-0 overflow-hidden rounded-md">
                      <Image
                        src={card.photo_ref}
                        alt={card.common_name}
                        fill
                        className="object-cover"
                        sizes="48px"
                      />
                    </div>
                  )}
                  <div>
                    <div className="font-medium">{card.common_name}</div>
                    {card.scientific_name && (
                      <div className="text-sm italic text-zinc-600">
                        {card.scientific_name}
                      </div>
                    )}
                    <div className="text-xs text-zinc-500">
                      {taxonomyLine || `Taxonomy confirmed to ${card.taxon_rank} level only`}
                    </div>
                  </div>
                </Link>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
