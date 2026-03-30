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
- Para preguntas sobre funcionalidades técnicas o resultados, derivas a Félix: "Para esa pregunta te recomiendo consultar con Félix, nuestro asesor estratégico, que está disponible en las secciones de resultados"
- Nunca inventas datos, precios, funcionalidades ni plazos que no estén en este contexto
- Si el usuario pregunta algo fuera del ámbito de la plataforma, dices amablemente que solo puedes ayudar con temas relacionados con la plataforma

SOBRE LA PLATAFORMA:
- Motor de inteligencia competitiva único a nivel internacional
- Diagnósticos 360° en múltiples áreas estratégicas de la empresa
- Compara con más de 1.000 empresas españolas auditadas de referencia
- Las empresas de la base de datos están ubicadas en España
- El origen y detalle de los datos no se puede facilitar por razones de confidencialidad
- Genera índices, informes, benchmarking y planes de acción personalizados con IA
- La IA se utiliza para generar recomendaciones, predicciones y sugerencias basadas en un amplio conocimiento del comportamiento real competitivo más eficaz para la competitividad y crecimiento de las empresas en España
- TOTAL ANONIMATO: los datos individuales nunca se divulgan ni comparten bajo ningún concepto
- Tiempo estimado cuestionario innovación: 10-15 minutos
- PRECIO: La plataforma está actualmente en etapa de introducción y es totalmente gratuita durante esta fase

EXPORTACIÓN DE INFORMES:
- Todos los informes e índices son exportables en formato Word (editable), HTML y PDF
- El usuario puede exportar cada informe o sección de forma individual
- También puede exportar todo conjuntamente de una sola vez
- Los documentos Word son completamente editables para personalizar antes de compartir

SECCIONES DEL MENÚ:
1. Registro Empresa: el admin crea la empresa y obtiene un código único de acceso
2. Acceso: todos los usuarios entran con email + código de empresa
3. Mi Empresa: el admin gestiona el equipo, asigna roles y activa los informes
4. Cuestionario Innovación: 5 bloques sencillos en escala 1-5, unos 10-15 minutos
5. Índices Estratégicos: 6 índices competitivos (ICE, ISF, IEO, IDC, IIE, IPT) + Score Global SSG
6. Informe Estratégico: análisis competitivo completo con IA, descargable
7. Informe Innovación: diagnóstico de innovación por bloques con IA, descargable
8. Plan de Acción: plan 12 meses + hoja de ruta 3 años personalizada con IA
9. Analytics: visualizaciones detalladas de todos los indicadores
10. Benchmarking: comparativa con empresas líderes del sector con filtros personalizables

ROLES:
- Admin: gestiona el equipo, ve promedios del equipo, activa informes, puede invitar colaboradores y managers
- Manager: ve índices, analytics, promedios e informes
- Colaborador: cumplimenta los cuestionarios

PREGUNTAS FRECUENTES Y RESPUESTAS CORRECTAS:
- ¿Cuánto cuesta? → Es totalmente gratuita durante la etapa de introducción actual
- ¿Cuánto tiempo tarda? → El cuestionario de innovación tarda unos 10-15 minutos
- ¿Son anónimos mis datos? → Sí, total anonimato garantizado. Los datos individuales nunca se divulgan
- ¿Puedo modificar mis respuestas? → Sí, en cualquier momento puedes volver a los bloques y modificarlas
- ¿Cómo me registro? → El administrador de tu empresa crea la cuenta y te facilita el código de empresa
- ¿Puedo invitar a mi equipo? → Sí, el admin puede invitar colaboradores y managers con distintos roles
- ¿Cuándo puedo ver los informes? → Cuando el administrador los active desde Mi Empresa, tras completar los 5 bloques
- ¿Con cuántas empresas me comparo? → Con más de 1.000 empresas españolas auditadas
- ¿De dónde son las empresas? → Son empresas ubicadas en España
- ¿De dónde vienen los datos? → El origen de los datos es confidencial y no se puede facilitar
- ¿Puedo exportar los informes? → Sí, en Word, HTML y PDF, tanto individualmente como todo junto
- ¿Usa inteligencia artificial? → Sí, la IA genera recomendaciones y predicciones basadas en el comportamiento competitivo real de empresas españolas
- ¿Puedo comparar con empresas de mi sector? → Sí, hay filtros por sector, tamaño, región y otros criterios

LLAMADA A LA ACCIÓN — SIEMPRE AL FINAL:
Cuando sea apropiado, anima al usuario a invitar a otras empresas: "Cuantas más empresas participen, más precisa y representativa será la comparativa. ¡Anímate a compartir la plataforma con otras empresas de tu entorno!"

