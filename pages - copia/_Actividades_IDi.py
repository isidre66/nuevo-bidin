import streamlit as st

st.set_page_config(page_title="Bloque 1: I+D+i", layout="wide")

# Mantener los valores de los sliders al cambiar de página
items = ["it_111", "it_112", "it_121", "it_122", "it_123", "it_131", "it_132"]
for i in items:
    if i not in st.session_state: st.session_state[i] = 1

st.title("BLOQUE 1: ACTIVIDADES DE I+D+i")

# Subindicador 1.1
st.subheader("Departamento I+D")
r111 = st.select_slider("1.1.1: Recursos técnicos", options=[1, 2, 3, 4, 5], key="it_111")
r112 = st.select_slider("1.1.2: Recursos humanos", options=[1, 2, 3, 4, 5], key="it_112")

# Subindicador 1.2
st.subheader("Presupuesto I+D")
r121 = st.select_slider("1.2.1: Asignación presupuestaria", options=[1, 2, 3, 4, 5], key="it_121")
r122 = st.select_slider("1.2.2: Subvenciones", options=[1, 2, 3, 4, 5], key="it_122")
r123 = st.select_slider("1.2.3: Proyectos públicos", options=[1, 2, 3, 4, 5], key="it_123")

# Subindicador 1.3
st.subheader("Gasto en Innovación")
r131 = st.select_slider("1.3.1: Gasto sobre ventas", options=[1, 2, 3, 4, 5], key="it_131")
r132 = st.select_slider("1.3.2: Evolución futura", options=[1, 2, 3, 4, 5], key="it_132")

if st.button("💾 FINALIZAR Y GUARDAR BLOQUE 1"):
    # Cálculo con algoritmo invisible
    s1 = (r111 + r112) / 2
    s2 = (r121 + r122 + r123) / 3
    s3 = (r131 + r132) / 2
    
    st.session_state['score_sub1_1'] = s1
    st.session_state['score_sub1_2'] = s2
    st.session_state['score_sub1_3'] = s3
    st.session_state['score_b1'] = (s1 * 0.2) + (s2 * 0.4) + (s3 * 0.4)
    st.session_state['b1_finalizado'] = True
    st.success("Bloque guardado. Ya puedes consultar el radar.")