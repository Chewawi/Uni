from discord.ext import commands 

from core import Uni, Embed
import discord 

class Information(Uni.Cog):
    def __init__(self, bot: 'Uni.Bot') -> None:
        self.bot = bot

    @commands.command()
    async def user(self, ctx: 'Uni.Context', user: 'discord.User')  -> None:
        embed = Embed(ctx)
        embed.title = "User Info"
        embed.add_field(
            name="_ _ Username", value=f"`{user.name}`"
        )
        await ctx.send(embed=embed)

async def setup(bot: 'Uni.Bot') -> None:
    await bot.add_cog(
        Information(bot)
    )
    