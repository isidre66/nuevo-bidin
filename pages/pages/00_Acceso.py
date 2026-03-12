import streamlit as st
import json, os, random, string
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
 
st.set_page_config(page_title="Acceso · Diagnóstico Estratégico", layout="wide")
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&display=swap');
.acceso-box {
    max-width: 480px; margin: 60px auto; background: #ffffff;
    border: 1px solid #e2e8f0; border-radius: 16px; padding: 36px 40px;
    box-shadow: 0 4px 24px rgba(0,0,0,.08);
}
</style>
""", unsafe_allow_html=True)
 
try:
    from supabase_client import get_supabase
    sb = get_supabase()
except Exception:
    sb = None
 
PERFIL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'perfil_empresa.json')
def cargar_perfil():
    if os.path.exists(PERFIL_FILE):
        with open(PERFIL_FILE,'r',encoding='utf-8') as f: return json.load(f)
    return {}
def guardar_perfil(datos):
    with open(PERFIL_FILE,'w',encoding='utf-8') as f: json.dump(datos,f,ensure_ascii=False,indent=2)
 
# ── Si ya hay sesión activa ────────────────────────────────
if st.session_state.get('usuario_email') and st.session_state.get('empresa_codigo'):
    email  = st.session_state['usuario_email']
    codigo = st.session_state['empresa_codigo']
    es_admin = st.session_state.get('es_admin', False)
    rol = "Administrador" if es_admin else "Colaborador"
    st.success(f"✅ Sesión activa · {email} · {rol} · Empresa {codigo}")
    if st.button("Cerrar sesión", type="secondary"):
        for k in ['usuario_email','empresa_codigo','es_admin','usuario_nombre']:
            st.session_state.pop(k, None)
        st.rerun()
    st.stop()
 
# ── Formulario de acceso ───────────────────────────────────
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
        elif sb is None:
            st.error("Error de conexión con la base de datos.")
        else:
            codigo = codigo.strip().upper()
            # Verificar que la empresa existe
            try:
                emp = sb.table('empresas').select('*').eq('codigo', codigo).execute()
                if not emp.data:
                    st.error("❌ Código de empresa no encontrado. Comprueba que es correcto.")
                else:
                    empresa = emp.data[0]
                    # Verificar que el email está autorizado
                    usr = sb.table('usuarios').select('*')\
                        .eq('empresa_codigo', codigo)\
                        .eq('email', email.strip().lower()).execute()
                    if not usr.data:
                        st.error("❌ Tu email no está autorizado para esta empresa. Contacta con el administrador.")
                    else:
                        usuario = usr.data[0]
                        # Guardar sesión
                        st.session_state['usuario_email']   = email.strip().lower()
                        st.session_state['usuario_nombre']  = nombre
                        st.session_state['empresa_codigo']  = codigo
                        st.session_state['es_admin']        = usuario.get('es_admin', False)
                        # Cargar perfil de empresa en session_state
                        for campo in ['sector','tamano','region','exportacion','antiguedad',
                                      'ventas','empleados','roa','var_ventas','var_empleados',
                                      'productividad','coste_empleado','endeudamiento']:
                            if empresa.get(campo) is not None:
                                mapa = {
                                    'sector':'save_sector_nombre','tamano':'save_tam_nombre',
                                    'region':'save_reg_nombre','exportacion':'save_export_nombre',
                                    'antiguedad':'save_anti_nombre','ventas':'save_ventas',
                                    'empleados':'save_empleados','roa':'save_roa',
                                    'var_ventas':'save_var_vtas','var_empleados':'save_var_empl',
                                    'productividad':'save_productiv','coste_empleado':'save_coste_emp',
                                    'endeudamiento':'save_endeud'
                                }
                                st.session_state[mapa[campo]] = empresa[campo]
                        st.success(f"✅ Bienvenido/a, {nombre}. Ya puedes completar el cuestionario.")
                        st.rerun()
            except Exception as e:
                st.error(f"Error de conexión: {e}")
 
    st.markdown("---")
    st.markdown("""<div style="text-align:center;font-size:.82rem;color:#94a3b8;">
        ¿Eres el administrador y aún no has registrado tu empresa?<br>
        Ve a la página <strong>Mi Empresa</strong> en el menú lateral.</div>""",
        unsafe_allow_html=True)