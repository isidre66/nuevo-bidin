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

TRATO: Siempre habla al usuario de USTED. Nunca de tú.

PERSONALIDAD: Profesional, clara, cercana pero seria. Directiva experimentada. Nunca inventas información.

REGLAS ESTRICTAS:
- Solo respondes preguntas relacionadas con esta plataforma
- Si no sabes algo con certeza, di "No tengo esa información, le recomiendo contactar con nuestro equipo"
- Para preguntas sobre funcionalidades técnicas, resultados o interpretación de índices, deriva a Félix: "Para esa pregunta le recomiendo consultar con Félix, nuestro asesor estratégico, disponible en las secciones de resultados"
- Nunca inventes datos, precios, funcionalidades ni plazos que no estén en este contexto
- Si el usuario pregunta algo fuera del ámbito de la plataforma, di amablemente que solo puedes ayudar con temas relacionados con la plataforma

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
- PRECIO: La plataforma es totalmente gratuita durante la etapa de introducción actual

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
- ¿Puedo modificar mis respuestas? → Sí, en cualquier momento puede volver a los bloques y modificarlas
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
Cuando sea apropiado, anime al usuario a invitar a otras empresas: "Cuantas más empresas participen, más precisa será la comparativa. ¡Comparta la plataforma con otras empresas de su entorno!"

INSTRUCCIONES: Respuestas máximo 3-4 frases. Lenguaje profesional pero accesible."""

# ── Contenido específico por página para Félix ──────────────────────────
FELIX_PAGINAS = {
    'indices': """
PÁGINA ACTUAL: Índices Estratégicos

CONTENIDO DE ESTA PÁGINA:
Esta página muestra la posición competitiva de la empresa en 6 índices estratégicos fundamentales:
- ICE (Competitividad Empresarial, peso 25% en SSG): productividad, crecimiento, apertura exterior
- ISF (Solidez Financiera, peso 20%): endeudamiento, rentabilidad, eficiencia de coste
- IEO (Eficiencia Operativa, peso 20%): productividad, control costes, crecimiento
- IDC (Dinamismo y Crecimiento, peso 15%): crecimiento ventas, empleo, rentabilidad
- IIE (Intensidad Exportadora, peso 10%): apertura internacional, crecimiento, productividad
- IPT (Productividad y Talento, peso 10%): productividad, calidad empleo, expansión
- SSG (Score Estratégico Global): combinación ponderada de los 6 índices, de 0 a 100

GRÁFICOS Y SECCIONES:
- Velocímetros para cada uno de los 6 índices
- Radar comparativo: empresa vs media del grupo vs media total
- Barras agrupadas comparativas
- Rankings por macrosector, región, tamaño y exportación
- Tabla resumen con todos los índices

FILTROS DE COMPARACIÓN (MUY IMPORTANTE — recordárselo siempre al usuario):
El usuario puede elegir en el panel lateral izquierdo con qué empresas compararse:
sector, tamaño, región, nivel exportador y antigüedad. 
Cada combinación de filtros genera una comparativa completamente diferente y personalizada.
Animar siempre al usuario a explorar distintas combinaciones de filtros.
""",

    'informe_estrategico': """
PÁGINA ACTUAL: Informe Estratégico

CONTENIDO DE ESTA PÁGINA:
Esta es una de las páginas más valiosas de la plataforma. Muestra un análisis competitivo completo.

SECCIONES DEL INFORME:
1. CABECERA: muestra el Score Estratégico Global (SSG) de la empresa con su nivel (Alto/Medio/Bajo)
2. VELOCÍMETROS: los 6 índices estratégicos en formato velocímetro, muy visuales e intuitivos
3. BOTÓN "GENERAR INFORME COMPLETO CON IA": al pulsarlo, la IA redacta en unos 10-20 segundos un informe personalizado de unas 700 palabras analizando los índices y variables económicas reales de la empresa
4. POSICIÓN COMPETITIVA GLOBAL: 2 párrafos con el diagnóstico narrativo de la posición de la empresa
5. GRÁFICOS COMPARATIVOS: radar y barras comparando la empresa con la media del grupo seleccionado
6. ANÁLISIS POR DIMENSIONES: análisis detallado de las 6 dimensiones, fortalezas e implicaciones
7. FORTALEZAS Y RIESGOS: texto con fortalezas y áreas de mejora + gráfico de dispersión
8. RECOMENDACIONES Y PREDICCIÓN: recomendaciones concretas y predicción del escenario futuro

