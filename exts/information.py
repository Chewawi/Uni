from discord.ext import commands 

from core import Uni
    
class Information(Uni.Cog):
    def __init__(self, bot: 'Uni.Bot') -> None:
        self.bot = bot

    @commands.command()
    async def user(self, ctx: 'Uni.Context')  -> None:
        await ctx.send("Pong!")

async def setup(bot: 'Uni.Bot') -> None:
    await bot.add_cog(
        Information(bot)
    )
    