import requests
import boto3
import os
from dotenv import load_dotenv
import time
import google.generativeai as genai


load_dotenv()

# Import custom functions
from functions.database import get_recent_messages

# Retrieve Environment Variables
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)


# Initialize the Transcribe client
transcribe_client = boto3.client(
    'transcribe',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)


s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)


bucket_name = "your bucket name" #put your bucket name

def upload_to_s3(file):
    try:
        file_key = f"uploads/{file.filename}"
        s3_client.upload_fileobj(file.file, bucket_name, file_key)
        return f"s3://{bucket_name}/{file_key}"
    except Exception as e:
        print(f"Failed to upload file to S3: {e}")
        return None

# Convert Audio to text
def convert_audio_to_text(audio_uri: str):
    job_name = f"transcription_job_{int(time.time())}"
    try:
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': audio_uri},
            MediaFormat='wav',  # wav format
            LanguageCode='en-US',
        )
        while True:
            response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            status = response['TranscriptionJob']['TranscriptionJobStatus']
            if status in ['COMPLETED', 'FAILED']:
                break
            print("Waiting for transcription to complete...")
            time.sleep(5)
        if status == 'COMPLETED':
            transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
            transcript_response = requests.get(transcript_uri)
            transcript_data = transcript_response.json()
            return transcript_data['results']['transcripts'][0]['transcript']
        else:
            return None
    except Exception as e:
        print(f"Failed to transcribe audio: {e}")
        return None


# Get Chat Response

def get_chat_response(message_input):
    try:
        # Instantiate the model
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
         # Get recent messages for context
        messages = get_recent_messages()
        user_message = {"role": "user", "content": message_input}
        messages.append(user_message)
        
        # Create a combined prompt with the instruction
        combined_prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        
        # Generate content based on the combined prompt
        response = model.generate_content(combined_prompt)
        
        # Extract the response text
        if response and hasattr(response, 'candidates') and len(response.candidates) > 0:
            gemini_response = response.candidates[0].content.parts[0].text.strip()
            return gemini_response
        else:
            return "Failed to get response from Gemini"
    except Exception as e:
        print("Failed to get response from Gemini:", e)
        return "Failed to get response from Gemini"

        
           