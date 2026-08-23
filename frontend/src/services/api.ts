import axios from 'axios';
import type {
  AnalysisResponse,
  GeneratedSection,
  ResearchDNA,
  ResearchGap,
  ResearchPaper,
} from '../types';

const API_BASE = 'http://localhost:8000/api/research';

export const analyzeIdeology = async (payload: {
  raw_ideology: string;
  problem_statement: string;
  proposed_approach?: string;
}): Promise<AnalysisResponse> => {
  const res = await axios.post(`${API_BASE}/analyze`, payload);
  return res.data;
};

export const generatePaperSection = async (payload: {
  section_name: string;
  dna: ResearchDNA;
  discovered_papers: ResearchPaper[];
  research_gaps: ResearchGap[];
  custom_instructions?: string;
}): Promise<GeneratedSection> => {
  const res = await axios.post(`${API_BASE}/paper/generate-section`, payload);
  return res.data;
};

export const exportPaper = async (payload: {
  title: string;
  authors: string[];
  sections: Record<string, string>;
  references: ResearchPaper[];
  export_format: 'latex' | 'markdown';
}): Promise<string> => {
  const res = await axios.post(`${API_BASE}/paper/export`, payload, {
    responseType: 'text',
  });
  return res.data;
};