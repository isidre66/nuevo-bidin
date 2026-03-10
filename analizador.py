import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuración de la página
st.set_page_config(layout="wide", page_title="Diagnóstico Maestro")

# 1. Localización del archivo
ruta_actual = os.path.dirname(os.path.abspath(__file__))
archivo_excel = os.path.join(ruta_actual, 'datos.xlsx')

st.title("🏆 Plataforma de Diagnóstico: 1.000 Empresas")

try:
    # 2. Carga de datos
    df = pd.read_excel(archivo_excel, engine='openpyxl')
    df.columns = df.columns.str.strip()
    
    # Identificar columnas automáticamente
    col_reg = [c for c in df.columns if 'egi' in c.lower()][0]
    col_vta = [c for c in df.columns if 'enta' in c.lower()][0]
    col_inn = [c for c in df.columns if 'INNO' in c.upper()][0]

    # Limpiar datos numéricos
    df[col_vta] = pd.to_numeric(df[col_vta], errors='coerce')
    df = df.dropna(subset=[col_vta])

    # --- BLOQUE DE DIAGNÓSTICO ---
    with st.container():
        st.subheader("📝 Introduce tus datos para el Diagnóstico")
        col1, col2, col3 = st.columns(3)
        
        mi_venta = col1.number_input("Tus Ventas:", value=5000.0)
        mi_inno = col2.slider("Tu Innovación:", 1, 100, 50)
        mi_region = col3.selectbox("Comparar con Región:", sorted(df[col_reg].unique()))

        if st.button("🚀 REALIZAR DIAGNÓSTICO"):
            media = df[df[col_reg] == mi_region][col_vta].mean()
            if mi_venta >= media:
                st.success(f"✅ Estás POR ENCIMA de la media en la {mi_region}.")
            else:
                st.warning(f"⚠️ Estás POR DEBAJO de la media. Te faltan {media - mi_venta:,.0f} para alcanzarla.")

    # --- GRÁFICO ---
    st.markdown("---")
    fig = px.scatter(df, x=col_inn, y=col_vta, color=col_reg, 
                     title="Mapa Competitivo del Sector", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error al cargar el Excel: {e}")
    st.info("Asegúrate de que 'datos.xlsx' está en la misma carpeta que este código.")