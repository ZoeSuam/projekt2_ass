import os
from time import sleep
from packaging import version
from flask import Flask, request, jsonify
import openai
from openai import OpenAI
import functions

# Check OpenAI version is correct
required_version = version.parse("1.1.1")
current_version = version.parse(openai.__version__)
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
if current_version < required_version:
  raise ValueError(f"Error: OpenAI version {openai.__version__}"
                   " is less than the required version 1.1.1")
else:
  print("OpenAI version is compatible.")

# Start Flask app
app = Flask(__name__)

# Init client
client = OpenAI(
    api_key=OPENAI_API_KEY)  # should use env variable OPENAI_API_KEY in secrets (bottom left corner)

# Create new assistant or load existing
assistant_id = functions.create_assistant(client)

# Start conversation thread
@app.route('/start', methods=['GET'])
def start_conversation():
  print("Starting a new conversation...")  # Debugging line
  thread = client.beta.threads.create()
  print(f"New thread created with ID: {thread.id}")  # Debugging line
  return jsonify({"thread_id": thread.id})

# Generate response
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    thread_id = data.get('thread_id')
    user_input = data.get('message', '')
    lesson_choice = data.get('lesson_choice', '')

    if not thread_id:
        print("Error: Missing thread_id")
        return jsonify({"error": "Missing thread_id"}), 400

    # Bestimmung des Dokuments basierend auf der lesson_choice
    if lesson_choice and not user_input:
        # Erster Aufruf: Auswahl des Dokuments
        document_path = functions.select_document(lesson_choice)
        print(f"Selected document for lesson {lesson_choice}: {document_path}")
        response_text = f"What is your question regarding {document_path.split('/')[-1]}?"
        return jsonify({"response": response_text})

    elif user_input and lesson_choice:
        # Zweiter Aufruf: Verarbeitung der Nutzeranfrage
        document_path = functions.select_document(lesson_choice)  # Sicherstellen, dass das korrekte Dokument verwendet wird
        # Hier sollte eine Logik implementiert sein, die die Anfrage im Dokument verarbeitet
        # (Beispielhaft, dies sollte durch tatsächliche Logik zur Dokumentsuche ersetzt werden)
        response_text = f"Based on {document_path}, here is the information regarding '{user_input}'."
        return jsonify({"response": response_text})

    return jsonify({"error": "Required data is missing"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)



