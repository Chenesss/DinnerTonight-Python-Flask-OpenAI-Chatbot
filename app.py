# Import necessary libraries
from flask import Flask, render_template, request, redirect
from openai import OpenAI
import os
import time
from yelp_fusion_api import get_yelp_businesses
import json

# Set the OpenAI API key in your environment or in here
# openai.api_key = ""
client = OpenAI()

# Define the name of the bot
name = 'BOT'

# Define the role of the bot
role = 'customer service'

# Define the impersonated role with instructions
system_context = f"""
    You are a good friend that recommmends restaurants and recommends specific dishes in that restaurant and why it is worth going there for dinner tonight. 
    If no location is given, please ask the user for the location.
    If no cusine is given, pick a random cusine.
    
    Please use proper formatting with new lines.
"""

# Initialize variables for chat history
explicit_input = ""
chatgpt_output = 'Chat log: /n'
cwd = os.getcwd()
i = 1

# Find an available chat history file
while os.path.exists(os.path.join(cwd, f'chat_history{i}.txt')):
    i += 1

history_file = os.path.join(cwd, f'chat_history{i}.txt')

# Initialize chat history
chat_history = ''

# Create a Flask web application
app = Flask(__name__)

# Function to complete chat input using OpenAI's GPT-4 Turbo
def chatcompletion(user_input, system_context, explicit_input, chat_history):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        temperature=1,
        presence_penalty=0,
        frequency_penalty=0,
        messages=[
            {"role": "system", "content": f"{system_context}. Conversation history: {chat_history}"},
            {"role": "user", "content": f"{user_input}. {explicit_input}"},
        ],
        tools=[
            {
                "type" : "function",
                "function" : {
                    "name" : "get_restaurant_recommendations",
                    "description" : "Gets a list of restaurant recommendations given some parameters",
                    "parameters" : {
                        "type": "object",
                        "properties" : {
                            "location" : {
                                "type": "string",
                                "description": "The city and the state. E.g. San Francisco, CA",
                            },
                            "cusine" : {
                                "type": "string",
                                "description" : "Asian",
                            },
                        },
                        "required": ["location", "cusine"],
                
                    },
                }    
            }
        ],
        tool_choice="auto"
    )


    return response.choices[0]

# Function to handle user chat input
def chat(user_input):
    global chat_history, name, chatgpt_output
    current_day = time.strftime("%d/%m", time.localtime())
    current_time = time.strftime("%H:%M:%S", time.localtime())
    chat_history += f'\nUser: {user_input}\n'
    
    chatgpt_raw_output = chatcompletion(user_input, system_context, explicit_input, chat_history)
    if chatgpt_raw_output.message.tool_calls:
        result = json.loads(chatgpt_raw_output.message.tool_calls[0].function.arguments)

        businesses_json_str = get_yelp_businesses(result["location"], result["cusine"])
        
        chatgpt_raw_output = chatcompletion(user_input, system_context + "\n Use the following JSON as the list of restaurants to pick from. " + json.dumps(businesses_json_str['businesses']), "Pick a restaurant from the JSON list and convince why it is good. Imagine that all restaurants on this list is the same cusine that I requested for.", chat_history)

    chatgpt_raw_output = chatgpt_raw_output.message.content
    chatgpt_output = f'{name}: {chatgpt_raw_output}'


    return chatgpt_raw_output

# Function to get a response from the chatbot
def get_response(userText):
    return chat(userText)

# Define app routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
# Function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    return str(get_response(userText))

@app.route('/refresh')
def refresh():
    time.sleep(600) # Wait for 10 minutes
    return redirect('/refresh')

# Run the Flask app
if __name__ == "__main__":
    app.run()
