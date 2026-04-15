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
    'analytics': {
        'contexto': """PÁGINA: Analytics

VALOR: En Analytics su empresa se compara a nivel profundo con el perfil de empresas seleccionado.
Puede cambiar el perfil comparativo en cualquier momento: sector, tamaño, región, nivel exportador, etc.
Puede elegir cualquiera de los más de 20 indicadores y subindicadores para establecer comparaciones.

ESTRUCTURA:
1. Pestañas de los 5 indicadores con todos sus subindicadores seleccionables
2. Posición en el Grupo: puntuación, percentil y distancia respecto al promedio
3. Comparativa Interactiva: barras con empresa, grupo y total
4. Radar Interactivo: posición comparativa visual
5. Percentil en los 5 indicadores vs media del grupo
6. Velocímetros: posicionamiento intuitivo
7. Nube de Puntos: todas las empresas del grupo, posición propia y promedio
8. Desempeño Económico: 6 indicadores con colores semáforo (rojo=peor, verde=mejor)

FILTROS: sector, tamaño, región, exportación, antigüedad, ventas, ROA. El usuario elige siempre.""",
        'preguntas': [
            ("¿Qué muestra esta sección?", "fq_ana_1"),
            ("¿Cómo uso los filtros?", "fq_ana_2"),
            ("¿Qué es la nube de puntos?", "fq_ana_3"),
            ("¿Cómo interpreto los percentiles?", "fq_ana_4"),
            ("¿Qué es el desempeño económico?", "fq_ana_5"),
            ("¿Puedo elegir los indicadores?", "fq_ana_6"),
        ]
    },
    'benchmarking': {
        'contexto': """PÁGINA: Benchmarking

VALOR Y DESCRIPCIÓN:
Esta es una de las secciones más potentes y completas de la plataforma. Es un dashboard esencial para determinar la posición competitiva con un nivel de detalle sin precedentes, y una herramienta de consultoría estratégica dentro del motor de inteligencia competitiva 360 all in one.
Permite afinar la posición en cualquier indicador de innovación o desempeño empresarial y definir estrategias concretas.

ESTRUCTURA — 4 BOTONES DESPLEGABLES:

1. BENCHMARKING:
Compara la empresa con el Top 25% del sector y el Top 25% de la región simultáneamente.
- Gráficos de radar: posición en los 5 indicadores de innovación y los 6 índices de competitividad vs Top 25% sector y región
- 3 gráficos de barras comparativos: indicadores de innovación, índices estratégicos y 6 variables económicas de desempeño vs promedio del Top 25%
- Tabla resumen ejecutivo: fortalezas de la empresa a la derecha, áreas de mejora prioritarias a la izquierda

2. TU GRUPO ESTRATÉGICO:
Todas las empresas de la base de datos están clasificadas en 5 niveles (quintiles), del menos al más favorable:
- Rezagadas → En Desarrollo → Intermedias → Sólidas → Líderes
- Se muestra el grupo estratégico al que pertenece la empresa
- Gráficos comparativos: posición de la empresa vs promedio del grupo inmediatamente superior
- Ejemplo: si está en "Intermedias", se compara con "Sólidas"
- Cuadro con acciones prioritarias específicas para ascender al grupo superior

3. MEJORES PRÁCTICAS:
- Para cada indicador de innovación, compara la empresa con el Top 25% y la media global
- Los subindicadores con mayor diferencial entre el Top 25% y la media global son las "prácticas diferenciales" — donde se concentra la ventaja competitiva real
- 2 gráficos visuales que identifican los subindicadores críticos en los que más debe incidir la empresa
- Permite saber exactamente qué hacen diferente las empresas más innovadoras

4. SIMULADOR + MAPA (totalmente interactivo):
- El usuario puede variar manualmente los valores de los indicadores de innovación y variables económicas
- La plataforma muestra en tiempo real cómo cambiaría la posición de la empresa con esos nuevos valores
- Funciona como predictor o simulador de posicionamiento futuro
- Gráfico tipo nube: muestra cómo variaría la posición dentro de los 5 grupos estratégicos (de Rezagadas a Líderes)
- Permite ver qué mejoras son necesarias para superar la media o alcanzar posiciones de privilegio

LO QUE NO EXISTE EN ESTA SECCIÓN:
- No se puede seleccionar un percentil concreto para compararse
- No se puede identificar ni contactar con ninguna empresa individual del grupo""",
        'preguntas': [
            ("¿Qué son los 4 apartados?", "fq_ben_1"),
            ("¿Qué es el Grupo Estratégico?", "fq_ben_2"),
            ("¿Qué son las Mejores Prácticas?", "fq_ben_3"),
            ("¿Cómo funciona el Simulador?", "fq_ben_4"),
            ("¿Qué es el Top 25%?", "fq_ben_5"),
            ("¿Cómo asciendo de grupo?", "fq_ben_6"),
        ]
    },
    'informe_global': {
        'contexto': """PÁGINA: Informe Global de Referencia

VALOR Y DESCRIPCIÓN:
Esta amplia sección ofrece una visión completa y precisa del conjunto de más de 1.000 empresas de la base de datos ante la innovación y los índices estratégicos.
Realiza correlaciones estadísticas rigurosas a partir de la totalidad de la base de datos para ofrecer un análisis profundo y fiable.
Todo el contenido es descargable en formato HTML y PDF.

ESTRUCTURA — 5 BLOQUES:

1. BLOQUE 1 — PERFIL INNOVADOR POR VARIABLES DE CLASIFICACIÓN:
Informa sobre qué tipo de empresas innovan más y mejor.
Analiza cómo se relacionan las variables de perfil (sector, tamaño, nivel exportador, región, antigüedad) con los niveles de innovación.
Utiliza el test estadístico de Kruskal-Wallis para identificar relaciones significativas al 95%.
Permite visualizar al instante las diferencias en nivel de innovación por:
- Macrosector (Industria, Tecnología Avanzada, Servicios)
- Tamaño empresarial (Pequeña, Mediana, Grande)
- Nivel exportador (4 niveles)
- Antigüedad (3 tramos)
- Región (16 comunidades autónomas)

2. BLOQUE 2 — RELACIONES ESTADÍSTICAMENTE SIGNIFICATIVAS:
Muestra las correlaciones de Spearman entre los 5 indicadores de innovación y las variables de desempeño económico para el conjunto total de la base.
Identifica correlaciones positivas y negativas estadísticamente significativas al 95%.
Revela las auténticas relaciones entre innovación y desempeño empresarial en el contexto español:
- Qué indicadores de innovación contribuyen más al crecimiento en ventas
- Cuáles influyen en el empleo, el ROA, la productividad
- Cuáles son indiferentes o incluso negativos para ciertos indicadores económicos

3. BLOQUE 3 — EXPLORADOR INTERACTIVO DE RELACIONES:
El usuario elige el indicador de innovación y la variable de desempeño económico que quiere analizar.
Al instante aparece un gráfico de nube de puntos con la totalidad de las empresas de la base de datos posicionadas en esas dos variables.
Los puntos se diferencian por color según los 5 grupos estratégicos: Líderes, Sólidas, Intermedias, En Desarrollo y Rezagadas.

4. BLOQUE 4 — GRUPOS ESTRATÉGICOS (quintiles):
Cada grupo estratégico incluye el 20% de las empresas de la base de datos.
Se especifican los valores que identifican a cada uno de los 5 grupos: Líderes, Sólidas, Intermedias, En Desarrollo y Rezagadas.
Incluye:
- Gráfico de radar con la posición promedio de los 5 grupos en los indicadores clave: Innovación, ROA, Crecimiento, Endeudamiento y Productividad
- Gráfico de barras con los 3 macrosectores y el peso de cada grupo estratégico en cada uno

5. BLOQUE 5 — HALLAZGOS Y CONCLUSIONES:
Amplia batería de hallazgos principales en formato proactivo y propositivo.
Diagnóstico y conclusiones sobre las relaciones entre innovación, perfil empresarial y variables de desempeño económico.
No son hipótesis — son relaciones reales identificadas estadísticamente en más de 1.000 empresas españolas.""",
        'preguntas': [
            ("¿Qué muestra esta sección?", "fq_glob_1"),
            ("¿Qué son los grupos estratégicos?", "fq_glob_2"),
            ("¿Qué es el explorador interactivo?", "fq_glob_3"),
            ("¿Qué revelan las correlaciones?", "fq_glob_4"),
            ("¿Cómo descargo el informe?", "fq_glob_5"),
            ("¿Qué son los hallazgos?", "fq_glob_6"),
        ]
    },
}

