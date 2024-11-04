# IMPORTACIONES
import flet as ft
import sqlite3
from componentes import crear_dropdown

def main(page: ft.Page):
    # CONECTOR A BASE app.db
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # DATOS PARA LOS DROPDOWNS
    cursor.execute("SELECT DISTINCT TIPO_ESCALA FROM modulacion")
    TIPO_ESCALA_Q = cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT TONALIDAD FROM modulacion")
    TONALIDAD_Q = cursor.fetchall()

    # CONSULTA GENERAL, PARAMETRO 1 = TIPO_ESCALA, PARAMETRO 2 = TONALIDAD
    sql_tabla = """
    SELECT TIPO_DATO, ATRIBUTO, VALOR 
    FROM modulacion 
    WHERE TIPO_ESCALA = ? AND TONALIDAD = ?
    """

    # TABLA NULL POR DEFAULT
    table = ft.DataTable(
        columns=[ft.DataColumn(ft.Text("No hay datos disponibles"))],
        rows=[],
        visible=False
    )
    message = ft.Text()

    # FUNCION PARA ACTUALIZAR LA TABLA
    def actualizar_tabla(e):
        valor_dd1 = dd1.value
        valor_dd2 = dd2.value

        if valor_dd1 and valor_dd2:
            cursor.execute(sql_tabla, (valor_dd1, valor_dd2))
            rows = cursor.fetchall()

            if rows:
                tipo_datos_order = [
                    'DIST. INTERVÁLICA',
                    'TIPO DE ACORDE',
                    'FUNCIÓN',
                    'ACORDES',
                    'NOTAS DEL ACORDE',
                    'MODO (ESCALA)',
                    'NOTAS DEL MODO',
                    'EXTENSIÓN DISPONIBLE',
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

                # COLUMNAS
                columns = [ft.DataColumn(ft.Text(""))]
                for atributo in atributos:
                    columns.append(ft.DataColumn(ft.Text(atributo)))

                # FILAS
                data_rows = []
                for tipo_dato in tipo_datos:
                    cells = [ft.DataCell(ft.Text(tipo_dato))]
                    for atributo in atributos:
                        valor = data.get((tipo_dato, atributo), "")
                        cells.append(ft.DataCell(ft.Text(str(valor))))
                    data_rows.append(ft.DataRow(cells=cells))

                # ACTUALIZAR LA TABLA CON LOS DATOS
                table.columns = columns
                table.rows = data_rows
                table.visible = True
                message.value = ""
            else:
                table.rows = []
                table.visible = True
                message.value = "No hay resultados para las opciones seleccionadas."

            page.update()
        else:
            # VALORES NULOS => OCULTAR TABLA
            table.visible = False
            message.value = ""
            page.update()

    # CREA LOS DROPDOWNS Y LLAMA A componentes.py
    dd1, t1 = crear_dropdown(
        TIPO_ESCALA_Q, 
        titulo="Elige una escala", 
        on_change=actualizar_tabla
    )
    dd2, t2 = crear_dropdown(
        TONALIDAD_Q, 
        titulo="Elige una tonalidad", 
        on_change=actualizar_tabla
    )
    
    # AGREGAR TODOS LOS COMPONENTES A LA PAGINA
    page.add(dd1, dd2, message, table)
    
    # MANTIENE LA CONEXION DURANTE LA SESION
    page.on_close = lambda e: conn.close()

ft.app(target=main)