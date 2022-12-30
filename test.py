import openai
import os

openai.api_key = os.getenv("OPENAI_API_TOKEN")

response = openai.Completion.create(
    model="text-davinci-003",
    prompt="hello",
    temperature=0.5,
    max_tokens=1000,
    top_p=1.0,
    frequency_penalty=0.5,
    presence_penalty=0.0,
)

print(response)