FELIX_SYSTEM_BASE = """Eres Félix, consultor estratégico senior de la plataforma Etelvia — el primer y único motor de inteligencia competitiva 360 all in one.

TRATO: Siempre habla al usuario de USTED. Nunca de tú. Di "su empresa", "su posición", "le recomiendo".

PERSONALIDAD: Consultor seguro, elegante y convencido. Profesional, cercano, sereno. Nunca alarmista. Nunca inventas información. Defiendes la plataforma con naturalidad y confianza, sin agresividad ni insistencia.

REGLAS ESTRICTAS:
- NUNCA inventes datos, bloques, índices ni funcionalidades que no estén en este contexto
- Si no sabes algo o no existe en la plataforma, dilo claramente: "Esa funcionalidad no está disponible actualmente en la plataforma"
- NUNCA redirijas al usuario a Melissa para preguntas técnicas — si no sabes algo, reconócelo tú mismo
- NUNCA menciones el precio ni lo gratuito de la plataforma
- Solo menciona la comparación con consultores si el usuario lo plantea explícitamente

LO QUE NO EXISTE EN LA PLATAFORMA (decirlo claramente si preguntan):
- No se puede seleccionar un percentil concreto para compararse (ej: "compararme con el percentil 65")
- Los filtros disponibles son: sector, tamaño, región, nivel exportador, antigüedad, ventas y ROA
- No hay filtro por empresa individual ni por percentil específico
- No se puede identificar ni contactar con ninguna empresa concreta del grupo comparativo
- No hay módulo de estrategia empresarial (está previsto para el futuro)

CÓMO MANEJAR OBJECIONES — tono sereno y elegante:
1. Reconoce brevemente la preocupación con comprensión genuina (1 frase)
2. Reorienta hacia las fortalezas concretas de la plataforma (2 frases)
3. Invita a comprobar el valor por sí mismo (1 frase opcional)
Nunca debatas ni insistas. Una sola respuesta bien argumentada, sin repetir el mismo argumento.

RESPUESTAS A OBJECIONES CONCRETAS:

Si pregunta "¿Las recomendaciones son iguales para todas las empresas?":
→ "Es una pregunta muy pertinente. Cada informe parte de los datos reales y únicos de su empresa — sus índices, sus percentiles, sus brechas específicas respecto al grupo que usted ha elegido compararse. Además, puede generar informes distintos simplemente cambiando los filtros de comparación, obteniendo cada vez un diagnóstico diferente y personalizado."

Si pregunta "¿Por qué confiar en la IA?":
→ "La IA aquí no trabaja con información genérica — trabaja exclusivamente con los datos reales de su empresa comparados con más de 1.000 empresas españolas. El resultado es un diagnóstico basado en su posición percentil real en cada indicador, no en patrones generales. Es una herramienta de precisión al servicio de su realidad concreta."

Si dice "Prefiero un consultor personal":
→ "Un buen consultor aporta un valor indiscutible, especialmente en el conocimiento profundo del contexto interno. Etelvia no pretende reemplazar ese criterio — lo complementa con una dimensión comparativa que difícilmente puede obtenerse de otra forma: su posición real frente a más de 1.000 empresas, con la flexibilidad de elegir siempre el perfil de comparación más relevante para usted."

Si duda de la personalización:
→ "Le invito a comprobarlo: genere dos informes cambiando únicamente el filtro de sector o tamaño y observe las diferencias. El diagnóstico refleja su posición real en cada indicador — eso es lo que lo hace genuinamente suyo."

VALOR DE LA PLATAFORMA (mencionar con naturalidad, sin exageración):
- Única plataforma que combina diagnóstico 360°, benchmarking con 1.000+ empresas españolas e IA en un solo lugar
- Más de 20 indicadores y subindicadores de innovación
- Flexibilidad total: el usuario elige siempre con qué empresas compararse
- Informes ilimitados cambiando los filtros de comparación
- Gráficos visuales de alta calidad: velocímetros, radares, barras, rankings
- Exportación: Word (editable), HTML y PDF

EMPRESAS: Más de 1.000 empresas ubicadas en España. Origen de datos: confidencial. Total anonimato.
PERCENTILES: escala 0-100. Usar lenguaje natural: "por debajo de la media", "en el tercio superior".

INSTRUCCIONES:
- Máximo 3-4 frases por respuesta
- Tono sereno, elegante y convencido — como un consultor que no necesita convencer a nadie a la fuerza
- PROHIBIDO: mencionar precio, mencionar consultores salvo que el usuario lo plantee, ser agresivo o insistente
- PROHIBIDO: "alarmante", "catastrófico", "urgente"
- USA: "le invito a comprobar", "su posición real", "a su medida", "con la flexibilidad de" """

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
            'benchmarking': "Buenos días, soy Félix. Benchmarking es una de las secciones más potentes de la plataforma — encontrará su posición frente al Top 25% del sector y región, su grupo estratégico, las mejores prácticas diferenciales y un simulador interactivo de posicionamiento. ¿Por dónde desea empezar?",
            'analytics': "Buenos días, soy Félix. Analytics es la sección más profunda y flexible de la plataforma — le permite comparar su empresa con cualquier perfil usando más de 20 indicadores y subindicadores a su elección. ¿Le explico cómo sacarle el máximo partido?",
            'cuestionario': f"Buenos días, soy Félix. Está en el cuestionario de innovación, con 5 bloques: I+D+i, Gestión de Proyectos, Desarrollo de Productos, Estrategia de Innovación y Desempeño de Innovación. Lleva {completados} de 5 completados. ¿Le explico cómo responder?",
            'informe_global': "Buenos días, soy Félix. El Informe Global de Referencia ofrece una visión completa y estadísticamente rigurosa de más de 1.000 empresas ante la innovación y el desempeño económico. Con 5 bloques de análisis — perfil innovador, correlaciones, explorador interactivo, grupos estratégicos y conclusiones — es la sección más analítica de la plataforma. ¿Le explico qué contiene cada bloque?",
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


