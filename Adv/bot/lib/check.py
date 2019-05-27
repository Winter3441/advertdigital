import discord, asyncio, aiosqlite
from discord.ext import commands
from time import time
from lib import embed

class checks:
    """a Module with all commands.check Instances"""

    async def user(ctx):
        return ctx.author.bot is False

    async def forbidden(ctx):
        try:
            if ctx.channel.permissions_for(ctx.guild.me).send_messages:
                return True
        except AttributeError: #<-- It is a DM
            await ctx.send(
                embed=embed.gen.idol(
                    f"{ctx.bot.user.mention} is not intended for DM-usage"
                )
            )

    def enabled(self):
        async def enabled_check(ctx):
            async with aiosqlite.connect(db) as cur:
                fetch = await cur.execute("Select ID from Guild WHERE ID=?",(ctx.message.channel.id,))
                result = await fetch.fetchone()
                if result:
                    return True
                await ctx.channel.send(embed=embed.gen.adbot("You have not set this channel to a Bump Channel!"))
        return commands.check(enabled_check)

    def vc(self):
        async def is_vc(ctx):
            if ctx.message.author.voice:
                return True
            await ctx.send(
                embed=embed.gen.idol(
                    f'Uh Oh, it does not seem like you are in a Voice Channel {ctx.author.name}!', discord.Colour.magenta()
                )
            )
        return commands.check(is_vc)

    def botvc(self):
        async def is_bot(ctx):
            if ctx.guild.voice_client:
                uvoice = ctx.author.voice.channel
                bvoice = ctx.guild.voice_client.channel
                if uvoice == bvoice:
                    return True
            await ctx.send(
                embed=embed.gen.idol(
                    f"Oops! I am not in the same Voice Channel as you {ctx.author.name}!", discord.Colour.magenta()
                )
            )
        return commands.check(is_bot)

    def cooldown(cooldown: int):
        async def cooldown_check(ctx):
            if ctx.author.id in user_bypass:
                return True
            try:
                LastUsed = time() \
                    - command_cooldown[ctx.command.name][ctx.author.id]
                if int(LastUsed) >= cooldown:
                    return True
                raise commands.CommandOnCooldown(
                    cooldown, cooldown - LastUsed)
            except KeyError:
                return True
        return commands.check(cooldown_check)