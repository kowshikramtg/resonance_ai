export interface ResearchPaper {
  paper_id: string;
  title: string;
  authors: string[];
  year?: number;
  venue?: string;
  url?: string;
  citation_count?: number;
  abstract?: string;
}

export interface ResearchDNA {
  core_problem: string;
  proposed_solution: string;
  key_innovations: string[];
  domain_tags: string[];
  search_queries: string[];
}

export interface ResearchGap {
  gap_id: string;
  description: string;
  maturity: 'established' | 'partially_explored' | 'potential_gap' | 'requires_verification';
  existing_limitations: string[];
  supporting_paper_ids: string[];
}

export interface AnalysisResponse {
  dna: ResearchDNA;
  discovered_papers: ResearchPaper[];
  research_gaps: ResearchGap[];
  errors?: string[];
}

export interface GeneratedSection {
  section_title: string;
  content: string;
  placeholders?: string[];
}