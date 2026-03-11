import streamlit as st
import json
import os

st.set_page_config(page_title="Desarrollo de Productos", layout="wide")

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

def ficha_dinamica(codigo, titulo, explicacion, mapa_opciones, clave, val_guardado):
    st.markdown(f"""
    <div style='background-color:#f0f9ff;padding:12px;border-radius:8px;border-left:5px solid #0ea5e9;margin-top:15px;'>
        <strong style='color:#0c4a6e;'>{codigo} - {titulo}</strong><br>
        <span style='color:#64748b;font-size:0.85rem;'>{explicacion}</span>
    </div>""", unsafe_allow_html=True)
    valor = st.select_slider(f"Selección {clave}", options=[1,2,3,4,5],
        value=val_guardado, label_visibility="collapsed")
    st.markdown(f"**Nivel {valor}:** *{mapa_opciones.get(valor,'')}*")
    return valor

st.title("🚀 Bloque 3: Desarrollo de Nuevos Productos")
if st.session_state.get('b3_finalizado'):
    st.success("✅ Bloque completado. Puedes modificar y volver a guardar.")

st.header("3.1 Estrategia y Recursos")
c1,c2 = st.columns(2)
with c1:
    r311 = ficha_dinamica("3.1.1","Estrategia","Estrategia y proceso de desarrollo de productos",
        {1:"Inexistente",2:"Puntual e informal",3:"Sólo ante oportunidades claras",4:"Analiza demanda y necesidades",5:"Enfoque multidisciplinar"},"311",perfil.get('p_311',1))
with c2:
    r312 = ficha_dinamica("3.1.2","Recursos","Gestión de recursos para el desarrollo",
        {1:"No se asignan",2:"Asignación puntual",3:"Recursos internos I+D",4:"Equipos multidisciplinares",5:"Colaboración con externos"},"312",perfil.get('p_312',1))

st.header("3.2 Oportunidad y Mercado")
c3,c4 = st.columns(2)
with c3:
    r321 = ficha_dinamica("3.2.1","Identificación","Capacidad de identificar oportunidades desatendidas",
        {1:"No, nunca",2:"Muy rara vez",3:"Algunas veces",4:"Bastantes veces",5:"Con mucha frecuencia"},"321",perfil.get('p_321',1))
    r323 = ficha_dinamica("3.2.3","Crec Prod","Potencial de ventas y crecimiento de nuevos productos",
        {1:"Nulo",2:"Bajo",3:"Moderado",4:"Alto",5:"Muy alto"},"323",perfil.get('p_323',1))
with c4:
    r322 = ficha_dinamica("3.2.2","Tamaño","Tamaño del mercado de las innovaciones",
        {1:"Nulo, marginal",2:"Pequeño",3:"Mediano",4:"Grande",5:"Muy grande"},"322",perfil.get('p_322',1))
    r324 = ficha_dinamica("3.2.4","Rent Prod","Rentabilidad de los nuevos productos",
        {1:"Negativa, nula",2:"Inferior al promedio",3:"Similar al promedio",4:"Superior al promedio",5:"Muy superior"},"324",perfil.get('p_324',1))

st.header("3.3 Receptividad y Valor")
c5,c6 = st.columns(2)
with c5:
    r331 = ficha_dinamica("3.3.1","Probar","Predisposición a probar nuevos productos",
        {1:"Nula",2:"Baja",3:"Media",4:"Alta",5:"Muy alta"},"331",perfil.get('p_331',1))
    r333 = ficha_dinamica("3.3.3","Valor","Diferenciación y valor de los nuevos productos",
        {1:"Nulo",2:"Bajo",3:"Moderado",4:"Alto",5:"Muy alto"},"333",perfil.get('p_333',1))
with c6:
    r332 = ficha_dinamica("3.3.2","Pagar","Predisposición a pagar por nuevos productos",
        {1:"Nula",2:"Baja",3:"Media",4:"Alta",5:"Muy alta"},"332",perfil.get('p_332',1))

st.header("3.4 Interacción con Clientes")
c7,c8 = st.columns(2)
with c7:
    r341 = ficha_dinamica("3.4.1","Diseño","Uso de herramientas de design thinking",
        {1:"No conocido",2:"Programado",3:"Puntual",4:"Considerable",5:"Total"},"341",perfil.get('p_341',1))
with c8:
    r342 = ficha_dinamica("3.4.2","Interacción","Contacto con usuarios durante el desarrollo",
        {1:"No, en absoluto",2:"Puntual y parcial",3:"En algunos proyectos",4:"Con frecuencia",5:"De forma continua"},"342",perfil.get('p_342',1))

st.header("3.5 Viabilidad e Impacto")
c9,c10 = st.columns(2)
with c9:
    r351 = ficha_dinamica("3.5.1","Eco-financ","Análisis económico y rentabilidad potencial",
        {1:"No, nunca",2:"Puntualmente",3:"En algunos proyectos",4:"Con frecuencia",5:"De forma continua"},"351",perfil.get('p_351',1))
with c10:
    r352 = ficha_dinamica("3.5.2","Viab Com","Uso de Business Model Canvas y similares",
        {1:"No conocido",2:"Programado",3:"Puntual",4:"Considerable",5:"Total"},"352",perfil.get('p_352',1))

st.divider()
if st.button("💾 Guardar Bloque 3", use_container_width=True, type="primary"):
    s31 = (r311+r312)/2
    s32 = (r321+r322+r323+r324)/4
    s33 = (r331+r332+r333)/3
    s34 = (r341+r342)/2
    s35 = (r351+r352)/2
    score_b3 = (s31*0.25)+(s32*0.20)+(s33*0.15)+(s34*0.15)+(s35*0.25)
    st.session_state['score_sub3_1']  = s31
    st.session_state['score_sub3_2']  = s32
    st.session_state['score_sub3_3']  = s33
    st.session_state['score_sub3_4']  = s34
    st.session_state['score_sub3_5']  = s35
    st.session_state['score_b3']      = score_b3
    st.session_state['b3_finalizado'] = True
    guardar_en_perfil({
        'score_sub3_1':s31,'score_sub3_2':s32,'score_sub3_3':s33,
        'score_sub3_4':s34,'score_sub3_5':s35,
        'score_b3':score_b3,'b3_finalizado':True,
        'p_311':r311,'p_312':r312,'p_321':r321,'p_322':r322,
        'p_323':r323,'p_324':r324,'p_331':r331,'p_332':r332,
        'p_333':r333,'p_341':r341,'p_342':r342,'p_351':r351,'p_352':r352,
    })
    st.success(f"✅ Bloque 3 guardado. Índice Desarrollo Productos: **{score_b3:.2f}/5**")