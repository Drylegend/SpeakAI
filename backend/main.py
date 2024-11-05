# uvicorn main:app
# uvicorn main:app --reload
# venv\Scripts\activate
#uvicorn main:app  --reload --host 0.0.0.0 --port 8000

# Main imports
from typing import Union
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import google.generativeai as genai # type: ignore
import os



# Custom Functions imports
from functions.database import store_messages, reset_messages
from functions.open_requests import convert_audio_to_text, get_chat_response, upload_to_s3
from functions.text_to_speech import convert_text_speech

# Initiate App
app = FastAPI()

# CORS - Origins
origins = [
    "https://localhost:5173",
    "https://localhost:5174",
    "https://localhost:4173",
    "https://localhost:4174",
    "https://localhost:3000",
]

# CORS - Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check health
@app.get("/health")
async def check_health():
    return {"message": "Healthy"}

# Reset messages
@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "Conversation Reset"}

# Post bot response
# Note: Not playing back in browser when using post request.
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):
    audio_uri = upload_to_s3(file)   #"s3://my-new-bucketlist/voice.mp3"  # Updated with S3 bucket URI

    if not audio_uri:
        raise HTTPException(status_code=400, detail="Failed to upload file to S3")

    # Decode audio
    message_decoded = convert_audio_to_text(audio_uri)
    print("Transcription:", message_decoded)

    # Guard: Ensure message decoded
    if not message_decoded:
        raise HTTPException(status_code=400, detail="Failed to decode audio")

    # Get chat response
    chat_response = get_chat_response(message_decoded)

    print("chat response:", chat_response)

    # Guard: Ensure chat response
    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed to get chat response")

    # Store messages
    store_messages(message_decoded, chat_response)

    #Converrt chat response to audio
    audio_output = convert_text_speech(chat_response)

    # Guard: Ensure audio output
    if not audio_output:
        raise HTTPException(status_code=400, detail="Failed to get Eleven Labs audio response")
    

    #Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    #Return Audio file
    return StreamingResponse(iterfile(), media_type="application/octet-stream")

   



