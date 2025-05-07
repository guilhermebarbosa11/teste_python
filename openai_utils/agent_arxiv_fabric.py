
import os
import json
import requests
import feedparser
from dotenv import load_dotenv

load_dotenv()
FABRIC_API_KEY = os.getenv("FABRIC_API_KEY")
FABRIC_CHAT_URL = os.getenv(
    "FABRIC_CHAT_URL",
    "https://api.researchmagic.com/fabric/v1/chat/completions"
)

if not FABRIC_API_KEY:
    raise ValueError("Defina FABRIC_API_KEY no seu .env")

HEADERS = {
    "Authorization": f"Bearer {FABRIC_API_KEY}",
    "Content-Type":  "application/json"
}

def get_latest_arxiv_papers(query: str, max_results: int = 5) -> dict:
    """
    Busca os papers mais recentes no arXiv que contenham 'query' em título/abstract.
    Retorna um dict serializável (JSON-ready).
    """
    resp = requests.get(
        "http://export.arxiv.org/api/query",
        params={
            "search_query": f"all:{query}",
            "sortBy":       "submittedDate",
            "sortOrder":    "descending",
            "max_results":  max_results
        }
    )
    feed = feedparser.parse(resp.text)
    papers = []
    for e in feed.entries:
        papers.append({
            "id":        e.id,
            "title":     e.title.strip(),
            "authors":   [a.name for a in e.authors],
            "summary":   e.summary.strip(),
            "published": e.published
        })
    return {"papers": papers}

FUNCTIONS = [
    {
        "name":        "get_latest_arxiv_papers",
        "description": "Recupera os artigos mais recentes do arXiv para um determinado tópico.",
        "parameters": {
            "type":       "object",
            "properties": {
                "query": {
                    "type":        "string",
                    "description": "Termo a ser buscado no título/abstract dos papers."
                },
                "max_results": {
                    "type":        "integer",
                    "description": "Número máximo de resultados a retornar."
                }
            },
            "required": ["query"]
        }
    }
]

def fabric_chat(messages: list, functions: list = None) -> dict:
    payload = {"messages": messages}
    if functions is not None:
        payload["functions"] = functions
        payload["function_call"] = {"mode": "auto"}  
    r = requests.post(FABRIC_CHAT_URL, headers=HEADERS, json=payload)
    r.raise_for_status()
    return r.json()

def main():
    messages = [
        {"role": "system",  "content": "Você é um agente especialista em buscar papers no arXiv."},
        {"role": "user",    "content": "Me mostre os 5 papers mais recentes na arXiv sobre agentes autônomos."}
    ]

    response = fabric_chat(messages, functions=FUNCTIONS)
    choice  = response["choices"][0]["message"]

    if choice.get("function_call"):
        fn_name = choice["function_call"]["name"]
        fn_args = json.loads(choice["function_call"]["arguments"])

        result = get_latest_arxiv_papers(**fn_args)

        messages.append(choice)
        messages.append({
            "role":    "function",
            "name":    fn_name,
            "content": json.dumps(result)
        })

        final = fabric_chat(messages) 
        print("\n=== Resposta Final do Agente ===\n")
        print(final["choices"][0]["message"]["content"])

    else:
        print("Saída direta:", choice.get("content"))

if __name__ == "__main__":
    main()
