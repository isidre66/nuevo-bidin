import streamlit as st

st.set_page_config(page_title="Desarrollo de Productos", layout="wide")

# --- NAVEGACIÓN ---
col_nav1, col_nav2 = st.columns([4, 1])
with col_nav1:
    st.title("🚀 Bloque 3: Desarrollo de nuevos productos")
with col_nav2:
    if st.button("⬅️ Volver al Inicio"):
        st.switch_page("plataforma.py")

# Función Maestra: Sintética e Intuitiva
def ficha_dinamica(codigo, titulo, explicacion, mapa_opciones, clave):
    st.markdown(f"""
    <div style='background-color: #f0f9ff; padding: 12px; border-radius: 8px; border-left: 5px solid #0ea5e9; margin-top: 15px;'>
        <strong style='color: #0c4a6e;'>{codigo} - {titulo}</strong><br>
        <span style='color: #64748b; font-size: 0.85rem;'>{explicacion}</span>
    </div>
    """, unsafe_allow_html=True)
    
    valor = st.select_slider(
        f"Selección para {clave}",
        options=[1, 2, 3, 4, 5],
        key=f"p_{clave}",
        label_visibility="collapsed"
    )
    
    texto_seleccionado = mapa_opciones.get(valor, "")
    st.markdown(f"**Nivel {valor}:** *{texto_seleccionado}*")
    return valor

# --- CONTENIDO ---

# 3.1 ESTRATEGIA
st.header("3.1 Estrategia y Recursos")
c1, c2 = st.columns(2)
with c1:
    dict_311 = {
        1: "Inexistente o informal", 2: "Puntual e informal", 3: "Sólo ante oportunidades claras de mercado",
        4: "Se analiza demanda potencial y necesidades clientes", 5: "Enfoque multidisciplinar: I+D, marketing, producción"
    }
    ficha_dinamica("3.1.1", "Estrategia", "Estrategia y proceso de desarrollo de productos", dict_311, "311")
with c2:
    dict_312 = {
        1: "No se asignan recursos", 2: "Asignación puntual e informal", 3: "Recursos internos del área I+D y afines",
        4: "Equipos internos integrados y multidisciplinares", 5: "Colaboración sistemática con agentes externos"
    }
    ficha_dinamica("3.1.2", "Recursos", "Gestión de recursos para el desarrollo", dict_312, "312")

# 3.2 OPORTUNIDAD
st.header("3.2 Oportunidad y Mercado")
c3, c4 = st.columns(2)
with c3:
    dict_321 = {
        1: "No, nunca", 2: "Muy rara vez", 3: "Algunas veces", 4: "Bastantes veces", 5: "Con mucha frecuencia, habitualmente"
    }
    ficha_dinamica("3.2.1", "Identificación", "Capacidad de identificar oportunidades desatendidas", dict_321, "321")
with c4:
    dict_322 = {
        1: "Nulo, marginal", 2: "Pequeño", 3: "Mediano", 4: "Grande", 5: "Muy grande"
    }
    ficha_dinamica("3.2.2", "Tamaño", "Tamaño del mercado de las innovaciones", dict_322, "322")

# 3.3 RECEPTIVIDAD
st.header("3.3 Receptividad y Valor")
c5, c6 = st.columns(2)
with c5:
    dict_331 = {
        1: "Nula", 2: "Baja", 3: "Media", 4: "Alta", 5: "Muy alta"
    }
    ficha_dinamica("3.3.1", "Valor", "Valor percibido por los clientes", dict_331, "331")
with c6:
    dict_332 = {
        1: "Nulo", 2: "Bajo", 3: "Moderado", 4: "Alto", 5: "Muy alto"
    }
    ficha_dinamica("3.3.2", "Diferenciación", "Nivel de distinción respecto a la competencia", dict_332, "332")

# 3.4 INTERACCIÓN
st.header("3.4 Interacción con Clientes")
c7, c8 = st.columns(2)
with c7:
    dict_341 = {
        1: "No conocido", 2: "Programado en futuro próximo", 3: "Uso puntual", 4: "Considerable", 5: "Uso total y sistemático"
    }
    ficha_dinamica("3.4.1", "Diseño", "Uso de herramientas como Design Thinking o Prototipado", dict_341, "341")
with c8:
    dict_342 = {
        1: "No, en absoluto", 2: "Puntual y parcial", 3: "En algunos proyectos", 4: "Con frecuencia", 5: "De forma continua y sistemática"
    }
    ficha_dinamica("3.4.2", "Interacción", "Contacto con usuarios durante el desarrollo", dict_342, "342")

# --- 3.5 VIABILIDAD E IMPACTO (AÑADIDO) ---
st.header("3.5 Viabilidad e Impacto")
c9, c10 = st.columns(2)
with c9:
    dict_351 = {
        1: "No, nunca", 2: "Puntualmente", 3: "En algunos proyectos", 4: "Con frecuencia", 5: "De forma continua y sistemática"
    }
    ficha_dinamica("3.5.1", "Eco-financ", "Análisis económico y rentabilidad potencial", dict_351, "351")
with c10:
    dict_352 = {
        1: "No conocido", 2: "Programado en futuro próximo", 3: "Uso puntual", 4: "Considerable", 5: "Uso total y sistemático"
    }
    ficha_dinamica("3.5.2", "Viabilidad Comercial", "Uso de Business Model Canvas o Validation Board", dict_352, "352")

st.divider()
if st.button("💾 Registrar Datos del Bloque 3"):
    st.balloons()
    st.success("¡Datos del Bloque 3 registrados correctamente!")