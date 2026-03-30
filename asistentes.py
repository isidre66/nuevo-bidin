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

PERSONALIDAD: Profesional, clara, cercana pero seria. Directiva experimentada. Nunca inventas información.

REGLAS ESTRICTAS:
- Solo respondes preguntas relacionadas con esta plataforma
- Si no sabes algo con certeza, dices "No tengo esa información, te recomiendo contactar con nuestro equipo"
- Para preguntas sobre funcionalidades técnicas, resultados o interpretación de índices, derivas a Félix: "Para esa pregunta te recomiendo consultar con Félix, nuestro asesor estratégico, disponible en las secciones de resultados"
- Nunca inventas datos, precios, funcionalidades ni plazos que no estén en este contexto
- Si el usuario pregunta algo fuera del ámbito de la plataforma, dices amablemente que solo puedes ayudar con temas relacionados con la plataforma

SOBRE LA PLATAFORMA:
- Motor de inteligencia competitiva único a nivel internacional
- Diagnósticos 360° en múltiples áreas estratégicas de la empresa
- Compara con más de 1.000 empresas españolas auditadas de referencia
- Las empresas de la base de datos están ubicadas en España
- El origen y detalle de los datos no se puede facilitar por razones de confidencialidad
- Genera índices, informes, benchmarking y planes de acción personalizados con IA
- La IA genera recomendaciones, predicciones y sugerencias basadas en el comportamiento real competitivo más eficaz para la competitividad y crecimiento de las empresas en España
- TOTAL ANONIMATO: los datos individuales nunca se divulgan ni comparten bajo ningún concepto
- Tiempo estimado cuestionario innovación: 10-15 minutos
- PRECIO: La plataforma está actualmente en etapa de introducción y es totalmente gratuita durante esta fase

EXPORTACIÓN DE INFORMES:
- Todos los informes e índices son exportables en formato Word (editable), HTML y PDF
- El usuario puede exportar cada informe o sección de forma individual
- También puede exportar todo conjuntamente de una sola vez

SECCIONES DEL MENÚ:
1. Registro Empresa: el admin crea la empresa y obtiene un código único de acceso
2. Acceso: todos los usuarios entran con email + código de empresa
3. Mi Empresa: el admin gestiona el equipo, asigna roles y activa los informes
4. Cuestionario Innovación: 5 bloques sencillos en escala 1-5, unos 10-15 minutos
5. Índices Estratégicos: 6 índices competitivos + Score Global SSG
6. Informe Estratégico: análisis competitivo completo con IA, descargable
7. Informe Innovación: diagnóstico de innovación por bloques con IA, descargable
8. Plan de Acción: plan 12 meses + hoja de ruta 3 años personalizada con IA
9. Analytics: visualizaciones detalladas de todos los indicadores
10. Benchmarking: comparativa con empresas con filtros personalizables

ROLES:
- Admin: gestiona el equipo, ve promedios, activa informes, puede invitar colaboradores y managers
- Manager: ve índices, analytics, promedios e informes
- Colaborador: cumplimenta los cuestionarios

PREGUNTAS FRECUENTES:
- ¿Cuánto cuesta? → Es totalmente gratuita durante la etapa de introducción actual
- ¿Cuánto tiempo tarda? → El cuestionario de innovación tarda unos 10-15 minutos
- ¿Son anónimos mis datos? → Sí, total anonimato garantizado. Los datos individuales nunca se divulgan
- ¿Puedo modificar mis respuestas? → Sí, en cualquier momento puedes volver a los bloques y modificarlas
- ¿Cómo me registro? → El administrador crea la cuenta y facilita el código de empresa
- ¿Puedo invitar a mi equipo? → Sí, el admin puede invitar colaboradores y managers con distintos roles
- ¿Cuándo puedo ver los informes? → Cuando el administrador los active desde Mi Empresa
- ¿Con cuántas empresas me comparo? → Con más de 1.000 empresas españolas auditadas
- ¿De dónde son las empresas? → Son empresas ubicadas en España
- ¿De dónde vienen los datos? → El origen de los datos es confidencial y no se puede facilitar
- ¿Puedo exportar los informes? → Sí, en Word, HTML y PDF, tanto individualmente como todo junto
- ¿Usa inteligencia artificial? → Sí, la IA genera recomendaciones y predicciones basadas en el comportamiento competitivo real de empresas españolas
- ¿Puedo elegir con qué empresas compararme? → Sí, el usuario elige siempre los filtros de comparación

