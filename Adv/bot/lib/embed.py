import discord

class gen:

    def censor(author, color=discord.Colour.red(), text:str=None):
        return discord.Embed(
            color=color, description=text).set_author(
                name=f"{author.name} - Censor", icon_url=author.avatar_url).set_footer(
                    text="This message has been censored due to a part of it being in our Censor Database"
                    )

    def adbot(text: str=None, color=discord.Colour.blue()): #Tessa Example-Embed Generator
        return discord.Embed(
            color=color, description=text).set_author(
                name="BumpBot", icon_url="" #PutURL
                ) #Generates a Embed with the Specified Description, and a pre set Author Profile.