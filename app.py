from flask import Flask
from assistants.assistant_interface import create_assistant_and_store, create_thread, client
from Resources.setup_prompt import setup_prompt

app = Flask(__name__)
#add session key

assistant = create_assistant_and_store(client, setup_prompt, "vs_2JsFtCulgmmlvWdkV11hdMI9")
thread = create_thread(client)

import views
