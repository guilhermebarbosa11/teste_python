import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("Variável OPENAI_API_KEY não definida!")

response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a joke teller."},
        {"role": "user",   "content": "Faça-me uma piada."}
    ],
    temperature=0.7,
    max_tokens=100
)

print(response.choices[0].message.content)