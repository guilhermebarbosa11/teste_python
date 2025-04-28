import os
import openai

def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("Defina a variável OPENAI_API_KEY antes de executar.")

    text = input("Digite o texto para gerar embedding: ")
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )

    embedding = response['data'][0]['embedding']
    print("Embedding gerado (vetor):", embedding)

if __name__ == "__main__":
    main()