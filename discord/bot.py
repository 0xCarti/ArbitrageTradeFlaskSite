# https://discord.com/api/oauth2/authorize?client_id=1064391470330695782&permissions=199680&scope=bot%20applications.commands
import os
import sqlite3
from datetime import datetime
import discord
from dotenv import load_dotenv
from discord.ext import commands

help_command = commands.DefaultHelpCommand(no_category='Commands')
intents = discord.Intents(message_content=True, typing=True, messages=True, members=True, guilds=True)
bot = commands.Bot(command_prefix='!', description='', intents=intents)


@bot.hybrid_command(name='trades', description='Spin and get a restaurant from the list.', with_app_command=True)
async def trades(ctx, amount: int = 5, minimum_price: int = 0):
    conn = sqlite3.connect('../watcher/database.db')
    c = conn.cursor()

    c.execute(f"SELECT * FROM sqltrade "
              f"WHERE profit >= {minimum_price} "
              f"ORDER BY id DESC "
              f"LIMIT {amount}")
    trades_list = c.fetchall()

    output = '```'
    for trade in trades_list:
        buy_trade = f'[{trade[2]}, {trade[3]}, {trade[4]:.3f} + {trade[5]:.5f}]'.center(40, ' ')
        sell_trade = f'[{trade[6]}, {trade[7]}, {trade[8]:.3f} + {trade[9]:.5f}]'.center(40, ' ')
        profit = f'[+{trade[10]:.2f} {trade[3][3:]}]'.rjust(15, ' ')
        output = f'{output}\n{trade[1]}\t{buy_trade} --> {sell_trade}{profit}'
    await ctx.reply(f'{output}\n\nCollected from https://trades.brycecotton.ca```')


@bot.event
async def on_ready():
    print('Connected to server:')
    for guild in bot.guilds:
        bot.tree.copy_global_to(guild=guild)
        cmds = await bot.tree.sync(guild=guild)
        print(f'\t{guild.name}-{guild.id}-[{len(cmds)}] Commands Copied')


@bot.event
async def on_guild_join(guild):
    print('Bot has connected to {} @ {}'.format(guild.name, datetime.now()))


load_dotenv('../.env')
bot.run(os.getenv('TOKEN'))
