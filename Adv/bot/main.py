import discord, traceback, aiosqlite, asyncio, random, aiohttp, sys, os, psutil, random, logging
from lib.config import token, db, defprefix
from datetime import datetime, timedelta
from lib.constant import prefix_dict
from lib import embed
from discord.ext import commands
from pathlib import Path

async def prefix_load(): #<-- Loads all Prefixes into the bot on-start
    async with aiosqlite.connect(db) as cur:
        await cur.execute('CREATE TABLE IF NOT EXISTS PrefixList(ID, Prefix)')
        await cur.execute("CREATE TABLE IF NOT EXISTS Donor(ID)")
        await cur.execute("CREATE TABLE IF NOT EXISTS Guild(ID)")
        IDQuery = await cur.execute('SELECT ID FROM PrefixList')
        ID = await IDQuery.fetchall()
        PrefixQuery = await cur.execute('SELECT Prefix FROM PrefixList')
        Prefix = await PrefixQuery.fetchall()
        for _ in range(len(ID)):
            prefix_dict[ID[_][0]] = Prefix[_][0]

async def get_prefix(bot, message): #<-- Allows Custom Prefixes to be Run
    try:
        return prefix_dict.get(message.guild.id, defprefix)
    except AttributeError:
        return defprefix

class Bot(commands.AutoShardedBot): #<-- Makes Cog more Cleanly and run Faster using UV

    async def load_cog(self): #<-- Loads all Bot Module in the Module Folder
        cog_dir = Path('./module')
        cog_dir.mkdir(exist_ok=True)
        for ex in cog_dir.iterdir():
            if ex.suffix == '.py':
                path = '.'.join(ex.with_suffix('').parts)
                bot.log.info(f'Loading: {path}')
                try:
                    bot.load_extension(path)
                except Exception:
                    bot.log.exception(
                        "Exception: %s `%s`:\n%s" % (
                            path,
                            ex.stem,
                            traceback.format_exc()
                        ))
        bot.log.info("Loading: Complete")

    async def on_command_completion(self,ctx):
        bot.log.info(f"Command: {ctx.author}({ctx.author.id}) - {ctx.message.content} - {datetime.now()}")

    async def on_ready(self): #<-- This is what the Bot does when it is ready to run
        bot.log.info(f"Login: {bot.user.name}({bot.user.id}) - {datetime.now()}")
        await prefix_load()
        await self.load_cog()

bot = Bot(command_prefix=get_prefix) #Generates Bot Object using UV (Makes it 2.4x Faster) through a custom Class

# Bot Logger #
bot.log = logging.getLogger('terminal')
bot.log.setLevel(logging.INFO)
bot.log.addHandler(
    logging.FileHandler(
        filename='logs/terminal.log', #<-- Log Name
        encoding='utf-8',
        mode='w'
    )
)

# Discord Logger#
bot.log.addHandler(logging.StreamHandler())
dpy_log = logging.getLogger('discord')
dpy_log.setLevel(logging.INFO)
dpy_log.addHandler(
    logging.FileHandler(
        filename='logs/discord.log', #<-- Log Name
        encoding='utf-8',
        mode='w'
    )
)
            

bot.run(token) #<-- Nothing should go under this Line. Anything under bot.run is not going to be Noticed by the Program