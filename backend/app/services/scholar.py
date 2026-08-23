import httpx
from typing import List
from app.schemas.research import ResearchPaperMetadata

OPENALEX_BASE = "https://api.openalex.org/works"

async def fetch_real_papers(queries: List[str], max_results: int = 6) -> List[ResearchPaperMetadata]:
    papers = []
    seen_ids = set()

    async with httpx.AsyncClient(timeout=12.0) as client:
        for query in queries:
            if len(papers) >= max_results:
                break
            
            clean_q = query.replace("\n", " ").strip()
            if not clean_q:
                continue

            params = {
                "search": clean_q,
                "per_page": 4,
                "sort": "cited_by_count:desc"
            }
            
            try:
                res = await client.get(OPENALEX_BASE, params=params)
                if res.status_code == 200:
                    data = res.json()
                    for item in data.get("results", []):
                        if not item or not isinstance(item, dict):
                            continue

                        paper_id = str(item.get("id", "")).replace("https://openalex.org/", "")
                        if not paper_id or paper_id in seen_ids:
                            continue

                        # Null-safe author extraction
                        authorships = item.get("authorships") or []
                        authors = []
                        for a in authorships[:3]:
                            if isinstance(a, dict):
                                author_obj = a.get("author") or {}
                                name = author_obj.get("display_name") if isinstance(author_obj, dict) else None
                                if name:
                                    authors.append(name)
                        
                        # Abstract reconstruction
                        abstract_text = ""
                        inv_index = item.get("abstract_inverted_index")
                        if isinstance(inv_index, dict):
                            word_positions = []
                            for word, positions in inv_index.items():
                                if isinstance(positions, list):
                                    for pos in positions:
                                        word_positions.append((pos, word))
                            word_positions.sort(key=lambda x: x[0])
                            abstract_text = " ".join([wp[1] for wp in word_positions])[:350] + "..."

                        # Null-safe venue extraction
                        primary_loc = item.get("primary_location") or {}
                        source = primary_loc.get("source") if isinstance(primary_loc, dict) else {}
                        venue_name = source.get("display_name") if isinstance(source, dict) else "Academic Source"

                        raw_url = item.get("doi") or item.get("id")
                        
                        paper = ResearchPaperMetadata(
                            paper_id=paper_id,
                            title=item.get("title") or "Untitled Paper",
                            authors=authors if authors else ["Unknown Author"],
                            year=item.get("publication_year"),
                            venue=str(venue_name or "Academic Source"),
                            url=raw_url if (raw_url and str(raw_url).startswith("http")) else None,
                            citation_count=item.get("cited_by_count", 0),
                            abstract=abstract_text if abstract_text else "Abstract unavailable.",
                            is_user_uploaded=False
                        )
                        
                        seen_ids.add(paper_id)
                        papers.append(paper)
            except Exception as e:
                print(f"[OpenAlex Search Error]: {e}")
                
    return papers