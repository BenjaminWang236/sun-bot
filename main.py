# IMPORT DISCORD.PY. ALLOWS ACCESS TO DISCORD'S API.
import discord
import os
import time

# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
from discord.ext import commands
from datetime import date, datetime
from helper_functions.upgrade_cost import *
from helper_functions.keep_alive import *

# Loads the .env file that resides on the same level as the script.
load_dotenv()
default_prefixes = ['']
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=default_prefixes, intents=intents)
"""
liz_url = 'https://cdn.discordapp.com/emojis/807427398533775362.png?v=1'  # :wElizabeth:
din_url = 'https://cdn.discordapp.com/emojis/807443877886951436.png?v=1'  # :wDin:
ice_url = 'https://cdn.discordapp.com/emojis/807441258439507978.png?v=1'  # :zIceTower:
ta_url = 'https://cdn.discordapp.com/emojis/807446499516612688.png?v=1'  # :wArcher:
castle_url = 'https://cdn.discordapp.com/emojis/807448829732585532.png?v=1'  # :zCastle:
crystal_url='https://cdn.discordapp.com/emojis/784252518590578718.png?v=1'  # :zCrystal:
coins_url='https://cdn.discordapp.com/emojis/455521544068661248.png?v=1'    # :Coins:
coin_url='https://discord.com/assets/11b9d8164d204c7fd48a88a515745c1d.svg'  # :coin:
# :coin: is a Discord default Emoji, just use the literal ':coin:' in string
"""


def custom_embed(ctx, title, description, hero, castle, ta, base):
    embed = discord.Embed(
        title=title,
        description=description,
        url='https://repl.it/@Suntoria/sun-bot#main.py',
        color=0xFF5733,  #,color=Hex code
        timestamp=datetime.now())
    embed.set_author(
        name=ctx.author.display_name,
        url='https://www.youtube.com/channel/UCFod3BWeZwhg2W1kBi15-pA/featured',
        icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(
        url='https://media3.giphy.com/media/2ZYKKfCr0rkvvTkdum/source.gif')
    embed.add_field(name=f'{bot.get_emoji(807427398533775362)} Hero | ' +
                    f' {bot.get_emoji(807443877886951436)} Leader | ' +
                    f'{bot.get_emoji(807441258439507978)} Tower',
                    value=f':coin:\t_{hero:,}\tgold_',
                    inline=False)
    embed.add_field(name=f'{bot.get_emoji(807448829732585532)} Castle',
                    value=f':coin:\t_{castle:,}\tgold_',
                    inline=False)
    embed.add_field(name=f'{bot.get_emoji(807446499516612688)} Tower-Archer',
                    value=f':coin:\t_{ta:,}\tgold_',
                    inline=False)
    embed.add_field(
        name=f'{bot.get_emoji(807782825524330557)} Castle Piece/Base',
        value=f'_{bot.get_emoji(784252518590578718)}\t{base:,}\t crystals_',
        inline=False)
    # embed.set_image(url='https://i.giphy.com/media/13yNFN1TlNCjC0/200.gif')
    embed.set_footer(
        text=
        f'All types costs an extra 100 crystals at prestige (level {10000:,})\n'
        + 'by Suntoria#4680',
        icon_url=
        'https://static.wikia.nocookie.net/thegigaverse/images/6/66/Dark_soulz.jpg/revision/latest?cb=20190719081349'
    )
    return embed


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
        embed = custom_embed(
            ctx, '__GC Upgrade Cost__',
            f"Value difference between level {current_level:,} and level {target_level:,}",
            upgrade_cost_diff(current_level, target_level),
            upgrade_castle_diff(current_level, target_level),
            upgrade_TA_diff(current_level, target_level),
            upgrade_base_diff(current_level, target_level))
        await ctx.send(embed=embed)


@upgrade.command(
    name='total',
    help=
    '[target lvl] | Get the cost in gold to get from level 1 to target-level')
async def total_cost(ctx, target_level: int = 10000):
    embed = custom_embed(ctx, '__GC Total Value__',
                         f"Total value at level {target_level:,}",
                         upgrade_cost_total(target_level),
                         upgrade_castle_total(target_level),
                         upgrade_TA_total(target_level),
                         upgrade_base_total(target_level))
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")


def main():
    keep_alive()
    bot.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()
