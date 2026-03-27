import streamlit as st  # v2
import json, os

st.set_page_config(page_title="Diagnóstico Estratégico 360°", layout="wide")

REGIONES = {"Andalucia":1,"Aragon":2,"Asturias":3,"Baleares":4,"Canarias":5,"Cantabria":6,
    "Castilla la Mancha":7,"Castilla y León":8,"Cataluña":9,"Com Valenciana":10,
    "Extremadura":11,"Galicia":12,"Madrid":13,"Murcia":14,"Navarra":15,"Pais Vasco":16}
TAMANIOS = {"Pequeña":1,"Mediana":2,"Grande":3}
EXPORTACIONES = {"Menos 10 %":1,"10 - 30 %":2,"30 - 60 %":3,"> 60 %":4}
ANTIGUEDADES = {"Menos 10 años":1,"10-30 años":2,"> 30 años":3}

PERFIL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'perfil_empresa.json')

def cargar_perfil():
    if os.path.exists(PERFIL_FILE):
        with open(PERFIL_FILE,'r',encoding='utf-8') as f: return json.load(f)
    return {}

def guardar_perfil(datos):
    with open(PERFIL_FILE,'w',encoding='utf-8') as f: json.dump(datos,f,ensure_ascii=False,indent=2)

# ── Cargar perfil local ───────────────────────────────────────────────────────
perfil = cargar_perfil()
for k,v in perfil.items():
    if k not in st.session_state: st.session_state[k] = v

# ── Restaurar sesión desde perfil local ───────────────────────────────────────
if not st.session_state.get('usuario_email') and perfil.get('sesion_email'):
    st.session_state['usuario_email']  = perfil['sesion_email']
    st.session_state['empresa_codigo'] = perfil.get('sesion_codigo','')
    st.session_state['es_admin']       = perfil.get('sesion_es_admin', False)
    st.session_state['usuario_nombre'] = perfil.get('sesion_nombre','')
    st.session_state['usuario_rol']    = perfil.get('sesion_rol','colaborador')

# ── Cargar datos de empresa desde Supabase si no están ───────────────────────
def cargar_desde_supabase():
    ec = st.session_state.get('empresa_codigo')
    if not ec: return
    if st.session_state.get('save_reg_user') and st.session_state.get('save_sector_nombre'): return
    try:
        from supabase import create_client
        url = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL",""))
        key = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY",""))
        if not url or not key: return
        sb = create_client(url, key)
        emp = sb.table('empresas').select('*').eq('codigo', ec).execute()
        if not emp.data: return
        e = emp.data[0]
        SECTOR_MAP = {"Alimentación y bebidas":1,"Textil y confección":2,"Cuero y calzado":3,
            "Química y plásticos":4,"Minerales no metálicos":5,"Metalmecanico":6,
            "Maquinaria equipo":7,"Otras manufacturas":8,"Electrónica, telecomunicaciones":9,
            "Informática, software. Robótica, IA":10,"Actividades I+D: biotech, farmacia":11,
            "Transporte y logística":12,"Consultoría y servicios profesionales":13,
            "Turismo y hosteleria":14,"Retail y comercio":15,"Otros servicios":16}
        MACRO_MAP = {1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:2,10:2,11:2,12:3,13:3,14:3,15:3,16:3}
        TAMANIOS_INV = {"Pequeña":1,"Mediana":2,"Grande":3}
        REGIONES_INV = {"Andalucia":1,"Aragon":2,"Asturias":3,"Baleares":4,"Canarias":5,
            "Cantabria":6,"Castilla la Mancha":7,"Castilla y León":8,"Cataluña":9,
            "Com Valenciana":10,"Extremadura":11,"Galicia":12,"Madrid":13,
            "Murcia":14,"Navarra":15,"Pais Vasco":16}
        EXPORT_INV = {"Menos 10 %":1,"10 - 30 %":2,"30 - 60 %":3,"> 60 %":4}
        ANTI_INV = {"Menos 10 años":1,"10-30 años":2,"> 30 años":3}
        sector_cod = SECTOR_MAP.get(e.get('sector',''), 0)
        macro_cod  = MACRO_MAP.get(sector_cod, 3)
        datos = {
            'save_sector_nombre': e.get('sector',''),
            'save_tam_nombre':    e.get('tamano',''),
            'save_reg_nombre':    e.get('region',''),
            'save_export_nombre': e.get('exportacion',''),
            'save_anti_nombre':   e.get('antiguedad',''),
            'save_ventas':        float(e.get('ventas') or 0),
            'save_empleados':     int(e.get('empleados') or 0),
            'save_roa':           float(e.get('roa') or 0),
            'save_var_vtas':      float(e.get('var_ventas') or 0),
            'save_var_empl':      float(e.get('var_empleados') or 0),
            'save_productiv':     float(e.get('productividad') or 0),
            'save_coste_emp':     float(e.get('coste_empleado') or 0),
            'save_endeud':        float(e.get('endeudamiento') or 0),
            'save_reg_user':      REGIONES_INV.get(e.get('region',''), 0),
            'save_tam_user':      TAMANIOS_INV.get(e.get('tamano',''), 0),
            'save_sector_cod':    sector_cod,
            'save_macro_cod':     macro_cod,
            'save_export_cod':    EXPORT_INV.get(e.get('exportacion',''), 0),
            'save_anti_cod':      ANTI_INV.get(e.get('antiguedad',''), 0),
        }
        st.session_state.update(datos)
        # Cargar scores si hay respuestas
        if not st.session_state.get('score_b1'):
            resp = sb.table('respuestas').select('*').eq('empresa_codigo', ec).execute().data or []
            if resp:
                from collections import defaultdict
                sumas = defaultdict(list)
                for r in resp:
                    sumas[f"B{r['bloque']}_{r['item']}"].append(r['valor'])
                promedios = {k: round(sum(v)/len(v),2) for k,v in sumas.items()}
                for b in range(1,6):
                    items_b = [v for k,v in promedios.items() if k.startswith(f"B{b}_")]
                    if items_b: st.session_state[f'score_b{b}'] = round(sum(items_b)/len(items_b),2)
                bloques = set(r['bloque'] for r in resp)
                if len(bloques) >= 5: st.session_state['informes_activados'] = True
    except Exception:
        pass

