token = 'OTczMjE5Njg5MTM0MTk0NzY4.Ynkbdw.oZ-IYCYChkRmKT3S7hWGEVdr9W0'
steaming_url = "https://www.youtube.com/watch?v=j-jUOwAIj5o"
sign_plus = "+"
sign_minus = "-"
sign_clear = "--"
sign_all = "*все"
channel_inv = "инвентари"
channel_hello = "чат"
sign_create = "++"
sign_get = "=="
cmd_inv = ["!инв", "!inv"]
cmd_state = ["!стат", "!state"]
emoji_warn = 974728703017889903
emoji_accept = 974728682037968918
emoji_load = 974728375472103484
emoji_hello = 974728692909633576
emoji_love = 974728714170544168


async def welcome_message(bot, name):
    return f"{str(bot.get_emoji(emoji_load))} *Загрузка соображалки* {str(bot.get_emoji(emoji_load))}\n\nХэллов, " \
           f"фриендс, я Гаечка, мг, встречайте! {str(bot.get_emoji(emoji_hello))}\nРада видеть вас на сервере {name}:]\nЖлаю удачного рп!!! {str(bot.get_emoji(emoji_love))}"
