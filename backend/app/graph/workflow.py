from langgraph.graph import StateGraph, END
from app.graph.state import ResearchGraphState
from app.graph.nodes import (
    extract_research_dna,
    discover_literature,
    analyze_gaps_and_novelty,
)

# this defines executable pipeline graph with all nodes

def build_research_graph() -> StateGraph:
    workflow = StateGraph(ResearchGraphState)

    # Add Nodes
    workflow.add_node("extract_dna", extract_research_dna)
    workflow.add_node("discover_literature", discover_literature)
    workflow.add_node("analyze_gaps", analyze_gaps_and_novelty)

    # Define Edges / Execution Flow
    workflow.set_entry_point("extract_dna")
    workflow.add_edge("extract_dna", "discover_literature")
    workflow.add_edge("discover_literature", "analyze_gaps")
    workflow.add_edge("analyze_gaps", END)

    return workflow.compile()

research_pipeline = build_research_graph()