import pymongo
import datetime
import time
import threading
import requests
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError

class MongoDB(object):
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
            try:
                cls._client = MongoClient(
                    "mongodb://mongo:KDnHMBhbiawymvixrpoIGIPdyeKusBcR@centerbeam.proxy.rlwy.net:15797",
                    maxPoolSize=20,
                    minPoolSize=5,
                    maxIdleTimeMS=60000,
                    connectTimeoutMS=10000,
                    serverSelectionTimeoutMS=10000,
                    retryWrites=True,
                    retryReads=True,
                    socketTimeoutMS=10000,
                    heartbeatFrequencyMS=30000
                )
                cls._client.server_info()  # Verificar conexión
                cls._instance.db = cls._client["bot"]
                cls._instance.user = cls._instance.db["user"]
                cls._instance.group = cls._instance.db["group"]
                cls._instance.key = cls._instance.db["keys"]
                
                # Limpiar documentos duplicados antes de crear índices
                cls._instance._clean_duplicates()
                
                # Crear índices para mejorar el rendimiento
                try:
                    cls._instance.user.create_index("id", unique=True)
                    cls._instance.group.create_index("id", unique=True)
                    cls._instance.key.create_index("key", unique=True)
                except DuplicateKeyError as e:
                    print(f"Advertencia: No se pudieron crear algunos índices únicos: {e}")
                
            except ConnectionFailure:
                raise Exception("No se pudo conectar a MongoDB")
        return cls._instance

    def _clean_duplicates(self):
        """Limpia documentos duplicados manteniendo el más reciente"""
        # Limpiar duplicados en group
        pipeline = [
            {"$sort": {"dias": -1}},  # Ordenar por dias descendente
            {"$group": {
                "_id": "$id",
                "doc": {"$first": "$$ROOT"}
            }},
            {"$replaceRoot": {"newRoot": "$doc"}}
        ]
        
        # Obtener documentos únicos
        unique_docs = list(self.group.aggregate(pipeline))
        
        # Eliminar todos los documentos
        self.group.delete_many({})
        
        # Insertar documentos únicos
        if unique_docs:
            self.group.insert_many(unique_docs)

    def query_user(self, id:int=None):
        if id:
            return self.user.find_one({"id":id})
        return self.user.find()

    def query_group(self, id:int=None):
        if id:
            return self.group.find_one({"id":id})
        return self.group.find()

    def query_key(self, key=None):
        if key:
            return self.key.find_one({"key":key})
        return None

    def insert_user(self, data:dict):
        return self.user.insert_one(data)

    def key_add(self, key, dias):
        return self.key.insert_one({"key":key, "dias":dias})

    def update_user(self, idw, dia):
        usuario = self.query_user(idw)
        ahora = datetime.datetime.now()
        # Si el usuario ya es premium y la fecha de expiración es futura, sumar los días
        if usuario and usuario.get('plan') == 'premium' and usuario.get('since') and usuario['since'] > ahora.timestamp():
            nueva_fecha = datetime.datetime.fromtimestamp(usuario['since']) + datetime.timedelta(days=dia)
        else:
            nueva_fecha = ahora + datetime.timedelta(days=dia)
        times = nueva_fecha.timestamp()
        self.user.update_one(
            {"id": idw},
            {"$set": {
                "plan": "premium",
                "since": times,
                "antispam": 20
            }}
        )

    def delete_user_p(self, idw):
        self.user.update_one(
            {"id": idw},
            {"$set": {
                "plan": "free",
                "since": None,
                "antispam": 40
            }}
        )

    def add_antispam(self, id, ant):
        self.user.update_one({"id": id}, {"$set": {"antispam": ant}})

    def add_crdits(self, id, crdit):
        self.user.update_one(
            {"id": id},
            {"$inc": {"credits": crdit}}
        )

    def update_group(self, idw, dias):
        tiempo_futuro = datetime.datetime.now() + datetime.timedelta(days=dias)
        times = tiempo_futuro.timestamp()
        self.group.insert_one({"id":idw, "dias":times})

    def key_delete(self, key):
        return self.key.delete_one({"key":key})

    def delete_chat(self, id):
        return self.group.delete_one({"id":id})

    def ban(self, id):
        self.user.update_one({"id": id}, {"$set": {"role": 'baneado'}})

    def unban(self, id):
        self.user.update_one({"id": id}, {"$set": {"role": 'user'}})
    
    def add_role(self, id, role):
        self.user.update_one({"id": id}, {"$set": {"role": role}})
        
    def save_key(self, key, dias):
        return self.key.insert_one({"key":key, "dias":dias})
        
    def admin(self, id):
        query = self.query_user(id)
        if not query:
            return False
        return query['role'] in ['admin', 'seller', 'owner', 'co-funders']

    def owner(self, id):
        query = self.query_user(id)
        if not query:
            return False
        return query['role'] in ['owner', 'co-funders']

def expulse_user():
    client = MongoClient(
        "mongodb://mongo:KDnHMBhbiawymvixrpoIGIPdyeKusBcR@centerbeam.proxy.rlwy.net:15797",
        maxPoolSize=50,
        minPoolSize=10
    )
    db = client["bot"]
    collection = db["user"]
    collection1 = db["group"]

    while True:
        try:
            # Procesar grupos expirados
            expired_groups = collection1.find({"dias": {"$lt": time.time()}})
            for user in expired_groups:
                MongoDB().delete_chat(user['id'])
                
                # Enviar notificaciones
                bot_token = '7708784779:AAEZWekoQQx1go9fIaUaWxDsEB2cmotqtuA'
                base_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
                
                # Notificar al usuario
                requests.post(
                    base_url,
                    params={
                        'chat_id': user['id'],
                        'text': '<b>Se acabo tu acceso al grupo de usar nuestro bot.❗️</b>',
                        'parse_mode': 'HTML'
                    }
                )
                
                # Notificar al grupo
                requests.post(
                    base_url,
                    params={
                        'chat_id': -1002726521405 ,
                        'text': f'<b>Se le acabo el acceso de dias al chat con id :( {user["id"]}  )❗️</b>',
                        'parse_mode': 'HTML'
                    }
                )

            # Procesar usuarios expirados
            expired_users = collection.find({"since": {"$lt": time.time()}})
            for user in expired_users:
                collection.update_one(
                    {"_id": user["_id"]},
                    {"$set": {
                        "plan": "free",
                        "antispam": 40,
                        "key": None,
                        "since": None
                    }}
                )
                collection1.delete_one({"id": user['id']})
                
                # Enviar notificaciones
                bot_token = '7708784779:AAEZWekoQQx1go9fIaUaWxDsEB2cmotqtuA'
                base_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
                
                # Notificar al usuario
                requests.post(
                    base_url,
                    params={
                        'chat_id': user['id'],
                        'text': '<b>Se acabo tu plan premium con nuestro bot.❗️</b>',
                        'parse_mode': 'HTML'
                    }
                )
                
                # Notificar al grupo
                requests.post(
                    base_url,
                    params={
                        'chat_id': -1002726521405 ,
                        'text': f'<b>Se le acabo el plan premium al usuario( {user["id"]}  )❗️</b>',
                        'parse_mode': 'HTML'
                    }
                )

        except Exception as e:
            print(f"Error en expulse_user: {e}")
            
        time.sleep(20)

thread2 = threading.Thread(target=expulse_user)
thread2.start()
