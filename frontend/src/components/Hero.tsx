import React from "react";
import { ArrowDown } from "lucide-react";

interface HeroProps {
  onScrollToStudio: () => void;
}

export const Hero: React.FC<HeroProps> = ({ onScrollToStudio }) => {
  return (
    <section className="max-w-5xl mx-auto px-6 pt-20 md:pt-28 pb-12 text-center">
      <div className="mb-7 text-[11px] font-mono font-medium tracking-[0.18em] text-[#315c91] dark:text-[#9dbce0] uppercase">
        Research intelligence / paper engineering
      </div>

      <h1 className="max-w-4xl mx-auto text-5xl md:text-7xl tracking-tight font-normal text-[#17202a] dark:text-[#f3f5f8] leading-[0.98]">
        Intelligence that <br />
        <span className="font-serif italic text-[#315c91] dark:text-[#9dbce0]">
          makes research actionable
        </span>
      </h1>

      <p className="max-w-xl mx-auto mt-7 text-base text-slate-600 dark:text-slate-300 leading-relaxed">
        Turn an early technical idea into a structured research direction,
        grounded literature review, and working manuscript.
      </p>

      <div className="mt-8">
        <button
          onClick={onScrollToStudio}
          className="px-5 py-3 rounded-sm bg-[#17202a] dark:bg-[#f3f5f8] hover:bg-[#263542] dark:hover:bg-white text-white dark:text-[#17202a] font-medium text-xs tracking-wide inline-flex items-center gap-2 transition cursor-pointer"
        >
          <span>Start with a research brief</span>
          <ArrowDown className="w-4 h-4" />
        </button>
      </div>
    </section>
  );
};
