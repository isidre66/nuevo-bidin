import streamlit as st
from asistentes import mostrar_melissa_cuestionario
import json, os

st.set_page_config(page_title="Estrategia de Innovación", layout="wide")

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
        res=sb.table("respuestas").select("item,valor").eq("empresa_codigo",ec).eq("usuario_email",ue).eq("bloque",4).execute()
        return {r["item"]:int(r["valor"]) for r in res.data} if res.data else {}
    except Exception: return {}
def guardar_en_supabase(items_dict):
    sb=get_supabase(); ec=st.session_state.get("empresa_codigo"); ue=st.session_state.get("usuario_email")
    if not sb or not ec or not ue: return False
    try:
        for item,valor in items_dict.items():
            sb.table("respuestas").upsert({"empresa_codigo":ec,"usuario_email":ue,"bloque":4,"item":item,"valor":float(valor)},
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

mostrar_melissa_cuestionario(bloque=4)
st.title("🎯 Bloque 4: Estrategia de Innovación")
if resp_prev: st.success("✅ Tienes respuestas guardadas. Puedes modificarlas y volver a guardar.")
elif st.session_state.get('b4_finalizado'): st.success("✅ Bloque completado. Puedes modificar y volver a guardar.")

st.header("4.1 Innovación Estratégica")
c1,c2=st.columns(2)
with c1:
    st.markdown("**4.1.1: Alineación innovación-estrategia**")
    aclaracion("411","Evalúe el nivel de integración de la innovación en la estrategia empresarial. 1=Nula alineación · 2=Relación puntual · 3=Innovación forma parte de la estrategia · 4=Las decisiones estratégicas incorporan la innovación · 5=Estrategia proactiva búsqueda nuevas oportunidades.")
    r411=st.select_slider("Alinear",options=[1,2,3,4,5],value=val('e_411'),label_visibility="collapsed")
    st.caption("1=Nula · 2=Puntual · 3=Parte estrategia · 4=Decisiones · 5=Proactiva")
with c2:
    st.markdown("**4.1.2: Liderazgo en innovación**")
    aclaracion("412","Evalúe el posicionamiento de su organización ante la innovación. 1=No se contempla · 2=Solo imitar consolidadas · 3=Puntual y poco diferenciada · 4=Innovación continuada · 5=Innovación sistemática y disruptiva.")
    r412=st.select_slider("Lider",options=[1,2,3,4,5],value=val('e_412'),label_visibility="collapsed")
    st.caption("1=No contempla · 2=Imitar · 3=Puntual · 4=Continuada · 5=Disruptiva")
c413,_=st.columns(2)
with c413:
    st.markdown("**4.1.3: Objetivos de innovación**")
    aclaracion("413","Valore la capacidad para definir objetivos claros de innovación e impactos esperados. 1=Nula · 2=Baja · 3=Moderada · 4=Elevada · 5=Definición exhaustiva de objetivos e impactos.")
    r413=st.select_slider("ObjInn",options=[1,2,3,4,5],value=val('e_413'),label_visibility="collapsed")
    st.caption("1=Nula · 2=Baja · 3=Moderada · 4=Elevada · 5=Exhaustiva")

st.header("4.2 Cultura de Innovación")
st.markdown(":orange[⚠️ Los dos primeros ítems tienen valoración inversa: 1 es la mejor opción y 5 la peor.]")
c3,c4=st.columns(2)
with c3:
    st.markdown("**4.2.1: Innovación incremental** _(valoración inversa)_")
    aclaracion("421","Evalúe si su empresa tiende a priorizar innovaciones incrementales de bajo impacto dirigidas a clientes ya existentes. Valoración INVERSA: 1=No, en absoluto (mejor) · 5=Siempre (peor).")
    r421=st.select_slider("Increm",options=[1,2,3,4,5],value=val('e_421'),label_visibility="collapsed")
    st.caption("⚠️ Inversa: 1=No (mejor) · 5=Siempre (peor)")
with c4:
    st.markdown("**4.2.2: Riesgo nuevos segmentos** _(valoración inversa)_")
    aclaracion("422","Evalúe el nivel de riesgo que su empresa asigna a expandirse a nuevos segmentos. Valoración INVERSA: 1=No, en absoluto (mejor) · 5=Riesgo inasumible (peor).")
    r422=st.select_slider("Riesgo",options=[1,2,3,4,5],value=val('e_422'),label_visibility="collapsed")
    st.caption("⚠️ Inversa: 1=Sin riesgo (mejor) · 5=Inasumible (peor)")
c423,_=st.columns(2)
with c423:
    st.markdown("**4.2.3: Conocimiento interno**")
    aclaracion("423","Valore si los mandos medios conocen adecuadamente los proyectos de innovación. 1=No · 2=Parcialmente · 3=Solo su área · 4=También otras áreas · 5=Conocimiento profundo de todos los proyectos.")
    r423=st.select_slider("ConInterno",options=[1,2,3,4,5],value=val('e_423'),label_visibility="collapsed")
    st.caption("1=No · 2=Parcial · 3=Su área · 4=Otras áreas · 5=Profundo")

st.header("4.3 Obstáculos a la Innovación")
st.markdown(":orange[⚠️ Ambos ítems tienen valoración inversa: 1 significa sin obstáculos (mejor) y 5 muchos obstáculos (peor).]")
c5,c6=st.columns(2)
with c5:
    st.markdown("**4.3.1: Obstáculos internos** _(valoración inversa)_")
    aclaracion("431","Describa la incidencia de obstáculos internos. Valoración INVERSA. 1=No hay obstáculos (mejor) · 2=Limitaciones tecnológicas puntuales · 3=+Organizativas y de gestión · 4=+Falta competencias · 5=Limitaciones financieras y falta de voluntad (peor).")
    r431=st.select_slider("Obst Int",options=[1,2,3,4,5],value=val('e_431'),label_visibility="collapsed")
    st.caption("⚠️ Inversa: 1=Sin obstáculos (mejor) · 5=Graves limitaciones (peor)")
with c6:
    st.markdown("**4.3.2: Obstáculos externos** _(valoración inversa)_")
    aclaracion("432","Describa la incidencia de obstáculos externos. Valoración INVERSA. 1=No hay obstáculos (mejor) · 2=Dificultad puntual partners · 3=Dificultad financiación · 4=Competencia intensa · 5=Elevada incertidumbre mercado (peor).")
    r432=st.select_slider("Obst Ext",options=[1,2,3,4,5],value=val('e_432'),label_visibility="collapsed")
    st.caption("⚠️ Inversa: 1=Sin obstáculos (mejor) · 5=Alta incertidumbre (peor)")

st.header("4.4 Innovación Abierta")
c7,c8=st.columns(2)
with c7:
    st.markdown("**4.4.1: Cultura colaborativa**")
    aclaracion("441","Evalúe su grado de cooperación en innovación con otros agentes. 1=Nulo · 2=Puntual · 3=Solo con otras empresas · 4=Además con centros tecnológicos y universidades · 5=Además con ecosistema emprendedor.")
    r441=st.select_slider("Colab Inn",options=[1,2,3,4,5],value=val('e_441'),label_visibility="collapsed")
    st.caption("1=Nulo · 2=Puntual · 3=Empresas · 4=+Centros tecnológicos · 5=+Ecosistema")
with c8:
    st.markdown("**4.4.2: Rendimiento de la cooperación**")
    aclaracion("442","Evalúe el rendimiento que obtiene con proyectos colaborativos. 1=Impacto nulo · 2=Algunas mejoras puntuales · 3=Contribuye a innovar · 4=Genera ventajas competitivas · 5=Liderazgo en innovación disruptiva.")
    r442=st.select_slider("RdCoop",options=[1,2,3,4,5],value=val('e_442'),label_visibility="collapsed")
    st.caption("1=Nulo · 2=Mejoras puntuales · 3=Innovaciones · 4=Ventajas · 5=Liderazgo")

st.header("4.5 Fomento de la Creatividad")
c9,c10=st.columns(2)
with c9:
    st.markdown("**4.5.1: Fomento de nuevas ideas**")
    aclaracion("451","Evalúe si su empresa fomenta la creatividad y proponer nuevas ideas. 1=No · 2=Poco y sin incentivos · 3=Con incentivos puntuales · 4=Se fomenta de forma sistemática · 5=La creatividad es un pilar fundamental de la cultura de la empresa.")
    r451=st.select_slider("Ideas",options=[1,2,3,4,5],value=val('e_451'),label_visibility="collapsed")
    st.caption("1=No · 2=Sin incentivos · 3=Incentivos puntuales · 4=Sistemático · 5=Pilar cultural")
with c10:
    st.markdown("**4.5.2: Evaluación de ideas**")
    aclaracion("452","Valore la capacidad para filtrar y evaluar ideas de innovación. 1=No, en absoluto · 2=Puntual · 3=Con cierta frecuencia · 4=Evaluación sistemática · 5=Elevada efectividad nuevas ideas.")
    r452=st.select_slider("EvalIdeas",options=[1,2,3,4,5],value=val('e_452'),label_visibility="collapsed")
    st.caption("1=No · 2=Puntual · 3=Frecuente · 4=Sistemática · 5=Alta efectividad")

st.divider()
if st.button("💾 Guardar Bloque 4", use_container_width=True, type="primary"):
    s41=(r411+r412+r413)/3; s42=(r421+r422+r423)/3; s43=(r431+r432)/2; s44=(r441+r442)/2; s45=(r451+r452)/2
    score_b4=(s41*0.25)+(s42*0.25)+(s43*0.20)+(s44*0.20)+(s45*0.10)
    st.session_state.update({'score_sub4_1':s41,'score_sub4_2':s42,'score_sub4_3':s43,
        'score_sub4_4':s44,'score_sub4_5':s45,'score_b4':score_b4,'b4_finalizado':True})
    items={'e_411':r411,'e_412':r412,'e_413':r413,'e_421':r421,'e_422':r422,'e_423':r423,
           'e_431':r431,'e_432':r432,'e_441':r441,'e_442':r442,'e_451':r451,'e_452':r452}
    guardar_en_perfil({**{'score_sub4_1':s41,'score_sub4_2':s42,'score_sub4_3':s43,
        'score_sub4_4':s44,'score_sub4_5':s45,'score_b4':score_b4,'b4_finalizado':True},**items})
    if ec and ue:
        ok=guardar_en_supabase(items)
        if ok: st.success(f"✅ Bloque 4 guardado en la plataforma. Índice Estrategia Innovación: **{score_b4:.2f}/5**")
        else: st.warning(f"⚠️ Guardado localmente. Índice: **{score_b4:.2f}/5**")
    else: st.success(f"✅ Bloque 4 guardado. Índice Estrategia Innovación: **{score_b4:.2f}/5**")