import random
import asyncio
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import Message, ChatAction
from deep_translator import GoogleTranslator
from RISHUCHATBOT import RISHUCHATBOT
from RISHUCHATBOT.idchatbot.helpers import get_ai_response
from config import OPENAI_API_KEY

# MongoDB Connection
mongo = MongoClient("MONGO_URL")
db = mongo["ChatBotDB"]
lang_db = db.ChatLangDb.LangCollection
status_db = db.chatbot_status_db.status
user_names = db.user_names  # User names store karne ke liye
chatai = db.chatai  # Stickers & Media DB (not changed)

@Client.on_message(filters.incoming)
async def chatbot_response(client: Client, message: Message):
    try:
        chat_id = message.chat.id
        bot_id = client.me.id

        # Ignore Commands
        if message.text and any(message.text.startswith(prefix) for prefix in ["!", "/", ".", "?", "@", "#"]):
            return

        # 3-5 sec typing delay for human-like response
        await asyncio.sleep(random.uniform(3, 5))
        await client.send_chat_action(chat_id, ChatAction.TYPING)

        # **"Tum bot ho?"** Ka reply nahi dega
        bot_questions = ["tum bot ho?", "kya tum ek bot ho?", "kya tum AI ho?", "tum insaan ho ya bot?", "tum real ho?"]
        if message.text.lower() in bot_questions:
            return  # Ignore the message, no reply

        # **Agar naam puche to "Aradhna" bataye**
        if any(x in message.text.lower() for x in ["tumhara naam kya hai", "apna naam batao", "aap kaun ho", "what's your name", "who are you"]):
            return await message.reply_text("Aradhna")

        # **Agar puche "tumhe kisne banaya?" to fixed reply**
        if any(x in message.text.lower() for x in ["tumhe kisne banaya", "who created you", "who made you"]):
            return await message.reply_text("Kya yaar, sabko uske mummy papa hi janma dete.")

        # **Agar koi apna naam bataye to yaad rakhe**
        if "mera naam" in message.text.lower() or "my name is" in message.text.lower():
            user_name = message.text.split()[-1]
            await user_names.update_one({"user_id": message.from_user.id}, {"$set": {"name": user_name}}, upsert=True)
            return await message.reply_text(f"Acha {user_name}, yaad rahega!")

        # **Agar user ka naam pehle se saved hai to use kare**
        saved_user = await user_names.find_one({"user_id": message.from_user.id})
        user_name = saved_user["name"] if saved_user else None

        # **Check if sticker, image, or media response is in DB**
        reply_data = await chatai.find_one({"word": message.text})
        if reply_data:
            if reply_data["check"] == "sticker":
                return await message.reply_sticker(reply_data["text"])
            elif reply_data["check"] == "photo":
                return await message.reply_photo(reply_data["text"])
            elif reply_data["check"] == "video":
                return await message.reply_video(reply_data["text"])
            elif reply_data["check"] == "audio":
                return await message.reply_audio(reply_data["text"])
            elif reply_data["check"] == "gif":
                return await message.reply_animation(reply_data["text"])
            elif reply_data["check"] == "voice":
                return await message.reply_voice(reply_data["text"])
            else:
                return await message.reply_text(reply_data["text"])

        # **AI-based human-like reply**
        ai_response = await get_ai_response(message.text)
        if ai_response:
            reply_text = f"{user_name}, {ai_response}" if user_name else ai_response
            return await message.reply_text(reply_text)

        # **Default fallback response**
        await message.reply_text("Mujhe samajh nahi aaya, kya kehna chahte ho?")
    
    except Exception as e:
        print(f"Error: {e}")