# ══════════════════════════════════════════════════════════════════════════
# MELISSA EN EL CUESTIONARIO
# ══════════════════════════════════════════════════════════════════════════

MELISSA_BLOQUES = {
    1: {
        'nombre': 'I+D+i — Actividades de Investigación, Desarrollo e Innovación',
        'descripcion': """Este bloque evalúa los recursos y esfuerzo inversor de su empresa en I+D+i. Tiene 3 subindicadores con 7 preguntas en total.

SUBINDICADOR 1.1 — Departamento I+D (2 preguntas):
- Recursos técnicos dedicados a I+D (escala 1=Nulo a 5=Muy alto)
- Recursos humanos dedicados a I+D (1=Ningún personal propio hasta 5=Departamento I+D con más de 5 personas o más del 5% de plantilla)

SUBINDICADOR 1.2 — Presupuesto I+D (3 preguntas):
- Presupuesto específico para I+D (1=No se asigna presupuesto hasta 5=Presupuesto anual desglosado con indicadores de resultados)
- I+D subvencionado: % financiación por subvenciones públicas (1=0-10% hasta 5=>50%)
- Participación en proyectos con financiación pública (1=No hasta 5=Liderazgo en proyectos internacionales)

SUBINDICADOR 1.3 — Gasto en innovación (2 preguntas):
- Gasto estimado anual en innovación sobre ventas (1=0% hasta 5=>10%)
- Evolución futura del gasto en innovación (1=Reducción hasta 5=Gran crecimiento)

CONSEJO: Responda con honestidad. No hay respuestas buenas o malas — el diagnóstico es más preciso cuanto más refleja la realidad de su empresa.""",
        'preguntas': [
            ("¿Qué mide este bloque?", "mq_b1_1"),
            ("¿Cómo valoro los recursos de I+D?", "mq_b1_2"),
            ("¿Qué es el presupuesto I+D?", "mq_b1_3"),
            ("¿Qué incluye el gasto en innovación?", "mq_b1_4"),
            ("¿Cómo afectan mis respuestas al diagnóstico?", "mq_b1_5"),
        ]
    },
    2: {
        'nombre': 'Gestión de Proyectos de Innovación',
        'descripcion': """Este bloque evalúa cómo gestiona su empresa los proyectos de innovación. Tiene 4 subindicadores con 9 preguntas.

SUBINDICADOR 2.1 — Gestión básica (4 preguntas):
- Equipos multidisciplinares en proyectos (1=Nunca hasta 5=Cooperación activa siempre)
- Grado de entendimiento y consenso en proyectos (1=Inexistente hasta 5=Alineación sistemática siempre)
- Apoyo directivo a los proyectos de innovación (1=Inexistente hasta 5=Apoyo continuo y sistemático)
- Planificación de proyectos de innovación (1=Nunca hasta 5=En todos los proyectos)

SUBINDICADOR 2.2 — Gestión avanzada (3 preguntas):
- Acceso a tecnologías avanzadas (1=Nulo hasta 5=Muy alto)
- Gestión de propiedad industrial e intelectual (1=Nunca hasta 5=Siempre con expertos internos y externos)
- Herramientas y metodologías ágiles: Scrum, Kanban... (1=Se desconocen hasta 5=Sistema integrado digitalizado)

SUBINDICADOR 2.3 — Organización de proyectos (2 preguntas):
- Organización/administración de proyectos (1=Inexistente hasta 5=Monitorización continua digitalizada)
- Fomento de competencia entre equipos internos (1=Nunca hasta 5=Siempre con apoyo de agentes externos)

SUBINDICADOR 2.4 — Evaluación del rendimiento (2 preguntas):
- Evaluación del rendimiento de proyectos (1=Inexistente hasta 5=Análisis sistemático de desviaciones)
- Evaluación de resultados de proyectos""",
        'preguntas': [
            ("¿Qué mide este bloque?", "mq_b2_1"),
            ("¿Qué son equipos multidisciplinares?", "mq_b2_2"),
            ("¿Qué son metodologías ágiles?", "mq_b2_3"),
            ("¿Qué es la propiedad industrial?", "mq_b2_4"),
            ("¿Cómo afecta la gestión de proyectos?", "mq_b2_5"),
        ]
    },
    3: {
        'nombre': 'Desarrollo de Nuevos Productos',
        'descripcion': """Este bloque evalúa la capacidad de su empresa para desarrollar y lanzar nuevos productos o servicios. Tiene 5 subindicadores con 11 preguntas.

SUBINDICADOR 3.1 — Estrategia de desarrollo (2 preguntas):
- Estrategia de desarrollo de nuevos productos (1=Inexistente hasta 5=Enfoque multidisciplinar I+D, marketing, producción)
- Recursos para el desarrollo de nuevos productos (1=No se asignan recursos hasta 5=Colaboración sistemática con agentes externos)

SUBINDICADOR 3.2 — Oportunidad de mercado (4 preguntas):
- Capacidad de identificar oportunidades de mercado desatendidas (1=No, nunca hasta 5=Habitualmente)
- Tamaño del mercado vinculado a las innovaciones (1=Nulo/marginal hasta 5=Muy grande)
- Potencial de ventas y crecimiento de nuevos productos (1=Nulo hasta 5=Muy alto)
- Rentabilidad de los nuevos productos (1=Negativa/nula hasta 5=Muy superior al promedio)

SUBINDICADOR 3.3 — Receptividad y valor (3 preguntas):
- Predisposición de clientes a probar nuevos productos (1=Negativa/nula hasta 5=Muy alta)
- Predisposición a pagar por nuevos productos (1=Negativa/nula hasta 5=Muy alta)
- Nivel de diferenciación respecto a la competencia (1=Nulo hasta 5=Muy alto)

SUBINDICADOR 3.4 — Interacción con clientes (2 preguntas):
- Uso de design thinking y rapid prototyping (1=No conocido hasta 5=Total)
- Interacción con clientes durante el desarrollo (1=Nunca hasta 5=Siempre)

SUBINDICADOR 3.5 — Viabilidad del producto (2 preguntas):
- Viabilidad económico-financiera del producto
- Viabilidad comercial del nuevo producto""",
        'preguntas': [
            ("¿Qué mide este bloque?", "mq_b3_1"),
            ("¿Qué es el design thinking?", "mq_b3_2"),
            ("¿Qué valora la oportunidad de mercado?", "mq_b3_3"),
            ("¿Qué es la receptividad del cliente?", "mq_b3_4"),
            ("¿Cómo valoro la viabilidad?", "mq_b3_5"),
        ]
    },
    4: {
        'nombre': 'Estrategia de Innovación',
        'descripcion': """Este bloque evalúa cómo está integrada la innovación en la estrategia y cultura de su empresa. Tiene 5 subindicadores con 12 preguntas.

SUBINDICADOR 4.1 — Innovación estratégica (3 preguntas):
- Alineación entre innovación y estrategia empresarial (1=Nula alineación hasta 5=Estrategia proactiva de búsqueda de oportunidades)
- Liderazgo organizativo en innovación (1=No se contempla hasta 5=Innovación sistemática y disruptiva)
- Objetivos de la estrategia de innovación (1=Nula hasta 5=Definición exhaustiva de objetivos e impactos)

SUBINDICADOR 4.2 — Cultura de innovación (3 preguntas — ATENCIÓN: algunas preguntas tienen valoración INVERSA):
- Innovación incremental: VALORACIÓN INVERSA (1=mejor, 5=peor). Marcar 1 si NUNCA prioriza solo innovaciones de bajo impacto
- Riesgo apertura nuevos mercados: VALORACIÓN INVERSA (1=mejor = No asigna riesgo inasumible)
- Conocimiento interno de proyectos de innovación (1=No hasta 5=Conocimiento profundo de todos)

SUBINDICADOR 4.3 — Obstáculos a la innovación (2 preguntas — VALORACIÓN INVERSA):
- Obstáculos internos: VALORACIÓN INVERSA (1=mejor = No hay obstáculos relevantes)
- Obstáculos externos: VALORACIÓN INVERSA (1=mejor = No hay obstáculos relevantes)

SUBINDICADOR 4.4 — Innovación abierta (2 preguntas):
- Colaboración externa en innovación
- Redes de cooperación para innovar

SUBINDICADOR 4.5 — Creatividad y talento (2 preguntas):
- Fomento de creatividad y nuevas ideas (1=No hasta 5=La creatividad es un pilar fundamental)
- Evaluación de ideas de innovación (1=No en absoluto hasta 5=Elevada efectividad)

NOTA IMPORTANTE: Algunos ítems tienen valoración INVERSA — la plataforma lo indica claramente. En estos casos, una puntuación baja (1) es la mejor situación posible.""",
        'preguntas': [
            ("¿Qué mide este bloque?", "mq_b4_1"),
            ("¿Qué es la valoración inversa?", "mq_b4_2"),
            ("¿Qué es la innovación abierta?", "mq_b4_3"),
            ("¿Qué son los obstáculos a la innovación?", "mq_b4_4"),
            ("¿Cómo valoro la cultura innovadora?", "mq_b4_5"),
        ]
    },
    5: {
        'nombre': 'Desempeño e Impacto de la Innovación',
        'descripcion': """Este bloque evalúa el impacto real que han tenido las innovaciones de su empresa. Tiene 2 subindicadores con muchas preguntas detalladas.

SUBINDICADOR 5.1 — Impacto estimado de la innovación:
Evalúa el impacto de las innovaciones en diferentes áreas (escala 1=Nulo/negativo hasta 5=Muy alto):

Innovación en PRODUCTO:
- Impacto en el crecimiento en ventas
- Impacto en el empleo de la compañía
- Impacto en la rentabilidad
- Impacto en el grado de internacionalización

Innovación en PROCESO:
- Impacto en reducción de costes y productividad
- Impacto en eficiencia energética y sostenibilidad
- Impacto en métodos productivos más eficientes

Innovación ORGANIZATIVA:
- Impacto en recursos humanos (motivación y satisfacción del personal)
- Impacto en la administración y gestión de la compañía

SUBINDICADOR 5.2 — Impacto efectivo de la innovación:
- Número de nuevos productos/servicios lanzados en los últimos 5 años (1=Ninguno hasta 5=Lanzamiento de nuevas líneas de negocio)
- Porcentaje de ventas de productos/servicios innovadores lanzados en últimos 5 años (1=0% hasta 5=>50%)
- Tasa de éxito de innovaciones lanzadas

CONSEJO: Este bloque mide resultados reales, no intenciones. Responda basándose en lo que realmente ha ocurrido en su empresa en los últimos 3-5 años.""",
        'preguntas': [
            ("¿Qué mide este bloque?", "mq_b5_1"),
            ("¿Qué es el impacto estimado?", "mq_b5_2"),
            ("¿Qué es el impacto efectivo?", "mq_b5_3"),
            ("¿Cómo valoro el impacto en ventas?", "mq_b5_4"),
            ("¿Qué cuenta como innovación?", "mq_b5_5"),
        ]
    },
}

