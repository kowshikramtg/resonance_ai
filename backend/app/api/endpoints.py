from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from typing import Optional

from app.schemas.paper_gen import GenerateSectionRequest, PaperExportRequest
from app.services.paper_engine import generate_paper_section, format_to_latex
from app.services.research_engine import analyze_research_inputs

router = APIRouter()

class AnalyzeRequestPayload(BaseModel):
    raw_ideology: Optional[str] = ""
    target_problem: Optional[str] = Field(default="", alias="problem_statement")
    proposed_method: Optional[str] = Field(default="", alias="proposed_approach")

    class Config:
        populate_by_name = True

@router.post("/research/analyze")
async def analyze_research(payload: AnalyzeRequestPayload):
    try:
        result = await analyze_research_inputs(
            raw_ideology=payload.raw_ideology or "",
            target_problem=payload.target_problem or "",
            proposed_method=payload.proposed_method or ""
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/paper/generate-section")
async def generate_section(payload: GenerateSectionRequest):
    try:
        # Convert Pydantic models to dicts if needed
        papers_dict = [p if isinstance(p, dict) else p.model_dump(mode="json") for p in payload.discovered_papers]
        gaps_dict = [g if isinstance(g, dict) else g.model_dump(mode="json") for g in payload.research_gaps]

        section = await generate_paper_section(
            section_name=payload.section_name,
            dna=payload.dna,
            papers=papers_dict,
            gaps=gaps_dict,
            custom_instructions=payload.custom_instructions or ""
        )
        return section
    except Exception as e:
        print(f"[Endpoint Error /paper/generate-section]: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    
@router.post("/paper/export")
async def export_paper(payload: PaperExportRequest):
    if payload.export_format == "latex":
        content = format_to_latex(
            title=payload.title,
            authors=payload.authors,
            sections=payload.sections,
            references=payload.references
        )
        return PlainTextResponse(content, media_type="text/x-tex")
    
    elif payload.export_format == "markdown":
        md = [f"# {payload.title}\n", f"**Authors:** {', '.join(payload.authors)}\n\n---\n"]
        for sec, text in payload.sections.items():
            md.append(f"## {sec.replace('_', ' ').title()}\n{text}\n")
        return PlainTextResponse("\n".join(md), media_type="text/markdown")
    
    else:
        raise HTTPException(status_code=400, detail="Unsupported export format")