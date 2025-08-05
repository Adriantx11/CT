
from srca.configs import addCommand,Client
from db.mongo_client import MongoDB
import datetime


@addCommand('gplan')
def bin(_,m):

    querY = MongoDB().query_user(int(m.from_user.id))
    if  querY == None: return m.reply('Usar el comando $register para el registro.')
    
    if MongoDB().admin(int(m.from_user.id)) == False: return ...
    
    querG =  MongoDB().query_group(m.chat.id)
   
    if querG == None: 
        data = 'Sin dias'
        authorized  = 'No autorizado'
    else: 
        authorized = 'Autorizado'
        tiempo = datetime.datetime.fromtimestamp(querG['dias'])

        data = f'<code>{tiempo.day}/{tiempo.month}/{tiempo.year}</code>'
        

    
    text = f'''<b>𝙋𝙡𝙖𝙣 𝙂𝙧𝙪𝙥𝙤</b>
- - - - - - - - - - - - - - - - - - - -
<b>• Chat : {m.chat.title}</b>
<b>• ChatId :</b> <code>{m.chat.id}</code>
<b>• ChatType :</b> <code>{str(m.chat.type).replace("ChatType.", "").lower()}</code>
<b>• Authorization : {authorized}</b>
<b>• Expiracion : {data}</b>'''
    
    m.reply(text)