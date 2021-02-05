# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
# import discord
import os

# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
from discord.ext import commands
from helper_functions.upgrade_cost import *

# Loads the .env file that resides on the same level as the script.
load_dotenv()

# client = discord.Client()
bot = commands.Bot(command_prefix="&")


@bot.event
async def on_ready():
    """
    EVENT LISTENER FOR WHEN THE CLIENT/BOT HAS SWITCHED FROM OFFLINE TO ONLINE
    """
    guild_count = 0

    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count += 1

    print(f"Sun-bot is in {guild_count} guilds.")


@bot.command(
    name="upcost",
    help="Calculate the Upgrade cost in gold from current level to target level",
)
# @commands.has_role("Admin")
async def upgrade_cost(ctx, current_level: int = 1, target_level: int = 10000):
    """
    Calculate the upgrade cost in gold to upgrade the hero/leader/tower from the
    current level to the desired target level
    """
    cost = upgrade_cost_calc(current_level, target_level)
    await ctx.send(f"Upgrade {current_level} -> {target_level} costs {cost:,} gold")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")


# @bot.event
# async def on_error(event, *args, **kwargs):
#     """
#     EVENT LISTENER FOR DISCORD API'S "discord.DiscordException"
#     """
#     with open(os.getenv("ERROR_FILE"), "a+") as f:
#         if event == "on_message":
#             f.write(f"Unhandled message: {args[0]}\n")
#         else:
#             raise Exception("Uncleared Error(s)")


def main():
    # EXECUTES THE bot WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
    bot.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
