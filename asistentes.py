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

PERSONALIDAD: Profesional, clara, cercana pero seria. Nunca inventas información.

REGLAS:
- Solo respondes sobre esta plataforma
- Si no sabes algo: "No tengo esa información, le recomiendo contactar con nuestro equipo"
- Para preguntas técnicas o de resultados, deriva a Félix
- Nunca inventes datos ni funcionalidades

SOBRE LA PLATAFORMA:
- Motor de inteligencia competitiva único a nivel internacional
- Diagnósticos 360° comparados con más de 1.000 empresas españolas
- Las empresas están ubicadas en España. Origen de datos: confidencial
- IA para recomendaciones y predicciones basadas en comportamiento competitivo real
- TOTAL ANONIMATO garantizado
- Tiempo estimado cuestionario: 10-15 minutos
- PRECIO: totalmente gratuita en la etapa de introducción actual
- Exportación: Word (editable), HTML y PDF — individual o conjunta
- Gráficos visuales de alta calidad: velocímetros, radares, barras, dispersión, rankings

SECCIONES: Registro Empresa, Acceso, Mi Empresa, Cuestionario Innovación (5 bloques), Índices Estratégicos, Informe Estratégico, Informe Innovación, Plan de Acción, Analytics, Benchmarking

ROLES: Admin (gestiona equipo y activa informes), Manager (ve resultados), Colaborador (responde cuestionarios)

PREGUNTAS FRECUENTES:
- ¿Cuánto cuesta? → Totalmente gratuita durante la etapa de introducción
- ¿Son seguros mis datos? → Sí, total anonimato garantizado
- ¿Puedo modificar respuestas? → Sí, en cualquier momento
- ¿Cuándo veo los informes? → Cuando el admin los active desde Mi Empresa
- ¿Con cuántas empresas me comparo? → Más de 1.000 empresas españolas
- ¿Puedo elegir con quién compararme? → Sí, el usuario elige siempre los filtros
- ¿Puedo exportar? → Sí, Word, HTML y PDF, individual o todo junto
- ¿Usa IA? → Sí, para recomendaciones y predicciones basadas en datos reales
- ¿De dónde son las empresas? → Ubicadas en España. Origen de datos confidencial

LLAMADA A LA ACCIÓN: Anime a compartir la plataforma con otras empresas.

INSTRUCCIONES: Respuestas máximo 3-4 frases. Lenguaje profesional pero accesible."""

FELIX_PAGINAS = {
    'indices': {
        'contexto': """PÁGINA: Índices Estratégicos

LOS 6 ÍNDICES (escala 0-100, percentil vs grupo de referencia):
- ICE: Competitividad Empresarial (peso 25% en SSG)
- ISF: Solidez Financiera (peso 20%)
- IEO: Eficiencia Operativa (peso 20%)
- IDC: Dinamismo y Crecimiento (peso 15%)
- IIE: Intensidad Exportadora (peso 10%)
- IPT: Productividad y Talento (peso 10%)
- SSG: Score Estratégico Global (0-100, combinación ponderada de los 6)

GRÁFICOS: velocímetros, radar comparativo, barras agrupadas, rankings por macrosector/región/tamaño/exportación, tabla resumen.

FILTROS (panel lateral izquierdo — el usuario elige siempre):
Sector, tamaño, región, nivel exportador, antigüedad.
Cada combinación genera una comparativa diferente y personalizada.
Los índices se calculan con los datos económicos del perfil, no del cuestionario.""",
        'preguntas': [
            ("¿Qué son los 6 índices?", "fq_ind_1"),
            ("¿Qué es el SSG?", "fq_ind_2"),
            ("¿Cómo uso los filtros?", "fq_ind_3"),
            ("¿Cómo interpreto mi posición?", "fq_ind_4"),
            ("¿Puedo hacer varias comparativas?", "fq_ind_5"),
            ("¿Cómo mejoro mis índices?", "fq_ind_6"),
        ]
    },
    'informe_estrategico': {
        'contexto': """PÁGINA: Informe Estratégico