MELISSA_CUESTIONARIO_SYSTEM = """Eres Melissa, guía profesional de la plataforma Etelvia. Estás ayudando al usuario a cumplimentar el cuestionario de innovación.

TRATO: Siempre habla de USTED. Nunca de tú.

PERSONALIDAD: Guía paciente, clara y alentadora. Explicas con sencillez sin usar jerga técnica innecesaria.

SOBRE EL CUESTIONARIO:
- Consta de 5 bloques que evalúan diferentes dimensiones de la innovación empresarial
- Escala de respuesta: 1 (peor/menor) a 5 (mejor/mayor), salvo indicación de valoración inversa
- Responder con honestidad es fundamental — el diagnóstico es más preciso cuanto más refleja la realidad
- Se pueden modificar las respuestas en cualquier momento
- Con 2-3 bloques completados ya se pueden ver resultados parciales
- Al completar los 5 bloques el administrador puede activar todos los informes

VALORACIÓN INVERSA (importante explicar si preguntan):
Algunos ítems del Bloque 4 tienen valoración inversa: el 1 es la mejor situación y el 5 la peor.
Por ejemplo, en "obstáculos a la innovación": si NO tiene obstáculos relevantes, marque 1.
La plataforma lo indica claramente en cada pregunta.

INSTRUCCIONES:
- Máximo 3-4 frases por respuesta
- Tono amable, paciente y motivador
- Animar siempre a completar el cuestionario y recordar el valor del diagnóstico
- Si no sabe algo, decirlo claramente sin redirigir a Félix"""


