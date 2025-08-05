from srca.configs import addCommand,Client
from db.mongo_client import MongoDB
from random import randrange


@addCommand('creditos')
async def bin(_,m):
    querY = MongoDB().query_user(int(m.from_user.id))
    if  querY == None: return await m.reply('Usar el comando $register para el registro.')
    
    if MongoDB().admin(int(m.from_user.id)) == False: return ...
    
    data = m.text.split(' ')
    
    if len(data) < 3: return await m.reply('ingrese datos correctos <code>$creditos id numero</code>')

    idw = int(data[1])
    dias = int(data[2])
    
    MongoDB().add_crdits(idw,dias)
    await m.reply('se ha editado los creditos  de un  usuraio✅')

    texto= f'''<b>Ha Usado el antispam

Name: {m.from_user.first_name}
id: {m.from_user.id}
Username: @{m.from_user.username}
━━━━━━━━
Ha editado los creditos
• Id: <code>{idw}</code>
• <b>creditos :</b> <code>{dias}</code>
━━━━━━━━━━
</b>'''
    await Client.send_message(_,chat_id=-1002726521405 ,text=texto)