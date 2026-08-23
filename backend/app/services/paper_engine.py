import os
from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from app.schemas.research import PaperSection, SectionClaim

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-3.7-flash", google_api_key=api_key, temperature=0.2)

async def generate_paper_section(
    section_name: str,
    dna: Dict[str, Any],
    papers: List[Dict[str, Any]],
    gaps: List[Dict[str, Any]],
    custom_instructions: str = ""
) -> PaperSection:
    
    paper_context = "\n".join([
        f"- [{p['paper_id']}] Title: {p['title']} | Abstract: {(p.get('abstract') or '')[:200]}"
        for p in papers[:5]
    ])
    
    prompt = f"""
    You are an academic paper engineer writing the '{section_name.upper()}' section of a research paper.
    
    CORE RESEARCH DNA:
    Problem: {dna.get('core_problem')}
    Solution: {dna.get('proposed_solution')}
    Innovations: {dna.get('key_innovations')}
    
    LITERATURE CONTEXT:
    {paper_context}
    
    IDENTIFIED GAPS:
    {gaps}
    
    INSTRUCTIONS:
    - Write professional, dense academic prose appropriate for IEEE/ACM formats.
    - Attach paper IDs as citations (e.g., [https://openalex.org/W...]) when citing claims.
    - If empirical results, specific dataset metrics, or baselines are missing, DO NOT FABRICATE DATA. Instead, insert explicit placeholders like '[PLACEHOLDER: Empirical accuracy metric on dataset X]'.
    - Custom User Direction: {custom_instructions}
    """
    
    structured_llm = llm.with_structured_output(PaperSection, method="json_schema")
    return await structured_llm.ainvoke(prompt)


def format_to_latex(title: str, authors: List[str], sections: Dict[str, str], references: List[Dict[str, Any]]) -> str:
    """Exports structured paper dict into clean LaTeX document format."""
    author_str = " \\and ".join(authors) if authors else "Author Name"
    
    latex_doc = [
        "\\documentclass[10pt,journal,compsoc]{IEEEtran}",
        "\\usepackage{cite}",
        "\\usepackage{amsmath,amssymb,amsfonts}",
        "\\begin{document}",
        f"\\title{{{title}}}",
        f"\\author{{{author_str}}}",
        "\\maketitle",
    ]
    
    if "abstract" in sections:
        latex_doc.append(f"\\begin{{abstract}}\n{sections['abstract']}\n\\end{{abstract}}")
        
    for sec_name, content in sections.items():
        if sec_name.lower() == "abstract":
            continue
        formatted_title = sec_name.replace("_", " ").title()
        latex_doc.append(f"\\section{{{formatted_title}}}\n{content}\n")
        
    latex_doc.append("\\end{document}")
    return "\n".join(latex_doc)