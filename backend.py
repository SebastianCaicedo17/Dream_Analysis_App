from groq import Groq
from mistralai import Mistral
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
import requests
import os
import json

load_dotenv()
filename = "Audio.m4a"

def read_file(text_file_path):
    with open (text_file_path, "r") as file:
        return file.read()

def audio_to_text(filename, language='fr'):
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    with open(filename, "rb") as file:

        transcription = client.audio.transcriptions.create(
            file=file, # Required audio file
            model="whisper-large-v3-turbo", # Required model to use for transcription
            prompt="Extrait le text de l'audio le plus précis possible",  # Optional
            response_format="verbose_json",  # Optional
            timestamp_granularities = ["word", "segment"], # Optional (must set response_format to "json" to use and can specify "word", "segment" (default), or both)
            language=language,  # Optional
            temperature=0.0  # Optional
        )
        return transcription.text


def reve_analysis(text):

    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

    chat_response = client.chat.complete(
		model="mistral-large-latest",
		messages=[
			{
			"role": "system",
			"content": read_file(text_file_path="context.txt")
			},
			{
			"role": "user",
			"content": f"Analyse le texte ci-dessous (ta réponse doit être dans le format JSON) : {text}",
			},
		],
		response_format={"type": "json_object",}
	)
    predictions = json.loads(chat_response.choices[0].message.content) 
    return predictions

def ia_image(text):
    r = requests.post('https://clipdrop-api.co/text-to-image/v1',
    files = {
        'prompt': (None, text, 'text/plain')
    },
    headers = { 'x-api-key': os.environ["CLIPDROP_API_KEY"]}
    )
    if (r.ok):
        # r.content contains the bytes of the returned image
        image = Image.open(BytesIO(r.content))
        image.save("image_generée.png")
    else: 
        return r.raise_for_status()


if __name__ == "__main__":
    filename = "../Audio.m4a"
    reve = audio_to_text(filename, language='fr')
    analysis = reve_analysis(reve)
    print(reve)
    print("Voici l'analyse")
    print(analysis)
    image = ia_image(reve)