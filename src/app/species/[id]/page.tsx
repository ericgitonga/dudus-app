import { notFound } from "next/navigation";
import Link from "next/link";
import cards from "@/data/card_index.json";
import type { Card } from "@/types/card";

const allCards = cards as Card[];

export function generateStaticParams() {
  return allCards.map((card) => ({ id: card.id }));
}

export default async function SpeciesPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const card = allCards.find((c) => c.id === id);
  if (!card) notFound();

  const taxonomyLine = [card.family, card.order].filter(Boolean).join(" · ");

  return (
    <div className="flex flex-col flex-1 items-center bg-zinc-50 dark:bg-black">
      <main
        data-testid="species-detail"
        className="flex flex-1 w-full max-w-2xl flex-col items-stretch py-16 px-6 bg-white dark:bg-black"
      >
        <Link
          href="/"
          className="text-sm text-zinc-500 dark:text-zinc-400 hover:underline"
        >
          ← All species
        </Link>

        <h1 className="mt-4 text-2xl font-semibold tracking-tight">
          {card.common_name}
        </h1>
        {card.scientific_name && (
          <p className="mt-1 italic text-zinc-600 dark:text-zinc-400">
            {card.scientific_name}
          </p>
        )}
        <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-500">
          {taxonomyLine || `Taxonomy confirmed to ${card.taxon_rank} level only`}
        </p>

        <div className="mt-8 flex flex-col gap-6">
          {card.sections.map((section) => (
            <section key={section.heading}>
              <h2 className="text-lg font-medium">{section.heading}</h2>
              <p className="mt-1 text-zinc-700 dark:text-zinc-300">
                {section.body}
              </p>
            </section>
          ))}
        </div>
      </main>
    </div>
  );
}
