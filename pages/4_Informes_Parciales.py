import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import os

st.set_page_config(page_title="Informes Parciales", layout="wide")

# ── Cargar perfil local ───────────────────────────────────────────────────────
PERFIL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'perfil_empresa.json')

def cargar_perfil():
    if os.path.exists(PERFIL_FILE):
        with open(PERFIL_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

perfil = cargar_perfil()
for k, v in perfil.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Verificar perfil ──────────────────────────────────────────────────────────
if not st.session_state.get('save_reg_user'):
    st.warning("⚠️ Primero completa tu perfil de empresa en la página de Inicio.")
    st.stop()

# ── Datos de la empresa ───────────────────────────────────────────────────────
val_reg  = st.session_state.get('save_reg_user', '')
val_tam  = st.session_state.get('save_tam_user', '')
nom_reg  = st.session_state.get('save_reg_nombre', str(val_reg))
nom_tam  = st.session_state.get('save_tam_nombre', str(val_tam))
sector   = st.session_state.get('save_sector_nombre', 'Tu empresa')

# ── Cargar Excel ──────────────────────────────────────────────────────────────
ruta_excel = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datos.xlsx')
if not os.path.exists(ruta_excel):
    ruta_excel = "datos.xlsx"

try:
    df = pd.read_excel(ruta_excel)
    df.columns = df.columns.str.strip()
    df_reg = df[df['Region'] == val_reg]
    df_tam = df[df['Tamaño'] == val_tam]
except:
    df = df_reg = df_tam = None

def media(df_filtro, col):
    if df_filtro is not None and not df_filtro.empty:
        return df_filtro[col].mean()
    return 0

def media_tot(col):
    if df is not None:
        return df[col].mean()
    return 0

def grafico_radar(vals_emp, vals_reg, vals_tam, labels, nom_reg, nom_tam):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals_emp, theta=labels, fill='toself',
        name='Mi Empresa', line_color='#1E3A8A'))
    fig.add_trace(go.Scatterpolar(r=vals_reg, theta=labels,
        name=f'Media {nom_reg}', line_color='#10B981'))
    fig.add_trace(go.Scatterpolar(r=vals_tam, theta=labels,
        name=f'Media {nom_tam}', line_color='#F59E0B'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,5])),
        showlegend=True, height=380)
    return fig

def grafico_barras(vals_emp, vals_reg, vals_tam, vals_tot, labels, nom_reg, nom_tam):
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Mi Empresa', x=labels, y=vals_emp, marker_color='#1E3A8A'))
    fig.add_trace(go.Bar(name=f'Media {nom_reg}', x=labels, y=vals_reg, marker_color='#10B981'))
    fig.add_trace(go.Bar(name=f'Media {nom_tam}', x=labels, y=vals_tam, marker_color='#F59E0B'))
    fig.add_trace(go.Bar(name='Media Total', x=labels, y=vals_tot, marker_color='#94A3B8'))
    fig.update_layout(barmode='group', height=380, yaxis=dict(range=[0,5]),
        legend=dict(orientation='h', yanchor='bottom', y=1.02))
    return fig

def diagnostico(idx, ref, nom_reg):
    if idx >= 4:
        st.success(f"✅ **Posición DESTACADA** — Tu índice es **{idx:.2f}/5**, por encima de la media de {nom_reg} ({ref:.2f}).")
    elif idx >= ref:
        st.info(f"👍 **POR ENCIMA de la media** — Tu índice es **{idx:.2f}/5** frente a {ref:.2f} de media en {nom_reg}.")
    elif idx >= ref * 0.85:
        st.warning(f"⚠️ **PRÓXIMO a la media** — Tu índice es **{idx:.2f}/5**. Te faltan {ref-idx:.2f} puntos para la media de {nom_reg} ({ref:.2f}).")
    else:
        st.error(f"🔴 **POR DEBAJO de la media** — Tu índice es **{idx:.2f}/5** frente a {ref:.2f} de media en {nom_reg}.")

