import os
from openai import OpenAI

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Defina a variável OPENAI_API_KEY antes de executar.")

    client = OpenAI(api_key=api_key)

    prompt = input("Digite o prompt para geração de imagem: ")

    response = client.images.generate(
        model="gpt-image-1",     
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    url = response.data[0].url
    print("URL da imagem gerada:", url)

if __name__ == "__main__":
    main()