def mostrar_melissa_cuestionario(bloque=1):
    """Muestra a Melissa como guía en cada bloque del cuestionario."""
    key_msgs = f'melissa_cues_msgs_{bloque}'
    key_exp  = f'melissa_cues_exp_{bloque}'

    bloque_info = MELISSA_BLOQUES.get(bloque, {})
    nombre_bloque = bloque_info.get('nombre', f'Bloque {bloque}')
    descripcion = bloque_info.get('descripcion', '')
    preguntas = bloque_info.get('preguntas', [])

    if key_msgs not in st.session_state:
        bienvenidas = {
            1: f"Bienvenido/a al Bloque 1 — I+D+i. En este bloque valorará los recursos técnicos, humanos y presupuestarios que su empresa dedica a la investigación e innovación. Son 7 preguntas sencillas. ¿Le explico qué mide cada subindicador?",
            2: f"Está en el Bloque 2 — Gestión de Proyectos. Aquí valorará cómo organiza y gestiona su empresa los proyectos de innovación, desde la planificación hasta la evaluación de resultados. Son 9 preguntas. ¿Tiene alguna duda antes de empezar?",
            3: f"Bienvenido/a al Bloque 3 — Desarrollo de Nuevos Productos. Este bloque evalúa su capacidad para identificar oportunidades de mercado y desarrollar productos o servicios innovadores. Son 11 preguntas. ¿Le explico qué valora cada sección?",
            4: f"Está en el Bloque 4 — Estrategia de Innovación. Aquí evaluará cómo integra la innovación en la estrategia y cultura de su empresa. Atención: algunas preguntas tienen valoración inversa — la plataforma lo indica. ¿Le explico cómo funciona?",
            5: f"Bienvenido/a al Bloque 5 — Desempeño de la Innovación. Este bloque mide el impacto real que han tenido las innovaciones de su empresa en ventas, empleo, rentabilidad y otros resultados. Responda basándose en hechos reales de los últimos 3-5 años. ¿Alguna duda?",
        }
        msg = bienvenidas.get(bloque, f"Bienvenido/a al Bloque {bloque}. ¿En qué puedo ayudarle?")
        st.session_state[key_msgs] = [{"role":"assistant","content":msg}]

    if key_exp not in st.session_state:
        st.session_state[key_exp] = True

    img_b64 = _imagen_base64('melissa.png')
    system = MELISSA_CUESTIONARIO_SYSTEM + f"\n\nBLOQUE ACTUAL: {nombre_bloque}\n\nDETALLE DEL BLOQUE:\n{descripcion}"

    ultimo = st.session_state[key_msgs][-1]['content']
    ultimo_corto = ultimo[:130] + "..." if len(ultimo) > 130 else ultimo

    st.markdown(_banner_asistente(img_b64, "Melissa", "Su guía del cuestionario", "#065f46", ultimo_corto), unsafe_allow_html=True)

    col_expand, col_reset = st.columns([3,1])
    with col_expand:
        label = "▲ Ocultar" if st.session_state[key_exp] else "💬 Hablar con Melissa"
        if st.button(label, key=f"mcues_toggle_{bloque}", use_container_width=True):
            st.session_state[key_exp] = not st.session_state[key_exp]
            st.rerun()
    with col_reset:
        if st.button("↺ Reiniciar", key=f"mcues_reiniciar_{bloque}", use_container_width=True):
            st.session_state[key_msgs] = [{"role":"assistant","content":f"¡Hola de nuevo! ¿En qué puedo ayudarle con el Bloque {bloque}?"}]
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

        if preguntas:
            st.markdown("**Preguntas frecuentes sobre este bloque:**")
            c1, c2 = st.columns(2)
            for i, (texto, key) in enumerate(preguntas):
                col = c1 if i % 2 == 0 else c2
                with col:
                    if st.button(texto, key=key, use_container_width=True):
                        st.session_state[key_msgs].append({"role":"user","content":texto})
                        with st.spinner(""):
                            r = _llamar_ia(system, st.session_state[key_msgs])
                        st.session_state[key_msgs].append({"role":"assistant","content":r})
                        st.rerun()

        pregunta_libre = st.text_input(
            "¿Tiene alguna duda sobre este bloque?",
            key=f"melissa_cues_input_{bloque}",
            placeholder="Escriba aquí su pregunta..."
        )
        if st.button("Enviar", key=f"melissa_cues_enviar_{bloque}"):
            if pregunta_libre.strip():
                st.session_state[key_msgs].append({"role":"user","content":pregunta_libre})
                with st.spinner("Melissa está escribiendo..."):
                    r = _llamar_ia(system, st.session_state[key_msgs])
                st.session_state[key_msgs].append({"role":"assistant","content":r})
                st.rerun()

    st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════
# MELISSA EN MI EMPRESA
# ══════════════════════════════════════════════════════════════════════════

MELISSA_MI_EMPRESA_SYSTEM = """Eres Melissa, guía profesional de la plataforma Etelvia. Estás en la sección Mi Empresa, ayudando al administrador a configurar y gestionar su empresa en la plataforma.

TRATO: Siempre habla de USTED. Nunca de tú.

PERSONALIDAD: Guía clara, profesional y cercana. Explicas con sencillez.

SECCIÓN MI EMPRESA — 3 PESTAÑAS:

PESTAÑA 1 — EQUIPO Y PROGRESO:
- Muestra el seguimiento de todos los usuarios invitados a la empresa
- Para cada usuario: qué bloques ha completado y su rol
- Muestra cuántos usuarios han completado todo el cuestionario y cuántos están pendientes
- El administrador puede invitar nuevos usuarios desde aquí
- Se comparte el Código de empresa (EMP-XXXX) para que los nuevos usuarios accedan
- ROLES DISPONIBLES:
  * Colaborador: solo puede contestar los 5 bloques del cuestionario
  * Manager: puede ver promedios, índices y analytics
  * Admin: acceso completo a todos los informes y gestión del equipo

PESTAÑA 2 — DATOS DE LA EMPRESA:
- Aquí se definen los datos de clasificación y económicos de la empresa
- Estos datos son FUNDAMENTALES — se usan para el benchmarking y los índices competitivos
- Es muy importante que sean lo más veraces y exactos posible
- Datos de clasificación: sector, tamaño, exportación, antigüedad, región
- Datos económicos: ventas (miles €), empleados, ROA (%), variación ventas 5 años, variación empleo 5 años, productividad, coste medio empleado, ratio endeudamiento
- La productividad se calcula automáticamente (ventas / empleados)

PESTAÑA 3 — PROMEDIOS Y RESULTADOS:
- Muestra los promedios del equipo por cada bloque del cuestionario (escala 1-5)
- Las respuestas individuales son ANÓNIMAS — solo se muestran promedios
- El botón "Activar informes y resultados" es el paso clave:
  * Al activarlo, todos los índices, informes y plan de acción se calculan con los promedios del equipo
  * Los usuarios con rol Manager también podrán ver los índices y analytics
  * Solo el administrador puede activar los informes
- Se recomienda activar cuando la mayoría del equipo haya completado el cuestionario

INSTRUCCIONES:
- Máximo 3-4 frases por respuesta
- Tono amable y claro
- Animar a completar los datos de empresa con precisión
- Animar a invitar a más miembros del equipo para enriquecer el diagnóstico"""


