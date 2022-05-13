import discord
import re


async def get_channel(guild):
    return discord.utils.get(guild.channels, name="инвентари")


async def get_invs(guild):
    channel = discord.utils.get(guild.channels, name="инвентари")
    if channel == None:
        return None
    messages = await channel.history(limit=200).flatten()
    return messages


async def edit_inventory(inv, new_inventory):
    await inv.edit(content=new_inventory)


async def get_message(guild, id):
    invs = await get_invs(guild)
    if invs is None:
        return None
    for i in range(len(invs)):
        content = invs[i].content
        c_id = await get_id_from_inv(content)
        if len(c_id) == 0:
            continue
        if id.lower() == c_id[0].lower():
            return invs[i]
    return None


async def get_inv(guild, id):
    inv = await get_message(guild, id)
    if inv is None:
        return None
    else:
        return inv.content


async def get_id_from_inv(content):
    return re.findall(r'📦\s([^<>]+)\s📦', content)


async def get_content(inv):
    return (re.findall(r"```([^<>]+)```.n", repr(inv))[0]).replace("\\n", "\n")


async def put_content(inv, content):
    c = re.sub(r"(?<=```)(.*?)(?=```.n)", content, repr(inv))
    return c.replace("\\n", "\n")


async def get_states(inv):
    return (re.findall(r"(?<=СОСТОЯНИЕ\*\*```)(.*?)(?=```)", repr(inv))[0]).replace("\\n", "\n")


async def put_states(inv, content):
    c = re.sub(r"(?<=СОСТОЯНИЕ\*\*```)(.*?)(?=```)", content, repr(inv))
    return c.replace("\\n", "\n")


async def create_inv(id, items, states):
    return f"**📦 {id.upper()} 📦**\n\n**ВЕЩИ**```{items}```\n**СОСТОЯНИЕ**```{states}```"


async def strinv_to_objinv(string):
    output_object = {}
    raw_categories = string.split("\n\n")
    if string == "- ":
        return output_object
    for index in range(len(raw_categories)):
        items = raw_categories[index].split("\n", 1)[1].split("\n")
        categoria = raw_categories[index].split("\n")[0].replace(":", "")
        output_object[categoria] = {}
        for item_index in range(len(items)):
            raw_item = items[item_index].replace("- ", "", 1)
            m_item = re.sub(r".\([^)]+\)", "", raw_item)
            item = re.findall(r"(?<=\()(.*?)(?=\))", raw_item)
            if len(item) == 0:
                output_object[categoria][m_item] = None
            else:
                item = item[len(item) - 1]
                output_object[categoria][m_item] = item
    return output_object


async def objinv_to_strinv(objecte):
    output_string = ""
    for key in objecte:
        output_string = output_string + f"{key}:"
        for item in objecte[key]:
            count = objecte[key][item]
            if count is None:
                output_string = output_string + f"\n- {item}"
            else:
                count = f"({count})"
                output_string = output_string + f"\n- {item} {count}"
        if len(objecte[key]) == 0:
            output_string = output_string + f"\n- "
        if list(objecte.keys())[-1].lower() != key.lower():
            output_string = output_string + "\n\n"
    if len(objecte.keys()) == 0:
        output_string = "- "
    return output_string


async def strstate_to_objstate(string):
    output_object = {}
    items = string.split("\n")
    for item_index in range(len(items)):
        raw_item = items[item_index].replace("- ", "", 1)
        output_object[raw_item] = raw_item
    return output_object


async def objstate_to_strstate(objecte):
    output_string = ""
    for item in objecte:
        if list(objecte.keys())[0].lower() == item.lower():
            output_string = output_string + f"- {item}"
        else:
            output_string = output_string + f"\n- {item}"
    if len(objecte.keys()) == 0:
        output_string = "- "
    return output_string
