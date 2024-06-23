import os
from openai import OpenAI 


client = OpenAI(api_key=os.getenv("OPENAI_SECRET_KEY"))

def create_assistant(client, setup_prompt, model="gpt-4-1106-preview"):
  assistant = client.beta.assistants.create(
    name="Eldin Ring Oracle", 
    instructions=setup_prompt,
    tools=[{"type": "file_search"}],
    model=model
  )
  return assistant

def create_vector_store(client):
  vector_store = client.beta.vector_stores.create(name="Eldin Ring Info")
  file_paths = ["Resources\eldin_ring_info-1.json", "Resources\eldin_ring_info-2.json"]
  file_streams = [open(path, "rb") for path in file_paths]

  file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
  )

  print(file_batch.status)
  print(file_batch.file_counts)
  return vector_store

def attach_vector_store(client, assistant, vector_store_id):
  assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids":[vector_store_id]}},
  )
  return assistant

def create_assistant_and_store(client, setup_prompt, vector_store_id=None):
  assistant = create_assistant(client, setup_prompt)
  if vector_store_id is None:
    vector_store = create_vector_store(client)
    vector_store_id = vector_store.id
  assistant = attach_vector_store(client, assistant, vector_store_id)
  return assistant

def create_thread(client):
  thread = client.beta.threads.create()
  return thread

def add_message_to_thread(thread, message):
  message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=message
  )
  return message


def get_assitant_messages(client, thread, assistant):
  run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id, 
  )

  messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

  message_content = messages[0].content[0].text
  annotations = message_content.annotations
  citations = []
  for index, annotation in enumerate(annotations):
      message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
      if file_citation := getattr(annotation, "file_citation", None):
          cited_file = client.files.retrieve(file_citation.file_id)
          citations.append(f"[{index}] {cited_file.filename}")
  print(message_content.value)
  print("\n".join(citations))