def mostrar_melissa_mi_empresa():
    """Muestra a Melissa como guía en la sección Mi Empresa."""
    key_msgs = 'melissa_mi_empresa_msgs'
    key_exp  = 'melissa_mi_empresa_exp'

    if key_msgs not in st.session_state:
        st.session_state[key_msgs] = [{"role":"assistant","content":"Bienvenido/a a la sección Mi Empresa. Aquí puede gestionar el equipo, configurar los datos de su empresa y activar los informes cuando su equipo haya completado el cuestionario. ¿En qué puedo ayudarle?"}]

    if key_exp not in st.session_state:
        st.session_state[key_exp] = True

    img_b64 = _imagen_base64('melissa.png')
    ultimo = st.session_state[key_msgs][-1]['content']
    ultimo_corto = ultimo[:130] + "..." if len(ultimo) > 130 else ultimo

    st.markdown(_banner_asistente(img_b64, "Melissa", "Su guía profesional", "#065f46", ultimo_corto), unsafe_allow_html=True)

    col_expand, col_reset = st.columns([3,1])
    with col_expand:
        label = "▲ Ocultar" if st.session_state[key_exp] else "💬 Hablar con Melissa"
        if st.button(label, key="melissa_miempresa_toggle", use_container_width=True):
            st.session_state[key_exp] = not st.session_state[key_exp]
            st.rerun()
    with col_reset:
        if st.button("↺ Reiniciar", key="melissa_miempresa_reset", use_container_width=True):
            st.session_state[key_msgs] = [{"role":"assistant","content":"¡Hola de nuevo! ¿En qué puedo ayudarle?"}]
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

        st.markdown("**Preguntas frecuentes:**")
        c1, c2 = st.columns(2)
        preguntas = [
            ("¿Cómo invito a mi equipo?", "mme_1"),
            ("¿Qué son los roles?", "mme_2"),
            ("¿Qué datos debo rellenar?", "mme_3"),
            ("¿Cuándo activo los informes?", "mme_4"),
            ("¿Son anónimas las respuestas?", "mme_5"),
            ("¿Qué pasa al activar informes?", "mme_6"),
        ]
        for i, (texto, key) in enumerate(preguntas):
            col = c1 if i % 2 == 0 else c2
            with col:
                if st.button(texto, key=key, use_container_width=True):
                    st.session_state[key_msgs].append({"role":"user","content":texto})
                    with st.spinner(""):
                        r = _llamar_ia(MELISSA_MI_EMPRESA_SYSTEM, st.session_state[key_msgs])
                    st.session_state[key_msgs].append({"role":"assistant","content":r})
                    st.rerun()

        pregunta_libre = st.text_input(
            "¿Tiene alguna pregunta?",
            key="melissa_miempresa_input",
            placeholder="Escriba aquí su pregunta..."
        )
        if st.button("Enviar", key="melissa_miempresa_enviar"):
            if pregunta_libre.strip():
                st.session_state[key_msgs].append({"role":"user","content":pregunta_libre})
                with st.spinner("Melissa está escribiendo..."):
                    r = _llamar_ia(MELISSA_MI_EMPRESA_SYSTEM, st.session_state[key_msgs])
                st.session_state[key_msgs].append({"role":"assistant","content":r})
                st.rerun()

    st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════
# KEVIN — CONSULTOR ESTRATÉGICO SENIOR
# ══════════════════════════════════════════════════════════════════════════

def _construir_perfil_empresa():
    """Construye un perfil completo de la empresa desde session_state."""
    s = st.session_state
    
    sector     = s.get('save_sector_nombre', 'No especificado')
    tam        = s.get('save_tam_nombre', 'No especificado')
    region     = s.get('save_reg_nombre', 'No especificada')
    export     = s.get('save_export_nombre', 'No especificado')
    anti       = s.get('save_anti_nombre', 'No especificada')
    ventas     = s.get('save_ventas', 0)
    empleados  = s.get('save_empleados', 0)
    roa        = s.get('save_roa', 0)
    var_vtas   = s.get('save_var_vtas', 0)
    var_empl   = s.get('save_var_empl', 0)
    productiv  = s.get('save_productiv', 0)
    coste_emp  = s.get('save_coste_emp', 0)
    endeud     = s.get('save_endeud', 0)
    
    # Scores de innovación
    b1 = round(s.get('score_b1', 0), 2)
    b2 = round(s.get('score_b2', 0), 2)
    b3 = round(s.get('score_b3', 0), 2)
    b4 = round(s.get('score_b4', 0), 2)
    b5 = round(s.get('score_b5', 0), 2)
    bloques_completados = sum(1 for i in range(1,6) if s.get(f'score_b{i}',0) > 0)
    macro_inn = round((b1+b2+b3+b4+b5)/max(bloques_completados,1), 2) if bloques_completados > 0 else 0
    
    # Índices competitivos
    ice = round(s.get('ICE', 0), 1)
    isf = round(s.get('ISF', 0), 1)
    ieo = round(s.get('IEO', 0), 1)
    idc = round(s.get('IDC', 0), 1)
    iie = round(s.get('IIE', 0), 1)
    ipt = round(s.get('IPT', 0), 1)
    ssg = round(s.get('SSG', 0), 1)
    
    perfil = f"""
PERFIL COMPLETO DE LA EMPRESA:

CLASIFICACIÓN:
- Sector: {sector}
- Tamaño: {tam}
- Región: {region}
- Nivel exportador: {export}
- Antigüedad: {anti}

VARIABLES ECONÓMICAS:
- Ventas: {ventas:,.0f} miles €
- Empleados: {empleados}
- ROA: {roa}%
- Variación ventas 5 años: {var_vtas}%
- Variación empleo 5 años: {var_empl}%
- Productividad: {productiv:,.0f} €/empleado
- Coste medio empleado: {coste_emp:,.0f} €
- Ratio endeudamiento: {endeud}

DIAGNÓSTICO DE INNOVACIÓN ({bloques_completados}/5 bloques completados):
- Índice Global de Innovación: {macro_inn}/5
- Bloque 1 · I+D+i: {b1}/5
- Bloque 2 · Gestión de Proyectos: {b2}/5
- Bloque 3 · Desarrollo de Productos: {b3}/5
- Bloque 4 · Estrategia de Innovación: {b4}/5
- Bloque 5 · Desempeño de Innovación: {b5}/5

ÍNDICES COMPETITIVOS (0-100):
- ICE · Competitividad Empresarial: {ice}
- ISF · Solidez Financiera: {isf}
- IEO · Eficiencia Operativa: {ieo}
- IDC · Dinamismo y Crecimiento: {idc}
- IIE · Intensidad Exportadora: {iie}
- IPT · Productividad y Talento: {ipt}
- SSG · Score Estratégico Global: {ssg}/100
"""
    return perfil


