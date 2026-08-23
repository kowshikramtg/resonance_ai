import httpx
from typing import List, Dict, Any, Optional
from app.schemas.research import ResearchPaperMetadata

class ScholarlySearchService:
    def __init__(self, mailto_email: str = "user@example.com"):
        self.headers = {"User-Agent": f"ResearchPlatform/1.0 (mailto:{mailto_email})"}
    
    async def search_openalex(self, query: str, limit: int = 5) -> List[ResearchPaperMetadata]:
        url = "https://api.openalex.org/works"
        params = {
            "search": query,
            "per-page": limit,
            "select": "id,title,publication_year,primary_location,authorships,cited_by_count,abstract_inverted_index"
        }
        async with httpx.AsyncClient() as client:
            try:
                res = await client.get(url, params=params, headers=self.headers, timeout=10.0)
                res.raise_for_status()
                data = res.json()
                results = []
                for item in data.get("results", []):
                    # Basic reconstruction of abstract from inverted index
                    abstract = self._reconstruct_abstract(item.get("abstract_inverted_index"))
                    
                    authors = [
                        auth.get("author", {}).get("display_name", "") 
                        for auth in item.get("authorships", [])
                    ]
                    
                    location = item.get("primary_location") or {}
                    landing_page = location.get("landing_page_url")
                    
                    results.append(
                        ResearchPaperMetadata(
                            paper_id=item.get("id"),
                            title=item.get("title", "Untitled"),
                            authors=[a for a in authors if a],
                            year=item.get("publication_year"),
                            venue=location.get("source", {}).get("display_name") if location.get("source") else None,
                            url=landing_page if landing_page else None,
                            citation_count=item.get("cited_by_count", 0),
                            abstract=abstract,
                            is_user_uploaded=False
                        )
                    )
                return results
            except Exception as e:
                print(f"Error fetching from OpenAlex: {e}")
                return []

    def _reconstruct_abstract(self, inverted_index: Optional[Dict[str, List[int]]]) -> Optional[str]:
        if not inverted_index:
            return None
        word_positions = []
        for word, positions in inverted_index.items():
            for pos in positions:
                word_positions.append((pos, word))
        word_positions.sort()
        return " ".join([w for _, w in word_positions])