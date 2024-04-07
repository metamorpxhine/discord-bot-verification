import os
import typing
import disnake as discord
from disnake.ext import commands 
from disnake.ui import Button, View, Select, Modal
from disnake import TextInputStyle
import config
from config import token

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents) 
bot.remove_command('help')

print("Starting...")

for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

@bot.listen()
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

bot.run(token)