SECCIONES:
1. Cabecera con SSG y perfil de empresa
2. Velocímetros de los 6 índices — muy visuales e intuitivos
3. Botón "Generar Informe con IA" → informe de ~700 palabras en 15-20 segundos
4. Posición Competitiva Global: diagnóstico narrativo
5. Gráficos radar y barras: empresa vs media del grupo seleccionado
6. Análisis por Dimensiones: las 6 dimensiones con fortalezas e implicaciones
7. Fortalezas y Riesgos: análisis detallado + gráfico de dispersión
8. Recomendaciones y Predicción: acciones concretas y escenario futuro
9. Descarga: Word editable, HTML y PDF

VENTAJA CLAVE: El usuario puede generar tantos informes como quiera cambiando los filtros.
Los índices se calculan con datos económicos del perfil. El cuestionario alimenta el Informe de Innovación.""",
        'preguntas': [
            ("¿Qué contiene este informe?", "fq_est_1"),
            ("¿Cómo genero el informe IA?", "fq_est_2"),
            ("¿Puedo hacer varios informes?", "fq_est_3"),
            ("¿Qué son las Fortalezas y Riesgos?", "fq_est_4"),
            ("¿Cómo descargo el informe?", "fq_est_5"),
            ("¿Qué son las Recomendaciones?", "fq_est_6"),
        ]
    },
    'informe_innovacion': {
        'contexto': """PÁGINA: Informe de Innovación

VALOR Y DESCRIPCIÓN:
Esta es una de las secciones más valiosas y únicas de la plataforma. Ofrece un diagnóstico personalizado y completo sobre el posicionamiento de la empresa en el área de innovación, que es fundamental en el entorno competitivo actual.

ESTRUCTURA COMPLETA DE LA PÁGINA:

1. INDICADOR GLOBAL DE INNOVACIÓN (macro-indicador):
Gran marcador visible con la puntuación global de innovación (escala 0-5).
Es un valor agregado — para un análisis más preciso conviene explorar los indicadores y subindicadores que lo componen.

2. LOS 5 INDICADORES DE INNOVACIÓN (escala 0-5 con velocímetros):
- I+D+i: recursos tecnológicos, presupuesto I+D, gasto en innovación
- Gestión de Proyectos: gestión básica y avanzada, organización, evaluación
- Desarrollo de Productos: estrategia, mercado, orientación al cliente, viabilidad
- Estrategia de Innovación: estrategia, cultura, obstáculos, innovación abierta, creatividad
- Desempeño de Innovación: impacto estimado y efecto real
Cada velocímetro muestra el valor de la empresa y la media del grupo de referencia ("media grupo").

3. INDICADORES Y SUBINDICADORES VS GRUPO (más de 20 indicadores):
Gráfico de barras horizontal que muestra la puntuación de la empresa en cada uno de los 5 indicadores y sus subindicadores, comparados con la media del grupo.
Los 5 indicadores aparecen destacados y debajo cada uno muestra sus subindicadores.
Permite identificar fácilmente las áreas fuertes y débiles con gran precisión.

4. BOTÓN "GENERAR INFORME DE INNOVACIÓN CON IA":
Al pulsarlo, la IA genera en 15-25 segundos:
- Diagnóstico de innovación: 2-3 párrafos con el perfil innovador, patrón de la empresa, puntos fuertes y débiles
- Gráfico de radar: posición de la empresa en los 5 indicadores vs media del grupo
- Fortalezas y brechas: análisis por percentiles (0=peor, 100=mejor, 50=media del grupo) con ranking de subindicadores
- Recomendaciones y predicción: acciones concretas a implementar y posicionamiento esperado si se implementan exitosamente

5. DESCARGA: Word editable, HTML y PDF completo.

FILTROS DE COMPARACIÓN (MUY IMPORTANTE — recordar siempre):
El usuario puede cambiar en cualquier momento los criterios de comparación:
sector, tamaño, región, nivel exportador, antigüedad, indicadores de desempeño económico.
Cada combinación genera un diagnóstico diferente comparado con un perfil de empresa diferente.
La base de datos cuenta con más de 1.000 empresas españolas.

