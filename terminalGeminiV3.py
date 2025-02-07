import json
import google.generativeai as genai
import sys
from PIL import Image

# ~ TerminalGemini v3 ~
# ~ This version is equipped with a chat history ~
# ~ Also uses session ID ~
# ~ GOOGLE API KEY needed in config.json aswell as image folder PATH ~


# Function to start and manage chats
def start_chat():
    """Starts a chat session and allows multiple user prompts."""
    chat_sessions = {}  # Dictionary to store multiple chat histories

    while True:
        session_id = input("Enter session ID (or 'exit' to quit): ")
        if session_id.lower() == 'exit':
            break

        if session_id not in chat_sessions:
            chat_sessions[session_id] = model.start_chat(history=[])
            print(f"New chat session '{session_id}' started.")

        chat = chat_sessions[session_id]
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print(f"Exiting chat session '{session_id}'.")
                break

            try:
                response = chat.send_message(user_input)
                print(f"Gemini: {response.text}\n")  # Assuming 'text' is the correct attribute
            except Exception as e:
                print(f"Error during chat interaction: {e}\n")

# Load API key from configuration file
try:
    with open('config.json', 'r') as file:
        config = json.load(file)
        GOOGLE_API_KEY = config.get('GOOGLE_API_KEY')
        
except FileNotFoundError:
    print("Error: Configuration file 'config.json' not found.", file=sys.stderr)
    sys.exit(1)

if not GOOGLE_API_KEY:
    print("Error: API Key not found in configuration file.", file=sys.stderr)
    sys.exit(1)

# Configure the API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")



# Start the chat management system
if __name__ == "__main__":
    start_chat()
