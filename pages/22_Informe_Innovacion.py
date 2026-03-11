import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json, os, numpy as np, requests, unicodedata
from streamlit_echarts import st_echarts
from datetime import date

st.set_page_config(page_title="Informe de Innovación", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');
.report-header {
    background:linear-gradient(135deg,#0a1a0e,#0d2a1a);
    border:1px solid #1a3a2a; border-radius:14px;
    padding:28px 32px; margin-bottom:24px;
}
.section-title {
    font-family:'Rajdhani',sans-serif; font-size:1.2rem; font-weight:700; color:#fff;
    background:linear-gradient(90deg,rgba(16,185,129,0.2),rgba(16,185,129,0));
    border-left:5px solid #10b981; padding:10px 16px; border-radius:0 8px 8px 0;
    margin:28px 0 14px 0; text-shadow:0 0 12px rgba(16,185,129,0.6);
}
.text-block {
    background:linear-gradient(135deg,#0a1a0e,#0d2a1a);
    border:1px solid #1a3a2a; border-radius:12px;
    padding:22px 26px; margin-bottom:16px;
    color:#cbd5e1; line-height:1.8; font-size:.93rem;
}
.rec-block {
    background:linear-gradient(135deg,#1a1200,#2a1e00);
    border-left:4px solid #f59e0b; border-radius:0 10px 10px 0;
    padding:18px 22px; margin-bottom:14px;
    color:#cbd5e1; line-height:1.8; font-size:.93rem;
}
.pred-block {
    background:linear-gradient(135deg,#0a0a2e,#1a1035);
    border-left:4px solid #7c3aed; border-radius:0 10px 10px 0;
    padding:18px 22px; margin-bottom:14px;
    color:#cbd5e1; line-height:1.8; font-size:.93rem;
}
.pending {
    color:#475569; font-style:italic; background:#0a1a0e;
    border:1px dashed #1a3a2a; border-radius:10px;
    padding:18px 22px; margin-bottom:14px;
}
.kpi-inn {
    background:linear-gradient(135deg,#0a1a0e,#0d2a1a);
    border:1px solid #1a3a2a; border-radius:12px;
    padding:14px; text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ── API Key ────────────────────────────────────────────────────────────────
def cargar_api_key():
    try: return st.secrets["ANTHROPIC_API_KEY"]
    except: pass
    key = os.environ.get("ANTHROPIC_API_KEY","")
    if key: return key
    env = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..', '.env')
    if os.path.exists(env):
        with open(env,'r') as f:
            for line in f:
                if line.startswith("ANTHROPIC_API_KEY"):
                    return line.split("=",1)[1].strip().strip('"').strip("'")
    return ""

ANTHROPIC_API_KEY = cargar_api_key()

# ── Perfil ─────────────────────────────────────────────────────────────────
PERFIL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','perfil_empresa.json')
def cargar_perfil():
    if os.path.exists(PERFIL_FILE):
        with open(PERFIL_FILE,'r',encoding='utf-8') as f: return json.load(f)
    return {}
perfil = cargar_perfil()
for k,v in perfil.items():
    if k not in st.session_state: st.session_state[k] = v

if not st.session_state.get('save_reg_user'):
    st.warning("⚠️ Primero completa tu perfil en Inicio."); st.stop()

# ── Excel ──────────────────────────────────────────────────────────────────
ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','datos.xlsx')
if not os.path.exists(ruta): ruta = "datos.xlsx"
try:
    df = pd.read_excel(ruta); df.columns = df.columns.str.strip()
except Exception as e:
    st.error(f"Error: {e}"); st.stop()

EXPORTACIONES = {1:"Menos 10%",2:"10-30%",3:"30-60%",4:">60%"}
nom_sector = st.session_state.get('save_sector_nombre','—')
nom_reg    = st.session_state.get('save_reg_nombre','—')
nom_tam    = st.session_state.get('save_tam_nombre','—')
nom_export = EXPORTACIONES.get(st.session_state.get('save_export_cod',1),'—')
nom_anti   = st.session_state.get('save_anti_nombre','—')
mac_cod    = st.session_state.get('save_macro_cod',1)
tam_cod    = st.session_state.get('save_tam_user',1)
hoy        = date.today().strftime("%d/%m/%Y")

# ── Grupo de referencia ────────────────────────────────────────────────────
dff = df[(df['Macrosector']==mac_cod)&(df['Tamaño']==tam_cod)]
if len(dff) < 10: dff = df[df['Macrosector']==mac_cod]
if len(dff) < 10: dff = df.copy()
n_ref = len(dff)

# ── Scores innovación desde session_state ─────────────────────────────────
b1 = st.session_state.get('score_b1', 0)
b2 = st.session_state.get('score_b2', 0)
b3 = st.session_state.get('score_b3', 0)
b4 = st.session_state.get('score_b4', 0)
b5 = st.session_state.get('score_b5', 0)
macro_inn = (b1*0.20 + b2*0.20 + b3*0.20 + b4*0.20 + b5*0.20) if any([b1,b2,b3,b4,b5]) else 0

# Subindicadores desde session_state
SUBS = {
    'SUB_1.1_Dpto':     ('Dpto. y Recursos I+D',       'score_sub1_1'),
    'SUB_1.2_PresupID': ('Presupuesto I+D',             'score_sub1_2'),
    'SUB_1.3_Gasto':    ('Gasto en Innovación',         'score_sub1_3'),
    'SUB_2.1_Gbasica':  ('Gestión Básica Proy.',        'score_sub2_1'),
    'SUB_2.2_Gavanz':   ('Gestión Avanzada Proy.',      'score_sub2_2'),
    'SUB_2.3_OrgProy':  ('Organización Proyectos',      'score_sub2_3'),
    'SUB_2.4_EvalRdto': ('Evaluación Rendimiento',      'score_sub2_4'),
    'SUB_3.1_EstrDes':  ('Estrategia Nuevos Prod.',     'score_sub3_1'),
    'SUB_3.2_OportMdo': ('Oportunidad de Mercado',      'score_sub3_2'),
    'SUB_3.3_RecepNprod':('Receptividad Cliente',       'score_sub3_3'),
    'SUB_3.4_Clientes': ('Orientación al Cliente',      'score_sub3_4'),
    'SUB_3.5_ImpacNprod':('Viabilidad del Producto',    'score_sub3_5'),
    'SUB_4.1_InnEstrat':('Inn. Estratégica',            'score_sub4_1'),
    'SUB_4.2_CultInn':  ('Cultura Innovadora',          'score_sub4_2'),
    'SUB_4.3_Obstac':   ('Gestión Obstáculos',          'score_sub4_3'),
    'SUB_4.4_InnAb':    ('Innovación Abierta',          'score_sub4_4'),
    'SUB_4.5_Creativ':  ('Creatividad y Talento',       'score_sub4_5'),
    'SUB_5.1_ImpEstim': ('Impacto Estimado',            'score_sub5_1'),
    'SUB_5.2_InnEfect': ('Efecto Real Innovación',      'score_sub5_2'),
}

IND_INFO = {
    'IND_IDi':      ('I+D+i',               b1, ['SUB_1.1_Dpto','SUB_1.2_PresupID','SUB_1.3_Gasto']),
    'IND_GPROY':    ('Gestión Proyectos',    b2, ['SUB_2.1_Gbasica','SUB_2.2_Gavanz','SUB_2.3_OrgProy','SUB_2.4_EvalRdto']),
    'IND_DESPROD':  ('Desarrollo Productos', b3, ['SUB_3.1_EstrDes','SUB_3.2_OportMdo','SUB_3.3_RecepNprod','SUB_3.4_Clientes','SUB_3.5_ImpacNprod']),
    'IND_ESTRINN':  ('Estrategia Innovación',b4, ['SUB_4.1_InnEstrat','SUB_4.2_CultInn','SUB_4.3_Obstac','SUB_4.4_InnAb','SUB_4.5_Creativ']),
    'IND_DESMPINN': ('Desempeño Innovación', b5, ['SUB_5.1_ImpEstim','SUB_5.2_InnEfect']),
}

# Obtener valores de subindicadores
sub_vals = {}
for col, (nombre, key) in SUBS.items():
    val = st.session_state.get(key, 0)
    if val == 0 and col in dff.columns:
        val = 0  # no rellenamos con media, mostramos 0 si no hay dato
    sub_vals[col] = val

# Medias del grupo
ind_medias = {cod: round(dff[cod].mean(),2) if cod in dff.columns else 3.0
              for cod in IND_INFO}
sub_medias = {col: round(dff[col].mean(),2) if col in dff.columns else 3.0
              for col in SUBS}
macro_media = round(dff['MACRO_INNOVACION'].mean(),2) if 'MACRO_INNOVACION' in dff.columns else 3.0

# Percentiles
def pct(series, val, inv=False):
    if inv: return float(np.sum(series >= val)/len(series)*100)
    return float(np.sum(series <= val)/len(series)*100)

def col_v(v, mx=5):
    r = v/mx
    if r >= 0.66: return '#10b981'
    if r >= 0.40: return '#f59e0b'
    return '#ef4444'

def col_pct(v):
    if v >= 66: return '#10b981'
    if v >= 33: return '#f59e0b'
    return '#ef4444'

def nivel(v, mx=5):
    r = v/mx
    if r >= 0.66: return 'Alto'
    if r >= 0.40: return 'Medio'
    return 'Bajo'

def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD',s)
                   if unicodedata.category(c) != 'Mn').upper()

ind_pcts = {cod: round(pct(dff[cod], vals[1])) if cod in dff.columns else 50
            for cod, vals in IND_INFO.items()}
macro_pct = round(pct(dff['MACRO_INNOVACION'], macro_inn)) if 'MACRO_INNOVACION' in dff.columns else 50

# ── Items débiles más relevantes por bloque ────────────────────────────────
ITEMS_NOMBRES = {
    'IT_1.1.1_RecTec':'recursos tecnológicos para I+D',
    'IT_1.1.2_RecHum':'recursos humanos especializados en I+D',
    'IT_1.2.1_Presup':'presupuesto específico para I+D',
    'IT_1.2.2_SubvID':'obtención de subvenciones para I+D',
    'IT_1.2.3_IDPubl':'colaboración con organismos públicos de I+D',
    'IT_1.3.1_Gventas':'gasto en innovación sobre ventas',
    'IT_1.3.2_EvolFut':'evolución prevista del gasto en innovación',
    'IT_2.1.1_Multidis':'equipos multidisciplinares en proyectos',
    'IT_2.1.2_Consenso':'toma de decisiones por consenso',
    'IT_2.1.3_ApoyoDir':'apoyo de la dirección a proyectos',
    'IT_2.1.4_Planific':'planificación formal de proyectos',
    'IT_2.2.1_TecAvanz':'uso de tecnologías avanzadas',
    'IT_2.2.2_PropInd':'protección de propiedad industrial',
    'IT_2.2.3_GestAgil':'metodologías ágiles de gestión',
    'IT_2.3.1_AdmProy':'responsable formal de proyectos',
    'IT_2.3.2_CompetEq':'competencias del equipo de proyectos',
    'IT_2.4.1_RdtoProy':'seguimiento del rendimiento de proyectos',
    'IT_2.4.2_RdosProy':'evaluación de resultados de proyectos',
    'IT_3.1.1EstrNProd':'estrategia formal de nuevos productos',
    'IT_3.1.2_RecNprod':'recursos asignados a nuevos productos',
    'IT_3.2.1_IdentOp':'identificación de oportunidades de mercado',
    'IT_3.2.2_TamInn':'evaluación del tamaño del mercado innovador',
    'IT_3.2.3_CrecProd':'análisis del crecimiento del producto',
    'IT_3.2.4_RentProd':'análisis de rentabilidad del producto',
    'IT_3.3.1_Probar':'disposición del cliente a probar el producto',
    'IT_3.3.2_Pagar':'disposición del cliente a pagar por el producto',
    'IT_3.3.3_Valor':'percepción del valor por el cliente',
    'IT_3.4.1_Diseño':'diseño centrado en el cliente',
    'IT_3.4.2_Interac':'interacción activa con clientes en desarrollo',
    'IT_3.5.1_Ecofinanc':'viabilidad económico-financiera del producto',
    'IT_3.5.2_ViabCom':'viabilidad comercial del nuevo producto',
    'IT_4.1.1_Alinear':'alineación innovación con estrategia corporativa',
    'IT_4.1.2_LiderIT':'liderazgo directivo en innovación',
    'IT_4.1.3_ObjInn':'objetivos formales de innovación',
    'IT.4.2.1.Increm':'tolerancia al riesgo incremental',
    'IT_4.2.2_Riesgo':'cultura de asunción de riesgos',
    'IT_4.2.3_ConInterno':'conocimiento interno sobre innovación',
    'IT_4.3.1_ObstInt':'obstáculos internos a la innovación',
    'IT_4.3.2_ObstExt':'obstáculos externos a la innovación',
    'IT_4.4.1_ColabInn':'colaboración externa en innovación',
    'IT_4.4.2_RdCoop':'redes de cooperación para innovar',
    'IT_4.5.1_Ideas':'generación sistemática de ideas',
    'IT_4.5.2_EvalIdeas':'evaluación y selección de ideas',
    'IT_5.1.1_InnProd':'impacto de la innovación en productos',
    'IT_5.1.2_InnProc':'innovación en procesos',
    'IT_5.1.3.InnOrg':'innovación organizacional',
    'IT_5.2.1_NumNProd':'número de nuevos productos lanzados',
    'IT_5.2.1_PorcVtas':'porcentaje de ventas de nuevos productos',
    'IT_5.2.3_InnExito':'tasa de éxito de innovaciones lanzadas',
}

ITEM_SUB = {
    'SUB_1.1_Dpto':['IT_1.1.1_RecTec','IT_1.1.2_RecHum'],
    'SUB_1.2_PresupID':['IT_1.2.1_Presup','IT_1.2.2_SubvID','IT_1.2.3_IDPubl'],
    'SUB_1.3_Gasto':['IT_1.3.1_Gventas','IT_1.3.2_EvolFut'],
    'SUB_2.1_Gbasica':['IT_2.1.1_Multidis','IT_2.1.2_Consenso','IT_2.1.3_ApoyoDir','IT_2.1.4_Planific'],
    'SUB_2.2_Gavanz':['IT_2.2.1_TecAvanz','IT_2.2.2_PropInd','IT_2.2.3_GestAgil'],
    'SUB_2.3_OrgProy':['IT_2.3.1_AdmProy','IT_2.3.2_CompetEq'],
    'SUB_2.4_EvalRdto':['IT_2.4.1_RdtoProy','IT_2.4.2_RdosProy'],
    'SUB_3.1_EstrDes':['IT_3.1.1EstrNProd','IT_3.1.2_RecNprod'],
    'SUB_3.2_OportMdo':['IT_3.2.1_IdentOp','IT_3.2.2_TamInn','IT_3.2.3_CrecProd','IT_3.2.4_RentProd'],
    'SUB_3.3_RecepNprod':['IT_3.3.1_Probar','IT_3.3.2_Pagar','IT_3.3.3_Valor'],
    'SUB_3.4_Clientes':['IT_3.4.1_Diseño','IT_3.4.2_Interac'],
    'SUB_3.5_ImpacNprod':['IT_3.5.1_Ecofinanc','IT_3.5.2_ViabCom'],
    'SUB_4.1_InnEstrat':['IT_4.1.1_Alinear','IT_4.1.2_LiderIT','IT_4.1.3_ObjInn'],
    'SUB_4.2_CultInn':['IT.4.2.1.Increm','IT_4.2.2_Riesgo','IT_4.2.3_ConInterno'],
    'SUB_4.3_Obstac':['IT_4.3.1_ObstInt','IT_4.3.2_ObstExt'],
    'SUB_4.4_InnAb':['IT_4.4.1_ColabInn','IT_4.4.2_RdCoop'],
    'SUB_4.5_Creativ':['IT_4.5.1_Ideas','IT_4.5.2_EvalIdeas'],
    'SUB_5.1_ImpEstim':['IT_5.1.1_InnProd','IT_5.1.2_InnProc','IT_5.1.3.InnOrg'],
    'SUB_5.2_InnEfect':['IT_5.2.1_NumNProd','IT_5.2.1_PorcVtas','IT_5.2.3_InnExito'],
}

def items_debiles_bloque(sub_col):
    items = ITEM_SUB.get(sub_col, [])
    debiles = []
    for it in items:
        if it not in dff.columns: continue
        mi_val = st.session_state.get(f"val_{it.replace('.','_')}", 0)
        if mi_val == 0: continue
        media = dff[it].mean()
        p25   = dff[it].quantile(0.25)
        if mi_val < p25:
            debiles.append((ITEMS_NOMBRES.get(it, it), round(mi_val,2), round(media,2), 'crítico'))
        elif mi_val < media - 0.2:
            debiles.append((ITEMS_NOMBRES.get(it, it), round(mi_val,2), round(media,2), 'débil'))
    return sorted(debiles, key=lambda x: x[1])[:2]  # máx 2 por subindicador

# Construir resumen de brechas para la IA
def resumen_brechas():
    lineas = []
    for cod, (nombre, val, subs_lista) in IND_INFO.items():
        media = ind_medias[cod]
        p_ind = ind_pcts[cod]
        lineas.append(f"\n[{nombre}]: {val:.2f}/5 vs media {media:.2f} (P{p_ind})")
        for sub in subs_lista:
            sv = sub_vals.get(sub, 0)
            sm = sub_medias.get(sub, 3.0)
            sn = SUBS[sub][0]
            if sv > 0:
                gap = round(sv - sm, 2)
                lineas.append(f"  • {sn}: {sv:.2f}/5 vs {sm:.2f} (gap {gap:+.2f})")
                # Items débiles
                for nombre_it, mi_v, med_v, grav in items_debiles_bloque(sub):
                    lineas.append(f"    → {grav.upper()}: '{nombre_it}' ({mi_v}/5 vs media {med_v}/5)")
    return "\n".join(lineas)

# ═══════════════════════════════════════════════════════════════════════════
# LLAMADA IA
# ═══════════════════════════════════════════════════════════════════════════
def llamar_ia():
    if not ANTHROPIC_API_KEY:
        return "ERROR: API Key no configurada."

    brechas = resumen_brechas()

    # Mapa indicador → color para el prompt
    ind_resumen = " | ".join([
        f"{vals[0]}: {vals[1]:.2f}/5 (P{ind_pcts[cod]}°)"
        for cod, vals in IND_INFO.items()
    ])

    prompt = f"""Eres un consultor experto en innovación empresarial. Redacta un informe ejecutivo de diagnóstico de innovación en español. Máximo 750 palabras. Tono directo y profesional. Escribe en párrafos narrativos fluidos.

PERFIL: {nom_sector} | {nom_tam} | {nom_reg} | Exportación: {nom_export} | Antigüedad: {nom_anti}
Grupo de referencia: {n_ref} empresas comparables.

ÍNDICE GLOBAL DE INNOVACIÓN: {macro_inn:.2f}/5 (percentil {macro_pct}° en el grupo)

LOS 5 INDICADORES (siempre menciónalos por este nombre exacto):
{ind_resumen}

ANÁLISIS DETALLADO POR BLOQUE:
{brechas}

REGLAS DE FORMATO OBLIGATORIAS — MUY IMPORTANTES:
1. Cada vez que menciones un indicador, escríbelo entre corchetes dobles así: [[I+D+i]], [[Gestión Proyectos]], [[Desarrollo Productos]], [[Estrategia Innovación]], [[Desempeño Innovación]]. Esto es crítico para el resaltado visual.
2. Antes de mencionar cualquier subindicador o ítem débil, identifica SIEMPRE el indicador al que pertenece: "En [[Gestión Proyectos]] (2,8/5), la gestión avanzada muestra..."
3. Las recomendaciones deben empezar identificando el indicador afectado: "1. [[Estrategia Innovación]]: Implementar..."
4. Nunca menciones un subindicador sin haber nombrado antes su indicador padre en el mismo párrafo.

INSTRUCCIONES DE CONTENIDO:
- Identifica PATRONES sistémicos, no solo puntuaciones individuales.
- Menciona máximo 2-3 ítems concretos por nombre en todo el informe, los más relevantes.
- Conecta debilidades de innovación con consecuencias reales en competitividad.
- Recomendaciones: acciones concretas con horizonte temporal y resultado esperado.

TONO Y ESTILO — OBLIGATORIO:
- Escribe como un consultor estratégico senior (estilo McKinsey, BCG). Tono sobrio, preciso y constructivo.
- PROHIBIDO: "alarmante", "crítico", "catastrófico", "grave", "urgente", "preocupante", "peligroso", "severo", "excelente", "fantástico", "brillante", "impresionante".
- USA EN SU LUGAR: "por debajo de la media del sector", "margen de mejora relevante", "área de desarrollo prioritario", "posición sólida", "ventaja competitiva sostenida", "brecha que merece atención", "oportunidad de mejora", "inferior a la media del grupo", "superior a la media".
- Las debilidades se presentan como oportunidades de mejora, no como fracasos.
- Los datos numéricos contextualizan, no dramatizan.

ESTRUCTURA EXACTA — usa estos 3 títulos con ##:

## DIAGNOSTICO DE INNOVACION
2 párrafos. Perfil innovador general. Menciona el índice global y los 2-3 indicadores más relevantes con [[nombre]].

## FORTALEZAS Y BRECHAS
2 párrafos. Fortalezas primero con [[indicador]] y datos. Luego brechas críticas, siempre empezando por [[indicador]] antes de bajar al subindicador o ítem concreto.

## RECOMENDACIONES Y PREDICCION
3 recomendaciones numeradas, cada una empezando por [[indicador afectado]]. Luego 1 párrafo de predicción: escenario si actúa vs si no actúa en 2-3 años.

Escribe los títulos SIN tildes tal como aparecen arriba."""

    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type":"application/json",
                     "x-api-key": ANTHROPIC_API_KEY,
                     "anthropic-version":"2023-06-01"},
            json={"model":"claude-sonnet-4-20250514","max_tokens":1600,
                  "messages":[{"role":"user","content":prompt}]},
            timeout=45
        )
        data = resp.json()
        if 'content' in data and data['content']:
            return data['content'][0]['text']
        return f"ERROR: {data.get('error',{}).get('message','Respuesta inesperada')}"
    except requests.exceptions.Timeout:
        return "ERROR: Tiempo de espera agotado. Inténtalo de nuevo."
    except Exception as e:
        return f"ERROR: {e}"

def parsear(texto):
    resultado = []
    for parte in [p.strip() for p in texto.split('##') if p.strip()]:
        lineas = parte.split('\n',1)
        titulo_orig = lineas[0].strip()
        cuerpo = lineas[1].strip() if len(lineas)>1 else ''
        resultado.append((norm(titulo_orig), titulo_orig, cuerpo))
    return resultado

def buscar(secciones, *kws):
    for tn, to, cu in secciones:
        for kw in kws:
            if norm(kw) in tn: return cu
    return None

def render(texto, estilo='normal'):
    if not texto: return ''
    import re
    # Colores por indicador
    IND_COLORES_TEXT = {
        'I+D+i':                '#3b82f6',
        'Gestión Proyectos':    '#8b5cf6',
        'Gestión de Proyectos': '#8b5cf6',
        'Desarrollo Productos': '#10b981',
        'Estrategia Innovación':'#f59e0b',
        'Estrategia de Innovación':'#f59e0b',
        'Desempeño Innovación': '#ef4444',
        'Desempeño de la Innovación':'#ef4444',
    }
    def reemplazar(m):
        nombre = m.group(1).strip()
        color = '#00d4ff'  # color por defecto
        for k, c in IND_COLORES_TEXT.items():
            if k.lower() in nombre.lower():
                color = c; break
        return (f'<span style="color:{color};font-weight:700;'
                f'background:rgba(255,255,255,0.06);'
                f'border-radius:4px;padding:1px 6px;">{nombre}</span>')

    texto = re.sub(r'\[\[(.+?)\]\]', reemplazar, texto)
    html = texto.replace('\n\n','</p><p>').replace('\n','<br>')
    css = {'normal':'text-block','rec':'rec-block','pred':'pred-block'}.get(estilo,'text-block')
    return f'<div class="{css}"><p>{html}</p></div>'

# ═══════════════════════════════════════════════════════════════════════════
# CABECERA
# ═══════════════════════════════════════════════════════════════════════════
macro_c = col_v(macro_inn)
st.markdown(f"""
<div class="report-header">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;">
    <div>
      <div style="font-size:.7rem;color:#64748b;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">
        Informe de Innovación · Diagnóstico por Bloques</div>
      <h1 style="font-family:Rajdhani,sans-serif;color:#10b981;margin:0;font-size:2rem;">{nom_sector}</h1>
      <p style="color:#94a3b8;margin:6px 0 0 0;font-size:.88rem;">
        {nom_tam} · {nom_reg} · Exportación: {nom_export} · {nom_anti}<br>
        <span style="color:#64748b;font-size:.8rem;">Referencia: {n_ref} empresas · {hoy}</span>
      </p>
    </div>
    <div style="text-align:center;background:rgba(0,0,0,0.35);border:1px solid {macro_c}55;
                border-radius:12px;padding:16px 28px;">
      <div style="font-size:.65rem;color:#64748b;letter-spacing:1.5px;text-transform:uppercase;">
        Índice Global de Innovación</div>
      <div style="font-family:Rajdhani,sans-serif;font-size:4.2rem;font-weight:700;
                  color:{macro_c};line-height:1;">{macro_inn:.2f}</div>
      <div style="font-size:.78rem;color:#94a3b8;">/ 5 · Percentil {macro_pct}° · {nivel(macro_inn)}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPIs 5 bloques ─────────────────────────────────────────────────────────
kcols = st.columns(5)
for col_st, (cod, (nombre, val, _)) in zip(kcols, IND_INFO.items()):
    p_ind = ind_pcts[cod]
    col_st.markdown(f"""
    <div class="kpi-inn">
      <div style="font-size:.62rem;color:#64748b;letter-spacing:.5px;">{nombre}</div>
      <div style="font-family:Rajdhani,sans-serif;font-size:1.9rem;font-weight:700;
                  color:{col_v(val)};">{val:.2f}</div>
      <div style="font-size:.7rem;color:#64748b;">/ 5 · P{p_ind}°</div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# GRÁFICO 1 — VELOCÍMETROS 5 INDICADORES
# ═══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">⚡ Los 5 Indicadores de Innovación</div>', unsafe_allow_html=True)

gcols = st.columns(5)
for col_st, (cod, (nombre, val, _)) in zip(gcols, IND_INFO.items()):
    media = ind_medias[cod]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=val,
        number={'font':{'size':26,'color':col_v(val)},'valueformat':'.2f'},
        title={'text':f"{nombre[:18]}<br><span style='font-size:8px;color:#64748b;'>Media: {media:.2f}</span>",
               'font':{'size':10,'color':'#94a3b8'}},
        gauge={
            'axis':{'range':[0,5],'tickcolor':'#334155','tickfont':{'color':'#64748b','size':7}},
            'bar':{'color':col_v(val),'thickness':0.28},
            'bgcolor':'#0a0e1a','borderwidth':0,
            'steps':[{'range':[0,2],'color':'#1a0505'},
                     {'range':[2,3.3],'color':'#1a1200'},
                     {'range':[3.3,5],'color':'#051a0a'}],
            'threshold':{'line':{'color':'#475569','width':2},
                         'thickness':0.75,'value':media}
        }
    ))
    fig.update_layout(height=195,margin=dict(l=8,r=8,t=45,b=4),
                      paper_bgcolor='rgba(0,0,0,0)')
    col_st.plotly_chart(fig, use_container_width=True)

st.caption("La línea gris marca la media del grupo de referencia en cada indicador.")

# ═══════════════════════════════════════════════════════════════════════════
# GRÁFICO 2 — BARRAS AGRUPADAS: INDICADOR + SUBINDICADORES
# ═══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📊 Indicadores y Subindicadores vs. Grupo</div>', unsafe_allow_html=True)

# Construir datos para barras agrupadas
categorias = []
vals_emp   = []
vals_grp   = []
colores_emp= []
es_ind     = []   # True si es indicador principal, False si subindicador

IND_COLORES = {
    'IND_IDi':      '#3b82f6',
    'IND_GPROY':    '#8b5cf6',
    'IND_DESPROD':  '#10b981',
    'IND_ESTRINN':  '#f59e0b',
    'IND_DESMPINN': '#ef4444',
}
SUB_COLORES = {
    'IND_IDi':      'rgba(59,130,246,0.55)',
    'IND_GPROY':    'rgba(139,92,246,0.55)',
    'IND_DESPROD':  'rgba(16,185,129,0.55)',
    'IND_ESTRINN':  'rgba(245,158,11,0.55)',
    'IND_DESMPINN': 'rgba(239,68,68,0.55)',
}

for cod, (nombre, val, subs_lista) in IND_INFO.items():
    # Indicador principal
    categorias.append(nombre[:16])
    vals_emp.append(round(val,2))
    vals_grp.append(ind_medias[cod])
    colores_emp.append(IND_COLORES[cod])
    es_ind.append(True)
    # Subindicadores
    for sub in subs_lista:
        sv = sub_vals.get(sub, 0)
        sm = sub_medias.get(sub, 3.0)
        sn = SUBS[sub][0][:20]
        categorias.append(f"  ↳ {sn}")
        vals_emp.append(round(sv,2) if sv > 0 else 0)
        vals_grp.append(sm)
        colores_emp.append(SUB_COLORES[cod])
        es_ind.append(False)

bar_h = max(500, len(categorias) * 26)

bar_opt = {
    "backgroundColor":"#0a1a0e",
    "tooltip":{"trigger":"axis","axisPointer":{"type":"shadow"},
               "backgroundColor":"#1e293b","textStyle":{"color":"#e2e8f0"}},
    "legend":{"data":["Mi Empresa","Media Grupo"],
              "textStyle":{"color":"#94a3b8"},"top":5},
    "grid":{"left":"2%","right":"8%","bottom":"3%","top":"8%","containLabel":True},
    "xAxis":{"type":"value","min":0,"max":5,
             "axisLabel":{"color":"#64748b"},
             "splitLine":{"lineStyle":{"color":"#1e3a2a"}}},
    "yAxis":{"type":"category","data":categorias,"inverse":True,
             "axisLabel":{"color":"#94a3b8","fontSize":10}},
    "series":[
        {"name":"Mi Empresa","type":"bar",
         "data":[{"value":v,
                  "itemStyle":{"color":c,
                               "borderRadius":[0,4,4,0],
                               "borderWidth": 2 if ind else 0,
                               "borderColor": c}}
                 for v,c,ind in zip(vals_emp, colores_emp, es_ind)],
         "label":{"show":False},
         "barMaxWidth":18},
        {"name":"Media Grupo","type":"bar",
         "data":[{"value":v,"itemStyle":{"color":"rgba(100,116,139,0.4)",
                                          "borderRadius":[0,4,4,0]}}
                 for v in vals_grp],
         "label":{"show":False},
         "barMaxWidth":10},
    ],
    "barGap":"10%",
}
st_echarts(options=bar_opt, height=f"{bar_h}px")

# ═══════════════════════════════════════════════════════════════════════════
# BOTÓN IA
# ═══════════════════════════════════════════════════════════════════════════
st.divider()
if not ANTHROPIC_API_KEY:
    st.warning("⚠️ API Key no configurada. Consulta las instrucciones.")

col_btn, col_hint = st.columns([1,2])
with col_btn:
    generar = st.button("🚀 Generar Informe de Innovación con IA",
                        type="primary", use_container_width=True)
with col_hint:
    st.info("La IA analiza todos los bloques, subindicadores e ítems críticos para redactar un diagnóstico personalizado. ~15-25 segundos.")

if generar:
    with st.spinner("Analizando tu perfil innovador..."):
        texto = llamar_ia()
        st.session_state['inf2_texto'] = texto

texto_raw = st.session_state.get('inf2_texto','')
if texto_raw.startswith('ERROR:'):
    st.error(f"❌ {texto_raw}")
    st.stop()
secciones = parsear(texto_raw) if texto_raw else []

# ═══════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 — DIAGNÓSTICO
# ═══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🔍 Diagnóstico de Innovación</div>', unsafe_allow_html=True)
txt = buscar(secciones,'DIAGNOSTICO','INNOVACION','PERFIL')
if txt:
    st.markdown(render(txt), unsafe_allow_html=True)
else:
    st.markdown('<div class="pending">Pulsa "Generar Informe" para ver el diagnóstico personalizado.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# GRÁFICO 3 — RADAR 5 INDICADORES vs GRUPO
# ═══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🕸️ Radar de los 5 Indicadores vs. Grupo</div>', unsafe_allow_html=True)

ind_labels = [v[0] for v in IND_INFO.values()]
emp_ind    = [round(v[1],2) for v in IND_INFO.values()]
grp_ind    = [ind_medias[c] for c in IND_INFO]

cr1, _ = st.columns([1,1])
with cr1:
    r1_opt = {
        "backgroundColor":"#0a1a0e",
        "tooltip":{"trigger":"item","backgroundColor":"#1e293b","textStyle":{"color":"#e2e8f0"}},
        "legend":{"data":["Mi Empresa","Media Grupo"],"textStyle":{"color":"#94a3b8"},"bottom":0},
        "radar":{
            "indicator":[{"name":n,"max":5} for n in ind_labels],
            "shape":"polygon","splitNumber":5,
            "axisName":{"color":"#94a3b8","fontSize":13},
            "splitLine":{"lineStyle":{"color":["#1e3a2a"]*5}},
            "splitArea":{"areaStyle":{"color":["rgba(16,185,129,0.02)","rgba(16,185,129,0.06)"]}},
            "axisLine":{"lineStyle":{"color":"#1e3a2a"}},
            "radius":"65%",
        },
        "series":[{"type":"radar","data":[
            {"value":emp_ind,"name":"Mi Empresa",
             "itemStyle":{"color":"#10b981"},"lineStyle":{"color":"#10b981","width":2},
             "areaStyle":{"color":"rgba(16,185,129,0.2)"},"symbol":"circle","symbolSize":7},
            {"value":grp_ind,"name":"Media Grupo",
             "itemStyle":{"color":"#f59e0b"},"lineStyle":{"color":"#f59e0b","width":1.5,"type":"dashed"},
             "areaStyle":{"color":"rgba(245,158,11,0.06)"}},
        ]}],
    }
    st_echarts(options=r1_opt, height="400px")

# GRÁFICO 4 — RADAR TODOS LOS SUBINDICADORES — ancho completo
st.markdown('<div class="section-title">🕸️ Radar de los 19 Subindicadores vs. Grupo</div>', unsafe_allow_html=True)
st.caption("Cada eje representa un subindicador. El área azul es tu empresa, la línea naranja la media del grupo.")

sub_labels_r = [SUBS[s][0][:24] for s in SUBS]
emp_sub_r    = [round(sub_vals.get(s,0),2) for s in SUBS]
grp_sub_r    = [sub_medias.get(s,3.0) for s in SUBS]

r2_opt = {
    "backgroundColor":"#0a1a0e",
    "tooltip":{"trigger":"item","backgroundColor":"#1e293b","textStyle":{"color":"#e2e8f0"}},
    "legend":{"data":["Mi Empresa","Media Grupo"],"textStyle":{"color":"#94a3b8"},"bottom":0},
    "radar":{
        "indicator":[{"name":n,"max":5} for n in sub_labels_r],
        "shape":"polygon","splitNumber":5,
        "axisName":{"color":"#94a3b8","fontSize":10},
        "splitLine":{"lineStyle":{"color":["#1e3a2a"]*5}},
        "splitArea":{"areaStyle":{"color":["rgba(16,185,129,0.02)","rgba(16,185,129,0.05)"]}},
        "axisLine":{"lineStyle":{"color":"#1e3a2a"}},
        "radius":"58%",
        "center":["50%","52%"],
    },
    "series":[{"type":"radar","data":[
        {"value":emp_sub_r,"name":"Mi Empresa",
         "itemStyle":{"color":"#10b981"},"lineStyle":{"color":"#10b981","width":2},
         "areaStyle":{"color":"rgba(16,185,129,0.18)"},"symbol":"circle","symbolSize":5},
        {"value":grp_sub_r,"name":"Media Grupo",
         "itemStyle":{"color":"#f59e0b"},"lineStyle":{"color":"#f59e0b","width":1.5,"type":"dashed"},
         "areaStyle":{"color":"rgba(245,158,11,0.05)"}},
    ]}],
}
st_echarts(options=r2_opt, height="580px")

# ═══════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 — FORTALEZAS Y BRECHAS
# ═══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">⚖️ Fortalezas y Brechas de Innovación</div>', unsafe_allow_html=True)

cf, crank = st.columns([1,1])
with cf:
    txt = buscar(secciones,'FORTALEZA','BRECHA','DEBILIDAD')
    if txt:
        st.markdown(render(txt), unsafe_allow_html=True)
    else:
        st.markdown('<div class="pending">Fortalezas y brechas pendientes de generación.</div>', unsafe_allow_html=True)

# GRÁFICO 5 — RANKING PERCENTIL SUBINDICADORES
with crank:
    st.caption("**Ranking Percentil de Subindicadores**")
    sub_pcts_lista = []
    for sub_col, (sub_nombre, key) in SUBS.items():
        sv = sub_vals.get(sub_col, 0)
        if sv > 0 and sub_col in dff.columns:
            p = round(pct(dff[sub_col], sv))
            sub_pcts_lista.append((sub_nombre[:25], p))
    sub_pcts_lista.sort(key=lambda x: x[1])

    if sub_pcts_lista:
        s_labels = [x[0] for x in sub_pcts_lista]
        s_vals   = [x[1] for x in sub_pcts_lista]
        s_colors = [col_pct(v) for v in s_vals]
        rank_sub_opt = {
            "backgroundColor":"#0a1a0e",
            "tooltip":{"trigger":"axis","backgroundColor":"#1e293b","textStyle":{"color":"#e2e8f0"}},
            "grid":{"left":"2%","right":"12%","bottom":"3%","containLabel":True},
            "xAxis":{"type":"value","min":0,"max":100,
                     "axisLabel":{"color":"#64748b"},
                     "splitLine":{"lineStyle":{"color":"#1e3a2a"}}},
            "yAxis":{"type":"category","data":s_labels,"inverse":True,
                     "axisLabel":{"color":"#94a3b8","fontSize":9}},
            "series":[{
                "type":"bar",
                "data":[{"value":v,"itemStyle":{"color":c,"borderRadius":[0,4,4,0]}}
                        for v,c in zip(s_vals,s_colors)],
                "label":{"show":True,"position":"right","color":"#e2e8f0",
                         "fontSize":10,"formatter":"{c}°"},
                "markLine":{"silent":True,
                            "lineStyle":{"color":"#f59e0b","type":"dashed","width":1.5},
                            "data":[{"xAxis":50,"label":{"formatter":"Mediana",
                                                          "color":"#f59e0b","fontSize":9}}]},
            }]
        }
        h_rank = max(350, len(s_labels)*28)
        st_echarts(options=rank_sub_opt, height=f"{h_rank}px")
    else:
        st.info("Completa el cuestionario para ver el ranking de subindicadores.")

# ═══════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 — RECOMENDACIONES Y PREDICCIÓN
# ═══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🎯 Recomendaciones y Predicción</div>', unsafe_allow_html=True)

txt_rec = buscar(secciones,'RECOMENDACION','PREDICCION','ACCION')
if txt_rec:
    parrafos = [p.strip() for p in txt_rec.split('\n\n') if p.strip()]
    # Detectar recomendaciones: párrafos que empiezan por dígito + punto
    recs  = [p for p in parrafos if p and p[0].isdigit() and '.' in p[:3]]
    preds = [p for p in parrafos if p not in recs]
    # Si no detectamos estructura, mostrar todo junto
    if not recs and not preds:
        st.markdown(render(txt_rec, 'rec'), unsafe_allow_html=True)
    else:
        if recs:
            rec_html = '</p><p>'.join(recs)
            st.markdown(f'<div class="rec-block"><p>{rec_html}</p></div>', unsafe_allow_html=True)
        if preds:
            pred_html = '</p><p>'.join(preds)
            st.markdown(f'<div class="pred-block"><p>{pred_html}</p></div>', unsafe_allow_html=True)
else:
    c1,c2 = st.columns(2)
    c1.markdown('<div class="pending">Recomendaciones pendientes.</div>', unsafe_allow_html=True)
    c2.markdown('<div class="pending">Predicción pendiente.</div>', unsafe_allow_html=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# DESCARGA HTML
# ═══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📥 Descargar Informe</div>', unsafe_allow_html=True)

def generar_html():
    ia_html = ""
    colores = {'DIAGNOSTICO':'#0a7a3a','FORTALEZA':'#dc2626',
               'BRECHA':'#dc2626','RECOMENDACION':'#d97706','PREDICCION':'#7c3aed'}
    for tn, to, cu in secciones:
        color = '#0a7a3a'
        for kw,c in colores.items():
            if kw in tn: color=c; break
        ia_html += f"<h2 style='color:{color};border-left:4px solid {color};padding-left:10px;margin-top:28px;'>{to}</h2><p style='line-height:1.75;'>{cu.replace(chr(10),'<br>')}</p>"

    ind_tabla = "".join([
        f"<tr><td><b>{cod}</b></td><td>{vals[0]}</td>"
        f"<td style='text-align:center;font-weight:700;color:{'green' if vals[1]>=3.3 else 'orange' if vals[1]>=2 else 'red'};'>{vals[1]:.2f}/5</td>"
        f"<td style='text-align:center;color:#666;'>{ind_medias[cod]:.2f}/5</td>"
        f"<td style='text-align:center;'>{ind_pcts[cod]}°</td></tr>"
        for cod, vals in IND_INFO.items()
    ])

    return f"""<!DOCTYPE html><html><head><meta charset='utf-8'>
<style>body{{font-family:Georgia,serif;margin:50px auto;max-width:860px;color:#1a1a1a;line-height:1.75;}}
h1{{color:#0a7a3a;border-bottom:3px solid #0a7a3a;padding-bottom:10px;font-size:1.8rem;}}
.perfil{{background:#f0fff4;border-radius:8px;padding:16px;margin:16px 0;font-size:.9rem;}}
.inn-global{{font-size:2.8rem;font-weight:700;color:{'green' if macro_inn>=3.3 else 'orange' if macro_inn>=2 else 'red'};}}
table{{border-collapse:collapse;width:100%;margin:16px 0;font-size:.9rem;}}
th{{background:#0a7a3a;color:white;padding:10px;text-align:left;}}
td{{padding:9px 11px;border-bottom:1px solid #e5e7eb;}}
@media print{{body{{margin:20px;}}}}</style></head><body>
<h1>Informe de Innovación · Diagnóstico por Bloques</h1>
<div class="perfil">
<strong>{nom_sector}</strong> &nbsp;|&nbsp; {nom_tam} &nbsp;|&nbsp; {nom_reg}
&nbsp;|&nbsp; Exportación: {nom_export} &nbsp;|&nbsp; {nom_anti}<br>
Referencia: <strong>{n_ref} empresas comparables</strong> &nbsp;|&nbsp; Fecha: {hoy}
</div>
<p>Índice Global de Innovación: <span class="inn-global">{macro_inn:.2f}</span> / 5
&nbsp;·&nbsp; Percentil {macro_pct}° &nbsp;·&nbsp; {nivel(macro_inn)}</p>
<h2 style='color:#0a7a3a;'>Indicadores de Innovación</h2>
<table><tr><th>Código</th><th>Indicador</th><th>Mi Empresa</th><th>Media Grupo</th><th>Percentil</th></tr>
{ind_tabla}</table>
{ia_html if ia_html else '<p style="color:#6b7280;font-style:italic;">Genera el análisis IA antes de descargar.</p>'}
<hr style='margin-top:40px;'/>
<p style='color:#9ca3af;font-size:.78rem;text-align:center;'>Plataforma de Diagnóstico Estratégico · {hoy}</p>
</body></html>"""

html_out = generar_html()
c1, c2 = st.columns(2)
with c1:
    st.download_button("📥 Descargar Informe HTML", data=html_out,
        file_name=f"informe_innovacion_{nom_sector[:15].replace(' ','_')}.html",
        mime="text/html", type="primary", use_container_width=True)
with c2:
    st.info("Abre el HTML en tu navegador → **Ctrl+P** → **Guardar como PDF**")