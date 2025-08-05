import requests
from srca.configs import addCommand
from db.mongo_client import MongoDB


@addCommand('rnd')
def bin(_,m):
    # if MongoDB().query_group(m.chat.id) is None and not MongoDB().owner(m.from_user.id): return m.reply('Chat not Authorized.')

    querY = MongoDB().query_user(int(m.from_user.id))
    if  querY == None: return m.reply('Usar el comando $register para el registro.')
    if  querY['role'] == 'baneado': return m.reply('User baneado')
        
    bins = m.text.split(' ')
    
    if len(bins) < 2: return m.reply('ingrese el pais')
    
    req = requests.get(f'https://randomuser.me/api/?nat={bins[1]}&randomapi')

    dataR = req.json()['results'][0]

    text =f'''<b>[🌎] 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐜𝐢𝐨𝐧 𝐏𝐚𝐢𝐬
━━━━━━━━━━━━━━━━
<a href=\"https://t.me/\">• Name</a> : <code>{dataR['name']['first']} {dataR['name']['last']}</code>
<a href=\"https://t.me/\">• Street</a> : <code>{dataR['location']['street']['name']} {dataR['location']['street']['number']}</code>
<a href=\"https://t.me/\">• City</a> : <code>{dataR['location']['city']}</code>
<a href=\"https://t.me/\">• State</a> : <code>{dataR['location']['state']}</code>
<a href=\"https://t.me/\">• Zip</a> : <code>{dataR['location']['postcode']}</code>
<a href=\"https://t.me/\">• Country</a> : {dataR['location']['country']}
━━━━━━━━━━━━━━━━</b>'''

    m.reply(text)