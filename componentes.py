# IMPORTACIONES
import flet as ft

# COMPONENTE DROPDOWN
def crear_dropdown(opciones, titulo="Selecciona una opción", on_change=None):
    dd = ft.Dropdown(
        label=titulo,
        on_change=on_change,
        options=[ft.dropdown.Option(option[0]) for option in opciones],
        width=200,
    )
    t = ft.Text()
    return dd, t
