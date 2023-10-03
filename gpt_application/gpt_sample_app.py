
import os
import openai
openai.api_key = "api_key"

messages = []
user_content = input("user : ")
messages.append({"role": "user", "content": f"{user_content}"})

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
)

print(response['choices'][0]['message']['content'].strip())
