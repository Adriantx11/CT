from srca.configs import addCommand, Client
from paquetes.plantillas import perfil_text
from db.mongo_client import MongoDB
import datetime


@addCommand(['me', 'info', 'yo', 'perfil'])
async def me(client, message):
    with open('debug_callbacks.txt', 'a') as f:
        f.write(f"[ME] Handler ejecutado para ID: {message.from_user.id}\n")
    user_id = message.from_user.id
    querY = MongoDB().query_user(int(user_id))
    with open('debug_callbacks.txt', 'a') as f:
        f.write(f"[ME] ID: {user_id} | role: {querY['role'] if querY else None}\n")
    if querY is None:
        return await message.reply('Usar el comando $register para el registro.')
    if querY['role'] == 'baneado':
        return await message.reply('User baneado')
    if not MongoDB().admin(user_id) and querY['plan'] == 'free':
        return await message.reply('<b>🚫 Usuario Free</b>\n\n¡Aprovecha todo el potencial del bot!\nActualiza a premium y accede a herramientas exclusivas.\n👉 <a href="https://t.me/+A6wPSRDlqu8yZDMx">Solicitar upgrade</a>')

    try:
        # Verificar si 'since' existe y no es None
        if querY.get('since') is not None:
            tiempo = datetime.datetime.fromtimestamp(querY['since'])
            data = f'<code>{tiempo.day}/{tiempo.month}/{tiempo.year}</code>'
        else:
            data = '<code>N/A</code>'

        # Calcular días restantes si es premium
        dias_restantes = ""
        if querY['plan'] == 'premium' and querY.get('since') is not None:
            ahora = datetime.datetime.now()
            expiracion = datetime.datetime.fromtimestamp(querY['since'])
            diferencia = (expiracion - ahora).days
            if diferencia > 0:
                dias_restantes = f"\n<a href=\"https://t.me/\">＄</a> » Días restantes: <b>{diferencia}</b>"
            else:
                dias_restantes = "\n<a href=\"https://t.me/\">＄</a> » Días restantes: <b>0</b>"

        perfil_texta = perfil_text.format(
            user_id, 
            message.from_user.username, 
            message.from_user.first_name,
            querY['credits'], 
            querY['role'], 
            querY['plan'], 
            querY['antispam'], 
            data
        ) + dias_restantes

        await message.reply_photo(
            photo='https://imgur.com/p0G9YqD.png',
            caption=perfil_texta
        )

    except Exception as e:
        print(f"Error en /me: {e}")
        perfilt = '''<b>・𝘾𝙏 𝘾𝙃𝙆| Perfil
- - - - - - - - - - - - - - -
<a href=\"https://t.me/\">＄</a> » id: <code>{}</code>
<a href=\"https://t.me/\">＄</a> » Username: @{}
<a href=\"https://t.me/\">＄</a> » Name: <i>{}</i> 
<a href=\"https://t.me/\">＄</a> » Creditos: {}
<a href=\"https://t.me/\">＄</a> » Rango: {}
<a href=\"https://t.me/\">＄</a> » Plan: <i>{}</i>
<a href=\"https://t.me/\">＄</a> » Antispam: {}
- - - - - - - - - - - - - - -</b>'''
        await message.reply_photo(
            photo='https://imgur.com/p0G9YqD.png',
            caption=perfilt.format(
                user_id, 
                message.from_user.username, 
                message.from_user.first_name,
                querY['credits'], 
                querY['role'], 
                querY['plan'], 
                querY['antispam']
            )
        )
