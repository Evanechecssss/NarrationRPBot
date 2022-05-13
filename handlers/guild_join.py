from conf import config as config


async def on_join(bot, guild):
    channels = guild.text_channels
    if channels:
        channel = channels[0]
        await channel.send(await config.welcome_message(bot, guild.name))