import streamlit as st
import requests
import os
import base64

def _get_api_key():
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        pass
    return os.environ.get("ANTHROPIC_API_KEY","")

def _imagen_base64(nombre):
    base = os.path.dirname(os.path.abspath(__file__))
    for ruta in [
        os.path.join(base, 'assets', nombre),
        os.path.join('/mount/src/nuevo-bidin/assets', nombre),
    ]:
        if os.path.exists(ruta):
            with open(ruta, 'rb') as f:
                return base64.b64encode(f.read()).decode()
    return None

def _llamar_ia(system_prompt, messages, max_tokens=500):
    api_key = _get_api_key()
    if not api_key:
        return "Lo siento, no puedo responder en este momento."
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type":"application/json","x-api-key":api_key,"anthropic-version":"2023-06-01"},
            json={"model":"claude-sonnet-4-20250514","max_tokens":max_tokens,
                  "system":system_prompt,"messages":messages},
            timeout=30
        )
        data = resp.json()
        if data.get('content'): return data['content'][0]['text']
        return "Lo siento, no puedo responder en este momento."
    except Exception:
        return "Lo siento, no puedo responder en este momento."

MELISSA_SYSTEM = """Eres Melissa, guía profesional de la plataforma de Diagnóstico Estratégico 360°.
Tu rol es dar la bienvenida al usuario y guiarle para empezar.

PERSONALIDAD: Profesional, clara, cercana pero seria. Directiva experimentada.

SOBRE LA PLATAFORMA:
- Motor de inteligencia competitiva único a nivel internacional
- Diagnósticos 360° en múltiples áreas estratégicas
- Compara con más de 1.000 empresas auditadas de referencia
- Genera índices, informes, benchmarking y planes de acción con IA
- TOTAL ANONIMATO: los datos individuales nunca se divulgan
- Tiempo estimado cuestionario innovación: 10-15 minutos

SECCIONES:
1. Registro Empresa: el admin crea la empresa y obtiene código único
2. Acceso: todos entran con email + código de empresa
3. Mi Empresa: admin gestiona equipo, roles, activa informes
4. Cuestionario Innovación: 5 bloques sencillos (escala 1-5)
5. Índices Estratégicos: 6 índices competitivos + Score Global SSG
6. Informes con IA: Estratégico, Innovación, Global
7. Analytics, Benchmarking y Plan de Acción

ROLES:
- Admin: gestiona equipo, ve promedios, activa informes
- Manager: ve índices, analytics y promedios
- Colaborador: solo cumplimenta cuestionarios

INSTRUCCIONES: Respuestas máximo 3-4 frases. Lenguaje profesional pero accesible. Anima a empezar."""

def _felix_system(pagina=""):
    sector = st.session_state.get('save_sector_nombre','tu empresa')
    tam = st.session_state.get('save_tam_nombre','')
    reg = st.session_state.get('save_reg_nombre','')
    scores = [st.session_state.get(f'score_b{i}',0) for i in range(1,6)]
    completados = sum(1 for s in scores if s > 0)
    return f"""Eres Félix, consultor estratégico senior de la plataforma de Diagnóstico Estratégico 360°.

PERSONALIDAD: Consultor profesional, amable y cercano de 35 años. Experto en competitividad e innovación. Directo, preciso, constructivo. Nunca alarmista.

CONTEXTO EMPRESA: {sector} | {tam} | {reg} | Bloques completados: {completados}/5 | Página: {pagina}

COMPORTAMIENTO:
- Saluda proactivamente y explica qué encontrará en esta sección
- Si hay bloques sin completar, anima a completarlos
- Usa lenguaje descriptivo, NO "percentil 13", SÍ "por debajo de la media"
- Personaliza siempre con el sector de la empresa
- Máximo 3-4 frases por respuesta
- Tono consultor senior, nunca genérico
- PROHIBIDO: "alarmante", "catastrófico", "urgente"
- USA: "margen de mejora", "posición sólida", "área prioritaria"

MENSAJE INICIAL SEGÚN SECCIÓN:
- indices: Explica los 6 índices competitivos y el SSG, anima a interpretar su posición
- informe_estrategico: Explica que pulse Generar Informe para obtener análisis IA completo
- informe_innovacion: Explica diagnóstico detallado por bloques y subindicadores
- plan: Explica que generará plan 12 meses + hoja de ruta 1-3 años personalizada
- benchmarking: Explica comparativa con empresas líderes del sector
- analytics: Explica visualizaciones detalladas de todos los indicadores"""

