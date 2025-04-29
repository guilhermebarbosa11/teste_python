
import os
import json
import requests
import feedparser
from openai import OpenAI

def get_latest_arxiv_papers(query: str, max_results: int = 5):
    """
    Busca os papers mais recentes no arXiv que contenham 'query' em título/abstract.
    Retorna uma lista de dicionários com id, título, autores, resumo e data.
    """
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
            "title": entry.title,
            "authors": [a.name for a in entry.authors],
            "summary": entry.summary,
            "published": entry.published
        })
    return papers

def main():
    # 1) Chave de API
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Defina a variável OPENAI_API_KEY antes de executar.")
    client = OpenAI(api_key=api_key)

    # 2) Schema da função que o modelo pode chamar
    functions = [
        {
            "name": "get_latest_arxiv_papers",
            "description": "Retorna os papers mais recentes na arXiv para um tópico dado",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Termo a buscar nos papers (título/abstract)"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Número máximo de resultados"
                    }
                },
                "required": ["query"]
            }
        }
    ]

    # 3) Mensagem inicial pedindo ao agente os últimos papers
    user_request = "Me mostre os 5 papers mais recentes na arXiv sobre agentes autônomos."
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um assistente que busca papers na arXiv."},
            {"role": "user",   "content": user_request}
        ],
        functions=functions,
        function_call={"name": "get_latest_arxiv_papers"}  # força a chamada
    )

    # 4) Se o modelo pediu a função, executa e devolve os dados
    msg = resp.choices[0].message
    if msg.function_call:
        args = json.loads(msg.function_call.arguments)
        papers = get_latest_arxiv_papers(args["query"], args.get("max_results", 5))

        # 5) Envia os resultados de volta para o agente finalizar a resposta
        follow_up = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um assistente que busca papers na arXiv."},
                {"role": "assistant", "content": None, "function_call": msg.function_call.to_dict()},
                {"role": "function", "name": "get_latest_arxiv_papers", "content": json.dumps(papers)}
            ]
        )

        print(follow_up.choices[0].message.content)

    else:
        print("O agente não solicitou a função de busca.")

if __name__ == "__main__":
    main()
