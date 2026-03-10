import streamlit as st

st.set_page_config(page_title="Estrategia de Innovación", layout="wide")

# --- NAVEGACIÓN ---
col_nav1, col_nav2 = st.columns([4, 1])
with col_nav1:
    st.title("🎯 Bloque 4: Estrategia de Innovación")
with col_nav2:
    if st.button("⬅️ Volver al Inicio"):
        st.switch_page("plataforma.py")

def ficha_estrategia(codigo, titulo, explicacion, mapa_opciones, clave, inversa=False):
    bg_color = "#fff1f2" if inversa else "#fff7ed"
    border_color = "#e11d48" if inversa else "#f97316"
    
    st.markdown(f"""
    <div style='background-color: {bg_color}; padding: 12px; border-radius: 8px; border-left: 5px solid {border_color}; margin-top: 15px;'>
        <strong style='color: #7c2d12;'>{codigo} - {titulo} {'⚠️ (Valoración Inversa)' if inversa else ''}</strong><br>
        <span style='color: #475569; font-size: 0.85rem;'>{explicacion}</span>
    </div>
    """, unsafe_allow_html=True)
    
    valor = st.select_slider(
        f"Selección {clave}", options=[1, 2, 3, 4, 5], key=f"e_{clave}", label_visibility="collapsed"
    )
    
    texto = mapa_opciones.get(valor, "")
    st.markdown(f"**Nivel {valor}:** *{texto}*")
    return valor

# --- 4.1 INNOVACIÓN ESTRATÉGICA ---
st.header("4.1 Innovación Estratégica")
c1, c2 = st.columns(2)
with c1:
    d411 = {1: "Nula alineación", 2: "Relación puntual", 3: "Innovación en la estrategia", 4: "Decisiones con innovación", 5: "Estrategia proactiva sistemática"}
    ficha_estrategia("4.1.1", "Alinear", "Integración de la innovación en la estrategia", d411, "411")
with c2:
    d412 = {1: "No se contempla", 2: "Sólo imitar", 3: "Puntual poco diferenciada", 4: "Innovación continuada", 5: "Sistemática y disruptiva"}
    ficha_estrategia("4.1.2", "Lider", "Posicionamiento ante la innovación", d412, "412")

# --- 4.2 CULTURA (CON ITEMS INVERSOS) ---
st.header("4.2 Cultura de Innovación")
c3, c4 = st.columns(2)
with c3:
    d421 = {1: "Equilibrio Ideal", 2: "Baja prioridad incremental", 3: "Prioridad moderada", 4: "Prioridad alta", 5: "Foco total incremental (Peor)"}
    ficha_estrategia("4.2.1", "Increm", "Priorización de innovaciones incrementales", d421, "421", inversa=True)
with c4:
    d422 = {1: "Aceptación total riesgo", 2: "Riesgo controlado", 3: "Aceptación moderada", 4: "Aversión al riesgo", 5: "Miedo al fracaso (Peor)"}
    ficha_estrategia("4.2.2", "Riesgo", "Tolerancia al riesgo y al fracaso", d422, "422", inversa=True)

# --- 4.3 OBSTÁCULOS (INVERSOS) ---
st.header("4.3 Obstáculos")
c5, c6 = st.columns(2)
with c5:
    d431 = {1: "Sin obstáculos", 2: "Tecnológicos puntuales", 3: "Organizativos", 4: "Falta competencias", 5: "Financieros y falta voluntad (Peor)"}
    ficha_estrategia("4.3.1", "Obst Int", "Incidencia de obstáculos internos", d431, "431", inversa=True)
with c6:
    d432 = {1: "Entorno favorable", 2: "Dificultad partners", 3: "Dificultad finanza externa", 4: "Competencia intensa", 5: "Incertidumbre mercado (Peor)"}
    ficha_estrategia("4.3.2", "Obst Ext", "Incidencia de obstáculos externos", d432, "432", inversa=True)

# --- 4.5 CREATIVIDAD (NORMAL CON NUEVO ITEM 4.5.2) ---
st.header("4.5 Fomento de la Creatividad")
c7, c8 = st.columns(2)
with c7:
    d451 = {1: "Inexistente", 2: "Puntual e informal", 3: "Sesiones periódicas", 4: "Herramientas formalizadas", 5: "Sistema continuo de gestión"}
    ficha_estrategia("4.5.1", "Creativ", "Técnicas para generar ideas", d451, "451")
with c8:
    d452 = {1: "No se evalúan", 2: "Criterios subjetivos", 3: "Criterios técnicos básicos", 4: "Evaluación formalizada", 5: "Sistema experto de filtrado"}
    ficha_estrategia("4.5.2", "Evalideas", "Sistema de evaluación y selección de ideas", d452, "452")

if st.button("💾 Guardar Bloque 4"):
    st.success("Guardado.")