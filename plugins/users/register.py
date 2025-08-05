from srca.configs import addCommand,Client
from db.mongo_client import MongoDB
import time

@addCommand('register')
async def start(_,m):
    try:
        querY = MongoDB().query_user(int(m.from_user.id))
    #    if  querY['role'] == 'baneado': return await m.reply('User baneado')

        if  querY == None:
            data = {
                'id': int(m.from_user.id),
                'username': m.from_user.username,
                'first_name': m.from_user.first_name,
                'plan': 'free',
                'role': 'user',
                'credits': 0,
                'antispam': 40,
                'since': None,
                'registered_at': time.time(),
                'last_activity': time.time(),
                'total_checks': 0,
                'premium_days_used': 0
            }
            MongoDB().insert_user(data)

            texto= f'''<b>New User 

Name: {m.from_user.first_name}
id: {m.from_user.id}
Username: @{m.from_user.username}</b>'''
            await _.send_message(chat_id=-1002726521405 ,text=texto)
            
            return await m.reply_text(f'Welcome {m.from_user.first_name}, acabas de registrarte ✳️.')
        
        else:
            await m.reply('<b>Ya estas registrado.</b>')
    except:
        await m.reply('<b>Ya estas registrado.</b>')

