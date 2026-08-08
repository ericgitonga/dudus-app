"use client";

import { useState } from "react";

/**
 * In-app photo capture (issue #7). Uses accept="image/*" capture="environment" so mobile
 * browsers open the camera directly rather than the gallery — the honest limitation, agreed
 * with the user before building this, is that desktop browsers ignore `capture` and fall back
 * to a normal file picker (gallery included). No fully custom getUserMedia viewfinder was built;
 * this is the deliberately simpler option.
 *
 * Deliberately does nothing with the captured photo beyond a local preview — no upload, no
 * network call, nothing leaves the device. That's not a gap to fill in here: taxon-guessing
 * (#8) and index-matching (#9) are separate tickets, and geotag/EXIF handling (#10) has to be
 * settled before this photo ever gets processed, not folded in ad hoc.
 */
export default function PhotoCapture() {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setPreviewUrl((prev) => {
      if (prev) URL.revokeObjectURL(prev);
      return URL.createObjectURL(file);
    });
  }

  return (
    <div data-testid="photo-capture">
      <label
        htmlFor="specimen-photo"
        className="inline-block cursor-pointer rounded-lg border border-black/10 px-4 py-2 text-sm font-medium hover:opacity-70"
      >
        Take a photo
      </label>
      <input
        id="specimen-photo"
        type="file"
        accept="image/*"
        capture="environment"
        onChange={handleChange}
        className="sr-only"
        aria-label="Capture a photo of a specimen"
      />

      {previewUrl && (
        <div className="mt-4">
          {/* eslint-disable-next-line @next/next/no-img-element -- a locally captured blob: URL, not an optimizable static/remote asset */}
          <img
            data-testid="photo-preview"
            src={previewUrl}
            alt="Captured specimen"
            className="max-w-full rounded-lg"
          />
          <p className="mt-2 text-sm text-zinc-500">
            Identification isn&apos;t wired up yet — this just proves capture works.
          </p>
        </div>
      )}
    </div>
  );
}
