from typing import List, Dict
from .base import BaseConnector
from ..data.mock_docs import CONFLUENCE_DOCS


class ConfluenceConnector(BaseConnector):
    """
    Confluence connector.

    Prod swap-in: use `atlassian-python-api` and hit /rest/api/content/search
    with cql='type=page and space in (HR, COMP, ENG, SRE, IT)'. Map the CQL
    response to the normalized doc shape via self.normalize().
    """

    source_name = "confluence"

    def fetch(self) -> List[Dict]:
        return [self.normalize(d) for d in CONFLUENCE_DOCS]
