import Link from "next/link";
import PhotoCapture from "@/components/PhotoCapture";

export default function IdentifyPage() {
  return (
    <div className="flex flex-col flex-1 items-center bg-zinc-50">
      <main className="flex flex-1 w-full max-w-2xl flex-col items-stretch py-16 px-6 bg-white">
        <Link
          href="/"
          className="text-sm text-zinc-500 hover:underline"
        >
          ← All dudus
        </Link>

        <h1 className="mt-4 text-2xl font-semibold tracking-tight">
          Identify a dudu
        </h1>
        <p className="mt-1 text-sm text-zinc-600">
          Photograph what you found.
        </p>

        <div className="mt-8">
          <PhotoCapture />
        </div>
      </main>
    </div>
  );
}
