import streamlit as st
from asistentes import mostrar_melissa_cuestionario
import json, os

st.set_page_config(page_title="Desempeño e Impacto", layout="wide")

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
        res=sb.table("respuestas").select("item,valor").eq("empresa_codigo",ec).eq("usuario_email",ue).eq("bloque",5).execute()
        return {r["item"]:int(r["valor"]) for r in res.data} if res.data else {}
    except Exception: return {}
def guardar_en_supabase(items_dict):
    sb=get_supabase(); ec=st.session_state.get("empresa_codigo"); ue=st.session_state.get("usuario_email")
    if not sb or not ec or not ue: return False
    try:
        for item,valor in items_dict.items():
            sb.table("respuestas").upsert({"empresa_codigo":ec,"usuario_email":ue,"bloque":5,"item":item,"valor":float(valor)},
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

opt={1:"Nulo, negativo",2:"Escaso",3:"Moderado",4:"Alto",5:"Muy alto"}

mostrar_melissa_cuestionario(bloque=5)
st.title("📈 Bloque 5: Desempeño e Impacto de la Innovación")
if resp_prev: st.success("✅ Tienes respuestas guardadas. Puedes modificarlas y volver a guardar.")
elif st.session_state.get('b5_finalizado'): st.success("✅ Bloque completado. Puedes modificar y volver a guardar.")

st.header("5.1 Impacto Estimado de la Innovación")
st.subheader("📦 Innovación en Producto")
c1,c2=st.columns(2)
with c1:
    st.markdown("**5.1.1.1: Impacto en ventas**")
    aclaracion("5111","Evalúe el impacto de las innovaciones generadas en los últimos 5 años en la tasa de crecimiento en ventas. 1=Nulo o negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto.")
    r5111=st.select_slider("Inn Ventas",options=[1,2,3,4,5],value=val('d_5111'),label_visibility="collapsed")
    st.caption("1=Nulo/negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto")

    st.markdown("**5.1.1.3: Impacto en rentabilidad**")
    aclaracion("5113","Valore el impacto de las innovaciones en la rentabilidad de la compañía. 1=Nulo o negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto.")
    r5113=st.select_slider("Inn Rent",options=[1,2,3,4,5],value=val('d_5113'),label_visibility="collapsed")
    st.caption("1=Nulo/negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto")
with c2:
    st.markdown("**5.1.1.2: Impacto en empleo**")
    aclaracion("5112","Evalúe el impacto de las innovaciones en el empleo de la compañía. 1=Nulo o negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto.")
    r5112=st.select_slider("Inn Empl",options=[1,2,3,4,5],value=val('d_5112'),label_visibility="collapsed")
    st.caption("1=Nulo/negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto")

    st.markdown("**5.1.1.4: Impacto en internacionalización**")
    aclaracion("5114","Evalúe el impacto de las innovaciones en la internacionalización y apertura de nuevos mercados geográficos. 1=Nulo o negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto.")
    r5114=st.select_slider("Inn Internac",options=[1,2,3,4,5],value=val('d_5114'),label_visibility="collapsed")
    st.caption("1=Nulo/negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto")

st.subheader("⚙️ Innovación en Proceso")
c3,c4=st.columns(2)
with c3:
    st.markdown("**5.1.2.1: Impacto en costes y productividad**")
    aclaracion("5121","Valore el impacto de las innovaciones en reducción de costes y aumento de productividad. 1=Nulo o negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto.")
    r5121=st.select_slider("Inn Costes",options=[1,2,3,4,5],value=val('d_5121'),label_visibility="collapsed")
    st.caption("1=Nulo/negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto")

    st.markdown("**5.1.2.3: Impacto en métodos productivos**")
    aclaracion("5123","Valore el impacto en la incorporación de nuevos métodos de fabricación o prestación de servicios más eficientes. 1=Nulo o negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto.")
    r5123=st.select_slider("Inn Metod",options=[1,2,3,4,5],value=val('d_5123'),label_visibility="collapsed")
    st.caption("1=Nulo/negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto")
with c4:
    st.markdown("**5.1.2.2: Impacto en eficiencia energética**")
    aclaracion("5122","Evalúe el impacto en elevar la eficiencia en consumo energético y la sostenibilidad medioambiental. 1=Nulo o negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto.")
    r5122=st.select_slider("Inn Sost",options=[1,2,3,4,5],value=val('d_5122'),label_visibility="collapsed")
    st.caption("1=Nulo/negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto")

st.subheader("🏢 Innovación Organizativa")
c5,c6=st.columns(2)
with c5:
    st.markdown("**5.1.3.1: Impacto en recursos humanos**")
    aclaracion("5131","Evalúe el impacto de las innovaciones en el nivel de motivación y satisfacción del personal. 1=Nulo o negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto.")
    r5131=st.select_slider("Inn RH",options=[1,2,3,4,5],value=val('d_5131'),label_visibility="collapsed")
    st.caption("1=Nulo/negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto")
with c6:
    st.markdown("**5.1.3.2: Impacto en administración**")
    aclaracion("5132","Valore el impacto en el nivel de eficiencia administrativa y de gestión, optimizando tiempos y ahorrando costes. 1=Nulo o negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto.")
    r5132=st.select_slider("Inn Admin",options=[1,2,3,4,5],value=val('d_5132'),label_visibility="collapsed")
    st.caption("1=Nulo/negativo · 2=Escaso · 3=Moderado · 4=Alto · 5=Muy alto")

st.header("5.2 Impacto Efectivo de la Innovación")
c7,c8=st.columns(2)
with c7:
    st.markdown("**5.2.1: Número de nuevos productos**")
    aclaracion("521","Indique el número de nuevos productos o servicios lanzados en los últimos 5 años. 1=Ninguno · 2=1-2 · 3=3-5 · 4=Más de 5 · 5=Lanzamiento de nuevas líneas de negocio.")
    r521=st.select_slider("Num Nprod",options=[1,2,3,4,5],value=val('d_521'),label_visibility="collapsed")
    st.caption("1=Ninguno · 2=1-2 · 3=3-5 · 4=>5 · 5=Nuevas líneas negocio")
with c8:
    st.markdown("**5.2.2: % ventas de productos innovadores**")
    aclaracion("522","Indique el porcentaje de ventas de productos/servicios innovadores lanzados en los últimos 5 años. 1=0% · 2=Menos del 10% · 3=10-25% · 4=26-50% · 5=Más del 50%.")
    r522=st.select_slider("Porc Vtas",options=[1,2,3,4,5],value=val('d_522'),label_visibility="collapsed")
    st.caption("1=0% · 2=<10% · 3=10-25% · 4=26-50% · 5=>50%")
c9,_=st.columns(2)
with c9:
    st.markdown("**5.2.3: % productos innovadores con éxito**")
    aclaracion("523","Indique el porcentaje de nuevos productos lanzados en los últimos 5 años que han alcanzado o superado las expectativas previstas. 1=0-15% · 2=10-30% · 3=30-50% · 4=50-70% · 5=Más del 70%.")
    r523=st.select_slider("Inn Exito",options=[1,2,3,4,5],value=val('d_523'),label_visibility="collapsed")
    st.caption("1=0-15% · 2=10-30% · 3=30-50% · 4=50-70% · 5=>70%")

st.divider()
if st.button("💾 Guardar Bloque 5", use_container_width=True, type="primary"):
    s511=(r5111+r5112+r5113+r5114)/4; s512=(r5121+r5122+r5123)/3; s513=(r5131+r5132)/2
    s51=(s511*0.40)+(s512*0.35)+(s513*0.25); s52=(r521+r522+r523)/3
    score_b5=(s51*0.40)+(s52*0.60)
    st.session_state.update({'score_sub5_11':s511,'score_sub5_12':s512,'score_sub5_13':s513,
        'score_sub5_1':s51,'score_sub5_2':s52,'score_b5':score_b5,'b5_finalizado':True})
    items={'d_5111':r5111,'d_5112':r5112,'d_5113':r5113,'d_5114':r5114,
           'd_5121':r5121,'d_5122':r5122,'d_5123':r5123,
           'd_5131':r5131,'d_5132':r5132,'d_521':r521,'d_522':r522,'d_523':r523}
    guardar_en_perfil({**{'score_sub5_11':s511,'score_sub5_12':s512,'score_sub5_13':s513,
        'score_sub5_1':s51,'score_sub5_2':s52,'score_b5':score_b5,'b5_finalizado':True},**items})
    if ec and ue:
        ok=guardar_en_supabase(items)
        if ok: st.success(f"✅ Bloque 5 guardado en la plataforma. Índice Desempeño Innovación: **{score_b5:.2f}/5**")
        else: st.warning(f"⚠️ Guardado localmente. Índice: **{score_b5:.2f}/5**")
    else: st.success(f"✅ Bloque 5 guardado. Índice Desempeño Innovación: **{score_b5:.2f}/5**")