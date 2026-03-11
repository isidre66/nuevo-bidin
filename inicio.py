import streamlit as st
import json
import os

st.set_page_config(page_title="Diagnóstico Estratégico 360°", layout="wide")

# ── Mapas de códigos numéricos (igual que en el Excel) ───────────────────────
REGIONES = {
    "Andalucia": 1, "Aragon": 2, "Asturias": 3, "Baleares": 4,
    "Canarias": 5, "Cantabria": 6, "Castilla la Mancha": 7,
    "Castilla y León": 8, "Cataluña": 9, "Com Valenciana": 10,
    "Extremadura": 11, "Galicia": 12, "Madrid": 13, "Murcia": 14,
    "Navarra": 15, "Pais Vasco": 16
}
TAMANIOS = {"Pequeña": 1, "Mediana": 2, "Grande": 3}
EXPORTACIONES = {"Menos 10 %": 1, "10 - 30 %": 2, "30 - 60 %": 3, "> 60 %": 4}
ANTIGUEDADES = {"Menos 10 años": 1, "10-30 años": 2, "> 30 años": 3}

# ── Archivo de perfil guardado localmente ────────────────────────────────────
PERFIL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'perfil_empresa.json')

def cargar_perfil():
    if os.path.exists(PERFIL_FILE):
        with open(PERFIL_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_perfil(datos):
    with open(PERFIL_FILE, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

# ── Cargar perfil guardado al session_state ───────────────────────────────────
perfil = cargar_perfil()
for k, v in perfil.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.hero-box {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    border-radius: 16px; padding: 40px; text-align: center; color: white; margin-bottom: 20px;
}
.hero-title { font-size: 2.8rem; font-weight: 800; margin-bottom: 10px; color: white; }
.hero-subtitle { font-size: 1.2rem; color: #a8d8ea; margin-bottom: 20px; }
.feature-box {
    background: #f0f4ff; border-radius: 12px; padding: 20px; text-align: center;
    border-top: 4px solid #1E3A8A; height: 100%;
}
.feature-icon { font-size: 2.5rem; margin-bottom: 10px; }
.feature-title { font-weight: 700; color: #1E3A8A; font-size: 1rem; margin-bottom: 8px; }
.feature-text { color: #475569; font-size: 0.85rem; }
.step-box {
    background: white; border-radius: 10px; padding: 15px;
    border-left: 5px solid #10B981; margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
    <div class="hero-title">🏆 Diagnóstico Estratégico 360°</div>
    <div class="hero-subtitle">Tu consultor estratégico personalizado con Inteligencia Artificial</div>
    <p style="color:#cbd5e1; font-size:1rem; max-width:700px; margin:auto;">
        La única plataforma que combina <strong style="color:white;">diagnóstico integral automatizado</strong>, 
        <strong style="color:white;">análisis comparativo</strong> con más de 1.000 empresas y 
        <strong style="color:white;">recomendaciones estratégicas personalizadas</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

# ── 4 CARACTERÍSTICAS ─────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="feature-box"><div class="feature-icon">🔬</div><div class="feature-title">Diagnóstico Integral</div><div class="feature-text">Evalúa tu empresa en Innovación, Estrategia y Transformación Digital.</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="feature-box"><div class="feature-icon">📊</div><div class="feature-title">Dashboards Comparativos</div><div class="feature-text">Compara tu posición con empresas de tu sector, región y tamaño.</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="feature-box"><div class="feature-icon">🤖</div><div class="feature-title">IA y Predicciones</div><div class="feature-text">Recomendaciones estratégicas basadas en 1.000 empresas de referencia.</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="feature-box"><div class="feature-icon">📄</div><div class="feature-title">Informes PDF</div><div class="feature-text">Genera informes ejecutivos descargables con recomendaciones personalizadas.</div></div>', unsafe_allow_html=True)

st.divider()

# ── CÓMO FUNCIONA ─────────────────────────────────────────────────────────────
st.markdown("### 🗺️ ¿Cómo funciona?")
p1, p2, p3, p4 = st.columns(4)
with p1:
    st.markdown('<div class="step-box"><strong>Paso 1 · Perfil</strong><br><span style="color:#475569;font-size:0.9rem;">Completa el perfil de tu empresa aquí abajo</span></div>', unsafe_allow_html=True)
with p2:
    st.markdown('<div class="step-box"><strong>Paso 2 · Cuestionario</strong><br><span style="color:#475569;font-size:0.9rem;">Responde los bloques del área a diagnosticar</span></div>', unsafe_allow_html=True)
with p3:
    st.markdown('<div class="step-box"><strong>Paso 3 · Dashboard</strong><br><span style="color:#475569;font-size:0.9rem;">Visualiza tu posición en dashboards comparativos</span></div>', unsafe_allow_html=True)
with p4:
    st.markdown('<div class="step-box"><strong>Paso 4 · Informe</strong><br><span style="color:#475569;font-size:0.9rem;">Descarga tu informe ejecutivo personalizado</span></div>', unsafe_allow_html=True)

st.divider()

if not st.session_state.get('save_reg_user'):
    st.warning("⚠️ Para iniciar tu diagnóstico debes completar primero el perfil de tu empresa aquí abajo.")

# ── CLASIFICACIÓN ─────────────────────────────────────────────────────────────
relacion_sectores = {
    "Alimentación y bebidas": 1, "Textil y confección": 2, "Cuero y calzado": 3,
    "Química y plásticos": 4, "Minerales no metálicos": 5, "Metalmecánico": 6,
    "Maquinaria equipo": 7, "Otras manufacturas": 8,
    "Electrónica, telecomunicaciones": 9, "Informática, software. Robótica, IA": 10,
    "Actividades I+D: biotech, farmacia": 11, "Transporte y logística": 12,
    "Consultoría y servicios profesionales": 13, "Turismo y hosteleria": 14,
    "Retail y comercio": 15, "Otros servicios": 16
}
macrosector_map = {
    1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,
    9:2,10:2,11:2,
    12:3,13:3,14:3,15:3,16:3
}
macrosector_nombre = {1:"Industria", 2:"Tecnologia avanzada", 3:"Servicios"}

sectores_lista = list(relacion_sectores.keys())
regiones_lista = list(REGIONES.keys())
tamanios_lista = list(TAMANIOS.keys())

saved_sector = st.session_state.get('save_sector_nombre', sectores_lista[0])
saved_region = st.session_state.get('save_reg_nombre', regiones_lista[0])
saved_tam    = st.session_state.get('save_tam_nombre', tamanios_lista[0])
saved_export = st.session_state.get('save_export_nombre', "Menos 10 %")
saved_anti   = st.session_state.get('save_anti_nombre', "Menos 10 años")

with st.expander("📋 PASO 1 · PERFIL DE EMPRESA — Clasificación", expanded=not bool(st.session_state.get('save_reg_user'))):
    c1, c2 = st.columns(2)
    with c1:
        id_empresa = st.text_input("🔹 ID Empresa (A)", value=st.session_state.get('save_id_empresa', ''))
        sector_sel = st.selectbox("🔹 Sector (C)", sectores_lista,
            index=sectores_lista.index(saved_sector) if saved_sector in sectores_lista else 0)
        cod_sector = relacion_sectores[sector_sel]
        cod_macro  = macrosector_map[cod_sector]
        st.info(f"**Macrosector (B):** {macrosector_nombre[cod_macro]}")
        tam_sel = st.selectbox("🔹 Tamaño (D)", tamanios_lista,
            index=tamanios_lista.index(saved_tam) if saved_tam in tamanios_lista else 0)
    with c2:
        export_sel = st.selectbox("🔹 Exportación (E)", list(EXPORTACIONES.keys()),
            index=list(EXPORTACIONES.keys()).index(saved_export) if saved_export in EXPORTACIONES else 0)
        anti_sel = st.selectbox("🔹 Antigüedad (F)", list(ANTIGUEDADES.keys()),
            index=list(ANTIGUEDADES.keys()).index(saved_anti) if saved_anti in ANTIGUEDADES else 0)
        reg_sel = st.selectbox("🔹 Región (G)", regiones_lista,
            index=regiones_lista.index(saved_region) if saved_region in regiones_lista else 0)
        cluster = st.text_input("🔹 Cluster (H)", value=st.session_state.get('save_cluster', ''))

    if st.button("💾 Guardar Clasificación", use_container_width=True, type="primary"):
        # Guardar nombres para mostrar
        st.session_state['save_id_empresa']   = id_empresa
        st.session_state['save_sector_nombre']= sector_sel
        st.session_state['save_tam_nombre']   = tam_sel
        st.session_state['save_export_nombre']= export_sel
        st.session_state['save_anti_nombre']  = anti_sel
        st.session_state['save_reg_nombre']   = reg_sel
        st.session_state['save_cluster']      = cluster
        # Guardar CÓDIGOS NUMÉRICOS para comparar con Excel
        st.session_state['save_reg_user']     = REGIONES[reg_sel]
        st.session_state['save_tam_user']     = TAMANIOS[tam_sel]
        st.session_state['save_sector_cod']   = cod_sector
        st.session_state['save_macro_cod']    = cod_macro
        # Guardar en archivo local para que persista
        perfil_datos = {k: st.session_state[k] for k in [
            'save_id_empresa','save_sector_nombre','save_tam_nombre',
            'save_export_nombre','save_anti_nombre','save_reg_nombre',
            'save_cluster','save_reg_user','save_tam_user',
            'save_sector_cod','save_macro_cod'
        ]}
        guardar_perfil(perfil_datos)
        st.success("✅ Clasificación guardada correctamente.")
        st.rerun()

# ── DESEMPEÑO ECONÓMICO ───────────────────────────────────────────────────────
with st.expander("📊 PASO 1 · PERFIL DE EMPRESA — Desempeño Económico", expanded=False):
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        ventas    = st.number_input("🔹 Ventas (I) miles €", value=float(st.session_state.get('save_ventas', 0)), min_value=0.0)
        empleados = st.number_input("🔹 Empleados (J)", value=int(st.session_state.get('save_empleados', 0)), min_value=0)
    with d2:
        roa      = st.number_input("🔹 ROA (K) %", value=float(st.session_state.get('save_roa', 0.0)))
        var_vtas = st.number_input("🔹 Var. Ventas 5 años (L) %", value=float(st.session_state.get('save_var_vtas', 0.0)))
    with d3:
        var_empl = st.number_input("🔹 Var. Empleados 5 años (M) %", value=float(st.session_state.get('save_var_empl', 0.0)))
        productiv = round(ventas / empleados, 2) if empleados > 0 else 0.0
        st.metric("🔹 Productividad (N) — Automática", f"{productiv:,.2f}", help="Ventas / Empleados")
    with d4:
        coste_emp = st.number_input("🔹 Coste medio empleado (O)", value=float(st.session_state.get('save_coste_emp', 0.0)))
        endeud    = st.number_input("🔹 Ratio Endeudamiento (P) %", value=float(st.session_state.get('save_endeud', 0.0)))

    if st.button("💾 Guardar Desempeño Económico", use_container_width=True, type="primary"):
        st.session_state['save_ventas']    = ventas
        st.session_state['save_empleados'] = empleados
        st.session_state['save_roa']       = roa
        st.session_state['save_var_vtas']  = var_vtas
        st.session_state['save_var_empl']  = var_empl
        st.session_state['save_productiv'] = productiv
        st.session_state['save_coste_emp'] = coste_emp
        st.session_state['save_endeud']    = endeud
        perfil_datos = cargar_perfil()
        perfil_datos.update({
            'save_ventas': ventas, 'save_empleados': empleados,
            'save_roa': roa, 'save_var_vtas': var_vtas,
            'save_var_empl': var_empl, 'save_productiv': productiv,
            'save_coste_emp': coste_emp, 'save_endeud': endeud
        })
        guardar_perfil(perfil_datos)
        st.success("✅ Datos económicos guardados. ¡Ya puedes iniciar tu diagnóstico!")
        st.rerun()

st.divider()

# ── BOTÓN EMPEZAR ─────────────────────────────────────────────────────────────
if st.session_state.get('save_reg_user'):
    st.markdown("### ✅ Perfil completado — ¡Listo para el diagnóstico!")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Sector", st.session_state.get('save_sector_nombre', '-')[:25])
    col2.metric("Tamaño", st.session_state.get('save_tam_nombre', '-'))
    col3.metric("Región", st.session_state.get('save_reg_nombre', '-'))
    col4.metric("Ventas (miles €)", f"{st.session_state.get('save_ventas', 0):,.0f}")
    st.markdown(" ")
    if st.button("🚀 EMPEZAR DIAGNÓSTICO DE INNOVACIÓN", use_container_width=True, type="primary"):
        st.switch_page("pages/1_💻_Panel_Control.py")
else:
    st.info("👆 Completa y guarda tu perfil arriba para activar el botón de diagnóstico.") 