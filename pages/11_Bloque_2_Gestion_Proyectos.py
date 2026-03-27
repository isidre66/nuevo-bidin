import streamlit as st
import json, os

st.set_page_config(page_title="Gestión de Proyectos", layout="wide")

PERFIL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'perfil_empresa.json')
def cargar_perfil():
    if os.path.exists(PERFIL_FILE):
        with open(PERFIL_FILE,'r',encoding='utf-8') as f: return json.load(f)
    return {}
def guardar_en_perfil(datos):
    perfil=cargar_perfil(); perfil.update(datos)
    with open(PERFIL_FILE,'w',encoding='utf-8') as f: json.dump(perfil,f,ensure_ascii=False,indent=2)
def get_supabase():
    try:
        from supabase import create_client
        url=st.secrets.get("SUPABASE_URL",os.environ.get("SUPABASE_URL",""))
        key=st.secrets.get("SUPABASE_KEY",os.environ.get("SUPABASE_KEY",""))
        if url and key: return create_client(url,key)
    except Exception: pass
    return None
def cargar_respuestas_supabase():
    sb=get_supabase(); ec=st.session_state.get("empresa_codigo"); ue=st.session_state.get("usuario_email")
    if not sb or not ec or not ue: return {}
    try:
        res=sb.table("respuestas").select("item,valor").eq("empresa_codigo",ec).eq("usuario_email",ue).eq("bloque",2).execute()
        return {r["item"]:int(r["valor"]) for r in res.data} if res.data else {}
    except Exception: return {}
def guardar_en_supabase(items_dict):
    sb=get_supabase(); ec=st.session_state.get("empresa_codigo"); ue=st.session_state.get("usuario_email")
    if not sb or not ec or not ue: return False
    try:
        for item,valor in items_dict.items():
            sb.table("respuestas").upsert({"empresa_codigo":ec,"usuario_email":ue,"bloque":2,"item":item,"valor":float(valor)},
                on_conflict="empresa_codigo,usuario_email,bloque,item").execute()
        return True
    except Exception: return False

perfil=cargar_perfil()
for k,v in perfil.items():
    if k not in st.session_state: st.session_state[k]=v

ec=st.session_state.get("empresa_codigo"); ue=st.session_state.get("usuario_email")
if ec and ue:
    st.markdown(f"""<div style="background:#f0fdf4;border:1px solid #10b981;border-radius:8px;
        padding:8px 16px;margin-bottom:12px;font-size:.84rem;color:#065f46;">
        ✅ Sesión activa · <strong>{ue}</strong> · Empresa <strong>{ec}</strong></div>""",unsafe_allow_html=True)
    resp_prev=cargar_respuestas_supabase()
else:
    st.warning("⚠️ Para guardar tus respuestas en la plataforma, accede desde la página **Acceso**.")
    resp_prev={}

def val(key,default=1):
    if resp_prev: return int(resp_prev.get(key,default))
    if ec and ue: return default
    return int(perfil.get(key,default))

def aclaracion(key, texto):
    if st.button("ℹ️ Ver aclaración", key=f"acl_{key}"):
        st.session_state[f"show_acl_{key}"] = not st.session_state.get(f"show_acl_{key}", False)
    if st.session_state.get(f"show_acl_{key}"): st.info(texto)

st.title("⚙️ Bloque 2: Gestión de Proyectos de Innovación")
if resp_prev: st.success("✅ Tienes respuestas guardadas. Puedes modificarlas y volver a guardar.")
elif st.session_state.get('b2_finalizado'): st.success("✅ Bloque completado. Puedes modificar y volver a guardar.")

