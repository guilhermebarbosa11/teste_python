import os
import json
import openai

def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("Defina a variável OPENAI_API_KEY antes de executar.")

    file_path = "input.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )

    embedding = response['data'][0]['embedding']
    with open("embedding.json", "w", encoding="utf-8") as f:
        json.dump({"embedding": embedding}, f, ensure_ascii=False, indent=2)

    print("Embedding salvo em embedding.json")

if __name__ == "__main__":
    main()