# ── CABECERA ──────────────────────────────────────────────────────────────────
st.title("📊 Informes Parciales de Innovación")
st.markdown(f"**{sector}** · Región: **{nom_reg}** · Tamaño: **{nom_tam}**")
st.divider()

# ── Comprobar qué bloques están completados ───────────────────────────────────
bloques_completados = []
if st.session_state.get('b1_finalizado'): bloques_completados.append("Bloque 1 · I+D+i")
if st.session_state.get('b2_finalizado'): bloques_completados.append("Bloque 2 · Gestión Proyectos")
if st.session_state.get('b3_finalizado'): bloques_completados.append("Bloque 3 · Desarrollo Productos")
if st.session_state.get('b4_finalizado'): bloques_completados.append("Bloque 4 · Estrategia")
if st.session_state.get('b5_finalizado'): bloques_completados.append("Bloque 5 · Desempeño")

if not bloques_completados:
    st.warning("⚠️ Todavía no has completado ningún bloque. Ve al menú y rellena al menos uno.")
    st.stop()

st.info("📌 Estos son informes de muestra. Los informes completos estarán disponibles próximamente.")
st.success(f"✅ Tienes **{len(bloques_completados)}** bloque(s) completado(s): {', '.join(bloques_completados)}")
st.divider()

# ── PESTAÑAS ──────────────────────────────────────────────────────────────────
tabs = st.tabs(bloques_completados)
tab_idx = 0

# ── BLOQUE 1 ──────────────────────────────────────────────────────────────────
if st.session_state.get('b1_finalizado'):
    with tabs[tab_idx]:
        tab_idx += 1
        cols   = ['SUB_1.1_Dpto','SUB_1.2_PresupID','SUB_1.3_Gasto','IND_IDi']
        labels = ['Dpto I+D','Presupuesto I+D','Gasto Innovación','Índice Global']
        emp  = [st.session_state.get('score_sub1_1',0), st.session_state.get('score_sub1_2',0),
                st.session_state.get('score_sub1_3',0), st.session_state.get('score_b1',0)]
        reg  = [media(df_reg,c) for c in cols]
        tam  = [media(df_tam,c) for c in cols]
        tot  = [media_tot(c) for c in cols]

        st.markdown("### 🎯 Puntuaciones")
        m1,m2,m3,m4 = st.columns(4)
        for col_m, lbl, e, r in zip([m1,m2,m3,m4], labels, emp, reg):
            col_m.metric(lbl, f"{e:.2f}/5", f"{e-r:+.2f} vs {nom_reg}")

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🕸️ Radar")
            st.plotly_chart(grafico_radar(emp,reg,tam,labels,nom_reg,nom_tam), use_container_width=True)
        with c2:
            st.markdown("#### 📊 Barras")
            st.plotly_chart(grafico_barras(emp,reg,tam,tot,labels,nom_reg,nom_tam), use_container_width=True)

        st.divider()
        tabla = pd.DataFrame({'Indicador':labels,'Mi Empresa':[f"{v:.2f}" for v in emp],
            f'Media {nom_reg}':[f"{v:.2f}" for v in reg],
            f'Media {nom_tam}':[f"{v:.2f}" for v in tam],
            'Media Total':[f"{v:.2f}" for v in tot]})
        st.dataframe(tabla, use_container_width=True, hide_index=True)
        st.divider()
        diagnostico(st.session_state.get('score_b1',0), media(df_reg,'IND_IDi'), nom_reg)

