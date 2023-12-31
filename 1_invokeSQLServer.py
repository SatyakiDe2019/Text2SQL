#############################################################
#### Written By: SATYAKI DE                              ####
#### Written On: 17-Dec-2023                             ####
#### Modified On 31-Dec-2023                             ####
####                                                     ####
#### Objective: This is the main calling                 ####
#### python script that will invoke the                  ####
#### Open AI api to convert the enhanced prompts         ####
#### and then dynamically create the SQL.                ####
####                                                     ####
#############################################################

from flask import Flask, request, session
from openai import OpenAI

from clsConfigClient import clsConfigClient as cf
import os

from datetime import datetime, timedelta

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

########################################################
################    Global Area   ######################
########################################################

app = Flask(__name__)
app.secret_key = cf.conf['ADMIN_KEY']
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Configure OpenAI key
# Configure the default for all requests:
client = OpenAI(
    # default is 2
    api_key=cf.conf['OPEN_AI_KEY'],
    max_retries=0,
    timeout=20.0,
)

########################################################
################  End Of Global Area   #################
########################################################

@app.route('/message', methods=['POST'])
def message():
    input_text = request.json.get('input_text', None)
    session_id = request.json.get('session_id', None)

    print('*' * 240)
    print('User Input:')
    print(str(input_text))
    print('*' * 240)

    # Retrieve conversation history from the session or database
    conversation_history = session.get(session_id, [])

    # Add the new message to the conversation history
    conversation_history.append(input_text)

    # Call OpenAI API with the updated conversation
    response = client.with_options(max_retries=0).chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input_text,
            }
        ],
        model=cf.conf['MODEL_NAME'],
    )

    # Extract the content from the first choice's message
    chat_response = response.choices[0].message.content
    print('*' * 240)
    print('Resposne::')
    print(chat_response)
    print('*' * 240)

    conversation_history.append(chat_response)

    # Store the updated conversation history in the session or database
    session[session_id] = conversation_history

    return chat_response

if __name__ == '__main__':
    app.run()
