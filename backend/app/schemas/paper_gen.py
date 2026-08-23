from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class GenerateSectionRequest(BaseModel):
    section_name: str  # e.g., "abstract", "introduction", "related_work", "methodology"
    dna: Dict[str, Any]
    discovered_papers: List[Dict[str, Any]]
    research_gaps: List[Dict[str, Any]]
    custom_instructions: Optional[str] = ""

class PaperExportRequest(BaseModel):
    title: str
    authors: List[str]
    sections: Dict[str, str]  # {"abstract": "...", "methodology": "..."}
    references: List[Dict[str, Any]]
    export_format: str  # "latex", "markdown", "json"