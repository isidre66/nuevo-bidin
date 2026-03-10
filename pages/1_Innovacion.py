import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Dashboard Innovación · Bloque 1", layout="wide")

if not st.session_state.get('b1_finalizado'):
    st.warning("⚠️ Primero completa el Bloque 1 (Actividades I+D+i) y pulsa Guardar.")
    st.stop()

if not st.session_state.get('save_reg_user'):
    st.warning("⚠️ Primero completa tu perfil de empresa en la página de Inicio.")
    st.stop()

# Valores numéricos para filtrar el Excel
val_reg = st.session_state.get('save_reg_user', '')
val_tam = st.session_state.get('save_tam_user', '')

# Nombres para mostrar en gráficos
nom_reg = st.session_state.get('save_reg_nombre', str(val_reg))
nom_tam = st.session_state.get('save_tam_nombre', str(val_tam))

# Cargar Excel
ruta_excel = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datos.xlsx')
if not os.path.exists(ruta_excel):
    ruta_excel = "datos.xlsx"

try:
    df = pd.read_excel(ruta_excel)
    df.columns = df.columns.str.strip()

    # Filtrar por códigos numéricos
    df_reg = df[df['Region'] == val_reg]
    df_tam = df[df['Tamaño'] == val_tam]

    # Puntuaciones empresa
    empresa = {
        'SUB_1.1_Dpto':     st.session_state.get('score_sub1_1', 0),
        'SUB_1.2_PresupID': st.session_state.get('score_sub1_2', 0),
        'SUB_1.3_Gasto':    st.session_state.get('score_sub1_3', 0),
        'IND_IDi':          st.session_state.get('score_b1', 0),
    }

    cols = ['SUB_1.1_Dpto', 'SUB_1.2_PresupID', 'SUB_1.3_Gasto', 'IND_IDi']
    media_reg = {c: df_reg[c].mean() if not df_reg.empty else 0 for c in cols}
    media_tam = {c: df_tam[c].mean() if not df_tam.empty else 0 for c in cols}
    media_tot = {c: df[c].mean() for c in cols}

    labels_cortos = ['Dpto I+D', 'Presupuesto I+D', 'Gasto Innovación', 'Índice Global']

    # CABECERA
    st.title("📊 Dashboard · Bloque 1: Actividades de I+D+i")
    st.markdown(f"Comparativa de **{st.session_state.get('save_sector_nombre','tu empresa')}** · "
                f"Región: **{nom_reg}** · Tamaño: **{nom_tam}**")
    st.divider()

    # MÉTRICAS RÁPIDAS
    st.markdown("### 🎯 Tu puntuación vs. la competencia")
    m1, m2, m3, m4 = st.columns(4)
    for col_met, label, met in zip([m1, m2, m3, m4], labels_cortos, cols):
        val_emp  = empresa[met]
        val_ref  = media_reg[met]
        diferencia = val_emp - val_ref
        col_met.metric(
            label=label,
            value=f"{val_emp:.2f} / 5",
            delta=f"{diferencia:+.2f} vs media {nom_reg}"
        )

    st.divider()

    # RADAR + BARRAS
    col_radar, col_barras = st.columns(2)

    with col_radar:
        st.markdown("#### 🕸️ Radar Comparativo")
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[empresa[c] for c in cols], theta=labels_cortos,
            fill='toself', name='Mi Empresa', line_color='#1E3A8A'))
        fig_radar.add_trace(go.Scatterpolar(
            r=[media_reg[c] for c in cols], theta=labels_cortos,
            name=f'Media {nom_reg}', line_color='#10B981'))
        fig_radar.add_trace(go.Scatterpolar(
            r=[media_tam[c] for c in cols], theta=labels_cortos,
            name=f'Media {nom_tam}', line_color='#F59E0B'))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=True, height=400)
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_barras:
        st.markdown("#### 📊 Comparativa por Subindicador")
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name='Mi Empresa',
            x=labels_cortos, y=[empresa[c] for c in cols], marker_color='#1E3A8A'))
        fig_bar.add_trace(go.Bar(name=f'Media {nom_reg}',
            x=labels_cortos, y=[media_reg[c] for c in cols], marker_color='#10B981'))
        fig_bar.add_trace(go.Bar(name=f'Media {nom_tam}',
            x=labels_cortos, y=[media_tam[c] for c in cols], marker_color='#F59E0B'))
        fig_bar.add_trace(go.Bar(name='Media Total',
            x=labels_cortos, y=[media_tot[c] for c in cols], marker_color='#94A3B8'))
        fig_bar.update_layout(
            barmode='group', height=400,
            yaxis=dict(range=[0, 5]),
            legend=dict(orientation='h', yanchor='bottom', y=1.02))
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # TABLA RESUMEN
    st.markdown("### 📋 Tabla Resumen de Puntuaciones")
    tabla = pd.DataFrame({
        'Indicador / Subindicador': labels_cortos,
        'Mi Empresa':              [f"{empresa[c]:.2f}" for c in cols],
        f'Media {nom_reg}':        [f"{media_reg[c]:.2f}" for c in cols],
        f'Media {nom_tam}':        [f"{media_tam[c]:.2f}" for c in cols],
        'Media Total':             [f"{media_tot[c]:.2f}" for c in cols],
    })
    st.dataframe(tabla, use_container_width=True, hide_index=True)

    st.divider()

    # DIAGNÓSTICO AUTOMÁTICO
    st.markdown("### 💡 Diagnóstico Automático")
    idx = empresa['IND_IDi']
    ref = media_reg['IND_IDi']
    if idx >= 4:
        st.success(f"✅ **Posición DESTACADA** — Tu índice global es **{idx:.2f}/5**, "
                   f"por encima de la media de {nom_reg} ({ref:.2f}).")
    elif idx >= ref:
        st.info(f"👍 **POR ENCIMA de la media** — Tu índice es **{idx:.2f}/5** "
                f"frente a una media de {nom_reg} de {ref:.2f}.")
    elif idx >= ref * 0.85:
        st.warning(f"⚠️ **PRÓXIMO a la media** — Tu índice es **{idx:.2f}/5** "
                   f"frente a una media de {nom_reg} de {ref:.2f}. "
                   f"Te faltan {ref - idx:.2f} puntos.")
    else:
        st.error(f"🔴 **POR DEBAJO de la media** — Tu índice es **{idx:.2f}/5** "
                 f"frente a una media de {nom_reg} de {ref:.2f}.")

    st.divider()
    st.caption("💡 Completa más bloques para obtener un diagnóstico más completo.")

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")