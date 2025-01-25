from telethon import TelegramClient

# Credenciales obtenidas de my.telegram.org
API_ID = '11693772'
API_HASH = 'a7ef421e8d6d4435dc4b1fc37260236a'

# Número de teléfono asociado a tu cuenta
PHONE_NUMBER = '+593995365458'

# Nombre del destinatario (puede ser un usuario o el título de un grupo)
DESTINATARIO = '+593995365458'

# Mensaje a enviar
MENSAJE = '¡Hola! Este mensaje fue enviado sin un bot usando Telethon. 😊'

async def enviar_mensaje():
    # Crear cliente de Telethon
    async with TelegramClient('session_name', API_ID, API_HASH) as client:
        # Enviar mensaje al destinatario
        await client.send_message(DESTINATARIO, MENSAJE)
        print(f"Mensaje enviado a {DESTINATARIO}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(enviar_mensaje())
