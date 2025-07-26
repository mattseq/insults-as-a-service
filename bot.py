import os
import discord
import random
from insult_model import generate_async_insult
from chat_memory import ChatMemory
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

memory = ChatMemory(max_len=6)

@client.event
async def on_ready():
    print(f"Bot ready as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    memory.add_message(message.author.display_name, message.content)

    # chance to reply with an insult
    if random.random() < 1.00:
        history = memory.get_formatted_history()
        try:
            insult = await generate_async_insult(history)
            await message.channel.send(insult)
        except Exception as e:
            print(f"Error generating insult: {e}")

client.run(TOKEN)