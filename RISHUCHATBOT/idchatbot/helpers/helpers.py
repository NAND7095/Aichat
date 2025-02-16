import openai
from config import OPENAI_API_KEY

async def get_ai_response(text):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}]
    )
    return response["choices"][0]["message"]["content"]
