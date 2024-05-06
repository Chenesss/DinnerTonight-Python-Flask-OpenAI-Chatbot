from openai import OpenAI
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.pyplot as plt
# import os


client = OpenAI()
MODEL_NAME="gpt-4-turbo" #### You can change the model here and use your own fine tuned models
TEMPERATURE=0

def get_openai_response(user_content, system_content="", model=MODEL_NAME):

    response = client.chat.completions.create(
        model=model,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
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
                        "required": ["location"],
                
                    },
                }    
            }
        ],
        tool_choice="auto"

    )
    
    return response.choices[0].message.content




if __name__=="__main__":
    input_message = "What should I eat tonight in San Francisco CA if I want chinese?"
    print(get_openai_response(user_content=input_message, system_content="Help me find what to eat tonight?"))