st.header("2.1 Gestión Básica de Proyectos")
c1,c2=st.columns(2)
with c1:
    st.markdown("**2.1.1: Gestión multidisciplinar**")
    aclaracion("211","Valore si en la gestión de proyectos de innovación participan activamente equipos multidisciplinares: marketing, I+D, producción. 1=Nunca · 2=Puntualmente · 3=En algún proyecto · 4=En varios proyectos · 5=Cooperación activa siempre.")
    r211=st.select_slider("Multidisciplinar",options=[1,2,3,4,5],value=val('g_211'),label_visibility="collapsed")
    st.caption("1=Nunca · 2=Puntual · 3=Algún proyecto · 4=Varios · 5=Siempre")

    st.markdown("**2.1.2: Consenso en proyectos**")
    aclaracion("212","Valore el grado de entendimiento y consenso sobre tareas, plazos, recursos y resultados esperados. 1=Inexistente · 2=Escaso y puntual · 3=En algún proyecto · 4=En la mayoría · 5=Alineación sistemática siempre.")
    r212=st.select_slider("Consenso",options=[1,2,3,4,5],value=val('g_212'),label_visibility="collapsed")
    st.caption("1=Inexistente · 2=Escaso · 3=Algún proyecto · 4=Mayoría · 5=Siempre")
with c2:
    st.markdown("**2.1.3: Apoyo directivo**")
    aclaracion("213","Valore en qué medida los directivos apoyan y promueven activamente una relación fluida entre los agentes implicados en los proyectos. 1=Inexistente · 2=Escaso · 3=Algún proyecto · 4=Mayoría · 5=Apoyo continuo y sistemático.")
    r213=st.select_slider("Apoyo directivo",options=[1,2,3,4,5],value=val('g_213'),label_visibility="collapsed")
    st.caption("1=Inexistente · 2=Escaso · 3=Algún proyecto · 4=Mayoría · 5=Continuo")

    st.markdown("**2.1.4: Planificación**")
    aclaracion("214","Valore en qué medida su empresa realiza una planificación sistemática con asignación clara de responsables en cada fase del proyecto. 1=Nunca · 2=Puntualmente · 3=Algún proyecto · 4=Mayoría · 5=Todos los proyectos.")
    r214=st.select_slider("Planificación",options=[1,2,3,4,5],value=val('g_214'),label_visibility="collapsed")
    st.caption("1=Nunca · 2=Puntual · 3=Algún proyecto · 4=Mayoría · 5=Todos")

st.header("2.2 Gestión Avanzada")
c3,c4=st.columns(2)
with c3:
    st.markdown("**2.2.1: Tecnologías avanzadas**")
    aclaracion("221","Valore el volumen de fondos destinados a adquirir tecnologías de vanguardia desarrolladas por otras compañías. 1=Nulo · 2=Escaso y puntual · 3=Medio · 4=Alto · 5=Muy alto.")
    r221=st.select_slider("Tec. avanzadas",options=[1,2,3,4,5],value=val('g_221'),label_visibility="collapsed")
    st.caption("1=Nulo · 2=Escaso · 3=Medio · 4=Alto · 5=Muy alto")

    st.markdown("**2.2.2: Propiedad industrial**")
    aclaracion("222","Valore si la empresa recurre a expertos en gestión de la propiedad industrial/intelectual y la transferencia. 1=Nunca · 2=Puntualmente interno · 3=Con cierta frecuencia · 4=Habitualmente · 5=Siempre, con expertos internos y externos.")
    r222=st.select_slider("Prop. industrial",options=[1,2,3,4,5],value=val('g_222'),label_visibility="collapsed")
    st.caption("1=Nunca · 2=Puntual interno · 3=Frecuente · 4=Habitual · 5=Siempre expertos")
with c4:
    st.markdown("**2.2.3: Gestión ágil**")
    aclaracion("223","Evalúe el uso de herramientas y metodologías ágiles. 1=Se desconocen · 2=Se conocen y aplicarán · 3=Herramientas básicas (Trello, Asana) · 4=Metodologías avanzadas (Scrum, Kanban) · 5=Sistema integrado y digitalizado.")
    r223=st.select_slider("Gestión ágil",options=[1,2,3,4,5],value=val('g_223'),label_visibility="collapsed")
    st.caption("1=Desconocido · 2=Previsto · 3=Básico · 4=Avanzado · 5=Integrado")

