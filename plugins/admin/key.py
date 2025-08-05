from srca.configs import addCommand, Client
from db.mongo_client import MongoDB
from random import randrange
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@addCommand('key')
async def bin(client, m):
    try:
        querY = MongoDB().query_user(int(m.from_user.id))
        if querY is None:
            return await m.reply('Usar el comando $register para el registro.')
        
        if not MongoDB().admin(int(m.from_user.id)):
            return
        
        dias = m.text.split()
        
        if len(dias) < 2:
            return await m.reply('ingrese los dias.')

        keys1 = randrange(10000000)
        key = f'𝘾𝙏𝘾𝙃𝙆-{keys1}'

        text = f'''<b>
    [✅] 𝗞𝗲𝘆 𝗚𝗲𝗻𝗲𝗿𝗮𝗱𝗮
    ━━━━━━━━━━━━━━━━━━━━━ 
    • Key: <code>{key}</code>
    • <b>Dias Generados :</b> <code>{dias[1]}</code>
    ━━━━━━━━━━━━━━━━━━━━━ 
    • <b>Admin :</b> <a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a> [{querY["role"]}]</b>'''

        MongoDB().save_key(key, int(dias[1]), m.from_user.id)

        await m.reply(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Claim', url='https://t.me/CTCHKv1_bot')]
            ])
        )
        
        texto = f'''<b>New Key gen 

    Name: {m.from_user.first_name}
    id: {m.from_user.id}
    Username: @{m.from_user.username}
    ━━━━━━━━
    Ha generado una nueva key 
    • Key: <code>{key}</code>
    • <b>Dias Generados :</b> <code>{dias[1]}</code>
    ━━━━━━━━━━
    </b>'''
        
        await client.send_message(chat_id=-1002726521405, text=texto)
        
    except Exception as e:
        await m.reply(f'Error al generar la key: {e}')
            
                #Client.send_m(_,chat_id = '-1002125995809',text=f'<b><code>{m.from_user.first_name}| {m.from_user.id} a generado una key de {dias} Dias</code>.</b>')    
        

