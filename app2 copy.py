import flet as ft
from telethon import TelegramClient
import asyncio
import pandas as pd
# Credenciales obtenidas de my.telegram.org
API_ID = '11693772'
API_HASH = 'a7ef421e8d6d4435dc4b1fc37260236a'


# Variables globales
df = None
vector_3 = []
vector_4 = []


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

    page.bgcolor = ft.colors.WHITE
    page.title = "Enviar Mensajes con Telethon"
    page.window_width = 1200
    page.window_height = 800

    # Íconos personalizados
    icon_telegram = ft.IconButton(
        on_click=lambda e: asyncio.run(on_enviar_click(e)),
        icon=ft.icons.SEND,  # Ícono genérico para Telegram
        icon_color="#00ADB5",     # Color típico de Telegram
        icon_size=40,

    )

    icon_gmail = ft.Icon(
        name=ft.icons.EMAIL,  # Ícono genérico para Gmail
        color="#D14836",      # Color típico de Gmail
        size=40
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
                        ft.Text("Gmail", color="black",

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

    mensaje_input = ft.TextField(
        label="Mensaje a enviar", multiline=True, width=200, height=100,
        focused_border_color=ft.colors.BLACK87,
        text_style=ft.TextStyle(
            size=14,  # Tamaño del texto del input
            color=ft.colors.BLACK87,  # Texto en negro suave para mejor legibilidad
        ),

        label_style=ft.TextStyle(
            color=ft.colors.BLACK87,  # Color del texto de la etiqueta
            size=12,  # Tamaño moderado para la etiqueta
        ),
    )

    log_output = ft.Text(value="", color="green")

    def cargar_excel(e):
        global vector_3
        global vector_4
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
                vector_3 = df.iloc[:, 2].tolist()  # Tercera columna (índice 2)
                vector_4 = df.iloc[:, 3].tolist()  # Cuarta columna (índice 3)

                print("Tercera columna (vector_3):", vector_3)
                print("Cuarta columna (vector_4):", vector_4)
            else:
                snack_bar.content = ft.Text(
                    "El archivo no tiene suficientes columnas (se requieren al menos 4).")
                snack_bar.open = True
                page.update()
                return

            # Mostrar los datos en la interfaz
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

            # Limpiar el contenido de la página y mostrar la tabla
            page.controls.clear()
            ContainerDT = ft.Container(
                content=data_table,
                alignment=ft.alignment.center
            )

            # ColumnTa = ft.Column(
            #     controls=[
            #         mensaje_input,
            #         iconos,

            #     ]
            # )

            page.add(titulo_centrado, data_table, mensaje_input, ft.Text(f"Archivo cargado: {file_path}", color=ft.colors.BLACK87), iconos, log_output,
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

    global numero_envio
    numero_envio = "995365458"

    # async def on_enviar_click(e):
    #     destinatario = "+593"+numero_envio
    #     mensaje = mensaje_envio
    #     if destinatario and mensaje:
    #         log_output.value = "Enviando mensaje..."
    #         log_output.update()
    #         await enviar_mensaje(destinatario, mensaje, log_output)
    #     else:
    #         log_output.value = "Por favor, completa todos los campos."
    #         log_output.color = "red"
    #         log_output.update()

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

        # Actualizar la página con la nueva tabla
        page.controls.clear()
        page.add(titulo_centrado, data_table, ft.Text(
            "Actualización completa.", color=ft.colors.BLACK87), iconos, log_output, snack_bar,)
        page.update()

    async def on_enviar_click(e):
        global vector_3, df  # Usar el DataFrame y el vector globales

        if not vector_3:
            log_output.value = "El vector está vacío. Carga un archivo primero."
            log_output.color = "red"
            log_output.update()
            return

        log_output.value = "Iniciando el envío de mensajes..."
        log_output.update()

        for i, numero in enumerate(vector_3):
            destinatario = f"+593{numero}"  # Formatear el número
           # mensaje = vector_4[i] if i < len(vector_4) else "Mensaje predeterminado"  # Mensaje asociado
            mensaje = "Mensaje predeterminado"
            mensaje = mensaje_input.value
            if destinatario and mensaje:
                log_output.value = f"Enviando mensaje a {destinatario}..."
                log_output.update()
                try:
                    # Llamar a la función de envío
                    await enviar_mensaje(destinatario, mensaje, log_output)
                    # Actualizar el estado en el DataFrame
                    df.at[i, "Estado"] = "Enviado"
                    log_output.value = f"Mensaje enviado a {destinatario}."
                except Exception as ex:
                    # Registrar error si ocurre
                    df.at[i, "Estado"] = f"Error: {ex}"
                    log_output.value = f"Error enviando a {destinatario}: {ex}"
                    log_output.color = "red"

                log_output.update()
            else:
                log_output.value = f"Faltan datos para enviar a {numero}."
                log_output.color = "red"
                log_output.update()

        # Refrescar la tabla para mostrar los nuevos estados
        actualizar_tabla(page)
        log_output.value = "Envío completado."
        log_output.update()

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
