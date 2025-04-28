import os
from openai import OpenAI

def main():
    # Carrega a chave da variável de ambiente
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Defina a variável OPENAI_API_KEY antes de executar.")

    # Inicializa o cliente
    client = OpenAI(api_key=api_key)

    # Lê o prompt do usuário
    prompt = input("Digite o prompt para geração de imagem: ")

    # Chamada à nova API de geração de imagens
    response = client.images.generate(
        model="gpt-image-1",     # ou "dall-e-3", conforme disponíveis na sua conta
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    # Extrai e exibe a URL
    url = response.data[0].url
    print("URL da imagem gerada:", url)

if __name__ == "__main__":
    main()
