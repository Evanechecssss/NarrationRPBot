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


async def on_dm(bot, message):
    channel = message.channel
    author = message.author
    await channel.send(f"{author.name.mention}, зачем ты мне пишешь? Нас ниче не связывает.")