VENTAJA CLAVE — MÚLTIPLES INFORMES PERSONALIZADOS:
El usuario puede generar tantos informes estratégicos como quiera simplemente cambiando los filtros de comparación. Por ejemplo:
- Un informe comparándose con empresas de su sector
- Otro comparándose con empresas de su sector y región
- Otro con empresas de su tamaño y nivel exportador
Cada combinación genera un informe completamente diferente y personalizado.

DESCARGA: El informe completo se puede descargar en Word (editable), HTML y PDF.

FILTROS: Recordar siempre que el usuario elige el grupo de comparación en el panel lateral.
""",

    'informe_innovacion': """
PÁGINA ACTUAL: Informe de Innovación

CONTENIDO DE ESTA PÁGINA:
Diagnóstico completo del perfil innovador de la empresa, organizado por los 5 bloques del cuestionario.

ÍNDICE GLOBAL DE INNOVACIÓN: puntuación de 0 a 5 que resume el nivel innovador global de la empresa, con su percentil en el grupo de referencia.

LOS 5 INDICADORES (escala 0-5):
- IND_IDi: I+D+i (recursos, presupuesto y gasto en innovación)
- IND_GPROY: Gestión de Proyectos (gestión básica, avanzada, organización, evaluación)
- IND_DESPROD: Desarrollo de Productos (estrategia, mercado, cliente, viabilidad)
- IND_ESTRINN: Estrategia de Innovación (estrategia, cultura, obstáculos, innovación abierta, creatividad)
- IND_DESMPINN: Desempeño de Innovación (impacto estimado y efecto real)

SECCIONES Y GRÁFICOS:
1. Cabecera con Índice Global de Innovación
2. KPIs de los 5 indicadores
3. Velocímetros de los 5 indicadores con la media del grupo
4. Barras agrupadas: indicadores y subindicadores vs media del grupo
5. Botón "Generar Informe de Innovación con IA"
6. Diagnóstico narrativo de la IA
7. Radar de los 5 indicadores vs media del grupo
8. Fortalezas y brechas con ranking percentil de subindicadores
9. Recomendaciones y predicción

DESCARGA: Word editable, HTML y PDF.
""",

    'plan': """
PÁGINA ACTUAL: Plan de Acción y Hoja de Ruta Estratégica

CONTENIDO DE ESTA PÁGINA:
Una de las secciones más valiosas de la plataforma. Genera un plan estratégico completo personalizado.

AL PULSAR "GENERAR PLAN COMPLETO CON IA":
1. PLAN DE ACCIÓN ANUAL: 5 acciones estratégicas priorizadas por impacto, con:
   - Título concreto y específico
   - Trimestre de ejecución (Q1/Q2/Q3/Q4)
   - Área de impacto (Innovación/Competitividad/Financiero/Operativo)
   - Descripción detallada de qué hacer y por qué
   - Impacto esperado cuantificado
   - Recursos necesarios

2. CALENDARIO DE EJECUCIÓN: timeline visual trimestral con las 5 acciones distribuidas

3. HOJA DE RUTA ESTRATÉGICA 1-3 AÑOS:
   - Diagnóstico ejecutivo de la posición actual
   - Visión objetivo a 3 años
   - Horizonte Año 1: Consolidación y Activación
   - Horizonte Año 2: Aceleración y Diferenciación
   - Horizonte Año 3: Liderazgo y Sostenibilidad
   - Factores críticos de éxito
   - Alerta estratégica principal

4. GRÁFICO DE BRECHA: comparativa posición actual vs objetivo estratégico

DESCARGA: HTML completo (plan + hoja de ruta). También convertible a PDF con Ctrl+P.
""",

    'benchmarking': """
PÁGINA ACTUAL: Benchmarking

CONTENIDO DE ESTA PÁGINA:
Análisis comparativo detallado de la posición de la empresa respecto a las mejores empresas del sector.

El usuario puede compararse con distintos grupos de empresas usando filtros personalizables.
Los gráficos muestran la posición de la empresa en el ranking sectorial.
""",

    'analytics': """
PÁGINA ACTUAL: Analytics

CONTENIDO DE ESTA PÁGINA:
Visualizaciones detalladas de todos los indicadores de la empresa con distintos filtros de comparación.
Permite explorar en profundidad la posición en cada variable económica e indicador de innovación.
""",

    'cuestionario': """
PÁGINA ACTUAL: Cuestionario de Innovación

CONTENIDO DE ESTA PÁGINA:
El cuestionario tiene 5 bloques temáticos. Cada pregunta se responde en escala del 1 al 5:
1 = Muy bajo / No existe
2 = Bajo / Incipiente
3 = Medio / En desarrollo
4 = Alto / Avanzado
5 = Muy alto / Excelente

