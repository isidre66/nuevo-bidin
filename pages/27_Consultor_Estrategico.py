import streamlit as st
from asistentes import mostrar_kevin
import os
import pandas as pd
import numpy as np

st.set_page_config(page_title="Kevin · Consultor Estratégico", layout="wide")

# Control de acceso
if not st.session_state.get('save_reg_user'):
    st.warning("⚠️ Por favor, complete primero el perfil de su empresa en la sección Mi Empresa.")
    st.stop()

# ── Cargar scores desde Supabase si no están en session_state ─────────────
def cargar_scores_y_indices():
    try:
        from supabase import create_client
        url = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL",""))
        key = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY",""))
        ec  = st.session_state.get('empresa_codigo','')
        if not (url and key and ec):
            return
        sb = create_client(url, key)

        # Cargar respuestas y calcular scores por bloque
        resp = sb.table('respuestas').select('*').eq('empresa_codigo', ec).execute().data or []
        if resp:
            df_r = pd.DataFrame(resp)
            BLOQUES = {
                1: [c for c in df_r.columns if c.startswith('B1_')],
                2: [c for c in df_r.columns if c.startswith('B2_')],
                3: [c for c in df_r.columns if c.startswith('B3_')],
                4: [c for c in df_r.columns if c.startswith('B4_')],
                5: [c for c in df_r.columns if c.startswith('B5_')],
            }
            for b, cols in BLOQUES.items():
                if cols:
                    vals = df_r[cols].apply(pd.to_numeric, errors='coerce')
                    score = float(vals.mean().mean())
                    if score > 0:
                        st.session_state[f'score_b{b}'] = round(score, 2)

        # Cargar datos económicos y calcular índices
        emp_data = sb.table('empresas').select('*').eq('codigo', ec).execute().data or []
        if emp_data:
            e = emp_data[0]
            ventas    = float(e.get('ventas') or 0)
            empleados = int(e.get('empleados') or 1)
            roa       = float(e.get('roa') or 0)
            var_vtas  = float(e.get('var_ventas') or 0)
            var_empl  = float(e.get('var_empleados') or 0)
            productiv = ventas / max(empleados, 1)
            coste_emp = float(e.get('coste_empleado') or 0)
            endeud    = float(e.get('endeudamiento') or 0)

            # Índices simplificados (0-100)
            ice = min(100, max(0, round(
                (min(roa/20,1)*30 + min(var_vtas/100,1)*25 + min(productiv/500000,1)*25 + (1-min(endeud,1))*20), 1)))
            isf = min(100, max(0, round(
                ((1-min(endeud,1))*50 + min(roa/20,1)*50), 1)))
            ieo = min(100, max(0, round(
                (min(productiv/500000,1)*60 + (1-min(endeud,1))*40), 1)))
            idc = min(100, max(0, round(
                (min(var_vtas/100,1)*60 + min(var_empl/50,1)*40), 1)))
            exp_cod = st.session_state.get('save_export_cod', 0)
            iie = min(100, max(0, round(exp_cod / 4 * 100, 1)))
            ipt = min(100, max(0, round(
                (min(productiv/500000,1)*50 + min(roa/20,1)*50), 1)))
            ssg = round(ice*0.25 + isf*0.20 + ieo*0.20 + idc*0.15 + iie*0.10 + ipt*0.10, 1)

            st.session_state.update({
                'ICE': ice, 'ISF': isf, 'IEO': ieo,
                'IDC': idc, 'IIE': iie, 'IPT': ipt,
                'SSG': ssg,
                'save_ventas': ventas,
                'save_empleados': empleados,
                'save_roa': roa,
                'save_var_vtas': var_vtas,
                'save_var_empl': var_empl,
                'save_productiv': productiv,
                'save_coste_emp': coste_emp,
                'save_endeud': endeud,
            })
    except Exception as ex:
        st.warning(f"No se pudieron cargar algunos datos: {ex}")

# Cargar si SSG no está disponible
if not st.session_state.get('SSG'):
    cargar_scores_y_indices()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');
