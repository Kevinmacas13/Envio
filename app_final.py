import flet as ft
from telethon import TelegramClient
import asyncio
import pandas as pd
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Credenciales obtenidas de my.telegram.org
API_ID = '11693772'
API_HASH = 'a7ef421e8d6d4435dc4b1fc37260236a'


# Variables globales
df = None
vector_3 = []
vector_4 = []
matriz_resultados = []

# Configuración global del servidor SMTP
SMTP_SERVER = "devzone.ec"
SMTP_PORT = 465
EMAIL = "kevin.macas@devzone.ec"
PASSWORD = "-Kevin7-#1992"

# Mensajes
mensajes_dropbox = [
    "Estimado usuario, le recordamos que tiene una deuda de deuna",
    "Le recordamos que la venta de mantenimiento está programada para",
    "Gracias por tu tiempo, usuario.",
    "Por favor, espera un momento."
]


async def enviar_correo(destinatario, asunto, mensaje_html, log_output):
    try:
        # Crear el mensaje de correo
        mensaje = MIMEMultipart("alternative")
        mensaje["From"] = f"DevZone <{EMAIL}>"
        mensaje["To"] = destinatario if isinstance(
            destinatario, str) else ", ".join(destinatario)
        mensaje["Subject"] = asunto
        mensaje.attach(MIMEText(mensaje_html, "html"))
        # Enviar el correo
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(EMAIL, PASSWORD)  # Autenticación
            server.sendmail(EMAIL, destinatario,
                            mensaje.as_string())  # Enviar correo
        # Actualizar el log de salida
        log_output.value = f"Correo enviado exitosamente a {destinatario}"
        log_output.update()
    except Exception as e:
        log_output.value = f"Error al enviar el correo: {str(e)}"
        log_output.update()



async def enviar_mensaje(destinatario, mensaje, log_output):
    try:
        # Crear cliente de Telethon
        async with TelegramClient('session_name', API_ID, API_HASH) as client:
            # Verificar si el destinatario es válido
            try:
                entidad = await client.get_entity(destinatario)
            except Exception as e:
                log_output.value = f"El destinatario {destinatario} no es válido: {str(e)}"
                log_output.color = "red"
                log_output.update()
                return False

            # Intentar enviar el mensaje
            try:
                respuesta = await client.send_message(entidad, mensaje)

                # Validar si la respuesta tiene un mensaje válido
                if respuesta and hasattr(respuesta, "id"):
                    log_output.value = f"Mensaje enviado correctamente a {destinatario} (ID: {respuesta.id})"
                    log_output.color = "green"
                    log_output.update()
                    return True
                else:
                    log_output.value = f"Error al verificar el envío del mensaje a {destinatario}."
                    log_output.color = "red"
                    log_output.update()
                    return False
            except Exception as e:
                log_output.value = f"Error enviando mensaje a {destinatario}: {str(e)}"
                log_output.color = "red"
                log_output.update()
                return False

    except Exception as e:
        # Manejar errores generales (red, autenticación, etc.)
        log_output.value = f"Error general: {str(e)}"
        log_output.color = "red"
        log_output.update()
        return False


