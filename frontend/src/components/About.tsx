import React from "react";
import { ArrowLeft, ArrowRight } from "lucide-react";

interface AboutProps {
  onReturnHome: () => void;
}

export const About: React.FC<AboutProps> = ({ onReturnHome }) => {
  return (
    <main className="max-w-5xl mx-auto px-6 py-20 md:py-28">
      <button
        onClick={onReturnHome}
        className="inline-flex items-center gap-2 text-xs font-medium text-[#315c91] dark:text-[#9dbce0] hover:underline underline-offset-4"
      >
        <ArrowLeft className="w-4 h-4" /> Back to research brief
      </button>
      <div className="max-w-3xl mt-16">
        <p className="text-[11px] font-mono tracking-[0.18em] uppercase text-[#315c91] dark:text-[#9dbce0]">
          About Resonance
        </p>
        <h1 className="mt-5 text-5xl md:text-7xl font-normal font-serif leading-[0.98] text-[#17202a] dark:text-[#f3f5f8]">
          Serious tools for the early, uncertain part of research.
        </h1>
        <p className="mt-8 max-w-2xl text-lg leading-relaxed text-slate-600 dark:text-slate-300">
          Resonance helps engineers and researchers move from an initial idea to
          a defensible direction. It organizes the question, finds relevant
          literature, surfaces gaps, and gives the first manuscript a useful
          structure.
        </p>
      </div>
      <div className="grid md:grid-cols-3 gap-8 mt-20 pt-8 border-t border-slate-300 dark:border-slate-700">
        {[
          [
            "01",
            "Clarify",
            "Turn a rough technical idea into a brief with a precise question and context.",
          ],
          [
            "02",
            "Ground",
            "Connect the direction to current literature instead of starting from a blank page.",
          ],
          [
            "03",
            "Build",
            "Shape the findings into a working manuscript that can be reviewed and improved.",
          ],
        ].map(([number, title, description]) => (
          <article key={number}>
            <span className="font-mono text-xs text-[#315c91] dark:text-[#9dbce0]">
              {number}
            </span>
            <h2 className="mt-4 text-xl font-medium text-slate-900 dark:text-slate-100">
              {title}
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-slate-600 dark:text-slate-300">
              {description}
            </p>
          </article>
        ))}
      </div>
      <button
        onClick={onReturnHome}
        className="mt-16 inline-flex items-center gap-2 text-sm font-medium text-[#315c91] dark:text-[#9dbce0] hover:underline underline-offset-4"
      >
        Begin with a research brief <ArrowRight className="w-4 h-4" />
      </button>
    </main>
  );
};
