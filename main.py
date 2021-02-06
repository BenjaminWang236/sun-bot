# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
import os

# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
from discord.ext import commands
from helper_functions.upgrade_cost import *
from helper_functions.keep_alive import *

# Loads the .env file that resides on the same level as the script.
load_dotenv()
default_prefixes = ['']
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=default_prefixes, intents=intents)


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


Up_description = f'up cost [start lvl] [target lvl]\nup total [target lvl]'


@bot.group(name='up', help=Up_description, pass_context=True)
async def upgrade(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f'```{Up_description}```')


@upgrade.command(
    name='cost',
    help=
    '[start lvl] [target lvl] | Get the cost in gold needed to upgrade from the starting-level to target-level',
    pass_context=True)
async def upgrade_cost(ctx, current_level: int = 1, target_level: int = 10000):
    perimeter_status = verifyInputPerimeters(current_level, target_level)
    if error_code_table[perimeter_status] != 'OK':
        print(f"Error: {error_code_table[perimeter_status]}")
        await ctx.send(f"{error_code_table[perimeter_status]}")
    else:
        await ctx.send(
            f"Hero | Leader | Tower:\t{upgrade_cost_diff(current_level, target_level):,}\tgold\n"
            +
            f"Castle:\t\t\t\t\t\t\t\t{upgrade_castle_diff(current_level, target_level):,}\tgold\n"
            +
            f"Tower-Archer (TA):\t\t{upgrade_TA_diff(current_level, target_level):,}\tgold"
        )


@upgrade.command(
    name='total',
    help=
    '[target lvl] | Get the cost in gold to get from level 1 to target-level')
async def total_cost(ctx, target_level: int = 10000):
    await ctx.send(
        f"Hero | Leader | Tower:\t{upgrade_cost_total( target_level):,}\tgold\n"
        +
        f"Castle:\t\t\t\t\t\t\t\t{upgrade_castle_total( target_level):,}\tgold\n"
        + f"Tower-Archer (TA):\t\t{upgrade_TA_total( target_level):,}\tgold")


@bot.command(name='embed', help='testing Embedding')
async def embed(ctx):
    embed = discord.Embed(title="Your title here",
                          description="Your desc here",
                          url='https://repl.it/@Suntoria/sun-bot#main.py',
                          color=0xFF5733)  #,color=Hex code
    # embed.set_author(
    #     name='Suntoria',
    #     url='https://repl.it/@Suntoria',
    #     icon_url=
    #     'https://static.wikia.nocookie.net/thegigaverse/images/6/66/Dark_soulz.jpg/revision/latest/scale-to-width-down/884?cb=20190719081349'
    # )
    embed.set_author(name=ctx.author.display_name,
                     url='https://www.google.com',
                     icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(
        url=
        'https://static.wikia.nocookie.net/grow-castle/images/1/1f/Gold_Coin.png/revision/latest?cb=20180508232731'
    )
    embed.add_field(name='Hero | Leader | Tower',
                    value=f'{0}\tgold',
                    inline=False)
    embed.add_field(name='Castle',
                    value=f'{0}\tgold',
                    inline=False)
    embed.add_field(name='Tower-Archer',
                    value=f'{0}\tgold',
                    inline=False)
    # embed.add_field(name="Name",
    #                 value="you can make as much as fields you like to")
    # embed.set_footer(name="footer")  #if you like to
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")


def main():
    keep_alive()
    # EXECUTES THE bot WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
    bot.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
