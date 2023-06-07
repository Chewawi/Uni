import asyncio
from core import Uni, Components

async def run_uni():
    async with Uni.Bot() as bot:
        await Uni.Database(bot)
        await bot.start()


def main():
    """Launches the bot."""
    with Components.logger():
        asyncio.run(run_uni())


if __name__ == "__main__":
    main()