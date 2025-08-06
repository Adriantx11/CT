from srca.configs import addCommand
from db.mongo_client import MongoDB
import asyncio

@addCommand(['broadcast', 'msg', 'mensaje'])
async def broadcast(client, message):
    """
    Comando para enviar mensajes globales a todos los usuarios registrados.
    Solo disponible para administradores.
    """
    user_id = message.from_user.id
    
    # Verificar si el usuario está registrado
    querY = MongoDB().query_user(int(user_id))
    if querY is None:
        return await message.reply('Usar el comando $register para el registro.')
    
    # Verificar si el usuario es admin
    if not MongoDB().admin(user_id):
        return await message.reply('❌ No tienes permisos de administrador para usar este comando.')
    
    # Verificar que se proporcione un mensaje
    if len(message.command) < 2:
        return await message.reply('❌ Debes escribir el mensaje a enviar.\n\n**Ejemplo:**\n`/broadcast Hola a todos los usuarios!`\n`/msg Mensaje importante`\n`/mensaje Actualización del sistema`')
    
    # Obtener el mensaje (todo después del comando)
    mensaje = message.text.split(' ', 1)[1]
    
    # Mensaje de confirmación inicial
    confirm_msg = await message.reply(f'''📢 **Iniciando Broadcast...**

**Mensaje a enviar:**
`{mensaje}`

⏳ **Procesando usuarios...**''')
    
    try:
        # Obtener todos los usuarios de la base de datos
        usuarios = MongoDB().db.users.find({}, {"user_id": 1})
        usuarios_list = list(usuarios)
        
        if not usuarios_list:
            await confirm_msg.edit_text('❌ No hay usuarios registrados en la base de datos.')
            return
        
        total_usuarios = len(usuarios_list)
        enviados_exitosos = 0
        usuarios_no_validos = []
        errores_otros = []
        
        # Contador de progreso
        progreso_msg = await message.reply(f'📤 **Enviando mensajes...**\n\n✅ **Enviados:** 0/{total_usuarios}\n❌ **Errores:** 0\n⏳ **Procesando...**')
        
        for i, usuario in enumerate(usuarios_list):
            user_id_target = usuario.get("user_id")
            
            if not user_id_target:
                continue
                
            try:
                # Enviar mensaje individual
                await client.send_message(
                    chat_id=int(user_id_target), 
                    text=f'''📢 **Mensaje Global del Administrador**

{mensaje}

---
*Enviado por: {message.from_user.first_name}*
*ID Admin: {message.from_user.id}*'''
                )
                enviados_exitosos += 1
                
                # Actualizar progreso cada 10 envíos
                if (i + 1) % 10 == 0 or (i + 1) == total_usuarios:
                    await progreso_msg.edit_text(
                        f'📤 **Enviando mensajes...**\n\n'
                        f'✅ **Enviados:** {enviados_exitosos}/{total_usuarios}\n'
                        f'❌ **Errores:** {len(usuarios_no_validos) + len(errores_otros)}\n'
                        f'⏳ **Procesando...**'
                    )
                
                # Pequeña pausa para evitar rate limits
                await asyncio.sleep(0.1)
                
            except Exception as e:
                error_str = str(e)
                if "PEER_ID_INVALID" in error_str:
                    usuarios_no_validos.append(user_id_target)
                else:
                    errores_otros.append(f"{user_id_target}: {error_str}")
                continue
        
        # Mensaje final de resultados
        resultado_texto = f'''📢 **Broadcast Completado**

✅ **Enviados exitosamente:** {enviados_exitosos}/{total_usuarios}
❌ **Usuarios no válidos:** {len(usuarios_no_validos)}
⚠️ **Otros errores:** {len(errores_otros)}

**Mensaje enviado:**
`{mensaje}`

**Detalles:**
• **Admin:** {message.from_user.first_name} ({message.from_user.id})
• **Fecha:** {asyncio.get_event_loop().time()}'''

        if usuarios_no_validos:
            resultado_texto += f'\n\n❌ **Usuarios no válidos (PEER_ID_INVALID):**\n`{len(usuarios_no_validos)} usuarios`'
        
        if errores_otros:
            resultado_texto += f'\n\n⚠️ **Otros errores:**\n`{len(errores_otros)} errores`'
        
        await progreso_msg.edit_text(resultado_texto)
        
        # Log de la actividad
        MongoDB().add_log(
            user_id=message.from_user.id,
            action="broadcast",
            gate="admin",
            result="success",
            details=f"Sent to {enviados_exitosos}/{total_usuarios} users, {len(usuarios_no_validos)} invalid, {len(errores_otros)} errors"
        )
        
    except Exception as e:
        await confirm_msg.edit_text(f'❌ **Error al realizar el broadcast:**\n\n`{str(e)}`')
        
        # Log del error
        MongoDB().add_log(
            user_id=message.from_user.id,
            action="broadcast",
            gate="admin",
            result="error",
            details=f"Error: {str(e)}"
        ) 