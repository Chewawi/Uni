import discord
from discord.ext import commands
import os
import logging
import aiohttp
from .context import Context 
from .config import Config
from typing import Union
from cogwatch import watch
import i18n 

log = logging.getLogger('uni.bot')

# Jishaku Config
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

# i18n Config
i18n.load_path.append("./core/locales")
i18n.set("fallback", "en")
i18n.set("filename_format", "{namespace}.{format}")

description = """
Uni, the ultimate Discord bot for all your server needs. 
Maximize your server's potential with Uni's powerful commands and customizable features. 
Elevate your server experience with Uni, your all-in-one solution.
"""

def get_prefix(bot: commands.Bot, msg: discord.Message):
    user_id = bot.user.id
    base = [f"<@!{user_id}> ", f"<@{user_id}> "]
    if msg.guild is None:
        base.append("uni")
        base.append("?")
    else:
        base.extend(bot.prefixes.get(msg.guild.id, ["uni", "?"]))
    return base

class ProxyObject(discord.Object):
    def __init__(self, guild: discord.abc.Snowflake | None):
        super().__init__(id=0)
        self.guild: discord.abc.Snowflake | None = guild

class Bot(commands.Bot):
    def __init__(self):
        allowed_mentions = discord.AllowedMentions(
            roles=False, everyone=False, users=True
        )
        intents = discord.Intents(
            guilds=True,
            members=True,
            bans=True,
            emojis=True,
            voice_states=True,
            messages=True,
            reactions=True,
            message_content=True,
        )
        super().__init__(
            command_prefix=get_prefix,
            description=description,
            pm_help=None,
            help_attrs={"hidden": True},
            chunk_guilds_at_startup=False,
            heartbeat_timeout=150.0,
            allowed_mentions=allowed_mentions,
            intents=intents,
            enable_debug_events=True,
            strip_after_prefix=True,
            case_insensitive=True,
        )

    def __repr__(self):
        return '<Uni.Bot>'

    @watch(path='exts', default_logger=False)
    async def on_ready(self) -> None:
        if not hasattr(self, "uptime"):
            self.uptime = discord.utils.utcnow()
        print(' ')
        log.info("Ready: %s (ID: %s)", self.user, self.user.id)

    async def setup_hook(self) -> None:
        self.prefixes: Config[list[str]] = Config("prefixes.json")
        self.blacklist: Config[bool] = Config("blacklist.json")
        
        self.session = aiohttp.ClientSession()
        
        print(' ')
        for folder, _, files in os.walk('exts'):
            for filename in files:
                if filename.endswith(".py"):
                    cog_path = os.path.join(folder, filename)
                    cog_name = cog_path.replace(os.sep, ".")[:-3]
                    await self.load_extension(cog_name)
        print(' ')
        await self.load_extension('jishaku')

    async def get_context(
        self, origin: Union[discord.Interaction, discord.Message], /, *, cls=Context
    ) -> Context:
        return await super().get_context(origin, cls=cls)
        
    def get_guild_prefixes(
        self, guild: discord.abc.Snowflake | None, *, local_inject=get_prefix
    ) -> list[str]:
        proxy_msg = ProxyObject(guild)
        return local_inject(self, proxy_msg)  # type: ignore 

    def get_raw_guild_prefixes(self, guild_id: int) -> list[str]:
        _ = self.prefixes.get(guild_id, ["uni", "?"])
        return _

    async def set_guild_prefixes(
        self, guild: discord.abc.Snowflake, prefixes: list[str]
    ) -> None:
        if not prefixes:
            await self.prefixes.put(guild.id, [])
        elif len(prefixes) > 10:
            raise RuntimeError("Cannot have more than 10 custom prefixes.")
        else:
            await self.prefixes.put(guild.id, sorted(set(prefixes), reverse=True))

    async def add_to_blacklist(self, object_id: int):
        await self.blacklist.put(object_id, True)

    async def remove_from_blacklist(self, object_id: int):
        try:
            await self.blacklist.remove(object_id)
        except KeyError:
            pass

    async def close(self) -> None:
        await super().close()
        await self.session.close()

    async def start(self) -> None:
        await super().start(os.environ['UNI_TOKEN'], reconnect=True)
