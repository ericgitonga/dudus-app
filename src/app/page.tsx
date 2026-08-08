import Link from "next/link";
import cards from "@/data/card_index.json";
import type { Card } from "@/types/card";
import DuduGridCard from "@/components/DuduGridCard";

const allCards = cards as Card[];
const UNCLASSIFIED_LABEL = "Order not yet identified";

function groupByOrder(cards: Card[]) {
  const groups = new Map<string, Card[]>();
  for (const card of cards) {
    const key = card.order ?? UNCLASSIFIED_LABEL;
    const group = groups.get(key) ?? [];
    group.push(card);
    groups.set(key, group);
  }
  const orders = [...groups.keys()]
    .filter((order) => order !== UNCLASSIFIED_LABEL)
    .sort((a, b) => a.localeCompare(b));
  if (groups.has(UNCLASSIFIED_LABEL)) orders.push(UNCLASSIFIED_LABEL);
  return orders.map((order) => ({ order, cards: groups.get(order)! }));
}

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

        <div className="mt-8 flex flex-col gap-10">
          {groups.map(({ order, cards }) => (
            <section key={order} data-testid="order-group" data-order={order}>
              <h2 className="text-xl font-semibold text-zinc-900">{order}</h2>
              <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {cards.map((card) => (
                  <DuduGridCard key={card.id} card={card} />
                ))}
              </div>
            </section>
          ))}
        </div>
      </main>
    </div>
  );
}
