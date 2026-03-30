import streamlit as st
import json, os

st.set_page_config(page_title="Acceso · Diagnóstico Estratégico", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&display=swap');
</style>
""", unsafe_allow_html=True)

try:
    from supabase import create_client
    def get_supabase():
        url = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL",""))
        key = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY",""))
        if url and key: return create_client(url, key)
        return None
except Exception:
    def get_supabase(): return None

PERFIL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'perfil_empresa.json')

def cargar_perfil():
    if os.path.exists(PERFIL_FILE):
        with open(PERFIL_FILE,'r',encoding='utf-8') as f: return json.load(f)
    return {}

def guardar_perfil(datos):
    perfil = cargar_perfil(); perfil.update(datos)
    with open(PERFIL_FILE,'w',encoding='utf-8') as f: json.dump(perfil,f,ensure_ascii=False,indent=2)

# ── Inicializar cookies ───────────────────────────────────────────────────────
try:
    from streamlit_cookies_manager import EncryptedCookieManager
    cookies = EncryptedCookieManager(prefix="diagnostico360_", password="D1agn0st1c0360Secret!")
    if not cookies.ready():
        st.stop()
    COOKIES_OK = True
except Exception:
    cookies = None
    COOKIES_OK = False

def guardar_sesion_cookie(email, codigo, es_admin, nombre, rol):
    if not COOKIES_OK or cookies is None: return
    try:
        cookies['usuario_email']  = email
        cookies['empresa_codigo'] = codigo
        cookies['es_admin']       = str(es_admin)
        cookies['usuario_nombre'] = nombre
        cookies['usuario_rol']    = rol
        cookies.save()
    except Exception: pass

def limpiar_sesion_cookie():
    if not COOKIES_OK or cookies is None: return
    try:
        for k in ['usuario_email','empresa_codigo','es_admin','usuario_nombre','usuario_rol']:
            cookies[k] = ''
        cookies.save()
    except Exception: pass

def cargar_sesion_cookie():
    if not COOKIES_OK or cookies is None: return False
    try:
        email = cookies.get('usuario_email','')
        codigo = cookies.get('empresa_codigo','')
        if email and codigo:
            st.session_state['usuario_email']  = email
            st.session_state['empresa_codigo'] = codigo
            st.session_state['es_admin']       = cookies.get('es_admin','False') == 'True'
            st.session_state['usuario_nombre'] = cookies.get('usuario_nombre','')
            st.session_state['usuario_rol']    = cookies.get('usuario_rol','colaborador')
            return True
    except Exception: pass
    return False

# ── Cargar sesión de cookie si no hay sesión activa ───────────────────────────
perfil = cargar_perfil()
if not st.session_state.get('usuario_email'):
    # Intentar desde perfil local
    if perfil.get('sesion_email'):
        st.session_state['usuario_email']  = perfil['sesion_email']
        st.session_state['empresa_codigo'] = perfil.get('sesion_codigo','')
        st.session_state['es_admin']       = perfil.get('sesion_es_admin', False)
        st.session_state['usuario_nombre'] = perfil.get('sesion_nombre','')
        st.session_state['usuario_rol']    = perfil.get('sesion_rol','colaborador')
    else:
        cargar_sesion_cookie()

# ── Si ya hay sesión activa ────────────────────────────────────────────────────
if st.session_state.get('usuario_email') and st.session_state.get('empresa_codigo'):
    email  = st.session_state['usuario_email']
    codigo = st.session_state['empresa_codigo']
    es_admin = st.session_state.get('es_admin', False)
    rol = "Administrador" if es_admin else st.session_state.get('usuario_rol','Colaborador').capitalize()

    st.success(f"✅ Sesión activa · {email} · {rol} · Empresa {codigo}")

    if st.button("Cerrar sesión", type="secondary"):
        guardar_perfil({'sesion_email':None,'sesion_codigo':None,'sesion_es_admin':False,'sesion_nombre':'','sesion_rol':''})
        limpiar_sesion_cookie()
        for k in ['usuario_email','empresa_codigo','es_admin','usuario_nombre','usuario_rol']:
            st.session_state.pop(k, None)
        st.rerun()
    st.stop()

# ── Formulario de acceso ───────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-bottom:28px;">
  <h1 style="font-family:'Rajdhani',sans-serif;color:#1e293b;font-size:2rem;margin-bottom:4px;">
    Diagnóstico Estratégico 360°</h1>
  <p style="color:#64748b;font-size:.92rem;">Introduce tus datos para acceder al cuestionario</p>
</div>
""", unsafe_allow_html=True)

