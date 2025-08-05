
from srca.configs import addCommand,Client
from db.mongo_client import MongoDB
from random import randrange


@addCommand('addg')
def bin(_,m):
    querY = MongoDB().query_user(int(m.from_user.id))
    if  querY == None: return m.reply('Usar el comando $register para el registro.')
    
    if MongoDB().admin(int(m.from_user.id)) == False: return ...
    
    data = m.text.split(' ')
    
    if len(data) < 3: return m.reply('ingrese datos correctos <code>$addg id dias</code>')

    idw = int(data[1])
    dias = int(data[2])

    query = MongoDB().query_group(idw)

    if query == None: 
        MongoDB().update_group(idw,dias)
        m.reply('Id añadido con exito., ahora puede usar el chat.✅')
        texto= f'''<b>Ha aprovado un chat

Name: {m.from_user.first_name}
id: {m.from_user.id}
Username: @{m.from_user.username}
━━━━━━━━
Ha aprovado Un chat.
• Id: <code>{idw}</code>
• <b>Dias Generados :</b> <code>{dias}</code>
━━━━━━━━━━
</b>'''
        Client.send_message(_,chat_id=-1002726521405 ,text=texto)
        
    else: return m.reply('Ya tiene acceso al chat privado')




    

