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

PERSONALIDAD: Profesional, clara, cercana pero seria. Directiva experimentada.

SOBRE LA PLATAFORMA:
- Motor de inteligencia competitiva único a nivel internacional
- Diagnósticos 360° en múltiples áreas estratégicas
- Compara con más de 1.000 empresas auditadas de referencia
- Genera índices, informes, benchmarking y planes de acción con IA
- TOTAL ANONIMATO: los datos individuales nunca se divulgan
- PRECIO: La plataforma está actualmente en etapa de introducción y es totalmente gratuita durante esta fase
- Tiempo estimado cuestionario innovación: 10-15 minutos

SECCIONES DEL MENÚ:
1. Registro Empresa: el admin crea la empresa y obtiene código único
2. Acceso: todos entran con email + código de empresa
3. Mi Empresa: admin gestiona equipo, roles, activa informes
4. Cuestionario Innovación: 5 bloques sencillos escala 1-5
5. Índices Estratégicos: 6 índices competitivos + Score Global SSG
6. Informe Estratégico: análisis competitivo con IA
7. Informe Innovación: diagnóstico innovación con IA
8. Plan de Acción: plan 12 meses + hoja de ruta 3 años con IA
9. Analytics y Benchmarking: comparativas sectoriales

ROLES:
- Admin: gestiona equipo, ve promedios, activa informes
- Manager: ve índices, analytics y promedios
- Colaborador: solo cumplimenta cuestionarios

INSTRUCCIONES: Respuestas máximo 3-4 frases. Lenguaje profesional pero accesible."""

FELIX_SYSTEM_BASE = """Eres Félix, consultor estratégico senior de la plataforma de Diagnóstico Estratégico 360°.

PERSONALIDAD: Consultor profesional, amable y cercano de 35 años. Experto en competitividad e innovación. Directo, preciso, constructivo.

