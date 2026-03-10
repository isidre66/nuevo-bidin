import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Informe Radar", layout="wide")

# 1. Recuperar variables (con nombres exactos)
reg_user = st.session_state.get('save_reg_user')
tam_user = st.session_state.get('save_tam_user')

if not st.session_state.get('b1_finalizado'):
    st.warning("⚠️ Primero completa el Bloque 1 y pulsa el botón de Guardar.")
    st.stop()

st.title("🕸️ Radar de Posicionamiento Competitivo")

# 2. Carga de Excel
file_name = "datos.xlsx"
if not os.path.exists(file_name):
    st.error(f"No se encuentra el archivo {file_name}")
    st.stop()

try:
    df = pd.read_excel(file_name)
    # Limpiamos nombres de columnas y datos de espacios invisibles
    df.columns = df.columns.str.strip()
    df['Region'] = df['Region'].astype(str).str.strip()
    df['Tamaño'] = df['Tamaño'].astype(str).str.strip()

    # 3. Filtrado (Normalizando el texto del usuario también)
    val_reg = str(reg_user).strip()
    val_tam = str(tam_user).strip()

    df_reg = df[df['Region'] == val_reg]
    df_tam = df[df['Tamaño'] == val_tam]

    # 4. Preparación de datos (Secretos/Ponderados)
    labels = ['Dpto I+D', 'Presupuesto', 'Gasto Innov.', 'Índice Global']
    
    # Mi Empresa
    empresa = [
        st.session_state.get('score_sub1_1', 0),
        st.session_state.get('score_sub1_2', 0),
        st.session_state.get('score_sub1_3', 0),
        st.session_state.get('score_b1', 0)
    ]
    
    # Media Región
    if not df_reg.empty:
        reg_line = [df_reg['SUB_1.1_Dpto'].mean(), df_reg['SUB_1.2_PresupID'].mean(), df_reg['SUB_1.3_Gasto'].mean(), df_reg['IND_IDi'].mean()]
        nombre_reg = f"Media {val_reg}"
    else:
        reg_line = [0,0,0,0]
        nombre_reg = f"Sin datos en {val_reg}"

    # Media Tamaño
    if not df_tam.empty:
        tam_line = [df_tam['SUB_1.1_Dpto'].mean(), df_tam['SUB_1.2_PresupID'].mean(), df_tam['SUB_1.3_Gasto'].mean(), df_tam['IND_IDi'].mean()]
        nombre_tam = f"Media Tamaño {val_tam}"
    else:
        tam_line = [0,0,0,0]
        nombre_tam = f"Sin datos para tamaño {val_tam}"

    # 5. Gráfico Radar
    fig = go.Figure()

    # Capa Mi Empresa
    fig.add_trace(go.Scatterpolar(r=empresa, theta=labels, fill='toself', name='Mi Empresa', line_color='#1E3A8A'))
    
    # Capa Región
    fig.add_trace(go.Scatterpolar(r=reg_line, theta=labels, name=nombre_reg, line_color='#10B981'))
    
    # Capa Tamaño
    fig.add_trace(go.Scatterpolar(r=tam_line, theta=labels, name=nombre_tam, line_color='#F59E0B'))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        showlegend=True,
        height=600,
        title="Comparativa Multinivel"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Ayuda visual para depuración (Solo si hay errores)
    if df_reg.empty or df_tam.empty:
        with st.expander("Ayuda técnica: ¿Por qué no salen las otras líneas?"):
            st.write(f"Buscando Región: '{val_reg}'")
            st.write(f"Buscando Tamaño: '{val_tam}'")
            st.write("Valores disponibles en Excel (Región):", df['Region'].unique())
            st.write("Valores disponibles en Excel (Tamaño):", df['Tamaño'].unique())

except Exception as e:
    st.error(f"Error crítico: {e}")