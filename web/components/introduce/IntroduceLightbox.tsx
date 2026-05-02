/* eslint-disable i18n/no-literal-ui-text */
"use client";

import Image from "next/image";
import { useEffect } from "react";
import { X } from "lucide-react";
import type { IntroduceGalleryItem } from "./introduce-content";

interface IntroduceLightboxProps {
  item: IntroduceGalleryItem | null;
  onClose: () => void;
}

export function IntroduceLightbox({ item, onClose }: IntroduceLightboxProps) {
  useEffect(() => {
    if (!item) {
      return undefined;
    }

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onClose();
      }
    };

    document.body.style.overflow = "hidden";
    window.addEventListener("keydown", onKeyDown);

    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [item, onClose]);

  if (!item) {
    return null;
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-[#071024]/78 px-4 py-6 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby={`introduce-lightbox-title-${item.id}`}
        className="max-h-full w-full max-w-6xl overflow-hidden rounded-[28px] border border-white/12 bg-[#08101f] text-white shadow-[0_40px_120px_rgba(0,0,0,0.45)]"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-4 border-b border-white/10 px-5 py-4">
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-[0.16em] text-white/52">
              {item.tagVi} / {item.tagEn}
            </p>
            <h3
              id={`introduce-lightbox-title-${item.id}`}
              className="mt-2 text-2xl font-semibold tracking-[-0.04em] text-white"
            >
              {item.titleVi}
            </h3>
            <p className="mt-1 text-sm text-white/68">{item.titleEn}</p>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-white/12 bg-white/8 text-white transition-colors hover:bg-white/14"
            aria-label="Đóng / Close"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <div className="grid gap-0 lg:grid-cols-[minmax(0,1fr)_280px]">
          <div className="overflow-auto bg-[#040912] p-4">
            <div className="overflow-hidden rounded-[20px] border border-white/8">
              <Image
                src={item.src}
                alt={item.titleVi}
                width={1800}
                height={1100}
                className="h-auto w-full object-cover"
              />
            </div>
          </div>
          <div className="border-t border-white/10 px-5 py-5 lg:border-l lg:border-t-0">
            <p className="text-sm leading-7 text-white/86">{item.captionVi}</p>
            <p className="mt-3 text-sm leading-7 text-white/62">{item.captionEn}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
