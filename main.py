import flet as ft
import os

COLOR_APAGADO = "#1a1a2e"   
COLOR_ENCENDIDO = "#39ff14" 

def main(page: ft.Page):
    
    page.title = "Editor de Sprites 8x8 - Electrónica Digital"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 520
    page.window.height = 750
    page.window.resizable = False
    page.padding = 20

    
    texto_hex = ft.Text(
        value="0000000000000000",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=COLOR_ENCENDIDO,
        font_family="Courier New",
    )


    grid_botones = []  

        
    def actualizar_hex():
        print("actualizar_hex fue llamada")
        cadena_binaria = ""
        for fila_botones in grid_botones:
            for boton in fila_botones:
                if boton.bgcolor == COLOR_ENCENDIDO:
                    cadena_binaria += "1"
                else:
                    cadena_binaria += "0"

        valor_entero = int(cadena_binaria, 2)
        valor_hex = format(valor_entero, "016X")

        texto_hex.value = valor_hex
        page.update()

        
    def cargar_hex(e):
        texto_ingresado = campo_entrada.value.strip().upper()

        
        if len(texto_ingresado) > 16:
            campo_entrada.error_text = "Máximo 16 caracteres"
            page.update()
            return

        caracteres_validos = set("0123456789ABCDEF")
        if not all(c in caracteres_validos for c in texto_ingresado):
            campo_entrada.error_text = "Solo caracteres hexadecimales (0-9, A-F)"
            page.update()
            return

        campo_entrada.error_text = None  

        
        if texto_ingresado == "":
            valor_entero = 0
        else:
            valor_entero = int(texto_ingresado, 16)

        cadena_binaria = format(valor_entero, "064b")  # 64 caracteres, rellena con ceros

        
        indice = 0
        for fila_botones in grid_botones:
            for boton in fila_botones:
                bit = cadena_binaria[indice]
                if bit == "1":
                    boton.bgcolor = COLOR_ENCENDIDO
                else:
                    boton.bgcolor = COLOR_APAGADO
                indice += 1

        texto_hex.value = format(valor_entero, "016X")
        page.update()
    

    def click_pixel(e):
        contenedor = e.control
        if contenedor.bgcolor == COLOR_APAGADO:
            contenedor.bgcolor = COLOR_ENCENDIDO
        else:
            contenedor.bgcolor = COLOR_APAGADO
        actualizar_hex()  
    


    for fila in range(8):
        fila_botones = []
        for columna in range(8):
            boton = ft.Container(
                width=40,
                height=40,
                bgcolor=COLOR_APAGADO,
                border_radius=4,
                border=ft.Border.all(width=1, color="#333355"),
                on_click=click_pixel,
                ink=True,  # efecto visual al hacer clic
            )
            fila_botones.append(boton)
        grid_botones.append(fila_botones)

    filas_visuales = [
        ft.Row(fila_botones, spacing=4)
        for fila_botones in grid_botones
    ]

    cuadricula = ft.Column(filas_visuales, spacing=4)

    

    campo_entrada = ft.TextField(
        label="Código Hexadecimal",
        hint_text="Ej: FF00FF00FF00FF00",
        width=300,
    )

    boton_cargar = ft.ElevatedButton(
        content="Cargar Hex",
        on_click= cargar_hex,
    )

    panel_control = ft.Column(
        [
            ft.Row([campo_entrada, boton_cargar], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([texto_hex], alignment=ft.MainAxisAlignment.CENTER),
        ],
        spacing=15,
    )

    page.add(
        ft.Column(
            [
                cuadricula,
                ft.Divider(),
                panel_control,
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=int(os.environ.get("PORT", 8550)))