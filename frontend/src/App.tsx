import React, { useState } from "react";
import { Navbar } from "./components/Navbar";
import { Hero } from "./components/Hero";
import { WorkspaceDashboard } from "./components/WorkspaceDashboard";
import { RequirementStudio } from "./components/RequirementsStudio";
import { About } from "./components/About";
import {
  analyzeIdeology,
  generatePaperSection,
  exportPaper,
} from "./services/api.ts";
import type { AnalysisResponse, GeneratedSection } from "./types";

export default function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [activePage, setActivePage] = useState<"home" | "about">("home");

  // Studio Inputs
  const [ideology, setIdeology] = useState("");
  const [problem, setProblem] = useState("");
  const [approach, setApproach] = useState("");
  const [loading, setLoading] = useState(false);

  // Pipeline State
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [draftSections, setDraftSections] = useState<Record<string, string>>(
    {},
  );
  const [generatingSection, setGeneratingSection] = useState<string | null>(
    null,
  );

  const toggleTheme = () => {
    setDarkMode(!darkMode);
    document.documentElement.classList.toggle("dark");
  };

  const scrollToInput = () => {
    setActivePage("home");
    window.setTimeout(() => {
      document.getElementById("studio")?.scrollIntoView({ behavior: "smooth" });
    }, 0);
  };

  const showHome = () => {
    setActivePage("home");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const showAbout = () => {
    setActivePage("about");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await analyzeIdeology({
        raw_ideology: ideology,
        problem_statement: problem,
        proposed_approach: approach,
      });
      setAnalysis(data);
      window.scrollTo({ top: 300, behavior: "smooth" });
    } catch {
      alert("Analysis failed. Ensure FastAPI server is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateSection = async (sectionName: string) => {
    if (!analysis) return;
    setGeneratingSection(sectionName);
    try {
      const result: GeneratedSection = await generatePaperSection({
        section_name: sectionName,
        dna: analysis.dna,
        discovered_papers: analysis.discovered_papers,
        research_gaps: analysis.research_gaps,
      });
      setDraftSections((prev) => ({ ...prev, [sectionName]: result.content }));
    } catch {
      alert(`Failed to generate ${sectionName}`);
    } finally {
      setGeneratingSection(null);
    }
  };

  const handleExport = async (format: "latex" | "markdown") => {
    if (!analysis) return;
    const content = await exportPaper({
      title: analysis.dna.proposed_solution || "Research Contribution",
      authors: ["Kowshik"],
      sections: draftSections,
      references: analysis.discovered_papers,
      export_format: format,
    });

    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `paper.${format === "latex" ? "tex" : "md"}`;
    a.click();
  };

  return (
    <div
      className={`app-shell min-h-screen transition-colors duration-300 font-sans ${
        darkMode
          ? "bg-mesh-dark text-slate-100"
          : "bg-mesh-light text-slate-900"
      }`}
    >
      <Navbar
        darkMode={darkMode}
        toggleTheme={toggleTheme}
        onLaunchStudio={scrollToInput}
        activePage={activePage}
        onHome={showHome}
        onAbout={showAbout}
      />
      {activePage === "about" ? (
        <About onReturnHome={showHome} />
      ) : (
        <>
          <Hero onScrollToStudio={scrollToInput} />
          <RequirementStudio
            form={{
              raw_ideology: ideology,
              target_problem: problem,
              proposed_method: approach,
            }}
            loading={loading}
            onChange={(e) => {
              const setters = {
                raw_ideology: setIdeology,
                target_problem: setProblem,
                proposed_method: setApproach,
              };
              setters[e.target.name as keyof typeof setters](e.target.value);
            }}
            onSubmit={handleAnalyze}
          />
          {analysis && (
            <WorkspaceDashboard
              analysis={analysis}
              draftSections={draftSections}
              generatingSection={generatingSection}
              onGenerateSection={handleGenerateSection}
              onSectionChange={(sec, val) =>
                setDraftSections({ ...draftSections, [sec]: val })
              }
              onExport={handleExport}
            />
          )}
        </>
      )}
      <footer className="site-footer border-t border-slate-300 dark:border-slate-700">
        <div className="max-w-7xl mx-auto px-6 py-8 flex flex-col sm:flex-row justify-between gap-3 text-xs text-slate-600 dark:text-slate-400">
          <span className="font-medium text-slate-900 dark:text-slate-100">
            Resonance AI
          </span>
          <span>Research intelligence for clearer technical work.</span>
          <span className="font-mono">2026 / Research engineering</span>
        </div>
      </footer>
    </div>
  );
}
