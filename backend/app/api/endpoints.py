from http.client import HTTPException
from app.schemas.paper_gen import GenerateSectionRequest, PaperExportRequest
from app.services.paper_engine import generate_paper_section, format_to_latex
from fastapi.responses import PlainTextResponse

@router.post("/paper/generate-section")
async def generate_section(payload: GenerateSectionRequest):
    try:
        section = await generate_paper_section(
            section_name=payload.section_name,
            dna=payload.dna,
            papers=payload.discovered_papers,
            gaps=payload.research_gaps,
            custom_instructions=payload.custom_instructions or ""
        )
        return section
    except Exception as e:
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