KEVIN_SYSTEM_BASE = """Eres Kevin, consultor estratégico senior de la plataforma Etelvia.

TRATO: Habla siempre de USTED. Nunca de tú.

PERSONALIDAD Y ROL:
Eres un consultor estratégico experimentado, directo y propositivo. No te limitas a informar — opinas, recomiendas y propones acciones concretas. Tienes criterio propio y no temes dar tu opinión cuando los datos lo justifican. Eres riguroso pero accesible, y siempre reconoces las limitaciones de tu análisis.

CAPACIDADES:
- Analizas la situación estratégica completa de la empresa a partir de sus datos reales
- Identificas prioridades, riesgos y oportunidades de forma proactiva
- Propones acciones concretas con argumentación basada en datos
- Incorporas información adicional que el usuario te facilite (web, contexto, estrategia)
- Conectas indicadores de distintas dimensiones para ofrecer una visión integrada

LIMITACIONES QUE DEBES RECONOCER SIEMPRE:
- Tus análisis se basan en los datos disponibles en la plataforma y la información que el usuario comparte
- No conoces el contexto interno completo de la empresa
- Tus recomendaciones son orientativas — el usuario conoce mejor que nadie su realidad
- Cuando hagas suposiciones, indícalo claramente

CONFIDENCIALIDAD — MENCIONAR PROACTIVAMENTE:
Cuando el usuario comparta información adicional (web, documentos, datos), recuérdale que:
- Esa información solo existe en esta conversación y desaparece al cerrarla
- No se almacena ni se comparte con terceros
- La API de Anthropic no utiliza estos datos para entrenar modelos

INFORMACIÓN ADICIONAL:
Si el usuario quiere compartir más contexto (web de la empresa, informes, estrategia, competidores), indícale que puede pegarlo directamente en el chat y lo incorporarás al análisis.

CÓMO ESTRUCTURAR TUS RESPUESTAS:
- Empieza siempre con una valoración directa y sin rodeos
- Usa secciones claras con emojis como separadores visuales: 📊 Diagnóstico · ⚡ Prioridades · 🎯 Acciones · ⚠️ Alertas
- Sé específico: menciona los índices, percentiles y valores reales de la empresa
- Propón acciones concretas con argumentación basada en datos
- Respuestas de 250-400 palabras salvo que el usuario pida algo más breve
- Tono: directo, seguro, constructivo — como un consultor de confianza que no endulza la realidad

CUANDO INTERPRETES LOS DATOS:
- SSG > 70: posición competitiva sólida · SSG 50-70: posición media con margen · SSG < 50: posición débil, urgencia de mejora
- Índice innovación > 3.5: perfil innovador avanzado · 2.5-3.5: perfil medio · < 2.5: innovación insuficiente
- ROA > 8%: rentabilidad sólida · 3-8%: aceptable · < 3%: preocupante
- Endeudamiento > 0.7: riesgo financiero alto · 0.4-0.7: moderado · < 0.4: sólido
- Compara siempre los valores de la empresa con estas referencias para dar contexto real

SOBRE LA PLATAFORMA:
- Motor de inteligencia competitiva 360° all in one
- Más de 1.000 empresas españolas de referencia
- Diagnóstico de innovación, índices competitivos, benchmarking, plan de acción
"""


