import streamlit as st
import json
import os

st.set_page_config(page_title="Estrategia de Innovación", layout="wide")

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

perfil = cargar_perfil()
for k, v in perfil.items():
    if k not in st.session_state:
        st.session_state[k] = v

def ficha_estrategia(codigo, titulo, explicacion, mapa_opciones, clave, val_guardado, inversa=False):
    bg = "#fff1f2" if inversa else "#fff7ed"
    border = "#e11d48" if inversa else "#f97316"
    st.markdown(f"""
    <div style='background-color:{bg};padding:12px;border-radius:8px;border-left:5px solid {border};margin-top:15px;'>
        <strong style='color:#7c2d12;'>{codigo} - {titulo} {'⚠️ (Valoración Inversa)' if inversa else ''}</strong><br>
        <span style='color:#475569;font-size:0.85rem;'>{explicacion}</span>
    </div>""", unsafe_allow_html=True)
    valor = st.select_slider(f"Selección {clave}", options=[1,2,3,4,5],
        value=val_guardado, label_visibility="collapsed")
    st.markdown(f"**Nivel {valor}:** *{mapa_opciones.get(valor,'')}*")
    return valor

st.title("🎯 Bloque 4: Estrategia de Innovación")
if st.session_state.get('b4_finalizado'):
    st.success("✅ Bloque completado. Puedes modificar y volver a guardar.")

st.header("4.1 Innovación Estratégica")
c1,c2 = st.columns(2)
with c1:
    r411 = ficha_estrategia("4.1.1","Alinear","Integración de la innovación en la estrategia",
        {1:"Nula alineación",2:"Relación puntual",3:"Innovación en la estrategia",4:"Decisiones con innovación",5:"Estrategia proactiva sistemática"},"411",perfil.get('e_411',1))
with c2:
    r412 = ficha_estrategia("4.1.2","Lider","Posicionamiento ante la innovación",
        {1:"No se contempla",2:"Sólo imitar",3:"Puntual poco diferenciada",4:"Innovación continuada",5:"Sistemática y disruptiva"},"412",perfil.get('e_412',1))

c_413, _ = st.columns(2)
with c_413:
    r413 = ficha_estrategia("4.1.3","ObjInn","Definición de objetivos claros de innovación",
        {1:"Nula",2:"Baja",3:"Moderada",4:"Elevada",5:"Definición exhaustiva"},"413",perfil.get('e_413',1))

st.header("4.2 Cultura de Innovación")
c3,c4 = st.columns(2)
with c3:
    r421 = ficha_estrategia("4.2.1","Increm","Priorización de innovaciones incrementales",
        {1:"No, en absoluto",2:"Pocas veces",3:"Con cierta frecuencia",4:"Casi siempre",5:"Siempre"},"421",perfil.get('e_421',1),inversa=True)
with c4:
    r422 = ficha_estrategia("4.2.2","Riesgo","Tolerancia al riesgo y al fracaso",
        {1:"No, en absoluto",2:"Poco riesgo",3:"Riesgo moderado",4:"Riesgo elevado",5:"Riesgo inasumible"},"422",perfil.get('e_422',1),inversa=True)

c_423, _ = st.columns(2)
with c_423:
    r423 = ficha_estrategia("4.2.3","ConInterno","Conocimiento interno de proyectos de innovación",
        {1:"No",2:"Parcialmente",3:"Sólo su área",4:"También otras áreas",5:"Conocimiento profundo"},"423",perfil.get('e_423',1))

st.header("4.3 Obstáculos")
c5,c6 = st.columns(2)
with c5:
    r431 = ficha_estrategia("4.3.1","Obst Int","Incidencia de obstáculos internos",
        {1:"Sin obstáculos",2:"Tecnológicos puntuales",3:"Organizativos",4:"Falta competencias",5:"Financieros y falta voluntad"},"431",perfil.get('e_431',1),inversa=True)
with c6:
    r432 = ficha_estrategia("4.3.2","Obst Ext","Incidencia de obstáculos externos",
        {1:"Entorno favorable",2:"Dificultad partners",3:"Dificultad financiación",4:"Competencia intensa",5:"Incertidumbre mercado"},"432",perfil.get('e_432',1),inversa=True)

st.header("4.4 Innovación Abierta")
c7,c8 = st.columns(2)
with c7:
    r441 = ficha_estrategia("4.4.1","Colab Inn","Cultura abierta y colaborativa",
        {1:"Nulo",2:"Puntual",3:"Sólo con empresas",4:"Con centros tecnológicos",5:"Con ecosistema emprendedor"},"441",perfil.get('e_441',1))
with c8:
    r442 = ficha_estrategia("4.4.2","RdCoop","Rendimiento de la cooperación en innovación",
        {1:"Impacto nulo",2:"Mejoras puntuales",3:"Contribuye a innovar",4:"Ventajas competitivas",5:"Liderazgo disruptivo"},"442",perfil.get('e_442',1))

st.header("4.5 Fomento de la Creatividad")
c9,c10 = st.columns(2)
with c9:
    r451 = ficha_estrategia("4.5.1","Creativ","Técnicas para generar ideas",
        {1:"Inexistente",2:"Puntual e informal",3:"Sesiones periódicas",4:"Herramientas formalizadas",5:"Sistema continuo"},"451",perfil.get('e_451',1))
with c10:
    r452 = ficha_estrategia("4.5.2","EvalIdeas","Sistema de evaluación y selección de ideas",
        {1:"No se evalúan",2:"Criterios subjetivos",3:"Criterios técnicos básicos",4:"Evaluación formalizada",5:"Sistema experto"},"452",perfil.get('e_452',1))

st.divider()
if st.button("💾 Guardar Bloque 4", use_container_width=True, type="primary"):
    s41 = (r411+r412+r413)/3
    s42 = (r421+r422+r423)/3
    s43 = (r431+r432)/2
    s44 = (r441+r442)/2
    s45 = (r451+r452)/2
    score_b4 = (s41*0.25)+(s42*0.25)+(s43*0.20)+(s44*0.20)+(s45*0.10)
    st.session_state['score_sub4_1']  = s41
    st.session_state['score_sub4_2']  = s42
    st.session_state['score_sub4_3']  = s43
    st.session_state['score_sub4_4']  = s44
    st.session_state['score_sub4_5']  = s45
    st.session_state['score_b4']      = score_b4
    st.session_state['b4_finalizado'] = True
    guardar_en_perfil({
        'score_sub4_1':s41,'score_sub4_2':s42,'score_sub4_3':s43,
        'score_sub4_4':s44,'score_sub4_5':s45,
        'score_b4':score_b4,'b4_finalizado':True,
        'e_411':r411,'e_412':r412,'e_413':r413,
        'e_421':r421,'e_422':r422,'e_423':r423,
        'e_431':r431,'e_432':r432,
        'e_441':r441,'e_442':r442,
        'e_451':r451,'e_452':r452,
    })
    st.success(f"✅ Bloque 4 guardado. Índice Estrategia Innovación: **{score_b4:.2f}/5**")