def _header_html(img_src, nombre, subtitulo, color):
    img_tag = f'<img src="data:image/png;base64,{img_src}" style="width:44px;height:44px;border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,0.5);">' if img_src else f'<div style="width:44px;height:44px;border-radius:50%;background:{color};"></div>'
    return f"""<div style="background:{color};border-radius:12px 12px 0 0;padding:12px 16px;display:flex;align-items:center;gap:10px;">
        {img_tag}
        <div>
            <div style="font-weight:700;color:#fff;font-size:.95rem;">{nombre}</div>
            <div style="color:rgba(255,255,255,0.8);font-size:.72rem;">{subtitulo}</div>
        </div>
    </div>"""

def _mensajes_html(msgs):
    html = ""
    for m in msgs[-6:]:
        if m['role'] == 'assistant':
            html += f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px 12px 12px 2px;padding:10px 14px;font-size:.84rem;color:#1e293b;line-height:1.6;margin-bottom:8px;max-width:90%;">{m["content"]}</div>'
        else:
            html += f'<div style="background:#1e40af;color:#fff;border-radius:12px 12px 2px 12px;padding:10px 14px;font-size:.84rem;line-height:1.6;margin-bottom:8px;max-width:90%;align-self:flex-end;margin-left:auto;">{m["content"]}</div>'
    return f'<div style="background:#f8fafc;padding:12px;max-height:280px;overflow-y:auto;display:flex;flex-direction:column;">{html}</div>'

