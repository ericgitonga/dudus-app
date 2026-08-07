import cards from "@/data/card_index.json";
import type { Card } from "@/types/card";
import CardBrowser from "@/components/CardBrowser";

export default function Home() {
  return (
    <div className="flex flex-col flex-1 items-center bg-zinc-50 dark:bg-black">
      <main className="flex flex-1 w-full max-w-2xl flex-col items-stretch py-16 px-6 bg-white dark:bg-black">
        <h1 className="text-2xl font-semibold tracking-tight">Dudus</h1>
        <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
          Kenyan arthropods, researched and reviewed.
        </p>
        <div className="mt-8">
          <CardBrowser cards={cards as Card[]} />
        </div>
      </main>
    </div>
  );
}