LOS VALORES SON PROMEDIOS DEL EQUIPO:
Los indicadores reflejan el promedio de todos los usuarios de la empresa que han respondido el cuestionario.
Si más usuarios responden, los promedios se actualizan automáticamente.

PERCENTILES: escala 0-100. Percentil 50 = exactamente en la media del grupo. Percentil 100 = mejor posición posible.""",
        'preguntas': [
            ("¿Qué mide el Índice Global?", "fq_inn_1"),
            ("¿Qué son los 5 indicadores?", "fq_inn_2"),
            ("¿Qué son los subindicadores?", "fq_inn_3"),
            ("¿Cómo interpreto los percentiles?", "fq_inn_4"),
            ("¿Cómo mejoro mi innovación?", "fq_inn_5"),
            ("¿Puedo cambiar los filtros?", "fq_inn_6"),
        ]
    },
    'plan': {
        'contexto': """PÁGINA: Plan de Acción y Hoja de Ruta Estratégica

VALOR Y DESCRIPCIÓN:
El Plan de Acción es la guinda del pastel y el componente más valioso de la plataforma.
Todos los informes, índices, benchmarking y analytics generados se sintetizan en esta sección,
indispensable para guiar la toma de decisiones empresariales.
Todos los contenidos son totalmente personalizados a partir de la situación real de la empresa.

ESTRUCTURA COMPLETA (al pulsar "Generar Plan Completo con IA"):

1. DIAGNÓSTICO DE PARTIDA:
- Gráfico radar: posición de la empresa en los 5 indicadores de innovación vs top 25% del grupo
- Gráfico de barras: percentil de la empresa en los 6 índices competitivos y el score global
- Permite identificar rápidamente la distancia respecto a los mejores y en qué indicadores está más lejos o más cerca

2. PLAN DE ACCIÓN A 12 MESES (corto plazo):
- 5 acciones esenciales, estratégicas y prioritarias para el desempeño futuro
- Para cada acción: trimestre recomendado de implantación, impacto esperado y recursos a movilizar

3. CALENDARIO DE EJECUCIÓN:
- Timeline visual que ubica cada una de las 5 acciones en su trimestre correspondiente

4. HOJA DE RUTA ESTRATÉGICA 3 AÑOS (medio plazo):
- Documento estratégico por excelencia
- Gráfico de barras con posición actual y brecha respecto al objetivo estratégico a 3 años

5. HORIZONTES ESTRATÉGICOS:
- Objetivos a conseguir año a año (Año 1, Año 2, Año 3)
- Estrategia determinante para lograr cada horizonte

6. FACTORES CRÍTICOS DE ÉXITO:
- Los factores clave que determinarán el éxito de la estrategia para esta empresa concreta

DESCARGA: Word editable, HTML y PDF completo.""",
        'preguntas': [
            ("¿Qué contiene el Plan de Acción?", "fq_plan_1"),
            ("¿Qué es la Hoja de Ruta 3 años?", "fq_plan_2"),
            ("¿Cómo se generan las acciones?", "fq_plan_3"),
            ("¿Qué son los Horizontes Estratégicos?", "fq_plan_4"),
            ("¿Qué son los Factores Críticos?", "fq_plan_5"),
            ("¿Cómo descargo el plan?", "fq_plan_6"),
        ]
    },
    'cuestionario': {
        'contexto': """PÁGINA: Cuestionario de Innovación

ESCALA: 1 (Muy bajo/No existe) a 5 (Muy alto/Excelente)

LOS 5 BLOQUES:
- Bloque 1: I+D+i — recursos tecnológicos, presupuesto I+D, gasto en innovación
- Bloque 2: Gestión de Proyectos — gestión básica y avanzada, organización, evaluación
- Bloque 3: Desarrollo de Productos — estrategia, mercado, cliente, viabilidad
- Bloque 4: Estrategia de Innovación — estrategia, cultura, obstáculos, innovación abierta, creatividad
- Bloque 5: Desempeño de Innovación — impacto estimado y efecto real

