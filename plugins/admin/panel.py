from srca.configs import addCommand,Client
from db.mongo_client import MongoDB



@addCommand('panel')
async def bin(_,m):
    if MongoDB().admin(int(m.from_user.id)) == False: return ...

    panel_text = '''<b>📋 Panel de Administración</b>

<b>Comandos de Gestión de Usuarios:</b>
• <code>$ban id</code> - Banear a un usuario
• <code>$unban id</code> - Desbanear a un usuario
• <code>$free id</code> - Quitar acceso premium a un usuario
• <code>$creditos id cantidad</code> - Añadir créditos a un usuario
• <code>$antispam id días</code> - Configurar antispam para un usuario

<b>Comandos de Gestión de Grupos:</b>
• <code>$addg id días</code> - Añadir un grupo con días de acceso
• <code>$removeg id</code> - Remover acceso de un grupo
• <code>$gplan</code> - Ver información del plan del grupo actual

<b>Comandos de Gestión de Keys:</b>
• <code>$key días</code> - Generar una nueva key
• <code>$removekey key</code> - Eliminar una key existente

<b>Comandos de Roles:</b>
• <code>$role id rol</code> - Asignar rol a un usuario (solo owner)

━━━━━━━━━━━━━━━━━━━━━━
<i>Nota: Todos los comandos requieren permisos de administrador</i>'''

    await m.reply(panel_text)
    