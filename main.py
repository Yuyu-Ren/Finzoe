# Base requirements
import discord
from discord.ext import commands
import asyncio

# Logging
import logging

# Token
import os
# Based on Marlet for McGill University

# List the modules that should be loaded on startup.
startup= ["birthday", "timezone"]

bot=commands.Bot(command_prefix='?', case_insensitive=True)
logging.basicConfig(level=logging.INFO)

@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower() == "dammit lykai":
        await message.channel.send(":c")
    if message.content.lower() == "owo":
        await message.channel.send("What's this?")
    if message.content.lower() == "ono":
        await message.channel.send("What's wrong?")
    await bot.process_commands(message)


if __name__=="__main__":
    for extension in startup:
        try:
            bot.load_extension(extension)
        except Exception as e:
           print("Whoops, couldn't load {} due to '{}'".format(extension, e))
           pass
    bot.run(os.environ.get("DISCORD_TOKEN"))
