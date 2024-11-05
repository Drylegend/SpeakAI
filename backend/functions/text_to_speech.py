import requests
import os
from dotenv import load_dotenv

load_dotenv()

ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")


#ElevenLabs
#Convert Text to Speech

def convert_text_speech(message):
    #Define data body
    body = {
        "text": message,
        "voice_settings":{
            "stability": 0,
            "similarity_boost": 0,
        }
    }
    #Define voice
    voice_hope = "tnSpp4vdxKPjI9w0GnoV"
    #you can use different voices

    #Constructing headers and endpoint

    headers = {"xi-api-key": ELEVEN_LABS_API_KEY, "content-type": "application/json", "accept": "audio/mpeg"}
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_hope}"

    #sedn request

    try:
        response = requests.post(endpoint, json=body, headers=headers)
    

    except Exception as e:
        print(f"Failed to fetch audio: {e}")
        return None

    # Handle Response
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed with status code {response.status_code}")
        return None


    