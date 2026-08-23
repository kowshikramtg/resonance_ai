import React from "react";
import { Cpu, BookOpen, FileText, Download, Loader2 } from "lucide-react";
import type { AnalysisResponse } from "../types";

interface WorkspaceProps {
  analysis: AnalysisResponse;
  draftSections: Record<string, string>;
  generatingSection: string | null;
  onGenerateSection: (section: string) => void;
  onSectionChange: (section: string, value: string) => void;
  onExport: (format: "latex" | "markdown") => void;
}

export const WorkspaceDashboard: React.FC<WorkspaceProps> = ({
  analysis,
  draftSections,
  generatingSection,
  onGenerateSection,
  onSectionChange,
  onExport,
}) => {
  return (
    <section className="max-w-6xl mx-auto px-6 my-16 md:my-20">
      <div className="glass-card p-8 md:p-12 space-y-8">
        {/* Minimalist Header without dots */}
        <div className="flex justify-between items-center border-b border-slate-300 dark:border-slate-800 pb-5">
          <span className="text-xs font-mono font-medium tracking-widest uppercase text-slate-700 dark:text-slate-200">
            Workspace Console
          </span>
          <span className="text-xs font-mono font-semibold text-slate-700 dark:text-slate-400">
            resonance-workspace.ai
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-left pt-2">
          {/* DNA */}
          <div className="space-y-4 md:border-r border-slate-300 dark:border-slate-800 md:pr-6">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800 dark:text-slate-100 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-[#315c91] dark:text-[#92b8e2]" />{" "}
              Research DNA
            </h3>
            <div className="bg-white/80 dark:bg-[#171d28] p-5 rounded-sm border border-slate-300 dark:border-slate-700 text-xs space-y-3 shadow-sm">
              <p className="text-slate-700 dark:text-slate-200">
                <strong className="font-extrabold">Problem:</strong>{" "}
                {analysis.dna.core_problem}
              </p>
              <p className="text-slate-700 dark:text-slate-200">
                <strong className="font-extrabold">Solution:</strong>{" "}
                {analysis.dna.proposed_solution}
              </p>
            </div>
          </div>

          {/* Discovery */}
          <div className="space-y-4 md:border-r border-slate-300 dark:border-slate-800 md:pr-6">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800 dark:text-slate-100 flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-[#b6533c] dark:text-[#f0a38f]" />{" "}
              OpenAlex Discovery
            </h3>
            <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
              {analysis.discovered_papers.map((p) => (
                <div
                  key={p.paper_id}
                  className="p-4 bg-white/80 dark:bg-[#171d28] rounded-sm border border-slate-300 dark:border-slate-700 text-xs space-y-1.5 shadow-sm"
                >
                  <a
                    href={p.url || "#"}
                    target="_blank"
                    rel="noreferrer"
                    className="font-semibold text-[#315c91] dark:text-[#a9c8ec] hover:underline line-clamp-2"
                  >
                    {p.title}
                  </a>
                  <span className="text-[11px] font-medium text-slate-600 dark:text-slate-400 block font-mono">
                    Year: {p.year} | Citations: {p.citation_count}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Manuscripts */}
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-800 dark:text-slate-100 flex items-center gap-2">
                <FileText className="w-4 h-4 text-amber-600 dark:text-amber-400" />{" "}
                Manuscripts
              </h3>
              <div className="flex gap-2">
                <button
                  onClick={() => onExport("latex")}
                  className="px-3 py-1 rounded-sm bg-[#17202a] text-white dark:bg-[#f3f5f8] dark:text-[#17202a] text-[11px] font-bold flex items-center gap-1 hover:opacity-80 cursor-pointer"
                >
                  <Download className="w-3 h-3" /> LaTeX
                </button>
                <button
                  onClick={() => onExport("markdown")}
                  className="px-3 py-1 rounded-sm bg-[#17202a] text-white dark:bg-[#f3f5f8] dark:text-[#17202a] text-[11px] font-bold flex items-center gap-1 hover:opacity-80 cursor-pointer"
                >
                  <Download className="w-3 h-3" /> MD
                </button>
              </div>
            </div>

            <div className="space-y-4">
              {["abstract", "introduction", "methodology"].map((sec) => (
                <div
                  key={sec}
                  className="p-4 bg-white/80 dark:bg-[#171d28] rounded-sm border border-slate-300 dark:border-slate-700 space-y-3 shadow-sm"
                >
                  <div className="flex justify-between items-center">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-slate-800 dark:text-slate-100">
                      {sec}
                    </span>
                    <button
                      onClick={() => onGenerateSection(sec)}
                      disabled={generatingSection === sec}
                      className="px-3 py-1 bg-[#315c91] text-white dark:bg-[#92b8e2] dark:text-[#17202a] rounded-sm text-[10px] font-bold flex items-center gap-1.5 cursor-pointer hover:opacity-90"
                    >
                      {generatingSection === sec && (
                        <Loader2 className="animate-spin w-3 h-3" />
                      )}
                      Draft
                    </button>
                  </div>
                  <textarea
                    rows={3}
                    value={draftSections[sec] || ""}
                    onChange={(e) => onSectionChange(sec, e.target.value)}
                    placeholder={`Drafting ${sec}...`}
                    className="w-full bg-transparent text-xs font-medium text-slate-700 dark:text-slate-200 focus:outline-none font-mono resize-none leading-relaxed placeholder-slate-400"
                  />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
