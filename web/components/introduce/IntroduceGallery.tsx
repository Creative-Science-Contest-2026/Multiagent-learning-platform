/* eslint-disable i18n/no-literal-ui-text */
"use client";

import Image from "next/image";
import { useState } from "react";
import type { IntroduceGalleryItem } from "./introduce-content";
import { IntroduceLightbox } from "./IntroduceLightbox";

interface IntroduceGalleryProps {
  items: IntroduceGalleryItem[];
}

export function IntroduceGallery({ items }: IntroduceGalleryProps) {
  const [selectedItem, setSelectedItem] = useState<IntroduceGalleryItem | null>(null);

  return (
    <>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {items.map((item, index) => (
          <button
            key={item.id}
            type="button"
            onClick={() => setSelectedItem(item)}
            className={`group overflow-hidden rounded-[24px] border border-[rgba(10,21,48,0.08)] bg-white text-left shadow-[0_16px_48px_rgba(10,21,48,0.06)] transition-transform duration-200 hover:-translate-y-1 hover:shadow-[0_22px_60px_rgba(10,21,48,0.12)] ${
              index === 0 ? "md:col-span-2 xl:col-span-2" : ""
            }`}
            aria-label={`${item.titleVi} / ${item.titleEn}`}
          >
            <div className="overflow-hidden border-b border-[rgba(10,21,48,0.08)] bg-[#f6f5f4]">
              <Image
                src={item.src}
                alt={item.titleVi}
                width={1600}
                height={1000}
                className="h-auto w-full object-cover transition-transform duration-300 group-hover:scale-[1.01]"
              />
            </div>
            <div className="space-y-3 px-5 py-5">
              <div className="flex items-center justify-between gap-3">
                <span className="rounded-full bg-[#eef3fb] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-[#50607d]">
                  {item.tagVi}
                </span>
                <span className="text-[11px] font-semibold uppercase tracking-[0.16em] text-[#7a869c]">
                  Open
                </span>
              </div>
              <div>
                <h3 className="text-xl font-semibold tracking-[-0.03em] text-[#0a1530]">
                  {item.titleVi}
                </h3>
                <p className="mt-1 text-sm font-medium text-[#50607d]">{item.titleEn}</p>
              </div>
              <p className="text-sm leading-7 text-[#24324a]">{item.captionVi}</p>
              <p className="text-xs leading-6 text-[#50607d]">{item.captionEn}</p>
            </div>
          </button>
        ))}
      </div>

      <IntroduceLightbox item={selectedItem} onClose={() => setSelectedItem(null)} />
    </>
  );
}
