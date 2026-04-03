import streamlit as st
from asistentes import mostrar_melissa_cuestionario
import json, os

st.set_page_config(page_title="Bloque 1: I+D+i", layout="wide")

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
        res = sb.table("respuestas").select("item,valor").eq("empresa_codigo",ec).eq("usuario_email",ue).eq("bloque",1).execute()
        return {r["item"]: int(r["valor"]) for r in res.data} if res.data else {}
    except Exception: return {}

def guardar_en_supabase(items_dict):
    sb = get_supabase()
    ec = st.session_state.get("empresa_codigo"); ue = st.session_state.get("usuario_email")
    if not sb or not ec or not ue: return False
    try:
        for item, valor in items_dict.items():
            sb.table("respuestas").upsert({"empresa_codigo":ec,"usuario_email":ue,"bloque":1,"item":item,"valor":float(valor)},
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
    if resp_prev: return int(resp_prev.get(key, default))
    if ec and ue: return default
    return int(perfil.get(key, default))

# ── Helper para mostrar aclaración ───────────────────────────────────────────
def aclaracion(key, texto):
    if st.button(f"ℹ️ Ver aclaración", key=f"acl_{key}", use_container_width=False):
        st.session_state[f"show_acl_{key}"] = not st.session_state.get(f"show_acl_{key}", False)
    if st.session_state.get(f"show_acl_{key}"):
        st.info(texto)

# ── FORMULARIO ────────────────────────────────────────────────────────────────
mostrar_melissa_cuestionario(bloque=1
st.title("BLOQUE 1: ACTIVIDADES DE I+D+i")
if resp_prev: st.success("✅ Tienes respuestas guardadas. Puedes modificarlas y volver a guardar.")
elif st.session_state.get('b1_finalizado'): st.success("✅ Bloque completado. Puedes modificar y volver a guardar.")

st.subheader("1.1 Departamento I+D")

st.markdown("**1.1.1: Recursos técnicos dedicados a I+D**")
aclaracion("111", "Valore el nivel de recursos técnicos dedicados a actividades de investigación y desarrollo en su organización (laboratorios, equipos especializados, software técnico, etc.).")
r111 = st.select_slider("Recursos técnicos I+D", options=[1,2,3,4,5], value=val('it_111'), label_visibility="collapsed")
st.caption(f"1=Nulo · 2=Bajo · 3=Medio · 4=Alto · 5=Muy alto")

st.markdown("**1.1.2: Recursos humanos dedicados a I+D**")
aclaracion("112", "Valore los recursos humanos dedicados a actividades de I+D. 1=Ningún personal propio · 2=Una persona a tiempo parcial · 3=1-2 empleados a tiempo completo · 4=Equipo estable 3-5 personas · 5=Departamento I+D consolidado con más de 5 personas o más del 5% de la plantilla.")
r112 = st.select_slider("Recursos humanos I+D", options=[1,2,3,4,5], value=val('it_112'), label_visibility="collapsed")
st.caption(f"1=Ningún personal · 2=Parcial · 3=1-2 completo · 4=Equipo 3-5 · 5=Dpto. consolidado")

st.subheader("1.2 Presupuesto I+D")

st.markdown("**1.2.1: Presupuesto específico para I+D**")
aclaracion("121", "Evalúe el nivel de asignación presupuestaria específica para actividades de I+D. 1=No se asigna · 2=Gastos puntuales · 3=Presupuesto parcial no sistemático · 4=Presupuesto anual global · 5=Presupuesto anual desglosado con indicadores de resultados esperados.")
r121 = st.select_slider("Presupuesto I+D", options=[1,2,3,4,5], value=val('it_121'), label_visibility="collapsed")
st.caption(f"1=No se asigna · 2=Puntual · 3=Parcial · 4=Anual global · 5=Anual desglosado")

st.markdown("**1.2.2: I+D subvencionado**")
aclaracion("122", "Indique el porcentaje de financiación para actividades de I+D obtenido mediante subvenciones públicas y becas. 1=0-10% · 2=10-20% · 3=20-30% · 4=30-50% · 5=Más del 50%.")
r122 = st.select_slider("I+D subvencionado", options=[1,2,3,4,5], value=val('it_122'), label_visibility="collapsed")
st.caption(f"1=0-10% · 2=10-20% · 3=20-30% · 4=30-50% · 5=>50%")

st.markdown("**1.2.3: Participación en proyectos con financiación pública**")
aclaracion("123", "Evalúe el nivel de participación en proyectos de I+D con financiación pública. 1=No · 2=Puntual ámbito regional · 3=Puntual nacional-internacional · 4=Continua nacional-internacional · 5=Liderazgo en proyectos internacionales.")
r123 = st.select_slider("Financiación pública", options=[1,2,3,4,5], value=val('it_123'), label_visibility="collapsed")
st.caption(f"1=No · 2=Regional puntual · 3=Nacional puntual · 4=Continua · 5=Liderazgo internacional")

st.subheader("1.3 Gasto en Innovación")

st.markdown("**1.3.1: Gasto estimado anual en innovación sobre ventas**")
aclaracion("131", "Indique el porcentaje del gasto en innovación respecto a las ventas de los últimos 3 años. 1=0% · 2=Menos del 2% · 3=3-5% · 4=5-10% · 5=Más del 10%.")
r131 = st.select_slider("Gasto innovación/ventas", options=[1,2,3,4,5], value=val('it_131'), label_visibility="collapsed")
st.caption(f"1=0% · 2=<2% · 3=3-5% · 4=5-10% · 5=>10%")

st.markdown("**1.3.2: Evolución futura del gasto en innovación**")
aclaracion("132", "Indique la evolución prevista de sus gastos en innovación para los próximos años. 1=Reducción · 2=Mantenimiento · 3=Crecimiento escaso · 4=Crecimiento amplio · 5=Gran crecimiento.")
r132 = st.select_slider("Evolución futura gasto", options=[1,2,3,4,5], value=val('it_132'), label_visibility="collapsed")
st.caption(f"1=Reducción · 2=Mantenimiento · 3=Crecimiento escaso · 4=Amplio · 5=Gran crecimiento")

st.divider()

if st.button("💾 GUARDAR BLOQUE 1", use_container_width=True, type="primary"):
    s1=(r111+r112)/2; s2=(r121+r122+r123)/3; s3=(r131+r132)/2
    score_b1=(s1*0.2)+(s2*0.4)+(s3*0.4)
    st.session_state.update({'score_sub1_1':s1,'score_sub1_2':s2,'score_sub1_3':s3,
        'score_b1':score_b1,'b1_finalizado':True})
    items = {'it_111':r111,'it_112':r112,'it_121':r121,'it_122':r122,'it_123':r123,'it_131':r131,'it_132':r132}
    guardar_en_perfil({**{'score_sub1_1':s1,'score_sub1_2':s2,'score_sub1_3':s3,
        'score_b1':score_b1,'b1_finalizado':True}, **items})
    if ec and ue:
        ok = guardar_en_supabase(items)
        if ok: st.success(f"✅ Bloque 1 guardado en la plataforma. Índice I+D+i: **{score_b1:.2f}/5**")
        else: st.warning(f"⚠️ Guardado localmente. Índice: **{score_b1:.2f}/5**")
    else:
        st.success(f"✅ Bloque 1 guardado. Índice I+D+i: **{score_b1:.2f}/5**")
    st.info("Ahora puedes ir al siguiente bloque del cuestionario.")