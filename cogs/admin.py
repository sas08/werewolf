import discord
from discord.ext import commands

from lib.instant import Instant
from lib.player import Players



class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.instant = Instant(bot)
        self.players = Players()


    @commands.command()
    async def status(self,ctx):
        await ctx.send(self.bot.system.status)

    @commands.command()
    async def players(self,ctx):
        await ctx.send(self.bot.system.players)

    @commands.command()
    async def guild(self,ctx):
        await ctx.send(self.bot.system.guild)


def setup(bot):
    bot.add_cog(Admin(bot))
