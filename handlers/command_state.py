import re

from utiles import datautile as data
from conf import config as config


async def on_command(bot, message):
    if not message.author.guild_permissions.administrator:
        return
    if len(message.content.split(" ", 1)) == 1:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    content = message.content.split(" ", 1)[1]
    args = await parseArgs(content)
    if args['id'] is None or args['state'] is None:
        return
    if args['state'] == config.sign_clear:
        await clear_states(bot, message, args)
        return
    if args['state'] == config.sign_get:
        await get_states(bot, message, args)
        return
    if args['operation'] is None:
        return
    if args['operation'] == config.sign_create:
        await add_state(bot, message, args)
        return
    if args['operation'] == config.sign_clear:
        await remove_state(bot, message, args)
        return


async def clear_states(bot, message, args):
    inv_message = await data.get_validate_messages(message.guild, args['id'])
    if inv_message is None or len(inv_message) == 0:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    for _message in inv_message:
        if _message is None:
            await message.add_reaction(bot.get_emoji(config.emoji_warn))
            continue
        content = await data.get_states(_message.content)
        inv_object = await data.strstate_to_objstate(content)
        inv_object.clear()
        inv_string = await data.objstate_to_strstate(inv_object)
        new_inv = await data.put_states(_message.content, inv_string)
        await data.edit_inventory(_message, new_inv[1:-1])


async def add_state(bot, message, args):
    inv_message = await data.get_validate_messages(message.guild, args['id'])
    if inv_message is None or len(inv_message) == 0:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    for _message in inv_message:
        if _message is None:
            await message.add_reaction(bot.get_emoji(config.emoji_warn))
            continue
        content = await data.get_states(_message.content)
        inv_object = await data.strstate_to_objstate(content)
        if '' in inv_object:
            del inv_object['']
        for _state in args['state'].split(","):
            inv_object[_state] = _state
        inv_string = await data.objstate_to_strstate(inv_object)
        new_inv = await data.put_states(_message.content, inv_string)
        await data.edit_inventory(_message, new_inv[1:-1])


async def remove_state(bot, message, args):
    inv_message = await data.get_validate_messages(message.guild, args['id'])
    if inv_message is None or len(inv_message) == 0:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    for _message in inv_message:
        if _message is None:
            await message.add_reaction(bot.get_emoji(config.emoji_warn))
            continue
        content = await data.get_states(_message.content)
        inv_object = await data.strstate_to_objstate(content)
        for _state in args['state'].split(","):
            if _state not in inv_object:
                await message.add_reaction(bot.get_emoji(config.emoji_warn))
                continue
            del inv_object[_state]
        inv_string = await data.objstate_to_strstate(inv_object)
        new_inv = await data.put_states(_message.content, inv_string)
        await data.edit_inventory(_message, new_inv[1:-1])


async def get_states(bot, message, args):
    inv_message = await data.get_validate_messages(message.guild, args['id'])
    if inv_message is None or len(inv_message) == 0:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    for _message in inv_message:
        if _message is None:
            await message.add_reaction(bot.get_emoji(config.emoji_warn))
            continue
        else:
            states = await data.get_states(_message.content)
            c_id = await data.get_id_from_inv(_message.content)
            await message.channel.send(f"**{c_id[0].upper()} — СОСТОЯНИЕ**```{states}```")


async def parseArgs(string):
    output = {
        "id": None,
        "state": None,
        "operation": None
    }
    args = re.findall(r"(?<=\()(.*?)(?=\))", string)
    count_of_args = len(args)
    if count_of_args > 0:
        output['id'] = args[0]
    if count_of_args > 1:
        output['state'] = args[1]
    if count_of_args > 2:
        output['operation'] = args[2]

    return output
