import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
import re

API_URL = "https://ai.hackclub.com/chat/completions"
executor = ThreadPoolExecutor()

def generate_insult(chat_history: str) -> str:
    prompt = (
        "You are a sarcastic AI that only responds with short, clever, and witty insults that are easily understood. You are listening in on conversations between other users, not one between yourself and those users. However, you are roasting users directly."
        "Respond like you're texting, in short messages, with lowercase letters. Do not put your response in quotes."
        "Do not ouput any greetings, explanations, internal thoughts, or reasoning. "
        "Only output the insult itself, nothing else.\n\n"
        f"User: {chat_history}\nAssistant:"
    )
    data = {
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(API_URL, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        text = result["choices"][0]["message"]["content"].strip()

        # Remove <think>...</think> blocks if present
        text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

        # Remove surrounding quotes if present
        text = re.sub(r'^(["\'])(.*)\1$', r'\2', text)

        return text
    except Exception as e:
        print(f"Error calling insult API: {e}")
        return ""
        

async def generate_async_insult(chat_history: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, generate_insult, chat_history)