from pyrogram import Client, filters
from paquetes.plantillas import atras
from db.mongo_client import MongoDB
import datetime

@Client.on_callback_query(filters.regex(r"^perfil:"))
async def perfil_cmon(client, call):
    with open('debug_callbacks.txt', 'a') as f:
        f.write(f"[PERFIL] Handler específico ejecutado. Data: {call.data}\n")
    try:
        perfil_text = '''<b>・Perfil ☁️
- - - - - - - - - - - - - - -
<a href=\"https://t.me/\">＄</a> ID: <code>{}</code>
<a href=\"https://t.me/\">＄</a> Username: @{}
<a href=\"https://t.me/\">＄</a> Name: <i>{}</i>
<a href=\"https://t.me/\">＄</a> Creditos: {}
<a href=\"https://t.me/\">＄</a> Rango: {}
<a href=\"https://t.me/\">＄</a> Plan: <i>{}</i>
<a href=\"https://t.me/\">＄</a> Antispam: {}
- - - - - - - - - - - - - - -</b>'''
        querY = MongoDB().query_user(int(call.from_user.id))
        if querY is None:
            with open('debug_callbacks.txt', 'a') as f:
                f.write(f"[PERFIL] Usuario no registrado.\n")
            return await call.answer("Usuario no registrado", show_alert=True)
        await call.edit_message_text(
            perfil_text.format(
                call.from_user.id,
                call.from_user.username,
                call.from_user.first_name,
                querY['credits'],
                querY['role'],
                querY['plan'],
                querY['antispam']
            ),
            reply_markup=atras(call.from_user.id)
        )
    except Exception as e:
        with open('debug_callbacks.txt', 'a') as f:
            f.write(f"[PERFIL] Error: {str(e)}\n")
        await call.answer(f"Error: {str(e)}", show_alert=True)