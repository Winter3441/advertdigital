import discord, traceback, aiosqlite, asyncio, sqlite3, random, re, difflib, json, requests
from datetime import datetime, timedelta
from discord.ext import commands
from time import time
from lib import embed, config

button = ['⏪', '⬅', '➡', '⏩', '⏹']

class help:
    """A Cog with a Custom Help System"""

    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        self.bot.remove_command('help')

    async def remote(self, ctx, commandlist, reaction="⏪"): #L R L R STOP & DASH & UP & TALK B B A B S(tart)
        def controller(reaction, user):
            if str(reaction.emoji) in button and user.id == ctx.author.id and reaction.message.id == msg.id:
                return True
        page = 0
        msg = await ctx.send(
            embed=embed.gen.adbot(
                f"  ***{commandlist[page].name}***\n{commandlist[page].description}\n\n`{commandlist[page].brief.replace('///', ctx.prefix)}`"
            )
        )
        for emoji in button:
            await msg.add_reaction(emoji)
        while reaction != '⏹':
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=15, check=controller)
            except asyncio.TimeoutError:
                break
            if str(reaction.emoji) == '⏪':
                page = 0
            elif str(reaction.emoji) == '⬅':
                page -= 1
            elif str(reaction.emoji) == '➡':
                page += 1
            elif str(reaction.emoji) == '⏩':
                page = len(commandlist)-1
            else:
                break
            if page == len(commandlist):
                page = 0
            elif page < 0:
                page = len(commandlist)-1
            await msg.edit(
                embed=embed.gen.adbot(
                    f"  ***{commandlist[page].name}***\n{commandlist[page].description}\n\n`{commandlist[page].brief.replace('///', ctx.prefix)}`"
                    )
                )
        await msg.edit(
            embed=embed.gen.adbot(
                f"  ***{commandlist[page].name}***\n{commandlist[page].description}\n\n{commandlist[page].brief.replace('///', ctx.prefix)}"
            ).set_footer(
                text=f"Oh No! The Help Session Ended. Use {ctx.prefix}help again to create a new Session"
            )
        )
        return None
        

    @commands.command(
        hidden=True,
        description="Default Help System",
        brief='`///help [module-name]`')
    async def help(self, ctx, cog=None):
        try:
            Prefix = self.bot.prefix_dict.get(ctx.message.guild.id, ".")
        except:
            Prefix = '.'
        if cog == None:
            await ctx.send(
                embed=embed.gen.adbot(
                    "__**AdBot**__\nThe Primary cog of Adbot, You can Bump Servers, Remove and Add Notification Channels, and More!"
                ).set_footer(
                    text=f'Want more information about a specific module? Use {Prefix}help followed by its module Name!'
                    )
            )
        else:
            if cog.lower() in self.bot.cogs:
                Var = list(self.bot.get_cog_commands(cog))
                DefaultCog = ''
                VarSubCMD = []
                for item in Var:
                    try:
                        for sub in list(item.commands):
                            Var.append(sub)
                    except AttributeError:
                        pass
                await self.remote(ctx, Var)
            else:
                coglist = list(self.bot.cogs)
                ValidCog = ""
                for item in coglist:
                    ValidCog += f'{item} \n'
                await ctx.send(
                    embed=embed.gen.adbot(
                        f"***Sorry! But it looks like {cog} is not a Valid Module. Here is a Valid List of Modules***\n```{ValidCog}```"
                    )
                )

def setup(bot):
    bot.add_cog(help(bot))