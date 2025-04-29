
import os
import json
import requests
import feedparser
from agents import Agent, Runner, function_tool

@function_tool
def get_latest_arxiv_papers(query: str, max_results: int = 5) -> str:

    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": max_results
    }
    r = requests.get(base_url, params=params)
    feed = feedparser.parse(r.text)

    papers = []
    for entry in feed.entries:
        papers.append({
            "id": entry.id,
            "title": entry.title.strip(),
            "authors": [a.name for a in entry.authors],
            "summary": entry.summary.strip(),
            "published": entry.published
        })

    return json.dumps(papers, ensure_ascii=False, indent=2)

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Defina a variável OPENAI_API_KEY antes de executar.")
    
    agent = Agent(
        name="ArXiv Agent",
        instructions=(
            "Você é um agente especializado em buscar e resumir os papers mais recentes "
            "no arXiv sobre um tópico dado. Quando o usuário pedir, utilize a função "
            "`get_latest_arxiv_papers` para recuperar os dados e depois apresente um "
            "resumo amigável em português."
        ),
        tools=[get_latest_arxiv_papers]
    )

    user_input = "Me mostre os 5 papers mais recentes na arXiv sobre agentes autônomos."
    result = Runner.run_sync(agent, input=user_input)

    print(result.final_output)

if __name__ == "__main__":
    main()
