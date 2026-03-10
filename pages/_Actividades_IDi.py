import streamlit as st
import json
import os

st.set_page_config(page_title="Bloque 1: I+D+i", layout="wide")

# ── Archivo de perfil local ───────────────────────────────────────────────────
PERFIL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'perfil_empresa.json')

def cargar_perfil():
    if os.path.exists(PERFIL_FILE):
        with open(PERFIL_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_en_perfil(datos):
    perfil = cargar_perfil()
    perfil.update(datos)
    with open(PERFIL_FILE, 'w', encoding='utf-8') as f:
        json.dump(perfil, f, ensure_ascii=False, indent=2)

# ── Cargar datos guardados ────────────────────────────────────────────────────
perfil = cargar_perfil()
for k, v in perfil.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Leer valores guardados para los sliders ───────────────────────────────────
v111 = perfil.get('it_111', 1)
v112 = perfil.get('it_112', 1)
v121 = perfil.get('it_121', 1)
v122 = perfil.get('it_122', 1)
v123 = perfil.get('it_123', 1)
v131 = perfil.get('it_131', 1)
v132 = perfil.get('it_132', 1)

st.title("BLOQUE 1: ACTIVIDADES DE I+D+i")

if st.session_state.get('b1_finalizado'):
    st.success("✅ Este bloque ya está completado. Puedes modificar tus respuestas y volver a guardar.")

# Subindicador 1.1
st.subheader("1.1 Departamento I+D")
r111 = st.select_slider("1.1.1: Recursos técnicos dedicados a I+D",
    options=[1, 2, 3, 4, 5], value=v111)
r112 = st.select_slider("1.1.2: Recursos humanos dedicados a I+D",
    options=[1, 2, 3, 4, 5], value=v112)

# Subindicador 1.2
st.subheader("1.2 Presupuesto I+D")
r121 = st.select_slider("1.2.1: Presupuesto específico para I+D",
    options=[1, 2, 3, 4, 5], value=v121)
r122 = st.select_slider("1.2.2: I+D subvencionado",
    options=[1, 2, 3, 4, 5], value=v122)
r123 = st.select_slider("1.2.3: Participación en proyectos con financiación pública",
    options=[1, 2, 3, 4, 5], value=v123)

# Subindicador 1.3
st.subheader("1.3 Gasto en Innovación")
r131 = st.select_slider("1.3.1: Gasto estimado anual en innovación sobre ventas",
    options=[1, 2, 3, 4, 5], value=v131)
r132 = st.select_slider("1.3.2: Evolución futura del gasto en innovación",
    options=[1, 2, 3, 4, 5], value=v132)

st.divider()

if st.button("💾 GUARDAR BLOQUE 1", use_container_width=True, type="primary"):
    s1 = (r111 + r112) / 2
    s2 = (r121 + r122 + r123) / 3
    s3 = (r131 + r132) / 2
    score_b1 = (s1 * 0.2) + (s2 * 0.4) + (s3 * 0.4)

    st.session_state['score_sub1_1']  = s1
    st.session_state['score_sub1_2']  = s2
    st.session_state['score_sub1_3']  = s3
    st.session_state['score_b1']      = score_b1
    st.session_state['b1_finalizado'] = True

    guardar_en_perfil({
        'score_sub1_1': s1, 'score_sub1_2': s2,
        'score_sub1_3': s3, 'score_b1': score_b1,
        'b1_finalizado': True,
        'it_111': r111, 'it_112': r112,
        'it_121': r121, 'it_122': r122, 'it_123': r123,
        'it_131': r131, 'it_132': r132,
    })

    st.success(f"✅ Bloque 1 guardado. Índice I+D+i: **{score_b1:.2f}/5**")
    st.info("Ahora puedes ir al Dashboard de Innovación para ver tu posición comparativa.")