INSTRUCCIONES:
- Máximo 3-4 frases por respuesta
- Tono consultor senior, nunca genérico
- Personaliza con el sector de la empresa
- PROHIBIDO: "alarmante", "catastrófico", "urgente"
- USA: "margen de mejora", "posición sólida", "área prioritaria" """

def _banner_asistente(img_b64, nombre, subtitulo, color, ultimo_msg):
    img_tag = f'<img src="data:image/png;base64,{img_b64}" style="width:52px;height:52px;border-radius:50%;object-fit:cover;border:3px solid #fff;flex-shrink:0;">' if img_b64 else f'<div style="width:52px;height:52px;border-radius:50%;background:{color};flex-shrink:0;"></div>'
    return f"""<div style="background:{color};border-radius:12px;padding:14px 18px;display:flex;align-items:center;gap:14px;margin-bottom:12px;">
        {img_tag}
        <div style="flex:1;min-width:0;">
            <div style="font-weight:700;color:#fff;font-size:.95rem;">{nombre} <span style="font-weight:400;font-size:.78rem;color:rgba(255,255,255,0.75);">— {subtitulo}</span></div>
            <div style="color:rgba(255,255,255,0.92);font-size:.82rem;line-height:1.5;margin-top:3px;">{ultimo_msg}</div>
        </div>
    </div>"""

# ══════════════════════════════════════════════════════════════════════════
# MELISSA
# ══════════════════════════════════════════════════════════════════════════
def mostrar_melissa():
    if 'melissa_msgs' not in st.session_state:
        st.session_state['melissa_msgs'] = [{"role":"assistant","content":"¡Bienvenido/a! Soy Melissa, tu guía profesional. Esta plataforma te permitirá conocer el posicionamiento real de tu empresa comparado con más de 1.000 empresas. ¿Te explico cómo empezar?"}]
    if 'melissa_expandida' not in st.session_state:
        st.session_state['melissa_expandida'] = False

    img_b64 = _imagen_base64('melissa.png')
    ultimo_msg = st.session_state['melissa_msgs'][-1]['content'][:120] + "..." if len(st.session_state['melissa_msgs'][-1]['content']) > 120 else st.session_state['melissa_msgs'][-1]['content']

    # Banner siempre visible
    st.markdown(_banner_asistente(img_b64, "Melissa", "Tu guía profesional", "#065f46", ultimo_msg), unsafe_allow_html=True)

    # Botón para expandir/contraer
    col_expand, col_reset = st.columns([3,1])
    with col_expand:
        label = "▲ Ocultar conversación" if st.session_state['melissa_expandida'] else "💬 Abrir conversación con Melissa"
        if st.button(label, key="melissa_expand", use_container_width=True, type="secondary"):
            st.session_state['melissa_expandida'] = not st.session_state['melissa_expandida']
            st.rerun()
    with col_reset:
        if st.button("↺ Reiniciar", key="melissa_reset", use_container_width=True):
            st.session_state['melissa_msgs'] = [{"role":"assistant","content":"¡Hola de nuevo! ¿En qué puedo ayudarte?"}]
            st.rerun()

    if st.session_state['melissa_expandida']:
        # Mostrar historial
        for m in st.session_state['melissa_msgs'][-6:]:
            if m['role'] == 'assistant':
                with st.chat_message("assistant", avatar=f"data:image/png;base64,{img_b64}" if img_b64 else "🧑‍💼"):
                    st.write(m['content'])
            else:
                with st.chat_message("user"):
                    st.write(m['content'])

        # Botones rápidos
        st.markdown("**Preguntas frecuentes:**")
        c1, c2, c3, c4 = st.columns(4)
        preguntas = [
            ("¿Cómo empiezo?", c1, "mq1"),
            ("¿Qué obtengo?", c2, "mq2"),
            ("¿Mis datos?", c3, "mq3"),
            ("¿Los roles?", c4, "mq4"),
        ]
        for texto, col, key in preguntas:
            with col:
                if st.button(texto, key=key, use_container_width=True):
                    st.session_state['melissa_msgs'].append({"role":"user","content":texto})
                    with st.spinner(""):
                        r = _llamar_ia(MELISSA_SYSTEM, st.session_state['melissa_msgs'])
                    st.session_state['melissa_msgs'].append({"role":"assistant","content":r})
                    st.rerun()

        user_input = st.chat_input("Escribe tu pregunta a Melissa...", key="melissa_chat")
        if user_input:
            st.session_state['melissa_msgs'].append({"role":"user","content":user_input})
            with st.spinner("Melissa está escribiendo..."):
                r = _llamar_ia(MELISSA_SYSTEM, st.session_state['melissa_msgs'])
            st.session_state['melissa_msgs'].append({"role":"assistant","content":r})
            st.rerun()

    st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════
# FÉLIX
# ══════════════════════════════════════════════════════════════════════════
def mostrar_felix(pagina=""):
    key_msgs = f'felix_msgs_{pagina}'
    key_exp  = f'felix_exp_{pagina}'

    sector = st.session_state.get('save_sector_nombre','tu empresa')
    completados = sum(1 for i in range(1,6) if st.session_state.get(f'score_b{i}',0)>0)

    if key_msgs not in st.session_state:
        bienvenidas = {
            'indices': f"Hola, soy Félix. En Índices Estratégicos verás la posición competitiva de {sector} en 6 dimensiones. Tienes {completados}/5 bloques completados. ¿Quieres que te explique cada índice?",
            'informe_estrategico': f"Hola, soy Félix. El Informe Estratégico analiza con IA la posición competitiva de {sector}. Pulsa 'Generar Informe' para obtener el análisis completo. ¿Empezamos?",
            'informe_innovacion': f"Hola, soy Félix. Aquí verás el diagnóstico de innovación de {sector} por los 5 bloques. ¿Quieres que te explique cómo interpretar los indicadores?",
            'plan': f"Hola, soy Félix. El Plan de Acción generará 5 acciones prioritarias para {sector} más una hoja de ruta 1-3 años. ¿Lo generamos ahora?",
            'benchmarking': f"Hola, soy Félix. En Benchmarking puedes comparar {sector} con las empresas líderes del sector. ¿Te explico cómo usar los filtros?",
            'analytics': f"Hola, soy Félix. En Analytics encontrarás visualizaciones detalladas de todos los indicadores de {sector}. ¿En qué puedo ayudarte?",
        }
        msg = bienvenidas.get(pagina, f"Hola, soy Félix, tu consultor estratégico. Puedo ayudarte a interpretar los resultados y navegar por la plataforma. ¿En qué puedo ayudarte?")
        st.session_state[key_msgs] = [{"role":"assistant","content":msg}]

    if key_exp not in st.session_state:
        st.session_state[key_exp] = False

    img_b64 = _imagen_base64('felix.png')
    felix_system = FELIX_SYSTEM_BASE + f"\n\nCONTEXTO: {sector} | Bloques completados: {completados}/5 | Página: {pagina}"
    ultimo_msg = st.session_state[key_msgs][-1]['content'][:120] + "..." if len(st.session_state[key_msgs][-1]['content']) > 120 else st.session_state[key_msgs][-1]['content']

    # Banner siempre visible
    st.markdown(_banner_asistente(img_b64, "Félix", "Tu asesor estratégico", "#1e3a5f", ultimo_msg), unsafe_allow_html=True)

    col_expand, col_reset = st.columns([3,1])
    with col_expand:
        label = "▲ Ocultar conversación" if st.session_state[key_exp] else "💬 Preguntar a Félix"
        if st.button(label, key=f"felix_expand_{pagina}", use_container_width=True, type="secondary"):
            st.session_state[key_exp] = not st.session_state[key_exp]
            st.rerun()
    with col_reset:
        if st.button("↺ Reiniciar", key=f"felix_reset_{pagina}", use_container_width=True):
            st.session_state[key_msgs] = [{"role":"assistant","content":f"¡Hola de nuevo! ¿En qué puedo ayudarte con {sector}?"}]
            st.rerun()

    if st.session_state[key_exp]:
        for m in st.session_state[key_msgs][-6:]:
            if m['role'] == 'assistant':
                with st.chat_message("assistant", avatar=f"data:image/png;base64,{img_b64}" if img_b64 else "💼"):
                    st.write(m['content'])
            else:
                with st.chat_message("user"):
                    st.write(m['content'])

        user_input = st.chat_input("Pregunta a Félix...", key=f"felix_chat_{pagina}")
        if user_input:
            st.session_state[key_msgs].append({"role":"user","content":user_input})
            with st.spinner("Félix está analizando..."):
                r = _llamar_ia(felix_system, st.session_state[key_msgs])
            st.session_state[key_msgs].append({"role":"assistant","content":r})
            st.rerun()

    st.markdown("---")