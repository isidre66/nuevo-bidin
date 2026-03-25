import streamlit as st
import json, os

st.set_page_config(page_title="Bloque 1: I+D+i", layout="wide")

# ── Conexión Supabase ─────────────────────────────────────────────────────────
def get_supabase():
    try:
        from supabase import create_client
        url = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL",""))
        key = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY",""))
        if url and key:
            return create_client(url, key)
    except Exception:
        pass
    return None

# ── Archivo de perfil local (fallback) ───────────────────────────────────────
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

# ── Cargar respuestas previas de Supabase ─────────────────────────────────────
def cargar_respuestas_supabase():
    sb = get_supabase()
    empresa_codigo = st.session_state.get('empresa_codigo')
    usuario_email  = st.session_state.get('usuario_email')
    if not sb or not empresa_codigo or not usuario_email:
        return {}
    try:
        res = sb.table('respuestas').select('item,valor')\
            .eq('empresa_codigo', empresa_codigo)\
            .eq('usuario_email', usuario_email)\
            .eq('bloque', 1).execute()
        return {r['item']: r['valor'] for r in res.data} if res.data else {}
    except Exception:
        return {}

# ── Guardar respuestas en Supabase ────────────────────────────────────────────
def guardar_en_supabase(respuestas_dict):
    sb = get_supabase()
    empresa_codigo = st.session_state.get('empresa_codigo')
    usuario_email  = st.session_state.get('usuario_email')
    if not sb or not empresa_codigo or not usuario_email:
        return False
    try:
        for item, valor in respuestas_dict.items():
            sb.table('respuestas').upsert({
                'empresa_codigo': empresa_codigo,
                'usuario_email':  usuario_email,
                'bloque':         1,
                'item':           item,
                'valor':          float(valor)
            }, on_conflict='empresa_codigo,usuario_email,bloque,item').execute()
        return True
    except Exception:
        return False

# ── Cargar sesión ─────────────────────────────────────────────────────────────
perfil = cargar_perfil()
for k, v in perfil.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Mostrar estado de sesión ──────────────────────────────────────────────────
empresa_codigo = st.session_state.get('empresa_codigo')
usuario_email  = st.session_state.get('usuario_email')

if empresa_codigo and usuario_email:
    st.markdown(f"""<div style="background:#f0fdf4;border:1px solid #10b981;border-radius:8px;
        padding:8px 16px;margin-bottom:12px;font-size:.84rem;color:#065f46;">
        ✅ Sesión activa · <strong>{usuario_email}</strong> · Empresa <strong>{empresa_codigo}</strong>
    </div>""", unsafe_allow_html=True)
    # Cargar respuestas previas de Supabase para esta empresa/usuario
    resp_prev = cargar_respuestas_supabase()
else:
    st.warning("⚠️ Para guardar tus respuestas en la plataforma, accede desde la página **Acceso** con tu email y código de empresa.")
    resp_prev = {}

# ── Valores por defecto ───────────────────────────────────────────────────────
def val(key, default=1):
    # Prioridad: Supabase > perfil local > default
    if key in resp_prev:
        return int(resp_prev[key])
    return int(perfil.get(key, default))

v111 = val('it_111')
v112 = val('it_112')
v121 = val('it_121')
v122 = val('it_122')
v123 = val('it_123')
v131 = val('it_131')
v132 = val('it_132')

# ── Formulario ────────────────────────────────────────────────────────────────
st.title("BLOQUE 1: ACTIVIDADES DE I+D+i")

if st.session_state.get('b1_finalizado') and not resp_prev:
    st.success("✅ Este bloque ya está completado. Puedes modificar tus respuestas y volver a guardar.")
elif resp_prev:
    st.success("✅ Tienes respuestas guardadas para este bloque. Puedes modificarlas y volver a guardar.")

# Subindicador 1.1
st.subheader("1.1 Departamento I+D")
r111 = st.select_slider("1.1.1: Recursos técnicos dedicados a I+D",
    options=[1, 2, 3, 4, 5], value=v111)
r112 = st.select_slider("1.1.2: Recursos humanos dedicados a I+D",
    options=[1, 2, 3, 4, 5], value=v112)

# Subindicador 1.2
st.subheader("1.2 Presupuesto I+D")
r121 = st.select_slider("1.2.1: Presupuesto específico para I+D",
    options=[1, 2, 3, 4, 5], value=v121)
r122 = st.select_slider("1.2.2: I+D subvencionado",
    options=[1, 2, 3, 4, 5], value=v122)
r123 = st.select_slider("1.2.3: Participación en proyectos con financiación pública",
    options=[1, 2, 3, 4, 5], value=v123)

# Subindicador 1.3
st.subheader("1.3 Gasto en Innovación")
r131 = st.select_slider("1.3.1: Gasto estimado anual en innovación sobre ventas",
    options=[1, 2, 3, 4, 5], value=v131)
r132 = st.select_slider("1.3.2: Evolución futura del gasto en innovación",
    options=[1, 2, 3, 4, 5], value=v132)

st.divider()

if st.button("💾 GUARDAR BLOQUE 1", use_container_width=True, type="primary"):
    s1 = (r111 + r112) / 2
    s2 = (r121 + r122 + r123) / 3
    s3 = (r131 + r132) / 2
    score_b1 = (s1 * 0.2) + (s2 * 0.4) + (s3 * 0.4)

    st.session_state['score_sub1_1']  = s1
    st.session_state['score_sub1_2']  = s2
    st.session_state['score_sub1_3']  = s3
    st.session_state['score_b1']      = score_b1
    st.session_state['b1_finalizado'] = True

    # Guardar en perfil local (siempre)
    guardar_en_perfil({
        'score_sub1_1': s1, 'score_sub1_2': s2,
        'score_sub1_3': s3, 'score_b1': score_b1,
        'b1_finalizado': True,
        'it_111': r111, 'it_112': r112,
        'it_121': r121, 'it_122': r122, 'it_123': r123,
        'it_131': r131, 'it_132': r132,
    })

    # Guardar en Supabase (si hay sesión activa)
    if empresa_codigo and usuario_email:
        ok = guardar_en_supabase({
            'it_111': r111, 'it_112': r112,
            'it_121': r121, 'it_122': r122, 'it_123': r123,
            'it_131': r131, 'it_132': r132,
        })
        if ok:
            st.success(f"✅ Bloque 1 guardado en la plataforma. Índice I+D+i: **{score_b1:.2f}/5**")
        else:
            st.warning(f"⚠️ Bloque 1 guardado localmente. Índice I+D+i: **{score_b1:.2f}/5** (sin conexión a la plataforma)")
    else:
        st.success(f"✅ Bloque 1 guardado. Índice I+D+i: **{score_b1:.2f}/5**")

    st.info("Ahora puedes ir al Dashboard de Innovación para ver tu posición comparativa.")