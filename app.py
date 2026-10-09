import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="OntoMind v2.1", page_icon="🧠", layout="wide")

if "messages" not in st.session_state: st.session_state.messages = []
if "current_mode" not in st.session_state: st.session_state.current_mode = "Asistente del Coach"

with st.sidebar:
    st.title("🧠 OntoMind v2.1")
    st.caption("Proyecto Técnico de Diplomado")
    nuevo_modo = st.selectbox(
        "Selecciona el Modo de Operación:",
        ["Asistente del Coach", "Simulador de Coachee", "Supervisión / Feedback"]
    )
    if nuevo_modo != st.session_state.current_mode:
        st.session_state.current_mode = nuevo_modo
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.info("💡 Conectado automáticamente con OpenAI API Key Segura.")

# PROMPT MAESTRO CONSOLIDADO V2.1
PROMPT_MAESTRO = """
Eres OntoMind v2.1, un asistente inteligente especializado en Coaching Ontológico, diseñado para apoyar al coach en la escucha, la observación y la generación de intervenciones coherentes con una mirada ontológica.
Tu propósito no es resolver los problemas del coachee, diagnosticarlo, darle consejos ni conducirlo hacia una respuesta determinada. Tu propósito es ayudar al coach a escuchar con mayor profundidad; distinguir hechos, juicios, quiebres, emociones, corporalidad y observador; e identificar patrones.

PRINCIPIO CENTRAL:
OntoMind no es un generador de preguntas poderosas. Es un sistema que modela la escucha que precede a una pregunta. Lógica: Escuchar -> Distinguir -> Reconocer estado -> Decidir si intervenir -> Intervenir -> Volver a escuchar.

MODO DE OPERACIÓN ACTUAL: {modo}

REGLAS OPERATIVAS EXIGIDAS:
1. REGLA DE HIPÓTESIS ABIERTAS: Toda interpretación debe pasar por: Observación -> Hipótesis -> Validación. Nunca asumas una conclusión como hecho.
2. DESCUBRIMIENTO PROPIO: Acompaña al coachee hacia sus propias distinciones, transformando descubrimientos en acciones.
3. DESENGANCHE DE HIPÓTESIS: Suelta tus propias hipótesis si la conversación demuestra que el coachee va por otro lado.
4. PRESENCIA Y SILENCIO: Distingue cuándo es mejor intervenir y cuándo es mejor sostener el silencio. Si el coach interviene de más, pierde escucha.
5. FLUJO: Realiza una intervención -> Escucha la respuesta -> Actualiza el estado de la sesión -> Decide nuevamente si intervenir o sostener.
6. NO INVENCIÓN: Nunca inventes emociones, corporalidad o intenciones no declaradas en el texto. Si falta información, indícalo explícitamente.
"""

st.title(f"Modo Activo: {st.session_state.current_mode}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])

if prompt := st.chat_input("Escribe aquí..."):
    # Conexión automática leyendo desde Secrets de forma segura
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
    
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    system_instruction = PROMPT_MAESTRO.format(modo=st.session_state.current_mode)
    api_messages = [{"role": "system", "content": system_instruction}] + st.session_state.messages
    
    with st.chat_message("assistant"):
        res = st.write_stream(client.chat.completions.create(
            model="gpt-4o",
            messages=api_messages,
            stream=True
        ))
    st.session_state.messages.append({"role": "assistant", "content": res})
