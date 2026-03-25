import streamlit as st
import json, os

st.set_page_config(page_title="Desarrollo de Productos", layout="wide")

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
        res = sb.table("respuestas").select("item,valor").eq("empresa_codigo",ec).eq("usuario_email",ue).eq("bloque",3).execute()
        return {r["item"]: int(r["valor"]) for r in res.data} if res.data else {}
    except Exception: return {}

def guardar_en_supabase(items_dict):
    sb = get_supabase()
    ec = st.session_state.get("empresa_codigo"); ue = st.session_state.get("usuario_email")
    if not sb or not ec or not ue: return False
    try:
        for item, valor in items_dict.items():
            sb.table("respuestas").upsert({"empresa_codigo":ec,"usuario_email":ue,"bloque":3,"item":item,"valor":float(valor)},
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

def val(key, default=1): return resp_prev.get(key, int(perfil.get(key, default)))

def ficha(codigo, titulo, explicacion, mapa_opciones, clave, val_guardado):
    st.markdown(f"""<div style='background-color:#eff6ff;padding:12px;border-radius:8px;
        border-left:5px solid #3b82f6;margin-top:15px;'>
        <strong style='color:#1e40af;'>{codigo} - {titulo}</strong><br>
        <span style='color:#475569;font-size:0.85rem;'>{explicacion}</span></div>""", unsafe_allow_html=True)
    valor = st.select_slider(f"Selección {clave}", options=[1,2,3,4,5], value=val_guardado, label_visibility="collapsed")
    st.markdown(f"**Nivel {valor}:** *{mapa_opciones.get(valor,'')}*")
    return valor

st.title("🚀 Bloque 3: Desarrollo de Nuevos Productos")
if resp_prev: st.success("✅ Tienes respuestas guardadas. Puedes modificarlas y volver a guardar.")
elif st.session_state.get('b3_finalizado'): st.success("✅ Bloque completado. Puedes modificar y volver a guardar.")

st.header("3.1 Estrategia de Desarrollo")
c1,c2 = st.columns(2)
with c1:
    r311 = ficha("3.1.1","Estr. Nuevos Prod.","Estrategia formal para desarrollo de nuevos productos",
        {1:"Inexistente",2:"Informal y reactiva",3:"Planificación básica",4:"Estrategia definida",5:"Estrategia sistemática y proactiva"},"311",val('p_311'))
with c2:
    r312 = ficha("3.1.2","Recursos","Recursos asignados al desarrollo de nuevos productos",
        {1:"Sin recursos específicos",2:"Recursos puntuales",3:"Equipo parcial",4:"Equipo dedicado",5:"Centro de innovación propio"},"312",val('p_312'))

st.header("3.2 Oportunidades de Mercado")
c3,c4 = st.columns(2)
with c3:
    r321 = ficha("3.2.1","Identif. Oport.","Identificación sistemática de oportunidades",
        {1:"No se realiza",2:"Puntual e informal",3:"Análisis periódico",4:"Proceso estructurado",5:"Inteligencia de mercado continua"},"321",val('p_321'))
    r323 = ficha("3.2.3","Crec. Productos","Crecimiento en cartera de productos",
        {1:"Sin crecimiento",2:"Sustitución puntual",3:"Ampliación moderada",4:"Crecimiento sostenido",5:"Expansión continua y diversificada"},"323",val('p_323'))
with c4:
    r322 = ficha("3.2.2","Tam. Innovación","Tamaño e impacto de las innovaciones",
        {1:"Mejoras mínimas",2:"Cambios incrementales",3:"Innovaciones moderadas",4:"Innovaciones relevantes",5:"Innovaciones disruptivas"},"322",val('p_322'))
    r324 = ficha("3.2.4","Rent. Productos","Rentabilidad de nuevos productos",
        {1:"Pérdidas",2:"Punto de equilibrio",3:"Rentabilidad básica",4:"Alta rentabilidad",5:"Liderazgo en márgenes"},"324",val('p_324'))

st.header("3.3 Recepción de Nuevos Productos")
c5,c6 = st.columns(2)
with c5:
    r331 = ficha("3.3.1","Probar","Disposición del cliente a probar nuevos productos",
        {1:"Muy baja",2:"Baja",3:"Moderada",4:"Alta",5:"Muy alta"},"331",val('p_331'))
    r333 = ficha("3.3.3","Valor","Percepción de valor por el cliente",
        {1:"No percibe valor",2:"Valor bajo",3:"Valor moderado",4:"Valor alto",5:"Valor muy alto"},"333",val('p_333'))
with c6:
    r332 = ficha("3.3.2","Pagar","Disposición del cliente a pagar precio premium",
        {1:"Muy baja",2:"Baja",3:"Moderada",4:"Alta",5:"Muy alta"},"332",val('p_332'))

st.header("3.4 Orientación al Cliente")
c7,c8 = st.columns(2)
with c7:
    r341 = ficha("3.4.1","Diseño","Implicación del cliente en el diseño",
        {1:"Nula",2:"Puntual",3:"En algunos proyectos",4:"Habitual",5:"Co-creación sistemática"},"341",val('p_341'))
with c8:
    r342 = ficha("3.4.2","Interacción","Interacción y feedback continuo con clientes",
        {1:"Inexistente",2:"Puntual",3:"Periódica",4:"Frecuente",5:"Continua y digitalizada"},"342",val('p_342'))

st.header("3.5 Impacto de Nuevos Productos")
c9,c10 = st.columns(2)
with c9:
    r351 = ficha("3.5.1","Ecofinanc.","Impacto económico-financiero de los nuevos productos",
        {1:"Negativo",2:"Neutro",3:"Moderado positivo",4:"Alto positivo",5:"Transformador"},"351",val('p_351'))
with c10:
    r352 = ficha("3.5.2","Viab. Comercial","Viabilidad comercial de los nuevos productos",
        {1:"Muy baja",2:"Baja",3:"Moderada",4:"Alta",5:"Muy alta"},"352",val('p_352'))

st.divider()
if st.button("💾 Guardar Bloque 3", use_container_width=True, type="primary"):
    s31=(r311+r312)/2; s32=(r321+r322+r323+r324)/4; s33=(r331+r332+r333)/3
    s34=(r341+r342)/2; s35=(r351+r352)/2
    score_b3=(s31*0.25)+(s32*0.20)+(s33*0.15)+(s34*0.15)+(s35*0.25)
    st.session_state.update({'score_sub3_1':s31,'score_sub3_2':s32,'score_sub3_3':s33,
        'score_sub3_4':s34,'score_sub3_5':s35,'score_b3':score_b3,'b3_finalizado':True})
    items = {'p_311':r311,'p_312':r312,'p_321':r321,'p_322':r322,'p_323':r323,'p_324':r324,
             'p_331':r331,'p_332':r332,'p_333':r333,'p_341':r341,'p_342':r342,'p_351':r351,'p_352':r352}
    guardar_en_perfil({**{'score_sub3_1':s31,'score_sub3_2':s32,'score_sub3_3':s33,
        'score_sub3_4':s34,'score_sub3_5':s35,'score_b3':score_b3,'b3_finalizado':True}, **items})
    if ec and ue:
        ok = guardar_en_supabase(items)
        if ok: st.success(f"✅ Bloque 3 guardado en la plataforma. Índice Desarrollo Productos: **{score_b3:.2f}/5**")
        else: st.warning(f"⚠️ Guardado localmente. Índice: **{score_b3:.2f}/5**")
    else:
        st.success(f"✅ Bloque 3 guardado. Índice Desarrollo Productos: **{score_b3:.2f}/5**")