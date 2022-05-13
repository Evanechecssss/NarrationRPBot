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
    inv = await data.get_inv(message.guild, args['id'])
    if inv is None:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    message2 = await data.get_message(message.guild, args['id'])
    content = await data.get_states(inv)
    inv_object = await data.strstate_to_objstate(content)
    inv_object.clear()
    inv_string = await data.objstate_to_strstate(inv_object)
    new_inv = await data.put_states(inv, inv_string)
    await data.edit_inventory(message2, new_inv[1:-1])


async def add_state(bot, message, args):
    inv = await data.get_inv(message.guild, args['id'])
    if inv is None:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    message2 = await data.get_message(message.guild, args['id'])
    content = await data.get_states(inv)
    inv_object = await data.strstate_to_objstate(content)
    if '' in inv_object:
        del inv_object['']
    inv_object[args['state']] = args['state']
    inv_string = await data.objstate_to_strstate(inv_object)
    new_inv = await data.put_states(inv, inv_string)
    await data.edit_inventory(message2, new_inv[1:-1])


async def remove_state(bot, message, args):
    inv = await data.get_inv(message.guild, args['id'])
    if inv is None:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    message2 = await data.get_message(message.guild, args['id'])
    content = await data.get_states(inv)
    inv_object = await data.strstate_to_objstate(content)
    if args['state'] not in inv_object:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    del inv_object[args['state']]
    inv_string = await data.objstate_to_strstate(inv_object)
    new_inv = await data.put_states(inv, inv_string)
    await data.edit_inventory(message2, new_inv[1:-1])


async def get_states(bot, message, args):

    inv = await data.get_inv(message.guild, args['id'])
    if inv is None:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
    else:
        states = await data.get_states(inv)
        await message.channel.send(f"**{args['id'].upper()} — СОСТОЯНИЕ**```{states}```")


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
