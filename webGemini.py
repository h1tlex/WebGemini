from flask import Flask, session, render_template, request, jsonify
import json
import sqlite3
import google.generativeai as genai
import os
import secrets
import base64

# ~ webAI ~
# ~ Developed using flask and HTML with AJAX implementation ~
# ~ GOOGLE API KEY needed in config.json aswell as image folder PATH ~

# Initialize Flask app
app = Flask(__name__)

# Generate and load secret key
SECRET_KEY_FILE = "secret_key.txt"
if os.path.exists(SECRET_KEY_FILE): # if secret key exists
    with open(SECRET_KEY_FILE, "r") as f:
        app.secret_key = f.read().strip()
else: # generate secret_key
    secret_key = base64.b64encode(secrets.token_bytes(32)).decode('utf-8')
    with open(SECRET_KEY_FILE, "w") as f: # write secret key in file
        f.write(secret_key)
    app.secret_key = secret_key # set secret key

# Store messages temporarily for the session (in-memory)
# messages = [] # turn this into database

# Initialize connection to SQLite database
DATABASE = 'chat_hisotry.bd'
# Data base functions
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Return dictionaries instead of tuples
    return conn

def init_db():
    with get_db_connection() as conn:
        with open('schema.sql', 'r') as f:
            conn.cursor().executescript(f.read())
        conn.commit()
# Create schema.sql
# CREATE TABLE IF NOT EXISTS messages (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     role TEXT NOT NULL,
#     parts TEXT NOT NULL
# );

def save_message(role, parts):
    conn = get_db_connection()
    conn.execute("INSERT INTO messages (role, parts) VALUES (?, ?)", (role, json.dumps(parts)))
    conn.commit()
    conn.close()

def get_messages():
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages').fetchall()
    conn.close()
    return messages

def clear_chat_history():
    with get_db_connection() as conn:
        conn.execute("DELETE FROM messages")  # Delete all rows from the table
        conn.commit()

# Route homepage
@app.route("/")
def home():
	return render_template("index.html")

# Route chat session page
@app.route("/session", methods=["GET", "POST"])
def chat():
    model = gemini_init()  
    if model is None:
        return "Failed to initialize Gemini.", 500
    
    if 'messages' not in session:
        session['message'] = []
    
    messages = session.get('messages', [])

    if request.method == "POST":
        data = request.get_json()  # Expecting JSON data from AJAX
        user_input = data.get("user_input", "")

        chat_history_for_api = [{"role": m["role"], "parts": m["parts"]} for m in messages]
        chat = model.start_chat(history=chat_history_for_api)

        response =generate_gemini_response(user_input,chat)

        messages.append({"role": "user", "parts": [user_input]})  # Correct format
        messages.append({"role": "model", "parts": [response]})  # Correct format

        save_message("user", [user_input])
        save_message("model", [response])
        
        session['messages'] = messages
        session.modified = True
        return jsonify({"response": response})

    # Retrieve messages from database for current session
    db_messages = get_messages()
    messages_from_db = [{"user": json.loads(m[2])[0]} if m[1] == "user" else {"bot": json.loads(m[2])[0]} for m in db_messages ]
    return render_template("chat.html", messages=messages_from_db)

def gemini_init():
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model
    

def generate_gemini_response(prompt,chat):
    try:
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"An unexpected error occurred: {e}"
    


if __name__ == "__main__":
    try:
        with open('config.json', 'r') as file:
                config = json.load(file)
                GOOGLE_API_KEY = config.get('GOOGLE_API_KEY')
    except FileNotFoundError:
        print("Error: Configuration file 'config.json' not found.") 
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}") 
    except ImportError as e:
        print(f"ImportError: {e}") 

    if not GOOGLE_API_KEY:
        print("Error: API Key not found in configuration file.") 

    clear_chat_history()
    init_db()

    app.run(host="0.0.0.0", port=80, debug=True)

