import asyncio
from telethon import TelegramClient
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact

# Reemplaza estos valores con tus credenciales de Telegram API
API_ID = '11693772'
API_HASH = 'a7ef421e8d6d4435dc4b1fc37260236a'

class LogOutput:
    def __init__(self):
        self.value = ""
        self.color = "black"
    def update(self):
        print(f"[LOG] {self.color.upper()}: {self.value}")

async def enviar_mensaje(destinatario, mensaje, log_output, first_name):
    async with TelegramClient('session_name', API_ID, API_HASH) as client:
        try:
            # Intentar enviar el mensaje directamente
            await client.send_message(destinatario, mensaje)
            log_output.value = f"Mensaje enviado correctamente a {destinatario}"
            log_output.color = "green"
            log_output.update()
            return True
        except Exception as e:
            log_output.value = f"No se pudo enviar el mensaje a {destinatario}. Intentando agregar el contacto..."
            log_output.color = "orange"
            log_output.update()
            print(f"No se pudo enviar el mensaje: {e}")

            # Validar y preparar el número de teléfono
            if not destinatario.startswith("+"):
                destinatario = f"+{destinatario}"

            try:
                # Crear un contacto temporal
                contacto = InputPhoneContact(
                    client_id=0,  # ID único temporal
                    phone=destinatario,
                    first_name=first_name,
                    last_name="Temp"
                )
                result = await client(ImportContactsRequest([contacto]))
                if result.users:
                    log_output.value = f"Contacto {destinatario} agregado exitosamente. Reintentando enviar mensaje..."
                    log_output.color = "blue"
                    log_output.update()
                    print(f"Contacto agregado: {result.users[0].first_name}")

                    # Reintentar enviar el mensaje
                    await client.send_message(destinatario, mensaje)
                    log_output.value = f"Mensaje enviado correctamente a {destinatario} después de agregarlo."
                    log_output.color = "green"
                    log_output.update()
                    return True
                else:
                    log_output.value = f"No se pudo agregar el contacto {destinatario}."
                    log_output.color = "red"
                    log_output.update()
                    print("No se pudo agregar el contacto.")
                    return False
            except Exception as contact_error:
                log_output.value = f"Error al agregar el contacto: {str(contact_error)}"
                log_output.color = "red"
                log_output.update()
                print(f"Error al agregar el contacto: {contact_error}")
                return False

if __name__ == "__main__":
    DESTINATARIO = "+593968788894"  # Número de teléfono internacional
    MENSAJE = "¡Hola! Este es un mensaje de prueba enviado desde Telethon."
    FIRST_NAME = "Prueba"  # Nombre temporal del contacto
    log_output = LogOutput()

    # Ejecutar la función de envío de mensaje
    asyncio.run(enviar_mensaje(DESTINATARIO, MENSAJE, log_output, FIRST_NAME))
