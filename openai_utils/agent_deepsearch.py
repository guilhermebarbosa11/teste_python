
import os
import json
from dotenv import load_dotenv

from exa_py import Exa

from agents import Agent, Runner, function_tool

load_dotenv()
EXA_API_KEY = os.getenv("EXA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not EXA_API_KEY:
    raise ValueError("Defina EXA_API_KEY no seu .env")
if not OPENAI_API_KEY:
    raise ValueError("Defina OPENAI_API_KEY no seu .env")

exa = Exa(api_key=EXA_API_KEY)

@function_tool
def deep_search(query: str, max_results: int = 5) -> str:

    resp = exa.search_and_contents(
        query,
        type="auto",      
        text=True,        
        num_results=max_results
    )

    items = []
    for entry in resp.results:
        items.append({
            "url":       entry.url,
            "title":     getattr(entry, "title", ""),
            "snippet":   entry.text[:300].replace("\n", " "),  # primeiros 300 chars
        })

    return json.dumps(items, ensure_ascii=False, indent=2)

def main():
    agent = Agent(
        name="Exa DeepSearch Agent",
        instructions=(
            "Você é um agente de pesquisa que usa Exa para fazer buscas profundas na web. "
            "Quando o usuário pedir algo, invoque a função `deep_search` para obter os resultados, "
            "e depois apresente um resumo amigável em português."
        ),
        tools=[deep_search],
        llm_api_key=OPENAI_API_KEY
    )

    query = input("O que você quer pesquisar na web? ")
    result = Runner.run_sync(agent, input=query)

    print("\n=== Resultados da pesquisa ===\n")
    print(result.final_output)

if __name__ == "__main__":
    main()
