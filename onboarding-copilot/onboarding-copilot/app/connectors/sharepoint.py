from typing import List, Dict
from .base import BaseConnector
from ..data.mock_docs import SHAREPOINT_DOCS


class SharePointConnector(BaseConnector):
    """
    SharePoint connector.

    Prod swap-in: use the Microsoft Graph SDK. Walk each configured site,
    list drive items, download .docx/.pdf/.aspx, extract text with textract
    or Azure Document Intelligence, and use LastModifiedDateTime as
    updated_at.
    """

    source_name = "sharepoint"

    def fetch(self) -> List[Dict]:
        return [self.normalize(d) for d in SHAREPOINT_DOCS]
