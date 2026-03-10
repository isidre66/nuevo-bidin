import streamlit as st

st.set_page_config(
    page_title="Plataforma de Diagnóstico Estratégico",
    page_icon="🏆",
    layout="wide"
)

# ── Inicializar session_state si es la primera vez ──────────────────────────
# Clasificación
if 'save_id_empresa'   not in st.session_state: st.session_state['save_id_empresa']   = ""
if 'save_sector'       not in st.session_state: st.session_state['save_sector']       = ""
if 'save_macrosector'  not in st.session_state: st.session_state['save_macrosector']  = ""
if 'save_tam_user'     not in st.session_state: st.session_state['save_tam_user']     = ""
if 'save_export'       not in st.session_state: st.session_state['save_export']       = ""
if 'save_anti'         not in st.session_state: st.session_state['save_anti']         = ""
if 'save_reg_user'     not in st.session_state: st.session_state['save_reg_user']     = ""

# Desempeño económico
if 'save_ventas'       not in st.session_state: st.session_state['save_ventas']       = 0
if 'save_empleados'    not in st.session_state: st.session_state['save_empleados']    = 0
if 'save_roa'          not in st.session_state: st.session_state['save_roa']          = 0.0
if 'save_var_vtas'     not in st.session_state: st.session_state['save_var_vtas']     = 0.0
if 'save_var_empl'     not in st.session_state: st.session_state['save_var_empl']     = 0.0
if 'save_productiv'    not in st.session_state: st.session_state['save_productiv']    = 0.0
if 'save_coste_emp'    not in st.session_state: st.session_state['save_coste_emp']    = 0.0
if 'save_endeud'       not in st.session_state: st.session_state['save_endeud']       = 0.0

# Bloque 1 - I+D+i
if 'b1_finalizado'     not in st.session_state: st.session_state['b1_finalizado']     = False
if 'score_sub1_1'      not in st.session_state: st.session_state['score_sub1_1']      = 0.0
if 'score_sub1_2'      not in st.session_state: st.session_state['score_sub1_2']      = 0.0
if 'score_sub1_3'      not in st.session_state: st.session_state['score_sub1_3']      = 0.0
if 'score_b1'          not in st.session_state: st.session_state['score_b1']          = 0.0

# Bloque 2 - Gestión Proyectos
if 'b2_finalizado'     not in st.session_state: st.session_state['b2_finalizado']     = False
if 'score_b2'          not in st.session_state: st.session_state['score_b2']          = 0.0

# Bloque 3 - Desarrollo Productos
if 'b3_finalizado'     not in st.session_state: st.session_state['b3_finalizado']     = False
if 'score_b3'          not in st.session_state: st.session_state['score_b3']          = 0.0

# Bloque 4 - Estrategia
if 'b4_finalizado'     not in st.session_state: st.session_state['b4_finalizado']     = False
if 'score_b4'          not in st.session_state: st.session_state['score_b4']          = 0.0

# Bloque 5 - Desempeño Innovación
if 'b5_finalizado'     not in st.session_state: st.session_state['b5_finalizado']     = False
if 'score_b5'          not in st.session_state: st.session_state['score_b5']          = 0.0

# ── PANTALLA DE INICIO ───────────────────────────────────────────────────────
st.title("🏆 Plataforma de Diagnóstico Estratégico")
st.markdown("### Tu consultor estratégico personalizado")
st.divider()

st.markdown("""
Bienvenido a la **Plataforma de Diagnóstico Estratégico**.

Esta herramienta te permite obtener un diagnóstico completo y personalizado 
de tu empresa en las siguientes áreas:
""")

c1, c2, c3 = st.columns(3)
with c1:
    st.info("### 🚀 Innovación\nDiagnóstico completo de tus capacidades de innovación en 5 bloques.")
with c2:
    st.info("### 🎯 Estrategia\n*(Próximamente)*")
with c3:
    st.info("### 💻 Transformación Digital\n*(Próximamente)*")

st.divider()

# Estado actual de la sesión
st.markdown("### 📋 Estado de tu diagnóstico")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Bloque 1 · I+D+i",        "✅ Completado" if st.session_state['b1_finalizado'] else "⏳ Pendiente")
col2.metric("Bloque 2 · Gestión",       "✅ Completado" if st.session_state['b2_finalizado'] else "⏳ Pendiente")
col3.metric("Bloque 3 · Productos",     "✅ Completado" if st.session_state['b3_finalizado'] else "⏳ Pendiente")
col4.metric("Bloque 4 · Estrategia",    "✅ Completado" if st.session_state['b4_finalizado'] else "⏳ Pendiente")
col5.metric("Bloque 5 · Desempeño",     "✅ Completado" if st.session_state['b5_finalizado'] else "⏳ Pendiente")

st.divider()
st.caption("Para comenzar, ve al **Panel de Control** en el menú de la izquierda.")
