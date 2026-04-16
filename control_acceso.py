import streamlit as st

JERARQUIA = {'colaborador': 0, 'manager': 1, 'admin': 2}

def verificar_acceso(nivel_requerido='manager'):
    if not st.session_state.get('usuario_email') and not st.session_state.get('save_reg_user'):
        st.warning("Por favor, inicia sesion primero en la seccion Acceso.")
        st.stop()

    rol_usuario = st.session_state.get('usuario_rol', 'colaborador')
    nivel_usuario = JERARQUIA.get(rol_usuario, 0)
    nivel_necesario = JERARQUIA.get(nivel_requerido, 1)

    if nivel_usuario < nivel_necesario:
        if nivel_requerido == 'admin':
            texto = "Esta seccion esta disponible unicamente para el Administrador de la empresa."
        else:
            texto = "Esta seccion esta disponible para usuarios con rol Manager o Admin. Contacta con el administrador de tu empresa."

        st.markdown(f"""
        <div style="background:#0a1020;border:1px solid #1e3a5f;border-radius:14px;
             padding:40px 32px;text-align:center;margin:40px auto;max-width:600px;">
            <div style="font-size:2.5rem;margin-bottom:16px;">&#128274;</div>
            <div style="font-family:sans-serif;font-size:1.4rem;font-weight:700;
                 color:#e2e8f0;margin-bottom:12px;">Acceso restringido</div>
            <div style="color:#94a3b8;font-size:.95rem;line-height:1.7;">{texto}</div>
            <div style="margin-top:20px;padding:12px 16px;background:rgba(29,78,216,.1);
                 border-radius:8px;font-size:.85rem;color:#64748b;">
                Tu rol actual: <strong style="color:#e2e8f0;">{rol_usuario.capitalize()}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()