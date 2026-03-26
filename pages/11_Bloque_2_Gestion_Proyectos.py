import streamlit as st
import json, os

st.set_page_config(page_title="Gestión de Proyectos", layout="wide")

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
        res = sb.table("respuestas").select("item,valor").eq("empresa_codigo",ec).eq("usuario_email",ue).eq("bloque",2).execute()
        return {r["item"]: int(r["valor"]) for r in res.data} if res.data else {}
    except Exception: return {}

def guardar_en_supabase(items_dict):
    sb = get_supabase()
    ec = st.session_state.get("empresa_codigo"); ue = st.session_state.get("usuario_email")
    if not sb or not ec or not ue: return False
    try:
        for item, valor in items_dict.items():
            sb.table("respuestas").upsert({"empresa_codigo":ec,"usuario_email":ue,"bloque":2,"item":item,"valor":float(valor)},
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

def ficha_gestion(codigo, titulo, explicacion, mapa_opciones, clave, val_guardado):
    st.markdown(f"""<div style='background-color:#f0fdf4;padding:12px;border-radius:8px;
        border-left:5px solid #22c55e;margin-top:15px;'>
        <strong style='color:#166534;'>{codigo} - {titulo}</strong><br>
        <span style='color:#475569;font-size:0.85rem;'>{explicacion}</span></div>""", unsafe_allow_html=True)
    valor = st.select_slider(f"Selección {clave}", options=[1,2,3,4,5], value=val_guardado, label_visibility="collapsed")
    st.markdown(f"**Nivel {valor}:** *{mapa_opciones.get(valor,'')}*")
    return valor

st.title("⚙️ Bloque 2: Gestión de Proyectos de Innovación")
if resp_prev: st.success("✅ Tienes respuestas guardadas. Puedes modificarlas y volver a guardar.")
elif st.session_state.get('b2_finalizado'): st.success("✅ Bloque completado. Puedes modificar y volver a guardar.")

st.header("2.1 Gestión Básica de Proyectos")
c1,c2 = st.columns(2)
with c1:
    r211 = ficha_gestion("2.1.1","Multidisciplinar","Participación activa de marketing, I+D, producción",
        {1:"Nunca",2:"Puntualmente",3:"En algún proyecto",4:"En varios proyectos",5:"Cooperación activa siempre"},"211",val('g_211'))
    r212 = ficha_gestion("2.1.2","Consenso","Entendimiento sobre tareas, plazos y recursos",
        {1:"Inexistente",2:"Escaso, puntual",3:"En algún proyecto",4:"En la mayoría de proyectos",5:"Alineación sistemática siempre"},"212",val('g_212'))
with c2:
    r213 = ficha_gestion("2.1.3","Apoyo Directivo","Apoyo y promoción fluida de los directivos",
        {1:"Inexistente",2:"Escaso",3:"En algún proyecto",4:"En la mayoría de proyectos",5:"Apoyo continuo y sistemático"},"213",val('g_213'))
    r214 = ficha_gestion("2.1.4","Planificación","Planificación sistemática con responsables claros",
        {1:"Nunca",2:"Puntualmente",3:"En algún proyecto",4:"En la mayoría de proyectos",5:"En todos los proyectos"},"214",val('g_214'))

st.header("2.2 Gestión Avanzada")
c3,c4 = st.columns(2)
with c3:
    r221 = ficha_gestion("2.2.1","Tec. Avanzadas","Uso de herramientas de diseño y simulación",
        {1:"No se usan",2:"Puntualmente",3:"En algún proyecto",4:"En la mayoría de proyectos",5:"Uso avanzado y sistemático"},"221",val('g_221'))
    r222 = ficha_gestion("2.2.2","Prop. Industrial","Protección de patentes, marcas y diseños",
        {1:"Nulo",2:"Sólo registros de marca",3:"En algunos proyectos",4:"Gestión proactiva",5:"Estrategia integral de Prop. Ind."},"222",val('g_222'))
with c4:
    r223 = ficha_gestion("2.2.3","Gestión Ágil","Uso de metodologías ágiles en proyectos",
        {1:"No se conocen",2:"Interés futuro",3:"Uso puntual",4:"Uso frecuente",5:"Metodologías integradas (Agile/Lean)"},"223",val('g_223'))

st.header("2.3 Organización de Proyectos")
c5,c6 = st.columns(2)
with c5:
    r231 = ficha_gestion("2.3.1","Adm. Proyectos","Estructura y administración de los proyectos",
        {1:"Inexistente",2:"Administración puntual",3:"Procedimiento formalizado",4:"Seguimiento sistemático",5:"Monitorización digital continua"},"231",val('g_231'))
with c6:
    r232 = ficha_gestion("2.3.2","Competición","Fomento de competencia entre equipos internos",
        {1:"Nunca",2:"A veces",3:"Con cierta frecuencia",4:"Habitualmente",5:"Siempre con apoyo externo"},"232",val('g_232'))

st.header("2.4 Evaluación del Rendimiento")
c7,c8 = st.columns(2)
with c7:
    r241 = ficha_gestion("2.4.1","Rendimiento","Evaluación de KPIs y métricas de proyectos",
        {1:"Inexistente",2:"Informal, sin métricas",3:"Evaluación parcial",4:"Estructurado con KPIs",5:"Análisis sistemático de desviaciones"},"241",val('g_241'))
with c8:
    r242 = ficha_gestion("2.4.2","Aplicación","Uso de resultados para futuros proyectos",
        {1:"No se usan",2:"Uso informal y puntual",3:"Para corregir errores operativos",4:"Para seleccionar nuevos proyectos",5:"Guían la estrategia global"},"242",val('g_242'))

st.divider()
if st.button("💾 Guardar Bloque 2", use_container_width=True, type="primary"):
    s21=(r211+r212+r213+r214)/4; s22=(r221+r222+r223)/3; s23=(r231+r232)/2; s24=(r241+r242)/2
    score_b2=(s21*0.30)+(s22*0.35)+(s23*0.15)+(s24*0.20)
    st.session_state.update({'score_sub2_1':s21,'score_sub2_2':s22,'score_sub2_3':s23,
        'score_sub2_4':s24,'score_b2':score_b2,'b2_finalizado':True})
    items = {'g_211':r211,'g_212':r212,'g_213':r213,'g_214':r214,'g_221':r221,'g_222':r222,
             'g_223':r223,'g_231':r231,'g_232':r232,'g_241':r241,'g_242':r242}
    guardar_en_perfil({**{'score_sub2_1':s21,'score_sub2_2':s22,'score_sub2_3':s23,
        'score_sub2_4':s24,'score_b2':score_b2,'b2_finalizado':True}, **items})
    if ec and ue:
        ok = guardar_en_supabase(items)
        if ok: st.success(f"✅ Bloque 2 guardado en la plataforma. Índice Gestión Proyectos: **{score_b2:.2f}/5**")
        else: st.warning(f"⚠️ Guardado localmente. Índice: **{score_b2:.2f}/5**")
    else:
        st.success(f"✅ Bloque 2 guardado. Índice Gestión Proyectos: **{score_b2:.2f}/5**")