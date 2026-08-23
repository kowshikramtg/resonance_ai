import json
from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from app.graph.state import ResearchGraphState
from app.schemas.research import ResearchDNA, ResearchGapItem, MaturityLevel
from app.services.scholar import ScholarlySearchService



llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2)
scholar_service = ScholarlySearchService()


async def extract_research_dna(state: ResearchGraphState) -> Dict[str, Any]:
    """Node 1: Parses raw ideology into structured Research DNA and generates search queries."""
    prompt = f"""
    You are a principal research engineer. Analyze the following project ideology and synthesize its Research DNA.
    
    Ideology: {state['raw_ideology']}
    Problem Statement: {state['problem_statement']}
    Proposed Approach: {state.get('proposed_approach', 'N/A')}
    
    Extract the core problem, proposed solution, key technical innovations, domain tags, 
    and 3 to 5 targeted academic search queries for fetching prior literature.
    """
    
    structured_llm = llm.with_structured_output(ResearchDNA)
    dna_result: ResearchDNA = await structured_llm.ainvoke(prompt)
    
    return {
        "dna": dna_result.model_dump(),      # model_dump()-> converts 'data model instance' to 'python dictionary'.
        "generated_queries": dna_result.search_queries,
    }


async def discover_literature(state: ResearchGraphState) -> Dict[str, Any]:
    """Node 2: Executes parallel scholarly searches using OpenAlex."""

    queries = state.get("generated_queries", [])
    all_papers: List[Dict[str, Any]] = []
    seen_ids = set()

    # Preserve user-uploaded context first from the user inputs
    for paper in state.get("user_provided_papers", []):
        p_dict = paper.model_dump()
        seen_ids.add(p_dict["paper_id"])
        all_papers.append(p_dict)

    # Fetch top results for each query (IMP to note)
    for query in queries:
        results = await scholar_service.search_openalex(query=query, limit=4)
        for res in results:
            p_dict = res.model_dump()
            if p_dict["paper_id"] not in seen_ids:
                seen_ids.add(p_dict["paper_id"])
                all_papers.append(p_dict)

    return {"discovered_papers": all_papers}


# function to check gaps and justify the novality
async def analyze_gaps_and_novelty(state: ResearchGraphState) -> Dict[str, Any]:

    """Node 3: Compares proposed DNA against retrieved papers to find explicit research gaps."""

    dna = state["dna"]
    papers = state["discovered_papers"]

    # Format retrieved context succinctly for prompt compression
    paper_context = "\n".join([
        f"- ID: {p['paper_id']} | Title: {p['title']} | Abstract: {(p.get('abstract') or '')[:300]}..."
        for p in papers[:15]
    ])

    prompt = f"""
    Compare the Proposed Idea against the Literature Context to identify research gaps.
    
    PROPOSED IDEA:
    Problem: {dna['core_problem']}
    Solution: {dna['proposed_solution']}
    Innovations: {', '.join(dna['key_innovations'])}
    
    LITERATURE CONTEXT:
    {paper_context}
    
    Categorize gaps strictly by maturity: 'established', 'partially_explored', 'potential_gap', or 'requires_verification'.
    Do NOT claim guaranteed novelty. Be evidence-first.
    """

    class GapAnalysisResponse(ResearchDNA):
        gaps: List[ResearchGapItem]

    structured_llm = llm.with_structured_output(GapAnalysisResponse)
    try:
        res = await structured_llm.ainvoke(prompt)
        return {"research_gaps": [g.model_dump() for g in res.gaps]}
    except Exception as e:
        return {"errors": [f"Gap analysis error: {str(e)}"]}