import streamlit as st
import json, os
import sys

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
}
.seccion {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 14px; padding: 24px 28px; margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ── Supabase ───────────────────────────────────────────────────────────────────
def get_supabase():
    try:
        from supabase import create_client
        url = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL",""))
        key = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY",""))
        if url and key: return create_client(url, key)
    except Exception: pass
    return None

PERFIL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'perfil_empresa.json')
def cargar_perfil():
    if os.path.exists(PERFIL_FILE):
        with open(PERFIL_FILE,'r',encoding='utf-8') as f: return json.load(f)
    return {}
def guardar_perfil(datos):
    perfil = cargar_perfil(); perfil.update(datos)
    with open(PERFIL_FILE,'w',encoding='utf-8') as f: json.dump(perfil,f,ensure_ascii=False,indent=2)

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

ROLES = {"colaborador": "👤 Colaborador", "manager": "📊 Manager", "admin": "⚙️ Admin"}

# ── Verificar sesión admin ─────────────────────────────────────────────────────
es_admin   = st.session_state.get('es_admin', False)
emp_codigo = st.session_state.get('empresa_codigo', '')
usr_email  = st.session_state.get('usuario_email', '')

if not usr_email:
    st.warning("⚠️ Debes acceder primero desde la página **Acceso**.")
    st.stop()
if not es_admin:
    st.error("🔒 Solo el administrador de la empresa puede acceder a esta página.")
    st.stop()

sb = get_supabase()
if not sb:
    st.error("Error de conexión con la base de datos.")
    st.stop()

try:
    emp_data = sb.table('empresas').select('*').eq('codigo', emp_codigo).execute()
    empresa  = emp_data.data[0] if emp_data.data else {}
except Exception as e:
    st.error(f"Error cargando empresa: {e}")
    st.stop()

# ── Cabecera ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="admin-header">
  <div style="font-size:.68rem;color:#4a6fa5;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px;">
    Panel de Administración</div>
  <h1 style="font-family:'Rajdhani',sans-serif;color:#00d4ff;font-size:1.8rem;margin:0 0 4px;">
    Mi Empresa · {emp_codigo}</h1>
  <p style="color:#94a3b8;margin:0;font-size:.88rem;">Admin: {usr_email}</p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["👥 Equipo y progreso", "🏢 Datos de la empresa", "📊 Promedios y resultados"])

