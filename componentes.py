import flet as ft

def crear_dropdown(page, opciones, titulo="Selecciona una opción"):
    def dropdown_changed(e):
        t.value = f"Seleccionaste: {dd.value}"
        page.update()
    
    t = ft.Text()
    
    dd = ft.Dropdown(
        label=titulo,
        on_change=dropdown_changed,
        options=[ft.dropdown.Option(option[0]) for option in opciones],
        width=200,
    )
    
    page.add(dd, t)
    