import type { Metadata } from "next";
import { Newsreader, Archivo_Narrow, IBM_Plex_Mono } from "next/font/google";
import { Analytics } from "@vercel/analytics/next";
import { SpeedInsights } from "@vercel/speed-insights/next";
import "./globals.css";

// ericgitonga.com shared brand kit type trio — see globals.css for how these feed the
// Tailwind theme tokens, and SKILL.md/ONBOARDING.md context for the sibling repos this
// matches (eric-gitonga-links, dudu-merchandise PR #109).
const newsreader = Newsreader({
  variable: "--font-newsreader",
  subsets: ["latin"],
  weight: ["500"],
  style: ["italic"],
});

const archivoNarrow = Archivo_Narrow({
  variable: "--font-archivo-narrow",
  subsets: ["latin"],
  weight: ["500", "600"],
});

const ibmPlexMono = IBM_Plex_Mono({
  variable: "--font-ibm-plex-mono",
  subsets: ["latin"],
  weight: ["400", "500"],
});

export const metadata: Metadata = {
  title: "Dudus",
  description:
    "Photo-based lookup companion for the Dudus/Kito's Dudus Kenyan entomology curriculum",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${newsreader.variable} ${archivoNarrow.variable} ${ibmPlexMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <a
          href="https://ericgitonga.com"
          className="block border-b border-line px-4 py-2 text-center font-mono text-xs uppercase tracking-widest text-muted transition-colors hover:text-accent"
        >
          ← ericgitonga.com
        </a>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
