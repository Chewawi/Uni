import datetime

import discord 
import typing 

if typing.TYPE_CHECKING:
    from ..modules.context import Context 

class Embed(discord.Embed):
    def __init__(self, ctx: 'Context' = None, **kwargs):
        super().__init__(
            color=kwargs.get('color', discord.Color.dark_embed()),
            timestamp=discord.utils.utcnow(),
            **kwargs
        )

        if ctx:
            self.set_author(
                name=str(ctx.author),
                icon_url=ctx.author.display_avatar.url,
            )
            
        self.set_footer(
            text="© UniBot",
            icon_url=ctx.bot.user.display_avatar.url if ctx else None
        )
    