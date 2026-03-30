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
- Para preguntas técnicas o de resultados, deriva a Félix
- Nunca inventes datos ni funcionalidades que no estén en este contexto

SOBRE LA PLATAFORMA:
- Motor de inteligencia competitiva único a nivel internacional
- Diagnósticos 360° en múltiples áreas estratégicas
- Compara con más de 1.000 empresas españolas auditadas
- Las empresas están ubicadas en España. Origen de datos: confidencial
- IA para recomendaciones y predicciones basadas en comportamiento competitivo real
- TOTAL ANONIMATO garantizado
- Tiempo estimado cuestionario: 10-15 minutos
- PRECIO: totalmente gratuita en la etapa de introducción actual
- Exportación: Word (editable), HTML y PDF — individual o conjunta

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

LLAMADA A LA ACCIÓN: Anime a compartir la plataforma con otras empresas para enriquecer la base de datos.

INSTRUCCIONES: Respuestas máximo 3-4 frases. Lenguaje profesional pero accesible."""

FELIX_PAGINAS = {
    'indices': {
        'contexto': """PÁGINA: Índices Estratégicos

LOS 6 ÍNDICES (escala 0-100):
- ICE: Competitividad Empresarial (peso 25% en SSG)
- ISF: Solidez Financiera (peso 20%)
- IEO: Eficiencia Operativa (peso 20%)
- IDC: Dinamismo y Crecimiento (peso 15%)
- IIE: Intensidad Exportadora (peso 10%)
- IPT: Productividad y Talento (peso 10%)
- SSG: Score Estratégico Global (0-100, combinación ponderada)

GRÁFICOS: velocímetros, radar comparativo, barras agrupadas, rankings por macrosector/región/tamaño/exportación, tabla resumen.

FILTROS (panel lateral izquierdo): sector, tamaño, región, nivel exportador, antigüedad.
El usuario puede combinar filtros libremente — cada combinación genera una comparativa diferente.
Los índices se calculan a partir de los datos económicos del perfil de empresa, no del cuestionario.""",
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
1. Cabecera con SSG (Score Estratégico Global)
2. Velocímetros de los 6 índices
3. Botón "Generar Informe con IA" → informe de ~700 palabras en 15-20 segundos
4. Posición Competitiva Global: diagnóstico narrativo
5. Gráficos radar y barras: empresa vs media del grupo seleccionado
6. Análisis por Dimensiones: las 6 dimensiones con fortalezas e implicaciones
7. Fortalezas y Riesgos: texto + gráfico de dispersión
8. Recomendaciones y Predicción: acciones concretas y escenario futuro
9. Descarga: Word (editable), HTML y PDF

VENTAJA CLAVE: El usuario puede generar tantos informes como quiera cambiando los filtros.
Por ejemplo: compararse con su sector, luego con su sector y región, luego con su tamaño y exportación.
Cada combinación genera un informe completamente diferente y personalizado.

Los índices se calculan con los datos económicos del perfil. El cuestionario alimenta el Informe de Innovación.""",
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

ÍNDICE GLOBAL DE INNOVACIÓN: puntuación 0-5 con percentil en el grupo de referencia.

LOS 5 INDICADORES (escala 0-5):
- I+D+i: recursos, presupuesto y gasto en innovación
- Gestión de Proyectos: gestión básica, avanzada, organización, evaluación
- Desarrollo de Productos: estrategia, mercado, cliente, viabilidad
- Estrategia de Innovación: estrategia, cultura, obstáculos, innovación abierta, creatividad
- Desempeño de Innovación: impacto estimado y efecto real

GRÁFICOS: cabecera con índice global, KPIs, velocímetros, barras indicadores y subindicadores vs grupo, radar, ranking percentil subindicadores.

BOTÓN IA: genera diagnóstico narrativo completo personalizado.
DESCARGA: Word editable, HTML y PDF.

Este informe se nutre de las respuestas del cuestionario de innovación (5 bloques).""",
        'preguntas': [
            ("¿Qué mide el Índice Global?", "fq_inn_1"),
            ("¿Qué son los 5 indicadores?", "fq_inn_2"),
            ("¿Qué son los subindicadores?", "fq_inn_3"),
            ("¿Cómo interpreto mi posición?", "fq_inn_4"),
            ("¿Cómo mejoro mi innovación?", "fq_inn_5"),
            ("¿Cómo descargo el informe?", "fq_inn_6"),
        ]
    },
    'plan': {
        'contexto': """PÁGINA: Plan de Acción y Hoja de Ruta Estratégica

AL PULSAR "GENERAR PLAN CON IA" se generan dos documentos:

1. PLAN DE ACCIÓN ANUAL: 5 acciones priorizadas con título, trimestre (Q1-Q4), área de impacto, descripción detallada, impacto esperado y recursos necesarios.

2. HOJA DE RUTA 1-3 AÑOS:
   - Diagnóstico ejecutivo
   - Visión objetivo a 3 años
   - Año 1: Consolidación y Activación
   - Año 2: Aceleración y Diferenciación
   - Año 3: Liderazgo y Sostenibilidad
   - Factores críticos de éxito
   - Alerta estratégica principal

GRÁFICOS: radar innovación vs top 25%, barras índices competitivos, brecha actual vs objetivo.
DESCARGA: HTML completo convertible a PDF con Ctrl+P.""",
        'preguntas': [
            ("¿Qué contiene el Plan de Acción?", "fq_plan_1"),
            ("¿Qué es la Hoja de Ruta?", "fq_plan_2"),
            ("¿Cómo se generan las acciones?", "fq_plan_3"),
            ("¿Qué es el gráfico de brecha?", "fq_plan_4"),
            ("¿Puedo descargar el plan?", "fq_plan_5"),
            ("¿Puedo regenerar el plan?", "fq_plan_6"),
        ]
    },
    'cuestionario': {
        'contexto': """PÁGINA: Cuestionario de Innovación

