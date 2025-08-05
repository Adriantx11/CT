from pyrogram import Client
from pyrogram.types import CallbackQuery
import logging, os 

class GtwBot():
    def __init__(self):
        self.app = Client(
            "GtwBot",
            api_id    = 26433740,
            api_hash  = 'd0bdcf11090a60c1acc5846e097a92df',
            bot_token = '7708784779:AAEZWekoQQx1go9fIaUaWxDsEB2cmotqtuA',
            plugins   = dict(root="plugins"),
            workers   = 8,  # Aumentar workers para mejor rendimiento
            max_concurrent_transmissions = 8,  # Aumentar transmisiones concurrentes
            sleep_threshold = 5,  # Reducir el umbral de sueño
            no_updates = False,
            in_memory = True  # Mantener en memoria para mejor rendimiento
        )


    def runn(self):
        os.system("clear")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('bot.log'),
                logging.StreamHandler()
            ]
        )
        self.app.run()


if __name__ == "__main__":
    GtwBot().runn()