from groq import Groq
from mistralai import Mistral
from dotenv import load_dotenv
from pathlib import Path
from io import BytesIO
from PIL import Image
import requests
import os
import json

load_dotenv()

def read_file(text_file_path):
    with open (text_file_path, "r") as file:
        return file.read()

def audio_to_text(audio_input, language='fr'):
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    if isinstance(audio_input, (str, Path)):
        with open(audio_input, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=file,
                model="whisper-large-v3-turbo",
                prompt="Extrait le texte de l'audio le plus précis possible",
                response_format="verbose_json",
                timestamp_granularities=["word", "segment"],
                language=language,
                temperature=0.0
            )
    else:
        # Cas 2 : on suppose que c’est un fichier-like object (UploadedFile)
        # On réinitialise le curseur au début si jamais le fichier a été lu partiellement
        audio_input.seek(0)
        transcription = client.audio.transcriptions.create(
            file=audio_input,
            model="whisper-large-v3-turbo",
            prompt="Extrait le texte de l'audio le plus précis possible",
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"],
            language=language,
            temperature=0.0
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
        return image
    else: 
        return r.raise_for_status()


# if __name__ == "__main__":
#     audio_path = "../Audio.m4a"
#     reve = audio_to_text(audio_path, language='fr')
#     analysis = reve_analysis(reve)
#     print(reve)
#     print("Voici l'analyse")
#     print(analysis)
#     image = ia_image(reve)