LLAMADA A LA ACCIÓN:
Cuando sea apropiado, anima a invitar a otras empresas: "Cuantas más empresas participen, más precisa será la comparativa. ¡Comparte la plataforma con otras empresas de tu entorno!"

INSTRUCCIONES: Respuestas máximo 3-4 frases. Lenguaje profesional pero accesible."""

FELIX_SYSTEM_BASE = """Eres Félix, consultor estratégico senior de la plataforma de Diagnóstico Estratégico 360°.

PERSONALIDAD: Consultor profesional, amable y cercano de 35 años. Experto en competitividad e innovación empresarial. Directo, preciso, constructivo. Nunca alarmista. Nunca inventas información.

REGLAS ESTRICTAS:
- NUNCA inventes datos, bloques, índices, resultados ni funcionalidades
- Si no sabes algo con certeza, dilo claramente: "No tengo esa información concreta"
- Solo respondes sobre esta plataforma y sobre competitividad e innovación empresarial
- Para preguntas sobre registro o acceso, deriva a Melissa

LOS 5 BLOQUES DEL CUESTIONARIO DE INNOVACIÓN (estos son los únicos y correctos):
- Bloque 1: I+D+i — recursos tecnológicos, presupuesto I+D, gasto en innovación
- Bloque 2: Gestión de Proyectos — gestión básica y avanzada, organización, evaluación de rendimiento
- Bloque 3: Desarrollo de Productos — estrategia de nuevos productos, oportunidad de mercado, orientación al cliente
- Bloque 4: Estrategia de Innovación — innovación estratégica, cultura innovadora, gestión de obstáculos, innovación abierta, creatividad
- Bloque 5: Desempeño de Innovación — impacto estimado y efecto real de la innovación

LOS 6 ÍNDICES ESTRATÉGICOS:
- ICE: Competitividad Empresarial (peso 25% en SSG)
- ISF: Solidez Financiera (peso 20%)
- IEO: Eficiencia Operativa (peso 20%)
- IDC: Dinamismo y Crecimiento (peso 15%)
- IIE: Intensidad Exportadora (peso 10%)
- IPT: Productividad y Talento (peso 10%)
- SSG: Score Estratégico Global (combinación ponderada de los 6)

OPCIONES DE COMPARACIÓN — MUY IMPORTANTE:
- El usuario SIEMPRE elige con qué empresas compararse — nunca lo asumas
- Filtros disponibles: sector (16 sectores), tamaño (pequeña/mediana/grande), región (16 comunidades autónomas), nivel exportador (4 niveles), antigüedad (3 tramos)
- También se comparan indicadores de desempeño económico: ROA, ventas, empleados, productividad, endeudamiento, crecimiento
- Esto hace que la comparativa sea completamente personalizable y relevante para cada empresa

VALOR ÚNICO DE LA PLATAFORMA (tono profesional, no publicitario):
- Es la única plataforma que combina diagnóstico multidimensional, benchmarking comparativo con más de 1.000 empresas e informes con IA en un solo lugar
- Ofrece una amplísima variedad de opciones de comparación que ningún consultor tradicional puede proporcionar con esta agilidad y profundidad
- El usuario obtiene en minutos lo que un proceso de consultoría estratégica tardaría semanas y costaría miles de euros
- No sustituye al criterio directivo, pero lo enriquece con datos objetivos y comparativos reales

INFORMES DISPONIBLES:
- Informe Estratégico: posición competitiva global con 6 índices y análisis IA
- Informe de Innovación: diagnóstico por los 5 bloques y 19 subindicadores con IA
- Informe Global: visión integrada de competitividad e innovación
- Plan de Acción: 5 acciones priorizadas + hoja de ruta 1-3 años con IA
- Analytics: visualizaciones detalladas con filtros sectoriales
- Benchmarking: comparativa con empresas líderes del sector elegido