def main(page: ft.Page):
    page.bgcolor = ft.colors.WHITE
    page.title = "Enviar Mensajes con Telethon"
    page.window_width = 900
    page.window_height = 800

    # Íconos personalizados
    icon_telegram = ft.IconButton(
        # on_click=lambda e: asyncio.run(on_enviar_click(e)),
        on_click=lambda e: asyncio.run(on_enviar_click(e, "telegram")),
        icon=ft.icons.SEND,  # Ícono genérico para Telegram
        icon_color="#00ADB5",     # Color típico de Telegram
        icon_size=40,

    )

    icon_gmail = ft.IconButton(
        # on_click=lambda e: asyncio.run(on_enviar_click(e)),
        on_click=lambda e: asyncio.run(on_enviar_click(e, "correo")),
        icon=ft.icons.EMAIL,  # Ícono genérico para Gmail
        icon_color="#D14836",      # Color típico de Gmail
        icon_size=40
    )

    iconos = ft.Column(
        controls=[
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text("Telegram", color="black",
                                # color=ft.colors.BROWN_700,  # Combina con el fondo ámbar
                                size=12,  # Tamaño de la fuente
                                weight=ft.FontWeight.BOLD,  # Negrita para resaltar
                                font_family="Verdana",  # Fuente legible y moderna

                                ),

                        icon_telegram
                    ],

                ),
                border=ft.border.all(1, ft.Colors.BLACK87),
                border_radius=ft.border_radius.all(10),
                width=150,  # Ancho del contenedor (en píxeles)
                height=50,  # Altura del contenedor (en píxeles)
                alignment=ft.alignment.center,
                padding=ft.padding.only(left=20),
                bgcolor=ft.colors.AMBER_50,
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text("Correo", color="black",

                                size=12,  # Tamaño de la fuente
                                weight=ft.FontWeight.BOLD,  # Negrita para resaltar
                                font_family="Verdana",  # Fuente legible y moderna
                                ),
                        icon_gmail
                    ],
                    spacing=35
                ),
                border=ft.border.all(1, ft.Colors.BLACK87),
                border_radius=ft.border_radius.all(10),
                width=150,  # Ancho del contenedor (en píxeles)
                height=50,  # Altura del contenedor (en píxeles)
                alignment=ft.alignment.center,
                padding=ft.padding.only(left=20),
                bgcolor=ft.colors.AMBER_50,),

        ],
        spacing=20
    )

    titulo_centrado = ft.Container(
        content=ft.Text(
            "APP DE ENVÍO DE MENSAJES FIBRAMAX",
            size=32,
            weight="bold",
            color=ft.colors.AMBER_50,
            text_align="center",
            font_family="Verdana",

        ),
        padding=20,
        bgcolor=ft.colors.BLACK87,  # Fondo oscuro
        border_radius=ft.border_radius.all(12),  # Bordes redondeados
        alignment=ft.alignment.center,
    )

    imagen = ft.Image(src="static/image/logo3.png", width=300, height=200)
    # Crear una instancia de SnackBar con contenido inicial vacío
    snack_bar = ft.SnackBar(content=ft.Text(""))

    mensaje_input = ft.Dropdown(
        label="Selecciona un mensaje",
        options=[
            ft.dropdown.Option(mensaje) for mensaje in mensajes_dropbox
        ],
        width=600,
        height=50,
        focused_border_color=ft.colors.BLACK26,
        border_color=ft.colors.BLACK87,  # Cambia el color del borde cuando no está enfocado
        bgcolor=ft.colors.AMBER_50,  # Cambia el color de fondo de la barra desplegable
        text_style=ft.TextStyle(
            size=14,
            color=ft.colors.BLACK87,
        ),
        label_style=ft.TextStyle(
            color=ft.colors.BLACK87,
            size=12,
        ),
    )

    log_output = ft.Text(value="", color="green")

    def cargar_excel(e):
        global vector_nombre
        global vector_3
        global vector_4
        global vector_deuna
        global df
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
            df["Estado"] = "No enviado"

            # Guardar la tercera y cuarta columna en vectores
            if len(df.columns) >= 4:  # Verificar si hay suficientes columnas
                vector_nombre = df.iloc[:, 1].tolist()
                vector_3 = df.iloc[:, 2].tolist()  # Tercera columna (índice 2)
                vector_4 = df.iloc[:, 3].tolist()  # Cuarta columna (índice 3)
                # Cuarta columna (índice 3)
                vector_deuna = df.iloc[:, 4].tolist()

                print("Tercera columna (vector_3):", vector_3)
                print("Cuarta columna (vector_4):", vector_4)
            else:
                snack_bar.content = ft.Text(
                    "El archivo no tiene suficientes columnas (se requieren al menos 4).")
                snack_bar.open = True
                page.update()
                return

            # Mostrar los datos en la interfaz

              # Crear las columnas y filas para el DataTable
            data_table = ft.DataTable(
                columns=[ 
                    ft.DataColumn(
                        ft.Text(col, weight="bold", size=14, color="white"),
                        tooltip=f"Columna: {col}",
                    )
                    for col in df.columns
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Text(
                                    str(cell),
                                    size=12,
                                    color="black",
                                    tooltip=f"Dato: {cell}"
                                ),
                                on_tap=lambda e, cell=cell: print(f"Seleccionaste: {cell}")
                            )
                            for cell in row
                        ],
                        color=ft.colors.LIGHT_BLUE_50 if i % 2 == 0 else ft.colors.WHITE,
                    )
                    for i, row in enumerate(df.values)
                ],
                border=ft.border.all(1, ft.colors.BLUE_GREY_200),
                heading_row_color=ft.colors.BLUE_GREY_700,
                heading_row_height=40,
                horizontal_margin=10,
                column_spacing=15,
                show_bottom_border=True,
            )

            # Crear un contenedor con desplazamiento y agregar el DataTable
            scrollable_container = ft.Column(
                controls=[data_table],
                scroll=ft.ScrollMode.AUTO,  # Habilitar desplazamiento
                height=300  # Establecer la altura para hacer que el DataTable sea desplazable
            )

        
            page.controls.clear()

            ContaInput = ft.Container(
                content=mensaje_input,
                width=400,
                height=45,
            )

            page.add(titulo_centrado, ft.Text(f"Archivo cargado: {file_path}", color=ft.colors.BLACK87), scrollable_container, ContaInput, iconos, log_output,
                     snack_bar,)
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
        "Cargar archivo Excel",
        on_click=lambda _: file_picker.pick_files(allow_multiple=False),
        color=ft.colors.AMBER_50,  # Texto en blanco para buen contraste
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLACK87,  # Fondo azul que resalta en el fondo negro
            # Bordes redondeados para un diseño moderno
            shape=ft.RoundedRectangleBorder(radius=10),
            elevation=5,  # Sombra ligera para darle profundidad
            # Relleno para un tamaño adecuado
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
        )
    )

    # Agregar el SnackBar y el botón al contenido de la página
    log_output = ft.Text(value="", color="green")

   
    def actualizar_tabla(page):
        global df
        # Crear una nueva tabla basada en el DataFrame actualizado
        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(
                    ft.Text(col, weight="bold", size=14, color="white"),
                    tooltip=f"Columna: {col}",
                )
                for col in df.columns
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                str(cell),
                                size=12,
                                color="black",
                                tooltip=f"Dato: {cell}"
                            ),
                            on_tap=lambda e, cell=cell: print(
                                f"Seleccionaste: {cell}")
                        )
                        for cell in row
                    ],
                    color=ft.colors.LIGHT_BLUE_50 if i % 2 == 0 else ft.colors.WHITE,
                )
                for i, row in enumerate(df.values)
            ],
            border=ft.border.all(1, ft.colors.BLUE_GREY_200),
            heading_row_color=ft.colors.BLUE_GREY_700,
            heading_row_height=40,
            horizontal_margin=10,
            column_spacing=15,
            show_bottom_border=True,
        )

        scrollable_container = ft.Column(
                controls=[data_table],
                scroll=ft.ScrollMode.AUTO,  # Habilitar desplazamiento
                height=300  # Establecer la altura para hacer que el DataTable sea desplazable
            )
     

        # Actualizar la página con la nueva tabla
        page.controls.clear()
        page.add(titulo_centrado, scrollable_container, ft.Text(
            "Actualización completa.", color=ft.colors.BLACK87), mensaje_input, iconos, log_output, snack_bar,)
        page.update()

    
    
  
    async def on_enviar_click(e, metodo_envio):
        global vector_3, vector_4, df, vector_deuna, vector_nombre

        if not vector_3 or (metodo_envio == "correo" and not vector_4):
            log_output.value = "El vector está vacío. Carga un archivo primero."
            log_output.color = "red"
            log_output.update()
            return

        log_output.value = "Iniciando el envío de mensajes..."
        log_output.update()

        global matriz_resultados
        if not matriz_resultados:
            matriz_resultados = [[numero, vector_4[i] if i < len(vector_4) else None, False] for i, numero in enumerate(vector_3)]

      

        for i, fila in enumerate(matriz_resultados):
            numero, destinatario, enviado = fila

            # Solo intentar enviar si no se ha enviado previamente
            if not enviado:
                try:
                    if metodo_envio == "telegram":
                        destinatario = f"+593{numero}"
                    elif metodo_envio == "correo":
                        destinatario = fila[1]

                    if not destinatario:
                        log_output.value = f"Faltan datos para enviar a {numero}."
                        log_output.color = "red"
                        log_output.update()
                        continue

                    mensaje = mensaje_input.value or "Mensaje predeterminado"
                    if mensajes_dropbox.index(mensaje_input.value) == 0 and vector_deuna[i] > 0:
                        mensaje = f"Estimado {vector_nombre[i]}, le recordamos que tiene una deuda de {vector_deuna[i]}"

                    log_output.value = f"Enviando {metodo_envio} a {destinatario}..."
                    log_output.update()

                    if metodo_envio == "telegram":
                        resultado_envio = await enviar_mensaje(destinatario, mensaje, log_output)
                        enviado = bool(resultado_envio)
                        estado_envio = "Enviado a Telegram" if enviado else "No enviado (Telegram)"
                    elif metodo_envio == "correo":
                        asunto = "Asunto predeterminado"
                        html_content = f"<html><body>{mensaje}</body></html>"
                        await enviar_correo(destinatario, asunto, html_content, log_output)
                        enviado = True
                        estado_envio = "Enviado a Correo"

                    # Actualizar estado en el DataFrame y matriz
                    df.at[i, "Estado"] = estado_envio
                    matriz_resultados[i][2] = enviado

                except Exception as ex:
                    df.at[i, "Estado"] = "Mensaje no enviado"
                    log_output.value = f"Error enviando a {destinatario}: {ex}"
                    log_output.color = "red"
                    log_output.update()

        # Actualizar tabla y mostrar resultado final
        actualizar_tabla(page)
        log_output.value = "Envío completado." if all(fila[2] for fila in matriz_resultados) else "Envío completado con errores."
        log_output.update()

        # Mostrar la matriz de resultados
        print("Matriz de resultados:")
        for fila in matriz_resultados:
            print(fila)



  

    ColumnI = ft.Column(
        controls=[
            btn_cargar,
            iconos,
        ],


    )

    RowI = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ColumnI,
            imagen
        ],
    )

    page.add(
        titulo_centrado,
        RowI,
        log_output,
        snack_bar,
    )


ft.app(target=main)