# ── BLOQUE 2 ──────────────────────────────────────────────────────────────────
if st.session_state.get('b2_finalizado'):
    with tabs[tab_idx]:
        tab_idx += 1
        cols   = ['SUB_2.1_Gbasica','SUB_2.2_Gavanz','SUB_2.3_OrgProy','SUB_2.4_EvalRdto','IND_GPROY']
        labels = ['Gestión Básica','Gestión Avanzada','Organización','Evaluación','Índice Global']
        emp  = [st.session_state.get('score_sub2_1',0), st.session_state.get('score_sub2_2',0),
                st.session_state.get('score_sub2_3',0), st.session_state.get('score_sub2_4',0),
                st.session_state.get('score_b2',0)]
        reg  = [media(df_reg,c) for c in cols]
        tam  = [media(df_tam,c) for c in cols]
        tot  = [media_tot(c) for c in cols]

        st.markdown("### 🎯 Puntuaciones")
        cols_m = st.columns(5)
        for col_m, lbl, e, r in zip(cols_m, labels, emp, reg):
            col_m.metric(lbl, f"{e:.2f}/5", f"{e-r:+.2f} vs {nom_reg}")

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🕸️ Radar")
            st.plotly_chart(grafico_radar(emp,reg,tam,labels,nom_reg,nom_tam), use_container_width=True)
        with c2:
            st.markdown("#### 📊 Barras")
            st.plotly_chart(grafico_barras(emp,reg,tam,tot,labels,nom_reg,nom_tam), use_container_width=True)

        st.divider()
        tabla = pd.DataFrame({'Indicador':labels,'Mi Empresa':[f"{v:.2f}" for v in emp],
            f'Media {nom_reg}':[f"{v:.2f}" for v in reg],
            f'Media {nom_tam}':[f"{v:.2f}" for v in tam],
            'Media Total':[f"{v:.2f}" for v in tot]})
        st.dataframe(tabla, use_container_width=True, hide_index=True)
        st.divider()
        diagnostico(st.session_state.get('score_b2',0), media(df_reg,'IND_GPROY'), nom_reg)

# ── BLOQUE 3 ──────────────────────────────────────────────────────────────────
if st.session_state.get('b3_finalizado'):
    with tabs[tab_idx]:
        tab_idx += 1
        cols   = ['SUB_3.1_EstrDes','SUB_3.2_OportMdo','SUB_3.3_RecepNprod','SUB_3.4_Clientes','SUB_3.5_ImpacNprod','IND_DESPROD']
        labels = ['Estrategia','Oportunidad','Receptividad','Clientes','Viabilidad','Índice Global']
        emp  = [st.session_state.get('score_sub3_1',0), st.session_state.get('score_sub3_2',0),
                st.session_state.get('score_sub3_3',0), st.session_state.get('score_sub3_4',0),
                st.session_state.get('score_sub3_5',0), st.session_state.get('score_b3',0)]
        reg  = [media(df_reg,c) for c in cols]
        tam  = [media(df_tam,c) for c in cols]
        tot  = [media_tot(c) for c in cols]

        st.markdown("### 🎯 Puntuaciones")
        cols_m = st.columns(6)
        for col_m, lbl, e, r in zip(cols_m, labels, emp, reg):
            col_m.metric(lbl, f"{e:.2f}/5", f"{e-r:+.2f} vs {nom_reg}")

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🕸️ Radar")
            st.plotly_chart(grafico_radar(emp,reg,tam,labels,nom_reg,nom_tam), use_container_width=True)
        with c2:
            st.markdown("#### 📊 Barras")
            st.plotly_chart(grafico_barras(emp,reg,tam,tot,labels,nom_reg,nom_tam), use_container_width=True)

        st.divider()
        tabla = pd.DataFrame({'Indicador':labels,'Mi Empresa':[f"{v:.2f}" for v in emp],
            f'Media {nom_reg}':[f"{v:.2f}" for v in reg],
            f'Media {nom_tam}':[f"{v:.2f}" for v in tam],
            'Media Total':[f"{v:.2f}" for v in tot]})
        st.dataframe(tabla, use_container_width=True, hide_index=True)
        st.divider()
        diagnostico(st.session_state.get('score_b3',0), media(df_reg,'IND_DESPROD'), nom_reg)