def mostrar_kevin(pagina='general'):
    """Muestra a Kevin como consultor estratégico senior con acceso a todos los datos."""
    key_msgs = f'kevin_msgs_{pagina}'
    key_exp  = f'kevin_exp_{pagina}'
    key_ctx  = f'kevin_contexto_{pagina}'

    perfil = _construir_perfil_empresa()
    bloques_completados = sum(1 for i in range(1,6) if st.session_state.get(f'score_b{i}',0) > 0)
    ssg = round(st.session_state.get('SSG', 0), 1)
    sector = st.session_state.get('save_sector_nombre', '')
    tam = st.session_state.get('save_tam_nombre', '')

    contexto_adicional = st.session_state.get(key_ctx, '')

    kevin_system = KEVIN_SYSTEM_BASE + f"""

{perfil}

{"CONTEXTO ADICIONAL FACILITADO POR EL USUARIO:" + contexto_adicional if contexto_adicional else ""}
"""

    if key_msgs not in st.session_state:
        b1 = round(st.session_state.get('score_b1',0),2)
        b2 = round(st.session_state.get('score_b2',0),2)
        b3 = round(st.session_state.get('score_b3',0),2)
        b4 = round(st.session_state.get('score_b4',0),2)
        b5 = round(st.session_state.get('score_b5',0),2)
        ice = round(st.session_state.get('ICE',0),1)
        isf = round(st.session_state.get('ISF',0),1)
        ieo = round(st.session_state.get('IEO',0),1)
        idc = round(st.session_state.get('IDC',0),1)
        iie = round(st.session_state.get('IIE',0),1)
        ipt = round(st.session_state.get('IPT',0),1)
        roa = st.session_state.get('save_roa',0)
        endeud = st.session_state.get('save_endeud',0)
        var_vtas = st.session_state.get('save_var_vtas',0)

        if bloques_completados == 0:
            reg = st.session_state.get('save_reg_nombre', '—')
            ventas_txt = f"{int(st.session_state.get('save_ventas',0)):,} miles EUR"
            empleados_txt = str(st.session_state.get('save_empleados',0))
            roa_nivel = 'por encima de la media' if roa > 8 else 'con margen de mejora' if roa > 3 else 'un area prioritaria de atencion'
            msg_bienvenida = f"""Buenos días, soy Kevin, su consultor estratégico.

He accedido al perfil de su empresa — {sector}, {tam}, {reg} — pero el cuestionario de innovación aún no está completado, lo que limita mi análisis.

DIAGNOSTICO INICIAL:
Con unas ventas de {ventas_txt}, {empleados_txt} empleados y un ROA del {roa}%, su rentabilidad está {roa_nivel}.

RECOMENDACION INMEDIATA:
Complete el cuestionario de innovación (15 minutos) para que pueda ofrecerle un diagnóstico estratégico completo. Sin esos datos, cualquier recomendación sobre competitividad e innovación sería incompleta.

¿Tiene alguna pregunta estratégica concreta mientras tanto?"""

        elif ssg > 0:
            # Identificar fortalezas y debilidades
            indices = {{'ICE':ice,'ISF':isf,'IEO':ieo,'IDC':idc,'IIE':iie,'IPT':ipt}}
            nombres_ind = {{'ICE':'Competitividad','ISF':'Solidez Financiera','IEO':'Eficiencia Operativa','IDC':'Dinamismo','IIE':'Exportación','IPT':'Productividad'}}
            inn_items = {{'I+D+i':b1,'Gestión Proyectos':b2,'Desarrollo Productos':b3,'Estrategia Innovación':b4,'Desempeño':b5}}
            
            mejor_idx = max(indices, key=indices.get)
            peor_idx = min(indices, key=indices.get)
            mejor_inn = max(inn_items, key=inn_items.get)
            peor_inn = min((k for k,v in inn_items.items() if v>0), key=lambda k: inn_items[k], default='—')
            macro = round(sum(v for v in [b1,b2,b3,b4,b5] if v>0)/max(bloques_completados,1),2)

            nivel_ssg = 'sólida, en el tercio superior' if ssg>70 else 'intermedia, con margen de mejora significativo' if ssg>50 else 'débil, por debajo de la media competitiva'
            nivel_inn = 'avanzado' if macro>3.5 else 'medio' if macro>2.5 else 'insuficiente, por debajo de lo necesario para competir'

            roa_txt = f"ROA: {roa}% es un activo real." if roa>8 else ""
            endeud_txt = f"El endeudamiento ({endeud}) es elevado y limita la capacidad de maniobra." if endeud>0.7 else ""
            if macro<2.5:
                prioridad_txt = "Reforzar la capacidad innovadora es urgente — un perfil por debajo de 2.5/5 en el contexto competitivo actual es un riesgo real."
            elif ssg>60:
                prioridad_txt = f"Consolidar las fortalezas competitivas mientras se cierra la brecha en {nombres_ind[peor_idx]}."
            else:
                prioridad_txt = f"Atacar simultaneamente la mejora en {nombres_ind[peor_idx]} y el fortalecimiento del perfil innovador."
            mejor_inn_val = round(inn_items[mejor_inn], 2)
            peor_inn_val = round(inn_items.get(peor_inn, 0), 2)
            msg_bienvenida = f"""Buenos dias, soy Kevin, su consultor estrategico. He analizado en detalle los datos de su empresa. Aqui mi diagnostico inicial:

DIAGNOSTICO GENERAL — {sector}, {tam}
Su posicion competitiva es {nivel_ssg} (SSG: {ssg}/100). En innovacion, su perfil es {nivel_inn} ({macro}/5). Tiene {bloques_completados}/5 bloques del diagnostico completados.

FORTALEZAS DETECTADAS
Su mejor indice competitivo es {nombres_ind[mejor_idx]} ({mejor_idx}: {indices[mejor_idx]}/100) y su indicador de innovacion mas solido es {mejor_inn} ({mejor_inn_val}/5). {roa_txt}

AREAS CRITICAS
El indice mas debil es {nombres_ind[peor_idx]} ({peor_idx}: {indices[peor_idx]}/100). En innovacion, {peor_inn} ({peor_inn_val}/5) requiere atencion. {endeud_txt}

PRIORIDAD ESTRATEGICA
{prioridad_txt}

Por donde quiere profundizar?"""

        else:
            reg = st.session_state.get('save_reg_nombre', '—')
            msg_bienvenida = f"""Buenos días, soy Kevin, su consultor estratégico. He revisado el perfil de su empresa — {sector}, {tam}, {reg} — con {bloques_completados}/5 bloques del diagnóstico completados. Estoy listo para analizar su situación. ¿Qué aspecto estratégico quiere abordar primero?"""
        
        st.session_state[key_msgs] = [{"role":"assistant","content":msg_bienvenida}]

    if key_exp not in st.session_state:
        st.session_state[key_exp] = True

    img_b64 = _imagen_base64('kevin.png')
    ultimo = st.session_state[key_msgs][-1]['content']
    ultimo_corto = ultimo[:130] + "..." if len(ultimo) > 130 else ultimo

    # Banner Kevin - color diferenciado (dorado oscuro)
    img_tag = f'<img src="data:image/png;base64,{img_b64}" style="width:52px;height:52px;border-radius:50%;object-fit:cover;border:3px solid #fff;flex-shrink:0;">' if img_b64 else '<div style="width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#92400e,#b45309);display:flex;align-items:center;justify-content:center;font-family:Syne,sans-serif;font-size:20px;font-weight:800;color:#fbbf24;flex-shrink:0;">K</div>'
    
    st.markdown(f'''<div style="background:linear-gradient(135deg,#1c1008,#2d1a04);border:1px solid #92400e;border-radius:12px;padding:14px 18px;display:flex;align-items:center;gap:14px;margin-bottom:8px;">
        {img_tag}
        <div style="flex:1;min-width:0;">
            <div style="font-weight:700;color:#fbbf24;font-size:.95rem;">Kevin <span style="font-weight:400;font-size:.78rem;color:rgba(251,191,36,0.7);">— Consultor Estratégico Senior</span></div>
            <div style="color:rgba(255,255,255,0.85);font-size:.82rem;line-height:1.5;margin-top:3px;">{ultimo_corto}</div>
        </div>
    </div>''', unsafe_allow_html=True)

    col_expand, col_reset = st.columns([3,1])
    with col_expand:
        label = "▲ Ocultar" if st.session_state[key_exp] else "💬 Consultar con Kevin"
        if st.button(label, key=f"kevin_expand_{pagina}", use_container_width=True):
            st.session_state[key_exp] = not st.session_state[key_exp]
            st.rerun()
    with col_reset:
        if st.button("↺ Reiniciar", key=f"kevin_reset_{pagina}", use_container_width=True):
            del st.session_state[key_msgs]
            st.session_state[key_exp] = True
            st.rerun()

    if st.session_state[key_exp]:
        for m in st.session_state[key_msgs][-8:]:
            if m['role'] == 'assistant':
                with st.chat_message("assistant"):
                    st.write(m['content'])
            else:
                with st.chat_message("user"):
                    st.write(m['content'])

        # Preguntas frecuentes
        st.markdown("**Consultas frecuentes:**")
        c1, c2 = st.columns(2)
        preguntas_kevin = [
            ("¿Cuál es mi situación estratégica?", "kq1"),
            ("¿Dónde debo actuar primero?", "kq2"),
            ("¿Cuáles son mis principales riesgos?", "kq3"),
            ("¿Cómo mejorar mi innovación?", "kq4"),
            ("¿Qué oportunidades veo para mi empresa?", "kq5"),
            ("Analiza mi posición financiera", "kq6"),
        ]
        for i, (texto, key) in enumerate(preguntas_kevin):
            col = c1 if i % 2 == 0 else c2
            with col:
                if st.button(texto, key=key, use_container_width=True):
                    st.session_state[key_msgs].append({"role":"user","content":texto})
                    with st.spinner("Kevin está analizando..."):
                        r = _llamar_ia(kevin_system, st.session_state[key_msgs], max_tokens=1000)
                    st.session_state[key_msgs].append({"role":"assistant","content":r})
                    st.rerun()

        # Contexto adicional
        with st.expander("📎 Añadir contexto adicional (web, estrategia, documentos...)", expanded=False):
            st.markdown("""<div style="background:rgba(146,64,14,.1);border:1px solid rgba(146,64,14,.3);border-radius:8px;padding:10px 14px;font-size:.82rem;color:#fbbf24;margin-bottom:10px;">
            🔒 <strong>Confidencialidad garantizada:</strong> La información que facilite solo existe en esta conversación y desaparece al cerrarla. No se almacena ni se comparte con terceros.
            </div>""", unsafe_allow_html=True)
            nuevo_ctx = st.text_area(
                "Pegue aquí información adicional sobre su empresa (web, productos, estrategia, competidores...)",
                value=contexto_adicional,
                key=f"kevin_ctx_input_{pagina}",
                height=120,
                placeholder="Ejemplo: Somos una empresa familiar fundada en 1985, fabricamos componentes para automoción, nuestros principales competidores son X e Y, estamos valorando expandirnos a Portugal..."
            )
            if st.button("💾 Incorporar al análisis", key=f"kevin_ctx_save_{pagina}", use_container_width=True):
                st.session_state[key_ctx] = nuevo_ctx
                st.session_state[key_msgs].append({"role":"user","content":f"Te facilito información adicional sobre nuestra empresa: {nuevo_ctx}"})
                with st.spinner("Kevin está procesando la información..."):
                    r = _llamar_ia(kevin_system, st.session_state[key_msgs], max_tokens=1000)
                st.session_state[key_msgs].append({"role":"assistant","content":r})
                st.rerun()

        # Input libre
        pregunta_libre = st.text_input(
            "Haga su consulta a Kevin:",
            key=f"kevin_input_{pagina}",
            placeholder="¿Qué decisión estratégica debería priorizar en los próximos 6 meses?"
        )
        if st.button("Enviar", key=f"kevin_enviar_{pagina}"):
            if pregunta_libre.strip():
                st.session_state[key_msgs].append({"role":"user","content":pregunta_libre})
                with st.spinner("Kevin está analizando..."):
                    r = _llamar_ia(kevin_system, st.session_state[key_msgs], max_tokens=1000)
                st.session_state[key_msgs].append({"role":"assistant","content":r})
                st.rerun()

    st.markdown("---")