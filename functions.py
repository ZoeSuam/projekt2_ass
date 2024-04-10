import json
import os

def create_assistant(client):
  assistant_file_path = 'assistant.json'

  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    file = client.files.create(file=open("knowledge.docx", "rb"),
                               purpose='assistants')

    assistant = client.beta.assistants.create(instructions="""
         Your role is to assist students in understanding business studies concepts by guiding their inquiry without directly providing answers. Encourage students to think critically by posing questions that stimulate deeper thought and understanding. Offer hints and suggest resources for further research, fostering independence and self-directed learning. Reinforce the importance of applying concepts to practical examples, helping students make connections between theory and real-world application. Lastly, ensure your guidance upholds academic integrity and inspires confidence in students ability to solve problems on their own.You have a Knowledge document with all the coursematerials content you can use as a reference
          """,
                                              model="gpt-4-1106-preview",
                                              tools=[{
                                                  "type": "retrieval"
                                              }],
                                              file_ids=[file.id])

    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id