col_l, col_c, col_r = st.columns([1,2,1])
with col_c:
    st.markdown("#### Acceder al cuestionario")
    nombre = st.text_input("Tu nombre", placeholder="Nombre y apellido")
    email  = st.text_input("Tu email", placeholder="nombre@empresa.com")
    codigo = st.text_input("Código de empresa", placeholder="EMP-XXXX",
                           help="El administrador de tu empresa te lo habrá proporcionado")
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Entrar", use_container_width=True, type="primary"):
        if not nombre or not email or not codigo:
            st.error("Por favor rellena todos los campos.")
        else:
            sb = get_supabase()
            if sb is None:
                st.error("Error de conexión con la base de datos.")
            else:
                codigo = codigo.strip().upper()
                try:
                    emp = sb.table('empresas').select('*').eq('codigo', codigo).execute()
                    if not emp.data:
                        st.error("❌ Código de empresa no encontrado.")
                    else:
                        empresa = emp.data[0]
                        usr = sb.table('usuarios').select('*')\
                            .eq('empresa_codigo', codigo)\
                            .eq('email', email.strip().lower()).execute()
                        if not usr.data:
                            st.error("❌ Tu email no está autorizado. Contacta con el administrador.")
                        else:
                            usuario = usr.data[0]
                            es_admin = usuario.get('es_admin', False)
                            rol = usuario.get('rol', 'admin' if es_admin else 'colaborador')
                            email_clean = email.strip().lower()

                            # Limpiar scores si cambia de empresa
                            codigo_anterior = perfil.get('sesion_codigo','')
                            if codigo_anterior != codigo:
                                for k in ['score_b1','score_b2','score_b3','score_b4','score_b5',
                                          'b1_finalizado','b2_finalizado','b3_finalizado',
                                          'b4_finalizado','b5_finalizado']:
                                    st.session_state.pop(k, None)
                                guardar_perfil({
                                    'score_b1':0,'score_b2':0,'score_b3':0,'score_b4':0,'score_b5':0,
                                    'b1_finalizado':False,'b2_finalizado':False,'b3_finalizado':False,
                                    'b4_finalizado':False,'b5_finalizado':False,
                                    'informes_activados':False,'promedios_activados':False,
                                })

                            # Guardar sesión
                            st.session_state['usuario_email']  = email_clean
                            st.session_state['usuario_nombre'] = nombre
                            st.session_state['empresa_codigo'] = codigo
                            st.session_state['es_admin']       = es_admin
                            st.session_state['usuario_rol']    = rol

                            # Guardar en perfil local y cookie
                            guardar_perfil({
                                'sesion_email':    email_clean,
                                'sesion_codigo':   codigo,
                                'sesion_es_admin': es_admin,
                                'sesion_nombre':   nombre,
                                'sesion_rol':      rol,
                            })
                            guardar_sesion_cookie(email_clean, codigo, es_admin, nombre, rol)

                            # Cargar datos de empresa
                            mapa = {
                                'sector':'save_sector_nombre','tamano':'save_tam_nombre',
                                'region':'save_reg_nombre','exportacion':'save_export_nombre',
                                'antiguedad':'save_anti_nombre','ventas':'save_ventas',
                                'empleados':'save_empleados','roa':'save_roa',
                                'var_ventas':'save_var_vtas','var_empleados':'save_var_empl',
                                'productividad':'save_productiv','coste_empleado':'save_coste_emp',
                                'endeudamiento':'save_endeud'
                            }
                            for campo, ss_key in mapa.items():
                                if empresa.get(campo) is not None:
                                    st.session_state[ss_key] = empresa[campo]

                            rol_txt = "Administrador" if es_admin else rol.capitalize()
                            try:
                                resp_scores = sb.table('respuestas').select('bloque,item,valor').eq('empresa_codigo', codigo).execute().data or []
                                if resp_scores:
                                    from collections import defaultdict
                                    sumas = defaultdict(list)
                                    for r in resp_scores:
                                        sumas[r['bloque']].append(r['valor'])
                                    for b in range(1,6):
                                        vals = sumas.get(b,[])
                                        if vals:
                                            st.session_state[f'score_b{b}'] = round(sum(vals)/len(vals),2)
                                    bloques = set(r['bloque'] for r in resp_scores)
                                    if len(bloques) >= 5:
                                        st.session_state['informes_activados'] = True
                            except Exception:
                                pass
                            st.success(f"✅ Bienvenido/a, {nombre}. Rol: {rol_txt}")
                            st.rerun()
                except Exception as e:
                    st.error(f"Error de conexión: {e}")

    st.markdown("---")
    st.markdown("""<div style="text-align:center;font-size:.82rem;color:#94a3b8;">
        ¿Eres el administrador y aún no has registrado tu empresa?<br>
        Ve a la página <strong>Registro Empresa</strong> en el menú lateral.</div>""",
        unsafe_allow_html=True)