# ─────────────────────────────────────────────────────
# TAB 1 — EQUIPO Y PROGRESO
# ─────────────────────────────────────────────────────
with tab1:
    st.markdown("### Seguimiento del equipo")

    try:
        usuarios   = sb.table('usuarios').select('*').eq('empresa_codigo', emp_codigo).execute().data or []
        respuestas = sb.table('respuestas').select('usuario_email,bloque').eq('empresa_codigo', emp_codigo).execute().data or []
    except Exception as e:
        st.error(f"Error: {e}")
        usuarios = []; respuestas = []

    BLOQUES = {1:"Bloque 1 · I+D+i", 2:"Bloque 2 · Gest. Proyectos",
               3:"Bloque 3 · Dllo. Productos", 4:"Bloque 4 · Estrategia Inn.",
               5:"Bloque 5 · Desempeño Inn."}

    resp_por_usuario = {}
    for r in respuestas:
        email_r = r['usuario_email']
        if email_r not in resp_por_usuario: resp_por_usuario[email_r] = set()
        resp_por_usuario[email_r].add(r['bloque'])

    colaboradores = [u for u in usuarios if not u.get('es_admin')]
    total = len(colaboradores)
    completados = sum(1 for u in colaboradores if len(resp_por_usuario.get(u['email'],set()))==5)

    c1,c2,c3 = st.columns(3)
    c1.metric("Usuarios invitados", total)
    c2.metric("Han completado todo", completados)
    c3.metric("Pendientes", total-completados)

    st.markdown("<br>", unsafe_allow_html=True)

    # Lista de usuarios con progreso y selector de rol
    for u in usuarios:
        if u.get('es_admin'): continue
        email_u   = u['email']
        bloques_u = resp_por_usuario.get(email_u, set())
        completados_u = len(bloques_u)
        pct = int(completados_u/5*100)
        color = "#10b981" if completados_u==5 else "#f59e0b" if completados_u>0 else "#94a3b8"
        estado = "✅ Completado" if completados_u==5 else f"⏳ {completados_u}/5 bloques"
        rol_actual = u.get('rol', 'colaborador')

        col_info, col_rol = st.columns([3,1])
        with col_info:
            st.markdown(f"""<div class="user-card">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                  <div style="font-weight:600;color:#1e293b;font-size:.92rem;">{email_u}</div>
                  <div style="font-size:.78rem;color:#64748b;margin-top:2px;">
                    {', '.join([BLOQUES[b] for b in sorted(bloques_u)]) if bloques_u else 'Sin respuestas aún'}
                  </div>
                </div>
                <div style="text-align:right;min-width:120px;">
                  <div style="font-size:.82rem;font-weight:700;color:{color};margin-bottom:4px;">{estado}</div>
                  <div style="background:#e2e8f0;border-radius:20px;height:6px;">
                    <div style="background:{color};height:6px;width:{pct}%;border-radius:20px;"></div>
                  </div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)
        with col_rol:
            nuevo_rol = st.selectbox(
                f"Rol {email_u}",
                options=list(ROLES.keys()),
                format_func=lambda x: ROLES[x],
                index=list(ROLES.keys()).index(rol_actual),
                key=f"rol_{email_u}",
                label_visibility="collapsed"
            )
            if nuevo_rol != rol_actual:
                if st.button("Guardar", key=f"save_rol_{email_u}", use_container_width=True):
                    try:
                        sb.table('usuarios').update({'rol': nuevo_rol})\
                            .eq('empresa_codigo', emp_codigo).eq('email', email_u).execute()
                        st.success(f"Rol actualizado a {ROLES[nuevo_rol]}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Invitar nuevo usuario
    st.markdown("#### Invitar nuevo usuario")
    col_a, col_b = st.columns([3,1])
    with col_a:
        nuevo_email = st.text_input("Email", placeholder="colaborador@empresa.com", label_visibility="collapsed")
    with col_b:
        if st.button("Invitar", use_container_width=True, type="primary"):
            if not nuevo_email:
                st.error("Introduce un email.")
            elif len(colaboradores) >= 5:
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
                            'es_admin': False,
                            'rol': 'colaborador'
                        }).execute()
                        st.success(f"✅ {nuevo_email} invitado correctamente.")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown(f"""<div style="background:#eff6ff;border-left:3px solid #3b82f6;border-radius:0 8px 8px 0;
        padding:10px 16px;margin-top:12px;color:#1d4ed8;font-size:.85rem;">
        💡 Código de empresa para compartir: <strong style="font-size:1rem;">{emp_codigo}</strong></div>""",
        unsafe_allow_html=True)

    # Leyenda de roles
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:14px 18px;">
    <div style="font-weight:600;color:#1e293b;margin-bottom:8px;">Niveles de acceso:</div>
    <div style="font-size:.85rem;color:#475569;line-height:1.8;">
      👤 <strong>Colaborador</strong> — Solo puede contestar los bloques del cuestionario<br>
      📊 <strong>Manager</strong> — Puede ver promedios, índices y analytics<br>
      ⚙️ <strong>Admin</strong> — Acceso completo a todos los informes y gestión del equipo
    </div></div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# TAB 2 — DATOS EMPRESA
# ─────────────────────────────────────────────────────
with tab2:
    st.markdown("### Datos de clasificación y económicos")
    st.info("Estos datos se usan para el benchmarking y los índices competitivos.")

    c1,c2 = st.columns(2)
    with c1:
        sector_idx = SECTORES.index(empresa.get('sector',SECTORES[0])) if empresa.get('sector') in SECTORES else 0
        sector_sel = st.selectbox("Sector", SECTORES, index=sector_idx)
        tam_idx = list(TAMANIOS.keys()).index(empresa.get('tamano','Pequeña')) if empresa.get('tamano') in TAMANIOS else 0
        tam_sel = st.selectbox("Tamaño", list(TAMANIOS.keys()), index=tam_idx)
        exp_idx = list(EXPORTACIONES.keys()).index(empresa.get('exportacion','Menos 10 %')) if empresa.get('exportacion') in EXPORTACIONES else 0
        exp_sel = st.selectbox("Exportación", list(EXPORTACIONES.keys()), index=exp_idx)
    with c2:
        anti_idx = list(ANTIGUEDADES.keys()).index(empresa.get('antiguedad','Menos 10 años')) if empresa.get('antiguedad') in ANTIGUEDADES else 0
        anti_sel = st.selectbox("Antigüedad", list(ANTIGUEDADES.keys()), index=anti_idx)
        reg_idx = list(REGIONES.keys()).index(empresa.get('region','Madrid')) if empresa.get('region') in REGIONES else 0
        reg_sel = st.selectbox("Región", list(REGIONES.keys()), index=reg_idx)

    st.markdown("#### Datos económicos")
    d1,d2,d3,d4 = st.columns(4)
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
                'sector':sector_sel,'tamano':tam_sel,'exportacion':exp_sel,
                'antiguedad':anti_sel,'region':reg_sel,'ventas':ventas,
                'empleados':empleados,'roa':roa,'var_ventas':var_vtas,
                'var_empleados':var_empl,'productividad':productiv,
                'coste_empleado':coste_emp,'endeudamiento':endeud
            }).eq('codigo',emp_codigo).execute()
            st.session_state.update({
                'save_sector_nombre':sector_sel,'save_tam_nombre':tam_sel,
                'save_reg_nombre':reg_sel,'save_export_nombre':exp_sel,
                'save_anti_nombre':anti_sel,'save_ventas':ventas,
                'save_empleados':empleados,'save_roa':roa,
                'save_var_vtas':var_vtas,'save_var_empl':var_empl,
                'save_productiv':productiv,'save_coste_emp':coste_emp,
                'save_endeud':endeud,'save_reg_user':REGIONES[reg_sel],
                'save_tam_user':TAMANIOS[tam_sel],
            })
            guardar_perfil({
                'save_sector_nombre':sector_sel,'save_tam_nombre':tam_sel,
                'save_reg_nombre':reg_sel,'save_export_nombre':exp_sel,
                'save_anti_nombre':anti_sel,'save_ventas':ventas,
                'save_empleados':empleados,'save_roa':roa,
                'save_var_vtas':var_vtas,'save_var_empl':var_empl,
                'save_productiv':productiv,'save_coste_emp':coste_emp,
                'save_endeud':endeud,'save_reg_user':REGIONES[reg_sel],
                'save_tam_user':TAMANIOS[tam_sel],
            })
            st.success("✅ Datos guardados correctamente.")
        except Exception as e:
            st.error(f"Error: {e}")

# ─────────────────────────────────────────────────────
# TAB 3 — PROMEDIOS Y RESULTADOS
# ─────────────────────────────────────────────────────
with tab3:
    st.markdown("### Promedios del equipo")
    st.info("Las respuestas individuales son anónimas. Solo se muestran promedios.")

    try:
        todas_resp = sb.table('respuestas').select('*').eq('empresa_codigo', emp_codigo).execute().data or []
    except Exception as e:
        st.error(f"Error: {e}")
        todas_resp = []

    if not todas_resp:
        st.warning("Aún no hay respuestas registradas.")
    else:
        from collections import defaultdict
        sumas = defaultdict(list)
        for r in todas_resp:
            sumas[f"B{r['bloque']}_{r['item']}"].append(r['valor'])
        promedios = {k: round(sum(v)/len(v),2) for k,v in sumas.items()}

        BLOQUES_NOMBRES = {1:"I+D+i",2:"Gestión Proyectos",3:"Desarrollo Productos",
                           4:"Estrategia Innovación",5:"Desempeño Innovación"}
        scores_bloque = {}
        for b in range(1,6):
            items_b = [v for k,v in promedios.items() if k.startswith(f"B{b}_")]
            if items_b: scores_bloque[b] = round(sum(items_b)/len(items_b),2)

        if scores_bloque:
            st.markdown("#### Puntuación media por bloque (escala 1-5)")
            cols = st.columns(len(scores_bloque))
            for i,(b,score) in enumerate(scores_bloque.items()):
                color = "#10b981" if score>=3.5 else "#f59e0b" if score>=2.5 else "#ef4444"
                cols[i].markdown(f"""<div style="background:#f8fafc;border:1px solid #e2e8f0;
                    border-top:3px solid {color};border-radius:10px;padding:14px;text-align:center;">
                  <div style="font-size:.72rem;color:#64748b;font-weight:600;">{BLOQUES_NOMBRES[b]}</div>
                  <div style="font-family:'Rajdhani',sans-serif;font-size:1.8rem;font-weight:700;color:{color};">
                    {score}</div>
                  <div style="font-size:.7rem;color:#94a3b8;">sobre 5</div>
                </div>""", unsafe_allow_html=True)

            emails_con_resp = set(r['usuario_email'] for r in todas_resp)
            usuarios_total  = len([u for u in usuarios if not u.get('es_admin')])
            todos_completaron = len(emails_con_resp) >= max(usuarios_total, 1)

            st.markdown("<br>", unsafe_allow_html=True)

            if not todos_completaron:
                st.warning(f"⏳ {len(emails_con_resp)} de {usuarios_total} usuarios han contestado. Cuando todos completen el cuestionario podrás generar los informes.")

            st.markdown("""<div style="background:#f0fdf4;border:2px solid #10b981;border-radius:14px;
                padding:20px 24px;margin-top:16px;">
              <div style="font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:700;color:#065f46;margin-bottom:6px;">
                🚀 Activar informes y resultados con promedios del equipo</div>
              <div style="color:#475569;font-size:.87rem;margin-bottom:14px;">
                Al activar, todos los índices, informes y plan de acción se calcularán con los promedios 
                del equipo. Los usuarios con rol Manager también podrán ver los índices y analytics.</div>
            </div>""", unsafe_allow_html=True)

            if st.button("📊 Calcular promedios y activar informes", use_container_width=True, type="primary"):
                for b,score in scores_bloque.items():
                    st.session_state[f'score_b{b}'] = score
                for key,val in promedios.items():
                    st.session_state[f'prom_{key}'] = val
                st.session_state['informes_activados'] = True
                st.session_state['promedios_activados'] = True
                guardar_perfil({
                    **{f'score_b{b}': score for b,score in scores_bloque.items()},
                    'informes_activados': True,
                    'promedios_activados': True,
                })
                # ── Añadir empresa al benchmark con peso 5.0 ──────────
                try:
                    SECTOR_MAP = {"Alimentación y bebidas":1,"Textil y confección":2,
                        "Cuero y calzado":3,"Química y plásticos":4,"Minerales no metálicos":5,
                        "Metalmecanico":6,"Maquinaria equipo":7,"Otras manufacturas":8,
                        "Electrónica, telecomunicaciones":9,"Informática, software. Robótica, IA":10,
                        "Actividades I+D: biotech, farmacia":11,"Transporte y logística":12,
                        "Consultoría y servicios profesionales":13,"Turismo y hosteleria":14,
                        "Retail y comercio":15,"Otros servicios":16}
                    MACRO_MAP = {1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:2,10:2,11:2,12:3,13:3,14:3,15:3,16:3}
                    sector_cod = SECTOR_MAP.get(empresa.get('sector',''),0)
                    macro_cod  = MACRO_MAP.get(sector_cod, 3)
                    sb.table('benchmark_empresas').upsert({
                        'id':            emp_codigo,
                        'macrosector':   macro_cod,
                        'sector':        sector_cod,
                        'tamano':        TAMANIOS.get(empresa.get('tamano','Pequeña'),1),
                        'exportacion':   EXPORTACIONES.get(empresa.get('exportacion','Menos 10 %'),1),
                        'antiguedad':    ANTIGUEDADES.get(empresa.get('antiguedad','Menos 10 años'),1),
                        'region':        REGIONES.get(empresa.get('region','Madrid'),1),
                        'ventas':        empresa.get('ventas'),
                        'empleados':     empresa.get('empleados'),
                        'roa':           empresa.get('roa'),
                        'var_ventas_5a': empresa.get('var_ventas'),
                        'var_emp_5a':    empresa.get('var_empleados'),
                        'prod_venta_emp':empresa.get('productividad'),
                        'coste_med_emp': empresa.get('coste_empleado'),
                        'ratio_endeudamiento':empresa.get('endeudamiento'),
                        'validada':      True,
                        'es_nueva':      True,
                        'pendiente_validar': True,
                        'peso':          5.0,
                    }).execute()
                    for key, valor in promedios.items():
                        parts = key.split('_', 1)
                        if len(parts) == 2:
                            sb.table('benchmark_indicadores').upsert({
                                'empresa_id': emp_codigo,
                                'modulo':     'innovacion',
                                'indicador':  parts[1],
                                'valor':      float(valor),
                                'peso':       5.0,
                            }, on_conflict='empresa_id,modulo,indicador').execute()
                    st.success("✅ ¡Promedios activados y empresa añadida al benchmark con peso 5x!")
                except Exception as e:
                    st.warning(f"⚠️ Promedios activados pero error al añadir al benchmark: {e}")
                    st.success("✅ ¡Promedios activados!")
                st.balloons()
        else:
            st.warning("No hay suficientes respuestas para calcular promedios.")