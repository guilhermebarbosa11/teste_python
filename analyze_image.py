import os
import openai

def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("Defina a variável OPENAI_API_KEY antes de executar.")

    image_path = "input.jpg"
    with open(image_path, "rb") as f:
        img_data = f.read()

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Descreva a imagem anexada."}],
        files=[{"name": "input.jpg", "data": img_data}]
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()