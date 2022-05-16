import asyncio
import re

import discord

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
    if args['id'] is None:
        return
    if args['categoria'] == config.sign_create:
        await create_inventory(bot, message, args)
        return
    if args['categoria'] == config.sign_get:
        await get_inventory(bot, message, args)
        return
    if args['categoria'] == config.sign_clear:
        await del_inventory(bot, message, args)
        return
    if args['categoria'] is None:
        return
    if args['operation'] is None and args['item'] is not None:
        if args['item'] == config.sign_create:
            await add_categoria(bot, message, args)
            return
        if args['item'] == config.sign_clear:
            await del_categoria(bot, message, args)
            return
    if args['operation'] is not None and args['item'] is not None:
        if args['operation'] == config.sign_create:
            await plus_item(bot, message, args, 1, True,None)
            return
        if args['operation'] == config.sign_plus:
            await plus_item(bot, message, args, 1, False,None)
            return
        if args['operation'].find(config.sign_plus) != -1 and args['operation'] != config.sign_create:
            count = args['operation'].split(config.sign_plus, 1)[1]
            if count.isdigit():
                await plus_item(bot, message, args, int(count), False,None)
            return
        if args['operation'] == config.sign_minus:
            await plus_item(bot, message, args, -1, False,None)
            return
        if args['operation'] == config.sign_clear:
            await remove_item(bot, message, args)
            return
        if args['operation'].find(config.sign_minus) != -1 and args['operation'] != config.sign_clear:
            count = args['operation'].split(config.sign_minus, 1)[1]
            if count.isdigit():
                await plus_item(bot, message, args, int(count) * -1, False,None)
            return
        if args['operation'].isdigit():
            await plus_item(bot, message, args, int(args['operation']), True,None)
            return
        return
    if args['operation'] is None and args['item'] is None:
        return


async def create_inventory(bot, message, args):
    inv_channel = discord.utils.get(message.guild.channels, name=config.channel_inv)
    if inv_channel is None:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    for _id in args['id'].split(","):
        await inv_channel.send(await data.create_inv(_id, "- ", "- "))
    await message.add_reaction(bot.get_emoji(config.emoji_accept))


async def del_categoria(bot, message, args):
    inv_message = await data.get_validate_messages(message.guild, args['id'])
    if inv_message is None or len(inv_message) == 0:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    for _message in inv_message:
        if _message.content is None:
            await message.add_reaction(bot.get_emoji(config.emoji_warn))
            return
        content = await data.get_content(_message.content)
        inv_object = await data.strinv_to_objinv(content)
        for _categoria in args['categoria'].split(","):
            if _categoria not in inv_object:
                await message.add_reaction(bot.get_emoji(config.emoji_warn))
                continue
            del inv_object[_categoria]
        inv_string = await data.objinv_to_strinv(inv_object)
        new_inv = await data.put_content(_message.content, inv_string)
        await data.edit_inventory(_message, new_inv[1:-1])


async def add_categoria(bot, message, args):
    inv_message = await data.get_validate_messages(message.guild, args['id'])
    if inv_message is None or len(inv_message) == 0:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    for _message in inv_message:
        if _message.content is None:
            await message.add_reaction(bot.get_emoji(config.emoji_warn))
            return
        content = await data.get_content(_message.content)
        inv_object = await data.strinv_to_objinv(content)
        for _categoria in args['categoria'].split(","):
            inv_object[_categoria] = {"": None}
        inv_string = await data.objinv_to_strinv(inv_object)
        new_inv = await data.put_content(_message.content, inv_string)
        await data.edit_inventory(_message, new_inv[1:-1])


