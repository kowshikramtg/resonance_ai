import React from "react";
import { Sun, Moon } from "lucide-react";

interface NavbarProps {
  darkMode: boolean;
  toggleTheme: () => void;
  onLaunchStudio: () => void;
  activePage: "home" | "about";
  onHome: () => void;
  onAbout: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  darkMode,
  toggleTheme,
  onLaunchStudio,
  activePage,
  onHome,
  onAbout,
}) => {
  return (
    <nav className="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center border-b border-slate-300/70 dark:border-slate-700/70">
      <button
        onClick={onHome}
        className="flex items-center gap-2"
        aria-label="Resonance AI home"
      >
        <div className="w-9 h-9 rounded-sm bg-[#17202a] dark:bg-[#f3f5f8] text-[#f7f5ef] dark:text-[#17202a] flex items-center justify-center font-serif italic text-lg">
          R
        </div>
        <span className="font-bold text-sm tracking-tight text-[#17202a] dark:text-[#f3f5f8]">
          Resonance{" "}
          <span className="text-[#315c91] dark:text-[#92b8e2]">AI</span>
        </span>
      </button>

      <div className="absolute left-1/2 -translate-x-1/2 hidden sm:flex items-center gap-7 text-xs font-medium text-slate-600 dark:text-slate-300">
        <button
          onClick={onHome}
          className={
            activePage === "home"
              ? "text-slate-950 dark:text-white"
              : "hover:text-[#315c91] dark:hover:text-[#9dbce0]"
          }
        >
          Research brief
        </button>
        <button
          onClick={onAbout}
          className={
            activePage === "about"
              ? "text-slate-950 dark:text-white"
              : "hover:text-[#315c91] dark:hover:text-[#9dbce0]"
          }
        >
          About
        </button>
      </div>

      <div className="flex items-center gap-4">
        <button
          onClick={toggleTheme}
          aria-label={darkMode ? "Switch to light mode" : "Switch to dark mode"}
          className="p-2 rounded-sm border border-slate-300 dark:border-slate-600 bg-white/70 dark:bg-slate-800/70 hover:bg-white dark:hover:bg-slate-700 transition"
        >
          {darkMode ? (
            <Sun className="w-4 h-4 text-amber-400" />
          ) : (
            <Moon className="w-4 h-4 text-slate-600" />
          )}
        </button>
        <button
          onClick={onLaunchStudio}
          className="px-4 py-2.5 text-xs font-bold bg-[#315c91] text-white rounded-sm hover:bg-[#264b79] transition shadow-sm"
        >
          Launch Studio
        </button>
      </div>
    </nav>
  );
};