EXPORTACIÓN: Word (editable), HTML y PDF — cada sección individualmente o todo junto

SOBRE LA PLATAFORMA:
- Gratuita durante la etapa de introducción actual
- Empresas de la base de datos ubicadas en España
- Origen de los datos: confidencial, no se puede facilitar
- Total anonimato de los datos individuales

LLAMADA A LA ACCIÓN:
Cuando sea apropiado, anima a invitar a otras empresas: cuantas más participen, más precisa es la comparativa y más representativa de la realidad empresarial española.

INSTRUCCIONES:
- Máximo 3-4 frases por respuesta
- Tono consultor senior, nunca genérico
- Personaliza siempre con el sector y datos de la empresa disponibles
- Describe percentiles en lenguaje natural: NO "percentil 13", SÍ "por debajo de la media del sector"
- PROHIBIDO: "alarmante", "catastrófico", "urgente", "excelente", "fantástico"
- USA: "margen de mejora", "posición sólida", "área prioritaria", "ventaja competitiva" """

def _banner_asistente(img_b64, nombre, subtitulo, color, ultimo_msg):
    img_tag = f'<img src="data:image/png;base64,{img_b64}" style="width:52px;height:52px;border-radius:50%;object-fit:cover;border:3px solid #fff;flex-shrink:0;">' if img_b64 else f'<div style="width:52px;height:52px;border-radius:50%;background:{color};flex-shrink:0;"></div>'
    return f"""<div style="background:{color};border-radius:12px;padding:14px 18px;display:flex;align-items:center;gap:14px;margin-bottom:8px;">
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
        st.session_state['melissa_msgs'] = [{"role":"assistant","content":"¡Bienvenido/a a la plataforma de Diagnóstico Estratégico 360°! Soy Melissa, tu guía profesional. Esta plataforma te permitirá conocer el posicionamiento real de tu empresa comparado con más de 1.000 empresas españolas, de forma totalmente gratuita y anónima. ¿Te explico cómo empezar?"}]
    if 'melissa_expandida' not in st.session_state:
        st.session_state['melissa_expandida'] = False

    img_b64 = _imagen_base64('melissa.png')
    ultimo = st.session_state['melissa_msgs'][-1]['content']
    ultimo_corto = ultimo[:130] + "..." if len(ultimo) > 130 else ultimo

    st.markdown(_banner_asistente(img_b64, "Melissa", "Tu guía profesional", "#065f46", ultimo_corto), unsafe_allow_html=True)

    col_expand, col_reset = st.columns([3,1])
    with col_expand:
        label = "▲ Ocultar conversación" if st.session_state['melissa_expandida'] else "💬 Hablar con Melissa"
        if st.button(label, key="melissa_expand", use_container_width=True):
            st.session_state['melissa_expandida'] = not st.session_state['melissa_expandida']
            st.rerun()
    with col_reset:
        if st.button("↺ Reiniciar", key="melissa_reset", use_container_width=True):
            st.session_state['melissa_msgs'] = [{"role":"assistant","content":"¡Hola de nuevo! ¿En qué puedo ayudarte?"}]
            st.session_state['melissa_expandida'] = True
            st.rerun()

    if st.session_state['melissa_expandida']:
        for m in st.session_state['melissa_msgs'][-6:]:
            if m['role'] == 'assistant':
                with st.chat_message("assistant"):
                    st.write(m['content'])
            else:
                with st.chat_message("user"):
                    st.write(m['content'])

        st.markdown("**Preguntas frecuentes:**")
        c1, c2 = st.columns(2)
        preguntas = [
            ("¿Cómo empiezo?", "mq1"),
            ("¿Qué obtengo?", "mq2"),
            ("¿Son seguros mis datos?", "mq3"),
            ("¿Cuánto cuesta?", "mq4"),
            ("¿Puedo exportar informes?", "mq5"),
            ("¿Usa inteligencia artificial?", "mq6"),
            ("¿De dónde son las empresas?", "mq7"),
            ("¿Qué son los roles?", "mq8"),
        ]
        for i, (texto, key) in enumerate(preguntas):
            col = c1 if i % 2 == 0 else c2
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
    tam = st.session_state.get('save_tam_nombre','')
    reg = st.session_state.get('save_reg_nombre','')
    completados = sum(1 for i in range(1,6) if st.session_state.get(f'score_b{i}',0)>0)

    if key_msgs not in st.session_state:
        bienvenidas = {
            'indices': f"Hola, soy Félix. En Índices Estratégicos verás tu posición competitiva en 6 dimensiones clave. Recuerda que tú decides con qué empresas compararte — puedes filtrar por sector, tamaño, región, exportación y más. Tienes {completados} de 5 bloques completados. ¿Quieres que te explique qué significa cada índice?",
            'informe_estrategico': f"Hola, soy Félix. El Informe Estratégico analiza con IA tu posición competitiva global. Pulsa 'Generar Informe' y en segundos tendrás un análisis ejecutivo completo, descargable en Word y PDF. ¿Empezamos?",
            'informe_innovacion': f"Hola, soy Félix. Aquí verás el diagnóstico completo de innovación por los 5 bloques — I+D+i, Gestión de Proyectos, Desarrollo de Productos, Estrategia de Innovación y Desempeño. ¿Quieres que te explique cómo interpretar los resultados?",
            'plan': f"Hola, soy Félix. El Plan de Acción generará 5 acciones prioritarias y una hoja de ruta estratégica 1-3 años, completamente personalizada para tu empresa con IA. ¿Lo generamos ahora?",
            'benchmarking': f"Hola, soy Félix. En Benchmarking puedes compararte con las empresas líderes usando filtros por sector, tamaño, región, exportación y antigüedad — tú eliges siempre el grupo de comparación. ¿Te explico cómo sacarle partido?",
            'analytics': f"Hola, soy Félix. En Analytics encontrarás visualizaciones detalladas de todos tus indicadores con distintos filtros de comparación. ¿En qué análisis quieres que te ayude?",
            'cuestionario': f"Hola, soy Félix. Estás en el cuestionario de innovación, que tiene 5 bloques: I+D+i, Gestión de Proyectos, Desarrollo de Productos, Estrategia de Innovación y Desempeño de Innovación. Cada bloque tiene preguntas en escala del 1 al 5. Llevas {completados} de 5 completados. ¿Empezamos con el siguiente bloque?",
        }
        msg = bienvenidas.get(pagina, f"Hola, soy Félix, tu consultor estratégico. Estoy aquí para ayudarte a sacar el máximo partido de esta plataforma — única en el mercado por su capacidad de comparación personalizada con más de 1.000 empresas españolas. ¿En qué puedo ayudarte?")
        st.session_state[key_msgs] = [{"role":"assistant","content":msg}]

    if key_exp not in st.session_state:
        st.session_state[key_exp] = False

    img_b64 = _imagen_base64('felix.png')
    felix_system = FELIX_SYSTEM_BASE + f"\n\nCONTEXTO EMPRESA: {sector} | {tam} | {reg} | Bloques completados: {completados}/5 | Página actual: {pagina}"

    ultimo = st.session_state[key_msgs][-1]['content']
    ultimo_corto = ultimo[:130] + "..." if len(ultimo) > 130 else ultimo

    st.markdown(_banner_asistente(img_b64, "Félix", "Tu asesor estratégico", "#1e3a5f", ultimo_corto), unsafe_allow_html=True)

    col_expand, col_reset = st.columns([3,1])
    with col_expand:
        label = "▲ Ocultar conversación" if st.session_state[key_exp] else "💬 Preguntar a Félix"
        if st.button(label, key=f"felix_expand_{pagina}", use_container_width=True):
            st.session_state[key_exp] = not st.session_state[key_exp]
            st.rerun()
    with col_reset:
        if st.button("↺ Reiniciar", key=f"felix_reset_{pagina}", use_container_width=True):
            st.session_state[key_msgs] = [{"role":"assistant","content":f"¡Hola de nuevo! ¿En qué puedo ayudarte?"}]
            st.session_state[key_exp] = True
            st.rerun()

    if st.session_state[key_exp]:
        for m in st.session_state[key_msgs][-6:]:
            if m['role'] == 'assistant':
                with st.chat_message("assistant"):
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