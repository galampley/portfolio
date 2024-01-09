# Portfolio Site

## Introduction
My first take on a portfolio site. I am not a frontend developer so the site does not respond well on mobile...I'm working on it. 

Integrated a chatbot into the site as an unmissable example of my AI work. In its current state, best works for questions like "What are Greyson's greatest strengths?". Will time out on more queries that require answers from OpenAI that take longer than 10s to generate. 

## 'App' Directory Descriptions
1. chatbot - functions.py; provides OpenAI logs on backend + automates some backend routines for reference_content
2. reference_content - blog, about_me, resume
3. static - chatbot.js, styles.css, content
4. templates - index.html
5. main.py 


## Chatbot
Uses Flask as the micro web framework. I used FastAPI in Whoop_GPT because speed was more of a focus since I needed the backend API for Whoop authentication AND OpenAI queries instead of just OpenAI queries. 

chatbot.js powers queries being received and delivered with OpenAI API.