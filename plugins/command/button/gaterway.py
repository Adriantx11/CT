from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from paquetes.plantillas import atras
import asyncio

@Client.on_callback_query(filters.regex(r"^gates:"))
async def gates_coman(client, call):
    with open('debug_callbacks.txt', 'a') as f:
        f.write(f"[GATES] Handler específico ejecutado. Data: {call.data}\n")
    try:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Auth", callback_data="gates_auth"),
                InlineKeyboardButton("CCN", callback_data="gates_ccn"),
                InlineKeyboardButton("Massmode", callback_data="gates_massmode")
            ],
            [
                InlineKeyboardButton("Atrás", callback_data=f"atras:{call.from_user.id}")
            ]
        ])
        await asyncio.sleep(0.5)  # Reducido a 0.5 segundos
        await call.edit_message_text(f'''<b>・Hey @{call.from_user.username}, welcome to the Gates section ✨
Thanks for choosing our gateway system — secure, efficient, and reliable.</b>''', reply_markup=keyboard)
    except Exception as e:
        with open('debug_callbacks.txt', 'a') as f:
            f.write(f"[GATES] Error: {str(e)}\n")
        await call.answer(f"Error: {str(e)}", show_alert=True)

@Client.on_callback_query(filters.regex(r"^gates_auth$"))
async def gates_auth_handler(client, call):
    await asyncio.sleep(0.5)  # Reducido a 0.5 segundos
    await call.edit_message_text(
        """<b>・Auth Gateway ☁️
- - - - - - - - - - - - - - -
<a href=\"https://t.me/\">＄</a> Status    » <i>Premium</i>
<a href=\"https://t.me/\">＄</a> Type    » <i>Stripe Auth</i>
<a href=\"https://t.me/\">＄</a> Cmmd    » $au
<a href=\"https://t.me/\">＄</a> Format   » <code>$au cc|mm|yy|cvc</code>
- - - - - - - - - - - - - - -
<a href=\"https://t.me/\">＄</a> Status    » <i>Premium</i>
<a href=\"https://t.me/\">＄</a> Type    » <i>Braintree Auth Avs</i>
<a href=\"https://t.me/\">＄</a> Cmmd    » $b3
<a href=\"https://t.me/\">＄</a> Format   » <code>$b3 cc|mm|yy|cvc</code>
- - - - - - - - - - - - - - -
<a href=\"https://t.me/\">＄</a> Status    » <i>Premium</i>
<a href=\"https://t.me/\">＄</a> Type    » <i>vbv</i>
<a href=\"https://t.me/\">＄</a> Cmmd    » $vbv
<a href=\"https://t.me/\">＄</a> Format   » <code>$vbv cc|mm|yy|cvc</code>
- - - - - - - - - - - - - - -
""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Atrás", callback_data=f"gates:{call.from_user.id}")]
        ])
    )

@Client.on_callback_query(filters.regex(r"^gates_ccn$"))
async def gates_ccn_handler(client, call):
    await asyncio.sleep(0.5)  # Reducido a 0.5 segundos
    await call.edit_message_text(
        """<b>・CCN Gateway ☁️
- - - - - - - - - - - - - - -
<a href=\"https://t.me/\">＄</a> Status    » <i>Premium</i>
<a href=\"https://t.me/\">＄</a> Type    » <i>Paypal</i>
<a href=\"https://t.me/\">＄</a> Cmmd    » $pp
<a href=\"https://t.me/\">＄</a> Format   » <code>$pp cc|mm|yy|cvc</code>
- - - - - - - - - - - - - - -""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Atrás", callback_data=f"gates:{call.from_user.id}")]
        ])
    )

@Client.on_callback_query(filters.regex(r"^gates_massmode$"))
async def gates_massmode_handler(client, call):
    await asyncio.sleep(0.5)  # Reducido a 0.5 segundos
    await call.edit_message_text(
        """<b>・Massmode Gateway ☁️
- - - - - - - - - - - - - - -
<a href=\"https://t.me/\">＄</a> Status    » <i>Premium</i>
<a href=\"https://t.me/\">＄</a> Type    » <i>Mercado Pago</i>
<a href=\"https://t.me/\">＄</a> Cmmd    » $mp
<a href=\"https://t.me/\">＄</a> Format   » <code>$mp cc|mm|yy|cvc</code>
- - - - - - - - - - - - - - -
<a href=\"https://t.me/\">＄</a> Status    » <i>Premium</i>
<a href=\"https://t.me/\">＄</a> Type    » <i>Amazon Global</i>
<a href=\"https://t.me/\">＄</a> Cmmd    » $am
<a href=\"https://t.me/\">＄</a> Cookie    » <code>/cookie</code>
<a href=\"https://t.me/\">＄</a> Format   » <code>$am cc|mm|yy|cvc</code>
- - - - - - - - - - - - - - -
""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Atrás", callback_data=f"gates:{call.from_user.id}")]
        ])
    )