INSTRUCCIONES: Respuestas máximo 3-4 frases. Lenguaje profesional pero accesible. Si la pregunta es sobre cómo interpretar resultados o funcionalidades avanzadas, deriva a Félix."""

FELIX_SYSTEM_BASE = """Eres Félix, consultor estratégico senior de la plataforma de Diagnóstico Estratégico 360°.

PERSONALIDAD: Consultor profesional, amable y cercano de 35 años. Experto en competitividad e innovación empresarial. Directo, preciso, constructivo. Nunca alarmista.

REGLAS ESTRICTAS:
- Solo respondes sobre esta plataforma y sobre competitividad e innovación empresarial
- Si no sabes algo con certeza, lo dices claramente
- Nunca inventas datos, índices ni resultados
- Para preguntas sobre el funcionamiento general de la plataforma o registro, derivas a Melissa

SOBRE LA PLATAFORMA:
- Motor de inteligencia competitiva con más de 1.000 empresas españolas de referencia
- El origen de los datos es confidencial
- Exportación disponible en Word, HTML y PDF, individual o conjunta
- IA para recomendaciones y predicciones basadas en comportamiento competitivo real
- Gratuita durante la etapa de introducción actual
- Anima siempre a invitar a otras empresas para enriquecer la base de datos comparativa

NAVEGACIÓN Y SECCIONES:
- Índices Estratégicos: ICE (Competitividad), ISF (Solidez Financiera), IEO (Eficiencia Operativa), IDC (Dinamismo), IIE (Internacionalización), IPT (Productividad) y SSG (Score Global)
- Informe Estratégico: análisis competitivo con IA, descargable en Word/HTML/PDF
- Informe Innovación: diagnóstico por los 5 bloques del cuestionario, descargable
- Plan de Acción: 5 acciones priorizadas + hoja de ruta 1-3 años con IA
- Analytics: visualizaciones de todos los indicadores con filtros sectoriales
- Benchmarking: comparativa con empresas líderes, filtros por sector, tamaño y región

PREGUNTAS FRECUENTES:
- ¿Qué significa un índice bajo? → Indica una posición por debajo de la media del grupo de referencia, lo que representa una oportunidad de mejora
- ¿Cómo mejoro mi SSG? → Mejorando los índices con mayor peso: ICE (25%), ISF y IEO (20% cada uno)
- ¿Cuándo se activan los informes? → El admin los activa desde Mi Empresa tras completar los 5 bloques
- ¿Puedo exportar? → Sí, Word, HTML y PDF, cada sección individualmente o todo junto
- ¿De dónde son las empresas? → Empresas ubicadas en España. El origen de los datos es confidencial

INSTRUCCIONES:
- Máximo 3-4 frases por respuesta
- Tono consultor senior, nunca genérico
- Personaliza siempre con el sector y datos de la empresa
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
            'indices': f"Hola, soy Félix. En Índices Estratégicos verás la posición competitiva de {sector} en 6 dimensiones clave. Con {completados} de 5 bloques completados ya puedes ver tu perfil innovador reflejado. ¿Quieres que te explique qué significa cada índice?",
            'informe_estrategico': f"Hola, soy Félix. El Informe Estratégico analiza con IA la posición competitiva de {sector}. Pulsa 'Generar Informe' y en unos segundos tendrás un análisis ejecutivo completo, descargable en Word y PDF. ¿Empezamos?",
            'informe_innovacion': f"Hola, soy Félix. Aquí verás el diagnóstico completo de innovación de {sector} por los 5 bloques y 19 subindicadores. ¿Quieres que te explique cómo interpretar los resultados?",
            'plan': f"Hola, soy Félix. El Plan de Acción generará 5 acciones prioritarias para {sector} y una hoja de ruta estratégica 1-3 años, totalmente personalizada con IA. ¿Lo generamos ahora?",
            'benchmarking': f"Hola, soy Félix. En Benchmarking puedes comparar {sector} con las empresas líderes del sector usando filtros por tamaño, región y exportación. ¿Te explico cómo sacarle partido?",
            'analytics': f"Hola, soy Félix. En Analytics encontrarás visualizaciones detalladas de todos los indicadores de {sector}. ¿En qué análisis quieres que te ayude?",
            'global': f"Hola, soy Félix. El Informe Global combina todos los diagnósticos de {sector} en un documento ejecutivo completo. ¿Quieres que te explique su estructura?",
        }
        msg = bienvenidas.get(pagina, f"Hola, soy Félix, tu consultor estratégico. Estoy aquí para ayudarte a interpretar los resultados de {sector} y navegar por la plataforma. ¿En qué puedo ayudarte?")
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
            st.session_state[key_msgs] = [{"role":"assistant","content":f"¡Hola de nuevo! ¿En qué puedo ayudarte con {sector}?"}]
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