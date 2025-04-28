import os
import openai

def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("Defina a variável OPENAI_API_KEY antes de executar.")

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",   "content": "Tell me a joke"}
        ],
        temperature=0.7,
        max_tokens=100
    )

    joke = response.choices[0].message.content.strip()
    print("\n💡 Aqui vai sua piada:\n")
    print(joke)

if __name__ == "__main__":
    main()