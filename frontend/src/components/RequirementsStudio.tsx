import React from "react";
import { ArrowRight } from "lucide-react";

interface StudioProps {
  form: {
    raw_ideology: string;
    target_problem: string;
    proposed_method: string;
  };
  loading: boolean;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  onSubmit: (e: React.FormEvent) => void;
}

export const RequirementStudio: React.FC<StudioProps> = ({
  form,
  loading,
  onChange,
  onSubmit,
}) => {
  return (
    <section id="studio" className="max-w-4xl mx-auto px-6 pt-12 pb-24">
      <div className="border-t border-slate-300 dark:border-slate-700 pt-10 mb-9">
        <span className="text-[11px] font-mono font-medium tracking-[0.18em] text-[#315c91] dark:text-[#9dbce0] uppercase">
          Research brief / intake
        </span>
        <h2 className="mt-3 text-3xl md:text-4xl font-normal font-serif text-[#17202a] dark:text-[#f3f5f8]">
          Start with the question behind the work.
        </h2>
        <p className="mt-3 text-sm text-slate-600 dark:text-slate-300 max-w-xl leading-relaxed">
          A concise brief gives the pipeline enough context to find useful
          literature and shape a credible first draft.
        </p>
      </div>

      <form onSubmit={onSubmit} className="studio-card p-6 md:p-9 space-y-8">
        <div className="space-y-3">
          <label className="flex items-baseline gap-3 text-sm font-medium text-slate-900 dark:text-slate-100">
            <span className="text-[11px] font-mono text-[#315c91] dark:text-[#9dbce0]">
              01
            </span>
            <span>Research question</span>
          </label>
          <p className="ml-8 text-xs text-slate-500 dark:text-slate-400">
            What scientific or technical problem are you investigating?
          </p>
          <textarea
            name="raw_ideology"
            rows={3}
            value={form.raw_ideology}
            onChange={onChange}
            placeholder="Describe the question your work needs to answer."
            className="studio-textarea"
          />
        </div>

        <div className="space-y-3">
          <label className="flex items-baseline gap-3 text-sm font-medium text-slate-900 dark:text-slate-100">
            <span className="text-[11px] font-mono text-[#315c91] dark:text-[#9dbce0]">
              02
            </span>
            <span>Research context</span>
          </label>
          <p className="ml-8 text-xs text-slate-500 dark:text-slate-400">
            What limitation, situation, or knowledge gap motivates this
            research?
          </p>
          <textarea
            name="target_problem"
            rows={3}
            value={form.target_problem}
            onChange={onChange}
            placeholder="Explain what is missing, limited, or unresolved today."
            className="studio-textarea"
          />
        </div>

        <div className="space-y-3">
          <label className="flex items-baseline gap-3 text-sm font-medium text-slate-900 dark:text-slate-100">
            <span className="text-[11px] font-mono text-[#315c91] dark:text-[#9dbce0]">
              03
            </span>
            <span>Technical direction</span>
          </label>
          <p className="ml-8 text-xs text-slate-500 dark:text-slate-400">
            What methods, technologies, datasets, or constraints are relevant?
          </p>
          <textarea
            name="proposed_method"
            rows={3}
            value={form.proposed_method}
            onChange={onChange}
            placeholder="Note the methods, tools, data, or constraints you already have in mind."
            className="studio-textarea"
          />
        </div>

        <div className="flex justify-end pt-2">
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-3 bg-[#315c91] hover:bg-[#264b79] disabled:bg-slate-400 text-white rounded-sm font-medium text-xs tracking-wide flex items-center justify-center gap-2 transition cursor-pointer"
          >
            <span>
              {loading
                ? "Building research pipeline..."
                : "Build research pipeline"}
            </span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </form>
    </section>
  );
};
