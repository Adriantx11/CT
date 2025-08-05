from pyrogram import filters,Client
import requests,re
from pyrogram.types import ( InlineKeyboardButton,InlineKeyboardMarkup )
from db.mongo_client import MongoDB
from paquetes.luhn_ccs_gen import Generator


@Client.on_message(filters.command('gen', prefixes=["/",".","$","!","%","#"], case_sensitive=False) & filters.text)  
def hello(_,message): 
    # if MongoDB().query_group(message.chat.id) is None and not MongoDB().owner(message.from_user.id): return message.reply('Chat not Authorized.')
    querY = MongoDB().query_user(int(message.from_user.id))
    if  querY == None: return message.reply('Usar el comando $register para el registro.')
    
    if  querY['role'] == 'baneado': return message.reply('User baneado')
    
    else:
        try:
            ccbin = message.text[len('/gen '):]
            
            if not ccbin: return message.reply("<b>• Gen ccs\n• Format: /gen <code>cards</code>\n• Use: Free</b>",quote=True)
            if len(str(ccbin)) < 6: return message.reply('<b>el bin es menos de 6 digitos | ingrese un bin.</b>')
            geneo = re.findall(r'[0-9]+',message.text)
            if not geneo: return message.reply('<b>Ingrese el bin a generar | error de bin.</b>')

            binreq = requests.get(f'https://bins.antipublic.cc/bins/{ccbin[:6]}')
            
            if binreq.status_code == 520: return message.reply('<i>Invalid BIN.</i>')
            elif 'Invalid BIN' in binreq.text:return message.reply('<b>Invalid BIN.</b>')
            elif 'not found' in binreq.text:return message.reply('<b>not found</b>')
            else:
                extra = Generator(ccbin,10,True).generate_ccs()


                cc1 = extra[0]
                cc2 = extra[1]
                cc3 = extra[2]
                cc4 = extra[3]
                cc5 = extra[4]
                cc6 = extra[5]
                cc7 = extra[6]
                cc8 = extra[7]
                cc9 = extra[8]
                cc10 = extra[9]
                    
                texto= f'''<b>Generador ccs

Format: {ccbin}

<code>{cc1}</code>
<code>{cc2}</code>
<code>{cc3}</code>
<code>{cc4}</code>
<code>{cc5}</code>
<code>{cc6}</code>
<code>{cc7}</code>
<code>{cc8}</code>
<code>{cc9}</code>
<code>{cc10}</code>
- - - - - - - - - - - - - - -
<a href=\"https://t.me/\">• Bin Info</a> : 
<a href=\"https://t.me/\">Pais</a> : {binreq.json()['country_name']} [ {binreq.json()['country_flag']} ]
<a href=\"https://t.me/\">Banco</a> : {binreq.json()['bank']} 
<a href=\"https://t.me/\">Data</a> : {binreq.json()['brand']} - {binreq.json()['level']} - {binreq.json()['type']}
- - - - - - - - - - - - - - -
by: @{message.from_user.username}</b>'''
                re_gen = InlineKeyboardMarkup([[InlineKeyboardButton("regen",callback_data=f"regen:{message.from_user.id}")],])
                message.reply(texto,reply_markup=re_gen,reply_to_message_id=message.id)

        except Exception as e:
            
            message.reply(f'<b>• <i>Entrada invalida</i></b>')  