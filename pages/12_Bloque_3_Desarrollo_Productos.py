import streamlit as st
import json, os

st.set_page_config(page_title="Desarrollo de Productos", layout="wide")

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
        res=sb.table("respuestas").select("item,valor").eq("empresa_codigo",ec).eq("usuario_email",ue).eq("bloque",3).execute()
        return {r["item"]:int(r["valor"]) for r in res.data} if res.data else {}
    except Exception: return {}
def guardar_en_supabase(items_dict):
    sb=get_supabase(); ec=st.session_state.get("empresa_codigo"); ue=st.session_state.get("usuario_email")
    if not sb or not ec or not ue: return False
    try:
        for item,valor in items_dict.items():
            sb.table("respuestas").upsert({"empresa_codigo":ec,"usuario_email":ue,"bloque":3,"item":item,"valor":float(valor)},
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

st.title("🚀 Bloque 3: Desarrollo de Nuevos Productos")
if resp_prev: st.success("✅ Tienes respuestas guardadas. Puedes modificarlas y volver a guardar.")
elif st.session_state.get('b3_finalizado'): st.success("✅ Bloque completado. Puedes modificar y volver a guardar.")

st.header("3.1 Estrategia de Desarrollo")
c1,c2=st.columns(2)
with c1:
    st.markdown("**3.1.1: Estrategia de desarrollo de nuevos productos**")
    aclaracion("311","Valore la estrategia y proceso de desarrollo de nuevos productos/servicios. 1=Inexistente · 2=Puntual e informal · 3=Solo ante oportunidades claras · 4=Se analiza demanda y necesidades clientes · 5=Enfoque multidisciplinar: I+D, marketing, producción.")
    r311=st.select_slider("Estr. nuevos prod.",options=[1,2,3,4,5],value=val('p_311'),label_visibility="collapsed")
    st.caption("1=Inexistente · 2=Informal · 3=Oportunidades · 4=Análisis demanda · 5=Multidisciplinar")
with c2:
    st.markdown("**3.1.2: Recursos para el desarrollo**")
    aclaracion("312","Evalúe cómo gestiona su empresa los recursos para el desarrollo de nuevos productos. 1=No se asignan · 2=Asignación puntual informal · 3=Recursos internos I+D · 4=Equipos integrados multidisciplinares · 5=Además, colaboración con agentes externos.")
    r312=st.select_slider("Recursos nuevos prod.",options=[1,2,3,4,5],value=val('p_312'),label_visibility="collapsed")
    st.caption("1=Sin recursos · 2=Puntual · 3=I+D interno · 4=Multidisciplinar · 5=+Externo")

st.header("3.2 Oportunidades de Mercado")
c3,c4=st.columns(2)
with c3:
    st.markdown("**3.2.1: Identificación de oportunidades**")
    aclaracion("321","Valore en qué medida su empresa identifica oportunidades desatendidas por los competidores. 1=No, nunca · 2=Muy rara vez · 3=Algunas veces · 4=Bastantes veces · 5=Con mucha frecuencia, habitualmente.")
    r321=st.select_slider("Ident. oportunidades",options=[1,2,3,4,5],value=val('p_321'),label_visibility="collapsed")
    st.caption("1=Nunca · 2=Rara vez · 3=Algunas veces · 4=Bastantes · 5=Habitualmente")

    st.markdown("**3.2.3: Potencial de crecimiento**")
    aclaracion("323","Evalúe el potencial de ventas y crecimiento de los nuevos productos desarrollados en los últimos años. 1=Nulo · 2=Bajo · 3=Moderado · 4=Alto · 5=Muy alto.")
    r323=st.select_slider("Crec. productos",options=[1,2,3,4,5],value=val('p_323'),label_visibility="collapsed")
    st.caption("1=Nulo · 2=Bajo · 3=Moderado · 4=Alto · 5=Muy alto")
with c4:
    st.markdown("**3.2.2: Tamaño del mercado**")
    aclaracion("322","Evalúe el tamaño del mercado de destino de sus innovaciones recientes. 1=Nulo, marginal · 2=Pequeño · 3=Mediano · 4=Grande · 5=Muy grande.")
    r322=st.select_slider("Tam. innovación",options=[1,2,3,4,5],value=val('p_322'),label_visibility="collapsed")
    st.caption("1=Marginal · 2=Pequeño · 3=Mediano · 4=Grande · 5=Muy grande")

    st.markdown("**3.2.4: Rentabilidad de nuevos productos**")
    aclaracion("324","Valore la rentabilidad obtenida por nuevos productos lanzados en los últimos 3-5 años. 1=Negativa o nula · 2=Positiva pero inferior al promedio · 3=Similar al promedio · 4=Superior al promedio · 5=Muy superior al promedio.")
    r324=st.select_slider("Rent. productos",options=[1,2,3,4,5],value=val('p_324'),label_visibility="collapsed")
    st.caption("1=Negativa · 2=Inferior promedio · 3=Similar · 4=Superior · 5=Muy superior")

st.header("3.3 Receptividad y Valor")
c5,c6=st.columns(2)
with c5:
    st.markdown("**3.3.1: Predisposición a probar**")
    aclaracion("331","Valore la predisposición de clientes potenciales a probar sus nuevos productos. 1=Negativa o nula · 2=Baja · 3=Media · 4=Alta · 5=Muy alta.")
    r331=st.select_slider("Probar",options=[1,2,3,4,5],value=val('p_331'),label_visibility="collapsed")
    st.caption("1=Negativa · 2=Baja · 3=Media · 4=Alta · 5=Muy alta")

    st.markdown("**3.3.3: Diferenciación y valor**")
    aclaracion("333","Evalúe el nivel de diferenciación de sus nuevos productos respecto a la competencia. 1=Nulo · 2=Bajo · 3=Moderado · 4=Alto · 5=Muy alto.")
    r333=st.select_slider("Valor productos",options=[1,2,3,4,5],value=val('p_333'),label_visibility="collapsed")
    st.caption("1=Nulo · 2=Bajo · 3=Moderado · 4=Alto · 5=Muy alto")
with c6:
    st.markdown("**3.3.2: Predisposición a pagar**")
    aclaracion("332","Evalúe la predisposición de clientes a pagar los precios establecidos por sus nuevos productos. 1=Negativa o nula · 2=Baja · 3=Media · 4=Alta · 5=Muy alta.")
    r332=st.select_slider("Pagar",options=[1,2,3,4,5],value=val('p_332'),label_visibility="collapsed")
    st.caption("1=Negativa · 2=Baja · 3=Media · 4=Alta · 5=Muy alta")

st.header("3.4 Interacción con Clientes")
c7,c8=st.columns(2)
with c7:
    st.markdown("**3.4.1: Herramientas de diseño**")
    aclaracion("341","Evalúe el uso de técnicas de design thinking, rapid prototyping y similares para el diseño y validación de nuevos productos. 1=No conocido · 2=Programado en futuro próximo · 3=Puntual · 4=Considerable · 5=Total.")
    r341=st.select_slider("Diseño productos",options=[1,2,3,4,5],value=val('p_341'),label_visibility="collapsed")
    st.caption("1=Desconocido · 2=Previsto · 3=Puntual · 4=Considerable · 5=Total")
with c8:
    st.markdown("**3.4.2: Interacción con clientes**")
    aclaracion("342","Valore la interacción con clientes potenciales durante el desarrollo para ajustarse a las expectativas del mercado. 1=No, en absoluto · 2=Puntual y parcial · 3=En algunos proyectos · 4=Con frecuencia · 5=De forma continua y sistemática.")
    r342=st.select_slider("Interacción",options=[1,2,3,4,5],value=val('p_342'),label_visibility="collapsed")
    st.caption("1=No · 2=Puntual · 3=Algunos proyectos · 4=Frecuente · 5=Continua")

st.header("3.5 Viabilidad e Impacto")
c9,c10=st.columns(2)
with c9:
    st.markdown("**3.5.1: Análisis económico-financiero**")
    aclaracion("351","Evalúe la realización de análisis económico-financiero temprano y de rentabilidad potencial en el desarrollo de nuevos productos. 1=No, nunca · 2=Puntualmente · 3=En algunos proyectos · 4=Con frecuencia · 5=De forma continua y sistemática.")
    r351=st.select_slider("Eco-financiero",options=[1,2,3,4,5],value=val('p_351'),label_visibility="collapsed")
    st.caption("1=Nunca · 2=Puntual · 3=Algunos · 4=Frecuente · 5=Siempre")
with c10:
    st.markdown("**3.5.2: Análisis de viabilidad comercial**")
    aclaracion("352","Valore el uso de herramientas de análisis de viabilidad como Business Model Canvas, Validation Board y similares. 1=No conocido · 2=Programado · 3=Puntual · 4=Considerable · 5=Total.")
    r352=st.select_slider("Viab. comercial",options=[1,2,3,4,5],value=val('p_352'),label_visibility="collapsed")
    st.caption("1=Desconocido · 2=Previsto · 3=Puntual · 4=Considerable · 5=Total")

st.divider()
if st.button("💾 Guardar Bloque 3", use_container_width=True, type="primary"):
    s31=(r311+r312)/2; s32=(r321+r322+r323+r324)/4; s33=(r331+r332+r333)/3
    s34=(r341+r342)/2; s35=(r351+r352)/2
    score_b3=(s31*0.25)+(s32*0.20)+(s33*0.15)+(s34*0.15)+(s35*0.25)
    st.session_state.update({'score_sub3_1':s31,'score_sub3_2':s32,'score_sub3_3':s33,
        'score_sub3_4':s34,'score_sub3_5':s35,'score_b3':score_b3,'b3_finalizado':True})
    items={'p_311':r311,'p_312':r312,'p_321':r321,'p_322':r322,'p_323':r323,'p_324':r324,
           'p_331':r331,'p_332':r332,'p_333':r333,'p_341':r341,'p_342':r342,'p_351':r351,'p_352':r352}
    guardar_en_perfil({**{'score_sub3_1':s31,'score_sub3_2':s32,'score_sub3_3':s33,
        'score_sub3_4':s34,'score_sub3_5':s35,'score_b3':score_b3,'b3_finalizado':True},**items})
    if ec and ue:
        ok=guardar_en_supabase(items)
        if ok: st.success(f"✅ Bloque 3 guardado en la plataforma. Índice Desarrollo Productos: **{score_b3:.2f}/5**")
        else: st.warning(f"⚠️ Guardado localmente. Índice: **{score_b3:.2f}/5**")
    else: st.success(f"✅ Bloque 3 guardado. Índice Desarrollo Productos: **{score_b3:.2f}/5**")