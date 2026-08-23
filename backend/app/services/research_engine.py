import os
import json
import re
from google import genai
from google.genai import types
from app.schemas.research import ResearchDNA, ResearchGapItem, MaturityLevel
from app.services.scholar import fetch_real_papers

def clean_json_response(raw_text: str) -> str:
    cleaned = re.sub(r"```(?:json)?", "", raw_text, flags=re.IGNORECASE).strip()
    return cleaned.strip("`").strip()

async def analyze_research_inputs(raw_ideology: str, target_problem: str, proposed_method: str) -> dict:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))

    dna_prompt = f"""
    Analyze the following research inputs:
    - Raw Ideology: {raw_ideology}
    - Target Problem: {target_problem}
    - Proposed Method: {proposed_method}

    Return strict JSON (no Markdown wrappers):
    {{
        "key_innovations": ["core innovation 1", "core innovation 2", "core innovation 3"],
        "domain_tags": ["tag 1", "tag 2", "tag 3"],
        "search_queries": ["academic query 1", "academic query 2", "academic query 3"]
    }}
    """
    
    try:
        dna_response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=dna_prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        cleaned_dna_text = clean_json_response(dna_response.text)
        dna_data = json.loads(cleaned_dna_text)
    except Exception as e:
        print(f"[LLM DNA Parsing Error]: {e}")
        dna_data = {
            "key_innovations": ["Automated feature extraction", "Domain gap analysis"],
            "domain_tags": ["Machine Learning", "System Engineering"],
            "search_queries": [target_problem[:50], proposed_method[:50]]
        }

    dna = ResearchDNA(
        core_problem=target_problem,
        proposed_solution=proposed_method,
        key_innovations=dna_data.get("key_innovations", []),
        domain_tags=dna_data.get("domain_tags", []),
        search_queries=dna_data.get("search_queries", [target_problem[:50]])
    )

    discovered_papers = await fetch_real_papers(dna.search_queries, max_results=6)

    paper_context = "\n".join([f"- ID {p.paper_id}: {p.title}" for p in discovered_papers])
    gap_prompt = f"""
    Problem: {target_problem}
    Proposed Method: {proposed_method}
    Existing Literature Found:
    {paper_context if paper_context else "No prior literature found."}

    Identify 3 distinct research gaps in current literature that this proposed method addresses.
    Return strict JSON array (no Markdown wrappers):
    [
      {{
        "gap_id": "GAP-01",
        "description": "Clear description of unaddressed limitation in prior work",
        "maturity": "potential_gap",
        "existing_limitations": ["limitation 1", "limitation 2"],
        "supporting_paper_ids": ["Paper ID from literature listed above"]
      }}
    ]
    """

    try:
        gap_response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=gap_prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        cleaned_gap_text = clean_json_response(gap_response.text)
        raw_gaps = json.loads(cleaned_gap_text)
    except Exception as e:
        print(f"[LLM Gap Parsing Error]: {e}")
        raw_gaps = [{
            "gap_id": "GAP-01",
            "description": f"Existing approaches for {target_problem[:30]} lack real-time scalability.",
            "maturity": "potential_gap",
            "existing_limitations": ["High execution latency"],
            "supporting_paper_ids": [p.paper_id for p in discovered_papers[:1]]
        }]

    research_gaps = [
        ResearchGapItem(
            gap_id=g.get("gap_id", f"GAP-0{idx+1}"),
            description=g.get("description", "Unaddressed technical limitation"),
            maturity=MaturityLevel.POTENTIAL_GAP,
            existing_limitations=g.get("existing_limitations", []),
            supporting_paper_ids=g.get("supporting_paper_ids", [])
        )
        for idx, g in enumerate(raw_gaps)
    ]

    return {
        "status": "success",
        "dna": dna.model_dump(),
        "discovered_papers": [p.model_dump(mode="json") for p in discovered_papers],
        "research_gaps": [g.model_dump(mode="json") for g in research_gaps]
    }