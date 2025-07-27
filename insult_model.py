from llama_cpp import Llama

try:
    llm = Llama(model_path="models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf", n_ctx=2048, n_threads=8, verbose=False)
except Exception as e:
    print(f"Error loading model: {e}")
    generator = None

def generate_insult(chat_history: str) -> str:
    prompt = f"""You are a sarcastic AI that responds to user input with short, witty roasts. No greetings. No explanations.

    Users' messages: "{chat_history}"
    Roast:"""

    output = llm(prompt, max_tokens=100, stop=["</s>"])
    return output["choices"][0]["text"].strip()

import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

async def generate_async_insult(chat_history: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, generate_insult, chat_history)