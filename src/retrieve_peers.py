"""Historical retrieval script for peer issuer releases; saves raw HTML and extracted tables.

Not part of src.reproduce. Running it overwrites config/peer_source_urls.json.
"""
import json
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

URLS = {
    "now_2026q2.html": "https://investor.servicenow.com/news/news-details/2026/ServiceNow-Reports-Second-Quarter-2026-Financial-Results/default.aspx",
    "now_2025fy.html": "https://investor.servicenow.com/news/news-details/2026/ServiceNow-Reports-Fourth-Quarter-and-Full-Year-2025-Financial-Results-Board-of-Directors-Authorizes-Additional-5B-for-Share-Repurchase-Program/default.aspx",
    "crm_2027q2.html": "https://investor.salesforce.com/news/news-details/2026/Salesforce-Delivers-Record-Second-Quarter-Fiscal-2027-Results/default.aspx",
    "crm_2026fy.html": "https://investor.salesforce.com/news/news-details/2026/Salesforce-Delivers-Record-Fourth-Quarter-Fiscal-2026-Results/default.aspx",
}


def table_text(content):
    """Flatten every HTML table to pipe-separated text rows."""
    soup = BeautifulSoup(content, "html.parser")
    tables = []
    for table in soup.find_all("table"):
        lines = []
        for tr in table.find_all("tr"):
            cells = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
            if cells:
                lines.append(" | ".join(cells))
        tables.append("\n".join(lines))
    return "\n\n".join(tables)


def main():
    """Download each release, saving raw HTML and table text, or print the error."""
    for name, url in URLS.items():
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            content = urllib.request.urlopen(request, timeout=30).read()
            Path("data/raw", name).write_bytes(content)
            Path("data/processed", name + ".tables.txt").write_text(table_text(content), encoding="utf8")
            print(name, len(content))
        except Exception as error:
            print(name, type(error).__name__, str(error))
    Path("config/peer_source_urls.json").write_text(json.dumps(URLS, indent=2))


if __name__ == "__main__":
    main()
