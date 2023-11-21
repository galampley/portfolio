import os
import openai
import requests
import matplotlib.pyplot as plt
import time
from app.chatbot.functions import *
from flask import Flask, request, jsonify, render_template # moving to web requests instead of just console inputs
from dotenv import load_dotenv
import json

app = Flask(__name__)

dotenv_path = '/Users/galampley/Documents/secrets.env'  
load_dotenv(dotenv_path)

env_variable = os.getenv('OPENAI_API_KEY')
env_variable_blog = os.getenv('BLOG_API_KEY')

download_resume()
download_about_me()
download_blog("greysonlampley", env_variable_blog)

assistant=None
thread=None

@app.route('/chat', methods=['POST'])
def chat_with_assistant():
    global assistant, thread
    user_input = request.json['message']

    if assistant is None or thread is None: 
        assistant, thread = create_assistant_and_thread()

    # response = main(user_input) 
    response = run_and_get_response(user_input, thread, assistant)

    # Check if the response is a string and remove leading/trailing quotation marks
    if isinstance(response, str):
        response = response.strip('"')
    return response 

def create_assistant_and_thread(): 
    try:
        resume = openai.files.create(     
                file=open("app/reference_content/resume.pdf", "rb"),
                purpose='assistants'
        )

        about_me = openai.files.create(     
                file=open("app/reference_content/about_me.txt", "rb"),
                purpose='assistants'
        )
        
        # Directory containing the blog files
        directory = 'app/reference_content/blog'
        all_file_ids = []  # List to store the OpenAI file IDs
        blog_names = []

        # Iterate over each file in the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                # Open the file and create an OpenAI file object
                with open(file_path, 'rb') as file:
                    response = openai.files.create(
                        file=file,
                        purpose='assistants'  
                    )
                    all_file_ids.append(response.id)
                    blog_names.append(filename)
            except Exception as e:
                print(f"Failed to create OpenAI file object for {filename}: {e}")
       
        all_file_ids += [resume.id, about_me.id]

        # Create a new assistant
        assistant = openai.beta.assistants.create(
            name="Greyson's Portfolio Wiz",
            instructions=f"You will answer questions about Greyson's experience, background and opinions. Always keep responses short unless an elaborate answer is explicitly requested. I've provided you with the following documents but don't ever mention that you have access to these uploaded documents unless explicitly asked about it.:\
            \nabout_me.txt = {about_me.id}: Introduces Greyson and explains how/why he got into AI\
            \nresume.pdf = {resume.id}: Greyson's AI projects, certifications. As well as his education and work experience.\
            \nblog entries - {blog_names}: Greyson's thoughts on various AI topics.",
            tools=[{'type': 'retrieval'}],
            model="gpt-4-1106-preview",
            file_ids = all_file_ids,
            )

        print("\nstarting thread...\n")

        # Create a thread
        thread = openai.beta.threads.create()
    
        return assistant, thread
    
    except Exception as error:
        return {'error':str(error)}

def run_and_get_response(user_input, thread, assistant):
    # Pass in the user question into the existing thread
    openai.beta.threads.messages.create(
        role="user",
        content= user_input, #user_query,
        thread_id=thread.id
    )

    # Use runs to wait for the assistant response and then retrieve it
    run = openai.beta.threads.runs.create(
        assistant_id=assistant.id,
        thread_id=thread.id
    )

    # Polling mechanism to see if run_status is completed
    run_status = openai.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

    while run_status.status != "completed":
        run_status = openai.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    run_steps = fetch_and_display_run_steps(thread.id, run.id)

    messages = openai.beta.threads.messages.list(thread_id=thread.id)

    response_list = []
    
    for message in messages:  
        if message.role == 'assistant' and message.run_id == run.id:
            for content in message.content:
                if content.type == 'text':
                    assistant_response = content.text.value
                    response_list.append(assistant_response)  
                if content.type == 'image_file':
                    assistant_img = content.image_file.file_id
                    display_image(assistant_img)
        
    # Reverse the collected list once after all responses are collected
    response_list.reverse()

    # Join all the responses in the list into a single string
    # response_text = "\n".join(response_list)
    print(response_list)
    return response_list

    # Return the joined string
    # return response_text

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)