"""
Módulo de asistentes virtuales — Félix y Melissa
Importar en cada página con:
    from asistentes import mostrar_melissa, mostrar_felix
"""
import streamlit as st
from asistentes import mostrar_melissa
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
    """Carga imagen de assets como base64."""
    base = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(base, 'assets', nombre)
    if not os.path.exists(ruta):
        ruta = os.path.join('/mount/src/nuevo-bidin/assets', nombre)

    if os.path.exists(ruta):
        with open(ruta, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return None

def _llamar_ia(system_prompt, messages, max_tokens=600):
    api_key = _get_api_key()
    if not api_key:
        return "Lo siento, no puedo responder en este momento."
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type":"application/json","x-api-key":api_key,"anthropic-version":"2023-06-01"},
            json={"model":"claude-sonnet-4-20250514","max_tokens":max_tokens,
                  "system": system_prompt,
                  "messages": messages},
            timeout=30
        )
        data = resp.json()
        if data.get('content'): return data['content'][0]['text']
        return "Lo siento, no puedo responder en este momento."
    except Exception:
        return "Lo siento, no puedo responder en este momento."

def _css_asistentes():
    return """
<style>
.asistente-overlay {
    position: fixed; bottom: 0; right: 20px; z-index: 9999;
    display: flex; flex-direction: column; align-items: flex-end;
}
.asistente-btn {
    width: 64px; height: 64px; border-radius: 50%;
    border: 3px solid #ffffff; cursor: pointer;
    overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    transition: transform 0.2s;
}
.asistente-btn:hover { transform: scale(1.08); }
.asistente-btn img { width: 100%; height: 100%; object-fit: cover; }
.chat-panel {
    background: #ffffff; border-radius: 16px 16px 0 16px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.18);
    width: 360px; max-height: 520px;
    display: flex; flex-direction: column;
    overflow: hidden; margin-bottom: 8px;
    border: 1px solid #e2e8f0;
}
.chat-header {
    padding: 14px 16px; display: flex; align-items: center; gap: 10px;
}
.chat-header img {
    width: 44px; height: 44px; border-radius: 50%; object-fit: cover;
    border: 2px solid rgba(255,255,255,0.5);
}
.chat-header-info h4 { margin:0; font-size:.92rem; font-weight:700; color:#ffffff; }
.chat-header-info p  { margin:0; font-size:.72rem; color:rgba(255,255,255,0.8); }
.chat-messages {
    flex: 1; overflow-y: auto; padding: 14px;
    background: #f8fafc; display: flex; flex-direction: column; gap: 10px;
    max-height: 320px;
}
.msg-asistente {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 12px 12px 12px 2px;
    padding: 10px 14px; font-size:.85rem; color:#1e293b;
    line-height: 1.6; max-width: 90%; align-self: flex-start;
}
.msg-usuario {
    background: #1e40af; color: #ffffff;
    border-radius: 12px 12px 2px 12px;
    padding: 10px 14px; font-size:.85rem;
    line-height: 1.6; max-width: 90%; align-self: flex-end;
}
.chat-input-area {
    padding: 10px 12px; background: #ffffff;
    border-top: 1px solid #e2e8f0;
    display: flex; gap: 8px; align-items: center;
}
.quick-btns {
    padding: 8px 12px; background: #f8fafc;
    border-top: 1px solid #e2e8f0;
    display: flex; gap: 6px; flex-wrap: wrap;
}
.quick-btn {
    background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe;
    border-radius: 20px; padding: 4px 12px; font-size:.75rem;
    cursor: pointer; white-space: nowrap;
}
.quick-btn:hover { background: #dbeafe; }
</style>
"""

