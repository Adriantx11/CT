
from srca.configs import addCommand,Client
from db.mongo_client import MongoDB



@addCommand('removeg')
async def bin(client, m):
    querY = MongoDB().query_user(int(m.from_user.id))
    if  querY == None: return await m.reply('Usar el comando $register para el registro.')
    
    if MongoDB().admin(int(m.from_user.id)) == False: return ...
    
    data = m.text.split(' ')
    
    if len(data) < 2: return await m.reply('ingrese datos correctos <code>$removeg id </code>')

    idw = int(data[1])

    MongoDB().delete_chat(idw)

    texto= f'''<b>Removio un chat

Name: {m.from_user.first_name}
id: {m.from_user.id}
Username: @{m.from_user.username}
━━━━━━━━
Le quito el acceso a un chat 
• id: <code>{idw}</code>
━━━━━━━━━━
</b>'''
    await client.send_message(chat_id=-1002726521405, text=texto)
    return await m.reply('Grupo eliminado.')

