# backend/test_nodes.py
# to test the LangGraph pipeline nodes and execution flow

import asyncio
import warnings
import json

# Suppress the SDK warning for clean output
warnings.filterwarnings("ignore", category=UserWarning)

from app.graph.workflow import research_pipeline

async def test_pipeline():
    print("🚀 Invoking Research Graph Pipeline...")
    
    test_input = {
        "raw_ideology": "Autonomous satellite safeguard system using machine learning to predict CME disruptions and adjust satellite orbit orientations dynamically.",
        "problem_statement": "Coronal Mass Ejections (CMEs) inflict massive geomagnetic disruptions on low-earth orbit satellites, leading to data loss and system degradation.",
        "proposed_approach": "Train a light-weight ML model on CACTus solar event datasets to trigger active orbital re-orientation maneuvers ahead of CME impact.",
        "user_provided_papers": [],
        "discovered_papers": [],
        "errors": []
    }

    result = await research_pipeline.ainvoke(test_input)
    
    print("\n==========================================")
    print(" 1. EXTRACTED RESEARCH DNA")
    print("==========================================")
    dna = result.get("dna", {})
    print(f"• Core Problem: {dna.get('core_problem')}")
    print(f"• Solution: {dna.get('proposed_solution')}")
    print(f"• Search Queries: {dna.get('search_queries')}")

    print("\n==========================================")
    print(" 2. DISCOVERED LITERATURE (OpenAlex API)")
    print("==========================================")
    papers = result.get("discovered_papers", [])
    if not papers:
        print("  (No papers returned)")
    for i, paper in enumerate(papers[:5], 1):
        print(f"{i}. [{paper.get('paper_id')}] {paper.get('title')}")
        print(f"   Year: {paper.get('year')} | Citations: {paper.get('citation_count')}")

    print("\n==========================================")
    print(" 3. GAP & NOVELTY ANALYSIS")
    print("==========================================")
    gaps = result.get("research_gaps", [])
    if not gaps:
        print("  (No gaps generated or error occurred)")
    for gap in gaps:
        print(f"• Gap ID: {gap.get('gap_id')}")
        print(f"  Maturity: {gap.get('maturity')}")
        print(f"  Description: {gap.get('description')}")

    if result.get("errors"):
        print("\n⚠️ Pipeline Errors:", result.get("errors"))

if __name__ == "__main__":
    asyncio.run(test_pipeline())