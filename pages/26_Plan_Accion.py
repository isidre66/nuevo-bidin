import streamlit as st
from control_acceso import verificar_acceso
verificar_acceso('manager')
from asistentes import mostrar_felix
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests, json, os, unicodedata
from datetime import date

st.set_page_config(page_title="Plan de Acción & Hoja de Ruta", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&display=swap');

.page-header {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1b2a 50%, #1a1a2e 100%);
    border: 1px solid #1e3a5f; border-radius: 16px;
    padding: 28px 32px; margin-bottom: 10px; position: relative; overflow: hidden;
}
.page-header::before {
    content: ''; position: absolute; top: -60px; right: -60px;
    width: 200px; height: 200px; border-radius: 50%;
    background: radial-gradient(circle, rgba(0,212,255,0.08), transparent 70%);
}

.section-title {
    font-family: 'Rajdhani', sans-serif; font-size: 1.15rem; font-weight: 700; color: #e2e8f0;
    background: linear-gradient(90deg, rgba(0,212,255,0.18), rgba(0,212,255,0));
    border-left: 5px solid #00d4ff; padding: 9px 16px; border-radius: 0 8px 8px 0;
    margin: 24px 0 12px 0;
}
.section-title-gold {
    font-family: 'Rajdhani', sans-serif; font-size: 1.15rem; font-weight: 700; color: #e2e8f0;
    background: linear-gradient(90deg, rgba(245,158,11,0.18), rgba(245,158,11,0));
    border-left: 5px solid #f59e0b; padding: 9px 16px; border-radius: 0 8px 8px 0;
    margin: 24px 0 12px 0;
}

.accion-card {
    border-radius: 12px; padding: 18px 20px; margin-bottom: 12px;
    position: relative; overflow: hidden; background: #f8fafc;
}
.accion-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
}

.trimestre-badge {
    display: inline-block; border-radius: 20px; padding: 3px 12px;
    font-size: .72rem; font-weight: 700; letter-spacing: .5px; text-transform: uppercase;
}

.ruta-bloque {
    border-radius: 14px; padding: 22px 24px; margin-bottom: 14px;
    position: relative; background: #f8fafc;
}
.ruta-bloque::after {
    content: ''; position: absolute; left: 50%; bottom: -14px;
    width: 2px; height: 14px; background: #1e3a5f; z-index: 1;
}
.ruta-bloque:last-child::after { display: none; }

.kpi-objetivo {
    background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 10px;
    padding: 12px 16px; text-align: center;
}

.highlight-box {
    border-radius: 0 12px 12px 0; padding: 16px 20px; margin: 16px 0;
    color: #1e293b; line-height: 1.8; font-size: .9rem;
}

.ia-generando {
    background: #f8fafc; border: 1px dashed #94a3b8; border-radius: 10px;
    padding: 20px; text-align: center; color: #475569; font-size: .88rem;
}

