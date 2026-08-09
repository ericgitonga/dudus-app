import Link from "next/link";
import cards from "@/data/card_index.json";
import type { Card } from "@/types/card";
import { groupByOrder, orderTagline } from "@/lib/orders";

const allCards = cards as Card[];

export default function Home() {
  const groups = groupByOrder(allCards);

  return (
    <div className="min-h-screen bg-zinc-50" data-testid="browse-page">
      <main className="mx-auto max-w-5xl px-4 py-10">
        <div className="flex items-baseline justify-between">
          <h1 className="text-2xl font-semibold tracking-tight text-zinc-900">
            Dudus
          </h1>
          <div className="flex gap-4">
            <Link
              href="/search"
              className="text-sm font-medium underline hover:opacity-70"
            >
              Search
            </Link>
            <Link
              href="/identify"
              className="text-sm font-medium underline hover:opacity-70"
            >
              Identify a dudu
            </Link>
          </div>
        </div>
        <p className="mt-1 text-sm text-zinc-600">
          Kenyan arthropods, grouped by taxonomic order.
        </p>

        <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {groups.map(({ order, slug }) => (
            <Link
              key={order}
              href={`/orders/${slug}`}
              data-testid="order-button"
              data-order={order}
              className="flex flex-col rounded-lg border border-zinc-200 bg-white p-5 shadow-sm transition hover:shadow-md"
            >
              <span className="text-lg font-semibold text-zinc-900">
                {order}
              </span>
              <span className="mt-1 text-xs text-zinc-500">
                {orderTagline(order)}
              </span>
            </Link>
          ))}
        </div>
      </main>
    </div>
  );
}
