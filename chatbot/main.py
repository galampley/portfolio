import os
import openai
import requests
import matplotlib.pyplot as plt
import time
from functions import *

from dotenv import load_dotenv

dotenv_path = '/Users/galampley/Documents/secrets.env'  # Replace with the path to your .env file if it's not in the current directory
load_dotenv(dotenv_path)

env_variable = os.getenv('OPENAI_API_KEY')
env_variable_blog = os.getenv('BLOG_API_KEY')

download_resume()
download_about_me()
download_blog("greysonlampley", env_variable_blog)

def get_query(query):
    return input(query)

def main():
    try:
        resume = openai.files.create(     
                file=open("reference_content/resume.pdf", "rb"),
                purpose='assistants'
        )

        about_me = openai.files.create(     
                file=open("reference_content/about_me.txt", "rb"),
                purpose='assistants'
        )
        
        # Directory containing the blog files
        directory = 'reference_content/blog'
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
            instructions=f"You will answer questions about Greyson's experience, skills, thoughts and/or aspirations.\
            I've provided you with a blurb about_me, my resume.pdf and blog entries: {blog_names},\
            where I discuss my thoughts on diverse AI subjects",
            tools=[{'type': 'retrieval'}],
            model="gpt-4-1106-preview",
            file_ids = all_file_ids
            )

        print("\nHello there, I'm Greyson's Portfolio Wiz. Ask some questions about his experience, skills, blog or aspirations.\n")

        # Create a thread
        thread = openai.beta.threads.create()

        # Use keep_asking as state to keep asking questions
        keep_asking = True
        while keep_asking:
            user_query = get_query("\nUser: ")

            # Pass in the user question into the existing thread
            openai.beta.threads.messages.create(
                role="user",
                content=user_query,
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
            run_steps

            # Get the last assistant message from the messages array
            messages = openai.beta.threads.messages.list(thread_id=thread.id)

            response_list = []
            
            for message in messages:  
                if message.role == 'assistant' and message.run_id == run.id:
                    for content in message.content:
                        if content.type == 'text':
                            assistant_response = content.text.value
                            response_list.append(assistant_response)  # Append each value to the list
                        if content.type == 'image_file':
                            assistant_img = content.image_file.file_id
                            display_image(assistant_img)
                
            # Reverse the collected list once after all responses are collected
            response_list.reverse()

            # Print the reversed list as a string
            for response in response_list:
                print(response)  # Print each response from the list
            
    except Exception as error:
        print(error)

if __name__ == "__main__":
    main()