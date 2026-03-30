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
- Tiempo estimado cuestionario innovación: 10-15 minutos

SECCIONES DEL MENÚ LATERAL:
1. Inicio: presentación y acceso a la plataforma
2. Registro Empresa: el admin crea la empresa y obtiene código único
3. Acceso: todos entran con email + código de empresa
4. Mi Empresa: admin gestiona equipo, roles, activa informes
5. Cuestionario Innovación: 5 bloques sencillos escala 1-5
6. Índices Estratégicos: 6 índices competitivos + Score Global SSG
7. Informe Estratégico: análisis competitivo con IA
8. Informe Innovación: diagnóstico innovación con IA
9. Plan de Acción: plan 12 meses + hoja de ruta 3 años con IA
10. Analytics y Benchmarking: comparativas sectoriales

ROLES:
- Admin: gestiona equipo, ve promedios, activa informes
- Manager: ve índices, analytics y promedios
- Colaborador: solo cumplimenta cuestionarios

INSTRUCCIONES: Respuestas máximo 3-4 frases. Lenguaje profesional pero accesible."""

FELIX_SYSTEM_BASE = """Eres Félix, consultor estratégico senior de la plataforma de Diagnóstico Estratégico 360°.

PERSONALIDAD: Consultor profesional, amable y cercano de 35 años. Experto en competitividad e innovación. Directo, preciso, constructivo.

NAVEGACIÓN POR LA PLATAFORMA:
- Inicio: presentación general y perfil de empresa
- Acceso: entrada con email y código de empresa
- Mi Empresa: gestión del equipo y activación de informes
- Cuestionario Innovación: 5 bloques (I+D+i, Gestión Proyectos, Desarrollo Productos, Estrategia Innovación, Desempeño Innovación)
- Índices Estratégicos: ICE, ISF, IEO, IDC, IIE, IPT y Score Global SSG
- Informe Estratégico: análisis competitivo con IA descargable en Word y PDF
- Informe Innovación: diagnóstico de innovación con IA descargable
- Plan de Acción: plan 12 meses + hoja de ruta 3 años personalizada con IA
- Analytics: visualizaciones detalladas de indicadores
- Benchmarking: comparativa con empresas líderes del sector

