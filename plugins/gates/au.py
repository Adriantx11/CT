import asyncio
from srca.configs import find_cards, antispam
from plugins.gates.src.StripeAut import lasting
import time
from db.mongo_client import MongoDB
from srca.configs import addCommand
import random
from collections import defaultdict

# Diccionario para almacenar las colas de procesamiento por usuario
user_queues = defaultdict(asyncio.Queue)
# Diccionario para almacenar las tareas en curso por usuario
user_tasks = defaultdict(list)

async def process_queue(user_id, queue):
    while True:
        try:
            # Obtener el siguiente check de la cola
            check_data = await queue.get()
            if check_data is None:  # Señal para detener el procesamiento
                break
                
            message, cc_com, new = check_data
            try:
                ccs = cc_com.split('|')
                chk = await asyncio.to_thread(lasting, ccs[0], ccs[1], ccs[2], ccs[3])
                fin = time.time()
                
                # Obtener información del bin
                import requests
                proxy = get_proxy()
                if proxy:
                    proxies = {
                        "http": f"http://{proxy['username']}:{proxy['password']}@{proxy['server'].replace('http://', '')}",
                        "https": f"http://{proxy['username']}:{proxy['password']}@{proxy['server'].replace('http://', '')}"
                    }
                    req = await asyncio.to_thread(requests.get, f'https://binlist.io/lookup/{ccs[0][:6]}', proxies=proxies)
                else:
                    req = await asyncio.to_thread(requests.get, f'https://binlist.io/lookup/{ccs[0][:6]}')
                
                texto = f'''<b>・ Stripe Auth

• Cc: <code>{cc_com}</code>
• Status: {chk[0]}
• Response: <code>{chk[1]}</code>

• Bin: {req.json()['scheme']} {req.json()['type']} {req.json()['category']}
• Country:{req.json()['country']['name']} [{req.json()['country']['emoji']}]
• Bank: {req.json()['bank']['name']} 

• Pxs: Live ✅
• Time: <code>{fin-time.time():0.4f}'s</code>
• From: {message.from_user.first_name}</b>'''
                await new.edit_text(texto)
            except Exception as e:
                await new.edit_text(f"Error: {str(e)}")
            finally:
                queue.task_done()
        except Exception as e:
            print(f"Error en process_queue: {str(e)}")
            continue

@addCommand('au')
async def au(client, message):
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

    if ccs == '<b>ingrese la ccs.</b>':
        return await message.reply(ccs)

    new = await message.reply(f'''<b>・ Stripe Auth

• Cc: <code>{cc_com}</code>      
• Status: Processing... [ ☃️ ]
• From: {message.from_user.first_name}</b>''')

    # Iniciar el procesador de cola si no está activo
    if not user_tasks[user_id]:
        task = asyncio.create_task(process_queue(user_id, user_queues[user_id]))
        user_tasks[user_id].append(task)
    
    # Agregar el check a la cola
    await user_queues[user_id].put((message, cc_com, new))


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
