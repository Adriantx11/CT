from srca.configs import addCommand,Client
from paquetes.plantillas import commd
from db.mongo_client import MongoDB

@addCommand('start')
async def start(_,m):
    querY = MongoDB().query_user(int(m.from_user.id))

    if  querY == None: 
        return await m.reply('Usar el comando $register para el registro.')
        
    if  querY == None: return await m.reply('Usar el comando $register para el registro.')
    
    await m.reply_photo(
        photo='https://imgur.com/p0G9YqD.png',
        caption=f'''<b>Welcome to 𝘾𝙏 𝘾𝙃𝙆⚡️

Hey @{m.from_user.username}, welcome to the Gates section ✨
Thanks for choosing our gateway system — secure, efficient, and reliable.

Version ➝ 1.0
<a href="https://t.me/+A6wPSRDlqu8yZDMx">Support & Updates</a></b>''',
        reply_markup=commd(m.from_user.id)
    )