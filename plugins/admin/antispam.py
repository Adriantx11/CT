from srca.configs import addCommand,Client
from db.mongo_client import MongoDB
from random import randrange
from pyrogram.errors import PeerIdInvalid, ChatWriteForbidden


@addCommand('antispam')
async def bin(_,m):
    querY = MongoDB().query_user(int(m.from_user.id))
    if  querY == None: 
        await m.reply('Usar el comando $register para el registro.')
        return
    
    if MongoDB().admin(int(m.from_user.id)) == False: 
        return ...
    
    data = m.text.split(' ')
    
    if len(data) < 3: 
        await m.reply('ingrese datos correctos <code>$antispam id antispam</code>')
        return

    idw = int(data[1])
    dias = int(data[2])
    
    MongoDB().add_antispam(idw,dias)
    await m.reply('se ha editado el antidpam del usuraio✅')

    texto= f'''<b>Ha Usado el antispam

Name: {m.from_user.first_name}
id: {m.from_user.id}
Username: @{m.from_user.username}
━━━━━━━━
Ha aprovado Un chat.
• Id: <code>{idw}</code>
• <b>antispam :</b> <code>{dias}</code>
━━━━━━━━━━
</b>'''
    try:
        await Client.send_message(_,chat_id=-1002726521405 ,text=texto)
    except (PeerIdInvalid, ChatWriteForbidden) as e:
        print(f"Error al enviar mensaje de notificación: {str(e)}")
        # Opcionalmente, podemos enviar un mensaje al usuario sobre el error
        await m.reply("⚠️ No se pudo enviar la notificación al canal de logs.")
        




    