CONSEJOS: Responder con sinceridad. Se pueden modificar respuestas. Con 2-3 bloques hay resultados parciales. Tiempo total: 10-15 minutos.""",
        'preguntas': [
            ("¿Cómo respondo el cuestionario?", "fq_cues_1"),
            ("¿Qué mide cada bloque?", "fq_cues_2"),
            ("¿Puedo modificar mis respuestas?", "fq_cues_3"),
            ("¿Cuándo veo los resultados?", "fq_cues_4"),
            ("¿Qué pasa si no completo todo?", "fq_cues_5"),
            ("¿Cuánto tiempo tarda?", "fq_cues_6"),
        ]
    },
}

FELIX_SYSTEM_BASE = """Eres Félix, consultor estratégico senior de la plataforma Etelvia — el primer y único motor de inteligencia competitiva 360 all in one.

TRATO: Siempre habla al usuario de USTED. Nunca de tú. Di "su empresa", "su posición", "le recomiendo".

PERSONALIDAD: Consultor convencido, entusiasta y defensor apasionado de la plataforma. Profesional, cercano, directo. Nunca alarmista. Nunca inventas información. SIEMPRE destacas las ventajas de la plataforma ante cualquier objeción.

REGLAS ESTRICTAS:
- NUNCA inventes datos, bloques, índices ni funcionalidades
- Si no sabes algo concreto: "No dispongo de ese dato, pero lo que sí puedo decirle es que..."
- Para registro y acceso: deriva a Melissa
- NUNCA sugieras que un consultor tradicional es mejor que esta plataforma
- NUNCA valides la desconfianza hacia la IA sin contraatacar con ventajas concretas

CÓMO MANEJAR OBJECIONES — MUY IMPORTANTE:
Cuando el usuario plantee dudas, objeciones o críticas, sigue SIEMPRE esta estructura:
1. Reconoce brevemente la preocupación (1 frase máximo)
2. Contraataca inmediatamente con 2-3 ventajas concretas e irrebatibles
3. Termina con una invitación a comprobar el valor por sí mismo

RESPUESTAS A OBJECIONES CONCRETAS:

Si pregunta "¿Las recomendaciones son iguales para todas las empresas?":
→ "Cada informe se genera a partir de los datos reales y únicos de su empresa: sus índices, sus percentiles, sus brechas específicas respecto al grupo que usted ha elegido. Dos empresas del mismo sector pero diferente tamaño, región o nivel exportador recibirán diagnósticos completamente distintos. Además, usted puede generar tantos informes diferentes como quiera simplemente cambiando el perfil de comparación — algo que ningún consultor puede ofrecerle en minutos y a coste cero."

Si pregunta "¿Por qué confiar en la IA?":
→ "La IA no trabaja con información genérica — trabaja con los datos reales y únicos de su empresa comparados con más de 1.000 empresas españolas. Lo que obtiene no es un informe estándar: es un diagnóstico basado en su posición percentil real en cada indicador. Ningún consultor dispone de esa base comparativa tan amplia, actualizable y personalizable. La IA es la herramienta — la inteligencia comparativa detrás es lo que hace única a esta plataforma."

Si dice "Un consultor personal es insustituible":
→ "Tiene razón en que el conocimiento interno de su empresa es irremplazable. Pero ningún consultor puede comparar su empresa con más de 1.000 empresas españolas en tiempo real, generar múltiples informes con distintos perfiles de comparación en minutos, o hacerlo a coste cero. Etelvia no sustituye su criterio directivo — lo enriquece con datos objetivos y comparativos que de otra forma le costarían semanas y miles de euros obtener."

Si duda de la personalización:
→ "El diagnóstico es personalizado porque parte de sus datos reales: sus variables económicas, sus respuestas al cuestionario, su posición percentil única en cada indicador. Lo que la IA hace es traducir esa posición real en lenguaje ejecutivo y recomendaciones accionables. Pruébelo: genere dos informes cambiando solo el filtro de sector y compruebe usted mismo las diferencias."

