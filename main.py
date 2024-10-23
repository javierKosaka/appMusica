# IMPORTAIONES
import flet as ft
import sqlite3

# --- INICIO FUNCION MAIN---
def main(page: ft.Page):
    # OJO: BASE DE DESARROLLO
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # RESTA CONVERTIR LOS VALUES DE TIPO_ESCALA Y TONALIDAD EN VARIABLES.  PASAR COMO PARAMETRO DESDE UN SELECTOR.
    cursor.execute("""
        SELECT TIPO_DATO, ATRIBUTO, VALOR
        FROM modulacion
        WHERE TIPO_ESCALA = 'MENOR MELODICA' AND TONALIDAD = 'B'
    """)
    rows = cursor.fetchall()

    # Criterios de orden y ordenar
    tipo_datos_order = [
        'DIST. INTERVÁLICA',
        'TIPO DE ACORDE',
        'FUNCIÓN',
        'ACORDES',
        'NOTAS DEL ACORDE',
        'MODO (ESCALA)',
        'NOTAS DEL MODO',
        'EXTENSION DISPONIBLE',
        'NOTAS DE LA EXTENSIÓN',
        'RELATIVO MENOR',
        'DOM. SECUNDARIO',
        'MENOR ARMÓNICA',
        'MENOR MELÓDICA',
        'SUSTITUTO TRITONAL',
        'TWO - FIVE (II-V)',
        'TWO - FIVE (Tritono)'
    ]
    
    tipo_datos = [td for td in tipo_datos_order if any(row[0] == td for row in rows)]

    atributos = sorted(set(row[1] for row in rows))

    data = {}
    for row in rows:
        tipo_dato, atributo, valor = row
        data[(tipo_dato, atributo)] = valor

    # columnas =  ATRIBUTO
    columns = [ft.DataColumn(ft.Text("Tipo de dato / Atributo"))]
    for atributo in atributos:
        columns.append(ft.DataColumn(ft.Text(atributo)))

    # filas = TIPO_DATOS
    data_rows = []
    for tipo_dato in tipo_datos:
        cells = [ft.DataCell(ft.Text(tipo_dato))]
        for atributo in atributos:
            valor = data.get((tipo_dato, atributo), "")
            cells.append(ft.DataCell(ft.Text(str(valor))))
        data_rows.append(ft.DataRow(cells=cells))

    # Agrega tabla a la pagina
    table = ft.DataTable(columns=columns, rows=data_rows)
    page.add(table)
    
# --- FIN FUNCION MAIN ---

ft.app(target=main)
