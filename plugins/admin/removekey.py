
from srca.configs import addCommand,Client
from db.mongo_client import MongoDB
from random import randrange


@addCommand('removekey')
def bin(_,m):
    querY = MongoDB().query_user(int(m.from_user.id))
    if  querY == None: return m.reply('Usar el comando $register para el registro.')
    
    if MongoDB().admin(int(m.from_user.id)) == False: return ...
    
    dias = m.text.split(' ')
    
    if len(dias) < 2: return m.reply('ingrese La key ')


    MongoDB().key_delete(dias[1])

    m.reply('Key removida correctamente')
    
    texto= f'''<b>remove key

Name: {m.from_user.first_name}
id: {m.from_user.id}
Username: @{m.from_user.username}
━━━━━━━━
A removido una key
• Key: <code>{dias[1]}</code>
━━━━━━━━━━
</b>'''
    Client.send_message(_,chat_id=-1002726521405 ,text=texto)
        
    
           
            #Client.send_m(_,chat_id = '-1002125995809',text=f'<b><code>{m.from_user.first_name}| {m.from_user.id} a generado una key de {dias} Dias</code>.</b>')    
    

