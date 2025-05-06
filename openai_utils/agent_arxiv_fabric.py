
import os
import json
import requests
import feedparser
from dotenv import load_dotenv

load_dotenv()  

FABRIC_API_URL = os.getenv(
    "FABRIC_API_URL",
    "https://api.researchmagic.com/fabric/v1/jobs"  # ajuste se for outra URL
)
FABRIC_API_KEY = os.getenv("FABRIC_API_KEY")
if not FABRIC_API_KEY:
    raise ValueError("Defina FABRIC_API_KEY no seu arquivo .env")

def get_latest_arxiv_papers(query: str, max_results: int = 5):
    """
    Busca os papers mais recentes na arXiv que contenham 'query' em título/abstract.
    """
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "sortBy":       "submittedDate",
        "sortOrder":    "descending",
        "max_results":  max_results
    }
    resp = requests.get(base_url, params=params)
    feed = feedparser.parse(resp.text)
    papers = []
    for entry in feed.entries:
        papers.append({
            "id":        entry.id,
            "title":     entry.title.strip(),
            "authors":   [a.name for a in entry.authors],
            "summary":   entry.summary.strip(),
            "published": entry.published
        })
    return papers

def call_fabric(prompt: str, model: str = "wizard-ai", modules: list = None) -> dict:
    """
    Envia um 'job' ao Fabric Hypergrid para processar o prompt
    e retorna o resultado JSON.
    """
    payload = {
        "model":   model,
        "prompt":  prompt,
        "modules": modules or []
    }
    headers = {
        "Authorization": f"Bearer {FABRIC_API_KEY}",
        "Content-Type":  "application/json"
    }
    r = requests.post(FABRIC_API_URL, headers=headers, json=payload)
    r.raise_for_status()
    return r.json()

def main():
    query = "autonomous agents"
    papers = get_latest_arxiv_papers(query, max_results=5)

    prompt = (
        "Aqui estão os 5 papers mais recentes da arXiv sobre agentes autônomos:\n"
        f"{json.dumps(papers, indent=2, ensure_ascii=False)}\n\n"
        "Por favor, forneça um resumo breve de cada paper em português."
    )

    result = call_fabric(prompt)

    print("\n=== Resumos dos Papers ===\n")
    print(result.get("output", json.dumps(result, indent=2, ensure_ascii=False)))

if __name__ == "__main__":
    main()
