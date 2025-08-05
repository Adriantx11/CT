from pyrogram import Client, filters
from paquetes.plantillas import atras

@Client.on_callback_query(filters.regex(r"^tools:"))
async def tool_com(client, call):
    with open('debug_callbacks.txt', 'a') as f:
        f.write(f"[TOOLS] Handler específico ejecutado. Data: {call.data}\n")
    try:
        mensaje = """
<b>・Tools ☁️
- - - - - - - - - - - - - - -
<a href=\"https://t.me/\">＄</a> Status    » <i>Free</i>
<a href=\"https://t.me/\">＄</a> Comando   » $bin
<a href=\"https://t.me/\">＄</a> Formato   » $bin 456789
- - - - - - - - - - - - - - -
<a href=\"https://t.me/\">＄</a> Status    » <i>Free</i>
<a href=\"https://t.me/\">＄</a> Comando   » $gen
<a href=\"https://t.me/\">＄</a> Formato   » $gen 456789
- - - - - - - - - - - - - - -
<a href=\"https://t.me/\">＄</a> Status    » <i>Free</i>
<a href=\"https://t.me/\">＄</a> Comando   » $rnd
<a href=\"https://t.me/\">＄</a> Formato   » $rand us
- - - - - - - - - - - - - - -</b>"""
        await call.edit_message_text(mensaje, reply_markup=atras(call.from_user.id))
    except Exception as e:
        with open('debug_callbacks.txt', 'a') as f:
            f.write(f"[TOOLS] Error: {str(e)}\n")
        await call.answer(f"Error: {str(e)}", show_alert=True)