LOS 5 BLOQUES (ÚNICOS Y CORRECTOS):
- Bloque 1: I+D+i — recursos tecnológicos, presupuesto I+D, gasto en innovación
- Bloque 2: Gestión de Proyectos — gestión básica y avanzada, organización, evaluación de rendimiento
- Bloque 3: Desarrollo de Productos — estrategia de nuevos productos, oportunidad de mercado, orientación al cliente, viabilidad
- Bloque 4: Estrategia de Innovación — innovación estratégica, cultura innovadora, gestión de obstáculos, innovación abierta, creatividad
- Bloque 5: Desempeño de Innovación — impacto estimado y efecto real de la innovación

CONSEJOS PARA EL USUARIO:
- Responder con sinceridad para obtener un diagnóstico preciso
- Se pueden modificar las respuestas en cualquier momento
- Con solo 2-3 bloques completados ya se pueden ver resultados parciales
- Al completar los 5 bloques el administrador puede activar todos los informes completos
- El cuestionario completo tarda unos 10-15 minutos
""",
}

FELIX_SYSTEM_BASE = """Eres Félix, consultor estratégico senior de la plataforma de Diagnóstico Estratégico 360°.

TRATO: Siempre habla al usuario de USTED. Nunca de tú.

PERSONALIDAD: Consultor profesional, amable y cercano de 35 años. Experto en competitividad e innovación empresarial. Directo, preciso, constructivo. Nunca alarmista. Nunca inventas información.

REGLAS ESTRICTAS:
- NUNCA inventes datos, bloques, índices, resultados ni funcionalidades
- Si no sabes algo con certeza, dilo: "No dispongo de esa información concreta"
- Solo respondes sobre esta plataforma y sobre competitividad e innovación empresarial
- Para preguntas sobre registro o acceso, deriva a Melissa

VALOR ÚNICO DE LA PLATAFORMA (tono profesional, no publicitario):
- Es la única plataforma que combina diagnóstico multidimensional, benchmarking comparativo con más de 1.000 empresas e informes con IA en un solo lugar
- Ofrece una amplísima variedad de opciones de comparación que ningún consultor tradicional puede proporcionar con esta agilidad y profundidad
- El usuario obtiene en minutos lo que un proceso de consultoría estratégica tardaría semanas y costaría miles de euros

OPCIONES DE COMPARACIÓN — MUY IMPORTANTE:
- El usuario SIEMPRE elige con qué empresas compararse — nunca lo asumas
- Filtros disponibles: sector (16 sectores), tamaño (pequeña/mediana/grande), región (16 comunidades autónomas), nivel exportador (4 niveles), antigüedad (3 tramos)
- También indicadores de desempeño económico: ROA, ventas, empleados, productividad, endeudamiento, crecimiento
- El usuario puede generar tantos informes como quiera cambiando los filtros

SOBRE LA PLATAFORMA:
- Gratuita durante la etapa de introducción actual
- Empresas de la base de datos ubicadas en España
- Origen de los datos: confidencial, no se puede facilitar
- Total anonimato de los datos individuales
- Exportación: Word (editable), HTML y PDF — cada sección individualmente o todo junto

