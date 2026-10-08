from typing import List, Dict
from .base import BaseConnector
from ..data.mock_docs import GITHUB_DOCS


class GitHubConnector(BaseConnector):
    """
    GitHub connector.

    Prod swap-in: use PyGithub against the bank's GHE endpoint. Iterate the
    target orgs, pull README.md and docs/ folders, and use the commit
    timestamp of the last change to the file as updated_at.
    """

    source_name = "github"

    def fetch(self) -> List[Dict]:
        return [self.normalize(d) for d in GITHUB_DOCS]
