import streamlit as st

st.set_page_config(page_title="Plataforma de Auditoría", layout="wide")

# --- 1. LATERAL: CLASIFICACIÓN (AUTOMATIZADA) ---
with st.sidebar:
    st.header("Clasificación de la Empresa")
    id_empresa = st.text_input("ID (A)")
    
    relacion_sectores = {
        "Alimentación y bebidas": "Industria", "Textil y confección": "Industria",
        "Cuero y calzado": "Industria", "Química y plásticos": "Industria",
        "Minerales no metálicos": "Industria", "Metalmecánico": "Industria",
        "Maquinaria equipo": "Industria", "Otras manufacturas": "Industria",
        "Electrónica, telecomunicaciones": "Tecnología Avanzada",
        "Informática, software. Robótica, IA": "Tecnología Avanzada",
        "Actividades I+D: biotech, farmacia": "Tecnología Avanzada",
        "Comercio": "Servicios", "Transporte y logística": "Servicios",
        "Hostelería y turismo": "Servicios", "Servicios financieros y seguros": "Servicios",
        "Servicios a empresas": "Servicios", "Otros servicios": "Servicios"
    }
    
    sector_sel = st.selectbox("SECTOR (C)", list(relacion_sectores.keys()))
    macrosector_auto = relacion_sectores[sector_sel]
    st.info(f"**MACROSECTOR (B):** {macrosector_auto}")
    
    tamano = st.selectbox("TAMAÑO (D)", ["Pequeña", "Mediana", "Grande"])
    export = st.selectbox("EXPORTACIÓN (E)", ["Menos 10%", "10-30%", "30-60%", "> 60%"])
    anti = st.selectbox("ANTIGÜEDAD (F)", ["Menos 10 años", "10-30 años", "> 30 años"])
    reg = st.selectbox("REGIÓN (G)", ["Andalucía", "Aragón", "Asturias", "Baleares", "Canarias", "Cantabria", "Castilla la Mancha", "Castilla y León", "Cataluña", "Com Valenciana", "Extremadura", "Galicia", "Madrid", "Murcia", "Navarra", "País Vasco", "La Rioja"])
    st.text_input("CLUSTER (H)")

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
        st.switch_page("pages/4_🎯_Estrategia_Innovacion.py")
with c3:
    st.markdown("### 💻 **TRANSF. DIGITAL**")
    if st.button("Acceder a Digitalización", use_container_width=True):
        st.info("Módulo en desarrollo")

st.divider()

# --- 3. ABAJO: DESEMPEÑO (COLUMNAS I-P) ---
st.header("Indicadores de Desempeño Económico")
d1, d2, d3, d4 = st.columns(4)
with d1:
    st.number_input("VENTAS (I)", value=0); st.number_input("EMPLEADOS (J)", value=0)
with d2:
    st.number_input("ROA (K)", value=0.0); st.number_input("VAR. VENTAS 5A (L)", value=0.0)
with d3:
    st.number_input("VAR. EMPL 5A (M)", value=0.0); st.number_input("PRODUCTIVIDAD (N)", value=0.0)
with d4:
    st.number_input("COSTE MEDIO EMP (O)", value=0.0); st.number_input("RATIO ENDEUD. (P)", value=0.0)