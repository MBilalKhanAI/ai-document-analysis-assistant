from typing import List, Dict, Any
from pathlib import Path
import json
from datetime import datetime

class DocumentSearch:
    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.index_file = storage_dir / "search_index.json"
        self._load_index()

    def _load_index(self):
        """Load the search index from disk."""
        if self.index_file.exists():
            with open(self.index_file, "r") as f:
                self.index = json.load(f)
        else:
            self.index = {}

    def _save_index(self):
        """Save the search index to disk."""
        with open(self.index_file, "w") as f:
            json.dump(self.index, f)

    def index_document(self, doc_id: str, content: str, metadata: Dict[str, Any]):
        """Index a document for search."""
        self.index[doc_id] = {
            "content": content,
            "metadata": metadata,
            "indexed_at": datetime.now().isoformat(),
        }
        self._save_index()

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for documents matching the query."""
        results = []
        query = query.lower()

        for doc_id, doc_data in self.index.items():
            content = doc_data["content"].lower()
            if query in content:
                results.append({
                    "doc_id": doc_id,
                    "content": doc_data["content"],
                    "metadata": doc_data["metadata"],
                    "indexed_at": doc_data["indexed_at"],
                })

        # Sort by relevance (simple implementation)
        results.sort(key=lambda x: x["content"].count(query), reverse=True)
        return results[:limit]

    def delete_document(self, doc_id: str):
        """Remove a document from the search index."""
        if doc_id in self.index:
            del self.index[doc_id]
            self._save_index() 