import streamlit as st
from asistentes import mostrar_felix
import pandas as pd
import plotly.graph_objects as go
import json
import os
import numpy as np
from streamlit_echarts import st_echarts

st.set_page_config(page_title="Analytics Comparativo", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');
.section-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.25rem; font-weight: 700;
    color: #ffffff;
    background: linear-gradient(90deg, rgba(0,212,255,0.2), rgba(0,212,255,0.0));
    border-left: 5px solid #00d4ff;
    padding: 10px 16px;
    border-radius: 0 8px 8px 0;
    margin: 20px 0 15px 0;
    text-shadow: 0 0 12px rgba(0,212,255,0.8);
}
.kpi-card {
    background: linear-gradient(135deg, #0d1b2a, #1a2744);
    border: 1px solid #1e3a5f;
    border-radius: 12px; padding: 16px 18px; text-align: center;
    position: relative; overflow: hidden;
}
.kpi-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
    background: linear-gradient(90deg,#00d4ff,#0066ff,#7c3aed);
}
.kpi-label { font-size:0.68rem; color:#64748b; text-transform:uppercase; letter-spacing:1px; margin-bottom:5px; }
.kpi-value { font-family:'Rajdhani',sans-serif; font-size:1.8rem; font-weight:700; color:#00d4ff; line-height:1; }
.kpi-delta-pos { color:#10b981; font-size:0.78rem; }
.kpi-delta-neg { color:#ef4444; font-size:0.78rem; }
</style>
""", unsafe_allow_html=True)

# ── Cargar perfil ─────────────────────────────────────────────────────────────
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

if not st.session_state.get('save_reg_user'):
    st.warning("⚠️ Primero completa tu perfil en Inicio.")
    st.stop()

# ── Cargar Excel ──────────────────────────────────────────────────────────────
ruta_excel = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'datos.xlsx')
if not os.path.exists(ruta_excel): ruta_excel = "datos.xlsx"
try:
    df = pd.read_excel(ruta_excel)
    df.columns = df.columns.str.strip()
except Exception as e:
    st.error(f"Error al cargar datos: {e}")
    st.stop()

# ── Mapas ─────────────────────────────────────────────────────────────────────
REGIONES     = {1:"Andalucia",2:"Aragon",3:"Asturias",4:"Baleares",5:"Canarias",6:"Cantabria",7:"Castilla la Mancha",8:"Castilla y León",9:"Cataluña",10:"Com Valenciana",11:"Extremadura",12:"Galicia",13:"Madrid",14:"Murcia",15:"Navarra",16:"Pais Vasco"}
TAMANIOS     = {1:"Pequeña",2:"Mediana",3:"Grande"}
MACROSECTORES= {1:"Industria",2:"Tecnologia avanzada",3:"Servicios"}
EXPORTACIONES= {1:"Menos 10 %",2:"10 - 30 %",3:"30 - 60 %",4:"> 60 %"}
ANTIGUEDADES = {1:"Menos 10 años",2:"10-30 años",3:"> 30 años"}
SECTORES     = {1:"Alimentación y bebidas",2:"Textil y confección",3:"Cuero y calzado",4:"Química y plásticos",5:"Minerales no metálicos",6:"Metalmecánico",7:"Maquinaria equipo",8:"Otras manufacturas",9:"Electrónica, telecomunicaciones",10:"Informática, software. Robótica, IA",11:"Actividades I+D: biotech, farmacia",12:"Transporte y logística",13:"Consultoría y servicios profesionales",14:"Turismo y hosteleria",15:"Retail y comercio",16:"Otros servicios"}
SECTOR_MACRO = {1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:2,10:2,11:2,12:3,13:3,14:3,15:3,16:3}

INDICADORES = {
    "Ind.1 · I+D+i":           "IND_IDi",
    "Ind.2 · Gestión Proy.":   "IND_GPROY",
    "Ind.3 · Dllo Productos":  "IND_DESPROD",
    "Ind.4 · Estrategia Inn.": "IND_ESTRINN",
    "Ind.5 · Desempeño Inn.":  "IND_DESMPINN",
    "Sub 1.1 · Dpto I+D":      "SUB_1.1_Dpto",
    "Sub 1.2 · Presupuesto":   "SUB_1.2_PresupID",
    "Sub 1.3 · Gasto Inn.":    "SUB_1.3_Gasto",
    "Sub 2.1 · Gest. Básica":  "SUB_2.1_Gbasica",
    "Sub 2.2 · Gest. Avanz.":  "SUB_2.2_Gavanz",
    "Sub 2.3 · Organización":  "SUB_2.3_OrgProy",
    "Sub 2.4 · Evaluación":    "SUB_2.4_EvalRdto",
    "Sub 3.1 · Estrategia":    "SUB_3.1_EstrDes",
    "Sub 3.2 · Oportunidad":   "SUB_3.2_OportMdo",
    "Sub 3.3 · Receptividad":  "SUB_3.3_RecepNprod",
    "Sub 3.4 · Clientes":      "SUB_3.4_Clientes",
    "Sub 3.5 · Viabilidad":    "SUB_3.5_ImpacNprod",
    "Sub 4.1 · Inn Estrat.":   "SUB_4.1_InnEstrat",
    "Sub 4.2 · Cultura":       "SUB_4.2_CultInn",
    "Sub 4.3 · Obstáculos":    "SUB_4.3_Obstac",
    "Sub 4.4 · Inn Abierta":   "SUB_4.4_InnAb",
    "Sub 4.5 · Creatividad":   "SUB_4.5_Creativ",
    "Sub 5.1 · Imp. Estimado": "SUB_5.1_ImpEstim",
    "Sub 5.2 · Imp. Efectivo": "SUB_5.2_InnEfect",
}
COLS_INVERTIDAS = {'Ratio_Endeudamiento', 'SUB_4.3_Obstac'}

mis_valores_map = {
    "IND_IDi":           st.session_state.get('score_b1',0),
    "IND_GPROY":         st.session_state.get('score_b2',0),
    "IND_DESPROD":       st.session_state.get('score_b3',0),
    "IND_ESTRINN":       st.session_state.get('score_b4',0),
    "IND_DESMPINN":      st.session_state.get('score_b5',0),
    "SUB_1.1_Dpto":      st.session_state.get('score_sub1_1',0),
    "SUB_1.2_PresupID":  st.session_state.get('score_sub1_2',0),
    "SUB_1.3_Gasto":     st.session_state.get('score_sub1_3',0),
    "SUB_2.1_Gbasica":   st.session_state.get('score_sub2_1',0),
    "SUB_2.2_Gavanz":    st.session_state.get('score_sub2_2',0),
    "SUB_2.3_OrgProy":   st.session_state.get('score_sub2_3',0),
    "SUB_2.4_EvalRdto":  st.session_state.get('score_sub2_4',0),
    "SUB_3.1_EstrDes":   st.session_state.get('score_sub3_1',0),
    "SUB_3.2_OportMdo":  st.session_state.get('score_sub3_2',0),
    "SUB_3.3_RecepNprod":st.session_state.get('score_sub3_3',0),
    "SUB_3.4_Clientes":  st.session_state.get('score_sub3_4',0),
    "SUB_3.5_ImpacNprod":st.session_state.get('score_sub3_5',0),
    "SUB_4.1_InnEstrat": st.session_state.get('score_sub4_1',0),
    "SUB_4.2_CultInn":   st.session_state.get('score_sub4_2',0),
    "SUB_4.3_Obstac":    st.session_state.get('score_sub4_3',0),
    "SUB_4.4_InnAb":     st.session_state.get('score_sub4_4',0),
    "SUB_4.5_Creativ":   st.session_state.get('score_sub4_5',0),
    "SUB_5.1_ImpEstim":  st.session_state.get('score_sub5_1',0),
    "SUB_5.2_InnEfect":  st.session_state.get('score_sub5_2',0),
}

# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
   mostrar_felix(pagina='analytics')
    st.markdown("### 🔍 Filtros de Comparación")
    st.caption("Vacío = sin filtro (todas las empresas)")
    st.divider()
    REG_INV = {v:k for k,v in REGIONES.items()}
    TAM_INV = {v:k for k,v in TAMANIOS.items()}
    MAC_INV = {v:k for k,v in MACROSECTORES.items()}
    EXP_INV = {v:k for k,v in EXPORTACIONES.items()}
    ANT_INV = {v:k for k,v in ANTIGUEDADES.items()}
    SEC_INV = {v:k for k,v in SECTORES.items()}

    mi_reg = REGIONES.get(st.session_state.get('save_reg_user'))
    mi_tam = TAMANIOS.get(st.session_state.get('save_tam_user'))

    reg_sel = st.multiselect("📍 Región", list(REGIONES.values()), default=[mi_reg] if mi_reg else [])
    tam_sel = st.multiselect("🏢 Tamaño", list(TAMANIOS.values()), default=[mi_tam] if mi_tam else [])
    mac_sel = st.multiselect("🏭 Macrosector", list(MACROSECTORES.values()), default=[])

    if mac_sel:
        sects_disp = [v for k,v in SECTORES.items() if SECTOR_MACRO.get(k) in [MAC_INV.get(m) for m in mac_sel]]
    else:
        sects_disp = list(SECTORES.values())
    sec_sel = st.multiselect("🔧 Sector", sects_disp, default=[])
    exp_sel = st.multiselect("🌍 Exportación", list(EXPORTACIONES.values()), default=[])
    ant_sel = st.multiselect("📅 Antigüedad", list(ANTIGUEDADES.values()), default=[])
    st.divider()
    usar_ventas = st.checkbox("Filtrar por Ventas")
    if usar_ventas:
        rango_ventas = st.slider("Ventas (€)", int(df['Ventas'].min()), int(df['Ventas'].max()),
            (int(df['Ventas'].min()), int(df['Ventas'].max())))
    usar_roa = st.checkbox("Filtrar por ROA")
    if usar_roa:
        rango_roa = st.slider("ROA (%)", float(df['ROA'].min()), float(df['ROA'].max()),
            (float(df['ROA'].min()), float(df['ROA'].max())))

# ── Aplicar filtros ───────────────────────────────────────────────────────────
dff = df.copy()
if reg_sel: dff = dff[dff['Region'].isin([REG_INV[r] for r in reg_sel if r in REG_INV])]
if tam_sel: dff = dff[dff['Tamaño'].isin([TAM_INV[t] for t in tam_sel if t in TAM_INV])]
if mac_sel: dff = dff[dff['Macrosector'].isin([MAC_INV[m] for m in mac_sel if m in MAC_INV])]
if sec_sel: dff = dff[dff['Sector'].isin([SEC_INV[s] for s in sec_sel if s in SEC_INV])]
if exp_sel: dff = dff[dff['Exportacion'].isin([EXP_INV[e] for e in exp_sel if e in EXP_INV])]
if ant_sel: dff = dff[dff['Antigüedad'].isin([ANT_INV[a] for a in ant_sel if a in ANT_INV])]
if usar_ventas: dff = dff[(dff['Ventas']>=rango_ventas[0])&(dff['Ventas']<=rango_ventas[1])]
if usar_roa:    dff = dff[(dff['ROA']>=rango_roa[0])&(dff['ROA']<=rango_roa[1])]

n = len(dff)
nom_reg = st.session_state.get('save_reg_nombre','—')
nom_tam = st.session_state.get('save_tam_nombre','—')

# ── CABECERA ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='background:linear-gradient(135deg,#0d1b2a,#1a2744);border-radius:14px;padding:22px 28px;margin-bottom:18px;border:1px solid #1e3a5f;'>
    <h1 style='font-family:Rajdhani,sans-serif;color:#00d4ff;margin:0;font-size:1.9rem;'>📈 Analytics Comparativo</h1>
    <p style='color:#94a3b8;margin:4px 0 0 0;font-size:0.88rem;'>
        {st.session_state.get('save_sector_nombre','Tu empresa')} · 
        Región: <strong style='color:#e2e8f0;'>{nom_reg}</strong> · 
        Tamaño: <strong style='color:#e2e8f0;'>{nom_tam}</strong>
    </p>
</div>
""", unsafe_allow_html=True)

if n < 10:
    st.error(f"⚠️ Solo **{n} empresas** con estos filtros. Necesitas al menos 10. Reduce los criterios.")
    st.stop()
elif n < 30:
    st.warning(f"⚠️ **{n} empresas** en el grupo. Válido pero muestra pequeña.")
else:
    st.success(f"✅ Comparando con **{n} empresas** del grupo seleccionado.")

st.divider()

# ── SELECTOR INDICADORES ──────────────────────────────────────────────────────
ind_validos = {k:v for k,v in INDICADORES.items() if v in df.columns}
ind_sel = st.multiselect("📊 Indicadores a comparar:", list(ind_validos.keys()),
    default=["Ind.1 · I+D+i","Ind.2 · Gestión Proy.","Ind.3 · Dllo Productos",
             "Ind.4 · Estrategia Inn.","Ind.5 · Desempeño Inn."])

if not ind_sel:
    st.info("Selecciona al menos un indicador.")
    st.stop()

cols_sel = [ind_validos[i] for i in ind_sel]
emp_vals = [round(mis_valores_map.get(c,0),3) for c in cols_sel]
grp_vals = [round(dff[c].mean(),3) for c in cols_sel]
tot_vals = [round(df[c].mean(),3)  for c in cols_sel]

def calc_pct(col, mv):
    if col in COLS_INVERTIDAS:
        return round(float(np.sum(dff[col] >= mv) / len(dff) * 100))
    return round(float(np.sum(dff[col] <= mv) / len(dff) * 100))

pcts = [calc_pct(c, mv) for c, mv in zip(cols_sel, emp_vals)]

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ═════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🎯 Posición en el Grupo</div>', unsafe_allow_html=True)
n_show = min(len(ind_sel), 5)
kpi_cols = st.columns(n_show)
for i in range(n_show):
    d = emp_vals[i] - grp_vals[i]
    dc = "kpi-delta-pos" if d >= 0 else "kpi-delta-neg"
    di = "▲" if d >= 0 else "▼"
    kpi_cols[i].markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{ind_sel[i][:22]}</div>
        <div class="kpi-value">{emp_vals[i]:.2f}</div>
        <div class="{dc}">{di} {abs(d):.2f} vs media grupo</div>
        <div style="color:#a78bfa;font-size:0.75rem;margin-top:3px;">Percentil {pcts[i]}°</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# ECHARTS: BARRAS INTERACTIVAS
# ═════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📊 Comparativa Interactiva — Barras</div>', unsafe_allow_html=True)
st.caption("💡 Haz clic en la leyenda para mostrar/ocultar series. Pasa el ratón sobre las barras para ver detalles.")

bar_option = {
    "backgroundColor": "#0d1b2a",
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {"type": "shadow"},
        "backgroundColor": "#1e293b",
        "borderColor": "#334155",
        "textStyle": {"color": "#e2e8f0"},
    },
    "legend": {
        "data": ["Mi Empresa", f"Media Grupo ({n} emp)", "Media Total (1.000 emp)"],
        "textStyle": {"color": "#94a3b8"},
        "top": 10,
    },
    "grid": {"left": "3%", "right": "4%", "bottom": "15%", "containLabel": True},
    "xAxis": {
        "type": "category",
        "data": ind_sel,
        "axisLabel": {"color": "#94a3b8", "rotate": 20, "fontSize": 11},
        "axisLine": {"lineStyle": {"color": "#334155"}},
    },
    "yAxis": {
        "type": "value", "min": 0, "max": 5,
        "axisLabel": {"color": "#64748b"},
        "splitLine": {"lineStyle": {"color": "#1e3a5f"}},
    },
    "series": [
        {
            "name": "Mi Empresa",
            "type": "bar",
            "data": emp_vals,
            "itemStyle": {"color": "#00d4ff", "borderRadius": [4,4,0,0]},
            "emphasis": {"itemStyle": {"color": "#38bdf8", "shadowBlur": 20, "shadowColor": "rgba(0,212,255,0.6)"}},
            "label": {"show": True, "position": "top", "color": "#00d4ff", "fontSize": 10,
                      "formatter": "{c}"},
        },
        {
            "name": f"Media Grupo ({n} emp)",
            "type": "bar",
            "data": grp_vals,
            "itemStyle": {"color": "#10b981", "borderRadius": [4,4,0,0]},
            "emphasis": {"itemStyle": {"color": "#34d399", "shadowBlur": 20, "shadowColor": "rgba(16,185,129,0.6)"}},
            "label": {"show": True, "position": "top", "color": "#10b981", "fontSize": 10,
                      "formatter": "{c}"},
        },
        {
            "name": "Media Total (1.000 emp)",
            "type": "bar",
            "data": tot_vals,
            "itemStyle": {"color": "#f59e0b", "borderRadius": [4,4,0,0]},
            "emphasis": {"itemStyle": {"color": "#fbbf24", "shadowBlur": 20, "shadowColor": "rgba(245,158,11,0.6)"}},
            "label": {"show": True, "position": "top", "color": "#f59e0b", "fontSize": 10,
                      "formatter": "{c}"},
        },
    ],
}
st_echarts(options=bar_option, height="400px")

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# ECHARTS: RADAR INTERACTIVO
# ═════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🕸️ Radar Interactivo</div>', unsafe_allow_html=True)
st.caption("💡 Haz clic en la leyenda para activar/desactivar capas.")

radar_indicators = [{"name": lbl, "max": 5} for lbl in ind_sel]
radar_option = {
    "backgroundColor": "#0d1b2a",
    "tooltip": {"trigger": "item", "backgroundColor": "#1e293b",
                "borderColor": "#334155", "textStyle": {"color": "#e2e8f0"}},
    "legend": {
        "data": ["Mi Empresa", f"Media Grupo ({n} emp)", "Media Total"],
        "textStyle": {"color": "#94a3b8"}, "bottom": 0,
    },
    "radar": {
        "indicator": radar_indicators,
        "shape": "polygon",
        "splitNumber": 5,
        "axisName": {"color": "#94a3b8", "fontSize": 11},
        "splitLine": {"lineStyle": {"color": ["#1e3a5f","#1e3a5f","#1e3a5f","#1e3a5f","#1e3a5f"]}},
        "splitArea": {"areaStyle": {"color": ["rgba(0,212,255,0.02)","rgba(0,212,255,0.05)"]}},
        "axisLine": {"lineStyle": {"color": "#1e3a5f"}},
    },
    "series": [{
        "type": "radar",
        "data": [
            {
                "value": emp_vals,
                "name": "Mi Empresa",
                "itemStyle": {"color": "#00d4ff"},
                "lineStyle": {"color": "#00d4ff", "width": 2},
                "areaStyle": {"color": "rgba(0,212,255,0.15)"},
                "symbol": "circle", "symbolSize": 6,
            },
            {
                "value": grp_vals,
                "name": f"Media Grupo ({n} emp)",
                "itemStyle": {"color": "#10b981"},
                "lineStyle": {"color": "#10b981", "width": 2, "type": "dashed"},
                "areaStyle": {"color": "rgba(16,185,129,0.08)"},
                "symbol": "circle", "symbolSize": 5,
            },
            {
                "value": tot_vals,
                "name": "Media Total",
                "itemStyle": {"color": "#f59e0b"},
                "lineStyle": {"color": "#f59e0b", "width": 1.5, "type": "dotted"},
                "areaStyle": {"color": "rgba(245,158,11,0.05)"},
                "symbol": "circle", "symbolSize": 4,
            },
        ],
    }],
}
st_echarts(options=radar_option, height="500px")

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# ECHARTS: RANKING PERCENTIL
# ═════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🏆 Ranking Percentil en el Grupo</div>', unsafe_allow_html=True)
st.caption("💡 Pasa el ratón para ver detalles. Verde = top 33% · Amarillo = medio · Rojo = tercio inferior.")

colores_pct = ['#ef4444' if p < 33 else '#f59e0b' if p < 66 else '#10b981' for p in pcts]
pct_option = {
    "backgroundColor": "#0d1b2a",
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {"type": "shadow"},
        "backgroundColor": "#1e293b",
        "borderColor": "#334155",
        "textStyle": {"color": "#e2e8f0"},
        "formatter": "{b}: Percentil {c}°"
    },
    "grid": {"left": "2%", "right": "8%", "bottom": "5%", "containLabel": True},
    "xAxis": {
        "type": "value", "min": 0, "max": 100,
        "axisLabel": {"color": "#64748b", "formatter": "{value}°"},
        "splitLine": {"lineStyle": {"color": "#1e3a5f"}},
        "markLine": {"data": [{"xAxis": 50}]},
    },
    "yAxis": {
        "type": "category",
        "data": ind_sel,
        "axisLabel": {"color": "#94a3b8", "fontSize": 11},
        "inverse": True,
    },
    "series": [{
        "type": "bar",
        "data": [{"value": p, "itemStyle": {"color": c, "borderRadius": [0,4,4,0]}}
                 for p, c in zip(pcts, colores_pct)],
        "label": {
            "show": True, "position": "right",
            "color": "#e2e8f0", "fontSize": 11,
            "formatter": "{c}°"
        },
        "emphasis": {"itemStyle": {"shadowBlur": 15, "shadowColor": "rgba(255,255,255,0.2)"}},
        "markLine": {
            "silent": True,
            "lineStyle": {"color": "#f59e0b", "type": "dashed", "width": 2},
            "data": [{"xAxis": 50, "label": {"formatter": "Mediana grupo", "color": "#f59e0b"}}]
        },
    }],
}
st_echarts(options=pct_option, height=f"{max(300, len(ind_sel)*55)}px")

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# VELOCÍMETROS PLOTLY
# ═════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">⚡ Velocímetros por Indicador</div>', unsafe_allow_html=True)
n_g = min(len(ind_sel), 4)
gcols = st.columns(n_g)
for i in range(n_g):
    with gcols[i]:
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=emp_vals[i],
            delta={'reference': grp_vals[i], 'valueformat': '.2f',
                   'increasing': {'color':'#10b981'}, 'decreasing': {'color':'#ef4444'}},
            number={'valueformat':'.2f','font':{'size':26,'color':'#00d4ff'}},
            title={'text': ind_sel[i][:20], 'font':{'size':10,'color':'#94a3b8'}},
            gauge={
                'axis':{'range':[0,5],'tickcolor':'#334155','tickfont':{'color':'#64748b','size':8}},
                'bar':{'color':'#00d4ff','thickness':0.25},
                'bgcolor':'#0d1b2a', 'borderwidth':0,
                'steps':[{'range':[0,2],'color':'#1a0a0a'},{'range':[2,3.5],'color':'#1a1500'},{'range':[3.5,5],'color':'#0a1a0a'}],
                'threshold':{'line':{'color':'#f59e0b','width':3},'thickness':0.75,'value':grp_vals[i]}
            }
        ))
        fig_g.update_layout(height=200,margin=dict(l=15,r=15,t=40,b=10),
            paper_bgcolor='rgba(0,0,0,0)',font_color='#94a3b8')
        st.plotly_chart(fig_g, use_container_width=True)
        st.caption(f"🟡 Media grupo: {grp_vals[i]:.2f}")

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# ECHARTS: NUBE DE PUNTOS INTERACTIVA
# ═════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🌐 Nube de Puntos Interactiva</div>', unsafe_allow_html=True)
st.caption("💡 Zoom con rueda del ratón. Selecciona área con el ratón para explorar. Pasa el cursor sobre los puntos.")

