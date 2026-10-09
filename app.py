import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="OntoMind v2.1", page_icon="🧠", layout="wide")

if "messages" not in st.session_state: st.session_state.messages = []
if "current_mode" not in st.session_state: st.session_state.current_mode = "Asistente del Coach"

with st.sidebar:
    st.title("OntoMind v2.1")
    st.caption("Proyecto Tecnico de Diplomado")
    nuevo_modo = st.selectbox("Selecciona el Modo:", ["Asistente del Coach", "Simulador de Coachee", "Supervision / Feedback"])
    if nuevo_modo != st.session_state.current_mode:
        st.session_state.current_mode = nuevo_modo
        st.session_state.messages = []
        st.rerun()
    st.divider()
    api_key = st.text_input("Introduce tu OpenAI API Key:", type="password")

PROMPT_MAESTRO = "Eres OntoMind v2.1, especialista en Coaching Ontologico. MODO: {modo}"
st.title(f"Modo Activo: {st.session_state.current_mode}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])

if prompt := st.chat_input("Escribe aqui..."):
    if not api_key: st.error("Introduce tu OpenAI API Key en la barra lateral."); st.stop()
    client = OpenAI(api_key=api_key)
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        res = st.write_stream(client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": PROMPT_MAESTRO.format(modo=st.session_state.current_mode)}] + st.session_state.messages,
            stream=True
        ))
    st.session_state.messages.append({"role": "assistant", "content": res})
