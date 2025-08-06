import asyncio
from srca.configs import find_cards, antispam
from plugins.gates.src.braintreeauth import Braintre3
import time
from db.mongo_client import MongoDB
from srca.configs import addCommand
import random


@addCommand('b3')
async def b3(client, message):
    user_id = message.from_user.id
    querY = MongoDB().query_user(int(user_id))
    if querY is None:
        return await message.reply('Usar el comando $register para el registro.')
    if querY['role'] == 'baneado':
        return await message.reply('User baneado')
    if not MongoDB().admin(user_id) and querY['plan'] == 'free':
        return await message.reply('<b>🚫 Usuario Free</b>\n\n¡Aprovecha todo el potencial del bot!\nActualiza a premium y accede a herramientas exclusivas.\n👉 <a href="https://t.me/+A6wPSRDlqu8yZDMx">Solicitar upgrade</a>')
    
    inicio = time.time()

    if antispam(querY['antispam'], message):
        return

    if message.reply_to_message:
        ccs = find_cards(message.reply_to_message.text)
    else:
        ccs = find_cards(message.text)
    cc_com = '{}|{}|{}|{}'.format(ccs[0], ccs[1], ccs[2], ccs[3])

    def get_proxy():
        try:
            with open('srca/proxy.txt', 'r') as file:
                # Filtrar líneas válidas (no comentarios, no vacías, que contengan @)
                proxies = []
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#') and '@' in line:
                        proxies.append(line)
                
            if not proxies:
                print("No se encontraron proxies válidos en proxy.txt")
                return None
                
            proxy_str = random.choice(proxies)
            user_pass, ip_port = proxy_str.split('@')
            username, password = user_pass.split('://')[1].split(':')
            server = f"http://{ip_port}"
            proxy = {
                "server": server,
                "username": username,
                "password": password
            }
            print(f"Usando proxy: {proxy_str}")
            return proxy
            
        except FileNotFoundError:
            print("Error: No se encontró el archivo proxy.txt")
            return None
        except Exception as e:
            print(f"Error al procesar proxy: {str(e)}")
            return None

    import requests
    proxy = get_proxy()
    
    # Manejo mejorado de errores para binlist.io
    try:
        if proxy:
            proxies = {
                "http": f"http://{proxy['username']}:{proxy['password']}@{proxy['server'].replace('http://', '')}",
                "https": f"http://{proxy['username']}:{proxy['password']}@{proxy['server'].replace('http://', '')}"
            }
            req = await asyncio.to_thread(requests.get, f'https://binlist.io/lookup/{ccs[0][:6]}', proxies=proxies, timeout=15)
        else:
            req = await asyncio.to_thread(requests.get, f'https://binlist.io/lookup/{ccs[0][:6]}', timeout=15)
        
        bin_info = req.json()
        bin_text = f"• Bin: {bin_info.get('scheme', 'N/A')} {bin_info.get('type', 'N/A')} {bin_info.get('category', 'N/A')}\n• Country: {bin_info.get('country', {}).get('name', 'N/A')} [{bin_info.get('country', {}).get('emoji', '')}]\n• Bank: {bin_info.get('bank', {}).get('name', 'N/A')}"
    except Exception as e:
        print(f"Error al obtener información del BIN: {e}")
        bin_text = "• Bin: Error al obtener información\n• Country: N/A\n• Bank: N/A"

    if ccs == '<b>ingrese la ccs.</b>':
        return await message.reply(ccs)

    new = await message.reply(f'''<b>・ Braintree Charged

• Cc: <code>{cc_com}</code>      
• Status: Processing... [ ☃️ ]
• From: {message.from_user.first_name}</b>''')

    chk = await asyncio.to_thread(Braintre3().main, cc_com)

    fin = time.time()
    texto = f'''<b>・ Braintree Charged 

• Cc: <code>{cc_com}</code>
• Status: {chk[0]}
• Response: <code>{chk[1]}</code>

{bin_text}

• Pxs: Live ✅
• Time: <code>{fin-inicio:0.4f}'s</code>
• From: {message.from_user.first_name}</b>'''
    
    await new.edit_text(texto)

