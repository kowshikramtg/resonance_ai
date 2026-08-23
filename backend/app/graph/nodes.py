import os
import asyncio
import warnings
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from app.graph.state import ResearchGraphState
from app.schemas.research import ResearchDNA, ResearchGapItem
from app.services.scholar import ScholarlySearchService

warnings.filterwarnings("ignore")
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

# Primary & Fallback LLMs
primary_llm = ChatGoogleGenerativeAI(
    model="gemini-3.7-flash", 
    google_api_key=api_key, 
    temperature=0.2
)

fallback_llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash", 
    google_api_key=api_key, 
    temperature=0.2
)

scholar_service = ScholarlySearchService()


async def invoke_with_retry(schema_class, prompt: str, max_retries: int = 3):
    """Executes structured LLM calls with retry logic and fallback model handling."""
    for attempt in range(max_retries):
        try:
            model = primary_llm if attempt < 2 else fallback_llm
            structured_llm = model.with_structured_output(schema_class, method="json_schema")
            return await structured_llm.ainvoke(prompt)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            await asyncio.sleep(2 ** attempt)  # Exponential backoff (1s, 2s)


async def extract_research_dna(state: ResearchGraphState):
    prompt = f"""
    You are a principal research engineer. Analyze the project ideology and synthesize its Research DNA.
    
    Ideology: {state['raw_ideology']}
    Problem Statement: {state['problem_statement']}
    Proposed Approach: {state.get('proposed_approach', 'N/A')}
    
    Extract core problem, proposed solution, key innovations, domain tags, 
    and 3 targeted academic search queries for fetching prior literature.
    """
    
    dna_result: ResearchDNA = await invoke_with_retry(ResearchDNA, prompt)
    
    return {
        "dna": dna_result.model_dump(),
        "generated_queries": dna_result.search_queries,
    }


async def discover_literature(state: ResearchGraphState):
    queries = state.get("generated_queries", [])
    all_papers = []
    seen_ids = set()

    for paper in state.get("user_provided_papers", []):
        p_dict = paper.model_dump()
        seen_ids.add(p_dict["paper_id"])
        all_papers.append(p_dict)

    for query in queries[:2]:
        results = await scholar_service.search_openalex(query=query, limit=3)
        for res in results:
            p_dict = res.model_dump()
            if p_dict["paper_id"] not in seen_ids:
                seen_ids.add(p_dict["paper_id"])
                all_papers.append(p_dict)

    return {"discovered_papers": all_papers}


async def analyze_gaps_and_novelty(state: ResearchGraphState):
    dna = state["dna"]
    papers = state["discovered_papers"]

    paper_context = "\n".join([
        f"- ID: {p['paper_id']} | Title: {p['title']} | Abstract: {(p.get('abstract') or '')[:250]}..."
        for p in papers[:5]
    ])

    prompt = f"""
    Compare the Proposed Idea against Literature Context to identify research gaps.
    
    PROPOSED IDEA:
    Problem: {dna['core_problem']}
    Solution: {dna['proposed_solution']}
    
    LITERATURE CONTEXT:
    {paper_context}
    
    Categorize gaps strictly by maturity: 'established', 'partially_explored', 'potential_gap', or 'requires_verification'.
    Do NOT claim guaranteed novelty.
    """

    class GapResponse(ResearchDNA):
        gaps: list[ResearchGapItem]

    try:
        res = await invoke_with_retry(GapResponse, prompt)
        return {"research_gaps": [g.model_dump() for g in res.gaps]}
    except Exception as e:
        return {"errors": [f"Gap analysis error: {str(e)}"]}