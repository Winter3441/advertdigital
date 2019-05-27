import discord, traceback, aiosqlite, asyncio, random, aiohttp, sys, os, psutil, random, logging
from lib.config import token, db, defprefix
from datetime import datetime, timedelta
from lib.constant import prefix_dict
from lib import embed, check
from discord.ext import commands
from pathlib import Path

class adbot():

    def __init__(self, bot):
        self.bot = bot

    async def untuple(self, fetch):
        """Turns all Tuples into Lists

            Works with Fetchone and Fetchall
        """
        result = None
        for item in fetch:
            append = []
            for item in item:
                append.append(item)
            result = append
        return result

    async def on_command_error(self,ctx,error):
        if hasattr(ctx.command, 'on_error'):
            return
        
        ignored = (commands.CommandNotFound, commands.UserInputError)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(embed=embed.gen.adbot("You must wait {} seconds before doing that again.".format(int(error.retry_after))))

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    @commands.command(ignore_extra=False,description="Adds or Removes a Channel from the AdBot List\n",brief="Usage: ///channel add OR ///channel remove")
    async def channel(self, ctx, option):
        if option.lower() == "add":
            async with aiosqlite.connect(db) as cur:
                fetch = await cur.execute("Select ID from Guild WHERE ID=?",(ctx.message.channel.id,))
                result = await fetch.fetchone()
                if result:
                    return await ctx.send(
                        embed=embed.gen.adbot(
                            "Uh Oh, it looks like this channel has already been added to the Ad Bot!"
                        )
                    )
                await cur.execute("INSERT INTO Guild(ID) VALUES(?)",(ctx.message.channel.id,))
                await cur.commit()
                await ctx.send(embed=embed.gen.adbot("Success!"))
        elif option.lower() == "remove":
            async with aiosqlite.connect(db) as cur:
                fetch = await cur.execute("Select ID from Guild WHERE ID=?",(ctx.message.channel.id,))
                result = await fetch.fetchone()
                if not result:
                    return await ctx.send(
                        embed=embed.gen.adbot(
                            "Uh Oh, it looks like this channel is not already in the ad bot!"
                        )
                    )
                await cur.execute("DELETE FROM Guild WHERE ID=?",(ctx.channel.id,))
                await cur.commit()
                await ctx.send(embed=embed.gen.adbot("Success!"))
        else:
            await ctx.send(
                embed=embed.gen.adbot(
                    "Invalid Option! Please Select `Add` or `Remove`"
                )
            )

    @commands.command(ignore_extra=False,description="Bumps your Server!\n",brief="Usage: ///bump <url>")
    @commands.check(check.checks.enabled)
    @commands.cooldown(1,3600, commands.BucketType.user)
    async def bump(self, ctx, url:discord.Invite):
        def check(m):
            return len(m.content) < 64 and m.author.id == ctx.author.id
        #Check if link is valid
        async with aiosqlite.connect(db) as cur:
            fetch = await cur.execute("SELECT * FROM Guild")
            result = await self.untuple(await fetch.fetchall())
            print(result)
        await ctx.send(
            embed=embed.gen.adbot(
                "Post a Nice Description about your Server Here! (64 Character Limit)"
            )
        )
        try:
            description = await self.bot.wait_for('message', check=check, timeout=5000)
        except asyncio.TimeoutError:
            await ctx.send(embed=embed.gen.adbot("Command Timed Out, Please Try Again."))
        for _ in result:
            mes = self.bot.get_channel(_)
            await mes.send(
                embed=embed.gen.adbot(
                    f"{url}\n\n{description.content}"
                    )
                )

    def donator():
        async def donor(ctx):
            async with aiosqlite.connect(db) as cur:
                checkuser = await cur.execute("Select ID from Donor WHERE ID=?",(ctx.author.id,))
                checkdonor = await checkuser.fetchone()
                if not checkdonor:
                    await ctx.send(embed=embed.gen.adbot("Sorry, you are not a Donator! Please try Again"))
                    return False
                return True
        return commands.check(donor)

    @commands.command(ignore_extra=False,description="Adds a Donor (Owner Only)",brief="\nUsage: ///donroadd <user>")
    @commands.is_owner()
    async def donoradd(self, ctx, user:discord.Member):
        async with aiosqlite.connect(db) as cur:
            fetch = await cur.execute("Select ID from Donor WHERE ID=?",(user.id,))
            result = await fetch.fetchone()
            if result:
                return await ctx.send(
                    embed=embed.gen.adbot(
                        "Uh Oh, it looks like this Donator has already been added to the Ad Bot!"
                    )
                )
            await cur.execute("INSERT INTO Donor(ID) VALUES(?)",(user.id,))
            await cur.commit()
            await ctx.send(embed=embed.gen.adbot("Success!"))

    @commands.command(ignore_extra=False,description="Bumps your Server! (Donator Only)",brief="\nUsage: ///premiumbump <url>")
    @commands.check(donator)
    @commands.check(check.checks.enabled)
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def premiumbump(self, ctx, url:discord.Invite):
        def check(m):
            return m.author.id == ctx.author.id
        #Check if link is valid
        async with aiosqlite.connect(db) as cur:
            fetch = await cur.execute("SELECT * FROM Guild")
            result = await self.untuple(await fetch.fetchall())
        await ctx.send(
            embed=embed.gen.adbot(
                "Post a Nice Description about your Server Here!"
            )
        )
        try:
            description = await self.bot.wait_for('message', check=check, timeout=5000)
        except asyncio.TimeoutError:
            await ctx.send(embed=embed.gen.adbot("Command Timed Out, Please Try Again."))
        for _ in result:
            mes = self.bot.get_channel(_)
            await mes.send(
                embed=embed.gen.adbot(
                    f"{url}\n\n{description.content}"
                    )
                )

def setup(bot):
    bot.add_cog(adbot(bot))