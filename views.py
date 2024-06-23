from app import app, thread, assistant 
from flask import jsonify, render_template, request
from assistants.assistant_interface import create_assistant_and_store, create_thread, add_message_to_thread, get_assitant_messages, client
from Resources.setup_prompt import setup_prompt
from assistants.EventHandler import EventHandler
@app.route('/')
def home():
  return render_template("index.html")

@app.route('/get_message', methods=['POST'])
def get_message():
  user_message = request.form.get('message')
  print(user_message)
  message = add_message_to_thread(thread, user_message)

  with client.beta.threads.runs.stream(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="",
  event_handler=EventHandler(),
  ) as stream:
    stream.until_done()
  return render_template("index.html")





if __name__ == "__main__":
  app.run()