"""
IMPORTADOR EXCEL → SUPABASE
Importa las 1.000 empresas del Excel datos.xlsx a Supabase.
Ejecutar UNA SOLA VEZ desde la raíz: python importar_excel_supabase.py
"""
import pandas as pd
import os, sys, time
 
# ── Configuración ────────────────────────────────────────
EXCEL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datos.xlsx')
SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')
 
# Leer credenciales del .env si no están en variables de entorno
ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
if os.path.exists(ENV_FILE):
    with open(ENV_FILE) as f:
        for line in f:
            if line.startswith('SUPABASE_URL'):
                SUPABASE_URL = line.split('=',1)[1].strip().strip('"')
            elif line.startswith('SUPABASE_KEY'):
                SUPABASE_KEY = line.split('=',1)[1].strip().strip('"')
 
if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: No se encontraron las credenciales de Supabase.")
    print("Añade al archivo .env:")
    print('SUPABASE_URL = "https://..."')
    print('SUPABASE_KEY = "eyJ..."')
    sys.exit(1)
 
from supabase import create_client
sb = create_client(SUPABASE_URL, SUPABASE_KEY)
 
# ── Columnas de clasificación y económicas ───────────────
COLS_EMPRESA = {
    'ID':                  'id',
    'Macrosector':         'macrosector',
    'Sector':              'sector',
    'Tamaño':              'tamano',
    'Exportacion':         'exportacion',
    'Antigüedad':          'antiguedad',
    'Region':              'region',
    'Cluster':             'cluster',
    'Ventas':              'ventas',
    'Empleados':           'empleados',
    'ROA':                 'roa',
    'Var_Ventas_5a':       'var_ventas_5a',
    'Var_Emp_5a':          'var_emp_5a',
    'Prod_Venta_Emp':      'prod_venta_emp',
    'Coste_Med_Emp':       'coste_med_emp',
    'Ratio_Endeudamiento': 'ratio_endeudamiento',
}
 
# Todas las demás columnas son indicadores del módulo innovación
COLS_SKIP = set(COLS_EMPRESA.keys())
 
def main():
    print("=" * 60)
    print("  IMPORTADOR EXCEL → SUPABASE")
    print("=" * 60)
 
    # Leer Excel
    print(f"\n📂 Leyendo {EXCEL_FILE}...")
    df = pd.read_excel(EXCEL_FILE)
    print(f"  → {len(df)} empresas, {len(df.columns)} columnas")
 
    # Columnas de indicadores
    cols_indicadores = [c for c in df.columns if c not in COLS_SKIP]
    print(f"  → {len(cols_indicadores)} indicadores de innovación")
 
    errores = 0
    importadas = 0
 
    for i, row in df.iterrows():
        empresa_id = str(row['ID'])
 
        # ── 1. Insertar empresa ──────────────────────────
        empresa_data = {
            'id':                  empresa_id,
            'macrosector':         int(row['Macrosector'])          if pd.notna(row.get('Macrosector')) else None,
            'sector':              int(row['Sector'])               if pd.notna(row.get('Sector')) else None,
            'tamano':              int(row['Tamaño'])               if pd.notna(row.get('Tamaño')) else None,
            'exportacion':         int(row['Exportacion'])          if pd.notna(row.get('Exportacion')) else None,
            'antiguedad':          int(row['Antigüedad'])           if pd.notna(row.get('Antigüedad')) else None,
            'region':              int(row['Region'])               if pd.notna(row.get('Region')) else None,
            'cluster':             str(row['Cluster'])              if pd.notna(row.get('Cluster')) else None,
            'ventas':              float(row['Ventas'])             if pd.notna(row.get('Ventas')) else None,
            'empleados':           int(row['Empleados'])            if pd.notna(row.get('Empleados')) else None,
            'roa':                 float(row['ROA'])                if pd.notna(row.get('ROA')) else None,
            'var_ventas_5a':       float(row['Var_Ventas_5a'])      if pd.notna(row.get('Var_Ventas_5a')) else None,
            'var_emp_5a':          float(row['Var_Emp_5a'])         if pd.notna(row.get('Var_Emp_5a')) else None,
            'prod_venta_emp':      float(row['Prod_Venta_Emp'])     if pd.notna(row.get('Prod_Venta_Emp')) else None,
            'coste_med_emp':       float(row['Coste_Med_Emp'])      if pd.notna(row.get('Coste_Med_Emp')) else None,
            'ratio_endeudamiento': float(row['Ratio_Endeudamiento'])if pd.notna(row.get('Ratio_Endeudamiento')) else None,
            'validada':            True,
            'es_nueva':            False,
            'pendiente_validar':   False,
        }
 
        try:
            sb.table('benchmark_empresas').upsert(empresa_data).execute()
        except Exception as e:
            print(f"  ERROR empresa {empresa_id}: {e}")
            errores += 1
            continue
 
        # ── 2. Insertar indicadores ──────────────────────
        indicadores = []
        for col in cols_indicadores:
            val = row.get(col)
            if pd.notna(val):
                indicadores.append({
                    'empresa_id': empresa_id,
                    'modulo':     'innovacion',
                    'indicador':  col,
                    'valor':      float(val)
                })
 
        if indicadores:
            try:
                # Insertar en lotes de 50
                for j in range(0, len(indicadores), 50):
                    sb.table('benchmark_indicadores').upsert(
                        indicadores[j:j+50],
                        on_conflict='empresa_id,modulo,indicador'
                    ).execute()
            except Exception as e:
                print(f"  ERROR indicadores {empresa_id}: {e}")
                errores += 1
                continue
 
        importadas += 1
        if importadas % 100 == 0:
            print(f"  → {importadas}/{len(df)} empresas importadas...")
        time.sleep(0.05)  # pequeña pausa para no saturar la API
 
    print(f"\n{'=' * 60}")
    print(f"✅ Importación completada:")
    print(f"   → {importadas} empresas importadas correctamente")
    if errores:
        print(f"   → {errores} errores")
    print(f"{'=' * 60}")
 
if __name__ == '__main__':
    main()