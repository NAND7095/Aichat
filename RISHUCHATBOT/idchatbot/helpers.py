import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def get_ai_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Agar better accuracy chahiye to "gpt-4" use kar sakte ho
            messages=[{"role": "user", "content": user_message}],
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"AI Error: {e}")
        return "Mujhe samajh nahi aaya, kya kehna chahte ho?"
