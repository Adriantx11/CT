from srca.configs import addCommand, Client
from paquetes.plantillas import commd
from db.mongo_client import MongoDB
import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Cache para el mensaje de bienvenida
WELCOME_CACHE = {}

@addCommand('cmds')
async def cmds(client, message):
    user_id = message.from_user.id
    querY = MongoDB().query_user(int(user_id))
    if querY is None:
        return await message.reply('Usar el comando $register para el registro.')
    if querY['role'] == 'baneado':
        return await message.reply('User baneado')
    # Verificar cache
    if user_id in WELCOME_CACHE:
        cache_time, cached_message = WELCOME_CACHE[user_id]
        if asyncio.get_event_loop().time() - cache_time < 300:  # Cache válido por 5 minutos
            return await message.reply_photo(
                photo='https://imgur.com/p0G9YqD.png',
                caption=cached_message['caption'],
                reply_markup=cached_message['markup']
            )
    
    # Obtener datos del usuario
    querY = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: MongoDB().query_user(user_id)
    )
    
    if querY is None:
        return await message.reply('Usar el comando $register para el registro.')

    if querY['role'] == 'baneado':
        return await message.reply('User baneado')

    # Preparar mensaje
    welcome_msg = {
        'photo': 'https://imgur.com/p0G9YqD.png',
        'caption': f"""<b>Welcome to 𝘾𝙏 𝘾𝙃𝙆⚡️

Hey @{message.from_user.username}, glad to have you here ✨
Thanks for choosing our check system — simple, fast, and powerful.

Version ➝ 1.0
<a href="https://t.me/+A6wPSRDlqu8yZDMx">Support & Updates</a></b>""",
        'markup': commd(user_id)
    }
    
    # Guardar en cache
    WELCOME_CACHE[user_id] = (asyncio.get_event_loop().time(), welcome_msg)
    
    # Enviar mensaje
    await message.reply_photo(
        photo=welcome_msg['photo'],
        caption=welcome_msg['caption'],
        reply_markup=welcome_msg['markup']
    )
    