async def plus_item(bot, message, args, count, like_set, prepared):
    inv_message = await data.get_validate_messages(message.guild, args['id'])
    if inv_message is None or len(inv_message) == 0:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    for _message in inv_message:
        def check_value(_count, __categories, __item):
            if _count <= 0:
                del inv_object[__categories][__item]
            if _count == 1:
                inv_object[__categories][__item] = None
        if _message.content is None:
            await message.add_reaction(bot.get_emoji(config.emoji_warn))
            continue
        content = await data.get_content(_message.content)
        if prepared is None:
            inv_object = await data.strinv_to_objinv(content)
        else:
            inv_object = prepared
        for _categoria in args['categoria'].split(","):
            if _categoria not in inv_object:
                for __categoria in args['categoria'].split(","):
                    inv_object[__categoria] = {"": None}
                await plus_item(bot, message, args, count, like_set, inv_object)
                return
            for _item in args['item'].split(","):
                if _item not in inv_object[_categoria]:
                    for __categories in args['categoria'].split(","):
                        if __categories not in inv_object:
                            await message.add_reaction(bot.get_emoji(config.emoji_warn))
                            continue
                        if '' in inv_object[__categories]:
                            del inv_object[__categories]['']
                        for __item in args['item'].split(","):
                            inv_object[__categories][__item] = None
                    await plus_item(bot, message, args, count, like_set, inv_object)
                    return
                if inv_object[_categoria][_item] is None:
                    if like_set:
                        inv_object[_categoria][_item] = count
                        check_value(count, _categoria, _item)
                    else:
                        inv_object[_categoria][_item] = count + 1
                        check_value(count + 1, _categoria, _item)
                else:
                    if like_set:
                        inv_object[_categoria][_item] = str(count)
                        check_value(count, _categoria, _item)
                    else:
                        n_count = (count + int(inv_object[_categoria][_item]))
                        inv_object[_categoria][_item] = str(n_count)
                        check_value(n_count, _categoria, _item)
        inv_string = await data.objinv_to_strinv(inv_object)
        new_inv = await data.put_content(_message.content, inv_string)
        await data.edit_inventory(_message, new_inv[1:-1])


async def remove_item(bot, message, args):
    inv_message = await data.get_validate_messages(message.guild, args['id'])
    if inv_message is None or len(inv_message) == 0:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    for _message in inv_message:
        if _message.content is None:
            await message.add_reaction(bot.get_emoji(config.emoji_warn))
            return
        content = await data.get_content(_message.content)
        inv_object = await data.strinv_to_objinv(content)
        for _categories in args['categoria'].split(","):
            if _categories not in inv_object:
                await message.add_reaction(bot.get_emoji(config.emoji_warn))
                return
            for _item in args['item'].split(","):
                if _item in inv_object[_categories]:
                    del inv_object[_categories][_item]
        inv_string = await data.objinv_to_strinv(inv_object)
        new_inv = await data.put_content(_message.content, inv_string)
        await data.edit_inventory(_message, new_inv[1:-1])


async def del_inventory(bot, message, args):
    message1 = await data.get_validate_messages(message.guild, args['id'])
    if message1 is None or len(message1) == 0:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    for inv in message1:
        if inv is None:
            await message.add_reaction(bot.get_emoji(config.emoji_warn))
        else:
            await inv.delete()
    await message.add_reaction(bot.get_emoji(config.emoji_accept))


async def get_inventory(bot, message, args):
    invs = await data.get_validate_messages(message.guild, args['id'])
    if invs is None or len(invs) == 0:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    for inv in invs:
        if inv is None:
            await message.add_reaction(bot.get_emoji(config.emoji_warn))
        else:
            c_id = await data.get_id_from_inv(inv.content)
            inventory = await data.get_content(inv.content)
            await message.channel.send(f"**{c_id[0].upper()} — ИНВЕНТАРЬ**```{inventory}```")


async def parseArgs(string):
    output = {
        "id": None,
        "categoria": None,
        "item": None,
        "operation": None
    }
    args = re.findall(r"(?<=\()(.*?)(?=\))", string)
    count_of_args = len(args)
    if count_of_args > 0:
        output['id'] = args[0]
    if count_of_args > 1:
        output['categoria'] = args[1]
    if count_of_args > 2:
        output['item'] = args[2]
    if count_of_args > 3:
        output['operation'] = args[3]

    return output