c_x, c_y = st.columns(2)
with c_x:
    eje_x = st.selectbox("Eje X", list(ind_validos.keys()), index=0)
with c_y:
    eje_y = st.selectbox("Eje Y", list(ind_validos.keys()), index=min(1, len(ind_validos)-1))

col_x = ind_validos[eje_x]
col_y = ind_validos[eje_y]
mi_x  = round(mis_valores_map.get(col_x, 0), 3)
mi_y  = round(mis_valores_map.get(col_y, 0), 3)

scatter_data = [[round(float(x),3), round(float(y),3)]
                for x, y in zip(dff[col_x].fillna(0), dff[col_y].fillna(0))]

scatter_option = {
    "backgroundColor": "#0d1b2a",
    "tooltip": {
        "trigger": "item",
        "backgroundColor": "#1e293b",
        "borderColor": "#334155",
        "textStyle": {"color": "#e2e8f0"},
        "formatter": f"function(p){{ return p.seriesName + '<br/>{eje_x}: ' + p.value[0] + '<br/>{eje_y}: ' + p.value[1]; }}"
    },
    "legend": {"data": [f"Grupo ({n} emp)", "Media grupo", "Mi Empresa"],
               "textStyle": {"color": "#94a3b8"}, "top": 10},
    "xAxis": {
        "name": eje_x, "nameTextStyle": {"color": "#64748b"},
        "type": "value", "min": 0, "max": 5,
        "axisLabel": {"color": "#64748b"},
        "splitLine": {"lineStyle": {"color": "#1e3a5f"}},
    },
    "yAxis": {
        "name": eje_y, "nameTextStyle": {"color": "#64748b"},
        "type": "value", "min": 0, "max": 5,
        "axisLabel": {"color": "#64748b"},
        "splitLine": {"lineStyle": {"color": "#1e3a5f"}},
    },
    "dataZoom": [{"type": "inside"}, {"type": "slider", "bottom": 10}],
    "series": [
        {
            "name": f"Grupo ({n} emp)",
            "type": "scatter",
            "data": scatter_data,
            "symbolSize": 7,
            "itemStyle": {"color": "rgba(16,185,129,0.5)", "borderColor": "rgba(16,185,129,0.8)", "borderWidth": 1},
            "emphasis": {"itemStyle": {"color": "#34d399", "shadowBlur": 10}},
        },
        {
            "name": "Media grupo",
            "type": "scatter",
            "data": [[round(float(dff[col_x].mean()),3), round(float(dff[col_y].mean()),3)]],
            "symbolSize": 18,
            "symbol": "diamond",
            "itemStyle": {"color": "#f59e0b"},
        },
        {
            "name": "Mi Empresa",
            "type": "scatter",
            "data": [[mi_x, mi_y]],
            "symbolSize": 22,
            "symbol": "star",
            "itemStyle": {"color": "#00d4ff", "borderColor": "white", "borderWidth": 2,
                          "shadowBlur": 20, "shadowColor": "rgba(0,212,255,0.8)"},
            "label": {"show": True, "formatter": "⭐ Yo", "color": "#00d4ff",
                      "position": "top", "fontSize": 11},
        },
    ],
}
st_echarts(options=scatter_option, height="480px")

