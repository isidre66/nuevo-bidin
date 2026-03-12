import streamlit as st
import json, os, random, string
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
 
st.set_page_config(page_title="Mi Empresa · Admin", layout="wide")
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&display=swap');
.admin-header {
    background: linear-gradient(135deg,#0a0e1a,#0d1b2a);
    border: 1px solid #1e3a5f; border-radius: 14px;
    padding: 28px 32px; margin-bottom: 24px;
}
.user-card {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 14px 18px; margin-bottom: 8px;
    display: flex; align-items: center; justify-content: space-between;
}
.progress-bar-bg {
    background: #e2e8f0; border-radius: 20px; height: 8px; overflow: hidden;
}
.seccion {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 14px; padding: 24px 28px; margin-bottom: 20px;
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
 
REGIONES = {"Andalucia":1,"Aragon":2,"Asturias":3,"Baleares":4,"Canarias":5,
    "Cantabria":6,"Castilla la Mancha":7,"Castilla y León":8,"Cataluña":9,
    "Com Valenciana":10,"Extremadura":11,"Galicia":12,"Madrid":13,
    "Murcia":14,"Navarra":15,"Pais Vasco":16}
TAMANIOS = {"Pequeña":1,"Mediana":2,"Grande":3}
EXPORTACIONES = {"Menos 10 %":1,"10 - 30 %":2,"30 - 60 %":3,"> 60 %":4}
ANTIGUEDADES  = {"Menos 10 años":1,"10-30 años":2,"> 30 años":3}
SECTORES = ["Alimentación y bebidas","Textil y confección","Cuero y calzado",
    "Química y plásticos","Minerales no metálicos","Metalmecanico","Maquinaria equipo",
    "Otras manufacturas","Electrónica, telecomunicaciones","Informática, software. Robótica, IA",
    "Actividades I+D: biotech, farmacia","Transporte y logística",
    "Consultoría y servicios profesionales","Turismo y hosteleria","Retail y comercio","Otros servicios"]
 
def generar_codigo():
    return "EMP-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
 
# ══════════════════════════════════════════════════════
# VERIFICAR SESIÓN ADMIN
# ══════════════════════════════════════════════════════
es_admin   = st.session_state.get('es_admin', False)
emp_codigo = st.session_state.get('empresa_codigo', '')
usr_email  = st.session_state.get('usuario_email', '')
 
if not usr_email:
    st.warning("⚠️ Debes acceder primero desde la página **Acceso**.")
    st.stop()
 
if not es_admin:
    st.error("🔒 Solo el administrador de la empresa puede acceder a esta página.")
    st.stop()
 
# ══════════════════════════════════════════════════════
# CABECERA ADMIN
# ══════════════════════════════════════════════════════
st.markdown(f"""
<div class="admin-header">
  <div style="font-size:.68rem;color:#4a6fa5;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px;">
    Panel de Administración</div>
  <h1 style="font-family:'Rajdhani',sans-serif;color:#00d4ff;font-size:1.8rem;margin:0 0 4px;">
    Mi Empresa · {emp_codigo}</h1>
  <p style="color:#94a3b8;margin:0;font-size:.88rem;">Admin: {usr_email}</p>
</div>
""", unsafe_allow_html=True)
 
if sb is None:
    st.error("Error de conexión con la base de datos.")
    st.stop()
 
# Cargar datos empresa
try:
    emp_data = sb.table('empresas').select('*').eq('codigo', emp_codigo).execute()
    empresa  = emp_data.data[0] if emp_data.data else {}
except Exception as e:
    st.error(f"Error cargando empresa: {e}")
    st.stop()
 
# ══════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["👥 Seguimiento de usuarios", "🏢 Datos de la empresa", "📊 Resultados del equipo"])
 
# ─────────────────────────────────────────────────────
# TAB 1 — SEGUIMIENTO
# ─────────────────────────────────────────────────────
with tab1:
    st.markdown("### Usuarios invitados y progreso")
 
    try:
        usuarios = sb.table('usuarios').select('*').eq('empresa_codigo', emp_codigo).execute().data
        respuestas = sb.table('respuestas').select('usuario_email,bloque').eq('empresa_codigo', emp_codigo).execute().data
    except Exception as e:
        st.error(f"Error: {e}")
        usuarios = []
        respuestas = []
 
    BLOQUES = {1:"Bloque 1 · I+D+i", 2:"Bloque 2 · Gest. Proyectos",
               3:"Bloque 3 · Dllo. Productos", 4:"Bloque 4 · Estrategia Inn.",
               5:"Bloque 5 · Desempeño Inn."}
 
    # Calcular progreso por usuario
    resp_por_usuario = {}
    for r in respuestas:
        email_r = r['usuario_email']
        bloque_r = r['bloque']
        if email_r not in resp_por_usuario:
            resp_por_usuario[email_r] = set()
        resp_por_usuario[email_r].add(bloque_r)
 
    # Mostrar tabla de progreso
    total_usuarios = len([u for u in usuarios if not u.get('es_admin')])
    completados_total = sum(1 for u in usuarios if not u.get('es_admin')
                           and len(resp_por_usuario.get(u['email'],set())) == 5)
 
    col1, col2, col3 = st.columns(3)
    col1.metric("Usuarios invitados", total_usuarios)
    col2.metric("Han completado todo", completados_total)
    col3.metric("Pendientes", total_usuarios - completados_total)
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    for u in usuarios:
        if u.get('es_admin'): continue
        email_u   = u['email']
        bloques_u = resp_por_usuario.get(email_u, set())
        completados = len(bloques_u)
        pct = int(completados / 5 * 100)
        color = "#10b981" if completados == 5 else "#f59e0b" if completados > 0 else "#94a3b8"
        estado = "✅ Completado" if completados == 5 else f"⏳ {completados}/5 bloques"
 
        st.markdown(f"""<div class="user-card">
          <div>
            <div style="font-weight:600;color:#1e293b;font-size:.92rem;">{email_u}</div>
            <div style="font-size:.78rem;color:#64748b;margin-top:2px;">
              {'  ·  '.join([BLOQUES[b] for b in sorted(bloques_u)]) if bloques_u else 'Sin respuestas aún'}
            </div>
          </div>
          <div style="text-align:right;min-width:120px;">
            <div style="font-size:.82rem;font-weight:700;color:{color};margin-bottom:4px;">{estado}</div>
            <div class="progress-bar-bg">
              <div style="background:{color};height:8px;width:{pct}%;border-radius:20px;"></div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
 
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Invitar nuevo usuario")
    col_a, col_b = st.columns([3,1])
    with col_a:
        nuevo_email = st.text_input("Email del nuevo usuario", placeholder="colaborador@empresa.com", label_visibility="collapsed")
    with col_b:
        if st.button("Invitar", use_container_width=True, type="primary"):
            if not nuevo_email:
                st.error("Introduce un email.")
            elif total_usuarios >= 5:
                st.error("Has alcanzado el límite de 5 usuarios.")
            else:
                try:
                    existe = sb.table('usuarios').select('id').eq('empresa_codigo', emp_codigo)\
                        .eq('email', nuevo_email.strip().lower()).execute()
                    if existe.data:
                        st.warning("Este email ya está invitado.")
                    else:
                        sb.table('usuarios').insert({
                            'empresa_codigo': emp_codigo,
                            'email': nuevo_email.strip().lower(),
                            'es_admin': False
                        }).execute()
                        st.success(f"✅ {nuevo_email} invitado correctamente.")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
 
    st.markdown(f"""<div style="background:#eff6ff;border-left:3px solid #3b82f6;border-radius:0 8px 8px 0;
        padding:10px 16px;margin-top:12px;color:#1d4ed8;font-size:.85rem;">
        💡 Comparte este código con tus colaboradores para que accedan: 
        <strong style="font-size:1rem;">{emp_codigo}</strong></div>""", unsafe_allow_html=True)
 
# ─────────────────────────────────────────────────────
# TAB 2 — DATOS EMPRESA
# ─────────────────────────────────────────────────────
with tab2:
    st.markdown("### Datos de clasificación y económicos")
    st.info("Estos datos son los que se usan para el benchmarking y los índices competitivos.")
 
    c1, c2 = st.columns(2)
    with c1:
        sector_idx = SECTORES.index(empresa.get('sector', SECTORES[0])) if empresa.get('sector') in SECTORES else 0
        sector_sel = st.selectbox("Sector", SECTORES, index=sector_idx)
        tam_idx = list(TAMANIOS.keys()).index(empresa.get('tamano', 'Pequeña')) if empresa.get('tamano') in TAMANIOS else 0
        tam_sel = st.selectbox("Tamaño", list(TAMANIOS.keys()), index=tam_idx)
        exp_idx = list(EXPORTACIONES.keys()).index(empresa.get('exportacion', 'Menos 10 %')) if empresa.get('exportacion') in EXPORTACIONES else 0
        exp_sel = st.selectbox("Exportación", list(EXPORTACIONES.keys()), index=exp_idx)
    with c2:
        anti_idx = list(ANTIGUEDADES.keys()).index(empresa.get('antiguedad', 'Menos 10 años')) if empresa.get('antiguedad') in ANTIGUEDADES else 0
        anti_sel = st.selectbox("Antigüedad", list(ANTIGUEDADES.keys()), index=anti_idx)
        reg_idx = list(REGIONES.keys()).index(empresa.get('region', 'Madrid')) if empresa.get('region') in REGIONES else 0
        reg_sel = st.selectbox("Región", list(REGIONES.keys()), index=reg_idx)
 
    st.markdown("#### Datos económicos")
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        ventas    = st.number_input("Ventas (miles €)", value=float(empresa.get('ventas',0) or 0), min_value=0.0)
        empleados = st.number_input("Empleados", value=int(empresa.get('empleados',0) or 0), min_value=0)
    with d2:
        roa      = st.number_input("ROA (%)", value=float(empresa.get('roa',0) or 0))
        var_vtas = st.number_input("Var. ventas 5 años (%)", value=float(empresa.get('var_ventas',0) or 0))
    with d3:
        var_empl  = st.number_input("Var. empleo 5 años (%)", value=float(empresa.get('var_empleados',0) or 0))
        productiv = round(ventas/empleados,2) if empleados>0 else 0.0
        st.metric("Productividad", f"{productiv:,.0f} €")
    with d4:
        coste_emp = st.number_input("Coste medio empleado (€)", value=float(empresa.get('coste_empleado',0) or 0))
        endeud    = st.number_input("Ratio endeudamiento", value=float(empresa.get('endeudamiento',0) or 0))
 
    if st.button("💾 Guardar datos empresa", use_container_width=True, type="primary"):
        try:
            sb.table('empresas').update({
                'sector': sector_sel, 'tamano': tam_sel, 'exportacion': exp_sel,
                'antiguedad': anti_sel, 'region': reg_sel, 'ventas': ventas,
                'empleados': empleados, 'roa': roa, 'var_ventas': var_vtas,
                'var_empleados': var_empl, 'productividad': productiv,
                'coste_empleado': coste_emp, 'endeudamiento': endeud
            }).eq('codigo', emp_codigo).execute()
            # Actualizar session_state
            st.session_state.update({
                'save_sector_nombre': sector_sel, 'save_tam_nombre': tam_sel,
                'save_reg_nombre': reg_sel, 'save_export_nombre': exp_sel,
                'save_anti_nombre': anti_sel, 'save_ventas': ventas,
                'save_empleados': empleados, 'save_roa': roa,
                'save_var_vtas': var_vtas, 'save_var_empl': var_empl,
                'save_productiv': productiv, 'save_coste_emp': coste_emp,
                'save_endeud': endeud,
                'save_reg_user': REGIONES[reg_sel], 'save_tam_user': TAMANIOS[tam_sel],
            })
            st.success("✅ Datos guardados correctamente.")
        except Exception as e:
            st.error(f"Error: {e}")
 
# ─────────────────────────────────────────────────────
# TAB 3 — RESULTADOS DEL EQUIPO
# ─────────────────────────────────────────────────────
with tab3:
    st.markdown("### Promedios del equipo")
    st.info("Solo se muestran promedios — las respuestas individuales son anónimas.")
 
    try:
        todas_resp = sb.table('respuestas').select('*').eq('empresa_codigo', emp_codigo).execute().data
    except Exception as e:
        st.error(f"Error: {e}")
        todas_resp = []
 
    if not todas_resp:
        st.warning("Aún no hay respuestas registradas.")
    else:
        # Calcular promedios por item
        from collections import defaultdict
        sumas   = defaultdict(list)
        for r in todas_resp:
            sumas[f"B{r['bloque']}_{r['item']}"].append(r['valor'])
        promedios = {k: round(sum(v)/len(v),2) for k,v in sumas.items()}
 
        # Calcular scores por bloque
        BLOQUES_NOMBRES = {1:"I+D+i", 2:"Gestión Proyectos", 3:"Desarrollo Productos",
                           4:"Estrategia Innovación", 5:"Desempeño Innovación"}
        scores_bloque = {}
        for b in range(1,6):
            items_b = [v for k,v in promedios.items() if k.startswith(f"B{b}_")]
            if items_b:
                scores_bloque[b] = round(sum(items_b)/len(items_b),2)
 
        if scores_bloque:
            st.markdown("#### Puntuación media por bloque (escala 1-5)")
            cols = st.columns(len(scores_bloque))
            for i, (b, score) in enumerate(scores_bloque.items()):
                pct = int((score-1)/4*100)
                color = "#10b981" if score>=3.5 else "#f59e0b" if score>=2.5 else "#ef4444"
                cols[i].markdown(f"""<div style="background:#f8fafc;border:1px solid #e2e8f0;
                    border-top:3px solid {color};border-radius:10px;padding:14px;text-align:center;">
                  <div style="font-size:.72rem;color:#64748b;font-weight:600;margin-bottom:4px;">
                    {BLOQUES_NOMBRES[b]}</div>
                  <div style="font-family:'Rajdhani',sans-serif;font-size:1.8rem;font-weight:700;color:{color};">
                    {score}</div>
                  <div style="font-size:.7rem;color:#94a3b8;">sobre 5</div>
                </div>""", unsafe_allow_html=True)
 
            # Guardar promedios en session_state para que los informes los usen
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Aplicar promedios del equipo a los informes", use_container_width=True, type="primary"):
                for b, score in scores_bloque.items():
                    st.session_state[f'score_b{b}'] = score
                # Calcular subindicadores
                for key, val in promedios.items():
                    st.session_state[f'prom_{key}'] = val
                st.success("✅ Promedios aplicados. Ahora los informes usarán los datos del equipo.")
        else:
            st.warning("No hay suficientes respuestas para calcular promedios.")
 
        # Registrar usuarios que han contribuido (sin mostrar respuestas individuales)
        emails_con_resp = set(r['usuario_email'] for r in todas_resp)
        st.markdown(f"""<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;
            padding:14px 18px;margin-top:16px;font-size:.85rem;color:#475569;">
            📊 Basado en respuestas de <strong>{len(emails_con_resp)} personas</strong>.
            Las respuestas individuales son confidenciales.</div>""", unsafe_allow_html=True)