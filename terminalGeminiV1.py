import json
import sys
import google.generativeai as genai
from PIL import Image

# ~ TerminalGemini v1 ~
# ~ This version lets you input a prompt as an argument ~
# ~ It is also possible to input both prompt and image name as arguments ~
# ~ GOOGLE API KEY needed in config.json aswell as image folder PATH ~

# ~ Note that this version has no chat history ~


print("hello")
argc = len(sys.argv)
# Check for correct argument count
if not 2 <= argc <= 3:
    print(f"Usage: {sys.argv[0]} <prompt>\nUsage: {sys.argv[0]} <prompt> <image>\n", file=sys.stderr)
    sys.exit(1)

# Script name and input
if argc == 2:
    script_name = sys.argv[0]
    input_prompt = sys.argv[1]
else:
    script_name = sys.argv[0]
    input_prompt = sys.argv[1]
    image_name = sys.argv[2]

# Load API key from configuration file
try:
    with open('config.json', 'r') as file:
        config = json.load(file)
        GOOGLE_API_KEY = config.get('GOOGLE_API_KEY')
        if argc == 3:
            IMAGE_PATH = config.get('IMAGE_PATH')
except FileNotFoundError:
    print("Error: Configuration file 'config.json' not found.", file=sys.stderr)
    sys.exit(1)

if not GOOGLE_API_KEY:
    print("Error: API Key not found in configuration file.", file=sys.stderr)
    sys.exit(1)

if argc == 3:
    if not IMAGE_PATH:
        print("Error: IMAGE_PATH not found in config.json", file=sys.stderr)
        sys.exit(1)


# Configure the API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
#chat = model.start_chat(history=[]) # init chat

# Optional: Display an image
if argc == 3:
    IMAGE_PATH = IMAGE_PATH + "/" + image_name

    try:
        img = Image.open(IMAGE_PATH)
        img.show()
    except FileNotFoundError:
        print("Error: 'image.jpg' not found.", file=sys.stderr)
    except Exception as e:
        print(f"Error opening image: {e}", file=sys.stderr)

# Upload IMAGE to Gemeni database 

# Generate text using the API
try:
    if argc == 3:
        response = model.generate_content([input_prompt,img])
    else:
        response = model.generate_content(input_prompt)

    print(response.text)
except genai.APIError as e:
    print(f"Gemini API Error: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error during API call: {e}", file=sys.stderr)
    sys.exit(1)


sys.exit(0)