# ══════════════════════════════════════════════════════════════════════════════
# MELISSA — Guía de bienvenida
# ══════════════════════════════════════════════════════════════════════════════
MELISSA_SYSTEM = """Eres Melissa, guía profesional de la plataforma de Diagnóstico Estratégico 360°.
Tu rol es dar la bienvenida al usuario, explicarle las funcionalidades de la plataforma y guiarle para empezar.

PERSONALIDAD: Profesional, clara, cercana pero seria. Directiva experimentada que conoce perfectamente la plataforma.

SOBRE LA PLATAFORMA:
- Es el único motor de inteligencia competitiva de su clase a nivel internacional
- Permite realizar diagnósticos 360° en múltiples áreas estratégicas de la empresa
- Compara la empresa con más de 1.000 empresas auditadas de referencia
- Genera índices, informes, benchmarking sectorial y planes de acción personalizados con IA
- TOTAL ANONIMATO: los datos individuales nunca se divulgan ni comparten
- Tiempo estimado para el cuestionario de innovación: 10-15 minutos

SECCIONES DE LA PLATAFORMA:
1. Registro Empresa: el admin crea la empresa y obtiene un código único
2. Acceso: todos los usuarios entran con email + código de empresa
3. Mi Empresa: el admin gestiona el equipo, asigna roles, ve promedios y activa los informes
4. Cuestionario de Innovación: 5 bloques (I+D+i, Gestión Proyectos, Desarrollo Productos, Estrategia Innovación, Desempeño Innovación)
5. Índices Estratégicos: 6 índices competitivos (ICE, ISF, IEO, IDC, IIE, IPT) + Score Global SSG
6. Informes: Estratégico, de Innovación, Global — con análisis de IA
7. Analytics, Benchmarking y Plan de Acción

ROLES:
- Admin: gestiona el equipo, ve promedios del equipo, activa informes
- Manager: ve índices, analytics y promedios
- Colaborador: solo cumplimenta los cuestionarios

INSTRUCCIONES:
- Respuestas máximo 3-4 frases, claras y directas
- Usa lenguaje profesional pero accesible
- Anima siempre a empezar por Registro Empresa si es nuevo
- Si ya tiene cuenta, anima a completar el cuestionario
- Nunca inventes información que no esté en este contexto"""

