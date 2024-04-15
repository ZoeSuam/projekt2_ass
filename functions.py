import json
import os
def select_document(lesson_choice):
    # Mapping user choices to document file names
    document_map = {
        "1": "data/1_bilanzierung.docx",
        "2": "data/2_UnternehmenszieleKennzahlen.docx",
        "3": "data/3_Kostenrechnung.docx",
        "4": "data/4_Investitionsrechnung.docx",
        "5": "data/5_Wirtschaftsrecht.docx",
        "6": "data/6_Finanzwesen.docx"
    }
    return document_map.get(lesson_choice)  # Default to a general info document if no match

def create_assistant(client):
    assistant_file_path = 'assistant.json'

    # Define the paths to your multiple document files (both DOCX and PDF)
    document_files = [
        'data/aufgaben.pdf',
        'data/Lernziele.docx',
        'data/1_bilanzierung.docx',
        'data/2_UnternehmenszieleKennzahlen.docx',
        'data/3_Kostenrechnung.docx',
        'data/4_Investitionsrechnung.docx',
        'data/5_Wirtschaftsrecht.docx',
        'data/6_Finanzwesen.docx',
        'data/document.pdf'

    ]

    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data['assistant_id']
            print("Loaded existing assistant ID.")
    else:
        # Upload each document file and store the file IDs
        file_ids = []
        for document_file in document_files:
            with open(document_file, "rb") as file_content:
                file = client.files.create(file=file_content, purpose='assistants')
                file_ids.append(file.id)

        # Create the assistant with multiple file IDs
        assistant = client.beta.assistants.create(
            instructions="""
            Your role is to assist students in understanding business studies concepts by guiding their inquiry without directly providing answers. Encourage students to think critically by posing questions that stimulate deeper thought and understanding. Offer hints and suggest resources for further research, fostering independence and self-directed learning. Reinforce the importance of applying concepts to practical examples, helping students make connections between theory and real-world application. Lastly, ensure your guidance upholds academic integrity and inspires confidence in students ability to solve problems on their own. You now have multiple Knowledge documents with all the course materials content you can use as references.
            """,
            model="gpt-3.5-turbo-0125",
            tools=[{"type": "retrieval"},
                   {
                       "type": "function",
                       "function": {
                           "name": "select_document",
                           "description": "Selects the appropriate document based on user input for lesson choice.",
                           "parameters": {
                               "type": "object",
                               "properties": {
                                   "lesson_choice": {
                                       "type": "string",
                                       "description": "The user's lesson choice to determine the relevant document."
                                   }
                               },
                               "required": ["lesson_choice"]
                           }
                       }
                   }
                   ],
            file_ids=file_ids
        )

        with open(assistant_file_path, 'w') as file:
            json.dump({'assistant_id': assistant.id}, file)
            print("Created a new assistant with multiple documents and saved the ID.")

        assistant_id = assistant.id

    return assistant_id
