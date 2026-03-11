import os

PAGES = r"C:\Users\isidr\Desktop\NUEVO BIDIN\pages"

RENOMBRAR = {
    '_Actividades_IDi.py':       '10_Bloque_1_IDi.py',
    '2_Gestion_Proyectos.py':    '11_Bloque_2_Gestion_Proyectos.py',
    '3_Estrategia.py':           '12_Bloque_3_Desarrollo_Productos.py',
    '_Desarrollo_Productos.py':  '13_Bloque_4_Estrategia_Innovacion.py',
    '6_Indices_Estrategicos.py': '20_Indices_Estrategicos.py',
    '7_Informe_Estrategico.py':  '21_Informe_Estrategico.py',
    '8_Informe_Innovacion.py':   '22_Informe_Innovacion.py',
    '9_Informe_Global.py':       '23_Informe_Global.py',
    '5_Analytics.py':            '24_Analytics.py',
    '10_Benchmarking.py':        '25_Benchmarking.py',
    '11_Plan_Accion.py':         '26_Plan_Accion.py',
}

for viejo, nuevo in RENOMBRAR.items():
    ruta_vieja = os.path.join(PAGES, viejo)
    ruta_nueva = os.path.join(PAGES, nuevo)
    if os.path.exists(ruta_vieja):
        os.rename(ruta_vieja, ruta_nueva)
        print("OK:", viejo)
    else:
        print("No encontrado:", viejo)

print("LISTO")