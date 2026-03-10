import streamlit as st
import json
import os

st.set_page_config(page_title="Desempeño e Impacto", layout="wide")

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

def ficha_desempeno(codigo, titulo, explicacion, mapa_opciones, clave, val_guardado):
    st.markdown(f"""
    <div style='background-color:#f8fafc;padding:12px;border-radius:8px;border-left:5px solid #64748b;margin-top:15px;'>
        <strong style='color:#1e293b;'>{codigo} - {titulo}</strong><br>
        <span style='color:#475569;font-size:0.85rem;'>{explicacion}</span>
    </div>""", unsafe_allow_html=True)
    valor = st.select_slider(f"Selección {clave}", options=[1,2,3,4,5],
        value=val_guardado, label_visibility="collapsed")
    st.markdown(f"**Nivel {valor}:** *{mapa_opciones.get(valor,'')}*")
    return valor

opt = {1:"Nulo, negativo",2:"Escaso",3:"Moderado",4:"Alto",5:"Muy alto"}

st.title("📈 Bloque 5: Desempeño e Impacto de la Innovación")
if st.session_state.get('b5_finalizado'):
    st.success("✅ Bloque completado. Puedes modificar y volver a guardar.")

st.header("5.1 Impacto Estimado de la Innovación")

st.subheader("📦 Innovación en Producto")
c1,c2 = st.columns(2)
with c1:
    r5111 = ficha_desempeno("5.1.1.1","Inn Ventas","Impacto en crecimiento en ventas",opt,"5111",perfil.get('d_5111',1))
    r5113 = ficha_desempeno("5.1.1.3","Inn Rent","Impacto en rentabilidad",opt,"5113",perfil.get('d_5113',1))
with c2:
    r5112 = ficha_desempeno("5.1.1.2","Inn Empl","Impacto en el empleo",opt,"5112",perfil.get('d_5112',1))
    r5114 = ficha_desempeno("5.1.1.4","Inn Internac","Impacto en internacionalización",opt,"5114",perfil.get('d_5114',1))

st.subheader("⚙️ Innovación en Proceso")
c3,c4 = st.columns(2)
with c3:
    r5121 = ficha_desempeno("5.1.2.1","Inn Costes","Reducción de costes y productividad",opt,"5121",perfil.get('d_5121',1))
    r5123 = ficha_desempeno("5.1.2.3","Inn Metod","Impacto en métodos productivos",opt,"5123",perfil.get('d_5123',1))
with c4:
    r5122 = ficha_desempeno("5.1.2.2","Inn Sost","Impacto en eficiencia energética",opt,"5122",perfil.get('d_5122',1))

st.subheader("🏢 Innovación Organizativa")
c5,c6 = st.columns(2)
with c5:
    r5131 = ficha_desempeno("5.1.3.1","Inn RH","Impacto en motivación del personal",opt,"5131",perfil.get('d_5131',1))
with c6:
    r5132 = ficha_desempeno("5.1.3.2","Inn Admin","Impacto en eficiencia administrativa",opt,"5132",perfil.get('d_5132',1))

st.header("5.2 Impacto Efectivo de la Innovación")
c7,c8 = st.columns(2)
with c7:
    r521 = ficha_desempeno("5.2.1","Num Nprod","Número de nuevos productos últimos 5 años",
        {1:"Ninguno",2:"1-2",3:"3-5",4:"Más de 5",5:"Nuevas líneas de negocio"},"521",perfil.get('d_521',1))
with c8:
    r522 = ficha_desempeno("5.2.2","Porc Vtas","% ventas de productos innovadores",
        {1:"0%",2:"Menos del 10%",3:"10-25%",4:"26-50%",5:"Más del 50%"},"522",perfil.get('d_522',1))

c9,_ = st.columns(2)
with c9:
    r523 = ficha_desempeno("5.2.3","Inn Exito","% nuevos productos con éxito",
        {1:"0-15%",2:"10-30%",3:"30-50%",4:"50-70%",5:"Más del 70%"},"523",perfil.get('d_523',1))

st.divider()
if st.button("💾 Guardar Bloque 5", use_container_width=True, type="primary"):
    s511 = (r5111+r5112+r5113+r5114)/4
    s512 = (r5121+r5122+r5123)/3
    s513 = (r5131+r5132)/2
    s51  = (s511*0.40)+(s512*0.35)+(s513*0.25)
    s52  = (r521+r522+r523)/3
    score_b5 = (s51*0.40)+(s52*0.60)
    st.session_state['score_sub5_11'] = s511
    st.session_state['score_sub5_12'] = s512
    st.session_state['score_sub5_13'] = s513
    st.session_state['score_sub5_1']  = s51
    st.session_state['score_sub5_2']  = s52
    st.session_state['score_b5']      = score_b5
    st.session_state['b5_finalizado'] = True
    guardar_en_perfil({
        'score_sub5_11':s511,'score_sub5_12':s512,'score_sub5_13':s513,
        'score_sub5_1':s51,'score_sub5_2':s52,
        'score_b5':score_b5,'b5_finalizado':True,
        'd_5111':r5111,'d_5112':r5112,'d_5113':r5113,'d_5114':r5114,
        'd_5121':r5121,'d_5122':r5122,'d_5123':r5123,
        'd_5131':r5131,'d_5132':r5132,
        'd_521':r521,'d_522':r522,'d_523':r523,
    })
    st.success(f"✅ Bloque 5 guardado. Índice Desempeño Innovación: **{score_b5:.2f}/5**")