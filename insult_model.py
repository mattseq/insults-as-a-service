from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto", torch_dtype="auto")
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
except Exception as e:
    print(f"Error loading model: {e}")
    generator = None

def generate_insult(chat_history: str) -> str:
    prompt = f"""<|system|>You are Insults as a Service, a sarcastic AI that roasts users in short, witty responses.</s>
    <|user|>{chat_history}</s>
    <|assistant|>"""

    output = generator(prompt, max_new_tokens=150, do_sample=True, temperature=0.95, top_p=0.9)
    return output[0]["generated_text"].split("<|assistant|>")[-1].strip()

import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

async def generate_async_insult(chat_history: str) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, generate_insult, chat_history)