INSTRUCCIONES:
- Máximo 3-4 frases por respuesta
- Tono consultor senior, nunca genérico
- Personaliza con el sector de la empresa si está disponible
- PROHIBIDO: "alarmante", "catastrófico", "urgente"
- USA: "margen de mejora", "posición sólida", "área prioritaria" """

def _avatar_html(img_b64, nombre, subtitulo, color):
    img_tag = f'<img src="data:image/png;base64,{img_b64}" style="width:48px;height:48px;border-radius:50%;object-fit:cover;border:2px solid #fff;">' if img_b64 else f'<div style="width:48px;height:48px;border-radius:50%;background:{color};"></div>'
    return f"""<div style="background:{color};border-radius:10px;padding:10px 14px;display:flex;align-items:center;gap:10px;margin-bottom:8px;">
        {img_tag}
        <div>
            <div style="font-weight:700;color:#fff;font-size:.9rem;">{nombre}</div>
            <div style="color:rgba(255,255,255,0.8);font-size:.7rem;">{subtitulo}</div>
        </div>
    </div>"""

def _msgs_html(msgs):
    html = ""
    for m in msgs[-4:]:
        if m['role'] == 'assistant':
            html += f'<div style="background:#f1f5f9;border-radius:8px;padding:8px 10px;font-size:.78rem;color:#1e293b;line-height:1.5;margin-bottom:6px;">{m["content"]}</div>'
        else:
            html += f'<div style="background:#dbeafe;border-radius:8px;padding:8px 10px;font-size:.78rem;color:#1e3a8a;line-height:1.5;margin-bottom:6px;text-align:right;">{m["content"]}</div>'
    return html

# ══════════════════════════════════════════════════════════════════════════
# MELISSA — en sidebar
# ══════════════════════════════════════════════════════════════════════════
def mostrar_melissa():
    if 'melissa_msgs' not in st.session_state:
        st.session_state['melissa_msgs'] = [{"role":"assistant","content":"¡Bienvenido/a! Soy Melissa, tu guía profesional. Esta plataforma te permitirá conocer el posicionamiento real de tu empresa comparado con más de 1.000 empresas. ¿En qué puedo ayudarte?"}]
    if 'melissa_abierta' not in st.session_state:
        st.session_state['melissa_abierta'] = True

    img_b64 = _imagen_base64('melissa.png')

    with st.sidebar:
        st.markdown(_avatar_html(img_b64, "Melissa", "Tu guía profesional", "#065f46"), unsafe_allow_html=True)

        if st.session_state['melissa_abierta']:
            st.markdown(_msgs_html(st.session_state['melissa_msgs']), unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("¿Cómo empiezo?", key="mq1", use_container_width=True):
                    st.session_state['melissa_msgs'].append({"role":"user","content":"¿Cómo empiezo?"})
                    r = _llamar_ia(MELISSA_SYSTEM, st.session_state['melissa_msgs'])
                    st.session_state['melissa_msgs'].append({"role":"assistant","content":r})
                    st.rerun()
            with c2:
                if st.button("¿Qué obtengo?", key="mq2", use_container_width=True):
                    st.session_state['melissa_msgs'].append({"role":"user","content":"¿Qué obtengo con esta plataforma?"})
                    r = _llamar_ia(MELISSA_SYSTEM, st.session_state['melissa_msgs'])
                    st.session_state['melissa_msgs'].append({"role":"assistant","content":r})
                    st.rerun()
            c3, c4 = st.columns(2)
            with c3:
                if st.button("¿Mis datos?", key="mq3", use_container_width=True):
                    st.session_state['melissa_msgs'].append({"role":"user","content":"¿Son seguros mis datos?"})
                    r = _llamar_ia(MELISSA_SYSTEM, st.session_state['melissa_msgs'])
                    st.session_state['melissa_msgs'].append({"role":"assistant","content":r})
                    st.rerun()
            with c4:
                if st.button("¿Los roles?", key="mq4", use_container_width=True):
                    st.session_state['melissa_msgs'].append({"role":"user","content":"¿Qué son los roles de usuario?"})
                    r = _llamar_ia(MELISSA_SYSTEM, st.session_state['melissa_msgs'])
                    st.session_state['melissa_msgs'].append({"role":"assistant","content":r})
                    st.rerun()

            user_input = st.chat_input("Pregunta a Melissa...", key="melissa_chat")
            if user_input:
                st.session_state['melissa_msgs'].append({"role":"user","content":user_input})
                with st.spinner(""):
                    r = _llamar_ia(MELISSA_SYSTEM, st.session_state['melissa_msgs'])
                st.session_state['melissa_msgs'].append({"role":"assistant","content":r})
                st.rerun()

        toggle_label = "▲ Ocultar" if st.session_state['melissa_abierta'] else "▼ Abrir chat"
        if st.button(toggle_label, key="melissa_toggle", use_container_width=True):
            st.session_state['melissa_abierta'] = not st.session_state['melissa_abierta']
            st.rerun()

        st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════
# FÉLIX — en sidebar
# ══════════════════════════════════════════════════════════════════════════
def mostrar_felix(pagina=""):
    key_msgs = f'felix_msgs_{pagina}'
    key_vis  = f'felix_vis_{pagina}'

    sector = st.session_state.get('save_sector_nombre','tu empresa')
    completados = sum(1 for i in range(1,6) if st.session_state.get(f'score_b{i}',0)>0)

    if key_msgs not in st.session_state:
        bienvenidas = {
            'indices': f"Hola, soy Félix. En Índices Estratégicos verás la posición competitiva de {sector} en 6 dimensiones. Tienes {completados}/5 bloques completados. ¿Quieres que te explique cada índice?",
            'informe_estrategico': f"Hola, soy Félix. El Informe Estratégico analiza con IA la posición competitiva de {sector}. Pulsa 'Generar Informe' para obtener el análisis completo en segundos. ¿Empezamos?",
            'informe_innovacion': f"Hola, soy Félix. Aquí verás el diagnóstico de innovación de {sector} por los 5 bloques. ¿Quieres que te explique cómo interpretar los indicadores?",
            'plan': f"Hola, soy Félix. El Plan de Acción generará 5 acciones prioritarias para {sector} más una hoja de ruta 1-3 años. ¿Generamos el plan ahora?",
            'benchmarking': f"Hola, soy Félix. En Benchmarking puedes comparar {sector} con las empresas líderes. ¿Te explico cómo usar los filtros?",
            'analytics': f"Hola, soy Félix. En Analytics encontrarás visualizaciones detalladas de todos los indicadores de {sector}. ¿En qué quieres que te ayude?",
        }
        msg = bienvenidas.get(pagina, f"Hola, soy Félix, tu consultor estratégico. Puedo ayudarte a navegar por cualquier sección de la plataforma y a interpretar tus resultados. ¿En qué puedo ayudarte?")
        st.session_state[key_msgs] = [{"role":"assistant","content":msg}]

    if key_vis not in st.session_state:
        st.session_state[key_vis] = True

    img_b64 = _imagen_base64('felix.png')

    felix_system = FELIX_SYSTEM_BASE + f"\n\nCONTEXTO EMPRESA: {sector} | Bloques completados: {completados}/5 | Página actual: {pagina}"

    with st.sidebar:
        st.markdown(_avatar_html(img_b64, "Félix", "Tu asesor estratégico", "#1e3a5f"), unsafe_allow_html=True)

        if st.session_state[key_vis]:
            st.markdown(_msgs_html(st.session_state[key_msgs]), unsafe_allow_html=True)

            user_input = st.chat_input("Pregunta a Félix...", key=f"felix_chat_{pagina}")
            if user_input:
                st.session_state[key_msgs].append({"role":"user","content":user_input})
                with st.spinner(""):
                    r = _llamar_ia(felix_system, st.session_state[key_msgs])
                st.session_state[key_msgs].append({"role":"assistant","content":r})
                st.rerun()

        toggle_label = "▲ Ocultar" if st.session_state[key_vis] else "▼ Abrir chat"
        if st.button(toggle_label, key=f"felix_toggle_{pagina}", use_container_width=True):
            st.session_state[key_vis] = not st.session_state[key_vis]
            st.rerun()

        st.markdown("---")