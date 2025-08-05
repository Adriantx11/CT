
from srca.configs import addCommand,Client
from db.mongo_client import MongoDB
from random import randrange


@addCommand('free')
async def bin(client, m):
    querY = MongoDB().query_user(int(m.from_user.id))
    if  querY == None: return await m.reply('Usar el comando $register para el registro.')
    
    if MongoDB().admin(int(m.from_user.id)) == False: return ...
    
    data = m.text.split(' ')
    
    if len(data) < 2: return await m.reply('ingrese datos correctos <code>$free id </code>')

    idw = int(data[1])

    MongoDB().delete_user_p(idw)

    texto= f'''<b>Le quito el premium

Name: {m.from_user.first_name}
id: {m.from_user.id}
Username: @{m.from_user.username}
━━━━━━━━
Aquitado el acceso premium
• id: <code>{idw}</code>
━━━━━━━━━━
</b>'''
    await client.send_message(chat_id=-1002726521405, text=texto)
    return await m.reply('El usuario ahora es free.')

