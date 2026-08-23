import os
import json
import re
from typing import Dict, List, Any
from google import genai
from google.genai import types

def clean_json_text(raw_text: str) -> str:
    cleaned = re.sub(r"```(?:json)?", "", raw_text, flags=re.IGNORECASE).strip()
    return cleaned.strip("`").strip()


async def generate_paper_section(
    section_name: str,
    dna: Dict[str, Any],
    papers: List[Dict[str, Any]],
    gaps: List[Dict[str, Any]],
    custom_instructions: str = ""
) -> Dict[str, str]:
    print(f"🚀 [Manuscript Engine] Starting generation for section: '{section_name}'...")
    
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)

    paper_titles = [
        p.get("title", "") if isinstance(p, dict) else getattr(p, "title", "")
        for p in papers
    ]
    gap_descriptions = [
        g.get("description", "") if isinstance(g, dict) else getattr(g, "description", "")
        for g in gaps
    ]

    prompt = f"""
    You are an expert AI computer science research assistant drafting an academic paper section.

    Section to Draft: {section_name.upper()}
    Core Problem: {dna.get('core_problem', 'N/A')}
    Proposed Solution: {dna.get('proposed_solution', 'N/A')}
    Key Innovations: {', '.join(dna.get('key_innovations', []))}
    Related Literature Found: {', '.join(paper_titles[:5])}
    Target Research Gaps: {', '.join(gap_descriptions[:3])}
    Custom Instructions: {custom_instructions}

    Write a detailed, formal academic section (300-500 words).

    Return ONLY strict JSON matching:
    {{
        "section_name": "{section_name}",
        "content": "Full markdown text here..."
    }}
    """

    try:
        print(f"📡 [Gemini Call] Sending prompt for '{section_name}' to gemini-3.6-flash...")
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        cleaned_text = clean_json_text(response.text)
        data = json.loads(cleaned_text)
        print(f"✅ [Manuscript Engine] Completed drafting '{section_name}'.")
        
        return {
            "section_name": section_name,
            "content": data.get("content", f"Draft content for {section_name}.")
        }
    except Exception as e:
        print(f"❌ [Paper Generation Error - {section_name}]: {e}")
        sec_title = section_name.replace("_", " ").title()
        return {
            "section_name": section_name,
            "content": f"## {sec_title}\n\nDraft generated for **{dna.get('proposed_solution', 'the proposed framework')}** addressing {dna.get('core_problem', 'the core research problem')}."
        }


def format_to_latex(
    title: str,
    authors: List[str],
    sections: Dict[str, str],
    references: List[Dict[str, Any]]
) -> str:
    author_str = " \\and ".join(authors) if authors else "Author Name"
    latex_lines = [
        "\\documentclass{article}",
        "\\usepackage[utf8]{inputenc}",
        f"\\title{{{title}}}",
        f"\\author{{{author_str}}}",
        "\\date{\\today}",
        "\\begin{document}",
        "\\maketitle"
    ]
    for sec_key, content in sections.items():
        sec_heading = sec_key.replace("_", " ").title()
        latex_lines.append(f"\n\\section{{{sec_heading}}}")
        latex_lines.append(content.replace("**", "").replace("## ", ""))
    latex_lines.append("\n\\end{document}")
    return "\n".join(latex_lines)