st.divider()

# ═════════════════════════════════════════════════════════════════════════════
# DESEMPEÑO ECONÓMICO
# ═════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">💰 Desempeño Económico vs. Grupo</div>', unsafe_allow_html=True)

vars_eco = {
    "Ventas (€)":        ("Ventas",               st.session_state.get('save_ventas',0),    False),
    "Empleados":         ("Empleados",             st.session_state.get('save_empleados',0), False),
    "ROA (%)":           ("ROA",                   st.session_state.get('save_roa',0),       False),
    "Productividad":     ("Prod_Venta_Emp",         st.session_state.get('save_productiv',0),False),
    "Coste Emp.":        ("Coste_Med_Emp",          st.session_state.get('save_coste_emp',0),False),
    "Endeudamiento (%)": ("Ratio_Endeudamiento",    st.session_state.get('save_endeud',0),   True),
}

eco_kpi_cols = st.columns(len(vars_eco))
eco_labels, eco_mi, eco_grp, eco_tot, eco_pcts = [], [], [], [], []

for i, (lbl, (col, mi_v, inv)) in enumerate(vars_eco.items()):
    if col in dff.columns:
        mg = dff[col].mean()
        mt = df[col].mean()
        pct_e = round(float(np.sum(dff[col] >= mi_v) / len(dff) * 100) if inv else float(np.sum(dff[col] <= mi_v) / len(dff) * 100))
        d = mi_v - mg
        dc = "kpi-delta-neg" if (inv and d > 0) else ("kpi-delta-pos" if d >= 0 else "kpi-delta-neg")
        di = "▼" if (inv and d > 0) else ("▲" if d >= 0 else "▼")
        eco_kpi_cols[i].markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{lbl}</div>
            <div class="kpi-value" style="font-size:1.3rem;">{mi_v:,.0f}</div>
            <div class="{dc}">{di} {abs(d):,.0f} vs media</div>
            <div style="color:#a78bfa;font-size:0.72rem;margin-top:3px;">Percentil {pct_e}°</div>
        </div>""", unsafe_allow_html=True)
        eco_labels.append(lbl)
        eco_mi.append(round(float(mi_v),2))
        eco_grp.append(round(float(mg),2))
        eco_tot.append(round(float(mt),2))
        eco_pcts.append(pct_e)

st.markdown(" ")
st.caption("💡 Ranking de tu posición en cada variable económica dentro del grupo. Verde = top 33% · Amarillo = medio · Rojo = tercio inferior")

colores_eco_pct = ['#ef4444' if p < 33 else '#f59e0b' if p < 66 else '#10b981' for p in eco_pcts]
eco_pct_option = {
    "backgroundColor": "#0d1b2a",
    "tooltip": {
        "trigger": "axis",
        "axisPointer": {"type": "shadow"},
        "backgroundColor": "#1e293b",
        "borderColor": "#334155",
        "textStyle": {"color": "#e2e8f0"},
        "formatter": "{b}: Percentil {c}°"
    },
    "grid": {"left": "2%", "right": "10%", "bottom": "5%", "containLabel": True},
    "xAxis": {
        "type": "value", "min": 0, "max": 100,
        "axisLabel": {"color": "#64748b", "formatter": "{value}°"},
        "splitLine": {"lineStyle": {"color": "#1e3a5f"}},
    },
    "yAxis": {
        "type": "category",
        "data": eco_labels,
        "axisLabel": {"color": "#94a3b8", "fontSize": 11},
        "inverse": True,
    },
    "series": [{
        "type": "bar",
        "data": [{"value": p, "itemStyle": {"color": c, "borderRadius": [0,4,4,0]}}
                 for p, c in zip(eco_pcts, colores_eco_pct)],
        "label": {
            "show": True, "position": "right",
            "color": "#e2e8f0", "fontSize": 11,
            "formatter": "{c}°"
        },
        "emphasis": {"itemStyle": {"shadowBlur": 15, "shadowColor": "rgba(255,255,255,0.2)"}},
        "markLine": {
            "silent": True,
            "lineStyle": {"color": "#f59e0b", "type": "dashed", "width": 2},
            "data": [{"xAxis": 50, "label": {"formatter": "Mediana grupo", "color": "#f59e0b"}}]
        },
    }],
}
st_echarts(options=eco_pct_option, height="320px")

st.divider()
st.caption("💡 Ajusta los filtros del panel izquierdo para compararte con distintos grupos.")