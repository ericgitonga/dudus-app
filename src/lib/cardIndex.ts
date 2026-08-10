import type { Card } from "@/types/card";

export function sortCardsByCommonName(cards: Card[]): Card[] {
  return [...cards].sort((a, b) => a.common_name.localeCompare(b.common_name));
}

export function filterCardsByQuery(cards: Card[], query: string): Card[] {
  const q = query.trim().toLowerCase();
  if (!q) return cards;
  return cards.filter((card) => card.common_name.toLowerCase().includes(q));
}
