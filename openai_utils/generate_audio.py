import os
import openai

def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("Defina a variável OPENAI_API_KEY antes de executar.")

    text = input("Digite o texto para síntese de fala: ")
    response = openai.Audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )

    audio_data = response['data']
    with open("output.mp3", "wb") as f:
        f.write(audio_data)

    print("Áudio salvo em output.mp3")

if __name__ == "__main__":
    main()