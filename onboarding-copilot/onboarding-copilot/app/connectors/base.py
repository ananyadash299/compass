from abc import ABC, abstractmethod
from typing import List, Dict


class BaseConnector(ABC):
    """
    Contract every source connector must implement.

    Real Confluence/GitHub/SharePoint clients would hit their respective APIs
    here. In this prototype, connectors return pre-seeded banking mock docs
    so the demo is deterministic and doesn't require credentials.
    """

    source_name: str = "unknown"

    @abstractmethod
    def fetch(self) -> List[Dict]:
        """Return a list of normalized docs from this source."""
        raise NotImplementedError

    def normalize(self, raw: Dict) -> Dict:
        return {
            "id": raw["id"],
            "source": self.source_name,
            "title": raw["title"],
            "url": raw["url"],
            "author": raw["author"],
            "updated_at": raw["updated_at"],
            "tags": raw.get("tags", []),
            "body": raw["body"],
        }
