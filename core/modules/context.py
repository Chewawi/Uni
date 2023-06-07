import discord
from discord.ext import commands
from typing import TYPE_CHECKING, Any, Union
import i18n
if TYPE_CHECKING:
    from aiohttp import ClientSession
    from .bot import Bot

class Context(commands.Context):
    channel: Union[
        discord.VoiceChannel, discord.TextChannel, discord.Thread, discord.DMChannel
    ]
    prefix: str
    command: commands.Command[Any, ..., Any]
    bot: 'Bot'
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
    def __repr__(self):
        return '<Uni.Context>'
        
    @property
    def lang(self) -> str:
        return 'es' # self.bot.get_lang(self.guild.id)

    @property
    def session(self) -> 'ClientSession':
        return self.bot.session

    def t(self, key: str, **kwargs) -> str:
        i18n.set("locale", self.lang)

        cmd = str(self.command.qualified_name).replace(" ", "_").lower()
        cog = self.cog.__cog_name__.lower()
        _key = key
        
        if len(key.split(".")) == 2:
            key = f"{cog}.{key}"
        elif len(key.split(".")) == 1:
            p = self.command.parent
            key = f"{cog}.{p.name if p else cmd}.{key}"

        _ = i18n.t(key, **kwargs).replace("\\n", chr(10))
        if _key == _:
            _ = ' '.join(key.split('.')).title()
            
        return _
