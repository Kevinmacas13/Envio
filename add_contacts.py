from telethon import TelegramClient
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact

# Credenciales de la API de Telegram
api_id = '11693772'
api_hash = 'a7ef421e8d6d4435dc4b1fc37260236a'
phone_number = '+593995365458'  

# Crear cliente de Telethon
client = TelegramClient('session_name', api_id, api_hash)

async def agregar_contactos(contactos):
    # Preparar la lista de contactos para importar
    contactos_importar = [
        InputPhoneContact(client_id=0, phone=contacto['telefono'], first_name=contacto['nombre'], last_name="")
        for contacto in contactos
    ]
    
    # Importar los contactos
    resultado = await client(ImportContactsRequest(contactos_importar))
    print("Contactos agregados:", resultado.users)

# Lista de contactos (puedes reemplazarla con datos de un archivo CSV)
contactos = [
    {'nombre': 'Juan', 'telefono': '+1234567890'},
    {'nombre': 'Ana', 'telefono': '+9876543210'},
]

# Ejecutar la tarea asincrónica
with client:
    client.loop.run_until_complete(agregar_contactos(contactos))
