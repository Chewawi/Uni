from discord.ext import commands 

from core import Uni
    
class Utility(Uni.Cog):
    def __init__(self, bot: 'Uni.Bot') -> None:
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: 'Uni.Context')  -> None:
        await ctx.send("Pong!")

async def setup(bot: 'Uni.Bot') -> None:
    await bot.add_cog(
        Utility(bot)
    )
