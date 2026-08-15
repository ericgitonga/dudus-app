import Link from "next/link";
import Image from "next/image";
import type { Card } from "@/types/card";
import TechnicalReportLink from "@/components/TechnicalReportLink";

export default function DuduGridCard({ card }: { card: Card }) {
  return (
    <div
      data-testid="grid-card"
      data-dudu-id={card.id}
      className="flex flex-col overflow-hidden rounded-lg border border-zinc-200 bg-white shadow-sm transition hover:shadow-md"
    >
      <Link href={`/dudus/${card.id}`}>
        {card.photo_ref ? (
          <div className="relative aspect-[4/3] w-full bg-zinc-100">
            <Image
              src={card.photo_ref}
              alt={card.common_name}
              fill
              className="object-cover"
              sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
            />
          </div>
        ) : (
          <div className="flex aspect-[4/3] w-full items-center justify-center bg-zinc-100 text-sm text-zinc-400">
            No photo yet
          </div>
        )}
      </Link>

      {card.technical_sections.length > 0 && (
        <div className="border-b border-zinc-100 px-4 py-2">
          <TechnicalReportLink
            commonName={card.common_name}
            sections={card.technical_sections}
          />
        </div>
      )}

      <Link href={`/dudus/${card.id}`} className="p-4">
        <p className="font-semibold text-zinc-900">{card.common_name}</p>
        {card.scientific_name && (
          <p className="text-sm italic text-zinc-500">{card.scientific_name}</p>
        )}
      </Link>
    </div>
  );
}
