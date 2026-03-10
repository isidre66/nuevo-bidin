import streamlit as st

st.set_page_config(page_title="Desempeño e Impacto", layout="wide")

# --- NAVEGACIÓN ---
col_nav1, col_nav2 = st.columns([4, 1])
with col_nav1:
    st.title("📈 Bloque 5: Desempeño e Impacto de la Innovación")
with col_nav2:
    if st.button("⬅️ Volver al Inicio"):
        st.switch_page("plataforma.py")

# Función para visualización dinámica
def ficha_desempeno(codigo, titulo, explicacion, mapa_opciones, clave):
    st.markdown(f"""
    <div style='background-color: #f8fafc; padding: 12px; border-radius: 8px; border-left: 5px solid #64748b; margin-top: 15px;'>
        <strong style='color: #1e293b;'>{codigo} - {titulo}</strong><br>
        <span style='color: #475569; font-size: 0.85rem;'>{explicacion}</span>
    </div>
    """, unsafe_allow_html=True)
    
    valor = st.select_slider(
        f"Selección {clave}",
        options=[1, 2, 3, 4, 5],
        key=f"d_{clave}",
        label_visibility="collapsed"
    )
    
    texto_seleccionado = mapa_opciones.get(valor, "")
    st.markdown(f"**Nivel {valor}:** *{texto_seleccionado}*")
    return valor

# Opciones estándar para impacto (usadas en casi todo el bloque)
opt_impacto = {1: "Nulo, negativo", 2: "Escaso", 3: "Moderado", 4: "Alto", 5: "Muy alto"}

# --- 5.1 IMPACTO ESTIMADO ---
st.header("5.1 Impacto Estimado de la Innovación")

# 5.1.1 Innovación en Producto
st.subheader("📦 Impacto en Producto")
c1, c2 = st.columns(2)
with c1:
    ficha_desempeno("5.1.1.1", "Inn Ventas", "Impacto en la tasa de crecimiento en ventas", opt_impacto, "5111")
    ficha_desempeno("5.1.1.2", "Inn Empl", "Impacto en el empleo de la compañía", opt_impacto, "5112")
with c2:
    ficha_desempeno("5.1.1.3", "Inn Rent", "Impacto en la rentabilidad de la compañía", opt_impacto, "5113")
    ficha_desempeno("5.1.1.4", "Inn Internac", "Impacto en la internacionalización y nuevos mercados", opt_impacto, "5114")

# 5.1.2 Innovación en Proceso
st.subheader("⚙️ Impacto en Proceso")
c3, c4 = st.columns(2)
with c3:
    ficha_desempeno("5.1.2.1", "Inn Costes", "Reducción de costes y aumento de productividad", opt_impacto, "5121")
with c4:
    ficha_desempeno("5.1.2.2", "Inn Calidad", "Mejora en calidad de productos o servicios", opt_impacto, "5122")

# 5.1.3 Innovación Organizativa
st.subheader("🏢 Impacto Organizativo")
c5, c6 = st.columns(2)
with c5:
    ficha_desempeno("5.1.3.1", "Inn RH", "Impacto en motivación y satisfacción del personal", opt_impacto, "5131")
with c6:
    ficha_desempeno("5.1.3.2", "Inn Admin", "Eficiencia administrativa y ahorro de costes de gestión", opt_impacto, "5132")

st.divider()

# --- 5.2 IMPACTO EFECTIVO ---
st.header("5.2 Impacto Efectivo de la Innovación")
c7, c8 = st.columns(2)
with c7:
    d521 = {1: "Ninguno", 2: "1-2", 3: "3-5", 4: "Más de 5", 5: "Lanzamiento nuevas líneas de negocio"}
    ficha_desempeno("5.2.1", "Num Nprod", "Número de nuevos productos/servicios (últimos 5 años)", d521, "521")
    
    d522 = {1: "0%", 2: "Menos del 10%", 3: "10-25%", 4: "26-50%", 5: "Más del 50%"}
    ficha_desempeno("5.2.2", "Porc Vtas", "% ventas de productos innovadores (últimos 5 años)", d522, "522")

with c8:
    d523 = {1: "0%", 2: "Menos del 10%", 3: "10-25%", 4: "26-50%", 5: "Más del 50%"}
    ficha_desempeno("5.2.3", "Inn Exito", "% de nuevos productos que han tenido éxito", d523, "523")

st.divider()
if st.button("💾 Finalizar Área de Innovación"):
    st.balloons()
    st.success("Bloque 5 guardado. Área de Innovación completada al 100%.")