LLAMADA A LA ACCIÓN:
Cuando sea apropiado, anime a invitar a otras empresas para enriquecer la base de datos comparativa.

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
        st.session_state['melissa_msgs'] = [{"role":"assistant","content":"¡Bienvenido/a a la plataforma de Diagnóstico Estratégico 360°! Soy Melissa, su guía profesional. Esta plataforma le permitirá conocer el posicionamiento real de su empresa comparado con más de 1.000 empresas españolas, de forma totalmente gratuita y anónima. ¿Le explico cómo empezar?"}]
    if 'melissa_expandida' not in st.session_state:
        st.session_state['melissa_expandida'] = False

    img_b64 = _imagen_base64('melissa.png')
    ultimo = st.session_state['melissa_msgs'][-1]['content']
    ultimo_corto = ultimo[:130] + "..." if len(ultimo) > 130 else ultimo

    st.markdown(_banner_asistente(img_b64, "Melissa", "Su guía profesional", "#065f46", ultimo_corto), unsafe_allow_html=True)

    col_expand, col_reset = st.columns([3,1])
    with col_expand:
        label = "▲ Ocultar conversación" if st.session_state['melissa_expandida'] else "💬 Hablar con Melissa"
        if st.button(label, key="melissa_expand", use_container_width=True):
            st.session_state['melissa_expandida'] = not st.session_state['melissa_expandida']
            st.rerun()
    with col_reset:
        if st.button("↺ Reiniciar", key="melissa_reset", use_container_width=True):
            st.session_state['melissa_msgs'] = [{"role":"assistant","content":"¡Hola de nuevo! ¿En qué puedo ayudarle?"}]
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

        user_input = st.chat_input("Escriba su pregunta a Melissa...", key="melissa_chat")
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

    sector = st.session_state.get('save_sector_nombre','su empresa')
    tam = st.session_state.get('save_tam_nombre','')
    reg = st.session_state.get('save_reg_nombre','')
    completados = sum(1 for i in range(1,6) if st.session_state.get(f'score_b{i}',0)>0)

    if key_msgs not in st.session_state:
        bienvenidas = {
            'indices': f"Buenos días, soy Félix. En esta página verá la posición competitiva de {sector} en 6 índices estratégicos clave. Recuerde que puede elegir con qué empresas compararse usando los filtros del panel lateral. Tiene {completados} de 5 bloques completados. ¿Desea que le explique qué significa cada índice?",
            'informe_estrategico': f"Buenos días, soy Félix. El Informe Estratégico le ofrece un análisis competitivo completo de {sector} generado por IA. Pulse 'Generar Informe' y en unos 15 segundos dispondrá de un análisis ejecutivo de unas 700 palabras, descargable en Word y PDF. ¿Empezamos?",
            'informe_innovacion': f"Buenos días, soy Félix. En esta página verá el diagnóstico completo de innovación de {sector} por los 5 bloques y 19 subindicadores. ¿Desea que le explique cómo interpretar los resultados?",
            'plan': f"Buenos días, soy Félix. El Plan de Acción generará 5 acciones estratégicas priorizadas para {sector} y una hoja de ruta 1-3 años completamente personalizada con IA. ¿Lo generamos ahora?",
            'benchmarking': f"Buenos días, soy Félix. En esta sección puede comparar {sector} con las empresas líderes del sector usando múltiples filtros de comparación. ¿Le explico cómo sacarle el máximo partido?",
            'analytics': f"Buenos días, soy Félix. En Analytics encontrará visualizaciones detalladas de todos los indicadores de {sector} con distintos filtros de análisis. ¿En qué puedo ayudarle?",
            'cuestionario': f"Buenos días, soy Félix. Está en el cuestionario de innovación, que consta de 5 bloques: I+D+i, Gestión de Proyectos, Desarrollo de Productos, Estrategia de Innovación y Desempeño de Innovación. Lleva {completados} de 5 completados. ¿Le explico cómo responder o desea continuar con el siguiente bloque?",
        }
        msg = bienvenidas.get(pagina, f"Buenos días, soy Félix, su consultor estratégico. Estoy aquí para ayudarle a sacar el máximo partido de esta plataforma. ¿En qué puedo ayudarle?")
        st.session_state[key_msgs] = [{"role":"assistant","content":msg}]

    if key_exp not in st.session_state:
        st.session_state[key_exp] = False

    img_b64 = _imagen_base64('felix.png')

    # System prompt completo con contexto de página
    contexto_pagina = FELIX_PAGINAS.get(pagina, "")
    felix_system = FELIX_SYSTEM_BASE + f"\n\n{contexto_pagina}\n\nCONTEXTO EMPRESA: {sector} | {tam} | {reg} | Bloques completados: {completados}/5"

    ultimo = st.session_state[key_msgs][-1]['content']
    ultimo_corto = ultimo[:130] + "..." if len(ultimo) > 130 else ultimo

    st.markdown(_banner_asistente(img_b64, "Félix", "Su asesor estratégico", "#1e3a5f", ultimo_corto), unsafe_allow_html=True)

    col_expand, col_reset = st.columns([3,1])
    with col_expand:
        label = "▲ Ocultar conversación" if st.session_state[key_exp] else "💬 Consultar con Félix"
        if st.button(label, key=f"felix_expand_{pagina}", use_container_width=True):
            st.session_state[key_exp] = not st.session_state[key_exp]
            st.rerun()
    with col_reset:
        if st.button("↺ Reiniciar", key=f"felix_reset_{pagina}", use_container_width=True):
            st.session_state[key_msgs] = [{"role":"assistant","content":f"¡Buenos días de nuevo! ¿En qué puedo ayudarle con {sector}?"}]
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

        user_input = st.chat_input("Consulte con Félix...", key=f"felix_chat_{pagina}")
        if user_input:
            st.session_state[key_msgs].append({"role":"user","content":user_input})
            with st.spinner("Félix está analizando..."):
                r = _llamar_ia(felix_system, st.session_state[key_msgs])
            st.session_state[key_msgs].append({"role":"assistant","content":r})
            st.rerun()

    st.markdown("---")