
from srca.configs import addCommand,Client
from db.mongo_client import MongoDB
from random import randrange


@addCommand('role')
def bin(_,m):
    querY = MongoDB().query_user(int(m.from_user.id))
    if  querY == None: return m.reply('Usar el comando $register para el registro.')
    
    if MongoDB().owner(int(m.from_user.id)) == False: return ...
    
    data = m.text.split(' ')
    
    if len(data) < 3: return m.reply('ingrese datos correctos <code>$role id antispam</code>')

    idw = int(data[1])
    dias = str(data[2])
    
    MongoDB().add_role(idw,dias)
    m.reply(f'Ahora el usuario {idw}, cumple el rol: {dias}')

    texto= f'''<b>Role usado

Name: {m.from_user.first_name}
id: {m.from_user.id}
Username: @{m.from_user.username}
━━━━━━━━
Ha editado los Rol
• Id: <code>{idw}</code>
• <b>rol: </b> <code>{dias}</code>
━━━━━━━━━━
</b>'''
    Client.send_message(_,chat_id=-1002726521405 ,text=texto)