from pyrogram import Client, filters
from paquetes.plantillas import commd

@Client.on_callback_query(filters.regex(r"^atras:"))
async def atras(client, call):
    with open('debug_callbacks.txt', 'a') as f:
        f.write(f"[ATRAS] Handler específico ejecutado. Data: {call.data}\n")
    try:
        await call.edit_message_text(
            f'''<b>Welcome to CT Chk ⚡️\n\nHey @{call.from_user.username}, glad to have you here ✨\nThanks for choosing our check system — simple, fast, and powerful.\n\nVersion ➝ 1.0\n<a href="https://t.me/+A6wPSRDlqu8yZDMx">Support & Updates</a></b>''',
            reply_markup=commd(call.from_user.id)
        )
    except Exception as e:
        with open('debug_callbacks.txt', 'a') as f:
            f.write(f"[ATRAS] Error: {str(e)}\n")
        await call.answer(f"Error: {str(e)}", show_alert=True)