def mostrar_melissa():
    """Muestra el asistente Melissa en la página de Inicio."""
    img_b64 = _imagen_base64('melissa.png')
    img_src = f"data:image/png;base64,{img_b64}" if img_b64 else ""

    # Inicializar estado
    if 'melissa_abierto' not in st.session_state:
        st.session_state['melissa_abierto'] = True
    if 'melissa_msgs' not in st.session_state:
        st.session_state['melissa_msgs'] = [
            {"role": "assistant", "content": "¡Bienvenido/a a la plataforma de Diagnóstico Estratégico 360°! Soy Melissa, tu guía profesional. Esta plataforma es un motor de inteligencia competitiva único que te permitirá conocer el posicionamiento real de tu empresa comparado con más de 1.000 empresas. ¿Te explico cómo empezar?"}
        ]

    st.markdown(_css_asistentes(), unsafe_allow_html=True)

    # Panel de chat
    if st.session_state['melissa_abierto']:
        msgs_html = ""
        for m in st.session_state['melissa_msgs']:
            css = "msg-asistente" if m['role'] == 'assistant' else "msg-usuario"
            msgs_html += f'<div class="{css}">{m["content"]}</div>'

        header_color = "#065f46"
        st.markdown(f"""
        <div style="position:fixed;bottom:80px;right:20px;z-index:9998;width:360px;">
          <div class="chat-panel">
            <div class="chat-header" style="background:{header_color};">
              {'<img src="'+img_src+'" alt="Melissa"/>' if img_src else '<div style="width:44px;height:44px;border-radius:50%;background:#10b981;"></div>'}
              <div class="chat-header-info">
                <h4>Melissa</h4>
                <p>Tu guía profesional</p>
              </div>
              <div style="margin-left:auto;color:rgba(255,255,255,0.7);cursor:pointer;font-size:1.2rem;" onclick="document.getElementById('melissa-panel').style.display='none'">×</div>
            </div>
            <div class="chat-messages" id="melissa-msgs">{msgs_html}</div>
            <div class="quick-btns">
              <span class="quick-btn" id="qb1">¿Cómo empiezo?</span>
              <span class="quick-btn" id="qb2">¿Qué obtengo?</span>
              <span class="quick-btn" id="qb3">¿Son seguros mis datos?</span>
              <span class="quick-btn" id="qb4">¿Qué son los roles?</span>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Input del usuario
    col_input, col_btn_cerrar = st.columns([4,1])
    with col_input:
        user_input = st.text_input("Pregunta a Melissa", key="melissa_input",
                                   placeholder="Escribe tu pregunta...",
                                   label_visibility="collapsed")
    with col_btn_cerrar:
        if st.button("✕", key="melissa_cerrar", help="Cerrar Melissa"):
            st.session_state['melissa_abierto'] = False
            st.rerun()

    # Botones rápidos
    col1, col2, col3, col4 = st.columns(4)
    preguntas_rapidas = {
        "¿Cómo empiezo?": col1,
        "¿Qué obtengo?": col2,
        "¿Mis datos?": col3,
        "¿Los roles?": col4,
    }
    for pregunta, col in preguntas_rapidas.items():
        with col:
            if st.button(pregunta, key=f"melissa_q_{pregunta}", use_container_width=True):
                user_input = pregunta

    # Procesar input
    if user_input and user_input.strip():
        st.session_state['melissa_msgs'].append({"role":"user","content":user_input})
        with st.spinner("Melissa está escribiendo..."):
            respuesta = _llamar_ia(MELISSA_SYSTEM, st.session_state['melissa_msgs'])
        st.session_state['melissa_msgs'].append({"role":"assistant","content":respuesta})
        st.rerun()

    # Botón para reabrir si está cerrado
    if not st.session_state['melissa_abierto']:
        if img_src:
            st.markdown(f"""
            <div style="position:fixed;bottom:20px;right:20px;z-index:9999;">
              <div class="asistente-btn" title="Hablar con Melissa">
                <img src="{img_src}" alt="Melissa"/>
              </div>
            </div>
            """, unsafe_allow_html=True)
        if st.button("💬 Melissa — Guía profesional", key="melissa_reabrir"):
            st.session_state['melissa_abierto'] = True
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# FÉLIX — Consultor estratégico
# ══════════════════════════════════════════════════════════════════════════════
def _felix_system(pagina_actual=""):
    sector = st.session_state.get('save_sector_nombre','tu sector')
    tam    = st.session_state.get('save_tam_nombre','')
    reg    = st.session_state.get('save_reg_nombre','')
    b1 = st.session_state.get('score_b1', 0)
    b2 = st.session_state.get('score_b2', 0)
    b3 = st.session_state.get('score_b3', 0)
    b4 = st.session_state.get('score_b4', 0)
    b5 = st.session_state.get('score_b5', 0)
    bloques_completados = sum(1 for b in [b1,b2,b3,b4,b5] if b > 0)

    contexto_empresa = f"""
EMPRESA: {sector} | {tam} | {reg}
BLOQUES COMPLETADOS: {bloques_completados}/5
SCORES: B1={b1:.2f} B2={b2:.2f} B3={b3:.2f} B4={b4:.2f} B5={b5:.2f}
PÁGINA ACTUAL: {pagina_actual}
"""
    return f"""Eres Félix, consultor estratégico senior de la plataforma de Diagnóstico Estratégico 360°.

PERSONALIDAD: Consultor profesional, amable y cercano de unos 35 años. Experto en competitividad e innovación empresarial. Directo, preciso, constructivo. Nunca alarmista.

CONTEXTO DE LA EMPRESA:
{contexto_empresa}

TU COMPORTAMIENTO:
- Cuando el usuario llega a una nueva sección, salúdale proactivamente y explica qué encontrará
- Si hay bloques sin completar, anímale a completarlos con argumentos concretos
- Cuando expliques índices o resultados, usa lenguaje descriptivo (NO "percentil 13", sí "por debajo de la media del sector")
- Personaliza siempre tus respuestas con el sector y datos de la empresa
- Si los informes no están activados, explica que el admin debe activarlos desde Mi Empresa

MENSAJES DE BIENVENIDA POR SECCIÓN (úsalos como base):
- Índices Estratégicos: "Aquí puedes ver tu posición competitiva real en 6 dimensiones clave. Con {bloques_completados} bloques completados, los índices ya reflejan tu perfil innovador. ¿Quieres que te explique qué significa cada índice?"
- Informe Estratégico: "Este informe analiza tu posición competitiva global con inteligencia artificial. Primero pulsa 'Generar Informe' y en 20 segundos tendrás un análisis completo. ¿Empezamos?"
- Informe Innovación: "Aquí verás tu diagnóstico detallado de innovación por bloques y subindicadores. ¿Quieres entender cómo se interpreta?"
- Plan & Ruta: "Este es uno de los documentos más valiosos — un plan de acción de 12 meses y una hoja de ruta 1-3 años totalmente personalizada. ¿Generamos el plan ahora?"
- Cuestionario: "Estás en el cuestionario de innovación. Cada bloque tiene entre 3 y 5 preguntas sencillas en escala del 1 al 5. Llevas {bloques_completados} de 5 completados. ¿Continuamos?"

INSTRUCCIONES:
- Respuestas máximo 3-4 frases
- Tono consultor senior, nunca genérico
- Siempre ofrece ayuda adicional al final
- PROHIBIDO: "alarmante", "catastrófico", "urgente", "excelente"
- USA: "margen de mejora", "posición sólida", "área prioritaria", "ventaja competitiva" """

def mostrar_felix(pagina=""):
    """Muestra el asistente Félix en páginas de resultados."""
    img_b64 = _imagen_base64('felix.png')
    img_src = f"data:image/png;base64,{img_b64}" if img_b64 else ""

    # Inicializar estado
    key_abierto = f'felix_abierto_{pagina}'
    key_msgs = f'felix_msgs_{pagina}'
    key_saludo = f'felix_saludado_{pagina}'

    if key_abierto not in st.session_state:
        st.session_state[key_abierto] = True
    if key_msgs not in st.session_state:
        # Mensaje de bienvenida contextual
        b1 = st.session_state.get('score_b1', 0)
        b2 = st.session_state.get('score_b2', 0)
        b3 = st.session_state.get('score_b3', 0)
        b4 = st.session_state.get('score_b4', 0)
        b5 = st.session_state.get('score_b5', 0)
        completados = sum(1 for b in [b1,b2,b3,b4,b5] if b > 0)
        sector = st.session_state.get('save_sector_nombre','tu empresa')

        bienvenidas = {
            'indices': f"Hola, soy Félix. Estás en **Índices Estratégicos**, donde puedes ver la posición competitiva de {sector} en 6 dimensiones clave. Tienes {completados} de 5 bloques completados. ¿Quieres que te explique qué significa cada índice y cómo interpretarlos?",
            'informe_estrategico': f"Hola, soy Félix. El **Informe Estratégico** analiza con IA la posición competitiva global de {sector}. Pulsa 'Generar Informe' y en unos segundos tendrás un análisis ejecutivo completo. ¿Empezamos?",
            'informe_innovacion': f"Hola, soy Félix. Este es el **Informe de Innovación** de {sector}, con análisis detallado por los 5 bloques del cuestionario. ¿Quieres que te explique cómo interpretar los indicadores?",
            'plan': f"Hola, soy Félix. Estás en el **Plan de Acción y Hoja de Ruta** — uno de los documentos más valiosos de la plataforma. Generará 5 acciones prioritarias para {sector} más una hoja de ruta 1-3 años. ¿Generamos el plan ahora?",
            'benchmarking': f"Hola, soy Félix. En el **Benchmarking** puedes comparar {sector} con las empresas líderes de tu sector. ¿Quieres que te explique cómo usar los filtros para compararte con empresas similares a la tuya?",
            'analytics': f"Hola, soy Félix. En **Analytics** encontrarás visualizaciones detalladas de todos tus indicadores. ¿Quieres que te explique qué análisis son más relevantes para {sector}?",
        }
        msg_inicial = bienvenidas.get(pagina, f"Hola, soy Félix, tu consultor estratégico. Estoy aquí para ayudarte a sacar el máximo partido de esta sección. ¿En qué puedo ayudarte?")
        st.session_state[key_msgs] = [{"role":"assistant","content": msg_inicial}]

    st.markdown(_css_asistentes(), unsafe_allow_html=True)

    # Panel flotante
    if st.session_state[key_abierto]:
        msgs_html = ""
        for m in st.session_state[key_msgs][-6:]:  # últimos 6 mensajes
            css = "msg-asistente" if m['role'] == 'assistant' else "msg-usuario"
            msgs_html += f'<div class="{css}">{m["content"]}</div>'

        st.markdown(f"""
        <div style="position:fixed;bottom:80px;right:20px;z-index:9998;width:360px;">
          <div class="chat-panel">
            <div class="chat-header" style="background:#1e3a5f;">
              {'<img src="'+img_src+'" alt="Félix"/>' if img_src else '<div style="width:44px;height:44px;border-radius:50%;background:#2563eb;"></div>'}
              <div class="chat-header-info">
                <h4>Félix</h4>
                <p>Tu asesor estratégico</p>
              </div>
            </div>
            <div class="chat-messages">{msgs_html}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Input y controles
    col_input, col_cerrar = st.columns([4,1])
    with col_input:
        user_input = st.text_input("Pregunta a Félix", key=f"felix_input_{pagina}",
                                   placeholder="Pregunta a Félix...",
                                   label_visibility="collapsed")
    with col_cerrar:
        label = "▼ Cerrar" if st.session_state[key_abierto] else "💬 Félix"
        if st.button(label, key=f"felix_toggle_{pagina}"):
            st.session_state[key_abierto] = not st.session_state[key_abierto]
            st.rerun()

    # Procesar input
    if user_input and user_input.strip():
        st.session_state[key_msgs].append({"role":"user","content":user_input})
        with st.spinner("Félix está analizando..."):
            respuesta = _llamar_ia(_felix_system(pagina), st.session_state[key_msgs])
        st.session_state[key_msgs].append({"role":"assistant","content":respuesta})
        st.rerun()
        mostrar_melissa()