# ── BLOQUE 4 ──────────────────────────────────────────────────────────────────
if st.session_state.get('b4_finalizado'):
    with tabs[tab_idx]:
        tab_idx += 1
        cols   = ['SUB_4.1_InnEstrat','SUB_4.2_CultInn','SUB_4.3_Obstac','SUB_4.4_InnAb','SUB_4.5_Creativ','IND_ESTRINN']
        labels = ['Inn Estratégica','Cultura','Obstáculos','Inn Abierta','Creatividad','Índice Global']
        emp  = [st.session_state.get('score_sub4_1',0), st.session_state.get('score_sub4_2',0),
                st.session_state.get('score_sub4_3',0), st.session_state.get('score_sub4_4',0),
                st.session_state.get('score_sub4_5',0), st.session_state.get('score_b4',0)]
        reg  = [media(df_reg,c) for c in cols]
        tam  = [media(df_tam,c) for c in cols]
        tot  = [media_tot(c) for c in cols]

        st.markdown("### 🎯 Puntuaciones")
        cols_m = st.columns(6)
        for col_m, lbl, e, r in zip(cols_m, labels, emp, reg):
            col_m.metric(lbl, f"{e:.2f}/5", f"{e-r:+.2f} vs {nom_reg}")

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🕸️ Radar")
            st.plotly_chart(grafico_radar(emp,reg,tam,labels,nom_reg,nom_tam), use_container_width=True)
        with c2:
            st.markdown("#### 📊 Barras")
            st.plotly_chart(grafico_barras(emp,reg,tam,tot,labels,nom_reg,nom_tam), use_container_width=True)

        st.divider()
        tabla = pd.DataFrame({'Indicador':labels,'Mi Empresa':[f"{v:.2f}" for v in emp],
            f'Media {nom_reg}':[f"{v:.2f}" for v in reg],
            f'Media {nom_tam}':[f"{v:.2f}" for v in tam],
            'Media Total':[f"{v:.2f}" for v in tot]})
        st.dataframe(tabla, use_container_width=True, hide_index=True)
        st.divider()
        diagnostico(st.session_state.get('score_b4',0), media(df_reg,'IND_ESTRINN'), nom_reg)

# ── BLOQUE 5 ──────────────────────────────────────────────────────────────────
if st.session_state.get('b5_finalizado'):
    with tabs[tab_idx]:
        cols   = ['SUB_5.1_ImpEstim','SUB_5.2_InnEfect','IND_DESMPINN']
        labels = ['Impacto Estimado','Impacto Efectivo','Índice Global']
        emp  = [st.session_state.get('score_sub5_1',0), st.session_state.get('score_sub5_2',0),
                st.session_state.get('score_b5',0)]
        reg  = [media(df_reg,c) for c in cols]
        tam  = [media(df_tam,c) for c in cols]
        tot  = [media_tot(c) for c in cols]

        st.markdown("### 🎯 Puntuaciones")
        m1,m2,m3 = st.columns(3)
        for col_m, lbl, e, r in zip([m1,m2,m3], labels, emp, reg):
            col_m.metric(lbl, f"{e:.2f}/5", f"{e-r:+.2f} vs {nom_reg}")

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🕸️ Radar")
            st.plotly_chart(grafico_radar(emp,reg,tam,labels,nom_reg,nom_tam), use_container_width=True)
        with c2:
            st.markdown("#### 📊 Barras")
            st.plotly_chart(grafico_barras(emp,reg,tam,tot,labels,nom_reg,nom_tam), use_container_width=True)

        st.divider()
        tabla = pd.DataFrame({'Indicador':labels,'Mi Empresa':[f"{v:.2f}" for v in emp],
            f'Media {nom_reg}':[f"{v:.2f}" for v in reg],
            f'Media {nom_tam}':[f"{v:.2f}" for v in tam],
            'Media Total':[f"{v:.2f}" for v in tot]})
        st.dataframe(tabla, use_container_width=True, hide_index=True)
        st.divider()
        diagnostico(st.session_state.get('score_b5',0), media(df_reg,'IND_DESMPINN'), nom_reg)