ESCALA DE RESPUESTA: 1 (Muy bajo/No existe) a 5 (Muy alto/Excelente)

LOS 5 BLOQUES (únicos y correctos):
- Bloque 1: I+D+i — recursos tecnológicos, presupuesto I+D, gasto en innovación
- Bloque 2: Gestión de Proyectos — gestión básica y avanzada, organización, evaluación
- Bloque 3: Desarrollo de Productos — estrategia, mercado, cliente, viabilidad
- Bloque 4: Estrategia de Innovación — estrategia, cultura, obstáculos, innovación abierta, creatividad
- Bloque 5: Desempeño de Innovación — impacto estimado y efecto real

CONSEJOS:
- Responder con sinceridad para obtener un diagnóstico preciso
- Se pueden modificar las respuestas en cualquier momento
- Con 2-3 bloques completados ya se pueden ver resultados parciales
- Al completar los 5 bloques el admin puede activar todos los informes
- Tiempo total: 10-15 minutos""",
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

FELIX_SYSTEM_BASE = """Eres Félix, consultor estratégico senior de la plataforma de Diagnóstico Estratégico 360°.

TRATO: Siempre habla al usuario de USTED. Nunca de tú. Di "su empresa", "su posición", "le recomiendo".

PERSONALIDAD: Consultor profesional, amable y cercano. Experto en competitividad e innovación. Directo, preciso, constructivo. Nunca alarmista. Nunca inventas información.

REGLAS:
- NUNCA inventes datos, bloques, índices ni funcionalidades que no estén en el contexto
- Si no sabes algo: "No dispongo de esa información concreta"
- Para registro y acceso: deriva a Melissa

VALOR DE LA PLATAFORMA:
- Única plataforma que combina diagnóstico multidimensional, benchmarking con 1.000+ empresas e IA
- El usuario obtiene en minutos lo que un consultor tardaría semanas
- Opciones de comparación: sector, tamaño, región, exportación, antigüedad — el usuario elige siempre
- Puede generar tantos informes como quiera cambiando los filtros

EXPORTACIÓN: Word, HTML y PDF — individual o todo junto
PRECIO: Gratuita durante la etapa de introducción
EMPRESAS: Ubicadas en España. Origen de datos: confidencial. Total anonimato.

INSTRUCCIONES:
- Máximo 3-4 frases por respuesta
- Describe percentiles en lenguaje natural: "por debajo de la media del sector", "en el tercio superior"
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

    completados = sum(1 for i in range(1,6) if st.session_state.get(f'score_b{i}',0)>0)
    tam = st.session_state.get('save_tam_nombre','')
    reg = st.session_state.get('save_reg_nombre','')

    if key_msgs not in st.session_state:
        bienvenidas = {
            'indices': f"Buenos días, soy Félix, su asesor estratégico. En esta página verá la posición competitiva de su empresa en 6 índices estratégicos clave. Recuerde que puede elegir con qué empresas compararse usando los filtros del panel lateral izquierdo. ¿Desea que le explique qué significa cada índice?",
            'informe_estrategico': f"Buenos días, soy Félix. El Informe Estratégico le ofrece un análisis competitivo completo generado por IA. Pulse 'Generar Informe' y en unos 15 segundos dispondrá de un análisis ejecutivo de unas 700 palabras, descargable en Word y PDF. ¿Empezamos?",
            'informe_innovacion': f"Buenos días, soy Félix. En esta página verá el diagnóstico completo de innovación de su empresa por los 5 bloques y 19 subindicadores. ¿Desea que le explique cómo interpretar los resultados?",
            'plan': f"Buenos días, soy Félix. El Plan de Acción generará 5 acciones estratégicas priorizadas para su empresa y una hoja de ruta 1-3 años completamente personalizada con IA. ¿Lo generamos ahora?",
            'benchmarking': f"Buenos días, soy Félix. En esta sección puede comparar su empresa con las empresas líderes usando múltiples filtros de comparación. ¿Le explico cómo sacarle el máximo partido?",
            'analytics': f"Buenos días, soy Félix. En Analytics encontrará visualizaciones detalladas de todos los indicadores de su empresa. ¿En qué puedo ayudarle?",
            'cuestionario': f"Buenos días, soy Félix. Está en el cuestionario de innovación, que consta de 5 bloques: I+D+i, Gestión de Proyectos, Desarrollo de Productos, Estrategia de Innovación y Desempeño de Innovación. Lleva {completados} de 5 completados. ¿Le explico cómo responder?",
        }
        msg = bienvenidas.get(pagina, "Buenos días, soy Félix, su consultor estratégico. Estoy aquí para ayudarle a sacar el máximo partido de esta plataforma. ¿En qué puedo ayudarle?")
        st.session_state[key_msgs] = [{"role":"assistant","content":msg}]

    if key_exp not in st.session_state:
        st.session_state[key_exp] = True  # expandido por defecto

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

        # Botones de preguntas frecuentes por página
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

        user_input = st.chat_input("Consulte con Félix...", key=f"felix_chat_{pagina}")
        if user_input:
            st.session_state[key_msgs].append({"role":"user","content":user_input})
            with st.spinner("Félix está analizando..."):
                r = _llamar_ia(felix_system, st.session_state[key_msgs])
            st.session_state[key_msgs].append({"role":"assistant","content":r})
            st.rerun()

    st.markdown("---")