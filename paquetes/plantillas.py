from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup

def commd(user_id):
    commd = InlineKeyboardMarkup([
                                [
                                    InlineKeyboardButton(text='𝙋𝙚𝙧𝙛𝙞𝙡',callback_data=f'perfil:{user_id}'),
                                    InlineKeyboardButton(text='𝙂𝙖𝙩𝙚𝙒𝙖𝙮𝙨',callback_data=f'gates:{user_id}')
                                ],
                                [
                                    InlineKeyboardButton(text='𝙃𝙚𝙧𝙧𝙖𝙢𝙞𝙚𝙣𝙩𝙖𝙨',callback_data=f'tools:{user_id}')
                                ]
                            ])
    return commd


def atras(user_id):
    atras = InlineKeyboardMarkup([[InlineKeyboardButton(text='𝘼𝙩𝙧𝙖𝙨',callback_data=f'atras:{user_id}')]])
    return atras

perfil_text = '''<b>・ » 𝘾𝙏 𝘾𝙃𝙆| Perfil

<a href=\"https://t.me/\">＄</a> » id: <code>{}</code>
<a href=\"https://t.me/\">＄</a> » Username: @{}
<a href=\"https://t.me/\">＄</a> » Name: <i>{}</i> 
<a href=\"https://t.me/\">＄</a> » Creditos: {}
<a href=\"https://t.me/\">＄</a> » Rango: {}
<a href=\"https://t.me/\">＄</a> » Plan: <i>{}</i>
<a href=\"https://t.me/\">＄</a> » Antispam: {}</b>
'''