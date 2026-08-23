import React from "react";
import { Cpu, BookOpen, FileText, Download, Loader2, Sparkles } from "lucide-react";
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
      <div className="glass-card p-4 md:p-12 space-y-8">
        {/* Minimalist Header */}
        <div className="flex justify-between items-center border-b border-slate-300 dark:border-slate-800 pb-5">
          <span className="text-lg font-mono font-medium tracking-widest uppercase text-slate-700 dark:text-slate-200">
            Workspace Console
          </span>
          <span className="text-m font-mono text-slate-700 dark:text-slate-400">
            resonance-workspace.ai
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-left pt-2">
          {/* DNA Panel */}
          <div className="space-y-4 md:border-r border-slate-300 dark:border-slate-800 md:pr-6">
            <h3 className="text-s uppercase tracking-wider text-slate-800 dark:text-slate-100 flex items-center gap-2">
              <Cpu className="w-4 h-4 text-[#315c91] dark:text-[#92b8e2]" />{" "}
              Research DNA
            </h3>
            <div className="bg-white/80 dark:bg-[#171d28] p-5 rounded-sm border border-slate-300 dark:border-slate-700 text-xs space-y-3 shadow-sm">
              <p className="text-slate-700 dark:text-slate-200">
                <strong>Problem : </strong> {analysis.dna.core_problem}
              </p>
              <p className="text-slate-700 dark:text-slate-200">
                <strong>Solution : </strong> {analysis.dna.proposed_solution}
              </p>
            </div>
          </div>

          {/* Discovery Panel */}
          <div className="space-y-4 md:border-r border-slate-300 dark:border-slate-800 md:pr-6">
            <h3 className="text-s uppercase tracking-wider text-slate-800 dark:text-slate-100 flex items-center gap-2">
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
                    className="text-[15px] text-[#315c91] dark:text-[#a9c8ec] hover:underline line-clamp-2"
                  >
                    {p.title}
                  </a>
                  <span className="text-[13px] font-medium text-slate-600 dark:text-slate-400 block font-mono">
                    Year: {p.year} | Citations: {p.citation_count}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Manuscripts Panel */}
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-s uppercase tracking-wider text-slate-800 dark:text-slate-100 flex items-center gap-2">
                <FileText className="w-4 h-4 text-amber-600 dark:text-amber-400" />{" "}
                Manuscripts
              </h3>
              <div className="flex gap-2">
                <button
                  onClick={() => onExport("latex")}
                  className="px-3 py-1 rounded-sm bg-[#17202a] text-white dark:bg-[#f3f5f8] dark:text-[#17202a] text-[12px] font-bold flex items-center gap-1 hover:opacity-80 cursor-pointer"
                >
                  <Download className="w-3 h-3" /> LaTeX
                </button>
                <button
                  onClick={() => onExport("markdown")}
                  className="px-3 py-1 rounded-sm bg-[#17202a] text-white dark:bg-[#f3f5f8] dark:text-[#17202a] text-[12px] font-bold flex items-center gap-1 hover:opacity-80 cursor-pointer"
                >
                  <Download className="w-3 h-3" /> MD
                </button>
              </div>
            </div>

            <div className="space-y-4">
              {["Abstract", "Introduction", "Methodology"].map((sec) => {
                const isGenerating = generatingSection === sec;
                const hasContent = Boolean(draftSections[sec]?.trim());

                return (
                  <div
                    key={sec}
                    className={`p-3 bg-white/80 dark:bg-[#171d28] rounded-sm border transition-all duration-200 space-y-3 shadow-sm ${
                      isGenerating
                        ? "border-amber-500/80 ring-1 ring-amber-500/30 dark:border-amber-400/80"
                        : "border-slate-300 dark:border-slate-700"
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <div className="flex items-center gap-2">
                        <span className="text-[14px] font-medium tracking-wider text-slate-800 dark:text-slate-100">
                          {sec}
                        </span>
                        {isGenerating && (
                          <span className="flex items-center gap-1 text-[11px] font-mono text-amber-600 dark:text-amber-400 animate-pulse">
                            <span className="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                            Generating...
                          </span>
                        )}
                      </div>

                      <button
                        onClick={() => onGenerateSection(sec)}
                        disabled={isGenerating || generatingSection !== null}
                        className={`px-3 py-1 rounded-sm text-[12px] font-bold flex items-center gap-1.5 cursor-pointer transition-opacity ${
                          isGenerating
                            ? "bg-amber-600 text-white cursor-wait opacity-100"
                            : "bg-[#315c91] text-white dark:bg-[#92b8e2] dark:text-[#17202a] hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
                        }`}
                      >
                        {isGenerating ? (
                          <>
                            <Loader2 className="animate-spin w-3 h-3" />
                            Drafting
                          </>
                        ) : hasContent ? (
                          <>
                            <Sparkles className="w-3 h-3" />
                            Redraft
                          </>
                        ) : (
                          "Draft"
                        )}
                      </button>
                    </div>

                    <div className="relative">
                      <textarea
                        rows={isGenerating ? 4 : 3}
                        value={draftSections[sec] || ""}
                        disabled={isGenerating}
                        onChange={(e) => onSectionChange(sec, e.target.value)}
                        placeholder={
                          isGenerating
                            ? `Generating ${sec} section via Gemini... Please wait.`
                            : `Click "Draft" to synthesize ${sec}...`
                        }
                        className={`w-full bg-transparent text-[13px] font-medium text-slate-700 dark:text-slate-200 focus:outline-none font-mono resize-none leading-relaxed transition-opacity ${
                          isGenerating
                            ? "opacity-40 cursor-wait placeholder-amber-600/80 dark:placeholder-amber-400/80"
                            : "placeholder-slate-400"
                        }`}
                      />
                      {isGenerating && (
                        <div className="absolute inset-0 flex items-center justify-center bg-white/20 dark:bg-black/20 backdrop-blur-[1px]">
                          <div className="flex items-center gap-2 text-xs font-mono text-slate-800 dark:text-slate-200 bg-white dark:bg-[#1a2332] px-3 py-1.5 rounded border border-slate-300 dark:border-slate-700 shadow-md">
                            <Loader2 className="animate-spin w-3.5 h-3.5 text-amber-500" />
                            Drafting section content...
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};