st.header("2.3 Organización de Proyectos")
c5,c6=st.columns(2)
with c5:
    st.markdown("**2.3.1: Administración de proyectos**")
    aclaracion("231","Describa cómo es la organización/administración de los proyectos de innovación. 1=Inexistente · 2=Administración puntual · 3=Procedimiento formalizado · 4=Seguimiento y control sistemático · 5=Monitorización continua digitalizada.")
    r231=st.select_slider("Adm. proyectos",options=[1,2,3,4,5],value=val('g_231'),label_visibility="collapsed")
    st.caption("1=Inexistente · 2=Puntual · 3=Formalizado · 4=Sistemático · 5=Digital continuo")
with c6:
    st.markdown("**2.3.2: Competición interna**")
    aclaracion("232","Evalúe si se fomenta la competencia entre equipos internos para promover y elegir nuevos proyectos. 1=Nunca · 2=A veces · 3=Con cierta frecuencia · 4=Habitualmente · 5=Siempre con apoyo externo.")
    r232=st.select_slider("Competición eq.",options=[1,2,3,4,5],value=val('g_232'),label_visibility="collapsed")
    st.caption("1=Nunca · 2=A veces · 3=Frecuente · 4=Habitual · 5=Siempre+externo")

st.header("2.4 Evaluación del Rendimiento")
c7,c8=st.columns(2)
with c7:
    st.markdown("**2.4.1: Evaluación del rendimiento**")
    aclaracion("241","Describa cómo se evalúa el rendimiento de los proyectos. 1=Inexistente · 2=Valoración informal sin métricas · 3=Evaluación parcial · 4=Sistema estructurado con KPIs · 5=Además, análisis sistemático de desviaciones.")
    r241=st.select_slider("Rdto. proyectos",options=[1,2,3,4,5],value=val('g_241'),label_visibility="collapsed")
    st.caption("1=Inexistente · 2=Informal · 3=Parcial · 4=KPIs · 5=Análisis desviaciones")
with c8:
    st.markdown("**2.4.2: Aplicación de resultados**")
    aclaracion("242","Describa cómo se utilizan los resultados de la evaluación para futuros proyectos. 1=No se usan · 2=Uso informal y puntual · 3=Para corregir errores · 4=Para seleccionar nuevos proyectos · 5=Guían la estrategia de innovación global.")
    r242=st.select_slider("Rdos. proyectos",options=[1,2,3,4,5],value=val('g_242'),label_visibility="collapsed")
    st.caption("1=No se usan · 2=Informal · 3=Errores · 4=Selección · 5=Estrategia global")

st.divider()
if st.button("💾 Guardar Bloque 2", use_container_width=True, type="primary"):
    s21=(r211+r212+r213+r214)/4; s22=(r221+r222+r223)/3; s23=(r231+r232)/2; s24=(r241+r242)/2
    score_b2=(s21*0.30)+(s22*0.35)+(s23*0.15)+(s24*0.20)
    st.session_state.update({'score_sub2_1':s21,'score_sub2_2':s22,'score_sub2_3':s23,
        'score_sub2_4':s24,'score_b2':score_b2,'b2_finalizado':True})
    items={'g_211':r211,'g_212':r212,'g_213':r213,'g_214':r214,'g_221':r221,'g_222':r222,
           'g_223':r223,'g_231':r231,'g_232':r232,'g_241':r241,'g_242':r242}
    guardar_en_perfil({**{'score_sub2_1':s21,'score_sub2_2':s22,'score_sub2_3':s23,
        'score_sub2_4':s24,'score_b2':score_b2,'b2_finalizado':True},**items})
    if ec and ue:
        ok=guardar_en_supabase(items)
        if ok: st.success(f"✅ Bloque 2 guardado en la plataforma. Índice Gestión Proyectos: **{score_b2:.2f}/5**")
        else: st.warning(f"⚠️ Guardado localmente. Índice: **{score_b2:.2f}/5**")
    else: st.success(f"✅ Bloque 2 guardado. Índice Gestión Proyectos: **{score_b2:.2f}/5**")