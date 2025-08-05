import re
import time
import random
from pyrogram import Client, filters
from db.mongo_client import MongoDB
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
import inspect

# Crear un pool de hilos para operaciones asíncronas
thread_pool = ThreadPoolExecutor(max_workers=10)

# Cache para usuarios verificados
verified_users = {}

def padlock(callback_query):
    if callback_query.message.from_user.id == callback_query.from_user.id:
        callback_query.continue_propagation()
    else: 
        return callback_query.answer("Comando bloqueado ‼️")

@lru_cache(maxsize=1000)
def find_cards(text):
    try:
        card_info = re.search(r'(\d{15,16})+?[^0-9]+?(\d{1,2})[\D]*?(\d{2,4})[^0-9]+?(\d{3,4})', text)
        if not card_info:
            return '<b>ingrese la ccs.</b>'
        cc, mes, ano, cvv = card_info.groups()
        cc = cc.replace("-", "").replace(" ", "")
        return cc, mes, ano, cvv
    except: 
        return '<b>ingrese la ccs.</b>'

def addCommand(command):    
    prefixes = ['.','/','$','!','%','#','@','&','*','+','-','_','|','~','`']
    def decorator(func):
        @Client.on_message(filters.command(command, prefixes=prefixes))
        async def wrapper(client, message):
            user_id = message.from_user.id
            # Permitir el comando register aunque el usuario no esté registrado
            if command == 'register':
                if inspect.iscoroutinefunction(func):
                    return await func(client, message)
                else:
                    return func(client, message)
            # Verificar cache de usuario
            if user_id in verified_users:
                cache_time, user_data = verified_users[user_id]
                if time.time() - cache_time < 300:  # Cache válido por 5 minutos
                    if user_data['role'] == 'baneado':
                        return await message.reply('User baneado')
                    if inspect.iscoroutinefunction(func):
                        return await func(client, message)
                    else:
                        return func(client, message)
            # Ejecutar verificaciones en paralelo
            futures = []
            futures.append(thread_pool.submit(MongoDB().query_group, message.chat.id))
            futures.append(thread_pool.submit(MongoDB().query_user, user_id))
            group_result, user_result = [f.result() for f in futures]
            if group_result is None:
                # return await message.reply('Chat not Authorized.')
                pass
            if user_result is None:
                return await message.reply('Usar el comando $register para el registro.')
            if user_result['role'] == 'baneado':
                return await message.reply('User baneado')
            verified_users[user_id] = (time.time(), user_result)
            if inspect.iscoroutinefunction(func):
                return await func(client, message)
            else:
                return func(client, message)
        return wrapper
    return decorator

def rnd_prox():
    try:
        with open("srca/proxy.txt", "r") as archivo:
            proxies = archivo.readlines()
        ranP = random.choice(proxies).strip() 
        return {'http': ranP, 'https': ranP}
    except:
        return None

# Cache para el antispam
last_request_time = {}
antispam_cache = {}

def antispam(tiempo, message):
    user_id = message.from_user.id
    current_time = time.time()
    
    # Verificar cache primero
    if user_id in antispam_cache:
        cache_time, cache_result = antispam_cache[user_id]
        if current_time - cache_time < 1:  # Cache válido por 1 segundo
            return cache_result
    
    # Verificar si el usuario es owner o co-funders
    querY = MongoDB().query_user(user_id)
    if querY and (querY['role'] == 'owner' or querY['role'] == 'co-funders'):
        antispam_cache[user_id] = (current_time, False)
        return False
    
    if user_id in last_request_time and current_time - last_request_time[user_id] < tiempo:
        wait = int(tiempo - (current_time - last_request_time[user_id]))
        message.reply(f"<b>Antispam <code>{wait}s</code> !</b>")
        antispam_cache[user_id] = (current_time, True)
        return True  
    
    last_request_time[user_id] = current_time
    antispam_cache[user_id] = (current_time, False)
    return False 