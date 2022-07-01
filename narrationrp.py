import discord
from conf import config as config
from handlers import command_inv as cmd_inv
from handlers import command_state as cmd_state
from handlers import guild_join as guild_join


class NarrationRP(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_guild_join(self, guild):
        if not self.get_guild(guild.id).me.guild_permissions.administrator:
            await self.user.leave_guild(guild)
            return
        await guild_join.on_join(self, guild)

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel == message.author.dm_channel:
            await guild_join.on_dm(self, message)
            return
        if not self.get_guild(message.guild.id).me.guild_permissions.administrator:
            return
        first_w = message.content.split(" ", 1)[0]
        if first_w in config.cmd_inv:
            await cmd_inv.on_command(self, message)
        elif first_w in config.cmd_state:
            await cmd_state.on_command(self, message)


if __name__ == "__main__":
    client = NarrationRP(intents=discord.Intents.all(),
                         activity=discord.Streaming(name='so long nerds', platform="YouTube", url=config.steaming_url,
                                                    twitch_name="some name"), status=discord.Status.online)
    client.run(config.token)