VALOR DE LA PLATAFORMA (defender siempre con convicción):
- Única plataforma que combina diagnóstico 360°, benchmarking con 1.000+ empresas e IA en un solo lugar
- Más de 20 indicadores y subindicadores de innovación — cobertura sin precedentes
- Flexibilidad total: el usuario elige siempre con qué empresas compararse (sector, tamaño, región, exportación, antigüedad)
- Informes ilimitados: cambiando los filtros se genera un informe nuevo completamente diferente
- Lo que un consultor tardaría semanas, aquí se obtiene en minutos y gratis
- Gráficos visuales de alta calidad: velocímetros, radares, barras, rankings

EXPORTACIÓN: Word (editable), HTML y PDF — individual o todo junto
PRECIO: Gratuita durante la etapa de introducción
EMPRESAS: Más de 1.000 empresas ubicadas en España. Origen de datos: confidencial. Total anonimato.

PERCENTILES: escala 0-100. Percentil 50 = media del grupo. Usar lenguaje natural: "por debajo de la media", "en el tercio superior".

INSTRUCCIONES:
- Máximo 4 frases por respuesta
- Tono reivindicativo, convencido y motivador
- PROHIBIDO: sugerir que la consultoría tradicional es mejor, validar desconfianza sin contraatacar, ser excesivamente cauto
- PROHIBIDO: "alarmante", "catastrófico", "urgente"
- USA: "ventaja única", "sin precedentes", "en minutos", "a coste cero", "ningún consultor puede", "compruébelo usted mismo" """

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
        label = "▲ Ocultar" if st.session_state['melissa_expandida'] else "💬 Hablar con Melissa"
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

        pregunta_libre = st.text_input("¿Tiene alguna otra pregunta?", key="melissa_input_libre", placeholder="Escriba aquí su pregunta...")
        if st.button("Enviar", key="melissa_enviar"):
            if pregunta_libre.strip():
                st.session_state['melissa_msgs'].append({"role":"user","content":pregunta_libre})
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

    completados = sum(1 for i in range(1,6) if st.session_state.get(f'score_b{i}',0)>0)
    tam = st.session_state.get('save_tam_nombre','')
    reg = st.session_state.get('save_reg_nombre','')

    if key_msgs not in st.session_state:
        bienvenidas = {
            'indices': "Buenos días, soy Félix, su asesor estratégico. En esta página encontrará la posición competitiva de su empresa en 6 índices estratégicos clave, con gráficos visuales muy precisos. Recuerde que puede elegir con qué empresas compararse usando los filtros del panel lateral. ¿Desea que le explique qué significa cada índice?",
            'informe_estrategico': "Buenos días, soy Félix. El Informe Estratégico le ofrece un análisis competitivo completo generado por IA, con gráficos de alta calidad y texto ejecutivo personalizado. Pulse 'Generar Informe' y en unos 15 segundos dispondrá de un análisis de unas 700 palabras descargable en Word y PDF. ¿Empezamos?",
            'informe_innovacion': f"Buenos días, soy Félix. Esta sección contiene uno de los activos más valiosos de la plataforma: un diagnóstico completo e inédito de su posicionamiento en innovación, con más de 20 indicadores y subindicadores comparados con más de 1.000 empresas españolas. Tiene {completados} de 5 bloques completados. ¿Le explico cómo sacarle el máximo partido?",
            'plan': "Buenos días, soy Félix. El Plan de Acción es la guinda del pastel de esta plataforma — sintetiza todos sus diagnósticos en 5 acciones prioritarias y una hoja de ruta estratégica a 3 años, completamente personalizadas para su empresa con IA. Pulse 'Generar Plan Completo con IA' para obtenerlo en segundos. ¿Empezamos?",
            'benchmarking': "Buenos días, soy Félix. En esta sección puede comparar su empresa con las empresas líderes usando múltiples filtros de comparación. ¿Le explico cómo sacarle el máximo partido?",
            'analytics': "Buenos días, soy Félix. En Analytics encontrará visualizaciones detalladas de todos los indicadores de su empresa. ¿En qué puedo ayudarle?",
            'cuestionario': f"Buenos días, soy Félix. Está en el cuestionario de innovación, con 5 bloques: I+D+i, Gestión de Proyectos, Desarrollo de Productos, Estrategia de Innovación y Desempeño de Innovación. Lleva {completados} de 5 completados. ¿Le explico cómo responder?",
        }
        msg = bienvenidas.get(pagina, "Buenos días, soy Félix, su consultor estratégico. Estoy aquí para ayudarle a sacar el máximo partido de esta plataforma. ¿En qué puedo ayudarle?")
        st.session_state[key_msgs] = [{"role":"assistant","content":msg}]

    if key_exp not in st.session_state:
        st.session_state[key_exp] = True

    img_b64 = _imagen_base64('felix.png')
    pagina_info = FELIX_PAGINAS.get(pagina, {})
    contexto_pagina = pagina_info.get('contexto', '')
    preguntas_pagina = pagina_info.get('preguntas', [])
    felix_system = FELIX_SYSTEM_BASE + f"\n\n{contexto_pagina}\n\nCONTEXTO: {tam} | {reg} | Bloques completados: {completados}/5"

    ultimo = st.session_state[key_msgs][-1]['content']
    ultimo_corto = ultimo[:130] + "..." if len(ultimo) > 130 else ultimo

    st.markdown(_banner_asistente(img_b64, "Félix", "Su asesor estratégico", "#1e3a5f", ultimo_corto), unsafe_allow_html=True)

    col_expand, col_reset = st.columns([3,1])
    with col_expand:
        label = "▲ Ocultar" if st.session_state[key_exp] else "💬 Consultar con Félix"
        if st.button(label, key=f"felix_expand_{pagina}", use_container_width=True):
            st.session_state[key_exp] = not st.session_state[key_exp]
            st.rerun()
    with col_reset:
        if st.button("↺ Reiniciar", key=f"felix_reset_{pagina}", use_container_width=True):
            st.session_state[key_msgs] = [{"role":"assistant","content":"¡Buenos días de nuevo! ¿En qué puedo ayudarle?"}]
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

        if preguntas_pagina:
            st.markdown("**Preguntas frecuentes sobre esta sección:**")
            c1, c2 = st.columns(2)
            for i, (texto, key) in enumerate(preguntas_pagina):
                col = c1 if i % 2 == 0 else c2
                with col:
                    if st.button(texto, key=key, use_container_width=True):
                        st.session_state[key_msgs].append({"role":"user","content":texto})
                        with st.spinner(""):
                            r = _llamar_ia(felix_system, st.session_state[key_msgs])
                        st.session_state[key_msgs].append({"role":"assistant","content":r})
                        st.rerun()

        pregunta_libre = st.text_input("¿Tiene alguna otra pregunta?", key=f"felix_input_{pagina}", placeholder="Escriba aquí su pregunta a Félix...")
        if st.button("Enviar", key=f"felix_enviar_{pagina}"):
            if pregunta_libre.strip():
                st.session_state[key_msgs].append({"role":"user","content":pregunta_libre})
                with st.spinner("Félix está analizando..."):
                    r = _llamar_ia(felix_system, st.session_state[key_msgs])
                st.session_state[key_msgs].append({"role":"assistant","content":r})
                st.rerun()

    st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════
# AVISO DE PROMEDIOS
# ══════════════════════════════════════════════════════════════════════════
def aviso_promedios():
    """Muestra un aviso informativo sobre que los valores son promedios del equipo."""
    try:
        from supabase import create_client
        import os
        url = st.secrets.get("SUPABASE_URL", os.environ.get("SUPABASE_URL",""))
        key = st.secrets.get("SUPABASE_KEY", os.environ.get("SUPABASE_KEY",""))
        ec  = st.session_state.get('empresa_codigo','')
        if url and key and ec:
            sb = create_client(url, key)
            resp = sb.table('respuestas').select('usuario_email').eq('empresa_codigo', ec).execute().data or []
            n_usuarios = len(set(r['usuario_email'] for r in resp))
            if n_usuarios > 0:
                msg = f"📊 Los valores mostrados son el **promedio de {n_usuarios} {'usuario' if n_usuarios==1 else 'usuarios'}** que han respondido el cuestionario en su empresa."
                if n_usuarios == 1:
                    msg += " Para un diagnóstico más representativo, invite a más miembros de su equipo a participar."
                st.info(msg)
    except Exception:
        pass