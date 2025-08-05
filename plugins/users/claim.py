from srca.configs import addCommand,Client
from paquetes.plantillas import  perfil_text
from db.mongo_client import MongoDB
import asyncio

# Diccionario de locks por usuario
user_locks = {}

@addCommand('claim')
async def start(_,m):
    user_id = m.from_user.id
    if user_id not in user_locks:
        user_locks[user_id] = asyncio.Lock()

    async with user_locks[user_id]:
        querY = MongoDB().query_user(int(user_id))

        if  querY == None: 
            return await m.reply_photo(
                photo='https://imgur.com/p0G9YqD.png',
                caption='Usar el comando $register para el registro.'
            )
        if querY['role'] == 'baneado': 
            return await m.reply_photo(
                photo='https://imgur.com/p0G9YqD.png',
                caption='User baneado'
            )
        
        bins = m.text.split(' ')
        if len(bins) < 2: 
            return await m.reply_photo(
                photo='https://imgur.com/p0G9YqD.png',
                caption='ingrese la key.'
            )
        
        querYl = MongoDB().query_key(bins[1])

        if not querYl or querYl.get('key') != bins[1]:
            await m.reply_photo(
                photo='https://imgur.com/p0G9YqD.png',
                caption='Invalid key'
            )
            return

        try:
            # Actualizar el plan del usuario
            MongoDB().update_user(user_id, querYl['dias'])
            # Eliminar la key usada
            MongoDB().key_delete(bins[1])
            
            # Notificar al usuario
            await m.reply_photo(
                photo='https://imgur.com/p0G9YqD.png',
                caption='<b>User updated successfully, ya eres premium.✅</b>'
            )

            # Notificar al grupo de administración
            texto= f'''<b>Key reclamada

Name: {m.from_user.first_name}
id: {m.from_user.id}
Username: @{m.from_user.username}
-------------
Reclamo key

key: {querYl['key']}
dias: {querYl['dias']}
-------------
</b>'''
            await Client.send_message(_,chat_id=-1002726521405 ,text=texto)
            return
        except Exception as e:
            print(f"Error en claim: {str(e)}")
            await m.reply_photo(
                photo='https://imgur.com/p0G9YqD.png',
                caption='<b>Ocurrió un error inesperado, contacta a soporte.</b>'
            )
            return