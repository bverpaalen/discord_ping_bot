import os
from discord.ext import commands
from utils.argparser import Parser


class everyone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.parser = Parser()
        self.env = os.getenv
        self.admins = self.env("ADMINS")

    @commands.command()
    async def force_everyone(self, ctx):
        if str(ctx.message.author.id) in self.admins:
            mentions = "PING PING "

            x = ctx.channel.members
            for member in x:
                mention = "<@" + str(member.id) + ">"
                mentions += mention + " "
            mentions += " PING PING PING"

            await ctx.message.channel.send(mentions)
            await self.ping_person(ctx, self.env("SYMEN_ID"))
        else:
            await self.no_admin(ctx)

    async def no_admin(self, ctx):
        await ctx.message.channel.send("Dit mag jij helemaal niet gebruiken BOEF!")
        for i in range(int(self.env("RETURN_SPAM_THRESHOLD"))):
            await self.ping_person(ctx, ctx.message.author.id)

    @commands.command()
    async def everyone(self, ctx):
        x = ctx.channel.members
        no_ping = self.env("NO_PING")
        mentions = "PING PING "
        for member in x:
            if str(member.id) not in no_ping:
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

    @commands.command()
    async def add_no_ping(self, ctx):
        no_ping_list = self.env("NO_PING")[1:-1].split(",")
        if str(ctx.message.author.id) not in no_ping_list:
            no_ping_list.append(str(ctx.message.author.id))
            write_list = "["

            for id in no_ping_list:
                write_list += str(id) + ","
            write_list = write_list[:-1] + "]"

            os.environ["NO_PING"] = str(write_list)


def setup(bot):
    bot.add_cog(everyone(bot))