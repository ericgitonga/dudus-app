import { notFound } from "next/navigation";
import Link from "next/link";
import cards from "@/data/card_index.json";
import type { Card } from "@/types/card";
import DuduGridCard from "@/components/DuduGridCard";
import { groupByOrder, orderTagline } from "@/lib/orders";

const allCards = cards as Card[];

export function generateStaticParams() {
  return groupByOrder(allCards).map((group) => ({ order: group.slug }));
}

export default async function OrderPage({
  params,
}: {
  params: Promise<{ order: string }>;
}) {
  const { order: slug } = await params;
  const group = groupByOrder(allCards).find((g) => g.slug === slug);
  if (!group) notFound();

  return (
    <div className="min-h-screen bg-zinc-50" data-testid="order-page" data-order={group.order}>
      <main className="mx-auto max-w-5xl px-4 py-10">
        <Link href="/" className="text-sm text-zinc-500 hover:underline">
          ← All orders
        </Link>

        <h1 className="mt-4 text-2xl font-semibold tracking-tight text-zinc-900">
          {group.order}
        </h1>
        <p className="mt-1 text-sm text-zinc-600">{orderTagline(group.order)}</p>

        <div className="mt-8 grid grid-cols-2 gap-2 sm:grid-cols-4 lg:grid-cols-6">
          {group.cards.map((card) => (
            <DuduGridCard key={card.id} card={card} />
          ))}
        </div>
      </main>
    </div>
  );
}
