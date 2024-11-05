import json
import random

# Get recent messages
def get_recent_messages():
    # Define the file name and leave instruction
    file_name = "stored_data.json"
    learn_instruction = {
        "role": "system",
        "content": "You are speaking with the user for a job as a friend. Give the user a satisfactory answer. Your name is SpeakAI. Keep your word under 30 words. Display some emotion like joy, sorrow, happiness, sadness based on the user message. "
    }

    # Initialize messages
    messages = []

    # Add a random element
    x = random.uniform(0, 1)
    if x < 0.5:
        learn_instruction["content"] += " Your response will include some dry humor."
    else:
        learn_instruction["content"] += " Your response will include a rather challenging question."

    # Append instruction to message
    messages.append(learn_instruction)

    # Get last messages
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            # Append last 5 items of data
            if data:
                if len(data) < 5:
                    messages.extend(data)
                else:
                    messages.extend(data[-5:])

    except Exception as e:
        print(e)
        pass

    # Return
    return messages or []

# Store messages
def store_messages(request_message, response_message):
    # Define the file name
    file_name = "stored_data.json"

    # Get recent messages
    messages = get_recent_messages()[1:]

    # Add messages to data
    user_message = {"role": "user", "content": request_message}
    assistant_message = {"role": "assistant", "content": response_message}
    messages.append(user_message)
    messages.append(assistant_message)

    # Save the updated file
    try:
        with open(file_name, "w") as f:
            json.dump(messages, f)
    except Exception as e:
        print(f"Failed to store messages: {e}")


#Reset messages
def reset_messages():

    #Overwrite current files with nothing
    open("stored_data.json","w")

