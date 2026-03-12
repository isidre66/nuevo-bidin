import streamlit as st
import json, os, random, string
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
 
st.set_page_config(page_title="Registro de Empresa", layout="wide")
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&display=swap');
</style>
""", unsafe_allow_html=True)
 
try:
    from supabase_client import get_supabase
    sb = get_supabase()
except Exception:
    sb = None
 
def generar_codigo():
    return "EMP-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
 
st.markdown("""
<div style="max-width:560px;margin:0 auto;">
<h1 style="font-family:'Rajdhani',sans-serif;color:#1e293b;font-size:1.8rem;margin-bottom:4px;">
  🏢 Registrar nueva empresa</h1>
<p style="color:#64748b;font-size:.9rem;margin-bottom:24px;">
  Crea el perfil de tu empresa para iniciar el diagnóstico colectivo.</p>
</div>
""", unsafe_allow_html=True)
 
col_l, col_c, col_r = st.columns([1,3,1])
with col_c:
    nombre_emp = st.text_input("Nombre de la empresa *", placeholder="Empresa S.L.")
    email_admin = st.text_input("Tu email (administrador) *", placeholder="admin@empresa.com")
 
    st.markdown("""<div style="background:#eff6ff;border-left:3px solid #3b82f6;
        border-radius:0 8px 8px 0;padding:10px 16px;margin:12px 0;color:#1d4ed8;font-size:.84rem;">
        Se generará automáticamente un <strong>código de empresa</strong> que compartirás
        con tus colaboradores para que accedan al cuestionario.</div>""", unsafe_allow_html=True)
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    if st.button("Crear empresa y obtener código", use_container_width=True, type="primary"):
        if not nombre_emp or not email_admin:
            st.error("Rellena todos los campos obligatorios.")
        elif sb is None:
            st.error("Error de conexión con la base de datos.")
        else:
            try:
                # Verificar si ya existe empresa para este admin
                existe = sb.table('empresas').select('codigo')\
                    .eq('email_admin', email_admin.strip().lower()).execute()
                if existe.data:
                    codigo_existente = existe.data[0]['codigo']
                    st.warning(f"Ya tienes una empresa registrada con este email. Tu código es: **{codigo_existente}**")
                    st.session_state['empresa_codigo'] = codigo_existente
                    st.session_state['usuario_email']  = email_admin.strip().lower()
                    st.session_state['es_admin']       = True
                else:
                    codigo = generar_codigo()
                    # Crear empresa
                    sb.table('empresas').insert({
                        'codigo': codigo,
                        'nombre': nombre_emp,
                        'email_admin': email_admin.strip().lower()
                    }).execute()
                    # Crear usuario admin
                    sb.table('usuarios').insert({
                        'empresa_codigo': codigo,
                        'email': email_admin.strip().lower(),
                        'nombre': nombre_emp,
                        'es_admin': True
                    }).execute()
                    # Guardar sesión
                    st.session_state['empresa_codigo'] = codigo
                    st.session_state['usuario_email']  = email_admin.strip().lower()
                    st.session_state['es_admin']       = True
 
                    st.success(f"✅ Empresa creada correctamente.")
                    st.markdown(f"""
                    <div style="background:#f0fdf4;border:2px solid #10b981;border-radius:14px;
                        padding:24px;text-align:center;margin-top:16px;">
                      <div style="font-size:.75rem;color:#065f46;font-weight:600;
                          letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">
                        Tu código de empresa</div>
                      <div style="font-family:'Rajdhani',sans-serif;font-size:2.4rem;
                          font-weight:700;color:#065f46;letter-spacing:4px;">{codigo}</div>
                      <div style="color:#475569;font-size:.85rem;margin-top:10px;">
                        Comparte este código con tus colaboradores para que accedan al cuestionario.</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.info("👉 Ve ahora a **Mi Empresa** en el menú lateral para invitar a tus colaboradores y configurar los datos de la empresa.")
            except Exception as e:
                st.error(f"Error al crear la empresa: {e}")