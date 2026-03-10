import streamlit as st

st.set_page_config(page_title="Gestión de Proyectos", layout="wide")

# --- NAVEGACIÓN ---
col_nav1, col_nav2 = st.columns([4, 1])
with col_nav1:
    st.title("⚙️ Bloque 2: Gestión de Proyectos de Innovación")
with col_nav2:
    if st.button("⬅️ Volver al Inicio"):
        st.switch_page("plataforma.py")

# Función Maestra para escala dinámica
def ficha_gestion(codigo, titulo, explicacion, mapa_opciones, clave):
    st.markdown(f"""
    <div style='background-color: #f0fdf4; padding: 12px; border-radius: 8px; border-left: 5px solid #22c55e; margin-top: 15px;'>
        <strong style='color: #166534;'>{codigo} - {titulo}</strong><br>
        <span style='color: #475569; font-size: 0.85rem;'>{explicacion}</span>
    </div>
    """, unsafe_allow_html=True)
    
    valor = st.select_slider(
        f"Selección {clave}",
        options=[1, 2, 3, 4, 5],
        key=f"g_{clave}",
        label_visibility="collapsed"
    )
    
    texto_seleccionado = mapa_opciones.get(valor, "")
    st.markdown(f"**Nivel {valor}:** *{texto_seleccionado}*")
    return valor

# --- 2.1 GESTIÓN BÁSICA ---
st.header("2.1 Gestión Básica de Proyectos")
c1, c2 = st.columns(2)
with c1:
    d211 = {1: "Nunca", 2: "Puntualmente", 3: "En algún proyecto", 4: "En varios proyectos", 5: "Cooperación activa siempre"}
    ficha_gestion("2.1.1", "Multidisciplinar", "Participación activa de marketing, I+D, producción, etc.", d211, "211")
    
    d212 = {1: "Inexistente", 2: "Escaso, puntual", 3: "En algún proyecto", 4: "En la mayoría de proyectos", 5: "Alineación sistemática siempre"}
    ficha_gestion("2.1.2", "Consenso", "Entendimiento sobre tareas, plazos y recursos", d212, "212")

with c2:
    d213 = {1: "Inexistente", 2: "Escaso", 3: "En algún proyecto", 4: "En la mayoría de proyectos", 5: "Apoyo continuo y sistemático"}
    ficha_gestion("2.1.3", "Apoyo Directivo", "Apoyo y promoción fluida de los directivos", d213, "213")
    
    d214 = {1: "Nunca", 2: "Puntualmente", 3: "En algún proyecto", 4: "En la mayoría de proyectos", 5: "En todos los proyectos"}
    ficha_gestion("2.1.4", "Planificación", "Planificación sistemática con responsables claros", d214, "214")

# --- 2.2 GESTIÓN AVANZADA ---
st.header("2.2 Gestión Avanzada")
c3, c4 = st.columns(2)
with c3:
    d221 = {1: "No se usan", 2: "Puntualmente", 3: "En algún proyecto", 4: "En la mayoría de proyectos", 5: "Uso avanzado y sistemático"}
    ficha_gestion("2.2.1", "Tec. Avanzadas", "Uso de herramientas de diseño y simulación", d221, "221")
    
    d222 = {1: "Nulo", 2: "Sólo registros de marca", 3: "En algunos proyectos", 4: "Gestión proactiva", 5: "Estrategia integral de Prop. Ind."}
    ficha_gestion("2.2.2", "Prop. Industrial", "Protección de patentes, marcas y diseños", d222, "222")

with c4:
    d223 = {1: "No se conocen", 2: "Interés futuro", 3: "Uso puntual", 4: "Uso frecuente", 5: "Metodologías integradas (Agile/Lean)"}
    ficha_gestion("2.2.3", "Gestión Ágil", "Uso de metodologías ágiles en proyectos", d223, "223")

# --- 2.3 ORGANIZACIÓN ---
st.header("2.3 Organización de Proyectos")
c5, c6 = st.columns(2)
with c5:
    d231 = {1: "Inexistente", 2: "Administración puntual", 3: "Procedimiento formalizado", 4: "Seguimiento sistemático", 5: "Monitorización digital continua"}
    ficha_gestion("2.3.1", "Adm. Proyectos", "Estructura y administración de los proyectos", d231, "231")
with c6:
    d232 = {1: "Nunca", 2: "A veces", 3: "Con cierta frecuencia", 4: "Habitualmente", 5: "Siempre con apoyo externo"}
    ficha_gestion("2.3.2", "Competición", "Fomento de competencia entre equipos internos", d232, "232")

# --- 2.4 EVALUACIÓN (EN PARALELO) ---
st.header("2.4 Evaluación del Rendimiento")
c7, c8 = st.columns(2)
with c7:
    d241 = {1: "Inexistente", 2: "Informal, sin métricas", 3: "Evaluación parcial", 4: "Estructurado con KPIs", 5: "Análisis sistemático de desviaciones"}
    ficha_gestion("2.4.1", "Rendimiento", "Evaluación de KPIs y métricas de proyectos", d241, "241")
with c8:
    d242 = {1: "No se usan", 2: "Uso informal y puntual", 3: "Para corregir errores operativos", 4: "Para seleccionar nuevos proyectos", 5: "Guían la estrategia global"}
    ficha_gestion("2.4.2", "Aplicación", "Uso de resultados para futuros proyectos", d242, "242")

st.divider()
if st.button("💾 Guardar Bloque 2"):
    st.success("Gestión de Proyectos registrada correctamente.")