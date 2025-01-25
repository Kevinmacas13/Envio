import flet as ft
import pandas as pd

def main(page: ft.Page):
    page.title = "Cargar archivo Excel"

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
                    ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row])
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
    btn_cargar = ft.ElevatedButton("Cargar archivo Excel", on_click=lambda _: file_picker.pick_files(allow_multiple=False))
    
    # Agregar el SnackBar y el botón al contenido de la página
    page.add(snack_bar, btn_cargar)

# Ejecutar la aplicación
if __name__ == "__main__":
    ft.app(target=main)