cargar_desde_supabase()

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.hero-box {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    border-radius: 16px; padding: 40px; text-align: center; color: white; margin-bottom: 20px;
}
.hero-title { font-size: 2.8rem; font-weight: 800; margin-bottom: 10px; color: white; }
.hero-subtitle { font-size: 1.2rem; color: #a8d8ea; margin-bottom: 20px; }
.feature-box {
    background: #f0f4ff; border-radius: 12px; padding: 20px; text-align: center;
    border-top: 4px solid #1E3A8A; height: 100%;
}
.feature-icon { font-size: 2.5rem; margin-bottom: 10px; }
.feature-title { font-weight: 700; color: #1E3A8A; font-size: 1rem; margin-bottom: 8px; }
.feature-text { color: #475569; font-size: 0.85rem; }
.step-box {
    background: white; border-radius: 10px; padding: 15px;
    border-left: 5px solid #10B981; margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── Mostrar sesión activa ─────────────────────────────────────────────────────
usuario_email  = st.session_state.get('usuario_email','')
empresa_codigo = st.session_state.get('empresa_codigo','')
if usuario_email and empresa_codigo:
    es_admin = st.session_state.get('es_admin', False)
    rol = "Administrador" if es_admin else st.session_state.get('usuario_rol','Colaborador').capitalize()
    st.markdown(f"""<div style="background:#f0fdf4;border:1px solid #10b981;border-radius:8px;
        padding:8px 16px;margin-bottom:12px;font-size:.84rem;color:#065f46;display:flex;justify-content:space-between;align-items:center;">
        <span>✅ Sesión activa · <strong>{usuario_email}</strong> · {rol} · Empresa <strong>{empresa_codigo}</strong></span>
    </div>""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
    <div class="hero-title">🏆 Diagnóstico Estratégico 360°</div>
    <div class="hero-subtitle">Tu consultor estratégico personalizado con Inteligencia Artificial</div>
    <p style="color:#cbd5e1; font-size:1rem; max-width:700px; margin:auto;">
        La única plataforma que combina <strong style="color:white;">diagnóstico integral automatizado</strong>, 
        <strong style="color:white;">análisis comparativo</strong> con más de 1.000 empresas y 
        <strong style="color:white;">recomendaciones estratégicas personalizadas</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

# ── 4 CARACTERÍSTICAS ─────────────────────────────────────────────────────────
c1,c2,c3,c4 = st.columns(4)
with c1:
    st.markdown('<div class="feature-box"><div class="feature-icon">🔬</div><div class="feature-title">Diagnóstico Integral</div><div class="feature-text">Evalúa tu empresa en Innovación, Estrategia y Transformación Digital.</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="feature-box"><div class="feature-icon">📊</div><div class="feature-title">Dashboards Comparativos</div><div class="feature-text">Compara tu posición con empresas de tu sector, región y tamaño.</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="feature-box"><div class="feature-icon">🤖</div><div class="feature-title">IA y Predicciones</div><div class="feature-text">Recomendaciones estratégicas basadas en 1.000 empresas de referencia.</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="feature-box"><div class="feature-icon">📄</div><div class="feature-title">Informes PDF</div><div class="feature-text">Genera informes ejecutivos descargables con recomendaciones personalizadas.</div></div>', unsafe_allow_html=True)

st.divider()

# ── CÓMO FUNCIONA ─────────────────────────────────────────────────────────────
st.markdown("### 🗺️ ¿Cómo funciona?")
p1,p2,p3,p4 = st.columns(4)
with p1:
    st.markdown('<div class="step-box"><strong>Paso 1 · Registro</strong><br><span style="color:#475569;font-size:0.9rem;">Registra tu empresa y accede con tu código</span></div>', unsafe_allow_html=True)
with p2:
    st.markdown('<div class="step-box"><strong>Paso 2 · Cuestionario</strong><br><span style="color:#475569;font-size:0.9rem;">Responde los bloques del área a diagnosticar</span></div>', unsafe_allow_html=True)
with p3:
    st.markdown('<div class="step-box"><strong>Paso 3 · Dashboard</strong><br><span style="color:#475569;font-size:0.9rem;">Visualiza tu posición en dashboards comparativos</span></div>', unsafe_allow_html=True)
with p4:
    st.markdown('<div class="step-box"><strong>Paso 4 · Informe</strong><br><span style="color:#475569;font-size:0.9rem;">Descarga tu informe ejecutivo personalizado</span></div>', unsafe_allow_html=True)

st.divider()

# ── ESTADO DEL DIAGNÓSTICO ────────────────────────────────────────────────────
if st.session_state.get('save_reg_user'):
    st.markdown("### ✅ Perfil completado — ¡Listo para el diagnóstico!")
    col1,col2,col3,col4 = st.columns(4)
    col1.metric("Sector", st.session_state.get('save_sector_nombre','-')[:25])
    col2.metric("Tamaño", st.session_state.get('save_tam_nombre','-'))
    col3.metric("Región", st.session_state.get('save_reg_nombre','-'))
    col4.metric("Ventas (miles €)", f"{st.session_state.get('save_ventas',0):,.0f}")

    # Mostrar progreso de bloques
    st.markdown("#### Progreso del cuestionario de innovación:")
    b_cols = st.columns(5)
    for i in range(1,6):
        score = st.session_state.get(f'score_b{i}', 0)
        completado = score > 0
        color = "#10b981" if completado else "#94a3b8"
        estado = f"{score:.2f}/5" if completado else "Pendiente"
        b_cols[i-1].markdown(f"""<div style="background:#f8fafc;border:1px solid #e2e8f0;
            border-top:3px solid {color};border-radius:10px;padding:10px;text-align:center;">
          <div style="font-size:.72rem;color:#64748b;">Bloque {i}</div>
          <div style="font-weight:700;color:{color};font-size:.9rem;">{estado}</div>
        </div>""", unsafe_allow_html=True)

    if st.session_state.get('informes_activados'):
        st.success("✅ Informes e índices activados — puedes acceder a todos los resultados desde el menú lateral.")
    else:
        st.info("💡 Completa los 5 bloques y el administrador activará los informes desde **Mi Empresa**.")
else:
    st.warning("⚠️ Para iniciar tu diagnóstico, ve a **Registro Empresa** para crear tu cuenta o a **Acceso** si ya tienes un código.")
    col_a, col_b = st.columns(2)
    with col_a:
        st.page_link("pages/00_Registro_Empresa.py", label="🏢 Registrar nueva empresa", use_container_width=True)
    with col_b:
        st.page_link("pages/00_Acceso.py", label="🔑 Acceder con código de empresa", use_container_width=True)