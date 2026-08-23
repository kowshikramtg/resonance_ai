from typing import List, Dict, Any, TypedDict, Annotated
import operator
from app.schemas.research import (
    ResearchDNA,
    ResearchPaperMetadata,
    ResearchGapItem,
    EvidenceMapping,
)

class ResearchGraphState(TypedDict):
    # Inputs
    raw_ideology: str
    problem_statement: str
    proposed_approach: str
    user_provided_papers: List[ResearchPaperMetadata]

    # Pipeline Extracted Data
    dna: Dict[str, Any]
    generated_queries: List[str]

    
    discovered_papers: Annotated[List[Dict[str, Any]], operator.add]
    
    # Outputs
    research_gaps: List[Dict[str, Any]]
    evidence_mappings: List[Dict[str, Any]]
    
    errors: List[str]