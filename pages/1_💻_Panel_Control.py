import streamlit as st

st.set_page_config(page_title="Plataforma de Auditoría", layout="wide")

# --- 1. LATERAL: CLASIFICACIÓN (AUTOMATIZADA) ---
with st.sidebar:
    st.header("Clasificación de la Empresa")
    id_empresa = st.text_input("ID (A)")
    
    relacion_sectores = {
        "Alimentación y bebidas": "Industria",
        "Textil y confección": "Industria",
        "Cuero y calzado": "Industria",
        "Química y plásticos": "Industria",
        "Minerales no metálicos": "Industria",
        "Metalmecánico": "Industria",
        "Maquinaria equipo": "Industria",
        "Otras manufacturas": "Industria",
        "Electrónica, telecomunicaciones": "Tecnologia avanzada",
        "Informática, software. Robótica, IA": "Tecnologia avanzada",
        "Actividades I+D: biotech, farmacia": "Tecnologia avanzada",
        "Comercio": "Servicios",
        "Transporte y logística": "Servicios",
        "Hostelería y turismo": "Servicios",
        "Servicios financieros y seguros": "Servicios",
        "Servicios a empresas": "Servicios",
        "Otros servicios": "Servicios"
    }
    
    sector_sel = st.selectbox("SECTOR (C)", list(relacion_sectores.keys()))
    macrosector_auto = relacion_sectores[sector_sel]
    st.info(f"**MACROSECTOR (B):** {macrosector_auto}")
    
    # ── Tamaño: igual que en el Excel ──
    tamano = st.selectbox("TAMAÑO (D)", ["Pequeña", "Mediana", "Grande"])
    
    export = st.selectbox("EXPORTACIÓN (E)", ["Menos 10 %", "10 - 30 %", "30 - 60 %", "> 60 %"])
    
    anti = st.selectbox("ANTIGÜEDAD (F)", ["Menos 10 años", "10-30 años", "> 30 años"])
    
    # ── Región: sin tildes, igual que en el Excel ──
    reg = st.selectbox("REGIÓN (G)", [
        "Andalucia", "Aragon", "Asturias", "Baleares", "Canarias",
        "Cantabria", "Castilla la Mancha", "Castilla y León", "Cataluña",
        "Com Valenciana", "Extremadura", "Galicia", "Madrid",
        "Murcia", "Navarra", "Pais Vasco"
    ])
    
    st.text_input("CLUSTER (H)")

    # ── Botón Guardar Clasificación ──
    st.divider()
    if st.button("💾 Guardar Clasificación", use_container_width=True):
        st.session_state['save_id_empresa']   = id_empresa
        st.session_state['save_sector']       = sector_sel
        st.session_state['save_macrosector']  = macrosector_auto
        st.session_state['save_tam_user']     = tamano
        st.session_state['save_export']       = export
        st.session_state['save_anti']         = anti
        st.session_state['save_reg_user']     = reg
        st.success("✅ Clasificación guardada correctamente.")


# --- 2. CENTRO: LOS 3 PILARES ---
st.title("Panel de Control de Auditoría")
st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("### 🚀 **INNOVACIÓN**")
    if st.button("Acceder a Innovación", use_container_width=True):
        st.switch_page("pages/1_📊_Actividades_IDi.py")
with c2:
    st.markdown("### 🎯 **ESTRATEGIA**")
    if st.button("Acceder a Estrategia", use_container_width=True):
        st.switch_page("pages/3_Estrategia.py")
with c3:
    st.markdown("### 💻 **TRANSF. DIGITAL**")
    if st.button("Acceder a Digitalización", use_container_width=True):
        st.info("Módulo en desarrollo")

st.divider()

# --- 3. ABAJO: DESEMPEÑO ECONÓMICO (COLUMNAS I-P) ---
st.header("Indicadores de Desempeño Económico")
d1, d2, d3, d4 = st.columns(4)
with d1:
    ventas    = st.number_input("VENTAS (I)", value=0)
    empleados = st.number_input("EMPLEADOS (J)", value=0)
with d2:
    roa       = st.number_input("ROA (K)", value=0.0)
    var_vtas  = st.number_input("VAR. VENTAS 5A (L)", value=0.0)
with d3:
    var_empl  = st.number_input("VAR. EMPL 5A (M)", value=0.0)
    productiv = st.number_input("PRODUCTIVIDAD (N)", value=0.0)
with d4:
    coste_emp = st.number_input("COSTE MEDIO EMP (O)", value=0.0)
    endeud    = st.number_input("RATIO ENDEUD. (P)", value=0.0)

st.divider()
if st.button("💾 Guardar Desempeño Económico", use_container_width=True):
    st.session_state['save_ventas']    = ventas
    st.session_state['save_empleados'] = empleados
    st.session_state['save_roa']       = roa
    st.session_state['save_var_vtas']  = var_vtas
    st.session_state['save_var_empl']  = var_empl
    st.session_state['save_productiv'] = productiv
    st.session_state['save_coste_emp'] = coste_emp
    st.session_state['save_endeud']    = endeud
    st.success("✅ Datos económicos guardados correctamente.")
