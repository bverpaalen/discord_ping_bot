import os
from discord.ext import commands
from utils.argparser import Parser


class everyone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.parser = Parser()
        self.env = os.getenv

    @commands.command()
    async def everyone(self, ctx):
        x = ctx.channel.members
        mentions = "PING PING "
        for member in x:
            mention = "<@" + str(member.id) + ">"
            mentions += mention + " "
        mentions += " PING PING PING"

        await ctx.message.channel.send(mentions)
        await self.ping_person(ctx, self.env("SYMEN_ID"))

    async def ping_person(self, ctx, person_id):
        await ctx.message.channel.send("<@"+str(person_id)+">")

    @commands.command()
    async def EVERYONE(self, ctx, amount=2):
        over_request = 0
        threshold = int(self.env("TAG_THRESHOLD"))
        if amount > threshold:
            over_request = amount - threshold
            amount = threshold

        for i in range(amount):
            await self.everyone(ctx)

        for i in range(over_request):
            await self.ping_person(ctx, ctx.message.author.id)

    @commands.command()
    async def SYMEN(self, ctx, amount=10):
        for i in range(amount):
            await self.ping_person(ctx, self.env("SYMEN_ID"))


def setup(bot):
    bot.add_cog(everyone(bot))