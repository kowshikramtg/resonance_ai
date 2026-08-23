from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl

class MaturityLevel(str, Enum):
    ESTABLISHED = "established"
    PARTIALLY_EXPLORED = "partially_explored"
    POTENTIAL_GAP = "potential_gap"
    REQUIRED_VERIFICATION = "required_verification"

class ResearchPaperMetadata(BaseModel):
    paper_id: str = Field(..., description="DOI, Semantic Scholar ID, or OpenAlex ID")
    title: str
    authors: List[str]
    year: Optional[int] = None
    venue: Optional[str] = None
    url : Optional[HttpUrl] = None
    citation_count: Optional[int] = None
    abstract: Optional[str] = None
    is_user_uploaded: bool = False

class ResearchDNA(BaseModel):
    core_problem: str
    proposed_solution: str
    key_innovations: List[str]
    domain_tags: List[str]
    search_queries: List[str]

class ResearchGapItem(BaseModel):
    gap_id: str
    description: str
    maturity: MaturityLevel
    existing_limitations: List[str]
    supporting_paper_ids: List[str]

class EvidenceMapping(BaseModel):
    feature_name: str
    existing_research_ids: List[str]
    solved_aspects: str
    weak_aspects: str
    proposed_improvement: str

class SectionClaim(BaseModel):
    claim_text: str
    citation_paper_ids: List[str]
    is_supported: bool = True

class PaperSection(BaseModel):
    section_title: str
    content: str
    claims: List[SectionClaim]
    placeholders: Optional[List[str]] = Field(
        default_factory=list, 
        description="Explicit placeholders for missing empirical evidence"
    )

class ResearchDraft(BaseModel):
    title: str
    abstract: PaperSection
    introduction: PaperSection
    related_work: PaperSection
    research_gap: PaperSection
    methodology: PaperSection
    architecture: PaperSection
    experimental_setup: Optional[PaperSection] = None
    references: Dict[str, ResearchPaperMetadata] 