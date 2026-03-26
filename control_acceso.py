"""
Helper de control de acceso por rol.
Importar al inicio de cada página de resultados.

Uso:
    from control_acceso import verificar_acceso
    verificar_acceso(nivel_minimo='manager')  # o 'admin'
"""
import streamlit as st
import json, os

PERFIL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'perfil_empresa.json')

def cargar_perfil():
    if os.path.exists(PERFIL_FILE):
        with open(PERFIL_FILE,'r',encoding='utf-8') as f: return json.load(f)
    return {}

def get_rol():
    """Devuelve el rol del usuario actual."""
    if st.session_state.get('es_admin'): return 'admin'
    # Intentar obtener rol de Supabase
    rol_sb = _get_rol_supabase()
    if rol_sb: return rol_sb
    return 'colaborador'

def _get_rol_supabase():
    try:
        from supabase import create_client
        url = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL",""))
        key = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY",""))
        if not url or not key: return None
        sb = create_client(url, key)
        ec = st.session_state.get('empresa_codigo')
        ue = st.session_state.get('usuario_email')
        if not ec or not ue: return None
        res = sb.table('usuarios').select('rol').eq('empresa_codigo',ec).eq('email',ue).execute()
        if res.data: return res.data[0].get('rol','colaborador')
    except Exception:
        pass
    return None

NIVEL = {'colaborador': 0, 'manager': 1, 'admin': 2}

def verificar_acceso(nivel_minimo='manager'):
    """
    Verifica que el usuario tiene el nivel mínimo requerido.
    Si no, muestra mensaje y detiene la ejecución.
    nivel_minimo: 'manager' o 'admin'
    """
    # Cargar perfil si no hay sesión
    if not st.session_state.get('usuario_email'):
        perfil = cargar_perfil()
        for k,v in perfil.items():
            if k not in st.session_state: st.session_state[k] = v

    usuario_email = st.session_state.get('usuario_email')
    empresa_codigo = st.session_state.get('empresa_codigo')

    # Sin sesión activa
    if not usuario_email or not empresa_codigo:
        st.markdown("""<div style="text-align:center;padding:60px 40px;">
          <div style="font-size:3rem;margin-bottom:16px;">🔒</div>
          <h2 style="font-family:'Rajdhani',sans-serif;color:#1e293b;">Acceso restringido</h2>
          <p style="color:#64748b;">Para ver esta página debes acceder primero con tu email y código de empresa.</p>
        </div>""", unsafe_allow_html=True)
        st.page_link("pages/00_Acceso.py", label="👉 Ir a Acceso", use_container_width=False)
        st.stop()

    rol = get_rol()
    nivel_usuario = NIVEL.get(rol, 0)
    nivel_requerido = NIVEL.get(nivel_minimo, 1)

    if nivel_usuario < nivel_requerido:
        if nivel_minimo == 'admin':
            msg = "Esta página es solo para el **administrador** de la empresa."
        else:
            msg = "Esta página requiere rol de **Manager** o superior. Contacta con el administrador de tu empresa para que te asigne ese rol."

        st.markdown(f"""<div style="text-align:center;padding:60px 40px;">
          <div style="font-size:3rem;margin-bottom:16px;">🔒</div>
          <h2 style="font-family:'Rajdhani',sans-serif;color:#1e293b;">Acceso restringido</h2>
          <p style="color:#64748b;max-width:480px;margin:0 auto;">{msg}</p>
        </div>""", unsafe_allow_html=True)
        st.stop()

    # Verificar que los informes están activados
    if not st.session_state.get('informes_activados'):
        perfil = cargar_perfil()
        if not perfil.get('informes_activados'):
            st.markdown("""<div style="text-align:center;padding:60px 40px;">
              <div style="font-size:3rem;margin-bottom:16px;">⏳</div>
              <h2 style="font-family:'Rajdhani',sans-serif;color:#1e293b;">Informes pendientes de activar</h2>
              <p style="color:#64748b;max-width:480px;margin:0 auto;">
                El administrador de tu empresa todavía no ha activado los informes.<br>
                Cuando todo el equipo complete el cuestionario, el admin podrá calcular los promedios 
                y activar el acceso a los resultados.</p>
            </div>""", unsafe_allow_html=True)
            st.stop()
        else:
            st.session_state['informes_activados'] = True

    return rol