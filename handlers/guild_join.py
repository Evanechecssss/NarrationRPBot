from conf import config as config


async def on_join(bot, guild):
    channels = guild.text_channels
    if channels:
        for channel in channels:
            if channel.name == config.channel_hello:
                await channel.send(await config.welcome_message(bot, guild.name))
                return
        channel = channels[0]
        await channel.send(await config.welcome_message(bot, guild.name))