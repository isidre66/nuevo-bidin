import streamlit as st
import json, os
from datetime import datetime

st.set_page_config(page_title="Superadmin · Panel de Control", layout="wide")

SUPERADMIN_EMAIL = "isidre.march@uv.es"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&display=swap');
.sa-header {
    background: linear-gradient(135deg,#0a0e1a,#0d1b2a);
    border: 1px solid #1e3a5f; border-radius: 14px;
    padding: 28px 32px; margin-bottom: 24px;
}
.empresa-card {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 16px 20px; margin-bottom: 10px;
}
.badge {
    display: inline-block; border-radius: 20px; padding: 3px 10px;
    font-size: .75rem; font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ── Verificar superadmin ───────────────────────────────────────────────────────
usuario_email = st.session_state.get('usuario_email', '')

if not usuario_email:
    st.markdown("""
    <div style="max-width:400px;margin:80px auto;text-align:center;">
    <div style="font-size:3rem;margin-bottom:16px;">🔐</div>
    <h2 style="font-family:'Rajdhani',sans-serif;color:#1e293b;">Acceso Superadmin</h2>
    <p style="color:#64748b;">Introduce tu email de superadministrador</p>
    </div>
    """, unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        email_input = st.text_input("Email", placeholder="tu@email.com")
        if st.button("Entrar", use_container_width=True, type="primary"):
            if email_input.strip().lower() == SUPERADMIN_EMAIL:
                st.session_state['usuario_email'] = email_input.strip().lower()
                st.session_state['es_superadmin'] = True
                st.rerun()
            else:
                st.error("❌ Email no autorizado.")
    st.stop()

if usuario_email != SUPERADMIN_EMAIL:
    st.error("🔒 Acceso restringido al superadministrador.")
    st.stop()

# ── Conexión Supabase ──────────────────────────────────────────────────────────
def get_supabase():
    try:
        from supabase import create_client
        url = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL",""))
        key = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY",""))
        if url and key: return create_client(url, key)
    except Exception: pass
    return None

sb = get_supabase()
if not sb:
    st.error("Error de conexión con Supabase.")
    st.stop()

# ── Cabecera ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sa-header">
  <div style="font-size:.68rem;color:#4a6fa5;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px;">
    Panel de Control</div>
  <h1 style="font-family:'Rajdhani',sans-serif;color:#00d4ff;font-size:1.8rem;margin:0 0 4px;">
    ⚡ Superadmin · Diagnóstico Estratégico 360°</h1>
  <p style="color:#94a3b8;margin:0;font-size:.88rem;">isidre.march@uv.es · Acceso total</p>
</div>
""", unsafe_allow_html=True)

# ── Cargar datos ───────────────────────────────────────────────────────────────
try:
    empresas   = sb.table('empresas').select('*').execute().data or []
    usuarios   = sb.table('usuarios').select('*').execute().data or []
    respuestas = sb.table('respuestas').select('*').execute().data or []
except Exception as e:
    st.error(f"Error cargando datos: {e}")
    st.stop()

# ── Métricas globales ──────────────────────────────────────────────────────────
total_emp  = len(empresas)
total_usr  = len([u for u in usuarios if not u.get('es_admin')])
total_resp = len(respuestas)
emp_con_resp = len(set(r['empresa_codigo'] for r in respuestas))

c1,c2,c3,c4 = st.columns(4)
c1.metric("🏢 Empresas registradas", total_emp)
c2.metric("👥 Usuarios totales", total_usr)
c3.metric("📝 Respuestas guardadas", total_resp)
c4.metric("✅ Empresas activas", emp_con_resp)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🏢 Empresas", "📊 Respuestas detalladas", "🗑️ Gestión"])

# ─────────────────────────────────────────────────────
# TAB 1 — EMPRESAS
# ─────────────────────────────────────────────────────
with tab1:
    st.markdown("### Todas las empresas registradas")

    # Calcular respuestas por empresa
    resp_por_empresa = {}
    for r in respuestas:
        ec = r['empresa_codigo']
        if ec not in resp_por_empresa:
            resp_por_empresa[ec] = set()
        resp_por_empresa[ec].add(r['bloque'])

    for emp in empresas:
        codigo  = emp.get('codigo','')
        nombre  = emp.get('nombre','Sin nombre')
        email_a = emp.get('email_admin','')
        sector  = emp.get('sector','—')
        bloques = resp_por_empresa.get(codigo, set())
        completado = len(bloques)
        pct = int(completado/5*100)
        color = "#10b981" if completado==5 else "#f59e0b" if completado>0 else "#94a3b8"
        validada = emp.get('validada', True)
        pendiente = emp.get('pendiente_validar', False)

        if pendiente:
            badge = '<span class="badge" style="background:#fef3c7;color:#92400e;">⏳ Pendiente validar</span>'
        elif validada:
            badge = '<span class="badge" style="background:#dcfce7;color:#166534;">✅ Validada</span>'
        else:
            badge = '<span class="badge" style="background:#fee2e2;color:#991b1b;">❌ No validada</span>'

        st.markdown(f"""<div class="empresa-card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
            <div>
              <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:700;color:#1e293b;">
                {nombre} <span style="font-size:.8rem;color:#64748b;font-weight:400;">· {codigo}</span></div>
              <div style="font-size:.82rem;color:#64748b;margin-top:2px;">Admin: {email_a} · Sector: {sector}</div>
              <div style="margin-top:6px;">{badge}</div>
            </div>
            <div style="text-align:right;min-width:140px;">
              <div style="font-size:.82rem;font-weight:700;color:{color};">{completado}/5 bloques completados</div>
              <div style="background:#e2e8f0;border-radius:20px;height:6px;margin-top:4px;">
                <div style="background:{color};height:6px;width:{pct}%;border-radius:20px;"></div>
              </div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        col_v, col_e = st.columns([1,1])
        with col_v:
            if pendiente:
                if st.button(f"✅ Validar {codigo}", key=f"val_{codigo}", use_container_width=True):
                    try:
                        sb.table('empresas').update({'validada':True,'pendiente_validar':False}).eq('codigo',codigo).execute()
                        st.success(f"Empresa {codigo} validada.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
        with col_e:
            if st.button(f"🗑️ Eliminar {codigo}", key=f"del_{codigo}", use_container_width=True):
                st.session_state[f'confirm_del_{codigo}'] = True

        if st.session_state.get(f'confirm_del_{codigo}'):
            st.warning(f"⚠️ ¿Seguro que quieres eliminar la empresa **{nombre}** ({codigo})? Esta acción no se puede deshacer.")
            cc1, cc2 = st.columns(2)
            with cc1:
                if st.button(f"Sí, eliminar", key=f"yes_{codigo}", type="primary"):
                    try:
                        sb.table('respuestas').delete().eq('empresa_codigo',codigo).execute()
                        sb.table('usuarios').delete().eq('empresa_codigo',codigo).execute()
                        sb.table('empresas').delete().eq('codigo',codigo).execute()
                        st.success(f"Empresa {codigo} eliminada.")
                        st.session_state.pop(f'confirm_del_{codigo}', None)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            with cc2:
                if st.button(f"Cancelar", key=f"no_{codigo}"):
                    st.session_state.pop(f'confirm_del_{codigo}', None)
                    st.rerun()

# ─────────────────────────────────────────────────────
# TAB 2 — RESPUESTAS DETALLADAS
# ─────────────────────────────────────────────────────
with tab2:
    st.markdown("### Respuestas detalladas por empresa")

    codigos = [e['codigo'] for e in empresas]
    nombres = {e['codigo']: e.get('nombre','Sin nombre') for e in empresas}

    if not codigos:
        st.info("No hay empresas registradas aún.")
    else:
        empresa_sel = st.selectbox("Selecciona empresa",
            options=codigos,
            format_func=lambda x: f"{nombres.get(x,x)} ({x})")

        resp_emp = [r for r in respuestas if r['empresa_codigo'] == empresa_sel]

        if not resp_emp:
            st.info("Esta empresa no tiene respuestas aún.")
        else:
            # Agrupar por usuario y bloque
            from collections import defaultdict
            por_usuario = defaultdict(lambda: defaultdict(dict))
            for r in resp_emp:
                por_usuario[r['usuario_email']][r['bloque']][r['item']] = r['valor']

            BLOQUES = {1:"I+D+i",2:"Gestión Proyectos",3:"Desarrollo Productos",
                       4:"Estrategia Innovación",5:"Desempeño Innovación"}

            for email_u, bloques_u in por_usuario.items():
                with st.expander(f"👤 {email_u}"):
                    for bloque_num in sorted(bloques_u.keys()):
                        st.markdown(f"**Bloque {bloque_num} · {BLOQUES.get(bloque_num,'')}**")
                        items = bloques_u[bloque_num]
                        cols = st.columns(4)
                        for i, (item, valor) in enumerate(sorted(items.items())):
                            cols[i%4].metric(item, f"{valor:.0f}/5")
                        st.divider()

            # Promedios del equipo
            st.markdown("### Promedios del equipo")
            sumas = defaultdict(list)
            for r in resp_emp:
                sumas[f"B{r['bloque']}_{r['item']}"].append(r['valor'])
            promedios = {k: round(sum(v)/len(v),2) for k,v in sumas.items()}

            scores = {}
            for b in range(1,6):
                items_b = [v for k,v in promedios.items() if k.startswith(f"B{b}_")]
                if items_b: scores[b] = round(sum(items_b)/len(items_b),2)

            if scores:
                cols = st.columns(len(scores))
                for i,(b,score) in enumerate(scores.items()):
                    color = "#10b981" if score>=3.5 else "#f59e0b" if score>=2.5 else "#ef4444"
                    cols[i].markdown(f"""<div style="background:#f8fafc;border:1px solid #e2e8f0;
                        border-top:3px solid {color};border-radius:10px;padding:14px;text-align:center;">
                      <div style="font-size:.72rem;color:#64748b;">{BLOQUES[b]}</div>
                      <div style="font-family:'Rajdhani',sans-serif;font-size:1.8rem;font-weight:700;color:{color};">
                        {score}</div></div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# TAB 3 — GESTIÓN
# ─────────────────────────────────────────────────────
with tab3:
    st.markdown("### Gestión de la plataforma")

    st.markdown("#### Empresas pendientes de validar")
    pendientes = [e for e in empresas if e.get('pendiente_validar')]
    if not pendientes:
        st.success("✅ No hay empresas pendientes de validar.")
    else:
        for emp in pendientes:
            col_a, col_b, col_c = st.columns([3,1,1])
            with col_a:
                st.markdown(f"**{emp.get('nombre')}** · {emp.get('codigo')} · {emp.get('email_admin')}")
            with col_b:
                if st.button("✅ Validar", key=f"vt_{emp['codigo']}"):
                    sb.table('empresas').update({'validada':True,'pendiente_validar':False}).eq('codigo',emp['codigo']).execute()
                    st.rerun()
            with col_c:
                if st.button("❌ Rechazar", key=f"rt_{emp['codigo']}"):
                    sb.table('respuestas').delete().eq('empresa_codigo',emp['codigo']).execute()
                    sb.table('usuarios').delete().eq('empresa_codigo',emp['codigo']).execute()
                    sb.table('empresas').delete().eq('codigo',emp['codigo']).execute()
                    st.rerun()

    st.markdown("---")
    st.markdown("#### Estadísticas de uso")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total respuestas en BD", total_resp)
        st.metric("Empresas con diagnóstico completo", len([e for e in empresas
            if len(resp_por_empresa.get(e['codigo'],set()))==5]))
    with col2:
        st.metric("Media respuestas por empresa", round(total_resp/max(emp_con_resp,1),1))
        st.metric("Usuarios por empresa (media)", round(total_usr/max(total_emp,1),1))