from discord.ext import commands
from termcolor import colored
import logging
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .context import Context
    from .bot import Bot
    
log = logging.getLogger('uni.cog')

class Cog(commands.Cog):
    def __init__(self, bot: 'Bot'):
        self.bot = bot

    def __repr__(self):
        return '<Uni.Cog>'
        
    def cog_check(self, ctx: 'Context'):
        return True

    def cog_command_error(self, ctx, error):
        ...

    def cog_load(self):
        log.info('Loaded cog: %s', colored(f"{self.__class__.__name__.upper()}", "green", attrs=['bold']))

    def cog_unload(self):
        log.info('Unloaded cog: %s', colored(f"{self.__class__.__name__.upper()}", "green", attrs=['bold']))