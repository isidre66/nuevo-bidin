import streamlit as st
import json, os

st.set_page_config(page_title="Desempeño e Impacto", layout="wide")

PERFIL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'perfil_empresa.json')

def cargar_perfil():
    if os.path.exists(PERFIL_FILE):
        with open(PERFIL_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    return {}

def guardar_en_perfil(datos):
    perfil = cargar_perfil(); perfil.update(datos)
    with open(PERFIL_FILE, 'w', encoding='utf-8') as f: json.dump(perfil, f, ensure_ascii=False, indent=2)

def get_supabase():
    try:
        from supabase import create_client
        url = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL",""))
        key = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY",""))
        if url and key: return create_client(url, key)
    except Exception: pass
    return None

def cargar_respuestas_supabase():
    sb = get_supabase()
    ec = st.session_state.get("empresa_codigo"); ue = st.session_state.get("usuario_email")
    if not sb or not ec or not ue: return {}
    try:
        res = sb.table("respuestas").select("item,valor").eq("empresa_codigo",ec).eq("usuario_email",ue).eq("bloque",5).execute()
        return {r["item"]: int(r["valor"]) for r in res.data} if res.data else {}
    except Exception: return {}

def guardar_en_supabase(items_dict):
    sb = get_supabase()
    ec = st.session_state.get("empresa_codigo"); ue = st.session_state.get("usuario_email")
    if not sb or not ec or not ue: return False
    try:
        for item, valor in items_dict.items():
            sb.table("respuestas").upsert({"empresa_codigo":ec,"usuario_email":ue,"bloque":5,"item":item,"valor":float(valor)},
                on_conflict="empresa_codigo,usuario_email,bloque,item").execute()
        return True
    except Exception: return False

perfil = cargar_perfil()
for k, v in perfil.items():
    if k not in st.session_state: st.session_state[k] = v

ec = st.session_state.get("empresa_codigo"); ue = st.session_state.get("usuario_email")
if ec and ue:
    st.markdown(f"""<div style="background:#f0fdf4;border:1px solid #10b981;border-radius:8px;
        padding:8px 16px;margin-bottom:12px;font-size:.84rem;color:#065f46;">
        ✅ Sesión activa · <strong>{ue}</strong> · Empresa <strong>{ec}</strong></div>""", unsafe_allow_html=True)
    resp_prev = cargar_respuestas_supabase()
else:
    st.warning("⚠️ Para guardar tus respuestas en la plataforma, accede desde la página **Acceso**.")
    resp_prev = {}

def val(key, default=1):
    if resp_prev: return resp_prev.get(key, default)
    if ec and ue: return default
    return int(perfil.get(key, default))

def ficha_desempeno(codigo, titulo, explicacion, mapa_opciones, clave, val_guardado):
    st.markdown(f"""<div style='background-color:#f8fafc;padding:12px;border-radius:8px;
        border-left:5px solid #64748b;margin-top:15px;'>
        <strong style='color:#1e293b;'>{codigo} - {titulo}</strong><br>
        <span style='color:#475569;font-size:0.85rem;'>{explicacion}</span></div>""", unsafe_allow_html=True)
    valor = st.select_slider(f"Selección {clave}", options=[1,2,3,4,5], value=val_guardado, label_visibility="collapsed")
    st.markdown(f"**Nivel {valor}:** *{mapa_opciones.get(valor,'')}*")
    return valor

opt = {1:"Nulo, negativo",2:"Escaso",3:"Moderado",4:"Alto",5:"Muy alto"}

st.title("📈 Bloque 5: Desempeño e Impacto de la Innovación")
if resp_prev: st.success("✅ Tienes respuestas guardadas. Puedes modificarlas y volver a guardar.")
elif st.session_state.get('b5_finalizado'): st.success("✅ Bloque completado. Puedes modificar y volver a guardar.")

st.header("5.1 Impacto Estimado de la Innovación")
st.subheader("📦 Innovación en Producto")
c1,c2 = st.columns(2)
with c1:
    r5111 = ficha_desempeno("5.1.1.1","Inn Ventas","Impacto en crecimiento en ventas",opt,"5111",val('d_5111'))
    r5113 = ficha_desempeno("5.1.1.3","Inn Rent","Impacto en rentabilidad",opt,"5113",val('d_5113'))
with c2:
    r5112 = ficha_desempeno("5.1.1.2","Inn Empl","Impacto en el empleo",opt,"5112",val('d_5112'))
    r5114 = ficha_desempeno("5.1.1.4","Inn Internac","Impacto en internacionalización",opt,"5114",val('d_5114'))

st.subheader("⚙️ Innovación en Proceso")
c3,c4 = st.columns(2)
with c3:
    r5121 = ficha_desempeno("5.1.2.1","Inn Costes","Reducción de costes y productividad",opt,"5121",val('d_5121'))
    r5123 = ficha_desempeno("5.1.2.3","Inn Metod","Impacto en métodos productivos",opt,"5123",val('d_5123'))
with c4:
    r5122 = ficha_desempeno("5.1.2.2","Inn Sost","Impacto en eficiencia energética",opt,"5122",val('d_5122'))

st.subheader("🏢 Innovación Organizativa")
c5,c6 = st.columns(2)
with c5:
    r5131 = ficha_desempeno("5.1.3.1","Inn RH","Impacto en motivación del personal",opt,"5131",val('d_5131'))
with c6:
    r5132 = ficha_desempeno("5.1.3.2","Inn Admin","Impacto en eficiencia administrativa",opt,"5132",val('d_5132'))

st.header("5.2 Impacto Efectivo de la Innovación")
c7,c8 = st.columns(2)
with c7:
    r521 = ficha_desempeno("5.2.1","Num Nprod","Número de nuevos productos últimos 5 años",
        {1:"Ninguno",2:"1-2",3:"3-5",4:"Más de 5",5:"Nuevas líneas de negocio"},"521",val('d_521'))
with c8:
    r522 = ficha_desempeno("5.2.2","Porc Vtas","% ventas de productos innovadores",
        {1:"0%",2:"Menos del 10%",3:"10-25%",4:"26-50%",5:"Más del 50%"},"522",val('d_522'))
c9,_ = st.columns(2)
with c9:
    r523 = ficha_desempeno("5.2.3","Inn Exito","% nuevos productos con éxito",
        {1:"0-15%",2:"10-30%",3:"30-50%",4:"50-70%",5:"Más del 70%"},"523",val('d_523'))

st.divider()
if st.button("💾 Guardar Bloque 5", use_container_width=True, type="primary"):
    s511=(r5111+r5112+r5113+r5114)/4; s512=(r5121+r5122+r5123)/3; s513=(r5131+r5132)/2
    s51=(s511*0.40)+(s512*0.35)+(s513*0.25); s52=(r521+r522+r523)/3
    score_b5=(s51*0.40)+(s52*0.60)
    st.session_state.update({'score_sub5_11':s511,'score_sub5_12':s512,'score_sub5_13':s513,
        'score_sub5_1':s51,'score_sub5_2':s52,'score_b5':score_b5,'b5_finalizado':True})
    items = {'d_5111':r5111,'d_5112':r5112,'d_5113':r5113,'d_5114':r5114,
             'd_5121':r5121,'d_5122':r5122,'d_5123':r5123,
             'd_5131':r5131,'d_5132':r5132,'d_521':r521,'d_522':r522,'d_523':r523}
    guardar_en_perfil({**{'score_sub5_11':s511,'score_sub5_12':s512,'score_sub5_13':s513,
        'score_sub5_1':s51,'score_sub5_2':s52,'score_b5':score_b5,'b5_finalizado':True}, **items})
    if ec and ue:
        ok = guardar_en_supabase(items)
        if ok: st.success(f"✅ Bloque 5 guardado en la plataforma. Índice Desempeño Innovación: **{score_b5:.2f}/5**")
        else: st.warning(f"⚠️ Guardado localmente. Índice: **{score_b5:.2f}/5**")
    else:
        st.success(f"✅ Bloque 5 guardado. Índice Desempeño Innovación: **{score_b5:.2f}/5**")