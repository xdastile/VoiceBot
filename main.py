#uvicorn main:app
#uvicorn main:app --reload
#Cross Origin Resource Sharing (CORS)
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

#Custom Functions Imports
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.database import store_messages, reset_messages
from functions.text_to_speech import text_to_speech


#Initiate App
app = FastAPI()


#CORS origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
]


#CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], #GET, POST, PUT, DELETE, OPTIONS, HEAD
    allow_headers=["*"],
)


#Check Health
@app.get("/health")
async def check_health():
    return {"message": "healthy"}

#Reset messages
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "conversation reset"}

#get audio file
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):

    # #Get saved audio file
    # audio_input = open("voice.mp3", "rb")

    #Get file from Frontend
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    audio_input = open(file.filename, "rb")

    #decode audio
    message_decoded=convert_audio_to_text(audio_input)
    
    #Guard: Ensure message is decoded
    if not message_decoded:
        return HTTPException(status_code=400, detail="Failed to decoded audio")
    
    #Get ChatGPT response
    chat_response=get_chat_response(message_decoded)

    #Guard: Ensure chat response is generated
    if not chat_response:
        return HTTPException(status_code=400, detail="Failed to handle chat response")

    #store messages
    store_messages(message_decoded, chat_response)

    #Convert chat response to audio
    audio_output=text_to_speech(chat_response)

    #Guard: Ensure audio is generated
    if not audio_output:
        return HTTPException(status_code=400, detail="Failed to get Eleven Labs response")
    
    #Create a generator that yields chuncks of data
    def iterfile():
        yield audio_output

    #Return audio file
    return StreamingResponse(iterfile(), media_type="application/octet-stream")



    return 'Done'




