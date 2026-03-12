"""
Helper para guardar respuestas de los bloques en Supabase.
Importar en cada bloque del cuestionario.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
 
def guardar_en_supabase(bloque_num, respuestas_dict):
    """
    Guarda las respuestas de un bloque en Supabase.
    respuestas_dict: {nombre_item: valor_float}
    Retorna True si OK, False si error.
    """
    empresa_codigo = st.session_state.get('empresa_codigo')
    usuario_email  = st.session_state.get('usuario_email')
 
    if not empresa_codigo or not usuario_email:
        return False, "No hay sesión activa. Accede desde la página Acceso."
 
    try:
        from supabase_client import get_supabase
        sb = get_supabase()
        if sb is None:
            return False, "Error de conexión con Supabase."
 
        for item, valor in respuestas_dict.items():
            sb.table('respuestas').upsert({
                'empresa_codigo': empresa_codigo,
                'usuario_email':  usuario_email,
                'bloque':         bloque_num,
                'item':           item,
                'valor':          float(valor)
            }, on_conflict='empresa_codigo,usuario_email,bloque,item').execute()
 
        return True, "Respuestas guardadas correctamente."
    except Exception as e:
        return False, f"Error al guardar: {e}"
 
 
def hay_sesion_activa():
    """Comprueba si hay usuario logueado."""
    return bool(st.session_state.get('usuario_email')) and bool(st.session_state.get('empresa_codigo'))
 
 
def mostrar_aviso_sesion():
    """Muestra aviso si no hay sesión."""
    if not hay_sesion_activa():
        st.warning("⚠️ Para que tus respuestas se guarden correctamente, accede primero desde la página **Acceso** con tu email y código de empresa.")
        return False
    email  = st.session_state.get('usuario_email','')
    codigo = st.session_state.get('empresa_codigo','')
    st.markdown(f"""<div style="background:#f0fdf4;border:1px solid #10b981;border-radius:8px;
        padding:8px 16px;margin-bottom:12px;font-size:.84rem;color:#065f46;">
        ✅ Sesión activa · <strong>{email}</strong> · Empresa <strong>{codigo}</strong>
    </div>""", unsafe_allow_html=True)
    return True