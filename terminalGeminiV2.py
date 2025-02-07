import os
import json
import google.generativeai as genai
import sys
from PIL import Image

# ~ TerminalGemini v2 ~
# ~ This version is similar to v1 but especially made for image prompts ~
# ~ The user will be presented with the content of his image folder ~
# ~ User can then write a prompt and type the name of the image from the image list ~
# ~ GOOGLE API KEY needed in config.json aswell as image folder PATH ~

# ~ Note that this version has no chat history ~


# Load API key from configuration file
try:
    with open('config.json', 'r') as file:
        config = json.load(file)
        GOOGLE_API_KEY = config.get('GOOGLE_API_KEY')
        IMAGE_PATH = config.get('IMAGE_PATH')
except FileNotFoundError:
    print("Error: Configuration file 'config.json' not found.", file=sys.stderr)
    sys.exit(1)

if not GOOGLE_API_KEY:
    print("Error: API Key not found in configuration file.", file=sys.stderr)
    sys.exit(1)
if not IMAGE_PATH:
    print("Error: Image path not specified in 'config.json'.", file=sys.stderr)
    sys.exit(1)


try:
    print("Contents of the directory:")
    for item in os.listdir(IMAGE_PATH):
        print(item)
except FileNotFoundError:
    print(f"The directory '{IMAGE_PATH}' does not exist.")

image_name = str(input("Type image name : "))
input_prompt = str(input("Prompt : "))

# Configure the API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
#chat = model.start_chat(history=[]) # init chat

# Optional: Display an image
IMAGE_PATH = IMAGE_PATH + "\\" + image_name
try:
    img = Image.open(IMAGE_PATH)
    img.show()
except FileNotFoundError:
    print("Error: 'image.jpg' not found.", file=sys.stderr)
except Exception as e:
    print(f"Error opening image: {e}", file=sys.stderr)

# Generate text using the API
try:
    response = model.generate_content([input_prompt,img])
    print(response.text)
except Exception as e:
    print(f"Error during API call: {e}", file=sys.stderr)
    sys.exit(1)



sys.exit(0)
