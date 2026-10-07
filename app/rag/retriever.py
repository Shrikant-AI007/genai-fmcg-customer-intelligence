from pathlib import Path
import re
from typing import List, Dict

class SimpleRetriever:
    """Lightweight lexical retriever used as a reliable local fallback."""
    def __init__(self, document_dir="data/sample_documents"):
        self.docs = []
        for p in Path(document_dir).glob("*.md"):
            text = p.read_text(encoding="utf-8")
            self.docs.append({"source": p.name, "text": text, "tokens": set(re.findall(r"[a-z0-9]+", text.lower()))})

    def search(self, query: str, k: int = 3) -> List[Dict]:
        q = set(re.findall(r"[a-z0-9]+", query.lower()))
        scored = []
        for d in self.docs:
            overlap = len(q & d["tokens"])
            scored.append((overlap, d))
        return [d for score,d in sorted(scored, key=lambda x: x[0], reverse=True)[:k] if score > 0]
