"""
AJUSTADOR DE PROMEDIOS — datos.xlsx
Genera datos_corregido.xlsx sin tocar el original.
"""
import pandas as pd
import numpy as np
import os

# ══════════════════════════════════════════════════════
# AJUSTES CONFIGURADOS
# ══════════════════════════════════════════════════════
AJUSTES = {
    'Var_Ventas_5a':   30.0,     # media actual: 62.0
    'Var_Emp_5a':      20.0,     # media actual: 48.0
    'Prod_Venta_Emp':  60000.0,  # media actual: 228.459
    'Coste_Med_Emp':   35000.0,  # media actual: 46.771
    'ROA':             8.0,      # media actual: 8.04 — apenas cambia
}

FACTOR_DISPERSION = 1.0   # 1.0 = misma dispersión, solo se traslada la media
RESPETAR_RANGO    = False  # False para permitir nuevos rangos realistas
DECIMALES         = 2

# ══════════════════════════════════════════════════════
# LÓGICA — no tocar
# ══════════════════════════════════════════════════════
def ajustar(serie, objetivo, factor, decimales):
    nueva = objetivo + (serie - serie.mean()) * factor
    if decimales is not None:
        nueva = nueva.round(decimales)
    return nueva

def main():
    script_dir   = os.path.dirname(os.path.abspath(__file__))
    ruta_entrada = os.path.join(script_dir, 'datos.xlsx')
    ruta_salida  = os.path.join(script_dir, 'datos_corregido.xlsx')

    if not os.path.exists(ruta_entrada):
        print(f"ERROR: No se encuentra datos.xlsx en {script_dir}")
        return

    print(f"Cargando {ruta_entrada} ...")
    df = pd.read_excel(ruta_entrada)
    df.columns = df.columns.str.strip()
    print(f"{len(df)} empresas cargadas.\n")

    print(f"{'COLUMNA':<22} {'MEDIA ACTUAL':>14} {'OBJETIVO':>12} {'DIFERENCIA':>12}")
    print("─" * 62)
    cols_ok = []
    for col, obj in AJUSTES.items():
        if col not in df.columns:
            print(f"  !! '{col}' no encontrada — omitida"); continue
        ma = df[col].mean()
        print(f"  {col:<20} {ma:>14.2f} {obj:>12.2f} {'▼' if obj<ma else '▲'} {obj-ma:>+10.2f}")
        cols_ok.append(col)
    print("─" * 62)

    if not cols_ok:
        print("No hay columnas válidas."); return

    ok = input("\n¿Aplicar y guardar datos_corregido.xlsx? (s/n): ")
    if ok.strip().lower() != 's':
        print("Cancelado."); return

    df_nuevo = df.copy()
    for col in cols_ok:
        df_nuevo[col] = ajustar(df[col], AJUSTES[col], FACTOR_DISPERSION, DECIMALES)

    df_nuevo.to_excel(ruta_salida, index=False)

    print(f"\nARCHIVO GUARDADO: {ruta_salida}\n")
    print(f"{'COLUMNA':<22} {'ORIGINAL':>12} {'NUEVO':>12} {'OBJETIVO':>12}  OK?")
    print("─" * 62)
    for col in cols_ok:
        mo = df[col].mean(); mn = df_nuevo[col].mean(); ob = AJUSTES[col]
        ok2 = "✓" if abs(mn-ob) < abs(ob)*0.01+0.5 else "revisar"
        print(f"  {col:<20} {mo:>12.2f} {mn:>12.2f} {ob:>12.2f}  {ok2}")

    print("\nPASOS SIGUIENTES:")
    print("  1. Abre datos_corregido.xlsx y comprueba que los valores tienen sentido")
    print("  2. Si todo OK → renombra datos.xlsx  a  datos_backup.xlsx")
    print("  3. Renombra datos_corregido.xlsx  a  datos.xlsx")
    print("  4. Reinicia Streamlit")

if __name__ == '__main__':
    main()