.informe-seccion {
    border-left: 3px solid #f59e0b; padding: 0 0 0 18px; margin: 20px 0;
}
.informe-titulo {
    font-family: 'Rajdhani', sans-serif; font-size: 1rem; font-weight: 700;
    color: #f59e0b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;
}
.informe-texto {
    font-family: 'Crimson Pro', serif; font-size: 1.02rem; color: #1e293b; line-height: 1.85;
}
.informe-destacado {
    background: #fffbeb; border-radius: 8px; padding: 12px 16px;
    margin: 12px 0; border-left: 3px solid #f59e0b;
    font-family: 'Crimson Pro', serif; font-size: 1rem; color: #78350f;
    font-style: italic; line-height: 1.7;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# CONSTANTES
# ═══════════════════════════════════════════════════════════
MACROSECTORES = {1:"Industria", 2:"Tec. Avanzada", 3:"Servicios"}
PESOS_ICE = [('Prod_Venta_Emp',.30),('Var_Ventas_5a',.25),('Var_Emp_5a',.15),('Ratio_Endeudamiento',.15),('Exportacion',.15)]
PESOS_ISF = [('Ratio_Endeudamiento',.40),('ROA',.35),('Coste_Med_Emp',.25)]
PESOS_IEO = [('Prod_Venta_Emp',.50),('Coste_Med_Emp',.30),('Var_Ventas_5a',.20)]
PESOS_IDC = [('Var_Ventas_5a',.40),('Var_Emp_5a',.35),('ROA',.25)]
PESOS_IIE = [('Exportacion',.60),('Var_Ventas_5a',.20),('Prod_Venta_Emp',.20)]
PESOS_IPT = [('Prod_Venta_Emp',.40),('Coste_Med_Emp',.30),('Var_Emp_5a',.30)]
INV_ECO   = {'Ratio_Endeudamiento','Coste_Med_Emp'}

INN_NAMES = {'IND_IDi':'I+D+i','IND_GPROY':'Gestión de Proyectos',
             'IND_DESPROD':'Desarrollo de Productos','IND_ESTRINN':'Estrategia de Innovación',
             'IND_DESMPINN':'Desempeño de Innovación'}
GE_LABELS = ['🚀 Líderes','⭐ Sólidas','📊 Intermedias','🔄 En Desarrollo','📉 Rezagadas']
GE_COLORS = ['#10b981','#3b82f6','#f59e0b','#f97316','#ef4444']
hoy = date.today().strftime("%d/%m/%Y")
anio = date.today().year

# ═══════════════════════════════════════════════════════════
# PERFIL
# ═══════════════════════════════════════════════════════════
PERFIL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','perfil_empresa.json')
def cargar_perfil():
    if os.path.exists(PERFIL_FILE):
        with open(PERFIL_FILE,'r',encoding='utf-8') as f: return json.load(f)
    return {}
for k,v in cargar_perfil().items():
    if k not in st.session_state: st.session_state[k] = v

if not st.session_state.get('save_reg_user'):
    st.warning("⚠️ Primero completa tu perfil en Inicio."); st.stop()

mac_cod    = int(st.session_state.get('save_macro_cod',1))
nom_sector = st.session_state.get('save_sector_nombre','—')
nom_tam    = st.session_state.get('save_tam_nombre','—')
nom_reg    = st.session_state.get('save_reg_nombre','—')
nom_mac    = MACROSECTORES.get(mac_cod,'—')
def gv(k,d=0): return st.session_state.get(k,d) or d

# ═══════════════════════════════════════════════════════════
# DATOS
# ═══════════════════════════════════════════════════════════
ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','datos.xlsx')
if not os.path.exists(ruta): ruta = "datos.xlsx"
try:
    df = pd.read_excel(ruta); df.columns = df.columns.str.strip()
except Exception as e:
    st.error(f"Error: {e}"); st.stop()

def calc_df(data, pesos, inv):
    s = pd.Series(0.0, index=data.index)
    for col,w in pesos:
        if col not in data.columns: continue
        s += data[col].rank(ascending=(col not in inv), pct=True)*100*w
    return s

@st.cache_data
def preparar(data):
    d = data.copy()
    d['ICE']=calc_df(d,PESOS_ICE,INV_ECO); d['ISF']=calc_df(d,PESOS_ISF,INV_ECO)
    d['IEO']=calc_df(d,PESOS_IEO,INV_ECO); d['IDC']=calc_df(d,PESOS_IDC,INV_ECO)
    d['IIE']=calc_df(d,PESOS_IIE,INV_ECO); d['IPT']=calc_df(d,PESOS_IPT,INV_ECO)
    d['SSG']=d['ICE']*.25+d['ISF']*.20+d['IEO']*.20+d['IDC']*.15+d['IIE']*.10+d['IPT']*.10
    gs=(d['MACRO_INNOVACION'].rank(pct=True)*.25+d['ROA'].rank(pct=True)*.25+
        d['Var_Ventas_5a'].rank(pct=True)*.20+d['Prod_Venta_Emp'].rank(pct=True)*.20+
        (1-d['Ratio_Endeudamiento'].rank(pct=True))*.10)
    d['GE_score']=gs*100
    d['GE']=4-pd.qcut(gs,q=5,labels=[0,1,2,3,4]).astype(int)
    return d

df = preparar(df)

# ═══════════════════════════════════════════════════════════
# VALORES EMPRESA
# ═══════════════════════════════════════════════════════════
mi_inn = {
    'MACRO_INNOVACION': round((gv('score_b1')+gv('score_b2')+gv('score_b3')+gv('score_b4')+gv('score_b5'))/5,3),
    'IND_IDi':gv('score_b1'),'IND_GPROY':gv('score_b2'),'IND_DESPROD':gv('score_b3'),
    'IND_ESTRINN':gv('score_b4'),'IND_DESMPINN':gv('score_b5'),
}
mi_eco = {
    'ROA':gv('save_roa'),'Var_Ventas_5a':gv('save_var_vtas'),'Var_Emp_5a':gv('save_var_empl'),
    'Prod_Venta_Emp':gv('save_productiv'),'Coste_Med_Emp':gv('save_coste_emp'),
    'Ratio_Endeudamiento':gv('save_endeud'),
}

def idx_emp(pesos,inv):
    s=0.0
    for col,w in pesos:
        if col not in df.columns: continue
        val=mi_eco.get(col,0)
        if val==0: continue
        p=float(np.sum(df[col]>=val)/len(df)*100) if col in inv else float(np.sum(df[col]<=val)/len(df)*100)
        s+=p*w
    return round(s,1)

mi_idx={'ICE':idx_emp(PESOS_ICE,INV_ECO),'ISF':idx_emp(PESOS_ISF,INV_ECO),
        'IEO':idx_emp(PESOS_IEO,INV_ECO),'IDC':idx_emp(PESOS_IDC,INV_ECO),
        'IIE':idx_emp(PESOS_IIE,INV_ECO),'IPT':idx_emp(PESOS_IPT,INV_ECO)}
mi_idx['SSG']=round(mi_idx['ICE']*.25+mi_idx['ISF']*.20+mi_idx['IEO']*.20+
                    mi_idx['IDC']*.15+mi_idx['IIE']*.10+mi_idx['IPT']*.10,1)

ge_score=round((float(np.sum(df['MACRO_INNOVACION']<=mi_inn['MACRO_INNOVACION'])/len(df))*.25+
                float(np.sum(df['ROA']<=mi_eco.get('ROA',0))/len(df))*.25+
                float(np.sum(df['Var_Ventas_5a']<=mi_eco.get('Var_Ventas_5a',0))/len(df))*.20+
                float(np.sum(df['Prod_Venta_Emp']<=mi_eco.get('Prod_Venta_Emp',0))/len(df))*.20+
                float(np.sum(df['Ratio_Endeudamiento']>=mi_eco.get('Ratio_Endeudamiento',1))/len(df))*.10)*100,1)
mi_ge=min(4,max(0,4-int(ge_score/20)))

# Grupo de referencia (mismo macrosector)
b_mac=df[df['Macrosector']==mac_cod] if len(df[df['Macrosector']==mac_cod])>=20 else df.copy()
def top25(base):
    gs=(base['MACRO_INNOVACION'].rank(pct=True)*.25+base['ROA'].rank(pct=True)*.25+
        base['Var_Ventas_5a'].rank(pct=True)*.20+base['Prod_Venta_Emp'].rank(pct=True)*.20+
        (1-base['Ratio_Endeudamiento'].rank(pct=True))*.10)
    return base[gs>=gs.quantile(0.75)]
top_ref=top25(b_mac)

# Percentiles clave
def pct(col,val,inv=False):
    if col not in b_mac.columns: return 50.0
    if inv: return round(float(np.sum(b_mac[col]>=val)/len(b_mac)*100),1)
    return round(float(np.sum(b_mac[col]<=val)/len(b_mac)*100),1)

pcts_inn={k:pct(k,v) for k,v in mi_inn.items() if k!='MACRO_INNOVACION'}
pcts_idx={k:pct(k,v) for k,v in mi_idx.items()}
pcts_eco={k:pct(k,v,k in INV_ECO) for k,v in mi_eco.items()}

# Top/bottom 3 innovación
inn_sorted=sorted(pcts_inn.items(),key=lambda x:x[1])
inn_debiles=inn_sorted[:2]   # los 2 más bajos
inn_fuertes=inn_sorted[-2:]  # los 2 más altos

# Grupo superior
ge_sup=max(0,mi_ge-1)
g_sup_df=df[df['GE']==ge_sup]

# ═══════════════════════════════════════════════════════════
# API KEY
# ═══════════════════════════════════════════════════════════
def cargar_api_key():
    try:
        if 'ANTHROPIC_API_KEY' in st.secrets:
            return st.secrets['ANTHROPIC_API_KEY']
    except Exception:
        pass
    if os.environ.get('ANTHROPIC_API_KEY'):
        return os.environ['ANTHROPIC_API_KEY']
    env_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..', '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith('ANTHROPIC_API_KEY'):
                    return line.split('=',1)[1].strip()
    return None

API_KEY=cargar_api_key()

def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn').upper()

def llamar_ia(prompt, max_tokens=2200):
    if not API_KEY: return None
    try:
        r=requests.post("https://api.anthropic.com/v1/messages",
            headers={"Content-Type":"application/json","x-api-key":API_KEY,"anthropic-version":"2023-06-01"},
            json={"model":"claude-sonnet-4-20250514","max_tokens":max_tokens,
                  "messages":[{"role":"user","content":prompt}]},timeout=60)
        data=r.json()
        return data['content'][0]['text'] if data.get('content') else None
    except: return None

# ═══════════════════════════════════════════════════════════
# CABECERA
# ═══════════════════════════════════════════════════════════
st.markdown(f"""
<div class="page-header">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
    <div>
      <div style="font-size:.66rem;color:#1e40af;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">
        Plan de Acción · Hoja de Ruta Estratégica</div>
      <h1 style="font-family:'Rajdhani',sans-serif;color:#00d4ff;margin:0;font-size:1.9rem;">{nom_sector}</h1>
      <p style="color:#334155;margin:4px 0 0;font-size:.84rem;">
        {nom_tam} · {nom_reg} · {nom_mac} · {hoy}</p>
    </div>
    <div style="display:flex;gap:12px;flex-wrap:wrap;">
      <div style="background:rgba(0,0,0,.4);border:1px solid {GE_COLORS[mi_ge]}50;border-radius:10px;padding:10px 18px;text-align:center;">
        <div style="font-size:.6rem;color:#475569;letter-spacing:1px;">Grupo Estratégico</div>
        <div style="font-family:'Rajdhani',sans-serif;font-size:1.3rem;font-weight:700;color:{GE_COLORS[mi_ge]};">{GE_LABELS[mi_ge]}</div>
        <div style="font-size:.68rem;color:#475569;">Score: {ge_score:.0f}/100</div>
      </div>
      <div style="background:rgba(0,0,0,.4);border:1px solid #00d4ff40;border-radius:10px;padding:10px 18px;text-align:center;">
        <div style="font-size:.6rem;color:#475569;letter-spacing:1px;">Innovación Global</div>
        <div style="font-family:'Rajdhani',sans-serif;font-size:1.3rem;font-weight:700;color:#00d4ff;">{mi_inn['MACRO_INNOVACION']:.2f}/5</div>
        <div style="font-size:.68rem;color:#475569;">P{pct('MACRO_INNOVACION',mi_inn['MACRO_INNOVACION']):.0f} sector</div>
      </div>
      <div style="background:rgba(0,0,0,.4);border:1px solid #a78bfa40;border-radius:10px;padding:10px 18px;text-align:center;">
        <div style="font-size:.6rem;color:#475569;letter-spacing:1px;">Score Competitivo</div>
        <div style="font-family:'Rajdhani',sans-serif;font-size:1.3rem;font-weight:700;color:#a78bfa;">{mi_idx['SSG']:.0f}/100</div>
        <div style="font-size:.68rem;color:#475569;">P{pcts_idx.get('SSG',50):.0f} sector</div>
      </div>
    </div>
  </div>
</div>
""",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# BOTÓN GENERAR
# ═══════════════════════════════════════════════════════════
st.markdown("<br>",unsafe_allow_html=True)

if 'plan_generado' not in st.session_state: st.session_state['plan_generado']=False
if 'plan_texto'    not in st.session_state: st.session_state['plan_texto']={}
mostrar_felix(pagina='plan')
col_btn,col_info=st.columns([1,2])
with col_btn:
    generar=st.button("🚀 Generar Plan Completo con IA",type="primary",use_container_width=True)
with col_info:
    st.markdown("""<div style="background:#f8fafc;border-left:3px solid #00d4ff;border-radius:0 8px 8px 0;
        padding:10px 16px;color:#334155;font-size:.84rem;line-height:1.6;">
        Genera un <strong style="color:#e2e8f0;">Plan de Acción anual</strong> con acciones trimestrales priorizadas
        + una <strong style="color:#f59e0b;">Hoja de Ruta 1–3 años</strong> completamente personalizada
        basada en tu posición real en el sector.
    </div>""",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# CONSTRUCCIÓN DEL CONTEXTO
# ═══════════════════════════════════════════════════════════
inn_debil_txt=", ".join([f"{INN_NAMES.get(k,k)} (P{p:.0f})" for k,p in inn_debiles])
inn_fuerte_txt=", ".join([f"{INN_NAMES.get(k,k)} (P{p:.0f})" for k,p in inn_fuertes])
ge_sup_inn=round(g_sup_df['MACRO_INNOVACION'].mean(),2) if len(g_sup_df)>0 else 0
ge_sup_roa=round(g_sup_df['ROA'].mean(),1) if len(g_sup_df)>0 else 0
ge_sup_crec=round(g_sup_df['Var_Ventas_5a'].mean(),1) if len(g_sup_df)>0 else 0

contexto=f"""
EMPRESA: {nom_sector} | {nom_tam} | {nom_reg} | Macrosector: {nom_mac}
GRUPO ESTRATÉGICO ACTUAL: {GE_LABELS[mi_ge]} (Score: {ge_score:.0f}/100)
GRUPO OBJETIVO (superior): {GE_LABELS[ge_sup]}

POSICIÓN INNOVACIÓN:
- Índice global: {mi_inn['MACRO_INNOVACION']:.2f}/5 (P{pct('MACRO_INNOVACION',mi_inn['MACRO_INNOVACION']):.0f} del sector)
- Puntos débiles: {inn_debil_txt}
- Puntos fuertes: {inn_fuerte_txt}

POSICIÓN COMPETITIVA (percentil en sector {nom_mac}):
- Score Global (SSG): {mi_idx['SSG']:.0f}/100 (P{pcts_idx.get('SSG',50):.0f})
- Competitividad (ICE): {mi_idx['ICE']:.0f}/100 (P{pcts_idx.get('ICE',50):.0f})
- Solidez Financiera (ISF): {mi_idx['ISF']:.0f}/100 (P{pcts_idx.get('ISF',50):.0f})
- Eficiencia Operativa (IEO): {mi_idx['IEO']:.0f}/100 (P{pcts_idx.get('IEO',50):.0f})
- Dinamismo (IDC): {mi_idx['IDC']:.0f}/100 (P{pcts_idx.get('IDC',50):.0f})

VARIABLES ECONÓMICAS:
- ROA: {mi_eco.get('ROA',0):.1f}% (P{pcts_eco.get('ROA',50):.0f} sector)
- Crecimiento ventas 5a: {mi_eco.get('Var_Ventas_5a',0):.1f}% (P{pcts_eco.get('Var_Ventas_5a',50):.0f})
- Productividad: {mi_eco.get('Prod_Venta_Emp',0):,.0f}€/emp (P{pcts_eco.get('Prod_Venta_Emp',50):.0f})
- Endeudamiento: {mi_eco.get('Ratio_Endeudamiento',0):.2f} (P{pcts_eco.get('Ratio_Endeudamiento',50):.0f} — invertido, menor=mejor)

GRUPO SUPERIOR ({GE_LABELS[ge_sup]}) — valores medios objetivo:
- Innovación media: {ge_sup_inn:.2f}/5
- ROA medio: {ge_sup_roa:.1f}%
- Crecimiento ventas medio: {ge_sup_crec:.1f}%
"""

# ═══════════════════════════════════════════════════════════
# GENERACIÓN IA
# ═══════════════════════════════════════════════════════════
if generar:
    st.session_state['plan_generado']=False
    st.session_state['plan_texto']={}

    with st.spinner("Analizando datos y generando plan personalizado..."):

        # PROMPT PLAN DE ACCIÓN
        prompt_plan=f"""Eres un consultor estratégico senior especializado en innovación y competitividad empresarial.
Basándote EXCLUSIVAMENTE en los datos reales de esta empresa, genera un Plan de Acción para los próximos 12 meses.

{contexto}

INSTRUCCIONES ESTRICTAS:
- Usa SOLO los datos proporcionados. Cada acción debe estar directamente vinculada a una brecha o fortaleza concreta de los datos.
- NUNCA uses abreviaciones de percentil como 'P13', 'P25', 'P50'. Escribe siempre 'percentil 13', 'percentil 25' o mejor aún describe en lenguaje natural: 'por debajo de la media del sector', 'en el cuartil inferior', 'entre los mejores del sector'.
- NO uses lenguaje genérico. Menciona percentiles, valores y métricas reales del contexto.
- Tono: consultor senior, directo, profesional. Sin alarmar. Sin eufemismos vacíos.
- PROHIBIDO: "excelente", "fantástico", "urgente", "alarmante", "catastrófico". Usar: "margen de mejora relevante", "palanca prioritaria", "oportunidad de desarrollo".
- Estructura EXACTA con estos marcadores:

## ACCION_1
Título: [título concreto y específico]
Trimestre: [Q1/Q2/Q3/Q4 {anio}]
Área: [Innovación / Competitividad / Financiero / Operativo]
Descripción: [2-3 frases muy concretas. Qué hacer exactamente, por qué ahora, qué métrica mejora]
Impacto esperado: [métrica concreta y cuantificada si es posible]
Recursos necesarios: [breve]

## ACCION_2
[mismo formato]

## ACCION_3
[mismo formato]

## ACCION_4
[mismo formato]

## ACCION_5
[mismo formato]

Genera exactamente 5 acciones ordenadas por impacto estratégico. La primera acción debe atacar la brecha más crítica identificada en los datos."""

        plan_raw=llamar_ia(prompt_plan, max_tokens=2000)

        # PROMPT HOJA DE RUTA
        prompt_ruta=f"""Eres un consultor estratégico senior. Basándote en los datos reales de esta empresa y en su Plan de Acción anual ya definido, genera una Hoja de Ruta Estratégica para los próximos 1 a 3 años.

{contexto}

INSTRUCCIONES:
- Narrativa ejecutiva de alto nivel, lista para presentar al Consejo de Administración.
- Muy personalizada: cita métricas reales y grupo estratégico actual y objetivo.
- NUNCA uses abreviaciones como 'P13', 'P50', 'P75'. Si mencionas percentiles, escríbelos como 'percentil 13' o mejor usa lenguaje descriptivo: 'por encima de la media', 'en el tercio superior del sector', 'en posición de rezago relativo'.
- Tono: estratégico, ambicioso pero realista, fundamentado en datos.
- PROHIBIDO lenguaje genérico o alarmista.
- Estructura EXACTA:

## DIAGNOSTICO_EJECUTIVO
[Párrafo de 4-5 frases: posición actual, fortalezas reales, brechas críticas, potencial de mejora. Cita datos concretos.]

## VISION_OBJETIVO
[2-3 frases: dónde debe estar la empresa en 3 años. Grupo estratégico objetivo, métricas de innovación y competitividad objetivo. Ambicioso pero basado en los datos del grupo superior.]

## HORIZONTE_1
Año 1 — Consolidación y Activación
[Párrafo: qué se consolida en el primer año, métricas diana, hitos clave]

## HORIZONTE_2
Año 2 — Aceleración y Diferenciación
[Párrafo: palancas de crecimiento, áreas de diferenciación, métricas objetivo año 2]

## HORIZONTE_3
Año 3 — Liderazgo y Sostenibilidad
[Párrafo: posición objetivo en el sector, métricas de innovación y competitividad esperadas, consolidación del modelo]

## FACTORES_CRITICOS
[3-4 factores críticos de éxito muy específicos para esta empresa. Cada uno en una línea empezando con —]

## ALERTA_ESTRATEGICA
[1 párrafo: el principal riesgo o condición que podría comprometer la hoja de ruta. Concreto y fundamentado.]"""

        ruta_raw=llamar_ia(prompt_ruta, max_tokens=2000)

        st.session_state['plan_texto']={'plan':plan_raw,'ruta':ruta_raw}
        st.session_state['plan_generado']=True

# ═══════════════════════════════════════════════════════════
# RENDER PLAN DE ACCIÓN
# ═══════════════════════════════════════════════════════════
LAYOUT=dict(paper_bgcolor='#ffffff',plot_bgcolor='#f8fafc',
            font=dict(color='#1e293b',size=12),margin=dict(t=30,b=20,l=10,r=10))

if st.session_state.get('plan_generado') and st.session_state['plan_texto'].get('plan'):
    plan_raw=st.session_state['plan_texto']['plan']
    ruta_raw=st.session_state['plan_texto'].get('ruta','')

    # ── Gráfico resumen posición actual ───────────────────
    st.markdown('<div class="section-title">📍 Diagnóstico de Partida</div>',unsafe_allow_html=True)

    d1,d2=st.columns(2)
    with d1:
        cats=['I+D+i','Gest.Proy','Dllo.Prod','Estr.Inn','Desemp.Inn']
        mi_v=[mi_inn.get(k,0) for k in ['IND_IDi','IND_GPROY','IND_DESPROD','IND_ESTRINN','IND_DESMPINN']]
        top_v=[round(top_ref[k].mean(),2) if k in top_ref.columns else 0
               for k in ['IND_IDi','IND_GPROY','IND_DESPROD','IND_ESTRINN','IND_DESMPINN']]
        fig_r=go.Figure()
        for vals,name,color,dash,op in [(mi_v,"Mi Empresa",'#00d4ff','solid',.18),(top_v,"Top 25%",'#ffffff','dash',.05)]:
            vc=vals+[vals[0]]; lc=cats+[cats[0]]
            r2,g2,b2=int(color[1:3],16),int(color[3:5],16),int(color[5:7],16)
            fig_r.add_trace(go.Scatterpolar(r=vc,theta=lc,fill='toself',name=name,
                line=dict(color=color,width=2,dash=dash),fillcolor=f'rgba({r2},{g2},{b2},{op})'))
        fig_r.update_layout(
            polar=dict(bgcolor='#f8fafc',
                radialaxis=dict(range=[0,5],gridcolor='#e2e8f0',tickfont=dict(color='#1e293b',size=8)),
                angularaxis=dict(gridcolor='#e2e8f0',tickfont=dict(color='#1e293b',size=10))),
            paper_bgcolor='#ffffff',font=dict(color='#e2e8f0'),height=300,
            margin=dict(t=10,b=10),legend=dict(bgcolor='rgba(0,0,0,0)',font=dict(color='#1e293b',size=10)))
        st.plotly_chart(fig_r,use_container_width=True)
        st.caption("Innovación: Mi empresa vs Top 25% del sector")

    with d2:
        idx_cats=['SSG','ICE','ISF','IEO','IDC','IIE','IPT']
        idx_noms=['Score\nGlobal','Competit.','Solidez\nFin.','Efic.\nOper.','Dinamismo','Int.\nExport.','Prod.\nTalento']
        mi_xv=[mi_idx.get(c,0) for c in idx_cats]
        colores_bar=['#10b981' if v>=66 else '#f59e0b' if v>=33 else '#ef4444' for v in mi_xv]
        fig_b=go.Figure(go.Bar(x=idx_noms,y=mi_xv,marker_color=colores_bar,
            text=[f"{v:.0f}" for v in mi_xv],textposition='outside',
            textfont=dict(color='#1e293b',size=11)))
        fig_b.add_hline(y=50,line_dash='dash',line_color='#64748b',
                        annotation_text="Media sector",annotation_font=dict(color='#64748b',size=10))
        fig_b.update_layout(**LAYOUT,height=300,
            yaxis=dict(range=[0,110],gridcolor='#e2e8f0',tickfont=dict(color='#1e293b')),
            xaxis=dict(gridcolor='#e2e8f0',tickfont=dict(color='#1e293b',size=10)),showlegend=False)
        st.plotly_chart(fig_b,use_container_width=True)
        st.caption("Índices competitivos (percentil 0-100 en el sector)")

    # ── Parse y render acciones ────────────────────────────
    st.markdown('<div class="section-title">📋 Plan de Acción · 12 Meses</div>',unsafe_allow_html=True)

    AREAS_COLOR={'Innovación':'#3b82f6','Competitividad':'#10b981',
                 'Financiero':'#f59e0b','Operativo':'#a78bfa','Estratégico':'#00d4ff'}
    TRIM_COLOR={'Q1':'#3b82f6','Q2':'#10b981','Q3':'#f59e0b','Q4':'#ef4444'}

    def parse_acciones(texto):
        acciones=[]
        bloques=texto.split('## ACCION_')[1:]
        for b in bloques:
            a={}
            lines=b.strip().split('\n')
            a['num']=lines[0].strip()
            for line in lines[1:]:
                for campo in ['Título','Titulo','Trimestre','Área','Area','Descripción','Descripcion','Impacto esperado','Recursos necesarios']:
                    if line.strip().startswith(campo+':'):
                        key=campo.replace('í','i').replace('é','e').replace('ó','o').replace('á','a').lower().replace(' ','_')
                        a[key]=line.split(':',1)[1].strip()
            acciones.append(a)
        return acciones

    acciones=parse_acciones(plan_raw)

    for i,ac in enumerate(acciones):
        titulo=ac.get('titulo',ac.get('t_tulo',f'Acción {i+1}'))
        trim=ac.get('trimestre','Q1')
        area=ac.get('_rea',ac.get('area','Estratégico'))
        desc=ac.get('descripci_n',ac.get('descripcion',''))
        impacto=ac.get('impacto_esperado','')
        recursos=ac.get('recursos_necesarios','')

        # Extraer Q1/Q2/Q3/Q4
        trim_key='Q1'
        for q in ['Q1','Q2','Q3','Q4']:
            if q in trim: trim_key=q; break

        area_color=AREAS_COLOR.get(area,'#a78bfa')
        trim_color=TRIM_COLOR.get(trim_key,'#64748b')
        n_icon=['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣'][min(i,4)]

        st.markdown(f"""<div class="accion-card" style="background:linear-gradient(135deg,{area_color}08,{area_color}03);
            border:1px solid {area_color}35;border-left:4px solid {area_color};">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;margin-bottom:10px;">
            <div style="display:flex;align-items:center;gap:10px;">
              <span style="font-size:1.2rem;">{n_icon}</span>
              <span style="font-family:'Rajdhani',sans-serif;font-size:1.05rem;font-weight:700;color:#e2e8f0;">{titulo}</span>
            </div>
            <div style="display:flex;gap:6px;flex-wrap:wrap;">
              <span class="trimestre-badge" style="background:{trim_color}20;color:{trim_color};border:1px solid {trim_color}50;">{trim}</span>
              <span class="trimestre-badge" style="background:{area_color}18;color:{area_color};border:1px solid {area_color}40;">{area}</span>
            </div>
          </div>
          <p style="color:#1e293b;font-size:.88rem;line-height:1.75;margin:0 0 10px 0;">{desc}</p>
          <div style="display:flex;gap:16px;flex-wrap:wrap;">
            <div style="flex:1;min-width:200px;">
              <span style="font-size:.72rem;color:#475569;text-transform:uppercase;letter-spacing:.5px;">Impacto esperado</span>
              <p style="color:{area_color};font-size:.85rem;margin:3px 0 0 0;font-weight:600;">{impacto}</p>
            </div>
            <div style="flex:1;min-width:200px;">
              <span style="font-size:.72rem;color:#475569;text-transform:uppercase;letter-spacing:.5px;">Recursos</span>
              <p style="color:#334155;font-size:.85rem;margin:3px 0 0 0;">{recursos}</p>
            </div>
          </div>
        </div>""",unsafe_allow_html=True)

    # Timeline visual
    st.markdown('<div class="section-title">🗓️ Calendario de Ejecución</div>',unsafe_allow_html=True)
    trimestres=['Q1','Q2','Q3','Q4']
    t_cols=st.columns(4)
    for ti,tcol in enumerate(t_cols):
        trim_label=trimestres[ti]
        acciones_t=[ac.get('titulo',ac.get('t_tulo',f'Acción')) for ac in acciones
                    if trim_label in ac.get('trimestre','')]
        tc=TRIM_COLOR[trim_label]
        items_html="".join([f'<div style="background:#ffffff;border-radius:6px;padding:7px 10px;margin-bottom:6px;font-size:.82rem;color:#1e293b;font-weight:500;border-left:3px solid {tc};">• {a}</div>' for a in acciones_t]) or '<div style="color:#64748b;font-size:.82rem;font-style:italic;padding:4px 0;">Sin acciones asignadas</div>'
        tcol.markdown(f"""<div style="background:#f8fafc;border:1px solid {tc}50;border-top:4px solid {tc};border-radius:0 0 10px 10px;padding:14px 12px;min-height:130px;">
          <div style="font-family:'Rajdhani',sans-serif;font-size:1.05rem;font-weight:700;color:{tc};margin-bottom:10px;padding-bottom:6px;border-bottom:1px solid {tc}25;">
            {trim_label} · <span style="color:#374151;">{anio}</span></div>
          {items_html}
        </div>""",unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════
    # HOJA DE RUTA ESTRATÉGICA
    # ═══════════════════════════════════════════════════════
    st.markdown("<br><br>",unsafe_allow_html=True)
    st.markdown(f"""<div style="background:linear-gradient(135deg,#fffbeb,#fef3c7);border:2px solid #f59e0b;
        border-radius:14px;padding:22px 28px;margin-bottom:4px;">
      <div style="font-size:.66rem;color:#92400e;letter-spacing:2px;text-transform:uppercase;font-weight:700;margin-bottom:4px;">
        Documento Estratégico Confidencial</div>
      <h2 style="font-family:'Rajdhani',sans-serif;color:#92400e;margin:0;font-size:1.8rem;">
        Hoja de Ruta Estratégica {anio}–{anio+2}</h2>
      <p style="color:#78350f;margin:4px 0 0;font-size:.84rem;font-weight:600;">{nom_sector} · {nom_mac} · {nom_tam}</p>
    </div>""",unsafe_allow_html=True)

    if ruta_raw:
        # Parser secciones hoja de ruta
        def get_seccion(texto, marcador):
            n=norm(texto); m=norm(marcador)
            idx=n.find(m)
            if idx==-1: return ''
            start=texto.find('\n',idx)+1
            # Buscar siguiente sección ##
            rest=texto[start:]
            next_sec=rest.find('\n## ')
            return rest[:next_sec].strip() if next_sec!=-1 else rest.strip()

        diagnostico  = get_seccion(ruta_raw,'## DIAGNOSTICO_EJECUTIVO')
        vision       = get_seccion(ruta_raw,'## VISION_OBJETIVO')
        h1           = get_seccion(ruta_raw,'## HORIZONTE_1')
        h2           = get_seccion(ruta_raw,'## HORIZONTE_2')
        h3           = get_seccion(ruta_raw,'## HORIZONTE_3')
        factores     = get_seccion(ruta_raw,'## FACTORES_CRITICOS')
        alerta       = get_seccion(ruta_raw,'## ALERTA_ESTRATEGICA')

        # Diagnóstico ejecutivo
        st.markdown('<div class="section-title-gold">🔎 Diagnóstico Ejecutivo</div>',unsafe_allow_html=True)
        if diagnostico:
            st.markdown(f'<div class="highlight-box" style="background:#fffbeb;border-left:4px solid #f59e0b;"><span class="informe-texto">{diagnostico}</span></div>',unsafe_allow_html=True)

        # Visión objetivo
        if vision:
            st.markdown(f'<div class="informe-destacado">🎯 {vision}</div>',unsafe_allow_html=True)

        # Gráfico brecha actual → objetivo
        st.markdown('<div class="section-title-gold">📈 Brecha Actual vs. Objetivo Estratégico</div>',unsafe_allow_html=True)

        ge_sup_score=round(g_sup_df['GE_score'].mean(),1) if len(g_sup_df)>0 else min(ge_score+20,100)
        categorias=['Innovación','ROA','Crec.Ventas','Productividad','Score Global']
        vals_actual=[
            round(float(np.sum(df['MACRO_INNOVACION']<=mi_inn['MACRO_INNOVACION'])/len(df)*100),1),
            round(float(np.sum(df['ROA']<=mi_eco.get('ROA',0))/len(df)*100),1),
            round(float(np.sum(df['Var_Ventas_5a']<=mi_eco.get('Var_Ventas_5a',0))/len(df)*100),1),
            round(float(np.sum(df['Prod_Venta_Emp']<=mi_eco.get('Prod_Venta_Emp',0))/len(df)*100),1),
            ge_score,
        ]
        vals_objetivo=[min(v+15,100) for v in vals_actual]  # objetivo conservador +15 percentiles
        if len(g_sup_df)>0:
            vals_objetivo=[
                round(float(np.sum(df['MACRO_INNOVACION']<=ge_sup_inn)/len(df)*100),1),
                round(float(np.sum(df['ROA']<=ge_sup_roa)/len(df)*100),1),
                round(float(np.sum(df['Var_Ventas_5a']<=ge_sup_crec)/len(df)*100),1),
                round(float(np.sum(df['Prod_Venta_Emp']<=g_sup_df['Prod_Venta_Emp'].mean())/len(df)*100),1),
                ge_sup_score,
            ]

        fig_brecha=go.Figure()
        fig_brecha.add_trace(go.Bar(name='Posición Actual',x=categorias,y=vals_actual,
            marker_color='#3b82f6',opacity=0.85,
            text=[f"P{v:.0f}" for v in vals_actual],textposition='outside',
            textfont=dict(color='#1e293b',size=11)))
        fig_brecha.add_trace(go.Bar(name=f'Objetivo {anio+2} ({GE_LABELS[ge_sup]})',x=categorias,y=vals_objetivo,
            marker_color='#f59e0b',opacity=0.5,
            text=[f"P{v:.0f}" for v in vals_objetivo],textposition='outside',
            textfont=dict(color='#f59e0b',size=11)))
        fig_brecha.update_layout(**LAYOUT,barmode='group',height=320,
            yaxis=dict(range=[0,115],gridcolor='#e2e8f0',title='Percentil en el sector',
                       tickfont=dict(color='#1e293b'),title_font=dict(color='#1e293b')),
            xaxis=dict(gridcolor='#e2e8f0',tickfont=dict(color='#1e293b')),
            legend=dict(bgcolor='rgba(0,0,0,0)',font=dict(color='#1e293b',size=11)))
        st.plotly_chart(fig_brecha,use_container_width=True)

        # Horizontes temporales
        st.markdown('<div class="section-title-gold">🗺️ Horizontes Estratégicos</div>',unsafe_allow_html=True)

        for idx_h,(label,año,texto,color,icono) in enumerate([
            (f"Año 1 — Consolidación y Activación",    anio,   h1,'#3b82f6','🔵'),
            (f"Año 2 — Aceleración y Diferenciación",  anio+1, h2,'#f59e0b','🟡'),
            (f"Año 3 — Liderazgo y Sostenibilidad",    anio+2, h3,'#10b981','🟢'),
        ]):
            if texto:
                # Limpiar encabezado del bloque si lo incluye la IA
                texto_limpio=texto.split('\n',1)[-1].strip() if texto.startswith('Año') else texto
                st.markdown(f"""<div class="ruta-bloque" style="background:linear-gradient(135deg,{color}08,{color}03);
                    border:1px solid {color}35;border-left:4px solid {color};">
                  <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
                    <span style="font-size:1.1rem;">{icono}</span>
                    <div>
                      <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:700;color:{color};">{label}</div>
                      <div style="font-size:.72rem;color:#475569;">{año}</div>
                    </div>
                  </div>
                  <p style="font-family:'Crimson Pro',serif;font-size:.98rem;color:#1e293b;line-height:1.8;margin:0;">{texto_limpio}</p>
                </div>""",unsafe_allow_html=True)

        # Factores críticos
        if factores:
            st.markdown('<div class="section-title-gold">⚡ Factores Críticos de Éxito</div>',unsafe_allow_html=True)
            items_f=[l.strip().lstrip('—-•').strip() for l in factores.split('\n') if l.strip() and len(l.strip())>5]
            f_cols=st.columns(min(2,len(items_f)))
            for i,item in enumerate(items_f[:4]):
                f_cols[i%2].markdown(f"""<div class="brecha-card" style="background:#f1f5f9;border-left:3px solid #f59e0b;border:1px solid #f59e0b25;border-left:3px solid #f59e0b;">
                    <span style="color:#f59e0b;font-weight:700;">⚡</span>
                    <span style="color:#1e293b;font-size:.88rem;"> {item}</span>
                </div>""",unsafe_allow_html=True)

        # Alerta estratégica
        if alerta:
            st.markdown(f"""<div class="highlight-box" style="background:#fef2f2;border-left:4px solid #ef4444;margin-top:20px;">
              <div style="font-size:.72rem;color:#b91c1c;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;">⚠️ Alerta Estratégica</div>
              <span class="informe-texto" style="color:#991b1b;">{alerta}</span>
            </div>""",unsafe_allow_html=True)

    # ── Descarga ───────────────────────────────────────────
    st.markdown("<br>",unsafe_allow_html=True)
    st.divider()

    def generar_html_completo():
        acc_html=""
        for i,ac in enumerate(acciones):
            titulo=ac.get('titulo',ac.get('t_tulo',f'Acción {i+1}'))
            trim=ac.get('trimestre',''); area=ac.get('_rea',ac.get('area',''))
            desc=ac.get('descripci_n',ac.get('descripcion',''))
            impacto=ac.get('impacto_esperado',''); recursos=ac.get('recursos_necesarios','')
            area_color=AREAS_COLOR.get(area,'#7c3aed')
            acc_html+=f"""<div style='border-left:4px solid {area_color};padding:12px 16px;margin:12px 0;background:#f8f9fa;border-radius:0 8px 8px 0;'>
                <div style='display:flex;justify-content:space-between;'><strong>{i+1}. {titulo}</strong>
                <span style='background:{area_color};color:white;border-radius:12px;padding:2px 10px;font-size:.8rem;'>{trim} · {area}</span></div>
                <p style='margin:8px 0 4px;'>{desc}</p>
                <p style='margin:4px 0;color:#6b7280;font-size:.88rem;'><strong>Impacto:</strong> {impacto}</p>
                <p style='margin:4px 0;color:#6b7280;font-size:.88rem;'><strong>Recursos:</strong> {recursos}</p>
            </div>"""

        return f"""<!DOCTYPE html><html><head><meta charset='utf-8'>
<style>
body{{font-family:Georgia,serif;max-width:900px;margin:50px auto;color:#1a1a1a;line-height:1.75;}}
h1{{color:#00d4ff;border-bottom:3px solid #00d4ff;padding-bottom:8px;font-size:1.8rem;}}
h2{{color:#f59e0b;border-left:4px solid #f59e0b;padding-left:12px;margin-top:32px;}}
h3{{color:#3b82f6;margin-top:24px;}}
.meta{{color:#6b7280;font-size:.88rem;margin-bottom:32px;}}
.vision{{background:#fffbeb;border-left:4px solid #f59e0b;padding:14px 18px;border-radius:0 8px 8px 0;font-style:italic;margin:16px 0;}}
.horizonte{{border-radius:8px;padding:16px 20px;margin:14px 0;}}
.factor{{border-left:3px solid #f59e0b;padding:8px 14px;margin:8px 0;background:#fffbeb;}}
.alerta{{background:#fef2f2;border-left:4px solid #ef4444;padding:14px 18px;border-radius:0 8px 8px 0;margin:16px 0;}}
</style></head><body>
<h1>Plan de Acción & Hoja de Ruta Estratégica</h1>
<div class="meta">{nom_sector} · {nom_tam} · {nom_reg} · {nom_mac} · {hoy}<br>
Grupo Estratégico: {GE_LABELS[mi_ge]} (Score: {ge_score:.0f}/100) · Innovación: {mi_inn['MACRO_INNOVACION']:.2f}/5</div>
<h2>Plan de Acción · {anio}</h2>
{acc_html}
<h2>Hoja de Ruta Estratégica {anio}–{anio+2}</h2>
{'<h3>Diagnóstico Ejecutivo</h3><p>'+diagnostico+'</p>' if diagnostico else ''}
{'<div class="vision">🎯 '+vision+'</div>' if vision else ''}
{'<h3>'+f'Año 1 ({anio}) — Consolidación'+'</h3><div class="horizonte" style="background:#eff6ff;border-left:4px solid #3b82f6;">'+h1+'</div>' if h1 else ''}
{'<h3>'+f'Año 2 ({anio+1}) — Aceleración'+'</h3><div class="horizonte" style="background:#fffbeb;border-left:4px solid #f59e0b;">'+h2+'</div>' if h2 else ''}
{'<h3>'+f'Año 3 ({anio+2}) — Liderazgo'+'</h3><div class="horizonte" style="background:#f0fdf4;border-left:4px solid #10b981;">'+h3+'</div>' if h3 else ''}
{'<h3>Factores Críticos de Éxito</h3>'+"".join([f'<div class="factor">{f}</div>' for f in [l.strip().lstrip("—-•").strip() for l in factores.split(chr(10)) if l.strip() and len(l.strip())>5][:4]]) if factores else ''}
{'<h3>Alerta Estratégica</h3><div class="alerta">'+alerta+'</div>' if alerta else ''}
<hr/><p style='color:#9ca3af;font-size:.78rem;text-align:center;'>Plataforma de Diagnóstico Estratégico · {hoy}</p>
</body></html>"""

    c1,c2=st.columns(2)
    with c1:
        st.download_button("📥 Descargar Plan Completo HTML",
            data=generar_html_completo(),
            file_name=f"plan_accion_{nom_sector[:15].replace(' ','_')}_{anio}.html",
            mime="text/html",type="primary",use_container_width=True)
    with c2:
        st.info("Abre el HTML en el navegador → **Ctrl+P** → **Guardar como PDF**")

else:
    # Estado inicial — sin generar
    st.markdown("""
    <div style="margin-top:24px;">
    """,unsafe_allow_html=True)

    st.markdown('<div class="section-title">📋 Plan de Acción · 12 Meses</div>',unsafe_allow_html=True)
    st.markdown("""<div class="ia-generando">
        <div style="font-size:2rem;margin-bottom:8px;">📋</div>
        <div style="color:#1e293b;font-size:.95rem;margin-bottom:4px;">Plan de Acción personalizado</div>
        <div style="color:#475569;font-size:.84rem;">5 acciones priorizadas con calendario trimestral,
        áreas de impacto y recursos necesarios</div>
    </div>""",unsafe_allow_html=True)

    st.markdown('<div class="section-title-gold">🗺️ Hoja de Ruta Estratégica · 1–3 años</div>',unsafe_allow_html=True)
    st.markdown("""<div class="ia-generando">
        <div style="font-size:2rem;margin-bottom:8px;">🗺️</div>
        <div style="color:#1e293b;font-size:.95rem;margin-bottom:4px;">Hoja de Ruta Estratégica 1–3 años</div>
        <div style="color:#475569;font-size:.84rem;">Diagnóstico ejecutivo · Visión objetivo · 3 horizontes temporales ·
        Factores críticos · Alerta estratégica</div>
    </div>""",unsafe_allow_html=True)

    st.markdown("</div>",unsafe_allow_html=True)