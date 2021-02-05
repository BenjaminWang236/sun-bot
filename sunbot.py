# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
import os

# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
from discord.ext import commands

# Loads the .env file that resides on the same level as the script.
load_dotenv()

client = discord.Client()


@client.event
async def on_ready():
    """
    EVENT LISTENER FOR WHEN THE CLIENT/BOT HAS SWITCHED FROM OFFLINE TO ONLINE
    """
    guild_count = 0

    for guild in client.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count += 1

    print(f"Sun-client is in {guild_count} guilds.")


@client.event
async def on_message(message):
    """
    EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL
    """

    # Prevent client from recursively triggering itself
    if message.author == client.user:
        return

    # CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
    if message.content == "hello":
        # SENDS BACK A MESSAGE TO THE CHANNEL.
        await message.channel.send("PRAISE THE SUN!")
    elif message.content == "test-exception":
        await message.channel.send("ERROR!")
        raise discord.DiscordException

    print("client message send complete")


@client.event
async def on_error(event, *args, **kwargs):
    """
    EVENT LISTENER FOR DISCORD API'S "DiscordException"
    """
    with open(os.getenv("ERROR_FILE"), "a+") as f:
        if event == "on_message":
            f.write(f"Unhandled message: {args[0]}\n")
        else:
            raise Exception("Uncleared Error(s)")


# EXECUTES THE client WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
client.run(os.getenv("DISCORD_TOKEN"))
