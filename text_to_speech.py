import requests
from decouple import config

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")

def text_to_speech(message):

    #Define Data (Body)
    body={
        "text": message,
        "voice settings": {
        "stability": 0,
        "similarity boost": 0,
        }
    }

    #define voice, you get the voice id from eleven labs api documentation
    voice_rachel="21m00Tcm4TlvDq8ikWAM"


    #Constructing headers and endpoints
    headers = {"xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json", "accept": "audio/mpeg"}
    endpoint=f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

    #Send request
    try:
        response=requests.post(endpoint, headers=headers, json=body)
    except Exception as e:
        print(e)
        return None
    
    #Handle response
    if response.status_code==200:
        return response.content
    else:
        return None