# ══════════════════════════════════════════════════════════════════════════
# MELISSA
# ══════════════════════════════════════════════════════════════════════════
def mostrar_melissa():
    if 'melissa_msgs' not in st.session_state:
        st.session_state['melissa_msgs'] = [{"role":"assistant","content":"¡Bienvenido/a a la plataforma de Diagnóstico Estratégico 360°! Soy Melissa, tu guía profesional. Esta plataforma es un motor de inteligencia competitiva único que te permitirá conocer el posicionamiento real de tu empresa comparado con más de 1.000 empresas. ¿Te explico cómo empezar?"}]
    if 'melissa_visible' not in st.session_state:
        st.session_state['melissa_visible'] = True

    img_b64 = _imagen_base64('melissa.png')

    st.markdown("---")
    col_titulo, col_toggle = st.columns([4,1])
    with col_titulo:
        st.markdown("### 💬 Melissa — Tu guía profesional")
    with col_toggle:
        label = "▲ Ocultar" if st.session_state['melissa_visible'] else "▼ Mostrar"
        if st.button(label, key="melissa_toggle"):
            st.session_state['melissa_visible'] = not st.session_state['melissa_visible']
            st.rerun()

    if st.session_state['melissa_visible']:
        st.markdown(_header_html(img_b64, "Melissa", "Tu guía profesional", "#065f46"), unsafe_allow_html=True)
        st.markdown(_mensajes_html(st.session_state['melissa_msgs']), unsafe_allow_html=True)

        # Botones rápidos
        st.markdown("**Preguntas frecuentes:**")
        c1, c2, c3, c4 = st.columns(4)
        preguntas = {
            "¿Cómo empiezo?": c1,
            "¿Qué obtengo?": c2,
            "¿Mis datos?": c3,
            "¿Los roles?": c4,
        }
        for pregunta, col in preguntas.items():
            with col:
                if st.button(pregunta, key=f"mq_{pregunta}", use_container_width=True):
                    st.session_state['melissa_msgs'].append({"role":"user","content":pregunta})
                    with st.spinner(""):
                        resp = _llamar_ia(MELISSA_SYSTEM, st.session_state['melissa_msgs'])
                    st.session_state['melissa_msgs'].append({"role":"assistant","content":resp})
                    st.rerun()

        # Input libre
        user_input = st.chat_input("Escribe tu pregunta a Melissa...", key="melissa_chat")
        if user_input:
            st.session_state['melissa_msgs'].append({"role":"user","content":user_input})
            with st.spinner("Melissa está escribiendo..."):
                resp = _llamar_ia(MELISSA_SYSTEM, st.session_state['melissa_msgs'])
            st.session_state['melissa_msgs'].append({"role":"assistant","content":resp})
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════
# FÉLIX
# ══════════════════════════════════════════════════════════════════════════
def mostrar_felix(pagina=""):
    key_msgs = f'felix_msgs_{pagina}'
    key_vis  = f'felix_vis_{pagina}'

    if key_msgs not in st.session_state:
        sector = st.session_state.get('save_sector_nombre','tu empresa')
        completados = sum(1 for i in range(1,6) if st.session_state.get(f'score_b{i}',0)>0)
        bienvenidas = {
            'indices': f"Hola, soy Félix. Estás en Índices Estratégicos, donde puedes ver la posición competitiva de {sector} en 6 dimensiones clave. Tienes {completados} de 5 bloques completados. ¿Quieres que te explique qué significa cada índice?",
            'informe_estrategico': f"Hola, soy Félix. El Informe Estratégico analiza con IA la posición competitiva global de {sector}. Pulsa 'Generar Informe' y en unos segundos tendrás un análisis ejecutivo completo. ¿Empezamos?",
            'informe_innovacion': f"Hola, soy Félix. Este es el Informe de Innovación de {sector}, con análisis detallado por los 5 bloques. ¿Quieres que te explique cómo interpretar los indicadores?",
            'plan': f"Hola, soy Félix. Estás en el Plan de Acción y Hoja de Ruta — uno de los documentos más valiosos. Generará 5 acciones prioritarias para {sector} más una hoja de ruta 1-3 años. ¿Generamos el plan?",
            'benchmarking': f"Hola, soy Félix. En Benchmarking puedes comparar {sector} con las empresas líderes de tu sector. ¿Quieres que te explique cómo usar los filtros?",
            'analytics': f"Hola, soy Félix. En Analytics encontrarás visualizaciones detalladas de todos tus indicadores. ¿En qué quieres que te ayude?",
        }
        msg = bienvenidas.get(pagina, f"Hola, soy Félix, tu consultor estratégico. Estoy aquí para ayudarte en esta sección. ¿En qué puedo ayudarte?")
        st.session_state[key_msgs] = [{"role":"assistant","content":msg}]

    if key_vis not in st.session_state:
        st.session_state[key_vis] = True

    img_b64 = _imagen_base64('felix.png')

    st.markdown("---")
    col_titulo, col_toggle = st.columns([4,1])
    with col_titulo:
        st.markdown("### 💼 Félix — Tu asesor estratégico")
    with col_toggle:
        label = "▲ Ocultar" if st.session_state[key_vis] else "▼ Mostrar"
        if st.button(label, key=f"felix_toggle_{pagina}"):
            st.session_state[key_vis] = not st.session_state[key_vis]
            st.rerun()

    if st.session_state[key_vis]:
        st.markdown(_header_html(img_b64, "Félix", "Tu asesor estratégico", "#1e3a5f"), unsafe_allow_html=True)
        st.markdown(_mensajes_html(st.session_state[key_msgs]), unsafe_allow_html=True)

        user_input = st.chat_input("Pregunta a Félix...", key=f"felix_chat_{pagina}")
        if user_input:
            st.session_state[key_msgs].append({"role":"user","content":user_input})
            with st.spinner("Félix está analizando..."):
                resp = _llamar_ia(_felix_system(pagina), st.session_state[key_msgs])
            st.session_state[key_msgs].append({"role":"assistant","content":resp})
            st.rerun()