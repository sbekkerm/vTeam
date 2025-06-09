# tools/mcp_jira.py
import os, requests
from llama_stack_client import MCPTool


class JiraFetcher(MCPTool):
    name = "jira_get_issue"
    description = "Fetch a Jira issue or feature by key"
    parameters = {"type": "object", "properties": {"key": {"type": "string"}}}

    def run(self, key: str) -> str:  # <- must return str/JSON-str
        url = f"{os.environ['JIRA_BASE']}/rest/api/3/issue/{key}"
        token = os.environ["JIRA_TOKEN"]
        r = requests.get(
            url,
            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        )
        r.raise_for_status()
        return r.text
