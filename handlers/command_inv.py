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
            await add_item(bot, message, args)
            return
        if args['operation'] == config.sign_plus:
            await plus_item(bot, message, args, 1, False)
            return
        if args['operation'].find(config.sign_plus) != -1 and args['operation'] != config.sign_create:
            count = args['operation'].split(config.sign_plus, 1)[1]
            if count.isdigit():
                await plus_item(bot, message, args, int(count), False)
            return
        if args['operation'] == config.sign_minus:
            await plus_item(bot, message, args, -1, False)
            return
        if args['operation'] == config.sign_clear:
            await remove_item(bot, message, args)
            return
        if args['operation'].find(config.sign_minus) != -1 and args['operation'] != config.sign_clear:
            count = args['operation'].split(config.sign_minus, 1)[1]
            if count.isdigit():
                await plus_item(bot, message, args, int(count) * -1, False)
            return
        if args['operation'].isdigit():
            await plus_item(bot, message, args, int(args['operation']), True)
            return
        return
    if args['operation'] is None and args['item'] is None:
        return


async def create_inventory(bot, message, args):
    inv_channel = await data.get_channel(message.guild)
    if inv_channel is None:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    await inv_channel.send(await data.create_inv(args["id"], "- ", "- "))
    await message.add_reaction(bot.get_emoji(config.emoji_accept))


async def del_categoria(bot, message, args):
    inv = await data.get_inv(message.guild, args['id'])
    if inv is None:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    message2 = await data.get_message(message.guild, args['id'])
    content = await data.get_content(inv)
    inv_object = await data.strinv_to_objinv(content)
    if args['categoria'] not in inv_object:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    del inv_object[args['categoria']]
    inv_string = await data.objinv_to_strinv(inv_object)
    new_inv = await data.put_content(inv, inv_string)
    await data.edit_inventory(message2, new_inv[1:-1])


async def add_categoria(bot, message, args):
    inv = await data.get_inv(message.guild, args['id'])
    if inv is None:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    message2 = await data.get_message(message.guild, args['id'])
    content = await data.get_content(inv)
    inv_object = await data.strinv_to_objinv(content)
    inv_object[args['categoria']] = {"": None}
    inv_string = await data.objinv_to_strinv(inv_object)
    new_inv = await data.put_content(inv, inv_string)
    await data.edit_inventory(message2, new_inv[1:-1])


async def plus_item(bot, message, args, count, like_set):
    def check_value(_count):
        if _count <= 0:
            del inv_object[args['categoria']][args['item']]
        if _count == 1:
            inv_object[args['categoria']][args['item']] = None

    inv = await data.get_inv(message.guild, args['id'])
    if inv is None:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    message2 = await data.get_message(message.guild, args['id'])
    content = await data.get_content(inv)
    inv_object = await data.strinv_to_objinv(content)
    if args['categoria'] not in inv_object:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    if args['item'] not in inv_object[args['categoria']]:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return

    if inv_object[args['categoria']][args['item']] is None:
        if like_set:
            inv_object[args['categoria']][args['item']] = count
            check_value(count)
        else:
            inv_object[args['categoria']][args['item']] = count + 1
            check_value(count + 1)
    else:
        if like_set:
            inv_object[args['categoria']][args['item']] = str(count)
            check_value(count)
        else:
            n_count = (count + int(inv_object[args['categoria']][args['item']]))
            inv_object[args['categoria']][args['item']] = str(n_count)
            check_value(n_count)
    inv_string = await data.objinv_to_strinv(inv_object)
    new_inv = await data.put_content(inv, inv_string)
    await data.edit_inventory(message2, new_inv[1:-1])


async def remove_item(bot, message, args):
    inv = await data.get_inv(message.guild, args['id'])
    if inv is None:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    message2 = await data.get_message(message.guild, args['id'])
    content = await data.get_content(inv)
    inv_object = await data.strinv_to_objinv(content)
    if args['categoria'] not in inv_object:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    if args['item'] in inv_object[args['categoria']]:
        del inv_object[args['categoria']][args['item']]
    inv_string = await data.objinv_to_strinv(inv_object)
    new_inv = await data.put_content(inv, inv_string)
    await data.edit_inventory(message2, new_inv[1:-1])


async def add_item(bot, message, args):
    inv = await data.get_inv(message.guild, args['id'])
    if inv is None:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    message2 = await data.get_message(message.guild, args['id'])
    content = await data.get_content(inv)
    inv_object = await data.strinv_to_objinv(content)
    if args['categoria'] not in inv_object:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
        return
    if '' in inv_object[args['categoria']]:
        del inv_object[args['categoria']]['']
    inv_object[args['categoria']][args['item']] = None
    inv_string = await data.objinv_to_strinv(inv_object)
    new_inv = await data.put_content(inv, inv_string)
    await data.edit_inventory(message2, new_inv[1:-1])


async def del_inventory(bot, message, args):
    message1 = await data.get_message(message.guild, args['id'])
    await message1.delete()
    await message.add_reaction(bot.get_emoji(config.emoji_accept))


async def get_inventory(bot, message, args):
    inv = await data.get_inv(message.guild, args['id'])
    if inv is None:
        await message.add_reaction(bot.get_emoji(config.emoji_warn))
    else:
        await message.channel.send(inv)


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