.kevin-header {
    background: linear-gradient(135deg, #1c1008, #2d1a04, #1c1008);
    border: 1px solid #92400e;
    border-radius: 14px;
    padding: 28px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.kevin-header::before {
    content: 'K';
    position: absolute;
    right: 32px;
    top: 50%;
    transform: translateY(-50%);
    font-family: 'Rajdhani', sans-serif;
    font-size: 120px;
    font-weight: 900;
    color: rgba(251,191,36,0.06);
    line-height: 1;
}
.kevin-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(251,191,36,0.1);
    border: 1px solid rgba(251,191,36,0.3);
    border-radius: 100px;
    padding: 4px 12px;
    font-size: .75rem;
    font-weight: 600;
    color: #fbbf24;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.kevin-titulo {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #fbbf24;
    margin-bottom: 8px;
}
.kevin-sub {
    color: rgba(255,255,255,0.65);
    font-size: .9rem;
    line-height: 1.6;
    max-width: 700px;
}
.aviso-conf {
    background: rgba(146,64,14,0.08);
    border: 1px solid rgba(146,64,14,0.25);
    border-radius: 10px;
    padding: 12px 18px;
    font-size: .82rem;
    color: #fbbf24;
    margin-bottom: 20px;
    display: flex;
    align-items: flex-start;
    gap: 10px;
}
</style>
""", unsafe_allow_html=True)

# Datos del perfil
sector = st.session_state.get('save_sector_nombre', '—')
tam    = st.session_state.get('save_tam_nombre', '—')
reg    = st.session_state.get('save_reg_nombre', '—')
ssg    = round(st.session_state.get('SSG', 0), 1)
bloques = sum(1 for i in range(1,6) if st.session_state.get(f'score_b{i}',0) > 0)
macro_inn = round(
    sum(st.session_state.get(f'score_b{i}',0) for i in range(1,6)) / max(bloques,1), 2
) if bloques > 0 else 0

# Cabecera
st.markdown(f"""
<div class="kevin-header">
    <div class="kevin-badge">⚡ Consultor Estratégico Senior · Etelvia</div>
    <div class="kevin-titulo">Kevin</div>
    <div class="kevin-sub">
        Su consultor estratégico personal con acceso completo a todos los datos de su empresa.
        Analiza, opina y recomienda — no solo informa. Incorpore contexto adicional para recibir
        asesoramiento aún más personalizado.
    </div>
    <div style="margin-top:16px;display:flex;gap:24px;flex-wrap:wrap;">
        <div>
            <span style="font-size:.75rem;color:#92400e;letter-spacing:1px;text-transform:uppercase;">Empresa</span><br>
            <span style="font-size:.95rem;color:#fbbf24;font-weight:600;">{sector} · {tam} · {reg}</span>
        </div>
        <div>
            <span style="font-size:.75rem;color:#92400e;letter-spacing:1px;text-transform:uppercase;">Score Global</span><br>
            <span style="font-size:.95rem;color:#fbbf24;font-weight:600;">{ssg}/100</span>
        </div>
        <div>
            <span style="font-size:.75rem;color:#92400e;letter-spacing:1px;text-transform:uppercase;">Innovación</span><br>
            <span style="font-size:.95rem;color:#fbbf24;font-weight:600;">{macro_inn}/5 · {bloques}/5 bloques</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Aviso confidencialidad
st.markdown("""
<div class="aviso-conf">
    🔒 <div><strong>Confidencialidad garantizada.</strong> Toda la información que comparta con Kevin
    existe únicamente en esta conversación y desaparece al cerrarla. No se almacena, no se comparte
    con terceros y la API de Anthropic no utiliza estos datos para entrenar modelos.</div>
</div>
""", unsafe_allow_html=True)

# Capacidades
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""<div style="background:rgba(146,64,14,.06);border:1px solid rgba(146,64,14,.15);border-radius:10px;padding:16px;">
        <div style="font-size:1.2rem;margin-bottom:6px;">🎯</div>
        <div style="font-size:.85rem;font-weight:700;color:#fbbf24;margin-bottom:4px;">Diagnóstico integrado</div>
        <div style="font-size:.78rem;color:#94a3b8;line-height:1.5;">Cruza innovación, índices competitivos y desempeño económico para identificar prioridades reales.</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div style="background:rgba(146,64,14,.06);border:1px solid rgba(146,64,14,.15);border-radius:10px;padding:16px;">
        <div style="font-size:1.2rem;margin-bottom:6px;">💡</div>
        <div style="font-size:.85rem;font-weight:700;color:#fbbf24;margin-bottom:4px;">Opinión y recomendación</div>
        <div style="font-size:.78rem;color:#94a3b8;line-height:1.5;">No solo informa — opina con criterio y propone acciones concretas basadas en sus datos reales.</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div style="background:rgba(146,64,14,.06);border:1px solid rgba(146,64,14,.15);border-radius:10px;padding:16px;">
        <div style="font-size:1.2rem;margin-bottom:6px;">📎</div>
        <div style="font-size:.85rem;font-weight:700;color:#fbbf24;margin-bottom:4px;">Contexto adicional</div>
        <div style="font-size:.78rem;color:#94a3b8;line-height:1.5;">Incorpora información adicional: web, estrategia, competidores, planes futuros.</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Kevin
mostrar_kevin(pagina='general')