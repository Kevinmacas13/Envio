import flet as ft
from telethon import TelegramClient
import asyncio
import pandas as pd
# Credenciales obtenidas de my.telegram.org
API_ID = '11693772'
API_HASH = 'a7ef421e8d6d4435dc4b1fc37260236a'

# Envío de mensajes


async def enviar_mensaje(destinatario, mensaje, log_output):
    try:
        # Crear cliente de Telethon
        async with TelegramClient('session_name', API_ID, API_HASH) as client:
            # Enviar mensaje al destinatario
            await client.send_message(destinatario, mensaje)
            log_output.value = f"Mensaje enviado a {destinatario}"
            log_output.update()
    except Exception as e:
        log_output.value = f"Error: {str(e)}"
        log_output.update()


def main(page: ft.Page):
    page.title = "Enviar Mensajes con Telethon"
    page.window_width = 800
    page.window_height = 600

    titulo = ft.Text("APP DE ENVÍO DE MENSAJES", size=24,
                     weight="bold", color="white")

    titulo_centrado = ft.Row(
        [titulo],
        alignment=ft.MainAxisAlignment.CENTER  # Centrar horizontalmente
    )

    # Crear una instancia de SnackBar con contenido inicial vacío
    snack_bar = ft.SnackBar(content=ft.Text(""))

    def cargar_excel(e):
        try:
            # Verificar si se seleccionó un archivo
            if not file_picker.result or not file_picker.result.files:
                snack_bar.content = ft.Text("No se seleccionó ningún archivo")
                snack_bar.open = True
                page.update()
                return

            # Ruta del archivo seleccionado
            file_path = file_picker.result.files[0].path

            # Leer el archivo Excel
            df = pd.read_excel(file_path)
            print(df)  # Mostrar el contenido del archivo en consola

            # Mostrar los datos en la interfaz
            data_table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text(col)) for col in df.columns
                ],
                rows=[
                    ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell)))
                               for cell in row])
                    for row in df.values
                ],
            )

            # Limpiar el contenido de la página y mostrar la tabla
            page.controls.clear()
            page.add(ft.Text(f"Archivo cargado: {file_path}"), data_table)
            page.update()

        except Exception as ex:
            # Mostrar un mensaje de error en el SnackBar
            snack_bar.content = ft.Text(f"Error al leer el archivo: {ex}")
            snack_bar.open = True
            page.update()

    # Crear un FilePicker para seleccionar el archivo
    file_picker = ft.FilePicker(on_result=cargar_excel)
    page.overlay.append(file_picker)

    # Botón para abrir el FilePicker
    btn_cargar = ft.ElevatedButton(
        "Cargar archivo Excel", on_click=lambda _: file_picker.pick_files(allow_multiple=False))

    # Agregar el SnackBar y el botón al contenido de la página

    numero_input = ft.TextField(label="Número de teléfono", width=350)
    mensaje_input = ft.TextField(
        label="Mensaje a enviar", multiline=True, width=200, height=100)
    log_output = ft.Text(value="", color="green")

    # Íconos personalizados
    icon_telegram = ft.IconButton(
        on_click=lambda e: asyncio.run(on_enviar_click(e)),
        icon=ft.icons.SEND,  # Ícono genérico para Telegram
        icon_color="#00ADB5",     # Color típico de Telegram
        icon_size=40,
    )

    icon_whatsapp = ft.Icon(
        name=ft.icons.CHAT,  # Ícono genérico para WhatsApp
        color="#25D366",     # Color típico de WhatsApp
        size=40
    )

    icon_gmail = ft.Icon(
        name=ft.icons.EMAIL,  # Ícono genérico para Gmail
        color="#D14836",      # Color típico de Gmail
        size=40
    )

    iconos = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("Telegram", color="white"),
                    icon_telegram
                ],
                spacing=10
            ),
            ft.Row(
                controls=[
                    ft.Text("WhatsApp", color="white"),
                    icon_whatsapp
                ],
                spacing=10
            ),
            ft.Row(
                controls=[
                    ft.Text("Gmail", color="white"),
                    icon_gmail
                ],
                spacing=10
            )
        ],
        spacing=20
    )

    async def on_enviar_click(e):
        destinatario = "+593"+numero_input.value
        mensaje = mensaje_input.value
        if destinatario and mensaje:
            log_output.value = "Enviando mensaje..."
            log_output.update()
            await enviar_mensaje(destinatario, mensaje, log_output)
        else:
            log_output.value = "Por favor, completa todos los campos."
            log_output.color = "red"
            log_output.update()

    # enviar_button = ft.ElevatedButton(
    #     "Enviar Mensaje",
    #     on_click=lambda e: asyncio.run(on_enviar_click(e)),
    #     bgcolor="#00ADB5",
    #     color="white",
    #     style=ft.ButtonStyle(
    #         shape=ft.RoundedRectangleBorder(radius=8),  # Bordes redondeados
    #         elevation={"pressed": 6, "default": 3},  # Elevación personalizada
    #     )
    # )
    page.add(
        titulo_centrado,
        numero_input,
        mensaje_input,
        log_output,
        snack_bar,
        btn_cargar,
        iconos
    )


ft.app(target=main)
