import os

import discord
from dotenv import load_dotenv
from utils.data import Bot, HelpFormat

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.members = True

bot = Bot(
    command_prefix=os.getenv("PREFIX"),
    prefix=os.getenv("PREFIX"),
    command_attrs=dict(hidden=True),
    help_command=HelpFormat(),
    intents=intents
)

for file in os.listdir("commands"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"commands.{name}")

try:
    bot.run(TOKEN)
except Exception as e:
    print(f'Error when logging in: {e}')